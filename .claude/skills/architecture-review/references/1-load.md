# /architecture-review — Phase 1: Load Everything

> Part of `/architecture-review`. `SKILL.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## Phase 1: Load Everything

**In this file:**

- Phase 1a — L0: Summary Scan (fast, low tokens)
- Phase 1b — L1/L2: Targeted Section Load
- Design Documents
- Architecture Documents
- Engine Reference
- Project Standards

### Phase 1a — L0: Summary Scan (fast, low tokens)

**Freshness check before any scan.** Locate the latest prior report — Glob
`docs/architecture/architecture-review-*.md` and take the newest — then:

```
Bash: bash .claude/scripts/review-receipts.sh check "[latest-report]" docs/architecture/adr-*.md design/gdd/*.md
```

- **Any `UNRESOLVED`** — check this FIRST; it disqualifies every option
  below. One of the two globs matched no file, so that whole document class
  was never examined and the comparison covered less than it appears to.
  Say which pattern came back unresolved and stop: an ADR or GDD directory
  that is empty, renamed or misspelled is a finding about the project, not a
  reason to stand on a prior report. Never read a set of `UNCHANGED` lines as
  "everything is current" while an `UNRESOLVED` line is present — the set
  compared was not the set requested.
- **Everything `UNCHANGED`** (and no `UNRESOLVED`, with explicit complete required
  coverage in the prior report) — nothing this review
  reads has changed since that report; re-running reproduces it. Surface the
  prior report's date and verdict and offer via `AskUserQuestion`: `[A] Stand
  on the prior report (Recommended)` / `[B] Re-run the full review anyway` —
  `guided` proceeds with [A] and notes it; `autonomous` logs via
  `log_decision` and stands on the prior report.
- **Some `CHANGED`/`NEW`** — name them, then scope instead of re-running
  everything: recommend `/architecture-review [system]` (single-system mode)
  for just the changed systems. A full re-run stays available on request,
  and structural changes (a `NEW` ADR, a deleted file) warrant one.
- **`RECEIPT: NONE`** — no prior report, or one written before receipts
  existed. Proceed with the full review; this run's report will carry the
  first stamps.

A prior report without complete reading coverage cannot establish that an
unchanged input was fully assessed. Re-run with the bounded protocol below;
input hashes alone are not coverage evidence.

Before reading any full document, use Grep to extract `## Summary` sections
from all GDDs and ADRs:

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 4
Grep pattern="## Summary" glob="docs/architecture/adr-*.md" output_mode="content" -A 3
```

**Fail open on a missing Summary.** Establish the denominator: glob
`design/gdd/*.md` and count **N**. A scan matching fewer than N means those GDDs
predate `## Summary` (`/design-system` emits it, but older GDDs lack it) — never
treat an absent Summary as a system out of scope. A zero-match scan means "no GDD
carries a Summary yet", not "nothing to review": review the unmatched set with
full bounded reads under Phase 1b's protocol.

For `single-gdd [path]` mode: use the target GDD's summary to identify which
ADRs reference the same system (Grep ADRs for the system name), then load only
those ADRs' sections per Phase 1b. Skip unrelated GDDs entirely.

For `engine` mode: load ADR sections only — GDDs are not needed for engine checks.
In practice this is the `## Engine Compatibility` scan alone.

For `coverage` or `full` mode: proceed to Phase 1b for the full in-scope set.
**This is a section load, not a full-file load** — see below for why, and for the
narrow cases that still justify escalating to a whole document.

### Phase 1b — L1/L2: Targeted Section Load

Read `.claude/docs/bounded-document-reading.md`. For each in-scope file, inventory
all heading/range pages with
`python3 .claude/scripts/read-markdown.py index "[path]" --offset 0 --limit 30`.
Read every selected section range, including nested subsections, using successive
`python3 .claude/scripts/read-markdown.py read "[path]" --start [line] --max-lines 120 --max-chars 8000`
calls and the returned actual line/column cursor. Keep required/read/unreviewed
ranges. Fixed-context grep output and summaries are discovery previews, not
complete section reads. All whole-file fallbacks below use the same protocol,
including preamble, unheaded text, and oversized-line fragments.

Load the sections the later phases actually consume — **not whole files**. This
skill reads the two largest document sets in the project (every GDD *and* every
ADR); at realistic sizes a full load of both exhausts the context window before
Phase 2 starts, and most of what it loads is narrative this skill never uses.

**Establish the denominator first.** Glob `design/gdd/*.md` and count **N_gdd**;
glob `docs/architecture/adr-*.md` and count **N_adr**. Report both. A section
scan matching fewer than the denominator means those documents lack the section —
**never treat an absent section as an absent document.** The scan narrows the
*read* set; it never shrinks the *in-scope* set.

### Design Documents

Phase 2 extracts *technical requirements* — data structures, performance
constraints, engine capabilities, cross-system communication, persistence,
threading, platform needs. Those live in a known set of sections; Overview and
Player Fantasy are narrative and yield none.

From each heading inventory select the complete Detailed Rules / Detailed Design,
Formulas, Dependencies, Tuning Knobs, and Acceptance Criteria ranges. Read them
to completion; a 40-line preview cannot establish their coverage.

Accept **either** `## Detailed Rules` or `## Detailed Design` — the design
standard and the GDD template disagree on the name and they denote the same
required section. Full-read a single GDD in bounded chunks when a selected section
cross-references material outside itself, or when a GDD matched zero sections
(it predates the template — read it whole and say so).

- `design/gdd/systems-index.md` — the authoritative list of systems; read whole
  in bounded chunks, verifying its line count rather than assuming it is small

### Architecture Documents

Phases 3–5 need the traceability table, the decision itself, engine claims, and
the dependency edges — not Context, Consequences, Alternatives, Migration Plan or
Validation Criteria, which explain *why* a decision was made.

Select the complete Status, Decision, GDD Requirements Addressed, Engine
Compatibility, ADR Dependencies, and Performance Implications ranges from each
ADR's heading inventory; read all their chunks. A 30-line preview is not a full
section. Record absent headings separately from unread content.

Interpret against **N_adr**, and distinguish the two zero-match cases — they are
not the same finding:

| Result | Meaning | Action |
|---|---|---|
| N_adr matches | Normal. | Proceed after complete bounded reads of the selected sections. |
| Some ADRs match, some do not | Those ADRs are missing sections. | Record each as a **structural gap** in the Phase 7 report — a missing `## GDD Requirements Addressed` is itself a traceability finding. |
| **0 matches, N_adr > 0** | **Malformed ADRs**, not "no architecture". | Retain all ADRs in scope and read unstructured content in full bounded chunks to assess the claims. Report the structural gap: "[N_adr] ADRs found, none carries a scannable section — run `/architecture-decision retrofit [file]` on each." If claims still cannot be assessed, name those checks `NOT ASSESSED`. Do **not** report zero coverage as if no architecture exists. |

Escalate to a full bounded read of one ADR when judging a conflict needs its
reasoning (Phase 4) — that is a per-ADR decision, not a blanket load.

- `docs/architecture/architecture.md` if it exists

### Engine Reference
- `docs/engine-reference/[engine]/VERSION.md`
- `docs/engine-reference/[engine]/breaking-changes.md`
- `docs/engine-reference/[engine]/deprecated-apis.md`
- **Only the module docs the in-scope ADRs actually name** — take the union of
  each ADR's `References Consulted` and `Post-Cutoff APIs Used` fields (already
  captured by the `## Engine Compatibility` scan above) and read those files.
  Reading the whole `modules/` directory loads engine subsystems the project may
  not use at all. If no ADR names any module, read none and note it: Phase 5
  cannot cross-check engine claims that were never made.

### Project Standards
- `project.yaml` — `naming.*` and `performance.*`; plus `.claude/docs/technical-preferences.md` for those keys when absent and for forbidden patterns / allowed libraries

Report counts: "Inventoried [N] GDDs, [M] ADRs; required ranges fully read:
[GDD count], [ADR count]; engine: [name + version]." Final reports include
coverage and exact unreviewed ranges/reasons. Unread required ranges, unfinished
fragments, or unresolved truncation make their checks `NOT ASSESSED` and prevent
approval; known failures remain visible and outrank unknown coverage. Agent
briefs carry paths and bounded scopes with the protocol's compact return contract,
not pasted document sets.

**Also read `docs/consistency-failures.md`** if it exists. Extract entries with
Domain matching the systems under review (Architecture, Engine, or any GDD domain
being covered). Surface recurring patterns as a "Known conflict-prone areas" note
at the top of the Phase 4 conflict detection output.

---
