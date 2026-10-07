# Website context

Source: recovered Proxmox CT 126 `/srv/aixa/releases/20261004-085443`, 137 files, recovered 4 October 2026. Original Windows generator was unavailable. Recovery evidence and dirty-checkout backup are under `/Users/agnieszkabesz/website-recovery/20261004T204051Z`.

Data flow prepared locally: `site/` → build → committed `public/` and `release-manifest.json`. CI rebuilds to reject stale publish output. Proposed delivery: read-only SSH Git fetch → exact committed publish blobs → trusted deterministic tar/manifest validation → restricted CT 126 release helper → health check → recorded deployed SHA. The Git path needs no GitHub Actions credential and runs no website code on CT 116.

Public route: Cloudflare → CT 102 tunnel → CT 106 NPMplus → CT 126 nginx. CT 116 currently deploys other sites to NAS. The prior artifact components and CT 126 receiver are installed, but no active besz.me target exists. The new Git publishing code is still local and requires approval before push/installation. This branch contains no production credentials or remote deployment commands.

Build checks internal href/src/srcset references and HTML fragment IDs. It does not check remote availability, CSS URL references, accessibility, content accuracy or all layouts. The manifest records file bytes and hashes; CI/deployer must bind it to the exact commit when deployment is configured. A tar checksum alone does not establish publisher authenticity.

Permanent publishing branch: develop. The approved switch follows the initial feat/besz-source release; source/public/manifest must be committed together. Main and GitHub Pages remain unchanged.
