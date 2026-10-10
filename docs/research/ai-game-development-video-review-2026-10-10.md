# AI game development workflows: recommendations for this studio

Prepared 2026-10-10 for the Codex Game Studios project.

**Recommendation:** retain Codex + Godot, strengthen visual direction and playtesting, pilot one Godot editor MCP, and introduce Blender asset production when a project needs 3D. Improve the existing playable-prototype workflow before expanding the tool catalogue.

## What was reviewed

Read complete English transcripts of all three requested videos, their descriptions and chapters, and selected on-screen steps from the third video. The first two transcripts are auto-generated; the third is labelled authored or unspecified. Checked the relevant tools against their maintainers' documentation. This is a workflow analysis, not an independent reproduction, audio review, or performance benchmark of the creators' games. Their private skills/templates were not available for inspection.

## The three workflows

### Letta Corporation — Godot platformer

[GPT 6.1 Sol Is OUTSTANDING at Building Godot Games…](https://www.youtube.com/watch?v=96XK-OJ5U3g)

The creator starts with concepts and images, chooses a paper-and-ink platformer, then supplies a design document and personal Godot skills. Godot AI MCP connects the editor; separate work produces character/enemy artwork and animation. Playtesting reveals UI, drawing-rule and collision problems, prompting further changes. Lessons from those corrections feed the next project's skills.

Useful segments: [skills and editor connection, 4:09](https://www.youtube.com/watch?v=96XK-OJ5U3g&t=249s); [playtest corrections, 12:11](https://www.youtube.com/watch?v=96XK-OJ5U3g&t=731s).

The creator reports a 27-page design document and roughly 12–16 hours of implementation. Those are observations about this session, not a controlled model comparison. The demonstrated value is reusable craft knowledge plus iteration.

### Bryan McAnulty — visual references and Blender

[GPT-6 Astra Makes 3D Game Development Feel Like Cheating](https://www.youtube.com/watch?v=Ta8siAhkEOw) — also presented under the title “The Easiest Way to Build a 3D Game With AI”.

The workflow first produces a basic game, then uses generated target screenshots to guide improvement. For the larger strategy prototype, an image-producing Codex agent supplies moodboards and multiple asset views; another agent builds and integrates models through Blender. Subsequent passes add textures, animations and screenshot-based corrections. The game uses Three.js, rather than Godot, and the creator says it remains in development.

Useful segments: [visual target, 1:39](https://www.youtube.com/watch?v=Ta8siAhkEOw&t=99s); [asset handoff, 6:13](https://www.youtube.com/watch?v=Ta8siAhkEOw&t=373s); [runtime inspection, 10:14](https://www.youtube.com/watch?v=Ta8siAhkEOw&t=614s).

Matching an image provides direction; it does not establish enjoyable controls or working collisions. LatchLoop's creator is also promoting his own platform here.

### Chong-U / AI Oriented Dev — assets, mechanic and release

[I Built (And Shipped) a 3D Game With Claude Opus 5.5](https://www.youtube.com/watch?v=3QwU8TM7Rag)

Pressure Wash Panic uses a Rust/WebAssembly/WebGPU template. The creator chooses mockups, makes reference turnarounds, uses Tripo for character generation and Blender for asset work, while prototyping the washing mechanic separately. Preview scenes check imported models and equipment attachment. Polish and staged tutorials precede browser distribution.

Useful segments: [mockups, 7:12](https://www.youtube.com/watch?v=3QwU8TM7Rag&t=432s); [mechanics gym, 10:28](https://www.youtube.com/watch?v=3QwU8TM7Rag&t=628s); [tutorial, 15:15](https://www.youtube.com/watch?v=3QwU8TM7Rag&t=915s).

Reported time is about 6.5 hours; roughly $233 is an API-equivalent estimate for the initial published version, not an itemized invoice. The [public game site](https://pressurewashpanic.com/) provides browser-play links. I did not independently test that game.

## What this means for your studio

Crystal Garden already demonstrates custom raster artwork, animation, a tiled environment, feedback, audio and an independently checked playable route. Its result supports the current pipeline's basic capability. The next improvement should increase intentional design and repeatability.

Use four reviewable artifacts for a small project:

1. **A short brief:** the core action, challenge, goal, target device and explicit scope.
2. **A target gameplay mockup:** camera framing, native resolution, world composition, HUD and representative character scale. Reference assets should be owned or appropriately sourced.
3. **A working mechanics scene:** movement, collision and the main interaction are playable before all presentation work is complete.
4. **A compact evidence pack:** rendered captures, motion recording, test results, human sound review where appropriate, and a build someone else can launch.

Evaluate the target on named dimensions—silhouette, palette, scale, layering, readability and feedback timing. Pixel-perfect matching is rarely an appropriate acceptance test across animation frames and camera movement. Keep visual scoring separate from mechanical correctness and enjoyment.

For a small experiment, reserve a short first checkpoint for the playable core rather than granting an open-ended overnight build. Agree a time and spending budget, assess what actually exists at the checkpoint, then expand deliberately. Track model usage separately from external asset credits and from human review time; record unavailable cost information as unknown.

## Tools worth using

| Tool | Recommendation | What it adds |
|---|---|---|
| Existing Codex studio and craft skills | Keep as the base | Project context, art/asset records, implementation and verification |
| Built-in image generation | Continue for current 2D experiments | Target mockups and cohesive raster families |
| Godot AI MCP, `hi-godot/godot-ai` | Pilot next in one project | Live scene/node inspection, editor operations and screenshots |
| MCP for Blender, `ahujasid/mcp-for-blender` | Introduce for a 3D project | Model/material authoring and asset inspection in Blender |
| PixelLab or Ludo | Evaluate when a concrete asset need arises | Specialized character animation and asset production |
| Tripo | Optional 3D generation experiment with a budget | Reference images to model generation and rigging services |
| LatchLoop or a custom Rust/WebGPU runtime | Evaluate for a specific requirement | Alternative collaboration/distribution/runtime approaches |

[Godot AI's current source documentation](https://github.com/hi-godot/godot-ai) supports Codex and GDScript; its v4 line requires Godot 4.7+, which fits your installed 4.7.2. Use a published release and its matching dock-generated Codex configuration. Scope it to the project where supported. Validate a small scene edit, save/reopen, script error reporting and screenshot capture before depending on it. The video/store setup may describe an older version. This bridge complements your generation and testing tools; it supplies editor access.

[MCP for Blender](https://github.com/ahujasid/mcp-for-blender) documents Codex configuration and model/material/visual inspection operations. It is a community integration. For a 3D pipeline, retain separate editable character, prop and environment sources and deliver `.glb` assets with declared scale, pivots, materials and animation clips. [Godot's 4.7 importer documentation](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html) recommends glTF and supports `.glb`; direct `.blend` importing also needs Blender on the importing machine. Check deformations, attachments, collision and performance inside Godot.

[PixelLab](https://www.pixellab.ai/mcp) documents pixel-art characters, directional animation and tilesets. [Ludo's CLI](https://ludo.ai/developers/cli) documents asset generation and Godot animation export. Neither was used by this research run. Your existing sprite pipeline is sufficient for another small 2D experiment; these become useful when its animation or production demands exceed what it handles reliably.

[Tripo's developer documentation](https://developers.tripo3d.ai/en/docs/introduction) covers image/multiview model generation, model processing and animation services. Treat provider-generated meshes as inputs requiring inspection. Budget the selected operations and retries before using them.

## Skills and workflow changes to prioritize

The repository already includes `studio-art-bible`, `studio-asset-spec`, `studio-ux-review`, `studio-perf-profile`, `studio-release-checklist` and `studio-skill-improve`. For prototypes, use their relevant checks proportionately rather than generating a full studio's paperwork.

Recommended changes to the existing `studio-playable-prototype` workflow:

- Make the chosen gameplay mockup a reference artifact before producing the full asset family.
- Maintain a small mechanics gym for the primary interaction and a separate asset preview scene for scale, pivots, layering or rigs.
- Define an asset handoff: filenames, dimensions/scale, state/clip names, pivots, collision role, provenance and intended scene integration.
- Add a first-use playtest: a new player should discover the goal and main action without the developer explaining every step.
- Add a proportionate distribution check: launch an exported build, or validate the intended web build, before calling something ready to share.
- Convert recurring playtest failures into small reusable lessons and meaningful regression checks. Keep game-specific details in that game's records; update shared skills from demonstrated evidence.

These are recommendations. No skills, connectors, accounts or project settings were installed or changed during this analysis.

Parallel asset production can be useful when you request it. Keep ownership explicit: one worker owns character assets, another environment assets, and the gameplay owner integrates agreed exports. Avoid multiple workers writing the same scene or running competing editor operations. A small prototype can follow the same stages sequentially.

## A practical next experiment

Extend Crystal Garden with one carefully scoped mechanic—for example, a short-range magnetic pull that draws a crystal toward the explorer while rocks block its path. Keep one garden and the existing art family. This tests whether visual direction and a mechanics gym improve an already verified base.

Start with a mockup and one interaction test scene. Then implement the mechanic, readable range/blocked-path feedback, and a brief introduction. Check reachable objectives, pickup uniqueness, obstruction, restart during effects, mute and the original movement/collision route. Export a build and ask another person to play for a few minutes without coaching.

If your next goal is specifically 3D, use a separate small Godot project: one fixed camera, one character, one room and one interaction. Pilot Blender with one prop and one animated character before generating a full environment. Keep multiplayer, large maps and progression outside that first asset-pipeline test.

## How to judge other YouTube demos

For each promising video, record the mechanic, runtime, asset origin, reusable template/skills, manual corrections, total attempts, time/cost basis and any independently runnable output. Give more weight to a small working release and documented corrections than to an attractive generated screenshot.

Ask whether the creator supplies a reproducible prompt/template and usable assets; whether model-only work is distinguished from external generators and pre-existing boilerplate; whether first-time controls, restart and collisions are shown; and whether the claimed completion level matches the demonstrated game. Sponsorships and creator-owned services are context for evaluating the recommendation, not proof that the method is ineffective.

Choose individual practices to test against your own acceptance criteria. The three videos use different game scopes, assets, runtimes and agent harnesses, so their outcomes cannot establish which model or platform is universally best.
