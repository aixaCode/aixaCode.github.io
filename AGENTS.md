# Legacy Pages redirect branch

Follow global Conventional Commit rules. Read README.md and docs/REDIRECT_REVIEW.md.
Keep this main-based redirect work separate from the dirty writing-first checkout
and the develop Proxmox website. Do not push or merge without the next approval.

redirects.json defines legacy HTML routes. Run scripts/build-redirects.py after
changes; never hand-edit generated redirect pages. Existing assets stay available.
The root cv.pdf is the reviewed current PDF; never replace it with HTML content.

Checks: python3 scripts/build-redirects.py --check; node test/redirect-test.cjs.
Publishing into main automatically triggers GitHub Pages, so merge is production
work. Leave GitHub Pages domain settings and the Proxmox branch unchanged.
