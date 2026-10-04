# Step 2: content review and proposed updates

Reviewed 2026-10-04. Proposal only: no website, PDF, production configuration, GitHub setting or deployer code has been changed.

## Recommendation

Keep the new besz.me design and the existing essay bodies. Correct navigation, outdated project descriptions, inconsistent CV copy and unavailable links before migration. Generate shared metadata, reading times, RSS and sitemap from a single content inventory during the build work.

## Scope and evidence

Compared all 24 recovered HTML pages against the local checkout, including its preserved uncommitted changes. Reviewed the downloadable two-page CV, article bodies, case studies, internal anchors and public links. The baseline is CT 126 release `20261004-085443`, recovered under `/Users/agnieszkabesz/website-recovery/20261004T204051Z/proxmox-site`.

Text comparisons and link-check evidence are preserved separately under the recovery directory's `content-review/` folder. The original Windows project has not been recovered, so its editorial/build history is unknown.

- All eight essay bodies are preserved in the live redesign. Differences are descriptions, authorship/reading-time metadata, contents navigation and related-reading/footer blocks.
- The nine case-study narratives are preserved. Most word-count reductions come from replacing HTML diagram labels with SVG illustrations and removing repeated contact sections. Do not restore the old layouts just to increase the count.
- CV HTML body text matches the local HTML. The PDF matches the local PDF byte for byte but has older project descriptions than the HTML.
- The recovered HTML href/src file references resolve; scanned internal anchor links target existing IDs. Each page has one H1 and no duplicate IDs.
- Public page canonical URLs use besz.me. The visible CV website URL and the PDF still point to github.io.
- No RSS file or RSS discovery link was recovered. The local feed generator is tied to the old domain and old HTML date markup.
- These checks establish content and reference consistency, not factual verification of employment, outcomes, private project implementation or every external page. Full visual/mobile review belongs to Step 3.

## Page-by-page disposition

| Page | Finding | Proposed action |
| --- | --- | --- |
| Home | Redesign intentionally changes the introduction and features the AI evidence essay. Existing experience and project themes remain. `~75 public builds per year` has no period attached. | Keep the editorial layout and featured essay. Date/source the release metric before treating it as current. |
| About | New page; role, platforms and maximum department scale align with the CV. | Keep. Retain the distinction between personal work and work delivered through teams. |
| CV HTML | Visible github.io URL; current/peak scope wording conflicts; `recent` hotfix-free period will age. | Apply proposed CV corrections below after approval. |
| CV PDF | Old domain; assistant describes isolated work/personal profiles; finance project still uses the older name. | Regenerate from the agreed CV source during implementation. |
| Leadership | Narrative preserved; central footer replaces repeated contact copy. | Keep. Preserve outcome-versus-proxy distinction. |
| Writing | All eight essays retained, now in one list. Original RSS entry point and explicit series grouping are absent. | Restore RSS and add a lightweight series label/order without reverting the design. |
| Projects index | All nine case studies retained. Filter categories overlap intentionally. | Keep. Derive counts from inventory rather than hard-code them. |
| AI Makes Building Easy | Body preserved; historical example mentions 45+ interfaces. | Keep body. Keep the example historical and avoid implying a newly measured result. Improve related-reading destination. |
| Before You Remove Code Review | Body preserved. Describes successive policy versions and risk-based automation. | Keep chronology; reconcile the simpler current-policy claim in the AI engineering case study. |
| Career Ladder | Body preserved. Current next essay is the general AI production essay. | Make the next series entry Feedback. |
| Feedback | Body preserved and identifies itself as part two. Current next essay is Career Ladder. | Make the next series entry Improvement Plans. Preserve CORE/SBI attribution. |
| Improvement Plans | Body preserved and identifies itself as part three. Current next essay is Feedback. | Make the next series entry AI Evidence, and label it a companion rather than falsely calling it part four. |
| AI Evidence | Body preserved. Its next essay currently loops back to Improvement Plans. | Add links to the earlier series entries; retain its human-ownership and source-boundary argument. |
| Prioritization | Body preserved. Empty contents widget because there are no section headings in the body. | Hide the empty widget. Keep short-note structure and original date. |
| Technical Direction | Body preserved. Empty contents widget and awkward `1 minute read` presentation. | Hide empty widget; use `1 min read` or consistent singular/plural handling. Keep it a short note. |
| Unity Explorer | Body preserved; diagrams are now SVGs. Release and hotfix figures lack a measurement period. | Keep architecture narrative. Date metrics; retain `targeting`/`toward` qualifiers for performance goals. |
| Scaling Engineering | Body preserved; 25-developer peak and earlier 50-person department are distinguished. | Keep. Match the CV's historical/peak scope wording. |
| Launcher | Body preserved. Initial download reduction is prominently stated. | Keep `initial launcher download` wording; confirm platform/version before adding a current or universal claim. |
| Engineering Dashboard | Body preserved. Some text attributes computed numbers to AI while describing pinned formulas. | Clarify collection/calculation versus AI interpretation, subject to implementation verification. |
| AI for Engineering Teams | Body preserved. Says every PR requires developer and QA approval, unlike the later risk-routed process in the essay. | Describe it as an initial policy or update to the verified current policy. Proposed safe wording below. |
| Multiplayer Mobile Game | Body preserved; explicitly in development, but `shipped` may imply a public launch. | Use built/distributed wording for client artifacts while keeping store release automation described separately. |
| AI Assistant | Body preserved but now stale relative to current project documentation; public Source link unavailable. | Update fallback, web/dashboard and future-work copy; remove unavailable Source link. |
| Accounting | Body preserved; privacy description says only aggregates reach the assistant. | Verify current integration boundary before changing this; retain evidence/calculation separation. |
| Home Infrastructure | Body preserved; omits current public static hosting example. | Add one concise Proxmox hosting sentence based on verified configuration. |
| 404 | New page; recovery links present. | Keep. Do not include it in RSS or indexable sitemap output. |

