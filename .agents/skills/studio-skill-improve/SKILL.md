---
name: studio-skill-improve
description: "Improve a skill via a test-fix-retest loop — static checks, targeted fixes, keep or revert on score change."
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
**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `AskUserQuestion` call and
every file write follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

# Skill Improve

Runs an improvement loop on a single skill:
test → fix → retest → keep or revert.

---

## Phase 1: Parse Argument

Read the skill name from the first argument. If missing, output usage and stop:

```
Usage: $studio-skill-improve [skill-name]
Example: $studio-skill-improve tech-debt
```

Verify `.claude/skills/[name]/SKILL.md` exists. If not, stop with:
"Skill '[name]' not found."

---

## Phase 2: Baseline Test

Run `$studio-skill-test static [name]` and record the baseline score:
- Count of FAILs
- Count of WARNs
- Which specific checks failed (Check 1–7)

Display to the user:
```
Static baseline:   [N] failures, [M] warnings
Failing: Check 4 (no ask-before-write), Check 5 (no handoff)
```

If the static result is **NOT ASSESSED** (the skill file could not be read or
parsed), stop and report it with its reason: there is no score to improve, and
0 FAILs from a file nobody could read is not a clean result.

If baseline is 0 FAILs and 0 WARNs, note it and proceed to Phase 2b.

### Phase 2b: Category Baseline

Look up the skill's `category:` field in `CCGS Skill Testing Framework/catalog.yaml`.

If no `category:` field is found, display:
"Category: not yet assigned — skipping category checks."
and skip to Phase 3.

If category is found, run `$studio-skill-test category [name]` and record the category baseline:
- Count of FAILs
- Count of WARNs
- Which specific category rubric metrics failed

Display to the user:
```
Category baseline: [N] failures, [M] warnings  ([category] rubric)
```

A category result of **NOT ASSESSED** (a rubric section the skill-test could not
find or apply) is reported with its reason and is not a zero: the category
dimension is then excluded from "already passes" below.

If BOTH static and category baselines are 0 FAILs and 0 WARNs — and neither is
NOT ASSESSED — stop:
"This skill already passes all static and category checks. No improvements needed."

---

## Phase 3: Diagnose

Read the full skill: `.claude/skills/[name]/SKILL.md` and every file in its `references/` folder,
if it has one — the longest skills keep each phase there. Name the file each
gap is in.

For each failing or warning **static** check, identify the exact gap:

- **Check 1 fail** → which frontmatter field is missing
- **Check 2 fail** → how many phases found vs. minimum required
- **Check 3 fail** → no verdict keywords anywhere in the skill body
- **Check 4 fail** → Write or Edit in allowed-tools but no ask-before-write language
- **Check 5 warn** → no follow-up or next-step section at the end
- **Check 6 warn** → `context: fork` set but fewer than 5 phases found
- **Check 7 warn** → argument-hint is empty or doesn't match documented modes

For each failing or warning **category** check (if category was assigned in Phase 2b),
identify the exact gap in the skill's text. For example:
- If G2 fails (gate mode, director panel width): skill body does not size the
  PHASE-GATE panel from `modes.workflow` (PR at `minimal`, TD + PR at `standard`,
  all 4 at `full`)
- If A2 fails (authoring, no per-section May-I-write): skill asks once at the end, not
  before each section write
- If T3 fails (team, BLOCKED not surfaced): skill doesn't halt dependent work on blocked agent

Show the full combined diagnosis to the user before proposing any changes.

---

## Phase 4: Propose Fix

Write a targeted fix for each failure and warning. Show the proposed changes
as clearly marked before/after blocks. Only change what is failing — do not
rewrite sections that are passing. In a skill with a `references/` folder, a
fix to a phase's steps goes in that phase's `references/` file, not back into
`SKILL.md`; the question below then names each file the fix changes.

Ask: "May I write this improved version to `.claude/skills/[name]/SKILL.md`?"

If the user says no, stop here.

---

## Phase 5: Write and Retest

Record the current content of each file the fix changes — the exact text, kept
in this conversation — so Phase 6 can restore it.

Write the improved skill to `.claude/skills/[name]/SKILL.md`, and to each
`references/` file the fix changes.

Re-run `$studio-skill-test static [name]` and record the new static score — measured by that run, never stated from the edit.
If a category was assigned, also re-run `$studio-skill-test category [name]` and record the new category score.

Display the comparison:
```
Static:   Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings
Category: Before [N] failures, [M] warnings  →  After [N'] failures, [M'] warnings  (if applicable)
Combined: [before] → [after] (improved / no change / worse)
```

`[before]` and `[after]` are the Phase 6 combined counts — failures plus
warnings, both dimensions — e.g. `Combined: 3 → 0 (improved)`.

---

## Phase 6: Verdict

Count the combined failure total: static FAILs + category FAILs + static WARNs + category WARNs.
**A re-test that comes back NOT ASSESSED** (for example, the edit broke the
frontmatter so the file no longer parses) is never an improvement, whatever its
counts: take the "did not improve" branch below.

**If combined score improved (combined failure count is lower than baseline):**
Report: "Score improved. Changes kept."
Show a summary of what was fixed in each dimension.

**If combined score is the same or worse:**
Report: "Combined score did not improve."
Show what changed and why it may not have helped.
Ask: "May I restore `.claude/skills/[name]/SKILL.md` to the content it had before this run?"
— naming every file Phase 5 wrote.
If yes: write the content recorded in Phase 5 back to each file with Write; if no, leave the files as written. Never
`git checkout` it — that returns the last *committed* version and discards any edits
made before this run that were not yet committed.

---

## Phase 7: Next Steps

- Run `$studio-skill-test static all` to find the next skill with failures.
- Run `$studio-skill-improve [next-name]` to continue the loop on another skill.
- Run `$studio-skill-test audit` to see overall coverage progress.
