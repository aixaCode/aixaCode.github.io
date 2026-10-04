# besz.me visual review

Reviewed 4 October 2026. Step 3 records recommendations only; no website assets, content or deployed files were changed.

## Scope and evidence

Reviewed the recovered CT 126 release: 31 raster images, 17 article diagram families (34 desktop/mobile SVGs), 11 project diagram families (22 SVGs), and identity icons. Inspected rendered asset contact sheets and sampled the live article/project layouts at phone widths of 320 and 390 pixels. Sampled pages had no horizontal page overflow; this is not an exhaustive responsive or accessibility test.

Evidence directory: `/Users/agnieszkabesz/website-recovery/20261004T204051Z/visual-review/`. It contains editorial, social, identity and icon contact sheets, eight diagram contact sheets and individual SVG renders.

## Recommended priorities

1. Restyle all 22 project SVGs to match the article palette: cream backgrounds, charcoal labels, restrained terracotta/sage/blue fills. Preserve architectural facts and distinguish branches with labels, not colour alone.
2. Relayout dense mobile diagrams. Labels should remain approximately 14–16 CSS pixels at actual phone display size, with wrapping and enough box space. Do not achieve fitting by shrinking text. In `demo-to-production-mobile-v2.svg`, authentication and permissions labels extend beyond their boxes.
3. Correct the promotion diagram topology: desktop currently branches from the written case to calibration and promotion, while mobile shows a sequence. Use the same agreed sequence in both, normally written case → calibration → promotion.
4. Rework the improvement-plan editorial illustration. Repeated cross/check rows suggest pass/fail grading. A shared plan showing diagnosis, support, observable work, opportunity and review better represents the article.
5. Build a consistent social-card template with article title, author/site identity and a smaller illustration. The current cards are cohesive but several become difficult to distinguish in small previews. Keep 1200 × 630 dimensions and protect titles from edge cropping.
6. Clarify conceptual diagrams where graphics imply more than the text establishes. Rename review-evolution's performance-sounding heading, align review gates with the agreed risk policy, and draw feedback return paths where a diagram claims to show a loop.

## Identity and editorial illustrations

| Asset/family | Recommendation | Reason |
| --- | --- | --- |
| Notebook hero and responsive variants | Keep; evaluate compression later | Fits the warm desk/notebook style. Full-size variant is about 445 KB; avoid unnecessary replacement. |
| Portrait | Keep | Authentic portrait; an optional cream frame can unify its presentation without altering the person. |
| Favicon, Apple touch icon, app icons | Keep | Peach and terracotta monogram matches the new palette. |
| AI: building versus production | Keep | Prototype-to-production boundary communicates the subject. |
| AI and code review | Keep | Diff/dependency motif supports the article. |
| Career ladder | Optional refinement | Branching technical hierarchy is more obvious than progression; not a migration blocker. |
| Development feedback | Keep | Work and conversation motifs support actionable feedback. |
| Performance improvement plan | Refine/replace | Repeated grading marks do not express diagnosis and support clearly. |
| Prioritisation | Keep | Queue and bottleneck image fits the argument. |
| Technical direction | Keep | Direction/decision motif works, although abstract. |
| AI evidence and responsibility | Keep; optional refinement | Evidence/timeline motif works. If changing it, prefer a visible human verification action over a launch symbol. |
| Eight essay social cards and default card | Retemplate | Add legible titles and site identity; retain the matching illustrations. |

## Article diagram families

All families retain the warm notebook direction. Recommendations apply to both desktop and mobile variants unless specified.

| Family | Recommendation |
| --- | --- |
| ai-evidence-boundary | Keep concept; improve mobile label size. |
| changing-constraint | Make today's active constraint and later active constraint visibly distinct. |
| delivery-effort | Keep illustrative disclaimer; do not present segment widths as measured effort. |
| demo-to-production | Fix mobile label overflow and increase text size. |
| development-feedback-loop | Add explicit return path to the next opportunity. |
| evidence-states | Keep concept; improve mobile label size. |
| feedback-core-path | Keep concept; improve mobile label size. |
| feedback-pattern | Keep concept; improve mobile label size. |
| human-owns-outcome | Keep concept; improve mobile label size. |
| pip-diagnosis | Keep concept; improve mobile label size. |
| prioritization-scoring-trap | Keep concept; improve mobile label size. |
| product-to-technology | Keep concept; improve mobile label size. |
| promotion-evidence | Align desktop/mobile topology and agreed promotion sequence. |
| review-evolution | Use a neutral heading such as “How review attention shifted”; retain illustrative framing and reconcile first-pass scope with the essay. |
| review-gate | Keep concept; reconcile gate policy with content audit. |
| risk-based-assurance | Keep concept; improve mobile label size. |
| winnable-improvement-plan | Keep concept; improve mobile label size. |

## Project diagram families

All 11 families need palette alignment and label fit checks. Their bright colours and white backgrounds visibly differ from the article diagrams. For dense mobile decision trees, separate context, proposal and permission/verification gates so collapsing the layout does not change its meaning.

| Family | Additional focus |
| --- | --- |
| accounting-evidence-pipeline | Fit long evidence labels inside boxes. |
| assistant-permission-boundary | Preserve the permission boundary clearly in mobile layout. |
| creator-content-pipeline | Fit queue/validation labels. |
| decision-ownership-shift | Maintain clear ownership stages. |
| engineering-ai-release-loop | Show the return path for work that is not ready; align release policy with content. |
| engineering-signal-to-decision | Preserve signal-to-decision sequence. |
| explorer-priority-decision | Simplify mobile branches without removing decision meaning. |
| explorer-product-boundaries | Keep product boundaries distinct in mobile layout. |
| launcher-verification-flow | Separate proposal/context from verification gate on mobile. |
| local-first-home-platform | Clarify shared controller connections if relayout makes the two paths look disconnected. |
| server-authoritative-game-state | Fit authorisation/check labels; preserve server decision ownership on mobile. |

## Implementation and review criteria

Use one palette and diagram typography source for future exports. Treat diagrams as source assets in Git rather than replacing them with generated raster images. Keep image provenance and any generation prompts alongside source assets where available; the recovered deployment does not include the original generator.

Verify changes in real article/project context at desktop, 320 px and 390 px widths. Check text fit, contrast, meaningful alternatives/captions, matching desktop/mobile logic, and social-card thumbnail readability. Inspect completed animation states rather than interpreting transition opacity as final contrast. Generate responsive WebP variants and record dimensions; use explicit image sizes to minimise layout movement.

Content claims flagged in `BESZ_CONTENT_REVIEW.md` still need resolution. This visual review does not approve changing career facts, metrics or deployment policy. Proposed artwork and palette changes should be shown in a local preview before production deployment.
