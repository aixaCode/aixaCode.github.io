# Legacy GitHub Pages redirects

This branch prepares browser redirects from aixaCode.github.io to besz.me.
Website source and Proxmox publishing live on develop in site/ and public/.

Regenerate: python3 scripts/build-redirects.py
Check: python3 scripts/build-redirects.py --check && node test/redirect-test.cjs

See docs/REDIRECT_REVIEW.md for scope, limitations and the approval boundary.
