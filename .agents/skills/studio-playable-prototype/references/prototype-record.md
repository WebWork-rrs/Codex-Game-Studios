# Compact prototype record

Use this structure inside the existing brief/art/QA records; one small project
can keep it in a single Markdown file. Reference existing artifacts rather than
duplicate them. Fill only the agreed scope. A blank status means NOT ASSESSED,
never PASS. Record out-of-scope categories explicitly with their reason.

## Target and scene map

- Brief, core action/challenge, target device, engine pin, native resolution.
- Gameplay mockup path and provenance; camera, palette, rider/character scale,
  layers and HUD; chosen direction or consequential choice still unresolved.
- Mechanics gym scene: shared controller, repeatable inputs/seed, boundary cases.
- Asset preview scene: states/clips, pivots, scale, layers and collision display.
- Runtime scene: integration owner and handoff destinations.

## Asset handoff

For each family, record these fields in a compact block or manifest entry:

- Source and final filename(s), dimensions/world scale, import settings.
- State/frame/clip names and timing; pivot/origin and attachment points.
- Collision role (visual-only, separate gameplay shape, or defined collision).
- Consumer scene/node or resource and integration owner.
- Generation/source provenance, license, cost (unknown if unavailable).
- Delivery status, preview result, retained evidence path, outstanding mismatch.

For example, a rider handoff declares a transparent 128 x 128 sprite family,
`ride` and `airborne` state names, a board-contact pivot, visual-only collision
role, and its exact consumer scene. Inspect the imported frames in motion at
game scale; these example values are not defaults for another game.

## Evidence ledger

Use PASS, PASS WITH WARNINGS, FAIL, or NOT ASSESSED for applicable categories.
A known failure outranks missing assessment; missing required evidence outranks
PASS. Keep editor-playable and shareable-build claims separate.

| Category | Status | Evidence path and observations | Missing scope / reason |
| --- | --- | --- | --- |
| Mechanics and boundary/restart cases | NOT ASSESSED | | |
| Rendered frame against chosen visual target | NOT ASSESSED | | |
| Asset preview playback and runtime integration | NOT ASSESSED | | |
| First use by an uncoached new player | NOT ASSESSED | | |
| Audio actually heard, when requested | NOT ASSESSED | | |
| Exported artifact launched on agreed target | NOT ASSESSED | | |

## First-use script

Start a fresh session. Give the player the build and ask them to play without
explaining the controls. Observe their first action, interpretation of the goal
or challenge, response to feedback, and recovery after failure. Record actual
confusion, changes, and a retest. A scripted agent run is flow evidence, not a
substitute for this human check. When no player is available, leave this script
and the category NOT ASSESSED.

## Distribution receipt

Record target OS/browser, engine version, preset/command and relevant settings,
artifact location and SHA-256, launch result, core loop, input, assets/audio,
retry and settings checks. Name missing templates/SDKs/signing/hardware as
blockers. Never include signing secrets or claim untested platforms.

## Lessons and next checkpoint

Record reproduction, observed cause, fix, and the meaningful regression or
rendered/audio comparison. Keep game-specific lessons in
`production/qa/prototype-lessons.md`; promote a shared lesson only from
repeatable evidence within authorized maintenance scope. If no recurring
failure was observed, record that result. Update the active checkpoint with
the next action, blockers, evidence paths and costs.
