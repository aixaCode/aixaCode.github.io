# Step 6: local content and visual implementation

Completed locally on 5 October 2026 in `/Users/agnieszkabesz/besz-migration`, branch
`feat/besz-source`. Original legacy root files and the dirty writing-first checkout
were preserved. No push, merge, Proxmox installation or public deployment occurred.

## Applied changes

- Retained the confirmed VP of Engineering title. Changed the CV highlight to
  published historical peak scope and removed the aging word “recent” from the
  existing 52-day result; numbers, dates and performance-target qualifiers remain.
- Updated the HTML CV's website address to besz.me and regenerated a visually
  checked two-page PDF from the same HTML source. Project names and summaries now
  match. Added a source-hash guard to require regeneration after HTML CV edits.
- Restored the leadership sequence: Career Ladder → Feedback → Improvement Plans,
  with AI Evidence as a companion. Added a shared reading sequence on all four.
- Removed empty contents panels from the two short notes.
- Added RSS discovery on all pages and an explicit Writing subscription link.
  Generated eight dated RSS entries, stable sitemap dates and body-only reading
  times from content/essays.json. Original publication dates remain unchanged.
- Updated assistant copy to configured fallback and code-level authenticated web/
  dashboard features based on local project documentation, removed the unavailable
  public Source button, and clarified that operational records require backups.
  The text does not claim that every feature is active in a particular deployment.
- Clarified reported metric definitions/evidence versus AI summaries, described
  Animal Park client artifacts as built rather than implying public launch, and
  added the verified static-hosting example to the home infrastructure case study.
- Rendered 56 v4 SVG diagrams from one editable graph/palette source. Project and
  article diagrams now share cream backgrounds, dark labels and pastel accents.
  Mobile labels use 34 SVG units at a 650-unit width (about 14.4 CSS px on a 276px
  content area). Long desktop flows stack rather than shrinking labels excessively.
- Corrected promotion/calibration order consistently and added feedback/return
  arrows. Review evolution uses a neutral illustrative heading; delivery-effort
  labels no longer resemble quantitative performance measurements.
- Replaced the improvement-plan checklist illustration with collaborative planning,
  support and opportunity. The built-in generation prompt and source are recorded
  in design/IMAGE_PROVENANCE.md. Kept hero, portrait, icons and other editorials.
- Added nine 1200x630 social cards with titles, author and besz.me. Versioned all
  changed artwork/diagram/card filenames and derive CSS/JS cache keys during build.

## Verification

- Four metadata/reference regression tests passed.
- All 24 source and built HTML pages pass local href/src/srcset/anchor checks.
- Browser layout checks on all 24 pages at 320, 390 and 1280 px found no horizontal
  overflow, missing H1 or empty contents panel.
- All 56 SVG variants passed actual browser text/box checks. Final long-flow and
  share-card exports were visually checked; font widths drive wrapping.
- All eight essay bodies match the recovered version after whitespace normalization
  and exclusion of figure/navigation text; no argument or original date was removed.
- PDF text checks confirm two pages, besz.me and matching project summaries. Both
  rendered pages were reviewed; no clipped text or orphaned role header remains.
- Repeated ordinary builds produce the same archive checksum. The prepared Step 5
  deployer accepted the actual updated tar/checksum/file manifest.
- npm ci and npm run social-cards succeeded with pinned Sharp. The ordinary CI build
  uses Python standard library only and publishes already reviewed image/PDF assets.
- Git diff whitespace checks and Python syntax compilation passed.

Browser screenshot/measurement evidence is under the private recovery directory:
`/Users/agnieszkabesz/website-recovery/20261004T204051Z/step6-review/`.
Local preview: http://127.0.0.1:8080/.

## Deliberately pending factual decisions

The user confirmed “VP of eng”, but did not provide measurement periods, team
responsibilities or a GB Factory destination. Therefore:

- Release figures (~75 annually and the 52-day period), employment dates and current
  ownership remain the already published claims, not newly independently verified.
- The GB Factory link remains unchanged despite its earlier 404 result. Do not
  substitute another studio's address without the user's chosen destination.
- The current engineering review policy versus initial rollout still needs the
  author's confirmation. The case study's approval requirement remains; diagrams
  describe the essay's illustrative evolution rather than certifying current policy.
- Exact live assistant version and accounting summary permissions remain unverified.
  Accounting privacy claims have not been expanded.

These should be resolved before the final production content approval. This local
implementation does not implicitly approve them.

## Next boundary

Push the migration branch and locally prepared deployer commit, verify GitHub CI
artifacts and keep public hosting unchanged. Proxmox access/installation, publishing
a new release and replacing GitHub Pages with redirects remain separate approvals.
