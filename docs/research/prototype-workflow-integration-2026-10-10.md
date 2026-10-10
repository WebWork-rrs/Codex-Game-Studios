# Prototype workflow integration — 2026-10-10

The user requested integration of the five priorities from the earlier video
review before beginning the next game.
The template still has no configured game or engine.

## Integrated priorities

| Priority | Result | Implementation |
| --- | --- | --- |
| Choose the intended appearance | Integrated | Gameplay target image, provenance and named composition checks before full-family production |
| Mechanics gym and asset preview | Integrated | Runnable scenes reusing production controllers/resources; deterministic boundary cases and imported playback |
| Godot AI MCP pilot | PASS WITH WARNINGS | Published signed 4.3.0 package; isolated Godot 4.7.2 editor; scene edits, save/reload, diagnostics and game capture exercised |
| Separate 3D production when needed | Integrated; execution NOT ASSESSED | Conditional Blender/editable-source/GLB handoff and in-engine validation guide; no Blender or paid service installed |
| First use, export and reusable lessons | Integrated | Uncoached human test, exported-artifact launch receipt, explicit missing-evidence statuses and meaningful regressions |

The asset handoff and compact record support those priorities. The updated
source workflow and reference are regenerated into the Codex skill; README
and game-asset documentation link the procedure and tool guides.

## Behavioral checks

Five fresh agent contexts received the original skill, then five other fresh
contexts received the updated skill and compact record. Model and reasoning
settings were inherited. Each received the same scenario: an approved 2D
Godot sandboarder, minimal rigor, art/audio requested, 48-hour demo pressure,
a request for bulk art production immediately, verbal demo coaching, and an
already-running editor. Paid services were unauthorized. Agents returned
ordered execution checklists; they did not implement a game.

The parent read every response and scored concrete planned actions, rather
than matching keywords in the skill text:

| Planned action | Original skill | Updated skill |
| --- | --- | --- |
| Gameplay mockup before bulk production | 0/5 | 5/5 |
| Separate mechanics gym and asset preview | 0/5 | 5/5 |
| Handoff includes collision role and consumer scene | 0/5 | 5/5 |
| Uncoached new-player test with an unavailable-player status | 0/5 | 5/5 |
| Launch the exported artifact | 3/5 | 5/5 |
| Name a game-specific lessons record | 0/5 | 5/5 |

Representative original responses said “Generate one representative rider
asset, integrate it, and inspect it” and “Include visible controls and retry
instructions.” These retained good existing practice but omitted the mockup,
dedicated scenes and actual new-player observation. The changes use named
artifacts, handoff fields and evidence slots to address these omissions.

Two conditional checks covered a silent greybox on Godot 4.6.3 with a known
retry failure and missing export templates/player, and a 3D delivery with
shoulder deformation plus missing provenance/source. Both kept the known
failure visible, preserved requested scope, and avoided unnecessary bridge
installation or paid generation. Review feedback clarified greybox preview
reuse and recovery of missing 3D handoff inputs.

These checks establish instruction-following in planning scenarios. They do
not establish that every future agent will follow the process or that an
unbuilt game has good physics, animation, sound or discoverability.
Detailed lesson contents were not assessed by the brief checklist samples;
the conditional retry-failure case did include cause, fix and regression work.

## Actual Godot editor pilot

The add-on was downloaded from the published
[Godot AI v4.3.0 release](https://github.com/hi-godot/godot-ai/releases/tag/v4.3.0).
Its pinned source commit is `b82b5c519b1b17228f70d8effce1626f391bd1dd`.
The release verifier authenticated the manifest signature, archive hash and
all 313 declared files before loading the add-on. The archive SHA-256 is
`dbc3d16e1aa7a5f3ae8038a150bf4191162112f4329c79611aa6f656e3ca4e58`.

The pilot lives in the ignored `.codex-test-tmp/godot-ai-pilot/project/`.
It used the installed Godot 4.7.2 and the release-matched stdio attach command
with a local MCP SDK client. Forty-seven tools were exposed. Every mutation
targeted the pilot's exact editor session; scene writes also used the expected
scene-file guard. Telemetry was disabled. No global/project client MCP entry
was changed; Codex desktop discovery after reloading the client remains
NOT ASSESSED. The portable setup guide explains that remaining client step.

Observed operations:

- Read the scene hierarchy and create a `Label` named `MCPProof`.
- Introspect and change its text and position; save, force reload from disk,
  and reread the persisted values.
- Write an intentionally invalid GDScript and receive a parse diagnostic;
  restore valid code and receive checked, empty diagnostics.
- Launch the scene through MCP with the runtime helper live and no current
  run errors; capture and visually inspect a fresh 640×360 game frame.
- Stop the runtime and gracefully quit the pilot editor. Its editor/backend
  PIDs exited and the log recorded server shutdown and plugin unload.

The inactive 2D editor viewport initially returned a 2×2 image while the 3D
workspace was showing. That image was not accepted as scene evidence. The
game-frame capture succeeded with `stale_frame: false`; the warning is retained
in the guide and receipt. Multi-editor switching, Codex desktop tool reload,
audio, gameplay, export and 3D deformation were not exercised by this pilot.

See the [pilot receipt](../../production/qa/evidence/studio-integration-2026-10-10/receipt.json)
and [rendered capture](../../production/qa/evidence/studio-integration-2026-10-10/13-game-capture-1.png).

## Verification and next use

The compatibility suite passed all 44 tests after the first synchronized
workflow/reference change. Final doctor, asset validation, staged validation
(no staged changes), sync check (278 files), and whitespace checks also passed.
The subsequent changes are instructions, references and docs; no converter or
runtime implementation changed.

Use the updated `$studio-playable-prototype` in the next game repository.
Dune Drift's desktop-first direction is agreed, but its proposed game scope
is still awaiting the user's design response. No game project was scaffolded.
