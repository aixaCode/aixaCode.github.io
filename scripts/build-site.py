#!/usr/bin/env python3
"""Build a deterministic static release with generated editorial metadata."""
import argparse
import importlib.util
import hashlib
import io
import json
import shutil
import tarfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SOURCE = (ROOT / 'site').resolve()
OUTPUT = ROOT / 'public'
DIST = ROOT / 'dist'
spec = importlib.util.spec_from_file_location('metadata', ROOT / 'scripts/content-metadata.py')
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.refs.append(attrs[key])
        for item in attrs.get('srcset', '').split(','):
            if item.strip():
                self.refs.append(item.strip().split()[0])


def inventory():
    expected = (ROOT / 'content/cv-pdf-source.sha256').read_text().strip()
    actual = hashlib.sha256((SOURCE / 'cv.html').read_bytes()).hexdigest()
    if expected != actual:
        raise ValueError('HTML CV changed: regenerate and review its PDF before building')
    files = sorted(p for p in SOURCE.rglob('*') if p.is_file())
    for path in SOURCE.rglob('*'):
        if path.is_symlink():
            raise ValueError(f'Symlink is not allowed: {path.relative_to(SOURCE)}')
        if path.relative_to(SOURCE).as_posix() != '.nojekyll' and any(part.startswith('.') for part in path.relative_to(SOURCE).parts):
            raise ValueError(f'Hidden file is not allowed: {path.relative_to(SOURCE)}')
    if not files or not (SOURCE / 'index.html').is_file():
        raise ValueError('Source must include index.html')
    return files


def check(files, root=SOURCE, generated=True):
    source = root.resolve()
    pages = {}
    for path in files:
        if path.suffix == '.html':
            page = Page()
            page.feed(path.read_text())
            pages[path.resolve()] = page
    errors = []
    for path, page in pages.items():
        for ref in page.refs:
            url = urlsplit(ref)
            if url.scheme or url.netloc:
                continue
            target = (source / unquote(url.path).lstrip('/') if url.path.startswith('/')
                      else path.parent / unquote(url.path)) if url.path else path
            target = target.resolve()
            if not target.is_relative_to(source):
                errors.append(f'{path.relative_to(source)}: reference escapes source: {ref}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if generated and target == (source / 'feed.xml').resolve():
                continue
            if not target.is_file():
                errors.append(f'{path.relative_to(source)}: missing {ref}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{path.relative_to(source)}: missing anchor {ref}')
    if errors:
        raise ValueError('\n'.join(errors))
    print(f'Checked {len(pages)} pages and {len(files)} files')


def build(files):
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir()
    essays = metadata.inventory()
    for path in files:
        relative = path.relative_to(SOURCE)
        destination = OUTPUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = path.read_bytes()
        if path.suffix == '.html':
            data = metadata.page_metadata(data.decode(), essays, relative.as_posix()).encode()
        destination.write_bytes(data)
    for name, data in metadata.outputs(essays, [p.relative_to(SOURCE).as_posix() for p in files]).items():
        (OUTPUT / name).write_bytes(data)
    check(sorted(p for p in OUTPUT.rglob('*') if p.is_file()), OUTPUT, generated=False)
    records = []
    for destination in sorted(p for p in OUTPUT.rglob('*') if p.is_file()):
        relative = destination.relative_to(OUTPUT)
        data = destination.read_bytes()
        records.append({'path': relative.as_posix(), 'bytes': len(data),
                        'sha256': hashlib.sha256(data).hexdigest()})
    DIST.mkdir(exist_ok=True)
    archive = DIST / 'site.tar'
    with tarfile.open(archive, 'w', format=tarfile.USTAR_FORMAT) as tar:
        for record in records:
            data = (OUTPUT / record['path']).read_bytes()
            info = tarfile.TarInfo(record['path'])
            info.size = len(data)
            info.mode = 0o644
            info.mtime = 0
            info.uid = info.gid = 0
            tar.addfile(info, io.BytesIO(data))
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (DIST / 'site.tar.sha256').write_text(f'{checksum}  site.tar\n')
    (DIST / 'manifest.json').write_text(json.dumps({'schema': 1, 'artifact_sha256': checksum,
                                                   'files': records}, indent=2) + '\n')
    # Sidecar stays outside the published tree. The trusted receiver recreates the
    # same deterministic tar from committed public/ bytes and checks this inventory.
    (ROOT / 'release-manifest.json').write_bytes((DIST / 'manifest.json').read_bytes())
    print(f'Built public/ and dist/site.tar ({checksum})')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate without generating output')
    args = parser.parse_args()
    try:
        files = inventory()
        check(files)
        if not args.check:
            build(files)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')
