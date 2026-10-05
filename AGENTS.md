# Repository agent guide

Read README.md and docs/AI_CONTEXT.md before changes. Preserve user-owned changes. Follow aixaCode/repo-template general conventions and Conventional Commits without scopes.

- `site/`: editable recovered besz.me source, including HTML, CSS, JS, fonts, images, SVG diagrams and CV PDF.
- Root HTML: legacy GitHub Pages content; do not replace during source preparation.
- `scripts/build-site.py`: dependency-free build and local reference checks.
- `public/` and `release-manifest.json`: committed generated publish files; rebuild from source and commit together, never edit by hand.
- `dist/`: ignored local release archive.
- `docs/BESZ_*`: migration audit and pending decisions.

Commands: `python3 scripts/build-site.py --check`; `python3 scripts/build-site.py`; preview with `python3 -m http.server 8080 --bind 127.0.0.1 --directory public`.

Versioning uses the continuous-deployment profile: commit SHA plus artifact SHA-256. Keep secrets and host credentials out of source and output. Never execute repository-supplied code on the deployer host. User requires approval at every migration step; pushes and deployment are not part of source preparation.

## Existing-repository exceptions

The repo currently uses main and working branches; development/promotion branches and protection have not been configured. Preserve this flow during migration preparation; changes to GitHub settings need separate approval. The migration branch starts at main to avoid mixing unreconciled local writing changes. Recovered HTML is the initial source because the original generator was unavailable; shared templates and content extraction require a later behavior-preserving conversion. This is a documented intermediate baseline, not the final editing architecture.

## Editorial source map

- content/essays.json: title, description and original publication date inventory.
- content/page-updates.json: deliberate content update dates; never stamp deploy dates.
- design/diagrams.json and scripts/render-diagrams.py: shared editable diagram source.
- design/IMAGE_PROVENANCE.md: artwork provenance and generation prompt.
- scripts/content-metadata.py: generated reading times, RSS, sitemap and cache hashes.
- scripts/render-cv.py: PDF from the public HTML CV, optional pinned ReportLab authoring tool.
- test/content-test.py: metadata/reference regression checks.

Update the source hash in content/cv-pdf-source.sha256 only after regenerating and
visually reviewing the PDF. No production build runs image generation or external
content scripts; it publishes the reviewed assets already committed in site/.
