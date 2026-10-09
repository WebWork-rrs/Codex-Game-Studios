# Implemented upstream issue fixes

Implemented on 2026-10-09 from the [upstream issue audit](upstream-issue-audit.md).
These are additions to the Codex adaptation; Donchitos's original framework
and MIT attribution remain intact.

## GDD validation (#133)

The commit hook now checks active top-level system GDDs and excludes archived,
review, and governance documents. It recognizes Markdown headings outside code
fences rather than keyword mentions and checks Summary. The shared
`.claude/scripts/gdd-structure.py` schema supplies heading aliases, tier rules,
and conditional requirements for both review and commit validation.

Regular commits inspect staged content. A pending `git add` or path-specific
commit uses the working content that the existing command scanner identified
as destined for that commit. Nested projects retain their repository prefix.
Checks remain advisory; unavailable helpers and unresolved semantic conditions
report SKIPPED / NOT ASSESSED. Category, numeric-rule, and dependency judgments
come from design review, rather than being guessed from prose keywords.

See [shared structure instructions](../.claude/docs/gdd-structure.md).

## Sprint goal prerequisites (#58)

New and updated plans must record goal prerequisites in every review mode:
PRESENT, PLANNED by an actual selected story, MISSING, or NOT ASSESSED. Evidence
includes paths, acceptance criteria, dependency order, and capacity. Planned
scenes are valid sprint work; missing prerequisites without a delivering story
block the final plan. Scope changes rerun the check. Unavailable evidence can
produce only an explicitly provisional plan with named readiness blockers.

## Bounded document reads (#136 / #140)

`.claude/scripts/read-markdown.py` provides paged heading inventories and reads
with exact line/column cursors. Its default output budget includes serialized
UTF-8 metadata, escapes, and multibyte characters. Oversized lines are split
without losing characters; document hashes detect changed inputs.

Single-document reviews retain full semantic coverage through successive
chunks. Cross-GDD and architecture reviews read their complete selected ranges
and expand when needed. Coverage ledgers and unresolved ranges govern verdicts.
Agent briefs give source paths, hashes, and ranges rather than pasting whole
files into every agent context. The Codex adapter preamble and AGENTS.md apply
this protocol across the generated skills and roles.

See [bounded reading protocol](../.claude/docs/bounded-document-reading.md).
This implements the reading-discipline part of those proposals. Anthropic model
profiles and Claude plugin-specific filtering/enforcement are not ported.

## Evidence

The full local suite passes **34 tests**, including 16 new focused regressions.
Generated-file consistency, doctor, asset validation, and shell syntax checks pass.

- The original archive/prose/Summary/staged-content failures were observed
  before the hook changes; focused regressions now exercise those boundaries,
  pending additions, nested repositories, tier/condition rules, and missing
  helpers.
- Reader tests recover every character across page and giant-line boundaries,
  reject invalid cursors/missing files, detect changed hashes, and preserve real
  headings after inline backtick spans.
- Independent workflow scenarios changed from the observed baseline failures
  to correct behavior for missing/planned prerequisites, scope updates, and
  complete large-document coverage.
- A synthetic 1,700,000-byte / 13,029-line document was recovered across 222
  bounded pages in the behavioral check, including a late conflicting rule
  and a 10,000-character line. This verifies transport and coverage behavior,
  not the quality of a real game's semantic review or measured token savings.
- Independent code review found two issues (fence parsing and conflicting
  cross-GDD brief instructions); both were corrected and rechecked.

Run the repository suite and consistency checks:

```bash
python3 -m unittest discover -s tools/codex/tests -v
python3 tools/codex/studio.py sync --check
python3 tools/codex/studio.py doctor
python3 tools/codex/studio.py validate
```

No game engine is configured. A playable end-to-end game remains a separate
validation task after engine selection; these changes do not claim that run.
