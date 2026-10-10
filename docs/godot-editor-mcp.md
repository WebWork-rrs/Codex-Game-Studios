# Godot editor MCP pilot

Godot AI is an optional community editor bridge. Keep it out of an unconfigured
template's default client configuration; install it in one selected game or
isolated pilot. The studio can still run Godot and retain native evidence
without an editor MCP.

## Install the matching release

1. Confirm the project's engine pin and actual executable. Godot AI v4 requires
   Godot 4.7+ in the 4.x series and `uvx`. Choose a published release compatible
   with the installed engine.
2. Close the pilot editor, follow the release's verification/installation
   instructions, and retain its tag, source commit, manifest/archive hashes
   and verification result. Preserve its license. Install into
   `addons/godot_ai/`, with `plugin.cfg` inside that directory. Follow the
   documented updater for an existing installation rather than overlaying it.
3. Open Godot from that project's directory and enable Godot AI in Project
   Settings → Plugins. Confirm the dock reports a healthy server.
4. Select project/local client scope where the client supports it, then use
   the dock's matching Codex command. Inspect its destination and any existing
   `godot-ai` entry first: configuring can replace that entry across scopes.
   Preserve unrelated servers and the user's configured scope. Do not bake a
   machine-specific command or local capability into this template.
5. Reload the client if needed. V4 uses `godot-ai attach` over stdio; a bare
   localhost HTTP URL is not a valid replacement for that generated command.

Source: [Godot AI setup and project scope](https://github.com/hi-godot/godot-ai).
The release selected for the local pilot on 2026-10-10 is
[v4.3.0](https://github.com/hi-godot/godot-ai/releases/tag/v4.3.0), with Godot
4.7.2. This is a recorded pilot pin, not an automatic future-update policy.

## Acceptance exercise

In a disposable scene, using the actual MCP tools exposed by that release:

- Read the current scene hierarchy and confirm the intended project.
- Add and modify one visible node, save, close/reopen, and verify persistence.
- Submit a deliberately invalid script, observe the reported parse error,
  restore valid code, and verify recovery.
- Capture the edited scene/game and inspect the returned pixels.
- Close the pilot editor and confirm the bridge loses that connection rather
  than silently editing another project. Restore/remove disposable test nodes
  where needed; preserve the pilot evidence and record any failed operation.

Keep a receipt under `production/qa/evidence/`: exact versions, configuration
scope, tool results, screenshot, and assessment per operation. An MCP listing
alone is insufficient. Unavailable native capture or a connection failure is
NOT ASSESSED/FAIL as appropriate, with the actual reason.

For a 2D editor capture, activate the 2D workspace and choose `viewport_2d`;
check dimensions and content before accepting the image. In the local pilot,
an inactive 2D viewport returned only 2×2 pixels. The running game's `game`
source returned a fresh 640×360 frame and was visually inspected. This is a
capture-source limitation to record. The 2×2 image does not establish scene
appearance; use a visible viewport or a fresh game capture.

This bridge supplies editor access, not an image model or paid asset account.
Use the existing asset and observation skills alongside it. Keep secrets out
of Git. Do not install a second bridge for the same editor unless a concrete
missing operation requires it.
