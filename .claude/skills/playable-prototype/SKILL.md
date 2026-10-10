---
name: playable-prototype
description: "Use when a small playable game or experiment needs coherent artwork, animation, audio, and gameplay feedback."
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

When live Godot editor access is useful, follow `docs/godot-editor-mcp.md` for
an isolated, release-matched pilot; verify actual operations before depending
on it. Preserve the user's client scope and existing server entries. The
unconfigured template must not enable a machine-specific connection by default.

## Choose a gameplay mockup

Before producing the full asset family, save a target gameplay image under
`production/art/gameplay-target.png` and link it from the brief. Use available
image generation, a composed mockup, or an existing user-chosen reference with
recorded provenance. Record camera framing, native resolution, character scale,
palette, foreground/background layers, and HUD placement. Reuse an accepted
reference instead of asking the user to choose it again. Resolve consequential
visual choices with the user when no direction exists.

Compare a rendered frame against those named dimensions; record differences
and intentional changes. A mockup guides composition, not proof of playable
physics. If the user requests a greybox or no artwork, record that scope and
use a simple layout sketch; if image tools are unavailable, record the gap and
continue authorized mechanics work without claiming generated artwork.

## Build a mechanics gym and asset preview

Before scaling up content, create a small runnable mechanics scene under the
engine's source root. For Godot, use `src/prototypes/mechanics_gym.tscn` or an
existing equivalent. Reuse production controllers and event hooks; isolate
movement, collision, the main interaction, failure, and restart. Test the
brief's boundary cases with repeatable inputs or seeds and record results.

Create a separate asset preview scene, for example
`src/prototypes/asset_preview.tscn`, that imports the delivered assets at their
intended gameplay scale. Show sprite states or animation clips, pivots,
layering, transparency, and collision boundaries; for 3D, include material,
rig/deformation and attachment checks. Inspect playback, not just a sheet.
Keep these scenes available for later regressions rather than copying their
logic into the game. Preserve equivalent scenes already present. For another
engine, use its actual scene/test format and source root.

For a mechanics-only greybox, reuse its layout/debug scene as the preview and
record generated artwork and audio as out of scope. Assess the requested
mechanics and layout without requiring an asset family or unrelated tools.

## Produce and integrate assets

Read `.agents/skills/create-game-assets/SKILL.md` and use its local templates
and relevant references. Keep a short art-direction brief and an asset
manifest with dimensions, states/frames, pivots, provenance, and status.
Use the compact record in `references/prototype-record.md` for the handoff.
For each asset or family, specify final filename, dimensions or world scale,
state/frame/clip names, pivot/origin, import settings, collision role,
provenance/license, owning consumer scene, and delivery/validation status.
Keep editable sources separate from engine-ready exports where applicable.
Test the handoff by importing one representative delivery into the preview
scene before expanding the family; record missing files or mismatched clips
as failures. A raster report or generator's success message is not integration.
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

For an approved 3D project, follow `docs/3d-assets.md`: separate editable
sources from `.glb` deliveries, declare scale/materials/clips/attachments, and
inspect the imported representative asset in the engine before expansion.
Blender MCP and paid model generation are conditional tools, not requirements
for a 2D experiment. Report missing tools or unobserved rigs explicitly.

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

## Check first use without coaching

Provide only the introduction needed for the agreed core action and goal,
including relevant input, failure/retry, pause, and mute cues. Run a first-use
playtest with a new player who has not received verbal instructions. Record
whether they discover the action, understand the objective or endless-run
challenge, recognize feedback, and recover from failure. Capture confusion
and resulting changes; rerun the affected flow after a fix. Do not invent a
human result: an agent's scripted walkthrough checks the flow but cannot
establish uncoached discoverability. If no new player is available, mark this
category NOT ASSESSED and leave a short executable playtest script.

## Verify the distributed build

Before calling a prototype ready to share, export the agreed target and launch
the exported artifact outside the editor. Exercise the core loop, inputs,
asset/audio loading, failure/retry, and settings in that build. For a web target,
serve and play the exported build in the intended browser. Record target OS or
browser, engine version, export settings/command, artifact location and hash,
and observed results. Keep credentials and signing secrets out of records.

When export templates, SDKs, signing, hardware, or browser support are missing,
name the blocker and mark distribution NOT ASSESSED. An editor-playable
prototype can be reported as such; it is not a verified shareable build.
Distribution checks apply to the agreed target, not every possible platform.

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

Record a compact evidence ledger using `references/prototype-record.md`:
mechanics, visual-target comparison, asset-preview playback, first use, audio,
and distribution each need a status, evidence path, and reason for gaps.
Keep readiness scoped: known failure outranks missing evidence, and an
unassessed required category prevents an overall PASS for that claim.

After playtesting, keep demonstrated failures and fixes in the game's
`production/qa/prototype-lessons.md`. Include reproduction, cause, fix, and a
regression that can catch recurrence. For visual, audio, or feel problems,
retain the appropriate observed comparison rather than asserting artistic
quality with a source-text test. If a failure recurs across projects, propose
a small shared-workflow improvement with before/after behavioral evidence;
apply it only within the user's authorization. Record no observed recurring
lesson when that is the result; do not invent one.
