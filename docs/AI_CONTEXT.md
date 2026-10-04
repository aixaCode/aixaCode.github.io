# Website context

Source: recovered Proxmox CT 126 `/srv/aixa/releases/20261004-085443`, 137 files, recovered 4 October 2026. Original Windows generator was unavailable. Recovery evidence and dirty-checkout backup are under `/Users/agnieszkabesz/website-recovery/20261004T204051Z`.

Data flow now: `site/` → validated byte-preserving build → `public/` + deterministic tar/file manifest. Proposed flow later: reviewed Git commit → successful GitHub CI artifact → CT 116 trusted destination → restricted CT 126 release helper → public health check → recorded deployed SHA.

Public route: Cloudflare → CT 102 tunnel → CT 106 NPMplus → CT 126 nginx. CT 116 currently deploys other sites to NAS and has no besz.me target. This branch contains no production credentials or remote deployment commands.

Build checks internal href/src/srcset references and HTML fragment IDs. It does not check remote availability, CSS URL references, accessibility, content accuracy or all layouts. The manifest records file bytes and hashes; CI/deployer must bind it to the exact commit when deployment is configured. A tar checksum alone does not establish publisher authenticity.
