---
name: sprint-plan
description: "New or updated sprint plan from the current milestone, completed work, and available capacity."
argument-hint: "[new|update|status] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Agent, AskUserQuestion, Bash(bash "*/.claude/skills/sprint-plan/../../hooks/yaml-helper.sh" resolve_config *)
model: sonnet
---

!`bash "${CLAUDE_SKILL_DIR}/../../hooks/yaml-helper.sh" resolve_config --keys review_mode,automation,story_granularity,workflow,qa.level,engine.name,engine.version`

Resolved above — use as-is; `--review` overrides `review_mode`. No block →
defaults in `.claude/docs/config-resolution.md`.

# Sprint Plan


## Existing Sprints

!`ls production/sprints/ 2>/dev/null || echo "(no production/sprints/ directory yet)"`

Resolved before this skill runs — use it to identify the previous sprint in
Phase 1 rather than re-globbing.

---

## Phase 0: Parse Arguments

Extract the mode argument (`new`, `update`, or `status`).

See `.claude/docs/director-gates.md` for the full check pattern. Individual gate definitions live in `.claude/docs/director-gates/[gate-id].md` — the spawned agent reads its own gate file; do not read it in the parent session.


Every `AskUserQuestion` call follows `.claude/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).
Apply the user's existing authorization first: routine reversible work already
authorized does not need another per-file write ask. Ask for unresolved design
choices, material scope changes, or work outside that authorization.

**`story_granularity`** — it sets how
many stories to allocate per sprint, scaled by velocity: **2–4** at `coarse` (the default, via `rigor: minimal`),
**6–10** at `balanced` (`rigor: standard`), **15–25** at `fine`. A Ready backlog
smaller than the range is planned whole — never padded with invented stories.

**Review mode check** (before gates run):
- Use the review mode from the resolved block above (`--review` overrides it
  for this run) — do not re-resolve it, and do not ask for it. With nothing
  configured it follows `modes.rigor`: `solo` at `minimal`, `lean` at `standard`.
- **Never write a review mode** — not to `project.yaml`, not to
  `production/review-mode.txt`. `modes.review_mode` is one of the knobs
  `modes.rigor` fronts: pinning it in `project.yaml` shadows the rigor
  expansion, and the legacy file sits *above* that expansion, so either write
  would freeze director-review depth for good. `--review` covers a one-off. If
  the user wants a different depth to persist, point them to changing
  `modes.rigor` (`/settings modes.rigor=<minimal|standard|full>`), or to pinning
  it on purpose with `/settings --local modes.review_mode=<full|lean|solo>` (a
  personal override in `project.local.yaml`).

---

## Phase 1: Gather Context

1. **Read the current milestone** from `production/milestones/` **if it exists**.
   No skill writes this directory — it is authored by hand from
   `.claude/docs/templates/milestone-definition.md`. On the majority of projects
   it is absent, which is the normal state, not a gap: note "no milestone
   defined — planning against the story backlog alone" and continue. Never block
   sprint planning on it, and never infer a milestone from the sprint files.

2. **Read the previous sprint** (if any) from `production/sprints/` to
   understand velocity and carryover. In `new` mode:
   - The new sprint's number `[N]` is the highest `sprint-NNN.md` in the
     Existing Sprints listing plus one (`001` when there is none). It is the
     `[N]` in the plan's title, its QA plan path and the write ask.
   - Every story of the previous sprint that is not `Complete` — by its status
     in `production/sprint-status.yaml`, else its story file's Status line —
     goes in the Carryover table with a Reason and a New Estimate. It appears
     only there, never again as new Must Have / Should Have / Nice to Have work.

3. **Find the stories to plan** — this is the actual backlog, and it is the one
   input this phase cannot do without:
   ```
   Glob production/epics/**/story-*.md
   Grep pattern="^> \*\*Status\*\*" glob="production/epics/**/story-*.md" output_mode="content"
   ```
   Stories live at `production/epics/[epic-slug]/story-NNN-[slug].md` — that is
   where `/create-stories` writes them and where `/dev-story` looks for them. Plan
   from the ones marked `Ready`. Use the grep rather than reading each story: at
   this stage you need status and title, not the body.

   If the glob returns nothing: "No stories found under `production/epics/`. Run
   `/create-stories` first (at `standard`/`full`, `/create-epics` before it)."
   Do not proceed to invent work items — a sprint plan that references stories
   which do not exist cannot be implemented. Verdict: **BLOCKED** — no stories to plan.

4. **Scan design documents** in `design/gdd/` for additional context on the
   features those stories implement. At `workflow: minimal` there are no
   per-system GDDs — use `design/game-brief.md` instead, and do not treat the
   absent GDDs as missing work. (Note: `/sprint-plan` is **optional** at
   `minimal` — the brief's Build order already is the plan.)

5. **Check the risk register** at `production/risk-register/` **if it exists**.
   Like the milestone above, no skill writes it — entries are authored by hand
   from `.claude/docs/templates/risk-register-entry.md`. If the directory is
   absent, say so once ("no risk register — risks assessed from the sprint
   contents only") rather than skipping risk assessment silently.

---

## Phase 1b: Sprint Goal Prerequisites

**Required for `new` and `update` in every review mode (`solo`, `lean`, `full`).**
This is a direct planning check, not an extra producer spawn. `status` remains
read-only. At `minimal`, sprint planning is still optional; when invoked, keep
this check to the proposed goal and its critical path.

1. **State the demonstrable goal** from the milestone, brief/GDD, and requested
   changes: what can a player or reviewer do at sprint end, in which scene,
   build, or test harness, and what observable result proves it? A logic-only
   sprint can demonstrate behavior in a harness; a playable-demo goal needs a
   runnable player flow. Story titles and a Ready status alone do not establish
   either goal. Read the candidate stories' acceptance criteria and dependencies.

2. **Inspect the actual project** for prerequisites implied by that goal:
   runnable scene/level and entry point, player input and control wiring,
   necessary assets/data (including acceptable placeholders), build/run path,
   verification harness, and configuration. Resolve roots from `engine.name`:
   Godot `src/` and `tests/` plus `project.godot`; Unity `Assets/`,
   `Assets/Tests/`, and `ProjectSettings/`; Unreal `Source/<Module>/`, its test
   directories, `Content/`, `Config/`, and the `.uproject`. Follow referenced
   scenes, input maps, assets, and runner settings to their real paths; do not
   infer absence from a search confined to another engine's roots. If the engine
   or access is unavailable, name exactly what could not be inspected.
   Derive required rows from the goal, not a fixed checklist of unrelated systems.

3. **Prepare the required prerequisite table** used in Phase 2. Every required
   prerequisite is one of:
   - **PRESENT** — inspected source/configuration path and relevant behavior;
     distinguish inspected wiring from a run actually observed.
   - **PLANNED** — an existing selected Must Have or carryover story's real ID
     and path, acceptance criteria that deliver the prerequisite, estimate, and
     dependency order before its consumers and the end-of-sprint demonstration.
     The ordered work must fit capacity. An absent scene or input map is valid
     planned work when such a story delivers it this sprint; it is not blocked
     merely because implementation has not started.
   - **MISSING** — inspection found it absent and no selected story delivers it,
     or the dependency order/capacity cannot deliver it in time.
   - **NOT ASSESSED** — inspection could not run; name the missing input, access,
     or tool and its effect on the goal. Unknown is not PRESENT or PLANNED.
   For a category irrelevant to this goal, state `N/A — [reason]`; do not make
   every sprint require a playable scene or production art.

4. **Resolve gaps before claiming feasibility.** For MISSING rows, revise the
   goal to a supported deliverable or select/create actual implementable
   prerequisite stories via `/create-stories` within the authorized scope, then
   re-read their saved files and re-run this check. Do not add invented IDs or
   placeholder tasks to make the table look complete. Ask only for missing design
   decisions or a material scope/capacity change not already authorized.
   Until repaired, verdict **BLOCKED**; no final plan write. If a required input
   cannot be inspected, verdict **NOT ASSESSED** with the reason; a provisional
   plan may record that limitation but must not claim the goal is feasible or
   playable. Otherwise verdict **FEASIBLE AS PLANNED**, not proof the game runs.
   Aggregate precedence: **BLOCKED > NOT ASSESSED > FEASIBLE AS PLANNED**.

Re-run Phase 1b after any goal, selected-story, dependency, or capacity change,
including update requests and producer revisions. All writes converge on Phase
5; its final check must use this table for the final scope.

---

## Phase 2: Generate Output

For `new`:

**Generate a sprint plan** following this format and present it to the user. Do NOT ask to write yet — the Phase 1b prerequisite check (all modes), producer feasibility gate (Phase 4, spawned only in `full` review mode — skipped in `lean`/`solo`), and QA plan check (Phase 5, all modes) may require revisions before the file is written.
Scale the Definition of Done to the resolved `qa.level` and workflow: at
`minimal`, automated tests are waived/advisory, not a new planning blocker.
Record waived or inapplicable checks by name; player-visible delivery still
needs a run observed and retained evidence, not only a parse check.

```markdown
# Sprint [N] — [Start Date] to [End Date]

