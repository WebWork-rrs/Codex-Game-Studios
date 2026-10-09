---
name: playable-prototype
description: "Build or polish a small playable game with cohesive assets, animation, and gameplay feedback. Use for experiments that should look and feel like a game."
---

# Playable prototype

Turn a small game concept or an existing greybox into a cohesive playable
experience. Keep planning proportional to the configured rigor; a small
prototype can use a one-page brief. Preserve the user's art, audio, scope,
and accessibility choices, including explicit requests for placeholders or
silence. This workflow is a Codex adaptation extension.

## Establish the target

Read `AGENTS.md`, `project.yaml`, the active checkpoint, and the game brief
when present. Inspect existing game code and screenshots before redesigning.
For an unconfigured engine, use `/setup-engine`; for an undefined concept,
use `/brainstorm`. Clarify only consequential missing choices. Preserve
existing authorization for routine assets and implementation work.

Record the intended view, art style, native resolution, and core loop.
Define a small presentation target alongside mechanical acceptance criteria:
coherent character/environment art, appropriate motion, readable gameplay
state, and feedback for pickups, hazards, goals, or other relevant events.
Do not add unrequested mechanics to make an experiment seem larger.

## Produce and integrate assets

Read `.agents/skills/create-game-assets/SKILL.md` and use its local templates
and relevant references. Keep a short art-direction brief and an asset
manifest with dimensions, states/frames, pivots, provenance, and status.
Choose one representative asset at game scale, then produce related assets
from the same direction. Use an available `imagegen` skill/tool for custom
raster artwork; save final files in the game repository and wire them into
the scenes. A generation prompt alone is not a delivered asset.

Licensed asset packs such as Kenney are a useful starting source; retain
their supplied license and provenance. If generation tools are unavailable,
explain the gap and offer sourcing rather than silently marking prompts or
greyboxes as finished artwork. Optional paid providers are described in
`docs/game-assets.md`; configure or spend on them only within the user's
authorization. Credentials remain local.

For Godot, load the relevant bundled craft skills from `.agents/skills/`:

- `godot-animation` for sprite playback, idle/movement states, and tweens.
- `godot-tilemap` when the environment uses tiles or terrain transitions.
- `godot-audio` and `audio-design` when sound or music is in scope.

For another engine, use its actual documentation and available importer
skills; do not apply Godot APIs. Optional related skills mentioned by the
vendored pack may not be installed. Use the installed skill's relevant
references or official documentation instead of assuming those files exist.

Check asset dimensions, alpha, frame alignment, scale, and import settings.
The bundled raster helpers require Pillow. Alpha-channel existence alone
does not establish a usable cutout: inspect the pixels and content bounds.
Review animation at game scale for drifting pivots or identity changes.

## Make actions feel responsive

Read `.agents/skills/game-feel/SKILL.md`. Add proportionate feedback to the
game's actual events: for example, a pickup sparkle, short sound, and counter
animation, or a goal opening and brief victory response. Keep visuals
separate from collision/movement, preserve input responsiveness, and restore
transient effects on restart. Camera shake and flashes are optional and
should respect the game's tone and accessibility choices.

Compose the screen around gameplay, with a compact readable HUD appropriate
to the game. Check layering so characters remain visible near goals and
props. Reuse existing systems and event hooks rather than replacing working
mechanics merely to add presentation.

## Observe before completion

Run relevant game tests and follow `.claude/docs/run-and-observe.md` for a
real rendered playthrough. Inspect and retain evidence under
`production/qa/evidence/`. Observe movement animation, interactions, goal
feedback, and restart where applicable. Actually listen before claiming
sound or music verified; otherwise label audio NOT ASSESSED.

Report mechanical and presentation results separately using PASS, PASS WITH
WARNINGS, FAIL, or NOT ASSESSED. A known failure outranks missing evidence;
an unobserved required category prevents an overall PASS. Static screenshots
prove layout, not motion, sound, or human enjoyment. State what was observed,
what is deferred, asset provenance, and any generator cost. Update the
checkpoint with the next actionable step. Do not call prompt text, a parse
check, or an unplayed build a finished playable experience.
