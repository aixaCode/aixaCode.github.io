# besz.me website

Migration source for the static website hosted on Proxmox. The existing root HTML remains the legacy GitHub Pages site during migration; the recovered redesign lives under `site/`.

## Local workflow

Requires Python 3.9 or newer; no packages or network access are needed.

```sh
python3 scripts/build-site.py --check
python3 scripts/build-site.py
python3 -m http.server 8080 --bind 127.0.0.1 --directory public
```

Open http://127.0.0.1:8080. Edit `site/`, then rebuild and refresh. Commit generated `public/` and `release-manifest.json` alongside each source change. `dist/` remains ignored. Never edit publish files by hand. The build validates local links, fragments and responsive image references, derives essay metadata/reading times, RSS and sitemap, and creates a deterministic `dist/site.tar`, SHA-256 file and file manifest. The archive contains only website files; deployment metadata is a sidecar.

## Version control and deployment

Continuous-deployment profile: the eventual release identity is the immutable Git commit SHA plus artifact SHA-256. No version tags are needed. This migration branch is `feat/besz-source`, based on local main at bf8113b; the existing dirty `writing-first` checkout is preserved separately.

The previously pushed source passed GitHub CI. CI now also rebuilds and checks that committed publish files match source; the new Git publishing preparation remains local until approved. CT 116 has the prior deployment components and CT 126 has a restricted receiver installed, with the besz target disabled. The proposed Git path uses a read-only SSH deploy key and publishes committed static files without a GitHub Actions token. GitHub Pages remains untouched until the new release is verified and redirects are approved.

See `docs/AI_CONTEXT.md`, `docs/DECISIONS.md`, and the migration/content/visual reviews. Step 6 applies the recorded editorial and visual fixes locally. RSS is restored; unconfirmed claims are listed in docs/BESZ_STEP6_REVIEW.md.

## Editing and regenerating editorial assets

Essay titles, descriptions and original publication dates live in
`content/essays.json`; body text remains in `site/posts/`. The build derives reading
times from body text at 220 words/minute, excluding navigation and figure captions.
It applies the same values to article bylines, Home and Writing cards, and generates
RSS and sitemap. Record real page update dates in `content/page-updates.json`;
deployment never advances those dates automatically.

`python3 scripts/render-diagrams.py` regenerates all v4 SVGs from
`design/diagrams.json` with no external packages. Long desktop flows use stacked
cards to keep their labels readable. Source assets and generated web assets are
both committed; the ordinary static build does not regenerate illustrations.

Optional authoring tools are separate from the production build:

- `pip install -r scripts/requirements-authoring.txt`, then
  `python3 scripts/render-cv.py` regenerates the two-page PDF from the HTML CV.
- `npm ci`, then `npm run social-cards` renders the native SVG/JPEG share cards.
- See `design/IMAGE_PROVENANCE.md` for image sources, the built-in generation
  prompt and exported variant paths. Keep originals outside public output.

Run `python3 test/content-test.py` and the build after changes. Updating the HTML
CV requires regenerating its PDF in the same reviewed change. CI checks the HTML
source hash in content/cv-pdf-source.sha256 so that a changed CV requires PDF regeneration. The hash is an editing guard,
not proof of visual correctness; review the regenerated pages before committing.