## Sprint Goal
[One sentence describing the observable end-of-sprint demonstration]

## Goal Prerequisites (Required — Phase 1b)
| Prerequisite | Status | Evidence path or selected story ID/path and acceptance criteria | Dependency order / capacity | Gap or assessment limitation |
|--------------|--------|----------------------------------------------------------------|-----------------------------|-----------------------------|

**Prerequisite verdict:** [FEASIBLE AS PLANNED / BLOCKED / NOT ASSESSED — reason]
**Demonstration / verification path:** [scene/build/harness and observable result;
state what was inspected, what was run, and what remains unverified]

## Capacity
- Total days: [X]
- Buffer (20%): [Y days reserved for unplanned work]
- Available: [Z days]

## Tasks

### Must Have (Critical Path)
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Should Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

### Nice to Have
| ID | Task | Agent/Owner | Est. Days | Dependencies | Acceptance Criteria |
|----|------|-------------|-----------|-------------|-------------------|

## Carryover from Previous Sprint
| Task | Reason | New Estimate |
|------|--------|-------------|

## Risks
| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|

## Dependencies on External Factors
- [List any external dependencies]

## Definition of Done for this Sprint
- [ ] All Must Have tasks completed
- [ ] All tasks pass acceptance criteria
- [ ] QA plan exists (`production/qa/qa-plan-[sprint-slug]-[date].md`, from `/qa-plan sprint`)
- [ ] All Logic/Integration stories have passing unit/integration tests
- [ ] Smoke check passed (`/smoke-check sprint`)
- [ ] QA sign-off report: APPROVED or APPROVED WITH CONDITIONS (`/team-qa sprint`)
- [ ] No S1 or S2 bugs in delivered features
- [ ] Design documents updated for any deviations
- [ ] Code reviewed and merged
```

For `update`:

**Update an existing sprint plan**:

1. Read the most recent sprint plan from `production/sprints/`.
2. Present the current story list with their current statuses from `production/sprint-status.yaml`.
3. Apply changes already requested; use `AskUserQuestion` only if the intended changes need clarification.
4. Re-run Phase 1b for the revised goal and story selection; add or refresh the required prerequisite table even if the old plan lacks one. Re-present the full revised plan for review.
5. Prepare the revised status yaml (Phase 3) and run Phase 4 according to review mode.
6. Run Phase 5 on the revised scope, then write both files only through its final write check (same authorization rules as `new`). There is no direct update write shortcut.

Note: `update` mode does not reset story statuses. Stories already marked `in-progress` or `done` keep their status. Only `backlog` and `ready-for-dev` stories can be removed or reprioritized freely.

For `status`:

**Generate a status report**:

```markdown
# Sprint [N] Status -- [Date]

