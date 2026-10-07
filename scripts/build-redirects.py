#!/usr/bin/env python3
"""Prepare static GitHub Pages redirects; --check never writes files."""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent


def page(target, unknown=False):
    expression = "'https://besz.me' + window.location.pathname" if unknown else json.dumps(target)
    script = f'window.location.replace({expression} + window.location.search + window.location.hash);'
    fallback = html.escape(target, quote=True)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>This page has moved — Agnieszka Besz</title>
<link rel="canonical" href="{fallback}">
<script>{script}</script>
<meta http-equiv="refresh" content="0;url={fallback}">
</head>
<body>
<p>This page has moved to <a href="{fallback}">besz.me</a>.</p>
</body>
</html>
'''


def outputs():
    routes = json.loads((ROOT / 'redirects.json').read_text())
    for path, target in routes.items():
        if (not path.endswith('.html') or path.startswith('/')
                or any(part in ('', '.', '..') for part in path.split('/'))):
            raise ValueError(f'Unsafe redirect path: {path}')
        url = urlsplit(target)
        if url.scheme != 'https' or url.netloc != 'besz.me' or url.query or url.fragment:
            raise ValueError(f'Unexpected destination: {target}')
    result = {path: page(target) for path, target in routes.items()}
    result['404.html'] = page('https://besz.me/', unknown=True)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, content in outputs().items():
        file = ROOT / path
        if args.check:
            if not file.exists() or file.read_text() != content:
                parser.exit(1, f'Regenerate redirect: {path}\n')
        else:
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content)
    print('Validated redirects' if args.check else 'Generated redirects')
