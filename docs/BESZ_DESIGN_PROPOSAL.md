# Design and readability proposal

Reviewed 2026-10-27 on branch `fix/site-content-and-readability`. Direction from
Aga: professional, but cute, nerdy and feminine.

## Already fixed on this branch

- Footer touched the screen edges below about 1400px (padding shorthand reset
  the shell gutter).
- Leadership and case-study headings sat directly on their text; paragraphs in
  those sections had no spacing; lines ran to about 105 characters. Now 22–24px
  heading gaps, 18px paragraph spacing, about 78 characters per line.
- 25 labels on Leadership were 9–11px; now at least 11.5px.
- Checked: no horizontal overflow on any page at 320 and 390px.

## What works

Warm cream paper, Instrument Serif headings, DM Sans body at 17–18px with
strong contrast (about 11:1), terracotta accent, watercolour editorial covers,
good alt text on every image. Keep the notebook direction.

## What holds it back

1. **Diagrams look like corporate flowcharts** next to hand-drawn art: ALL CAPS
   labels in rounded pastel boxes, colour cycling by position rather than
   meaning, heading and detail run together ("CONTEXT Where + when").
2. **Some diagrams contradict their text.** `review-evolution-v4` has no widths
   although its caption explains block widths; `risk-based-assurance-v5` colours
   high risk green and low risk peach; `delivery-effort-v4` is two text boxes
   where a stacked bar is described; `winnable-improvement-plan-v4` shows one
   column for "obligations on both sides"; `local-first-home-platform-v5` draws
   the remote path as a separate box instead of a dashed path into the
   controller.
3. **Very tall mobile diagrams**: pip-diagnosis 1311px, risk-based-assurance
   1117px, demo-to-production 784px. One essay is about 14,400px on a phone.
4. **Scroll-in fade (0.7s)** on every section; text and figures look washed out
   while skimming.
5. **Home on a phone** shows headline and picture only; the first essay starts
   about 1,140px down.
6. **Few people, little personality.** Covers are mostly browser-window
   wireframes; two covers look alike; the portrait is a white cut-out on cream;
   the Animal Park case study has no picture of the game.
7. **Positioning**: header and hero still say "a VP of Engineering" (present).

## Proposal

### Phase 1: readability (small, CSS and copy)

- Remove the scroll-in fade from body sections and figures.
- Line height 1.85 → about 1.65 in essays; cap the essay column near 65–70
  characters.
- Home on mobile: intro and featured essay above the hero image.
- Collapsible "In this essay" menu on mobile.
- Diagram `<img>` tags get width and height (stops layout jumps).
- Spelling: judgement, behaviour, optimised, prioritisation across captions and
  diagram labels.
- Hero and header line (needs Aga): "Engineering leader and builder", with
  "most recently VP of Engineering at Decentraland, now building through GB
  Factory".

### Phase 2: diagrams that look like the notebook (render-diagrams.py)

- Colour by role: blue input, green process, peach human decision or risk,
  terracotta for the one key node.
- Sentence case labels; heading on one line, detail lighter below.
- Minimum 15px label size; desktop width capped near 1100; breakpoint at 760px.
- Compact mobile layouts (cards or two columns) for the four tallest diagrams;
  horizontal or 2×2 layouts on desktop.
- Sketchy strokes and hand-drawn arrowheads; dot-grid paper behind figures.
- Redraw the five diagrams that contradict their text.
- Claim-style titles on project diagrams instead of slug titles.

### Phase 3: cute, nerdy, feminine (keep it professional)

| Idea | Where | Effort |
|---|---|---|
| Washi-tape corner and dot-grid paper on figures | figures | S |
| One handwritten margin note per diagram, terracotta, curly arrow | diagrams | S–M |
| Key takeaways as slightly rotated pastel sticky notes | essays | S |
| Portrait on a cream circle with a pencil-ring outline and a tiny doodle | home, about | S |
| Pixel heart or "+1 XP" marker on game projects; pixel "continue?" 404 | projects, 404 | S–M |
| A set of 8–10 line doodles (teacup, pencil, plant, controller) as section and card markers | site-wide | M |
| Animal Park screenshots or art in its case study | project page | S, needs assets |
| Regenerate career-ladder and one diff-window cover with people and hands, like the improvement-plan cover | covers | M–L |
| Fix share cards: title font, artwork to the edge, washi tape, per-project cards | social cards | M |

### Phase 4: housekeeping

- Add a 1000w hero image (the full one is 445 KB).
- Diagrams embed a 48 KB font each; reference the site font instead.
- 76 unreferenced image files (1.9 MB) ship with the site; confirm which are
  kept on purpose before pruning.
- About-page portrait should load eagerly.
