# Codex Game Studio

This repository adapts Claude Code Game Studios for Codex. Start with
`$studio-start` for game onboarding and `$studio-help` for workflow guidance.
Plain-language requests work too. A fresh copy has no engine or game concept;
inspect the actual project configuration before assuming its current state.

## Session and configuration

Work from the repository root. Read `project.yaml` and, when present,
`production/session-state/active.md` before continuing game work. Recover the
checkpoint after compaction or interruption instead of restarting. Resolve
effective settings using the upstream helper:

```bash
bash .claude/hooks/yaml-helper.sh resolve_config --keys rigor,workflow,automation,review_mode,qa.level,engine.name,engine.version
```

See `.claude/docs/config-resolution.md` for local overrides, legacy fallbacks,
and rigor expansion. Default rigor is `minimal`; do not seed the six derived
knobs because explicit values prevent rigor from changing them. Keep process
proportional to the selected rigor.

Resolve source/test roots from `engine.name`: Godot `src/` and `tests/`, Unity
`Assets/` and `Assets/Tests/`, Unreal `Source/<Module>/` and its test directories.
Never conclude that a project has no code by scanning the wrong engine root.
Engine setup populates `project.yaml`, legacy `CLAUDE.md`/technical-preferences
mirrors, and `docs/engine-reference/<engine>/VERSION.md`. Read that reference
explicitly when needed; `@` imports in `CLAUDE.md` are not Codex imports.
Verify uncertain APIs against official engine documentation.

## Authorization and execution

The user's request authorizes ordinary reversible work required to complete
it. Preserve that authorization across stages and agents; do not repeat
upstream per-file approval prompts for already authorized changes. Ask about
missing game-design choices, material scope changes, and actions outside the
user's authorization. Respect configured automation preferences and platform
permissions. Unanswered required questions are not approval. Do not commit,
push, publish, or message external people unless the user authorizes it.
Inspect the remote before publication: a clone's origin may still point to
the template's author instead of the user's game repository.

Read `.agents/skills/studio-*/SKILL.md` for workflows. Run their marked shell
blocks explicitly; Claude `!` preprocessing does not execute in Codex. Take
arguments from the user's message. Resolve supporting resources relative to
the selected skill folder. `.claude/docs`, `.claude/scripts`, `.claude/hooks`,
and templates are intentional shared dependencies.

For a small playable game with artwork, animation, or gameplay feedback, use
`$studio-playable-prototype`. Its focused craft dependencies are native skills
under `.agents/skills/`: `create-game-assets`, `game-feel`, `godot-animation`,
`godot-tilemap`, `godot-audio`, and `audio-design`. Read only what applies.
Keep the user's brief and existing art/audio choices; minimal rigor limits
paperwork, not requested presentation quality. The skills do not include an
image model or paid-service account. Use available image generation or
licensed asset sources, integrate the real files, and observe the result.
See `docs/game-assets.md`; report missing tools or unverified motion/audio.

In upstream references, map `/NAME` to `$studio-NAME` for known studio
workflows. Claude Read/Glob/Grep/Write/Edit/Bash/WebSearch are capabilities:
use actual Codex file, patch, shell, and web tools. AskUserQuestion maps to an
available question tool or plain text. Never invent tools or skip execution.

## Studio roles

`.codex/agents/*.toml` defines 49 roles. Use custom agent selection when
supported. If the spawn interface has no role selector, read the role TOML
and pass its `developer_instructions` in the task prompt. Models and reasoning
inherit the user's settings; Opus/Sonnet are not Codex model names.

Delegate only when requested by the user or explicitly required by an invoked
studio skill. Respect the available concurrency limit and queue work as
needed. Give agents bounded domains and destinations; collect and verify
their artifacts. Director/lead titles are responsibilities, not a mandate
to spawn every role. Avoid parallel writers to the same files. If delegation
is unavailable, perform required roles sequentially and report that limit.
Team/task/message labels map to available collaboration tools and a written
ledger. Apply relevant upstream escalation and error-recovery protocols.

## Document reading

Use `.claude/docs/bounded-document-reading.md` for design, architecture,
registry, and review inputs. Inventory headings/ranges with
`python3 .claude/scripts/read-markdown.py index <path>` and consume content
with its bounded `read` command and returned line/column cursors. A request to
read a full document means complete coverage through successive chunks.
Summaries, grep previews, or truncated output do not complete a review.
Record unreviewed ranges as NOT ASSESSED; preserve the user's model settings.

## Standards and evidence

Before game implementation, read `.claude/docs/coding-standards.md`. Load
relevant documents under `.claude/rules/` for files being changed:

| Area (including matching Unity/Unreal directories) | Rule |
| --- | --- |
| Gameplay | `gameplay-code.md` |
| Core/engine | `engine-code.md` |
| AI | `ai-code.md` |
| Networking | `network-code.md` |
| UI | `ui-code.md` |
| Game design documents | `design-docs.md` |
| Narrative | `narrative.md` |
| Asset data JSON | `data-files.md` |
| Shaders | `shader-code.md` |
| Tests | `test-standards.md` |
| Prototypes | `prototype-code.md` |
| Studio skills, roles, adapter | `skill-authoring.md` |
| Persistent role memory | `agent-memory.md` |

The rules' `paths` frontmatter defines the actual areas. Codex does not load
Claude rules automatically: apply them through this routing, with requested
rigor and user instructions taking precedence over blanket upstream role
requirements. Use configurable gameplay values and frame-rate-independent
logic. Honor accepted ADRs, story criteria, and engine boundaries.

Test changed behavior at the configured QA level. For player-visible changes,
launch and observe the game and retain screenshots under
`production/qa/evidence/`; a parse check is not a run. Report missing engines,
displays, or tools and exactly what was not checked rather than claiming the
game works. See `.claude/docs/run-and-observe.md`.

## Validation and maintenance

`.codex/hooks.json` supplies native lifecycle hooks. They run only in a
supported client after the user trusts the project and exact hook definitions.
Do not bypass trust or copy Claude permission settings. Use explicit checks
when hooks are unavailable and before reporting success:

```bash
python3 tools/codex/studio.py doctor
python3 tools/codex/studio.py validate
python3 tools/codex/studio.py validate --staged
```

JSON validation complements engine tests; it does not prove gameplay works.
Push warnings are advisory. Codex sandbox and approvals remain user-configured.

Workflow and role copies are generated. Edit `.claude/` sources or
`tools/codex/convert.py`, then run `python3 tools/codex/studio.py sync`.
The six native game-craft skills are copied from the hash-pinned sources in
`third_party/gamedev-skills/`; preserve their Apache-2.0 LICENSE and NOTICE.
Sync refuses to overwrite customized generated files. Verify with:

```bash
python3 tools/codex/studio.py sync --check
python3 -m unittest discover -s tools/codex/tests -v
```

See `CODEX.md` for setup, limitations, and publishing your own template.
