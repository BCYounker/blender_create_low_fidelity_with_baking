import bpy
import os
import math


# Import the mesh from .ply file
bpy.ops.import_mesh.ply(filepath="scene.ply")
# Adjust the imported mesh object's scale
bpy.context.object.scale = (0.001, 0.001, 0.001)
# Change Light
light = bpy.data.objects['Light']
light.location = (0, 0, -0.1)
# Delete default cube and camera
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects['Cube'].select_set(True)
bpy.ops.object.delete()
bpy.data.objects['Camera'].select_set(True)
bpy.ops.object.delete()
bpy.ops.wm.save_as_mainfile(filepath="scene_new.blend")


bpy.ops.wm.open_mainfile(filepath="scene_new.blend")
# Mesh Extrusion
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(
    TRANSFORM_OT_translate={"value": (0, 0, 0.005)}
)

# Adjustment
bpy.ops.object.mode_set(mode = 'OBJECT')
material = bpy.data.materials.new(name="Material")
material.use_nodes = True
obj = bpy.context.active_object
obj.data.materials.append(material)
nodes = material.node_tree.nodes
links = material.node_tree.links
attr_node = nodes.new(type="ShaderNodeAttribute")
attr_node.attribute_name = "Col"
links.new(attr_node.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])

# Mesh Duplication
bpy.context.view_layer.objects.active = bpy.data.objects['scene']
original = bpy.context.active_object
# Duplicate the object
new_object = original.copy()
new_object.name = 'scene_copy'
new_object.data = original.data.copy()
new_object.animation_data_clear()
if original.data.materials:
    new_object.data.materials.clear()
    for material in original.data.materials:
        new_object.data.materials.append(material.copy())
bpy.context.collection.objects.link(new_object)
original.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')


# Add a remesh modifier
bpy.context.view_layer.objects.active = bpy.data.objects['scene_copy']
duplicate = bpy.context.active_object
duplicate.select_set(True)
scene_copy = bpy.data.objects['scene_copy']
bpy.context.view_layer.objects.active = scene_copy
scene_copy.select_set(True)
remesh_modifier = scene_copy.modifiers.new(name="Remesh", type='REMESH')
remesh_modifier.mode = 'VOXEL'
remesh_modifier.voxel_size = 2
bpy.ops.object.modifier_apply(modifier=remesh_modifier.name)


# Other modifier
bpy.context.view_layer.objects.active = bpy.data.objects['scene_copy']
duplicate = bpy.context.active_object
duplicate.select_set(True)
shrinkwrap_mod = duplicate.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
shrinkwrap_mod.wrap_method = 'PROJECT'
shrinkwrap_mod.use_negative_direction = True
shrinkwrap_mod.target = bpy.data.objects['scene']
multires_mod = duplicate.modifiers.new(name="Multires", type='MULTIRES')
bpy.ops.object.multires_subdivide(modifier=multires_mod.name)
multires_mod.levels = 0
bpy.ops.object.modifier_apply(modifier=shrinkwrap_mod.name)


# Texture
image_diffuse = bpy.data.images.new("diffuse_texture", width=2048, height=2048)
image_normal = bpy.data.images.new("normal_texture", width=2048, height=2048, alpha=False, float_buffer=True)
scene_copy = bpy.data.objects['scene_copy']
bpy.context.view_layer.objects.active = scene_copy
scene_copy.select_set(True)
material = scene_copy.data.materials[0]
nodes = material.node_tree.nodes
links = material.node_tree.links
texture_diffuse_node = nodes.new(type="ShaderNodeTexImage")
texture_diffuse_node.image = image_diffuse
texture_diffuse_node.name = 'diffuse_texture'
texture_normal_node = nodes.new(type="ShaderNodeTexImage")
texture_normal_node.image = image_normal
texture_normal_node.name = 'normal_texture'
normal_map_node = nodes.new(type="ShaderNodeNormalMap")
links.new(texture_diffuse_node.outputs["Color"], nodes["Principled BSDF"].inputs["Base Color"])
links.new(texture_normal_node.outputs["Color"], normal_map_node.inputs["Color"])
links.new(normal_map_node.outputs["Normal"], nodes["Principled BSDF"].inputs["Normal"])

# UV
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=0.01)
bpy.ops.object.mode_set(mode='OBJECT')

# Baking 1
node_tree = material.node_tree
normal_texture_node = node_tree.nodes["normal_texture"]
normal_texture_node.select = True
node_tree.nodes.active = normal_texture_node
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 1024  # reduce max render samples to 1024
bpy.context.scene.render.use_bake_multires = True
bpy.ops.object.bake(type='NORMAL')
relative_path = "normal_texture.png"
file_path = os.path.join(os.path.dirname(__file__), relative_path)
image_normal.filepath_raw = file_path
image_normal.file_format = 'PNG'
image_normal.save()


# Baking 2
node_tree = material.node_tree
diffuse_texture_node = node_tree.nodes["diffuse_texture"]
diffuse_texture_node.select = True
node_tree.nodes.active = diffuse_texture_node
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 1024
bpy.context.scene.render.use_bake_multires = False
bpy.context.scene.render.bake.use_pass_color = True
bpy.context.scene.render.bake.use_pass_direct = False
bpy.context.scene.render.bake.use_pass_indirect = False
bpy.context.scene.render.bake.use_selected_to_active = True
bpy.context.scene.render.bake.use_cage = True
bpy.context.scene.render.bake.cage_extrusion = 0.1

# Save baked image to disk
relative_path = "diffuse_texture.png"
file_path = os.path.join(os.path.dirname(__file__), relative_path)
image_diffuse.filepath_raw = file_path
image_diffuse.file_format = 'PNG'
image_diffuse.save()


bpy.ops.wm.save_mainfile()

