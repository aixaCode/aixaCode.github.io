# Step 4: source and build preparation

Completed locally on 4 October 2026 in `/Users/agnieszkabesz/besz-migration`, branch `feat/besz-source`, from main bf8113b. The original writing-first checkout and its staged/unstaged work were preserved.

- Recovered source: 24 HTML pages, 137 total files, byte-identical to the CT 126 recovery.
- Dependency-free Python static build; public output and deterministic tar/checksum/manifest are generated and ignored.
- All local href/src/srcset and HTML fragment checks passed.
- Repeated archive builds matched SHA-256 `664447fb54c25cdff265d4a8d9e3db806bfe2aee3e5c2070cede152b6141f37f`.
- Deliberate missing href, missing fragment, missing srcset target and symlink checks were rejected successfully.
- Local homepage preview rendered with the recovered styling, font and hero image.
- CI validation/upload configuration is prepared, not run on GitHub. Action release versions were checked against GitHub release metadata.

No push, merge, GitHub Pages settings change, deployer change or production deployment occurred. Content reconciliation, RSS restoration, diagram restyling and template conversion remain pending. The initial source is recovered HTML rather than the unavailable original generator.

Preview: http://127.0.0.1:8080/. Screenshot evidence is in the private recovery visual-review directory. Run commands are in README.md.
