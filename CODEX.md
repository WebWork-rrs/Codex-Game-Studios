# Develop games with Codex

This is a Codex adaptation of
[Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios),
initially based on commit `be8993bbc5a1f016bc770b2846ce06272d284526`, framework
1.1.3. The original studio was created by **Donchitos**; the original MIT
license, copyright, and Claude sources are retained. See [credits](CREDITS.md).
The current integrated upstream commit is recorded in `tools/codex/upstream.json`.

## What a GitHub template means

**Use this template → Create a new repository** copies starter files and
folders into your own independent repository with new history. A fork keeps
its relationship to upstream; a clone downloads the repository and history.
Template copies do not automatically receive upstream updates.
See [GitHub's template documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template).

This starter supplies roles, workflows, standards, templates, and validation
tools. It contains no finished game.

## Start here

Follow the [README quickstart](README.md#start-your-first-game) to create your
own game repository. Open its cloned folder as a project in the Codex app,
or run `codex` from the repository root. Use a current Codex client.

Prerequisites: Git, Python 3.11+ for adapter tooling, Bash for upstream
helpers, and your chosen engine when beginning engine setup. Claude Code,
Anthropic credentials, and additional Python packages are not required.
Your existing Codex login and selected model are used.

Start a new chat/session to load `AGENTS.md` and the new skills, then type:

```text
$studio-start
```

Or ask: **“Read AGENTS.md and use the studio-start workflow to help me begin
my first game.”** Onboarding asks about your idea and process preferences.
`$studio-setup-engine` handles engine selection; Godot, Unity, and Unreal
guidance is retained. No engine has been chosen or installed by this adapter.

CLI/IDE clients support `$` and `/skills`; the app selector may use `@`.
Plain-language requests work too. If a workflow is omitted from a crowded
selector, explicitly name `.agents/skills/studio-NAME/SKILL.md`. The `studio-`
prefix avoids collisions with general brainstorming, review, and onboarding.

For a small first game, follow:

```text
$studio-start
$studio-setup-engine
$studio-brainstorm <your idea>
$studio-create-stories
$studio-dev-story <story path>
$studio-story-done <story path>
```

`$studio-help` recommends your next step based on actual project state.
[The workflow catalog](docs/codex-workflows.md) lists all 74 skills.
Choose `guided` automation during onboarding for routine execution with
consultation on major decisions. Rigor and automation are separate choices.
Only needed roles run; 49 definitions do not mean 49 concurrent agents.

## Compatibility mapping

| Claude mechanism | Codex mechanism |
| --- | --- |
| `CLAUDE.md`, `@` imports | `AGENTS.md`, explicit reference reads |
| 74 slash-command workflows | `.agents/skills/studio-*`, supported metadata |
| Skill-local resources | Converted copies alongside each Codex skill |
| `!` preprocessing, `CLAUDE_SKILL_DIR` | Explicit shell blocks and repository paths |
| 49 Markdown roles / Anthropic models | `.codex/agents/*.toml`, inherit Codex model |
| Agent/Task/question tools | Available Codex tools and sequential fallback |
| Claude path-scoped rules | Explicit rule routing in `AGENTS.md` |
| Claude hooks | Native lifecycle configuration and payload adapter |
| Claude permissions/status line | Existing Codex permissions/UI, not copied |

Do not delete `.claude/`: it remains the shared upstream source for helpers,
templates, and documentation. Engine setup retains upstream mirrors while
Codex reads `project.yaml` and engine references explicitly.

## Hooks and checks

SessionStart provides context; PreToolUse validates commits and warns about
pushes; PostToolUse validates asset data. Current local clients support
hooks; older/cloud clients may not. Start a new session and trust the project
through the normal client flow. In CLI, `/hooks` reviews and trusts exact
definitions. This adaptation never marks hooks trusted or bypasses approvals.

Post-edit feedback cannot undo edits. Checks cover direct file edits, patch
paths, shell edits, and staged JSON. Push warnings remain advisory. Hook
errors/timeouts are not a security boundary. Run explicit checks as needed:

```bash
python3 tools/codex/studio.py doctor
python3 tools/codex/studio.py validate
python3 tools/codex/studio.py validate --staged
python3 -m unittest discover -s tools/codex/tests -v
```

The adapter uses Python's standard library. Windows requires Git Bash and
`python3` on PATH for the bundled POSIX hook commands; otherwise run explicit
checks with your Python executable. Engine build/test/display/screenshot
commands are configured during engine setup.

## Customization and updates

Edit source workflows/roles under `.claude/`, or `tools/codex/convert.py`:

```bash
python3 tools/codex/studio.py sync
python3 tools/codex/studio.py sync --check
```

Sync checks destinations before writing and refuses to overwrite local edits
to generated files. Preserve those edits or move them into the source before
syncing. Additional personal skills/roles are not removed. After an upstream
upgrade, run sync, tests, and doctor. GitHub Actions checks adapter tests and
generated-file drift.
See [upstream synchronization](docs/upstream-sync.md) for daily update pull
requests, merge conflict handling, and manual commands.

Structural and operational adapter checks do not prove that every workflow
performs correctly in every engine. Full game sessions for each engine have
not been run against this empty starter. Claude session logs, notifications,
status-line styling, agent audit hooks, and permission enforcement are not
duplicated. Recovery uses `active.md` and startup context. Models, permissions,
and available collaboration tools remain properties of your Codex client.
See [validation results and environment limits](docs/codex-validation.md).

## Publish your own template

When cloning directly from upstream, `origin` points to the author. Publish
adaptations to a repository under your own account and set that repository
as origin before pushing. Enable **Settings → General → Template repository**
to offer **Use this template** for future games. Keep the MIT license and
upstream credit.

References: [skills](https://learn.chatgpt.com/docs/build-skills),
[AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[hooks](https://learn.chatgpt.com/docs/hooks).
