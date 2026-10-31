# Shared Blender setup for Block by Block renders: 2:1 isometric ortho camera, outlines, soft light.
import bpy, math, bmesh
from mathutils import Vector

def reset(res=128, ortho=4.4, target_z=0.25, samples=40, line=1.15):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = samples; sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    sc.render.use_freestyle = line > 0
    sc.render.line_thickness_mode = 'ABSOLUTE'; sc.render.line_thickness = line
    vl = sc.view_layers[0]; vl.use_freestyle = line > 0
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new('L')
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('LS')
    ls.select_by_visibility = True; ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    fs.crease_angle = math.radians(140)
    ls.linestyle.color = (0.06, 0.06, 0.075); ls.linestyle.thickness = line
    w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.42, 0.44, 0.5, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.9
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam'))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = ortho
    el = math.radians(30); d = 40
    cam.location = (d*math.cos(el)/math.sqrt(2), -d*math.cos(el)/math.sqrt(2), d*math.sin(el))
    cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat('-Z', 'Y').to_euler()
    cam.location += Vector((0, 0, target_z))
    cam.data.clip_end = 200
    sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN'))
    sun.data.energy = 3.2; sun.data.angle = math.radians(12)
    sc.collection.objects.link(sun)
    sun.rotation_euler = Vector((0.55, -1.0, 1.25)).to_track_quat('Z', 'Y').to_euler()
    return sc

def mat(name, rgb, rough=0.45, metal=0.0, emit=None, estr=4.0):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1); b.inputs['Emission Strength'].default_value = estr
    return m

def box(name, size, loc, m, bevel=0.06, parent=None, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if rot: o.rotation_euler = rot
    if bevel:
        bv = o.modifiers.new('B', 'BEVEL'); bv.width = bevel; bv.segments = 2
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def cyl(name, r, depth, loc, m, rot=(0, 0, 0), parent=None, verts=16):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, rotation=rot, vertices=verts)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def sphere(name, r, loc, m, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=16, ring_count=10)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    bpy.ops.object.shade_smooth()
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if parent: o.parent = parent
    return o

def render(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
