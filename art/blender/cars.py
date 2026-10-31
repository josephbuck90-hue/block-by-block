# Block by Block vehicle renders: 5 vehicles x 16 headings, 2:1 isometric, outlined, transparent.
# Model units: 1 = the vehicle's radius r in game. Car faces +X. Pure green (0,1,0) paint = recolour mask.
import bpy, math, os, sys
from mathutils import Vector

OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else '/tmp/cars'
RES = 128
ORTHO = 4.4
DIRS = 16
os.makedirs(OUT, exist_ok=True)

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 48
    sc.cycles.use_denoising = False
    sc.render.resolution_x = sc.render.resolution_y = RES
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'
    sc.view_settings.view_transform = 'Standard'
    sc.render.use_freestyle = True
    sc.render.line_thickness_mode = 'ABSOLUTE'
    sc.render.line_thickness = 1.15
    vl = sc.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    ls = fs.linesets[0] if fs.linesets else fs.linesets.new('L')
    ls.select_by_visibility = True
    ls.select_by_edge_types = True
    ls.select_silhouette = True; ls.select_border = True; ls.select_crease = True
    fs.crease_angle = math.radians(140)
    if ls.linestyle is None: ls.linestyle = bpy.data.linestyles.new('LS')
    ls.linestyle.color = (0.06, 0.06, 0.075)
    ls.linestyle.thickness = 1.15
    w = bpy.data.worlds.new('W'); sc.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.42, 0.44, 0.5, 1)
    w.node_tree.nodes['Background'].inputs[1].default_value = 0.9
    # camera: game iso = ortho, elevation 30deg, looking from game (+x,+y) = blender (+x,-y)
    cam = bpy.data.objects.new('Cam', bpy.data.cameras.new('Cam'))
    sc.collection.objects.link(cam); sc.camera = cam
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = ORTHO
    el = math.radians(30); d = 20
    cam.location = (d * math.cos(el) / math.sqrt(2), -d * math.cos(el) / math.sqrt(2), d * math.sin(el))
    direction = Vector((0, 0, 0.25)) - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
    cam.location += Vector((0, 0, 0.25))
    sun = bpy.data.objects.new('Sun', bpy.data.lights.new('Sun', 'SUN'))
    sun.data.energy = 3.2; sun.data.angle = math.radians(12)
    sc.collection.objects.link(sun)
    # light from screen-left/front (game south-west-ish) like the painted buildings
    sun.rotation_euler = Vector((0.55, -1.0, 1.25)).to_track_quat('Z', 'Y').to_euler()

def mat(name, rgb, rough=0.45, metal=0.0, emit=None):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit:
        b.inputs['Emission Color'].default_value = (*emit, 1)
        b.inputs['Emission Strength'].default_value = 4.0
    return m

def box(name, size, loc, m, bevel=0.06, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object; o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bv = o.modifiers.new('B', 'BEVEL'); bv.width = bevel; bv.segments = 2
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def taper(name, lb, wb, lt, wt, h, loc, m, shift=0.0, parent=None):
    """cabin: bottom LxW, top LxW, top shifted back by `shift`"""
    import bmesh
    me = bpy.data.meshes.new(name); o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    bm = bmesh.new()
    v = [bm.verts.new(p) for p in [(-lb/2,-wb/2,0),(lb/2,-wb/2,0),(lb/2,wb/2,0),(-lb/2,wb/2,0),
                                   (-lt/2-shift,-wt/2,h),(lt/2-shift,-wt/2,h),(lt/2-shift,wt/2,h),(-lt/2-shift,wt/2,h)]]
    for f in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]:
        bm.faces.new([v[i] for i in f])
    bm.to_mesh(me); bm.free()
    o.location = loc
    bv = o.modifiers.new('B', 'BEVEL'); bv.width = 0.035; bv.segments = 2
    o.data.materials.append(m)
    if parent: o.parent = parent
    return o

def wheel(x, y, r, root):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=0.2, location=(x, y, r), rotation=(math.pi/2, 0, 0), vertices=20)
    o = bpy.context.active_object; o.data.materials.append(mat('tyre', (0.03, 0.03, 0.035), 0.8)); o.parent = root
    bpy.ops.mesh.primitive_cylinder_add(radius=r*0.55, depth=0.22, location=(x, y, r), rotation=(math.pi/2, 0, 0), vertices=16)
    o = bpy.context.active_object; o.data.materials.append(mat('rim', (0.45, 0.46, 0.5), 0.35, 0.8)); o.parent = root

def lights(L, W, z, root, hw=0.14):
    for s in (-1, 1):
        box('hl', (0.05, hw, 0.07), (L/2, s*(W/2-0.16), z), mat('head', (1, 0.95, 0.8), emit=(1, 0.9, 0.6)), 0.01, root)
        box('tl', (0.05, hw, 0.07), (-L/2, s*(W/2-0.16), z), mat('tail', (0.8, 0.05, 0.05), emit=(1, 0.05, 0.03)), 0.01, root)

def root_obj():
    o = bpy.data.objects.new('root', None); bpy.context.scene.collection.objects.link(o); return o

GLASS = lambda: mat('glass', (0.05, 0.08, 0.12), 0.08, 0.2)
MASK = lambda: mat('mask', (0, 1, 0), 0.35)
MASKD = lambda: mat('maskdark', (0, 0.32, 0), 0.35)
TRIM = lambda: mat('trim', (0.07, 0.07, 0.08), 0.5)