## Progress: [X/Y tasks complete] ([Z%])

### Completed
| Task | Completed By | Notes |
|------|-------------|-------|

### In Progress
| Task | Owner | % Done | Blockers |
|------|-------|--------|----------|

### Not Started
| Task | Owner | At Risk? | Notes |
|------|-------|----------|-------|

### Blocked
| Task | Blocker | Owner of Blocker | ETA |
|------|---------|-----------------|-----|

## Burndown Assessment
[On track / Behind / Ahead]
[If behind: What is being cut or deferred]

## Emerging Risks
- [Any new risks identified this sprint]
```

---

## Phase 3: Prepare Sprint Status File

After generating a new sprint plan, also prepare the `production/sprint-status.yaml` content.
This is the machine-readable source of truth for story status — read by
`/sprint-status`, `/story-done`, and `/help` without markdown parsing.

**Do not write the yaml yet** — hold it in context. The producer feasibility gate (Phase 4, `full` review mode only) may revise the story list; re-run Phase 1b for those revisions. The QA plan check (Phase 5) runs in every mode. Both files are written together only through Phase 5's final write check.

Format:

```yaml
# Auto-generated by /sprint-plan. Updated by /story-done and /dev-story.
# DO NOT edit manually — use /story-done to update story status.
#
# Status value mapping (yaml ↔ story file Status field):
#   backlog        ↔  Not Started
#   ready-for-dev  ↔  Ready
#   in-progress    ↔  In Progress
#   review         ↔  In Review
#   done           ↔  Complete
#   blocked        ↔  Blocked

