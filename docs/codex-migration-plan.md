# Codex compatibility plan

Goal: use the upstream game studio workflows in Codex from this repository,
without installing Claude Code or changing personal Codex settings.

Source: Donchitos/Claude-Code-Game-Studios, commit
`be8993bbc5a1f016bc770b2846ce06272d284526` (framework 1.1.3).

## Design

Keep `.claude/` as the upstream source of workflows, roles, rules, templates,
and configuration helpers. Generate namespaced Codex skills under
`.agents/skills/studio-*` and standalone custom roles under `.codex/agents/`.
Copy each skill's supporting resources and translate command references and
Claude-only shell preprocessing. Models inherit the user's Codex selection.

Root `AGENTS.md` supplies Codex-specific tool mappings, authorization behavior,
engine routing, selective rule loading, and session recovery. Shared upstream
references remain available; their Claude-specific mechanics are interpreted
through this adapter. Engine setup writes `project.yaml` and retains the
upstream `CLAUDE.md` mirror for compatibility; Codex reads the configured engine
reference explicitly, without relying on `@` imports.

Use current native Codex lifecycle hooks for session context, commit/push
checks, and post-edit asset validation. Translate payloads before calling the
existing Bash validators; return structured Codex context. Hooks require the
client's normal project/hook trust. An explicit validator remains available
when hooks are disabled or unavailable. Do not copy Claude permission rules,
change sandbox policy, or bypass hook trust.

## Implementation and verification

- [x] Write regression tests for conversion, supporting files, configuration
  snippet execution, synchronization, and protection of local edits.
- [x] Implement deterministic generation and generate all 74 skills / 49 roles.
- [x] Test hook translation using real upstream validators, including malformed
  asset JSON, staged JSON, nested working directories, and patch edits.
- [x] Add startup instructions, workflow catalog, validation commands, and CI.
- [x] Run the full adapter test suite, generated-file checks, and local doctor;
  validate current Codex configuration parsing and discovery where possible.

Results and environment limits are recorded in `docs/codex-validation.md`.

Constraints: Python 3.11+ standard library for adapter tooling; Bash/Python 3
for upstream helpers. No engine choice, game concept, engine installation,
GitHub publication, commits, or personal configuration changes are part of
this adaptation. Engine execution and behavioral game QA occur after engine
setup, not against an empty template.
