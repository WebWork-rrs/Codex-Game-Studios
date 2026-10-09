---
name: studio-bug-triage
description: "Re-evaluate open bugs — priority vs severity, assign to sprints, surface systemic trends. Run when the count grows."
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


**Execute before proceeding** (from the repository root):

```bash
bash ".claude/hooks/yaml-helper.sh" resolve_config --keys automation,workflow
```
**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `AskUserQuestion` call and
every file write follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

# Bug Triage

This skill processes the open bug backlog into a prioritised, sprint-assigned
action list. It distinguishes between **severity** (how bad is the impact?) and
**priority** (how urgently must we fix it?), detects systemic trends, and
ensures no critical bug is lost between sprints.

**Output:** `production/qa/bug-triage-[date].md`

**When to run:**
- Sprint start — assign open bugs to the new sprint or backlog
- After `$studio-team-qa` completes and new bugs have been filed
- When the bug count crosses 10+ open items

---

## 1. Parse Arguments

**Modes:**
- `$studio-bug-triage sprint` — triage against the current sprint; assign fixable bugs
  to the sprint backlog; defer the rest
- `$studio-bug-triage full` — full triage of all bugs regardless of sprint scope
- `$studio-bug-triage trend` — trend analysis only (no assignment); read-only report
- No argument — run sprint mode if a current sprint exists, else full mode

---

## 2. Load Bug Backlog

### Step 2a — Discover bug files

Glob for bug reports in priority order:
1. `production/qa/bugs/*.md` — individual bug report files (preferred format)
2. `production/qa/bugs.md` — single consolidated bug log (fallback)
3. Any `production/qa/qa-plan-*.md` "Bugs Found" table (last resort)

If no bug files found:
> "No bug files found in `production/qa/bugs/`. If bugs are tracked in a
> different location, adjust the glob pattern. If no bugs exist yet, there is
> nothing to triage."

Stop and report. Do not proceed if no bugs exist. Verdict: **COMPLETE** — no bug files in `production/qa/bugs/`; nothing to triage.