sprint: [N]
goal: "[sprint goal]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

stories:
  - id: "[epic-story, e.g. 1-1]"
    name: "[story name]"
    file: "[production/epics/[epic-slug]/story-NNN-[slug].md]"   # the real path, verbatim from the Glob above
    priority: must-have        # must-have | should-have | nice-to-have
    status: ready-for-dev      # backlog | ready-for-dev | in-progress | review | done | blocked
    owner: ""
    estimate_days: 0
    blocker: ""
    completed: ""
```

Initialize each story from the sprint plan's task tables:
- Must Have tasks → `priority: must-have`, `status: ready-for-dev`
- Should Have tasks → `priority: should-have`, `status: backlog`
- Nice to Have tasks → `priority: nice-to-have`, `status: backlog`
- Carryover rows → the story's previous `priority`, and the `status` it has now

For `update`: read the existing `sprint-status.yaml`, carry over statuses for
stories that haven't changed, add new stories, remove dropped ones.

---

## Phase 4: Producer Feasibility Gate

**Review mode check** — apply before spawning PR-SPRINT:
- `solo` → skip. Note: "PR-SPRINT skipped — Solo mode." Proceed to Phase 5 (QA plan gate).
- `lean` → skip (not a PHASE-GATE). Note: "PR-SPRINT skipped — Lean mode." Proceed to Phase 5 (QA plan gate).
- `full` → spawn as normal.

Before finalising the sprint plan, spawn `producer` via `Agent` using gate **PR-SPRINT** (`.claude/docs/director-gates/pr-sprint.md`).

Pass: proposed story list (titles, estimates, dependencies), the Phase 1b goal/prerequisite table and verdict, total team capacity in hours/days, any carryover from the previous sprint, milestone constraints and deadline.

Present the producer's assessment.

If UNREALISTIC: revise the story selection (defer stories to Should Have or Nice to Have) and re-present the updated plan, then continue to Phase 5.

If NOT ASSESSED: name the missing input — it is not REALISTIC. Supply it and re-run PR-SPRINT, or record `NOT ASSESSED — [missing input]` for PR-SPRINT in the plan's header (`.claude/docs/director-gates.md`) and continue to Phase 5, repeating it at the write ask.

If CONCERNS, use `AskUserQuestion`:
- Prompt: "Producer flagged concerns with this sprint plan. How do you want to proceed?"
- Options:
  - `[A] Proceed as planned — I accept the risk`
  - `[B] Adjust scope — defer some Should Have stories`
  - `[C] Extend the sprint timeline`

If [A]: continue to Phase 5.
If [B]: revise the story list, re-present the updated plan, then continue to Phase 5.
If [C]: adjust sprint dates and capacity, re-present the updated plan, then continue to Phase 5.

After handling the producer's verdict, re-run Phase 1b for any changed scope,
dependencies, or capacity, and refresh the draft yaml. Then continue to Phase 5.
The write comes at its end, so the file you review already holds everything
Phase 5 adds. PR-SPRINT cannot override a BLOCKED or NOT ASSESSED prerequisite.

---

## Phase 5: QA Plan Gate

Before closing the sprint plan, check whether a QA plan exists for this sprint.

Use `Glob` for `production/qa/qa-plan-*.md` — `/qa-plan` writes `qa-plan-[sprint-slug]-[date].md` — and keep a file whose name or content references this sprint number.

**If a QA plan is found**: read its relevant sections and confirm it covers the
final selected stories and demonstration path. Record "QA Plan: `[path]`" and
any coverage gaps; file existence does not prove runnable prerequisites or
passing QA. Missing coverage needs a QA-plan update before implementation.

**If QA-plan discovery or reading could not run**: record `QA plan check: NOT
ASSESSED — [access/input/tool]` and the unverified coverage in the plan. Do not
report that no plan exists or that the check passed. A provisional write must
carry this limitation and cannot claim implementation readiness.

**If no QA plan exists**: do not silently proceed. Surface this explicitly:

> "This sprint has no QA plan. A sprint plan without a QA plan means test requirements are undefined — developers won't know what 'done' looks like from a QA perspective, and the sprint cannot pass the Production → Polish gate without one.
>
> Run `/qa-plan sprint` now, before starting any implementation. It takes one session and produces the test case requirements each story needs."

Use `AskUserQuestion`:
- Prompt: "No QA plan found for this sprint. How do you want to proceed?"
- Options:
  - `[A] Run /qa-plan sprint now — I'll do that before starting implementation (Recommended)`
  - `[B] Skip for now — I understand QA sign-off will be blocked at the Production → Polish gate`

