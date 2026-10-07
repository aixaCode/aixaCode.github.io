# GitHub Pages redirect preparation

Prepared locally from live GitHub Pages main at 0beca2f. No push, merge or Pages
setting change during preparation. Existing dirty writing-first checkout is intact.

The 22 existing HTML routes redirect to their corresponding besz.me destinations.
The home and projects index use / and /projects/. JavaScript uses location.replace
to preserve query strings and fragments and avoid adding a history entry. Each
page also has a canonical URL, immediate meta-refresh and a visible fallback link.
GitHub Pages serves static files, so these are browser redirects, not HTTP 301s.
Without JavaScript, the meta-refresh reaches the destination without query/fragment.

A custom 404 sends unknown legacy paths to the same path on besz.me; without
JavaScript its fallback is the home page. Unknown paths may still be 404 on besz.me.
Direct cv.pdf cannot issue an HTTP redirect on this host: its bytes are updated
to the reviewed besz.me PDF. Links through cv.html redirect to the current CV page.
Existing assets remain for cached legacy pages and historical asset links.

Validation: all 22 destinations must return HTTP 200. The generator's --check
verifies generated pages. Node tests execute the actual redirect scripts with
mock locations to verify normal/query/fragment cases and the fixed destination.

Publishing requires separate approval: push this branch, then merge into main
through a reviewed PR and verify GitHub Pages deployment and representative old
URLs. Do not change the Pages domain to besz.me: Proxmox hosts that domain.
Develop and the Proxmox publishing workflow are unaffected by these root files.
