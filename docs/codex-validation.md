# Codex adapter validation

Validated on 2026-10-09 with Python 3.14.6 and Codex CLI 0.157.0.

- All 74 generated skills pass the system skill-creator frontmatter validator.
- All 49 standalone role files parse as TOML and contain the documented
  `name`, `description`, and `developer_instructions` fields. They inherit the
  user's model and contain no Anthropic model settings.
- Adapter regression tests exercise configuration-command execution,
  supporting-resource conversion, repeatable generation, generated-file
  drift, source updates, retired skills, local-edit preservation, destination
  symlinks, actual asset-validation feedback, staged JSON from the Git index,
  nested patch paths, startup context, and configured/unconfigured engines.
- `sync --check`, asset validation, and the adapter doctor pass.
- The installed CLI's strict configuration diagnostic reports `config.load:
  ok` for this workspace. Its broader diagnostic fails on provider network
  reachability and personal state database integrity in this restricted
  environment; those are not counted as adapter checks passing.

A live app-server `skills/list` probe could not finish: default startup
cannot initialize the personal SQLite state from this sandbox, and a
workspace-state probe waited for a backfill under the personal Codex home.
Native live discovery, role spawning, and trusted-hook execution have not
been confirmed. Project hooks require the user's normal trust review in a
new session. Manual hook payload tests call the real upstream validators.

No engine or game is configured, so no game build, visual playthrough, or
engine-specific end-to-end workflow is claimed. The conversion retains
Godot, Unity, and Unreal instructions; test the selected engine during
`studio-setup-engine` and game implementation.

Reproduce the adapter checks:

```bash
python3 -m unittest discover -s tools/codex/tests -v
python3 tools/codex/studio.py sync --check
python3 tools/codex/studio.py doctor
python3 tools/codex/studio.py validate
```