If this decision requires an answer under the automation rules and existing
authorization, wait for it before writing. Missing QA remains explicitly
unresolved; choosing a follow-up is not a passed QA check.

If [A]: note in the plan "QA plan: run `/qa-plan sprint` before implementation begins."
If [B]: add a warning block to the sprint plan document:

```markdown
> ⚠️ **No QA Plan**: This sprint was started without a QA plan. Run `/qa-plan sprint`
> before implementation begins. The Production → Polish gate requires a QA
> sign-off report, which requires a QA plan.
```

### Write the plan

**Final write check — required for every `new`/`update`, including authorized
direct writes:** the final markdown must contain the Phase 1b table, evidence,
verdict, and demonstration path, consistent with the final yaml/story list and
capacity. Re-run stale or skipped checks. A MISSING prerequisite or BLOCKED
verdict stops the write until repaired. NOT ASSESSED prerequisites or unresolved
QA may be written only as an explicitly provisional plan with the reasons,
named evidence still blocking readiness, and required follow-up. NOT ASSESSED
prerequisites cannot support a feasible/playable claim; unresolved QA cannot
support a QA pass or implementation-readiness claim.

Present the final plan and its limitations. If the write is already authorized,
write `production/sprints/sprint-NNN.md` (`[N]` zero-padded to three digits) and
`production/sprint-status.yaml` together (creating directories as needed).
Otherwise apply the automation rules and ask, when required: "May I write the
sprint plan to `production/sprints/sprint-NNN.md` and
`production/sprint-status.yaml`?" An unanswered required ask does not authorize
writing. Verdict: **COMPLETE** — plan and status file written, naming any
provisional limitations; this is not a gameplay or QA pass. If declined:
**BLOCKED** — user declined write.

After writing, add:

> **Scope check:** If this sprint includes stories added beyond the original epic scope, run `/scope-check [epic]` to detect scope creep before implementation begins.

If the user chose `Run /qa-plan sprint now` in Phase 5, close with "Sprint plan written. Run `/qa-plan sprint` next — then begin implementation."

---

## Phase 6: Next Steps

After the sprint plan is written and QA plan status is resolved:

- `/qa-plan sprint` — **required before implementation begins** — defines test cases per story so developers implement against QA specs, not a blank slate
- `/story-readiness [story-file]` — validate a story is ready before starting it
- `/dev-story [story-file]` — begin implementing the first story
- `/sprint-status` — check progress mid-sprint
- `/scope-check [epic]` — verify no scope creep before implementation begins

**Review mode configuration:** All director gates (producer feasibility, QA review, code review) respect the project review mode, resolved in the block at the top of this skill (`--review` flag → `project.local.yaml` → `modes.review_mode` in `project.yaml` → `production/review-mode.txt` → the `modes.rigor` expansion, which yields `lean` at standard rigor and `solo` at minimal). This skill never asks for it or writes it; Phase 0 says where to point a user who wants a different depth. The mode is one of:
- `lean` — skip non-phase-gate director gates (the `rigor: standard` value)
- `full` — run all director gates as spawned sub-agents
- `solo` — skip all gate spawning unconditionally (single developer, no review)

`modes.review_mode` in `project.yaml` is the primary source; `production/review-mode.txt` is the legacy fallback. Both are read by `/sprint-plan`, `/story-readiness`, `/story-done`, and other gate-using skills at startup.
