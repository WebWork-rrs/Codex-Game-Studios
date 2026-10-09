---
name: studio-balance-check
description: "Find balance outliers, broken progressions, degenerate strategies, economy imbalances in formulas and data. 'Check game balance'."
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
bash ".claude/hooks/yaml-helper.sh" resolve_config --keys automation
```
# Balance Check



Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

## Insufficient input — check this before producing any report

**If the inputs this skill needs do not exist, the answer is "could not run" —
not a filled-in report.** Check first, and stop if the check fails.

1. List the inputs this skill reads (data files, prior reports, profiler output,
   test results, registries, source code).
2. For each, record `FOUND` or `ABSENT` — not "assumed present".
3. If any input required for a section is ABSENT, that section is
   **`NOT ASSESSED — NO DATA`**. Do not estimate it, do not infer it from an
   adjacent artifact, and do not leave a mandated cell to be filled by whoever
   reads the template next.
4. If **every** required input is ABSENT, stop and report
   **`NOT ASSESSED — NO DATA`** as the whole verdict, naming what was missing and
   which skill produces it.

**A verdict of `NOT ASSESSED` is a success.** It is the correct, useful answer to
"what does the data say?" when there is no data. The failure mode this prevents is
specific: a report whose verdict enum has no "could not run" state produces
**false clean passes** — an asset audit returning COMPLIANT on a project with no
assets and no standards, or a performance profile reporting ">99% headroom against
a 16.67ms budget" with zero profiler data and no budget ever set.

**Absence of evidence is never evidence of absence.** A scan that finds no
matches because there are no files to scan has not verified anything. Say which of
the two happened — a reader cannot tell from a green result.

---

## Phase 1: Identify Balance Domain

Determine the balance domain from `$ARGUMENTS` — the whole string, since a data-file path may contain spaces:

- **Combat** → weapon/ability DPS, time-to-kill, damage type interactions
- **Economy** → resource faucets/sinks, acquisition rates, item pricing
- **Progression** → XP/power curves, dead zones, power spikes
- **Loot** → rarity distribution, pity timers, inventory pressure
- **File path given** → load that file directly and infer domain from content

If no argument, ask the user which system to check.

---

## Phase 2: Read Data Files

Read relevant files from `assets/data/` and `design/balance/` for the identified domain.
Note every file read — they will appear in the Data Sources section of the report.

---

## Phase 3: Read Design Document

**Registry first.** If `design/registry/entities.yaml` exists, read it before the
GDD. Its `constants` and `formulas` sections hold the cross-GDD named values and
output ranges — the balance targets — already distilled, each with a `source:`
GDD and any `revised:` date:
```
Grep pattern="^  - name:" path="design/registry/entities.yaml" output_mode="content" -A 6
```
Take the intended values from the registry for any constant or formula it lists
(the `constants:` and `formulas:` blocks); these are the authoritative cross-doc
figures a GDD must not contradict. **If `design/registry/entities.yaml` does not
exist or has no entries** (it ships as an empty stub until `$studio-design-system`
populates it), skip this and use the GDD alone.

Then read the GDD for the system from `design/gdd/` to understand intended design
targets, tuning knobs, and expected value ranges — for anything the registry did
not already supply. This is the baseline for "correct" behaviour.

If the data files are FOUND but neither source gives targets for this domain,
the sections that judge against targets (Outliers Detected, and Progression
Analysis where the domain has a curve) are `NOT ASSESSED — NO DATA`. Each one names what was missing — the
GDD it looked for in `design/gdd/`, and whether the registry was absent or empty
— and names `$studio-design-system`, which writes both.

---

## Phase 4: Perform Analysis

**Every domain: compare each value with its target.** For each named value in the
data files, take its target from Phase 3 — a registry constant's `value`, a
registry formula's `output_range`, or the range the GDD states — and compare. A
value outside its target is a row in Outliers Detected (`player_damage_base` 140
against 90–110). A value with no target anywhere is neither in range nor an
outlier: list it under Values That Need Attention as `no stated range — not judged`.

Then run domain-specific checks:

**Combat balance:**
- Calculate DPS for all weapons/abilities at each power tier
- Check time-to-kill at each tier
- Identify any options that dominate all others (strictly better)
- Check if defensive options can create unkillable states
- Verify damage type/resistance interactions are balanced

**Economy balance:**
- Map all resource faucets and sinks with flow rates
- Project resource accumulation over time
- Check for infinite resource loops
- Verify gold sinks scale with gold generation
- Check if any items are never worth purchasing

**Progression balance:**
- Plot the XP curve and power curve
- Check for dead zones (no meaningful progression for too long)
- Check for power spikes (sudden jumps in capability)
- Verify content gates align with expected player power
- Check if skip/grind strategies break intended pacing

**Loot balance:**
- Calculate expected time to acquire each rarity tier
- Check pity timer math
- Verify no loot is strictly useless at any stage
- Check inventory pressure vs acquisition rate

---

## Phase 5: Output the Analysis

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [NOT ASSESSED / HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

Choose the Health Summary by the worst finding, first match wins:
- **CRITICAL ISSUES** — a degenerate strategy (one choice dominates every
  alternative), a progression that stalls or cannot be completed, or an economy
  loop with no sink
- **CONCERNS** — outliers or curve problems a tuning pass can fix, with no
  finding of the critical kind
- **NOT ASSESSED** — nothing to analyze (the no-data path above), a section that
  needs targets is `NOT ASSESSED — NO DATA`, or a value had no stated range to
  judge it against; name which. It ranks below the two finding verdicts, because
  a measured problem is more actionable than a gap, and above HEALTHY
- **HEALTHY** — every value judged against a stated target, no outliers, no
  degenerate strategies, progression within the stated targets

---

## Phase 6: Fix & Verify Cycle

After presenting the report, use `AskUserQuestion`:
- Prompt: "Balance check complete. What would you like to do next?"
- Options:
  - `[A] Fix highest-priority issue now — walk me through it`
  - `[B] Save report to design/balance/balance-check-[system]-[date].md`
  - `[C] Stop here — I'll review the findings manually`

If [A]:
- Ask which issue to address first (refer to the Recommendations table by priority row)
- Guide the user to update the relevant data file in `assets/data/` or formula in `design/balance/`
- After each fix, offer to re-run the relevant balance checks to verify no new outliers were introduced
- If the fix changes a tuning knob defined in a GDD or referenced by an ADR, remind the user:
  > "This value is defined in a design document. Run `$studio-propagate-design-change [path]` on the affected GDD to find downstream impacts before committing."

If [B]:
- Write the report to `design/balance/balance-check-[system]-[date].md` (create the directory if needed). Use the current date for [date] in YYYY-MM-DD format.
- Confirm the file was written, then end with: "Re-run `$studio-balance-check` after fixes to verify."

If [C]:
- Summarize open issues and end with: "Re-run `$studio-balance-check` after fixes to verify."
