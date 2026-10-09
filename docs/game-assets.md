# Game assets and presentation

Use `$studio-playable-prototype` for a small experiment that should have a
coherent game world, real artwork, appropriate animation, and gameplay
feedback. It works with minimal rigor and a short brief. Existing requests
for placeholders, silence, or a limited scope remain valid.

```text
Read AGENTS.md and use studio-playable-prototype to build my small coin game.
Use minimal rigor and guided automation. Give it a coherent visual style,
an animated player, a themed environment, coin pickup feedback, and a clear
goal and restart. Use available image generation and licensed free assets.
Run and observe the game, and report visuals, motion, and audio separately.
Ask before using a paid asset service. Keep the mechanics small.
```

## Included craft skills

Six native skills from [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills)
are included with their supporting scripts, references, templates, and
license notices:

| Skill | Purpose |
| --- | --- |
| `$create-game-assets` | Art direction, asset families, generation/source handoff, importing, and visual checks |
| `$game-feel` | Proportionate motion, particles, and interaction feedback |
| `$godot-animation` | Sprite animation, animation states, and tweens |
| `$godot-tilemap` | Tile environments and terrain transitions |
| `$godot-audio` | Godot playback, audio buses, and effects |
| `$audio-design` | Sound/musical feedback and mixing |

Their role is practical craft; the Studio workflows still manage the brief,
stories, checkpoints, implementation, and QA. Read only the skills and
references the task needs. This is a focused subset, so related-skill links
in upstream prose are not a promise that the entire pack is installed.
The Godot guidance targets 4.7; verify APIs against the actual project pin.

## Asset tools

The skills provide workflow instructions and raster inspection helpers.
They do not include an image model, asset library, or paid-service account.
When the Codex client exposes `imagegen`, use its normal built-in tool for
custom raster assets, save the results into the game repository, and inspect
them at game scale. Availability depends on the client. Generated animation
frames still require alignment, transparency, and playback checks.

[Kenney's free asset pages](https://kenney.nl/assets) offer a starting point
for coherent packs. Keep each downloaded pack's supplied license and record
its source. No asset pack is bundled in this template.

Optional providers, configured separately by the user:

- [Ludo CLI](https://ludo.ai/developers/cli): sprites, animation, audio, and
  other assets; its documented Godot export writes a SpriteFrames resource.
  CLI/API/MCP access requires an eligible account and consumes credits.
  Check current plan eligibility and set a budget before generation.
- [PixelLab MCP](https://www.pixellab.ai/mcp): pixel-art characters,
  directional animations, and terrain tilesets. It requires its own account
  and token.
- [ElevenLabs MCP](https://github.com/elevenlabs/elevenlabs-mcp): optional
  dedicated audio generation when free/source assets do not fit the project.

These connections are not enabled by this template. Keep credentials out
of Git, and do not assume connecting a provider validates its outputs.
A Godot MCP server is also optional: existing CLI and native app tools can
run and observe games.

The raster helpers need Python 3.10+ and Pillow. From the repository root:

```bash
python3 -m pip install -r .agents/skills/create-game-assets/scripts/requirements.txt
python3 .agents/skills/create-game-assets/scripts/asset_report.py assets/player.png --expect-size 64x64 --require-alpha --json
python3 .agents/skills/create-game-assets/scripts/build_preview_sheet.py assets/player.png assets/coin.png --out production/qa/evidence/asset-preview.png
```

The report checks dimensions and alpha-channel presence; it does not assess
artistic quality or guarantee meaningful transparent pixels. Inspect the
report's alpha range/content bounds and the actual image. A contact sheet is
useful evidence for static assets; rendered playback and listening are still
needed for animation and audio claims.

## Provenance and maintenance

`third_party/gamedev-skills/SOURCE.json` records the selected skills, exact
upstream commit, and source hashes. Sources are unchanged Apache-2.0 material
by Abhishek Barali and contributors. `LICENSE` and `NOTICE` are retained in
that directory and each generated native skill folder. See `CREDITS.md`.

`python3 tools/codex/studio.py sync` copies this pinned subset into
`.agents/skills/`; `sync --check` checks source hashes, supporting files,
licenses, and generated output. Customize the orchestration under
`.claude/skills/playable-prototype/`, then sync. Do not edit generated copies.

The daily Donchitos update job covers the original Studio framework.
The game-craft pack is separately pinned and receives reviewed updates:
download the same selected upstream folders at a chosen commit into a
temporary directory, compare the complete resources and license/notice,
replace the vendored sources, update SOURCE.json's commit and hashes, sync,
and run the compatibility suite before committing. Keep any deliberate
local source modifications marked in the provenance manifest. New game
repositories receive these files from the template; existing games need a
selective migration that preserves their settings and artwork.
