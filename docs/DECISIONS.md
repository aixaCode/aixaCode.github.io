# Decisions

## 2026-10-04: Recover a byte-preserving baseline

Keep the recovered deployed files under `site/` and generate output into ignored directories. The original generator was not recoverable; introducing templates and Markdown immediately would mix reconstruction with pending editorial decisions. Preserve exact page paths, assets and source bytes first; extract shared templates in a separately reviewed conversion.

## 2026-10-04: Isolate migration work

Use `feat/besz-source` in a separate local checkout so the staged and unstaged writing-first work remains intact. Commit the local source baseline; do not merge, push or configure deployment during this step. Root legacy files remain for later redirect work.

## 2026-10-04: Separate build from deployment

Use Python standard library tooling and deterministic tar metadata. Prepare CI validation/artifacts only. Website-deployer must consume validated artifacts and a trusted destination rather than run arbitrary repository code. Dedicated deployment authorization and identity will be handled in the next approved step.

## 2026-10-05: Generate editorial metadata and editable diagrams

Use content/essays.json for original publication dates and descriptions, body-only
reading times, RSS and sitemap. Keep actual page update dates explicit. Generate
SVG variants from a single graph specification and shared palette; use pixel-width
wrapping and larger mobile labels instead of compressing all meaning into a tiny
box. Long desktop flows stack to preserve readability. Keep versioned asset names
because production caches images for 30 days.

The HTML CV is the source for PDF regeneration; a recorded source hash prevents
ordinary edits from silently leaving its PDF stale. ReportLab and Sharp are optional
pinned authoring tools, not dependencies of the static production build. Generated
image provenance and the final prompt remain in Git outside the public output.

## 2026-10-06: Publish committed static files over SSH Git

Match the other sites' read-only Git deploy-key model. Commit generated public/
and release-manifest.json together with source; keep dist/ ignored. CI rebuilds
and fails on changed or untracked output. The trusted deployer reads only exact
commit blobs, reconstructs the deterministic tar and validates every manifest
entry. It never runs website code and needs no Actions download credential.
Keep the existing restricted receiver, health checks and atomic rollback.

The generated public tree duplicates source assets in Git; this is the deliberate
tradeoff for a simpler credential and publishing workflow. CI is a stale-output
check, not a runtime success gate in the SSH Git path. Publish only reviewed
commits on the configured branch; until branch protections/promotion are agreed,
pushing that branch after activation can trigger deployment before CI finishes.
The new path is prepared locally; push, host update and target activation remain
separate user approvals.
