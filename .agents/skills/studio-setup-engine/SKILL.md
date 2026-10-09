---
name: studio-setup-engine
description: "Configure engine and version. Pins it in CLAUDE.md; WebSearch fills reference docs when the version is beyond LLM training data."
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
- Edit upstream skill/role sources under `.claude/`, then run
  `python3 tools/codex/studio.py sync` to regenerate Codex copies. Do not edit
  generated files directly. Apply the same rule to framework self-tests.


# Engine Setup

When this skill is invoked:

**Execute before proceeding** (from the repository root):

```bash
bash ".claude/hooks/yaml-helper.sh" resolve_config --keys workflow
```
**Tier awareness.** The `workflow` tier resolved above governs which design
artifact this skill expects and the finish path it recommends in §12:
- **`minimal`** — the design artifact is the one-page `design/game-brief.md`
  (no GDDs, systems decomposition, or per-system design at this tier).
  `$studio-setup-engine` runs *first* in the minimal path, so a missing brief here is
  normal, not a gap. The finish path is the 4-step floor.
- **`standard` / `full`** — the design artifact is `design/gdd/game-concept.md`
  and the finish path is the full pipeline.

If the block did not render (shell preprocessing disabled), assume `minimal` (the default).

## 1. Parse Arguments

Four modes:

- **Full spec**: `$studio-setup-engine godot 4.6` — engine and version provided
- **Engine only**: `$studio-setup-engine unity` — engine provided, version will be looked up
- **No args**: `$studio-setup-engine` — fully guided mode (engine recommendation + version)
- **Refresh**: `$studio-setup-engine refresh` — update reference docs (see Section 10)
- **Upgrade**: `$studio-setup-engine upgrade [old-version] [new-version]` — migrate to a new engine version (see Section 11)

---

## 2. Guided Mode (No Arguments)

**Read `references/2-guided-mode.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 3. Look Up Current Version

**Read `references/3-version.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 4. Update CLAUDE.md Technology Stack

**Read `references/4-claude-md-stack.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5. Populate Technical Preferences

**Read `references/5-technical-preferences.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 5.5 Populate `project.yaml` (Primary Config Store)

**Read `references/5.5-project-yaml.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 6. Determine Knowledge Gap

**Read `references/6-knowledge-gap.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 7. Populate Engine Reference Docs

**Read `references/7-reference-docs.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 7.5 Scaffold the Engine Project

**Read `references/7.5-scaffold.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 8. Verify the CLAUDE.md Import

**Read `references/8-verify.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 9. Update Agent Instructions

Ask: "May I add a Version Awareness section to the engine specialist agent files?" before making any edits.

For the chosen engine's specialist agents, verify they have a
"Version Awareness" section. If not, add one following the pattern in
the existing Godot specialist agents.

The section should instruct the agent to:
1. Read `docs/engine-reference/<engine>/VERSION.md`
2. Check deprecated APIs before suggesting code
3. Check breaking changes for relevant version transitions
4. Use WebSearch to verify uncertain APIs

---

## 10. Refresh Subcommand

If invoked as `$studio-setup-engine refresh`:

1. Read the existing `docs/engine-reference/<engine>/VERSION.md` to get
   the current engine and version
2. Use WebSearch to check for:
   - New engine releases since last verification
   - Updated migration guides
   - Newly deprecated APIs
3. Update all reference docs with new findings
4. Update "Last verified" dates on all modified files
5. Report what changed

---

## 11. Upgrade Subcommand

**Read `references/11-upgrade.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## 12. Output Summary

**Read `references/12-output-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Guardrails

- NEVER guess an engine version — always verify via WebSearch or user confirmation
- `project.yaml` is the primary config store (v1.1). Always dual-write engine
  config to BOTH `project.yaml` (primary) and `technical-preferences.md` (legacy
  mirror). If the two ever diverge, `project.yaml` is authoritative.
- NEVER overwrite existing reference docs without asking — append or update
- If reference docs already exist for a different engine, ask before replacing
- Always show the user what you're about to change before making CLAUDE.md edits
- If WebSearch returns ambiguous results, show the user and let them decide
- When the user chose **GDScript**: copy the GDScript CLAUDE.md template from **A1** in `references/godot-language-config.md` exactly. NEVER add "C++ via GDExtension" to the Language field. GDScript projects may use GDExtension, but it is not a primary project language. The `godot-gdextension-specialist` in the routing table is available for when native extensions are needed — it does not make C++ a project language.

---

## Appendix A — Godot Language Configuration

Moved out of this file so it costs nothing on non-Godot runs.

**When the chosen engine is Godot, read**
`references/godot-language-config.md`
and use the subsection for the chosen language:

- **A1** — CLAUDE.md Technology Stack templates (GDScript / C# / Both)
- **A2** — naming conventions
- **A3** — engine specialist routing and file-extension tables

**Load discipline.** On any engine other than Godot, **never load it** — nothing in Sections 4, 5 or 5.5 needs it, and reading it anyway spends the tokens the split exists to save. On Godot, read it once when you first reach Section 4 and keep using it for Sections 5 and 5.5; do not re-read it at each reference.
