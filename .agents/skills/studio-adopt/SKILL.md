---
name: studio-adopt
description: "Brownfield audit — do existing artifacts actually work? Numbered migration plan. Unlike $studio-project-stage-detect, checks compliance not existence."
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
bash ".claude/hooks/yaml-helper.sh" resolve_config --keys review_mode,automation,automation_always_ask,workflow
```
Resolved above — use as-is. `$studio-adopt` also inspects `project.yaml` and the legacy
config files directly when reporting and writing migration state; that raw
inspection is deliberate and separate from the resolved values above.

# Adopt — Brownfield Template Adoption

This skill audits an existing project's artifacts for **format compliance** with
the template's skill pipeline, then produces a prioritised migration plan.

**This is not `$studio-project-stage-detect`.**
`$studio-project-stage-detect` answers: *what exists?*
`$studio-adopt` answers: *will what exists actually work with the template's skills?*

A project can have GDDs, ADRs, and stories — and every format-sensitive skill
will still fail silently or produce wrong results if those artifacts are in the
wrong internal format.

**Output:** `docs/adoption-plan-[date].md` — a persistent, checkable migration plan.

**Argument modes:**

**Audit mode:** `$ARGUMENTS` (blank = `full`)

- **No argument / `full`**: Complete audit — all artifact types
- **`gdds`**: GDD format compliance only
- **`adrs`**: ADR format compliance only
- **`stories`**: Story format compliance only
- **`infra`**: Infrastructure artifact gaps only (registry, manifest, sprint-status, stage.txt)

---

**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

**`workflow`** (per `.claude/docs/workflow-modes.md`). It scopes the Phase 2 audit and
Phase 3 severity: `full` audits all doc types at full structure; `standard` audits
only the required docs/sections (optional sections are informational, not gaps);
`minimal` is a `design/game-brief.md` format check — GDDs/ADRs/UX are not expected. See Phase 2.

## Phase 1: Detect Project State

**Read `references/1-detect.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 2: Format Audit

**Read `references/2-format-audit.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Classify and Prioritise Gaps

**Read `references/3-classify.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Build the Migration Plan

**Read `references/4-migration-plan.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Present Summary and Ask to Write

**Read `references/5-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Write the Adoption Plan

**Read `references/6-write.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 7: Offer First Action

**Read `references/7-first-action.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Collaborative Protocol

**Applies in `collaborative` mode (the default).** For `guided` and
`autonomous` modes, see `.claude/docs/automation-modes.md` — the rules below
describe what collaborative mode requires, not universal behavior.

1. **Read silently** — complete the full audit before presenting anything
2. **Show the summary first** — let the user see scope before asking to write
3. **Ask before writing** — always confirm before creating the adoption plan file
4. **Offer, don't force** — the plan is advisory; the user decides what to fix and when
5. **One action at a time** — after handing off the plan, offer one specific next step,
   not a list of six things to do simultaneously
6. **Never regenerate existing artifacts** — only fill gaps in what exists;
   do not rewrite GDDs, ADRs, or stories that already have content
