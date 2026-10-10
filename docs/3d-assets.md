# 3D asset production and handoff

Use this path when the approved game needs 3D assets. Keep 2D experiments on
their existing raster pipeline. Blender and optional generation services are
separate tools; the studio template does not bundle them or their accounts.

## Produce one representative asset first

Start from the gameplay mockup and short art direction. Record front/side/back
references where shape or rigging needs them, silhouette, palette/materials,
world scale, camera distance, and a practical geometry/texture budget. Reuse
the user's owned or appropriately licensed references and record provenance.

Keep separate editable character, prop and environment sources under the
game's `production/art/sources/` (or its established equivalent). Deliver
engine-ready `.glb` files to the game's asset root. Godot recommends glTF;
direct `.blend` imports require Blender on importing machines. Explicit `.glb`
exports make that dependency easier to manage.
[Godot 4.7 import guidance](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html)

For each delivery, declare filenames, unit/world scale, transforms, pivot and
origin, material/texture paths, animation clip names/timing/loop settings,
attachment points, collision role, consumer scene, editable source, license,
generation cost and import status. Keep collision shapes separate from visual
meshes where gameplay requires it. Declare a static asset as static rather
than inventing an animation requirement.

If provenance, usage terms or editable sources are missing, name the unresolved
handoff gap and seek the original project/provider records before accepting the
delivery. Repair a reproducible deformation in the original source where
possible, or replace the delivery with a documented source within the approved
scope. Label reconstructed editable sources as reconstructed. Retain the
original failing sample and compare the repaired export in motion.

## Inspect in Godot before expanding the family

In the separate asset preview scene:

- Check orientation, scale, ground/contact pivot, normals, material and texture
  appearance under representative lighting.
- Play every delivered clip; inspect deformation, root motion and loop seams.
- Check equipment attachments during motion and collision alignment.
- Inspect silhouette at game-camera scale and record measured geometry,
  texture and runtime costs against the project's budget.

Then integrate one representative asset in the actual game and observe it.
A provider's render or successful export does not prove Godot import quality.
Keep screenshots and motion evidence; record unobserved categories separately.

## Optional Blender editor connection

[MCP for Blender](https://github.com/ahujasid/mcp-for-blender) is a community
integration with Codex setup instructions. Install a pinned compatible version
only in the intended environment and preserve existing client settings. Use
one editor connection for the pilot. Verify scene inspection, one reversible
mesh/material edit, save/reopen, and a `.glb` handoff imported into Godot before
depending on it. Record actual tool results and capture evidence.

Tripo or another model generator is optional. Define the requested operations,
retry limit and credit budget before using an authorized account; keep tokens
local. No paid generation is required to begin modeling with Blender.

The 3D path is integrated as conditional production guidance. Blender tooling,
generated models, rig quality and exported 3D gameplay remain NOT ASSESSED until
an actual 3D project exercises them.