def sedan(root, paint, cop=False):
    L, W = 2.4, 1.2
    box('body', (L, W, 0.34), (0, 0, 0.36), paint, 0.1, root)
    box('bumpF', (0.08, W*0.95, 0.12), (L/2, 0, 0.24), TRIM(), 0.03, root)
    box('bumpR', (0.08, W*0.95, 0.12), (-L/2, 0, 0.24), TRIM(), 0.03, root)
    taper('cabin', 1.25, 1.06, 0.82, 0.92, 0.3, (-0.12, 0, 0.53), GLASS(), 0.06, root)
    box('roof', (0.78, 0.9, 0.05), (-0.18, 0, 0.84), paint, 0.03, root)
    if cop:
        box('bar', (0.16, 0.7, 0.07), (-0.16, 0, 0.9), TRIM(), 0.02, root)
        box('red', (0.14, 0.3, 0.06), (-0.16, -0.18, 0.95), mat('red', (1, 0.1, 0.1), emit=(1, 0.08, 0.05)), 0.01, root)
        box('blue', (0.14, 0.3, 0.06), (-0.16, 0.18, 0.95), mat('blue', (0.1, 0.3, 1), emit=(0.1, 0.35, 1)), 0.01, root)
        for s in (-1, 1):  # black doors on a white car
            box('door', (0.95, 0.03, 0.26), (-0.05, s*(W/2+0.005), 0.36), TRIM(), 0.01, root)
    for x in (-0.78, 0.78):
        for y in (-0.52, 0.52): wheel(x, y, 0.21, root)
    lights(L, W, 0.42, root)

def suv(root):
    L, W = 2.45, 1.3
    box('body', (L, W, 0.46), (0, 0, 0.44), MASKD(), 0.1, root)
    box('stripe', (L*0.9, W+0.01, 0.05), (0, 0, 0.5), MASK(), 0.0, root)
    taper('cabin', 1.75, 1.18, 1.55, 1.08, 0.36, (-0.2, 0, 0.67), GLASS(), 0.04, root)
    box('roof', (1.5, 1.06, 0.05), (-0.24, 0, 1.05), MASKD(), 0.03, root)
    box('rack', (1.1, 0.9, 0.03), (-0.24, 0, 1.1), TRIM(), 0.01, root)
    box('bull', (0.1, W*0.8, 0.2), (L/2+0.03, 0, 0.32), TRIM(), 0.03, root)
    for x in (-0.8, 0.82):
        for y in (-0.56, 0.56): wheel(x, y, 0.25, root)
    lights(L, W, 0.55, root)

def van(root):
    L, W = 2.6, 1.45
    steel = mat('steel', (0.2, 0.21, 0.23), 0.55, 0.4)
    box('body', (L*0.74, W, 1.05), (-L*0.13, 0, 0.72), steel, 0.08, root)
    box('cab', (L*0.28, W, 0.72), (L*0.36, 0, 0.56), steel, 0.08, root)
    taper('wind', 0.2, W*0.9, 0.12, W*0.86, 0.32, (L*0.47, 0, 0.62), GLASS(), 0.04, root)
    box('stripe', (L*0.98, W+0.01, 0.12), (0, 0, 0.7), MASK(), 0.0, root)
    for i in range(4):
        box('slit', (0.14, 0.02, 0.06), (-0.9+i*0.36, -(W/2+0.01), 0.98), TRIM(), 0.0, root)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.16, location=(-0.4, 0, 1.33), vertices=16)
    t = bpy.context.active_object; t.data.materials.append(steel); t.parent = root
    box('gun', (0.5, 0.06, 0.06), (-0.1, 0, 1.36), TRIM(), 0.0, root)
    for x in (-0.85, 0.85):
        for y in (-0.62, 0.62): wheel(x, y, 0.27, root)
    lights(L, W, 0.42, root)

def truck(root):
    L, W = 2.6, 1.45
    white = mat('truckwhite', (0.72, 0.73, 0.7), 0.45, 0.2)
    box('body', (L*0.7, W, 1.1), (-L*0.15, 0, 0.78), white, 0.08, root)
    box('cab', (L*0.3, W, 0.78), (L*0.35, 0, 0.6), mat('truckgrey', (0.32, 0.34, 0.37), 0.5, 0.3), 0.08, root)
    taper('wind', 0.2, W*0.9, 0.12, W*0.86, 0.32, (L*0.47, 0, 0.66), GLASS(), 0.04, root)
    box('band', (L*0.7, W+0.01, 0.16), (-L*0.15, 0, 0.95), mat('gold', (0.75, 0.6, 0.2), 0.4, 0.6), 0.0, root)
    for x in (-0.85, 0.85):
        for y in (-0.62, 0.62): wheel(x, y, 0.27, root)
    lights(L, W, 0.45, root)

BUILDS = {
    'civ': lambda r: sedan(r, MASK()),
    'ride': suv,
    'van': van,
    'cruiser': lambda r: sedan(r, mat('copwhite', (0.85, 0.86, 0.88), 0.35), cop=True),
    'truck': truck,
}

only = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else list(BUILDS)
for name in only:
    reset()
    root = root_obj()
    BUILDS[name](root)
    for i in range(DIRS):
        th = 2 * math.pi * i / DIRS          # game heading (x east, y south)
        root.rotation_euler = (0, 0, -th)    # game y is blender -y
        bpy.context.scene.render.filepath = os.path.join(OUT, f'{name}_{i:02d}.png')
        bpy.ops.render.render(write_still=True)
    print('done', name)
