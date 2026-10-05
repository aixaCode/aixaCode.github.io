# Second pass against live GitHub Pages

Reviewed 5 October 2026 against https://aixacode.github.io/, the preserved dirty
writing-first checkout, and the local migration source. No push or deployment.

## Findings

- All 22 legacy HTML routes returned HTTP 200 and have matching paths under
  site/. The redesign additionally has about.html and 404.html. Preserve these
  legacy paths when preparing the later GitHub Pages redirect change.
- A fresh text comparison found no missing long essay-body sentences across the
  eight essays. Differences around titles, bylines, navigation and figure labels
  come from the new presentation. Original article dates remain in the inventory.
- Project text differences match Step 6 corrections: assistant fallback, backup
  and dashboard wording; evidence-backed metrics; and built Animal Park artifacts.
- Legacy home introduction and project summaries are reorganized across the new
  home, About, CV and case studies. The old writing-first edits remain preserved
  separately; they are not an additional set of unpublished essays.
- Eight distinct HTTPS link destinations were checked with GET. Seven returned
  HTTP 200. https://gbfactory.uk/ still returns HTTP 404; its replacement remains
  an author decision. GitHub, LinkedIn, both public Decentraland repositories and
  both essay reference destinations were reachable.
- No new content fix was required by this pass. The previously documented factual
  questions about measurement periods, ownership and current review policy remain.

## Verification and evidence

The source check passed for 24 HTML pages and 204 source files; all four metadata
and reference regression tests passed. Live HTML snapshots, text comparisons and
external-link results are saved privately under
/Users/agnieszkabesz/website-recovery/20261004T204051Z/github-pages-pass/.

Link availability is a point-in-time check, not a guarantee of future availability.
The source comparison does not independently verify the author's career claims.

The next approval remains Step 7: push the prepared website branch and deployer
commit, then verify GitHub CI. Proxmox installation, release publication and
GitHub Pages redirects remain later approvals.