## Concrete proposed corrections

### 1. Use besz.me in both CV formats

Replace the visible website address and its link with `https://besz.me/`. Preserve the other contact details. Generate the HTML/PDF from the same approved CV content so project names and summaries cannot drift independently.

### 2. Distinguish current scope from historical peak

The career highlight says current scope includes Creator Tools and SDK, while the work-experience paragraph says they were led for a period.

Proposed career-highlight wording:

> Led technology departments of up to 50 people. At Decentraland, my peak scope covered client engineering, Creator Tools and SDK, with up to 25 developers across 10 countries.

This uses the already published historical scope and avoids deciding which teams are currently owned. Confirm the current title and responsibilities before changing the work-experience dates or present-tense role description.

### 3. Keep release achievements precise over time

Before publication, attach a source/measurement period to approximately 75 builds annually and the 52-day period. If no dates can be supplied, remove `recent` and describe the result historically:

> Led predictable weekly releases, including a 52-day period without a hotfix.

Keep 60 FPS at approximately 100 concurrent users framed as a target/work direction unless measured achievement is established. Do not invent dates, increase numbers or convert goals into outcomes.

### 4. Align the PDF's selected projects with HTML

Replace its older AI Assistant summary with the existing HTML summary:

> Self-hosted family assistant with attributed members, replaceable model providers, permission-gated capabilities, audit logs and durable user-owned data.

Use `AI Accounting & Company Records` consistently instead of the older PDF heading `AI Finance Automation`. Retain the existing deterministic-calculation summary. The PDF needs regeneration, not a binary text replacement.

### 5. Restore the leadership reading sequence

Use Career Ladder -> Feedback -> Improvement Plans. Link AI Evidence as a companion on evidence retrieval. Add a small series navigation block so readers can start at the beginning as well as continue. The existing order is a related-reading choice rather than a missing-body defect, but it clashes with the explicit part-two/part-three introductions.

For AI production and review essays, choose related reading by topic rather than merely moving backward through publication order. Preserve existing dates and URLs.

### 6. Restore RSS and consistent publication metadata

Generate `feed.xml` for all eight essays using besz.me URLs; restore its discovery link and a visible Writing-page link. Parse dates from structured content instead of old layout-specific selectors. Preserve original publication dates; add a substantive update date only when content actually changes.

Generate reading times from article body text, excluding navigation, footer and contents duplication. Use one rounding/minimum convention across Home, Writing and article pages. Generate sitemap modification dates from actual content changes rather than stamping every page with each deployment date.

### 7. Clarify the AI engineering review policy

The engineering case study says every PR needs developer and QA approval, while the review essay describes automated approval for some simple changes and conditional QA.

Proposed wording that preserves the historical account:

> We introduced AI review as an early check alongside developer review and QA. Later iterations routed attention by risk: simple maintenance could follow an automated approval path, while complex changes retained human developer review and QA requirements were assessed explicitly. The accountable people still owned the release outcome.

