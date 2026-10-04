# Migration to besz.me

Prepared 2026-10-04. This is a proposal; production and GitHub settings have not been changed.

## Recommended outcome

Keep `aixaCode/aixaCode.github.io` as the website's Git source, make besz.me the primary public address, and keep hosting on Proxmox CT 126. CT 116 should deploy approved, validated releases from GitHub. GitHub Pages should publish only a small redirect site preserving old page URLs.

## Verified starting point

- GitHub Pages publishes the older repository root from `main`, with no custom domain.
- Local branch `writing-first` has uncommitted content, styling, RSS and sitemap changes. Preserve these separately before importing anything.
- besz.me runs on CT 126 (`static-web`, 192.168.20.235), nginx root `/srv/aixa/current`.
- Public route: Cloudflare -> tunnel CT 102 -> NPMplus CT 106 -> CT 126.
- Active release: `/srv/aixa/releases/20261004-085443`. Release helper retains three releases and supports rollback.
- CT 116 (`website-deployer`) polls every five minutes but currently deploys configured sites to the NAS. besz.me is absent from its configuration.
- The current deployer must not run arbitrary scripts from website repositories. Its destination restrictions currently allow only the configured NAS root; adding CT 126 requires an explicit trusted target model and an update to those rules.
- The live site includes eight essays, nine case studies, About, CV, Leadership, Writing and a 404 page. Its sitemap uses besz.me; www redirects to the apex.
- A file-reference check of the copied live HTML found no missing href/src files. This did not test anchors, srcset variants, external links or all responsive layouts.
- The live release has no `feed.xml`. Several case-study pages have fewer words than their local equivalents; a semantic comparison is needed to distinguish intentional edits from lost content.
- Initial desktop review: cream backgrounds, terracotta accents, Instrument Serif headings, DM Sans text, warm notebook hero and sketch illustrations form a consistent direction. A full image and mobile review remains outstanding.

## 1. Recover and establish the source

1. Preserve the dirty local checkout and record the current GitHub SHA and live release.
2. Locate the original redesign source and `deploy-aixa.sh` before treating minified production HTML as editable source. If it cannot be recovered, import the release as a clearly documented baseline and reformat it without changing behavior.
3. Preserve repository history. Create a migration branch from main, then reconcile the current release with the uncommitted local changes page by page.
4. Keep editable content, shared templates, CSS, JS, original diagrams and image metadata in Git. Generate the public output into `public/`; avoid manually maintaining repeated page headers and footers.
5. Use a small deterministic static build. Markdown for essays/case studies plus shared templates is a reasonable choice, provided migration preserves existing URLs and content. Choose the tooling after inspecting the recovered source.
6. Add repository instructions and documentation following `aixaCode/repo-template` where this repository has no rule. Use Conventional Commits without scopes.

## 2. Reconcile content

Build a page inventory recording old URL, new URL, content differences, images and review status.

- Review every essay and case study for factual accuracy, supported claims, dates, readability and useful conclusions. Do not invent accomplishments or metrics.
- Align role, experience, biography and project descriptions across Home, About, CV and the PDF CV.
- Preserve article URLs and heading anchors where possible. Provide explicit mappings where they change.
- Generate canonical URLs, social metadata, sitemap and RSS from one content inventory using `https://besz.me`.
- Preserve original publication dates; distinguish substantive updates from deployment dates. Derive reading times consistently.
- Test navigation, contact links, the PDF, 404 behavior and internal/external references.

## 3. Finish the design and image audit

Treat the deployed design as the starting point, with shared color, type, spacing and image rules.

- Review all eight essay illustrations, hero, portrait, nine case-study diagram sets and social cards together.
- Keep illustrations tied to the specific argument; use diagrams to explain systems and screenshots when authentic product evidence is useful.
- Keep cream paper, charcoal lines, restrained terracotta/sage accents and consistent sketch treatment. Replace only images that fail the style or meaning review.
- Check image text and diagram labels at phone sizes, use the existing mobile diagram variants, and provide meaningful alt text/captions.
- Preserve responsive WebP variants and explicit dimensions. Version replaced image filenames because nginx caches images for 30 days.
- Record source, rights and generation prompts/settings where available. Keep originals outside the public output and production credentials outside Git.
- Check mobile navigation, keyboard access, contrast, motion preferences and layout overflow before release.

## 4. Extend the deployer

Recommended flow: reviewed main commit -> successful CI -> immutable static artifact -> CT 116 -> restricted release helper on CT 126 -> health check -> record deployed SHA.

- Keep builds in GitHub CI or a controlled build environment. CT 116 fetches and validates artifacts without executing arbitrary repository scripts.
- Add an explicit, host-controlled `static-web/aixa` target alongside the existing NAS backend. A Git repository must not choose an arbitrary host, path or remote command.
- Use a dedicated deploy identity restricted to the aixa release operation, not broad Proxmox root access. Keep keys on the hosts.
- Pin the artifact to a commit and verify its checksum, file inventory and allowed paths. Reject traversal, unsafe links, secrets and repository metadata.
- Stage and validate the release before switching `current`. After switching, verify Home, an essay, a project and assets, then automatically roll back on failure.
- Store deployed commit, artifact checksum, build time and release directory in a manifest. Update deployer state only after verification succeeds.
- Keep bounded release history and an operator rollback command. Separate NAS requirements from CT deployments so a NAS outage cannot block besz.me updates.
- Test target validation, failed upload/build, unhealthy release, repeat polling, rollback and continued operation of existing NAS sites.
- Run the deployer repository's required syntax and test checks. Update its README, architecture decisions and destination restrictions.

## 5. Migrate the old GitHub Pages address

Keep the besz.me Cloudflare/Proxmox DNS route. Generate a separate small GitHub Pages artifact with a redirect page for every old HTML URL, plus a useful fallback 404 page.

- Redirect to the matching besz.me path, preserving query strings and fragments when possible, with a visible fallback link and the destination canonical URL.
- GitHub Pages static redirect HTML is a browser redirect, not a server-side HTTP 301. Test both normal browser navigation and fallback behavior.
- Isolate redirect output from `public/` so CT 116 never deploys it to besz.me and creates a redirect loop.
- Account for legacy PDF/feed URLs separately; keep a compatible PDF copy if needed rather than serving HTML under a PDF filename.
- Switch Pages publication to the generated redirect artifact only after the new release is verified.
- Do not simply change GitHub Pages DNS instructions to point besz.me at GitHub; that would change the selected hosting architecture.

## 6. Release and ongoing maintenance

1. Produce a reviewable migration branch and preview, content checklist, image audit and deployer changes.
2. Verify the static build, references/anchors, metadata/feed, responsive pages and deployment failure behavior.
3. Deploy the selected release to besz.me and verify through both nginx and the public Cloudflare route.
4. Publish the GitHub Pages redirects and test representative old deep links.
5. Confirm deployed SHA, rollback, release retention and backup coverage for source/assets and host configuration. Three local releases are not a backup.

Normal editing becomes: edit content/assets -> preview -> commit -> CI -> reviewed merge to main -> deployer publishes the validated release. Avoid editing production files directly.

## Completion criteria

- The complete new website is reproducible from Git.
- All eight essays and nine case studies have recorded content/image review outcomes.
- The local changes are reconciled, RSS is restored, and all public metadata points to besz.me.
- CT 116 publishes and records a tested CT 126 release without disrupting its existing targets.
- Old GitHub Pages HTML URLs lead to their matching new pages.
- A failed release leaves or restores the healthy site, and rollback is documented and verified.
