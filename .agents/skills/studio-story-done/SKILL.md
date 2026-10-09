---
name: studio-story-done
description: "End-of-story completion review — verifies each acceptance criterion, checks GDD/ADR deviations, prompts code review, updates status."
---

## Codex execution adapter

Read the repository's `AGENTS.md` before this workflow. Its Codex mappings and
the user's existing authorization govern this workflow and all referenced
upstream documents. Work from the repository root.

- `$studio-NAME` invokes a repository skill; arguments are the text supplied
  with the invocation. Do not expect Claude slash commands or `$ARGUMENTS`
  substitution. Read another skill's `SKILL.md` when chaining workflows.
- Run each **Execute before proceeding** shell block explicitly; Codex does
  not run Claude's inline shell preprocessing. Use the real configuration
  output. Report command failures rather than silently assuming defaults.
- `AskUserQuestion` means ask with an available Codex question tool or plain
  text, and wait when the answer is required. Previously authorized routine
  edits need no repeated per-file approval. Preserve unresolved game-design
  choices and the configured automation mode.
- Claude `Agent`/`Task`, `subagent_type`, and named roles mean Codex subagents.
  Use `.codex/agents/<role>.toml` when custom role selection is supported;
  otherwise pass its `developer_instructions` to the available spawn tool.
  Use only actual available tools, inherit the user's model, respect the
  concurrency limit, and collect results. If delegation is unavailable,
  perform the roles sequentially and label that limitation.
- `Read`/`Glob`/`Grep`/`Write`/`Edit`/`Bash`/`WebSearch`/`WebFetch` are capability
  labels: map them to available file, patch, shell, and browsing tools.
  `TeamCreate`, `SendMessage`, and task lists map to available collaboration
  tools and a written task ledger; do not invent tools.
- Shared `.claude/docs`, `.claude/scripts`, `.claude/hooks`, and templates are
  intentional runtime dependencies. Relative `references/` and `scripts/`
  paths resolve against this skill's folder. Original references may still
  show `/NAME`: interpret known studio workflows as `$studio-NAME`.
- `CLAUDE.md` is a legacy engine/configuration mirror. Codex reads engine
  settings from `project.yaml` and explicitly reads the matching version
  reference. `@file` imports, Claude settings, status lines, and permissions
  do not configure Codex. Preserve `AGENTS.md` during engine setup.
- For design/architecture/registry/review inputs, apply
  `.claude/docs/bounded-document-reading.md`: inventory ranges and read with
  `.claude/scripts/read-markdown.py` using returned line/column cursors.
  Upstream "read in full" means complete coverage through bounded chunks,
  never an unbounded tool response. Record gaps as NOT ASSESSED.
- Edit upstream skill/role sources under `.claude/`, then run
  `python3 tools/codex/studio.py sync` to regenerate Codex copies. Do not edit
  generated files directly. Apply the same rule to framework self-tests.


**Execute before proceeding** (from the repository root):

```bash
bash ".claude/hooks/yaml-helper.sh" resolve_config --keys review_mode,automation,workflow,story_granularity,qa.level,testing.strict,system_overrides
```
Resolved above — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.claude/docs/config-resolution.md`.

# Story Done

This skill closes the loop between design and implementation. Run it at the end
of implementing any story. It ensures every acceptance criterion is verified
before the story is marked done, GDD and ADR deviations are explicitly
documented rather than silently introduced, code review is prompted rather than
forgotten, and the story file reflects actual completion status.

**Output:** Updated story file (Status: Complete) + surfaced next story.

---

## Phase 1: Find the Story

**Read `references/1-find-story.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 2: Read the Story

**Read `references/2-read-story.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Verify Acceptance Criteria

**Read `references/3-verify-criteria.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Check for Deviations

**Read `references/4-deviations.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Lead Programmer Code Review Gate

**Read `references/5-code-review-gate.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Present the Completion Report

**Read `references/6-completion-report.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 7: Update Story Status

**Read `references/7-update-status.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 8: Surface the Next Story

**Read `references/8-next-story.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Collaborative Protocol

**In `collaborative` mode (the default).** For `guided` and `autonomous` modes,
see `.claude/docs/automation-modes.md` — the rules below describe collaborative
behavior. The BLOCKED-override close (Phase 7) always prompts regardless of mode
(it's a `scope_changes` always-ask decision).

- **Never mark a story complete without user approval** — Phase 7 requires an
  explicit "yes" before any file is edited.
- **Never auto-fix failing criteria** — report them and ask what to do.
- **Deviations are facts, not judgments** — present them neutrally; the user
  decides if they are acceptable.
- **BLOCKED and NOT ASSESSED verdicts are advisory** — the user can override and
  mark complete anyway; document the risk explicitly if they do. For NOT
  ASSESSED, the documented risk is that the criterion was never evaluated, not
  that it failed — record which criteria those were, so the gap is recoverable
  later rather than closed over.
- Use `AskUserQuestion` for the code review prompt and for batching manual
  criteria confirmations.

---

## Recommended Next Steps

- At `minimal`: run `$studio-dev-story [next-story-path]` (`$studio-story-done` for an In Review one); when every story is Complete, play the build, then `$studio-create-stories` for more or `$studio-settings` to raise `modes.rigor`
- With a sprint plan: run `$studio-story-readiness [next-story-path]` to validate the next story before starting implementation
- If a sprint plan exists and all its Must Have stories are complete: run `$studio-smoke-check sprint` → `$studio-team-qa sprint` → `$studio-gate-check`
- If tech debt was logged: track it via `$studio-tech-debt` to keep the register current