Confirm this chronology/current policy before replacing the original absolute statement. Do not claim AI cannot approve a PR when the site's own essay says it did.

### 8. Bring the assistant case study up to date

Current local README/docs describe configured Codex fallback and an authenticated dashboard; the public page says there is no fallback and puts a dashboard in future work. Documentation confirms a code-level feature, not the exact live installation state.

Proposed replacement for absolute no-fallback wording:

> Model providers sit behind explicit configuration and shared permission boundaries. Fallback is limited to configured routes; it does not authorize an arbitrary provider change or expand tool permissions.

Proposed current-state addition:

> The codebase includes authenticated web interactions and a household dashboard with read-only projections and narrowly defined commands, alongside CLI, Telegram and email.

Remove the dashboard from the generic future-work list. Keep Docker packaging, local-model validation and ARM64 as future work unless separately verified. Review the claim that SQLite is wholly rebuildable: runtime lifecycle state and operational records still need their own verified backups/exports.

Remove the public `Source` button targeting `https://github.com/aixaCode/personal-assistant` (404). The local remote is under SilverdaleGames; do not publish a replacement private-repository link or change repository visibility as part of this content work.

### 9. Clarify deterministic metrics and AI summaries

The engineering dashboard presents pinned formulas but also refers to AI-computed numbers. Proposed wording, after checking its implementation:

> Each reported metric uses a fixed definition and links to the records counted. AI helps summarize changes and surface questions; the underlying records and definitions remain inspectable.

This avoids asserting an unverified deterministic implementation while preserving reproducibility as the intended contract.

### 10. Keep Animal Park's release status explicit

Replace the public-launch implication of `shipped as IL2CPP builds` with:

> The Unity/C# client is built as IL2CPP artifacts for Android and iOS, with separate development, staging and production environments.

Keep `in development` prominent and distinguish implemented TestFlight/Play automation from verified public availability. Do not introduce launch dates or player counts.

### 11. Add the current hosting example to Home Infrastructure

Proposed addition:

> The platform also hosts public static websites. Cloudflare Tunnel routes requests through a local reverse proxy to nginx in a dedicated Proxmox container; versioned releases allow the site to return to an earlier working version.

Do not yet describe automatic GitHub deployment as implemented. This plan's deployer integration is still future work.

### 12. Resolve the GB Factory destination

`https://gbfactory.uk/` returned 404 for both HEAD and GET. This link appears throughout the shared footer and in the CV. Before migration, either repair that site's routing in a separately approved task or choose a verified replacement destination. Do not silently substitute the design studio address: it may serve a different purpose.

## Public-link results

| Destination | Result | Interpretation |
| --- | --- | --- |
| GitHub profile | 200 | Reachable |
| Unity Explorer repository | 200 | Reachable |
| Launcher repository | 200 | Reachable |
| Referenced Pragmatic Engineer article | 200 | Reachable; no claim that paywalled material was fully verified |
| Radical Candor feedback reference | 200 | Primary source supports CORE's Context/Observation/Result/Next Steps and SBI inspiration |
| Assistant Source button | 404 | Not available to public visitors; remove or replace only with an approved public source |
| GB Factory homepage | 404, HEAD and GET | Needs routing correction or a chosen replacement |
| LinkedIn profile | 405 for HEAD | Automated check inconclusive; do not label it broken |

Attribution check: [Radical Candor's CORE explanation](https://www.radicalcandor.com/blog/give-humble-feedback) supports the Feedback article's description. [CCL's SBI explanation](https://www.ccl.org/articles/leading-effectively-articles/closing-the-gap-between-intent-vs-impact-sbii/) supports the underlying Situation-Behavior-Impact attribution.

## Editorial decisions still requiring evidence

- Current job title, current team ownership and whether the `Present` dates remain correct.
- Measurement period for release counts/hotfix results; launcher reduction's platform/version context.
- Current engineering review policy versus historical stages.
- Exact deployed assistant version and finance-summary permissions before claiming live behavior.
- Desired public destination for GB Factory.

Keep factual claims unchanged until supported or approved; straightforward domain/navigation corrections can proceed when the content update set is approved.

## Next approval boundary

Step 2 delivers this proposal, not applied copy changes. Step 3 is the image/diagram/style audit and replacement recommendations. Website implementation and PDF regeneration remain a later explicit approval; deployment and GitHub redirects remain separately approved steps.
