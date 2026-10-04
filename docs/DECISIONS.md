# Decisions

## 2026-10-04: Recover a byte-preserving baseline

Keep the recovered deployed files under `site/` and generate output into ignored directories. The original generator was not recoverable; introducing templates and Markdown immediately would mix reconstruction with pending editorial decisions. Preserve exact page paths, assets and source bytes first; extract shared templates in a separately reviewed conversion.

## 2026-10-04: Isolate migration work

Use `feat/besz-source` in a separate local checkout so the staged and unstaged writing-first work remains intact. Commit the local source baseline; do not merge, push or configure deployment during this step. Root legacy files remain for later redirect work.

## 2026-10-04: Separate build from deployment

Use Python standard library tooling and deterministic tar metadata. Prepare CI validation/artifacts only. Website-deployer must consume validated artifacts and a trusted destination rather than run arbitrary repository code. Dedicated deployment authorization and identity will be handled in the next approved step.
