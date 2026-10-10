# Build a prototype with a visual target

Use `$studio-playable-prototype` in the game repository. Keep minimal-rigor
planning to the existing short brief and a compact asset/evidence record.
This workflow now incorporates the video-review recommendations in order:

1. **Choose the appearance.** Keep a gameplay mockup at
   `production/art/gameplay-target.png`, with provenance and camera, scale,
   palette, layers, resolution and HUD notes. Compare actual rendered frames
   against those dimensions. Reuse the user's accepted direction.
2. **Isolate mechanics and asset inspection.** Keep a runnable mechanics gym
   and a separate asset preview scene. Both reuse production code/resources.
   Verify boundary cases and restart in the gym; inspect imported animation,
   pivots, scale, layering and collision alignment in the preview.
3. **Pilot editor access when useful.** Follow [Godot editor MCP](godot-editor-mcp.md)
   in one isolated project before enabling it in the game. The CLI and native
   observation workflow remain available. A listed MCP server is not evidence
   that its editor operations work.
4. **Use a 3D handoff when the game needs it.** Follow
   [3D asset production](3d-assets.md) for editable sources, `.glb` exports,
   rigs, materials and in-engine validation. A 2D project does not need Blender.
5. **Check first use and distribution.** Give a new player the build without
   explaining controls. Record confusion and retest changes. Launch the
   exported artifact outside the editor on the agreed platform before claiming
   it is ready to share. Feed demonstrated recurring failures into regressions
   and, within authorized maintenance scope, shared workflow improvements.

The skill includes a portable
[compact record template](../.agents/skills/studio-playable-prototype/references/prototype-record.md)
for handoffs, evidence, first-use observations, export receipts and lessons.
Use existing equivalent records and scenes instead of duplicating them.

## Start in a game project

```text
Read AGENTS.md and the current project configuration. Use
studio-playable-prototype for the approved game brief. Keep minimal rigor.
Choose a gameplay mockup before generating the full asset family. Maintain
a mechanics gym and a separate asset preview, with explicit asset handoffs.
Run and observe the game, test first use without coaching, and launch the
exported desktop build. Report mechanics, visuals, motion, audio, first use,
and distribution separately, with retained evidence and any missing checks.
Use authorized tools; ask before spending on a paid provider.
```

Existing requests for greyboxes, silence, or a narrower scope take precedence.
Unavailable generation, a missing new player, unheard audio, or a blocked
export is recorded as NOT ASSESSED for the corresponding required category.
It must not silently become a PASS. An editor-playable prototype and a
verified shareable build are different claims.

## What this integration establishes

The studio supplies repeatable instructions, templates and tool setup guidance.
Each game must still create its actual assets and scenes and retain its own
observed evidence. Workflow validation does not establish game quality,
animation, sound, human enjoyment, or an untested platform's compatibility.
