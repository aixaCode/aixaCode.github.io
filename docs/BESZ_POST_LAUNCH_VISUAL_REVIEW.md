# Post-launch image, graph and copy review

Reviewed 7 October 2026 against live release 5c104f2 and committed public files.
Review only: no source edits, pushes or production changes. Diagnostic contact
sheets and inventories are in the private recovery directory's visual-pass/.

## Scope and limits

All 85 referenced image/SVG/social-card assets and responsive variants return
HTTP 200 and match committed bytes. Every HTML image has nonempty alt text.
Visually inspected all 28 diagram families in desktop and mobile variants, all
eight editorial illustrations, hero, portrait and all nine social cards. The
cream/charcoal/pastel palette, photo and pencil illustrations work together.

The Mac is locked and no browser surface is available. This pass inspects the
exact deployed assets and source, not freshly rendered full-page layouts. Prior
Step6 browser layout evidence remains applicable because publish bytes match.

## Fix before the next polish release

1. **Ambiguous graph routing.** Stacked render-diagrams.py places every
   non-adjacent forward edge on x=62. Unrelated paths overlap into a shared bus,
   visually suggesting relationships absent from the graph specification.
   Affected: risk-based-assurance (desktop and mobile), pip-diagnosis (mobile),
   prioritization-scoring-trap (mobile), local-first-home-platform (mobile).
   Use explicitly grouped independent branches: low/medium/high risk lanes;
   diagnosis→response pairs; two independent scoring paths; local versus remote
   home paths. Preserve existing node labels and semantic edges. Single-source
   forks such as evidence-states and permission choices can share a bus safely.
2. **Social-card title obscured.** prioritization-is-constraint-management-og-v4.jpg
   loses the end of “Management” behind the artwork starting at x=645. Wrapping
   estimates Times widths while the renderer uses another serif/fallback font.
   Use actual render-font measurements or conservatively break the title into
   three lines, add a safe text/art gap and inspect the final JPEG. Version the
   replacement filename because production caches these files.
3. **Aging wording remains in the Explorer case.** unity-explorer.html still says
   “a recent 52-day period”, whereas the CV already says “a 52-day period”. Remove
   “recent” for consistency; do not invent dates or change the numbers.

## Author decisions still needed

- gbfactory.uk returns HTTP 404. Do not substitute another business address.
  Confirm the intended destination or remove the public link until restored.
- Approximately 75 annual public builds and the 52-day hotfix-free result remain
  published claims without a measurement period. Need the year/interval behind
  those figures; consistency checks do not independently validate them.
- Current review-policy wording versus illustrative evolution still needs the
  author's confirmation. This review does not certify current operational policy.

## What to keep

Hero and portrait work well with the warm page palette. Editorial covers are
coherent; the improvement-plan image communicates shared support rather than
grading. No replacement illustration is needed. Most single flows/forks are
clear. Nine social cards share good hierarchy; the identified prioritization
export needs correction. Decorative chart marks are illustrations, not evidence
of measured performance; current delivery-effort cards make no numeric claims.

## Proposed next approval

Prepare the four graph-family routing fixes, the social-card correction and the
one-word Explorer copy correction locally. Use new filenames and updated refs,
rebuild public/ + manifest, verify visual meaning as well as text bounds, then
present the concrete result before any push to auto-publishing develop.