**In `trend` mode, do not read full bug bodies.** Trend metrics (volume, severity
mix, by-system, by-date) are computable from the header fields alone:
```
Grep pattern="\*\*(Severity|Priority|Status|System|Category|Reported)\*\*" glob="production/qa/bugs/*.md" output_mode="content"
```
(Bug-report fields are bolded — `**Severity**:`, `- **System**:` — so match the
`**field**` form, not a bare line-start `Field:`.)
Full bug bodies are needed only for the priority-vs-severity **re-evaluation** in
`sprint`/`full` modes; `trend` is a read-only report and skips it. (The one
deviation check that needs a story's status — "bug filed against a Complete
story" — is a targeted story-status grep either way, not a bug-body read.)

### Step 2b — Load sprint context

Read the most recently modified file in `production/sprints/` to understand:
- Current sprint number / name
- Stories in scope (for assignment target)
- Sprint capacity constraints (if noted)

If no sprint file exists: note "No sprint plan found — assigning to backlog only." At `workflow: minimal` there are no sprints by design — say that instead, and name the P1 bugs as the next fixes, ahead of the next story in the brief's build order.

### Step 2c — Load severity reference

Read `.claude/docs/coding-standards.md` for severity/priority definitions if they
exist. If they do not exist, use the standard definitions in Step 3.

---

## 3. Classify Each Bug

For each bug, extract or infer:

### Severity (impact of the bug)

| Severity | Definition |
|----------|-----------|
| **S1 — Critical** | Game crashes, data loss, or complete feature failure. Cannot proceed past this point. |
| **S2 — High** | Major feature broken but game is still playable. Significant wrong behaviour. |
| **S3 — Medium** | Feature degraded but a workaround exists. Minor wrong behaviour. |
| **S4 — Low** | Visual glitch, cosmetic issue, typo. No gameplay impact. |

### Priority (urgency of the fix)

| Priority | Definition |
|----------|-----------|
| **P1 — Fix this sprint** | Blocks QA, blocks release, or is regression from last sprint |
| **P2 — Fix soon** | Should be resolved before the next major milestone |
| **P3 — Backlog** | Would be good to fix, but no active blocking impact |
| **P4 — Won't fix / Deferred** | Accepted risk or out of scope for current product scope |

### Assignment

For each P1/P2 bug in `sprint` mode:
- Identify which story or epic the fix belongs to
- Check whether the current sprint has remaining capacity
- If capacity exists: assign to sprint (`Sprint: [current]`)
- If capacity is full: flag as `Priority overflow — consider pulling from sprint`

For `full` mode: assign all P1 to current sprint, P2 to next sprint estimate,
P3+ to backlog.

### Deviation check

Flag bugs that suggest **systematic problems**:
- 3+ bugs from the same system in the same sprint → "Potential design or
  implementation quality issue in [system]"
- 2+ S1/S2 bugs in the same story → "Story may need to be reopened and
  re-reviewed before shipping"
- Bug filed against a story marked Complete → "Regression in completed story —
  story should be re-opened in sprint tracking"

---

## 4. Trend Analysis

After classifying all bugs, generate trend metrics:

### Volume trends
- Total open bugs: [N]
- Opened this sprint: [N]
- Closed this sprint: [N]
- Net change: [+N / -N]

### System hot spots
- Which system has the most open bugs?
- Which system has the highest S1/S2 ratio?

### Age analysis
- How many bugs are older than 2 sprints?
- Are any S1/S2 bugs un-assigned (sprint = none)?

### Regression indicator
- Any bugs filed against previously-completed stories?
- Count: [N] regression bugs (story reopened implied)

---

## 5. Generate Triage Report

```markdown
# Bug Triage Report

> **Date**: [date]
> **Mode**: [sprint | full | trend]
> **Generated by**: $studio-bug-triage
> **Open bugs processed**: [N]
> **Sprint in scope**: [sprint name, or "N/A"]

---

## Triage Summary

| Priority | Count | Notes |
|----------|-------|-------|
| P1 — Fix this sprint | [N] | [N] assigned to sprint, [N] overflow |
| P2 — Fix soon | [N] | Scheduled for next sprint |
| P3 — Backlog | [N] | Deferred |
| P4 — Won't fix | [N] | Accepted risk |

**Critical (S1/S2) unfixed count**: [N]

---

## P1 Bugs — Fix This Sprint

| ID | System | Severity | Summary | Assigned to | Story |
|----|--------|----------|---------|-------------|-------|
| BUG-NNNN | [system] | S[1-4] | [one-line description] | [sprint] | [story path] |

---

## P2 Bugs — Fix Soon

| ID | System | Severity | Summary | Target Sprint |
|----|--------|----------|---------|---------------|
| BUG-NNNN | [system] | S[1-4] | [one-line description] | Sprint [N+1] |

---

## P3/P4 Bugs — Backlog / Won't Fix

| ID | System | Severity | Summary | Disposition |
|----|--------|----------|---------|-------------|
| BUG-NNNN | [system] | S4 | [one-line description] | Backlog |

---

## Systemic Issues Flagged

[List any patterns from Step 3 deviation check, or "None identified."]

---

## Trend Analysis

**Volume**: [N] open / [+N] net change this sprint
**Hot spot**: [system with most bugs]
**Regressions**: [N] bugs against completed stories
**Aged bugs (>2 sprints old)**: [N]

[If N aged S1/S2 bugs > 0:]
> ⚠️ [N] high-severity bugs have been open for more than 2 sprints without
> assignment. These represent accepted risk that should be explicitly reviewed.

---

## Recommended Actions

1. [Most urgent action — usually "fix P1 bugs before QA hand-off"]
2. [Second action — usually "investigate [hot spot system] quality"]
3. [Third action — optional improvement]
```

---

## 6. Write and Gate

Present the report in conversation. If any bug is a P4 candidate, first ask
"Are these acceptable as Won't Fix?" and keep its disposition `P4 candidate`
until the user answers. Then ask:

"May I write this triage report to `production/qa/bug-triage-[date].md`?"

Write only after approval.

After writing:
- If any S1 bugs are unassigned: "S1 bugs must be assigned before the sprint
  can be considered healthy. Run `$studio-sprint-status` to see current capacity."
- If regression bugs exist: "Regressions found — consider re-opening the
  affected stories in sprint tracking and running `$studio-smoke-check` to re-gate."
- If no P1 bugs exist: "No P1 bugs — build is in good shape for QA hand-off."

Then, whether or not P1 bugs exist: Verdict: **COMPLETE** — triage report written.

If user declined write: Verdict: **BLOCKED** — user declined write.

---

## Collaborative Protocol

- **Never close or mark bugs Won't Fix without user approval** — surface them
  as P4 candidates and ask: "Are these acceptable as Won't Fix?"
- **Never auto-assign to a sprint at capacity** — flag overflow and let the
  sprint owner decide what to pull
- **Severity is objective; priority is a team decision** — present severity
  classifications as recommendations, not mandates
- **Trend data is informational** — do not block work on trend findings alone;
  surface them as observations
