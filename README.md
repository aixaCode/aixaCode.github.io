# besz.me website

Migration source for the static website hosted on Proxmox. The existing root HTML remains the legacy GitHub Pages site during migration; the recovered redesign lives under `site/`.

## Local workflow

Requires Python 3.9 or newer; no packages or network access are needed.

```sh
python3 scripts/build-site.py --check
python3 scripts/build-site.py
python3 -m http.server 8080 --bind 127.0.0.1 --directory public
```

Open http://127.0.0.1:8080. Edit `site/`, then rebuild and refresh. Generated `public/` and `dist/` are ignored. The build validates local links, fragments and responsive image references, copies source bytes unchanged, and creates a deterministic `dist/site.tar`, SHA-256 file and file manifest. The archive contains only website files; deployment metadata is a sidecar.

## Version control and deployment

Continuous-deployment profile: the eventual release identity is the immutable Git commit SHA plus artifact SHA-256. No version tags are needed. This migration branch is `feat/besz-source`, based on local main at bf8113b; the existing dirty `writing-first` checkout is preserved separately.

CI configuration is prepared to validate and upload a static artifact, but has not been pushed or executed on GitHub. It does not publish or deploy. CT 116 website-deployer and CT 126 hosting changes require separate approval. GitHub Pages remains untouched until the new release is verified and redirects are approved.

See `docs/AI_CONTEXT.md`, `docs/DECISIONS.md`, and the migration/content/visual reviews. Content and image recommendations remain pending; recovery does not resolve those issues or restore the missing RSS feed.
