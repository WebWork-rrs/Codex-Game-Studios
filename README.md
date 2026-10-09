# Codex Game Studios

A game-development starter for **OpenAI Codex**. Turn an idea into a game brief,
implement features, test gameplay, and prepare releases using structured studio
workflows and specialist roles. Includes engine guidance for **Godot, Unity,
and Unreal Engine**.

This is a reusable project template: it supplies the development process and
tools. You choose the game idea and engine, then build your game with Codex.

**Original framework:** [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios)
by **[Donchitos](https://github.com/Donchitos)**. The studio architecture, original
roles, workflows, rules, and templates are their work. The Codex adaptation is
maintained by [WebWork-rrs](https://github.com/WebWork-rrs).
The original MIT license and **Copyright (c) 2026 Donchitos** are retained.
See [credits](CREDITS.md) and [support the original creator](https://github.com/sponsors/Donchitos).

## Start your first game

### 1. Create your own game repository

On [this repository](https://github.com/WebWork-rrs/Codex-Game-Studios), select
**Use this template → Create a new repository**. Choose your GitHub account,
name it something like `my-first-game`, and create it from the default branch.

Clone **your new repository**, replacing `YOUR-USERNAME` with your account:

```bash
git clone https://github.com/YOUR-USERNAME/my-first-game.git
cd my-first-game
```

A [GitHub template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
copies the starter files into an independent repository with fresh history.
Your game has its own commits and settings. Future template updates are
integrated separately; see [keeping up to date](#keeping-up-to-date).

### 2. Open the project in Codex

You need:

- Codex installed and signed in. Use the [official Codex quickstart](https://developers.openai.com/codex/quickstart/) for installation and login.
- Git, Python **3.11 or newer**, and Bash for the bundled validation tools.
  On Windows, use Git Bash and make `python3` available on PATH.
- Your selected game engine when you reach engine setup.

**Codex app:** Add the cloned `my-first-game` folder as a project and start a
new chat in it. Open the repository root—the folder containing `AGENTS.md`
and `project.yaml`.

**Codex CLI:** From that same folder, run:

```bash
codex
```

The studio skills are included in `.agents/skills/`; you do not need to install
them individually. Codex uses your existing login and model selection.

### 3. Paste this starter prompt

```text
Read AGENTS.md and use the studio-start workflow to help me build my first game.

My idea: a small 2D game where the player collects coins and reaches an exit.
Target platform: desktop.
Use minimal rigor and guided automation. Help me choose an engine.
Keep the first playable version small, using placeholder art.
```

Replace the idea and platform with your own. If you have no idea yet, say
**“I don't have a game idea yet—help me explore one.”**

Onboarding establishes where you are starting and your process preferences.
For a small first game, `minimal` rigor keeps planning to a one-page game brief
and implementable stories. `guided` automation lets Codex carry out routine
work while consulting you on major decisions.

You can also invoke onboarding directly:

```text
$studio-start
```

The examples below use the Codex CLI/IDE `$studio-NAME` syntax. In the app,
you can ask for the workflow by name in plain language or select it in the
skill picker. See [official skill documentation](https://learn.chatgpt.com/docs/build-skills).

### 4. Build the first playable version

Let onboarding guide you through the next step. A typical **minimal** workflow is:

| Step | Workflow | What it does |
| --- | --- | --- |
| Choose an engine | `$studio-setup-engine` | Records the engine/version and helps configure the project. |
| Define the game | `$studio-brainstorm` | Develops your idea into `design/game-brief.md`, including the first version's scope and build order. |
| Plan features | `$studio-create-stories` | Turns the brief into small stories with acceptance criteria. |
| Implement a feature | `$studio-dev-story <story-path>` | Builds one story using the project's conventions. |
| Review completion | `$studio-story-done <story-path>` | Checks the implementation against the story's acceptance criteria. |

Replace `<story-path>` with an actual Markdown story file created by Codex.
Repeat the implementation and completion steps for each feature. Engine setup
and a completed brief come before implementation. Standard and full rigor add
more design, architecture, and review steps; `$studio-help` follows your
configured process.

For example, after the brief is ready, tell Codex:

```text
Use studio-create-stories to plan the first playable version from the game brief.
Then implement the first story with studio-dev-story. Run the game and check
that story's acceptance criteria. Report what you observed and anything you
could not test. Build toward a playable loop: move, collect coins, reach the exit.
```

The engine must be installed and runnable for gameplay verification. The starter
has no engine preconfigured; engine installation and a successful game run are
separate from validating the studio tools.

### 5. Continue in another session

Open the same project and ask:

```text
Read AGENTS.md and the current session checkpoint. Use studio-help to tell me
where the project stands and continue with the next unfinished story.
```

Project settings live in `project.yaml`; session checkpoints live under
`production/session-state/`. Commit your game's progress to your own repository
when ready.

## Already have a game?

Use `$studio-start` and select **Existing work**. Codex routes you through
`$studio-project-stage-detect` to identify the current stage and `$studio-adopt`
to audit how existing artifacts fit the workflows. Follow its migration plan
before moving or replacing existing game files.

## What's included

- **74 Codex skills** covering ideation, design, architecture, implementation,
  art/audio specifications, QA, production, and release preparation.
- **49 specialist role definitions**, including designers, programmers,
  producers, artists, audio specialists, and QA leads. Roles inherit your
  Codex model settings and run as needed within your client's capabilities.
- **Project instructions in `AGENTS.md`** that route coding standards, engine
  references, configuration, and workflow behavior for Codex.
- **Lifecycle hook configuration** for startup context, pre-tool checks, and
  post-edit asset validation, plus manual validation commands.
- **An upstream update workflow** that prepares reviewed integration branches
  while preserving the original project's history and attribution.

Browse [all studio workflows](docs/codex-workflows.md). Useful entry points:

| You want to… | Workflow |
| --- | --- |
| Find the next step | `$studio-help` |
| Make a throwaway prototype | `$studio-prototype` |
| Design a game system | `$studio-design-system` |
| Plan a sprint | `$studio-sprint-plan` |
| Review code | `$studio-code-review` |
| Report a bug | `$studio-bug-report` |
| Prepare for release | `$studio-release-checklist` |

## Project layout

```text
AGENTS.md                Codex project instructions
project.yaml             Game settings and workflow preferences
.agents/skills/          Codex studio workflows and supporting resources
.codex/                  Codex role definitions and hook configuration
.claude/                 Original framework sources and shared helpers
design/                  Game brief and design documents
docs/                    Architecture, engine references, and studio guides
production/              Stories, plans, QA evidence, and session checkpoints
tools/codex/             Adapter, validation, and upstream integration tools
```

Keep `.claude/`: shared helpers, templates, and documentation still depend on
it. Game code locations depend on the chosen engine: `src/` for Godot,
`Assets/` for Unity, and `Source/` for Unreal.

## Check the studio tools

Run these from the repository root:

```bash
python3 tools/codex/studio.py doctor
python3 tools/codex/studio.py sync --check
python3 tools/codex/studio.py validate
```

`doctor` checks the adapter and reports engine configuration status;
`sync --check` checks generated-file consistency; `validate` checks asset JSON.
These checks complement your engine's build, tests, and actual gameplay runs.

Hooks depend on client support and normal project/hook trust. Manual checks
remain available when hooks are unavailable. See [Codex setup and compatibility](CODEX.md)
and [validation results](docs/codex-validation.md) for details and limitations.

## Keeping up to date

This template repository checks Donchitos's upstream `main` daily at
**03:17 UTC / 09:17 Asia/Dhaka** through **Actions → Sync upstream studio**.
When changes exist, it merges them on `automation/upstream-sync`, regenerates
Codex files, runs checks, and publishes the review branch. Updates reach `main`
after review and merge.

**Current setup:** daily checks and review-branch preparation are enabled.
Automatic PR creation additionally requires GitHub's **Allow GitHub Actions to
create and approve pull requests** permission and the repository variable
`UPSTREAM_CREATE_PULL_REQUESTS=true`. Until those are enabled, the workflow
provides a link to open the PR manually.

New games created with **Use this template** have independent history and do
not automatically receive these updates. Ask Codex to review and selectively
migrate framework changes into your game, preserving its engine settings and
source code. See [upstream synchronization](docs/upstream-sync.md) for manual
integration, conflict handling, and the full automation setup.

To customize the studio itself, edit the original workflow/role sources under
`.claude/` or the adapter under `tools/codex/`, then regenerate and check:

```bash
python3 tools/codex/studio.py sync
python3 -m unittest discover -s tools/codex/tests -v
```

Generated skills and roles should be changed through their sources. The
converter refuses to overwrite customized generated files.

## Documentation and credits

- [Codex setup, compatibility, and troubleshooting](CODEX.md)
- [Complete workflow catalog](docs/codex-workflows.md)
- [Upstream synchronization](docs/upstream-sync.md)
- [Adapter validation and known limits](docs/codex-validation.md)
- [Implemented upstream fixes and evidence](docs/codex-fixes.md)
- [Original Claude Code Game Studios documentation](https://github.com/Donchitos/Claude-Code-Game-Studios#readme)
- [Credits](CREDITS.md) · [MIT license](LICENSE)

Created from Donchitos's work; independently adapted for Codex by WebWork-rrs.
