# Upstream issue audit for Codex Game Studios

Audit date: **2026-10-09**. Source: [Donchitos's issue tracker](https://github.com/Donchitos/Claude-Code-Game-Studios/issues).

Fetched **63 issue reports (41 open, 22 closed)**, their available comments,
and upstream PR statuses. Compared the open reports and relevant closed bugs
with the local Codex skills, shared scripts, adapter, and documentation.
Both current upstream `main` and our recorded upstream revision are
`be8993bbc5a1f016bc770b2846ce06272d284526` (framework 1.1.3).
The audited Codex repository revision is `f60ae52`.

An open upstream issue is not proof that our repository still has its bug:
several fixes are present in 1.1.3 while their reports and PRs remain open.
This audit records the findings at the audited revision. The three recommended
changes have since been implemented; see [implementation and evidence](codex-fixes.md).

## Recommended work, in order

### 1. Fix the commit hook's GDD checks — confirmed inherited bug

Upstream: [#133](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/133).
Priority: **P2 — medium**, first to fix because it is directly reproduced.
These are advisory warnings, not blocked commits.

The Codex pre-tool adapter calls the original `validate-commit.sh`
(`tools/codex/studio.py:117`), so this behavior reaches Codex when hooks run.
The original script:

- Includes subfolders through `^design/gdd/` (`validate-commit.sh:606`),
  despite the structure-check helper restricting its default scan to top-level
  system GDDs.
- Maintains its own list of required section names (`:620`), omitting Summary
  and conditional sections defined by the authoring workflow.
- Searches the entire lowercased document (`:656`), rather than headings.

Ran the actual hook in an isolated temporary Git repository with full rigor
and each fixture staged separately:

| Fixture | Observed result | Why it matters |
| --- | --- | --- |
| `design/gdd/archive/combat.md`, containing old notes | Eight missing-section warnings | Archived material is treated as an active system GDD. |
| Top-level `combat.md`, all eight section names in one prose line, no section headings | No design warnings | Keyword mentions are mistaken for real sections. |
| Top-level `combat.md`, eight headings present but no Summary | No design warnings | The hook does not check the summary required by the authoring workflow. |

All three hook invocations exited 0; warnings are advisory. The archive fixture
has eight distinct warnings repeated in two fields of the hook's JSON output.
No commit was executed, and the working project was not changed by these probes.

Fix scope:

1. Restrict checks to active, top-level system GDDs and retain governance-file
   exclusions.
2. Use one shared definition of headings, aliases, and tier/category conditions
   for deterministic structural checks. Keep judging semantic completeness in
   design review; do not guess conditional requirements from keywords.
3. Add fixture regressions for archives/reviews, governance files, prose-only
   mentions, missing Summary, heading aliases, and the workflow tiers.

The maintainer says the subfolder fix is planned for 1.2.0 and the redesigned
check for 2.0.0. Those comments describe future releases; the fixes are not in
our current upstream revision. A small local fix is reasonable, with later
upstream integration reviewed for overlap.

### 2. Check runnable prerequisites before planning a sprint — useful missing capability

Upstream: [#58](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/58).
Priority: **P2 — medium**. Related proposed change:
[PR #76](https://github.com/Donchitos/Claude-Code-Game-Studios/pull/76), still open.

`studio-sprint-plan` gathers backlog, milestone, design, and risk information
in Phase 1 (`.agents/skills/studio-sprint-plan/SKILL.md:100`), but has no explicit
sprint-goal prerequisite audit. The producer's gate considers dependencies,
but runs only in full review mode (`:303`). Phase 5 checks for a QA-plan file
(`:336`), not whether the game has the scenes, assets, build setup, or test
harness needed to demonstrate the goal.

The reported failure is a playtest goal scheduled alongside logic-only work
while its playable scene does not exist. This is a missing planning safeguard,
not a locally reproduced engine failure; no engine is configured here.

Fix scope:

- State the sprint's demonstrable goal and inspect its concrete prerequisites.
- Mark each prerequisite as present, planned within the sprint in dependency
  order, or missing/blocking. Do not block a sprint simply because it will build
  a needed scene as one of its stories.
- Apply the check in every review mode, before writing the plan, without adding
  routine approval prompts. Record intentional deferrals explicitly.

Sprint planning is optional at minimal rigor; this matters most when using
standard/full planning or voluntarily planning sprints.

### 3. Finish the document-reading improvements — relevant to Codex

Upstream: the reading-discipline portion of
[#136](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/136) and
[#140](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/140).
Priority: **P2 — medium**, especially for large projects.

The important ADR optimization is already implemented: `studio-dev-story`
uses story-embedded guidance after freshness/status checks. Holistic review
also starts with summaries and targeted sections. However,
`.agents/skills/studio-design-review/SKILL.md:127` still says to read the target
design document in full. Its full-read fallback and similar remaining
instructions can inflate context on large files.

Fix scope:

- Locate headings first and read bounded sections, covering every section
  required for a full review across successive reads. A bounded read should
  preserve review coverage, not silently narrow it.
- Give agent briefs explicit section scope and compact return contracts.
- Verify the change on a large fixture and, later, a real project. The cost
  measurements reported for Claude are not measured Codex savings.

Do **not** copy Anthropic model IDs, effort settings, or Claude plugin APIs
into Codex. Our roles intentionally inherit the user's Codex settings. Model
profiles or enforced read guards would be separate, optional work requiring
Codex-specific support and validation.

## Practical validation before claiming a game pipeline works

Reports [#46](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/46),
[#53](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/53), and
[#34](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/34) raise
productivity and playable-output concerns rather than reproducible template
bugs. Our minimal/guided quickstart and run-and-observe instructions address
part of this, but our adapter tests do not demonstrate a working game pipeline.

After choosing an engine, validate a small game through onboarding → brief →
story → implementation → launched playtest → completion review. Keep runtime
and screenshot evidence, and record failures. This should precede adding more
engines or a large asset-production toolchain. Current limitations are already
stated in [adapter validation](codex-validation.md).

## Already addressed or not inherited

| Upstream report | Finding in our repository |
| --- | --- |
| [#103](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/103), [#24](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/24): Codex support | The adaptation supplies AGENTS.md, 74 repository skills, 49 role definitions, and Codex tooling. Engine end-to-end validation remains separate. |
| [#63](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/63), [#64](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/64): redundant/full ADR reads | Already addressed in `studio-dev-story/references/2-load-context.md:60` and `4-implement.md:39`: trust current embedded summaries; check freshness and use targeted reads when needed. Claude's exact Read cap is not a Codex limit. |
| [#88](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/88): feasibility-gate wording | Phase 2 now explicitly says the gate runs only in full mode (`studio-sprint-plan/SKILL.md:153`). No need to make all review modes run a producer. The separate prerequisite gap above still matters. |
| [#86](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/86): narrative transition gate | An explicit Phase 2 → 3 gate exists at `studio-team-narrative/SKILL.md:182`, respecting automation mode and existing authorization. |
| [#81](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/81), [#69](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/69): hotfix approval sequence | The skill separates proposed fix/approval from Phase 4b implementation (`studio-hotfix/SKILL.md:139`) and requires deployment approval. Existing user authorization still governs Codex work. |
| [#83](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/83), closed [#44](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/44): ADR skill headings | `# Architecture Decision` exists at line 53; phase numbering is corrected. |
| [#70](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/70): unrelated-history upgrade instructions | `UPGRADING.md` now separates shared-history merge from selective migration and rejects forced unrelated-history merging. Our Codex update guide does the same. |
| [#72](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/72), closed [#128](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/128), [#33](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/33): Claude frontmatter/tool permissions | Those Claude metadata restrictions are not used as Codex tool permissions. The adapter explicitly maps tool capabilities and configuration reads. Skill-level workflows still need actual client tools. |
| Closed [#67](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/67), [#131](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/131): model mismatch/test drift | Codex roles omit Anthropic model pins and inherit user settings; our compatibility tests target the Codex artifacts. Upstream Claude test specifications are not Codex runtime configuration. |
| Closed [#71](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/71): skill discovery | Codex skills are in `.agents/skills/`, with plain-language/path fallback documented. This does not claim every client/UI combination was tested. |
| Closed [#39](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/39): stale startup preview | The shared hook reads the marked CHECKPOINT region, with bounded output and malformed-marker handling (`session-start.sh:260` onward). |
| Closed [#37](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/37): invalid GDScript ripgrep type | The specialist explicitly uses `--glob "*.gd"` and explains that `--type gdscript` is invalid. |
| Closed [#20](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/20): Claude audit-log field | The faulty Claude subagent-audit mechanism is not enabled in Codex. Agent audit logging is a documented compatibility limitation, not a claimed feature. |
| Closed [#104](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/104): flaky discovery-log test | This concerns a downstream game's Godot test file, which is absent from this starter. |

## Remaining open issue inventory

This covers the other open reports without treating feature requests, roadmap
questions, or empty reports as confirmed bugs.

| Issue(s) | Disposition |
| --- | --- |
| [#137](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/137): document condensation | Useful optional follow-up after bounded reads. Preserve formulas, acceptance criteria, decisions, and archived history; a cleanup must not change game behavior. |
| [#130](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/130): offline progress board | Optional improvement; deterministic status derived from existing artifacts could help long projects. |
| [#82](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/82): GitHub Project board | Optional integration; not required for local game development. |
| [#105](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/105), [#62](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/62), [#22](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/22): libGDX, Phaser, web/THREE.js | Optional engine additions, to prioritize after the user's engine choice. They need configuration, source-root, build/test, and runtime verification changes, not just new role files. |
| [#40](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/40), [#23](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/23), [#14](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/14): creative connectors, vendor assets, TTS | Optional asset-execution work. Adapt to available Codex tools; do not assume Claude connectors or paid credentials exist. PixelLab's proposed PR #115 is not merged. |
| [#47](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/47): unavailable image-pen skill | `image-pen` is not a shipped studio skill. Clarify available image-generation tools and asset handoff if expanding that workflow; this is not a missing adapter conversion. |
| [#19](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/19): tooling-project support | Optional new project type; PR #54 is still open. |
| [#18](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/18): subagents | Role definitions and explicit delegation/sequential fallback already exist; the report gives no further concrete failure to reproduce. |
| [#29](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/29): too many confirmations | Addressed in part by inherited automation modes plus the Codex authorization adapter and guided quickstart. Verify actual session behavior during a playable smoke run; do not add per-file approval gates. |
| [#12](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/12): Unity-only skills | Optional engine-focused guidance/catalog filtering. Shared workflows intentionally support several engines. |
| [#139](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/139): autonomy/platform roadmap | Track upstream: the maintainer says 2.0 targets platform agnosticism including Codex. This is intent, not a released replacement for our adapter. |
| [#112](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/112): maintenance question | Not a code defect; latest upstream release commit is dated 2026-10-08. |
| [#134](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/134): sponsorship | Commercial collaboration, not a repository bug. |
| [#97](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/97), [#17](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/17): experience/project sharing | No actionable failure in our starter. |
| [#56](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/56): dmf coroutine input | External Roblox/dmf runtime behavior; that toolchain is not shipped here. |
| [#138](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/138), [#27](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/27): empty reports | Insufficient details to diagnose. |
| [#28](https://github.com/Donchitos/Claude-Code-Game-Studios/issues/28): API intermediary promotion | No actionable studio issue. |

Other closed entries (#114, #109, #107, #102, #80, #57, #55, #38, #32,
#30, #26, #11) are deleted/test reports, unrelated runtime/integration
questions, or optional feature proposals. Their closed status is not taken
as evidence that those optional features are implemented here. In particular,
#80's body describes a different integration despite its hotfix title.

## Implementation and upstream coordination

For the three recommended changes, edit `.claude/` sources/shared helpers or
the adapter as appropriate, then regenerate Codex files with
`python3 tools/codex/studio.py sync`. Do not patch generated skills alone.
Add focused regressions and run the existing adapter suite and drift check.

Keep links to the originating issues and preserve attribution. Review future
upstream proposals for duplicate fixes or changed schemas. None of the proposed
upstream PRs inspected for this audit was treated as installed code, and no
upstream issue comment or new downstream GitHub issue was posted by this audit.
