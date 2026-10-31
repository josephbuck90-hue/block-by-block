# Street life renders: homeless figures (stand, shuffle, sit, slump, lie), stoop sitters, stray dogs and encampment props.
# Same camera and masks as characters.py: green = clothing colour, magenta = second colour, blue = skin.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from mathutils import Matrix
import characters as C
from blib import reset, mat, box, cyl, sphere, empty, render

OUT = sys.argv[sys.argv.index('--out') + 1]
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
os.makedirs(OUT, exist_ok=True)
DIRS = 8
M = C.M

C.SPEC['bum'] = dict(torso='main', long=True, pants='dark', hat='beanie', weapon='none')
C.SPEC['sitter'] = dict(torso='main', pants='dark', hat='hair', weapon='none')

def spine_rig(root):
    """reparent the upper body to a spine pivot at the pelvis so it can lean"""
    sp = empty('spine', (0, 0, .83), root)
    bpy.context.view_layer.update()
    for o in list(root.children):
        if o is sp or o.name.startswith('hip'): continue
        mw = o.matrix_world.copy(); o.parent = sp; o.matrix_world = mw
    return sp

def add_beard(parts_root):
    head = [o for o in bpy.data.objects if o.name.startswith('head') and o.type == 'EMPTY'][0]
    box('beard', (.08, .34, .2), (.24, 0, -.14), M('brown'), .03, head)
    return head

POSES_BUM = ['stand', 'w0', 'w1', 'w2', 'w3', 'sit', 'slump', 'lie']

def pose_body(root, parts, spine, head, p):
    hl, hr, sl, sr = parts['hipL'], parts['hipR'], parts['shL'], parts['shR']
    for o in (hl, hr, sl, sr, spine, head): o.rotation_euler = (0, 0, 0)
    root.location = (0, 0, 0); root.rotation_euler = (0, 0, 0)
    r = math.radians
    if p in ('stand', 'w0', 'w1', 'w2', 'w3'):
        sw = {'stand': 0, 'w0': 1, 'w1': 0, 'w2': -1, 'w3': 0}[p]
        hl.rotation_euler = (0, r(16) * sw, 0); hr.rotation_euler = (0, -r(16) * sw, 0)
        spine.rotation_euler = (0, r(14), 0)          # hunched
        head.rotation_euler = (0, r(18), 0)
        sl.rotation_euler = (0, r(-10) - r(10) * sw, 0); sr.rotation_euler = (0, r(-10) + r(10) * sw, 0)
    elif p in ('sit', 'slump'):
        root.location = (0, 0, -.62)
        hl.rotation_euler = (r(-6), r(-80), 0); hr.rotation_euler = (r(6), r(-70), 0)
        if p == 'sit':
            spine.rotation_euler = (0, r(-12), 0)     # leaning back on a wall
            sl.rotation_euler = (0, r(-50), 0); sr.rotation_euler = (0, r(-45), 0)
        else:
            spine.rotation_euler = (0, r(40), 0)      # folded forward, nodding off
            head.rotation_euler = (0, r(35), 0)
            sl.rotation_euler = (0, r(-15), 0); sr.rotation_euler = (0, r(-10), 0)
    elif p == 'lie':
        root.rotation_euler = (r(90), 0, 0); root.location = (0, 0, .3)
        hl.rotation_euler = (0, r(-30), 0); hr.rotation_euler = (0, r(-40), 0)
        sl.rotation_euler = (0, r(-40), 0); sr.rotation_euler = (0, r(-30), 0)

def people(t):
    reset(res=112, ortho=3.6, target_z=1.15, samples=28, line=1.5)
    root, parts, w = C.build(t)
    head = add_beard(root) if t == 'bum' else [o for o in bpy.data.objects if o.name.startswith('head') and o.type == 'EMPTY'][0]
    if t == 'bum':   # layered rags: a scarf in the second colour
        box('scarf', (.46, .72, .14), (0, 0, 1.72), M('dark'), .04, root)
    spine = spine_rig(root)
    turn = empty('turn'); root.parent = turn
    poses = POSES_BUM if t == 'bum' else ['sit']
    for p in poses:
        pose_body(root, parts, spine, head, p)
        for d in range(DIRS):
            turn.rotation_euler = (0, 0, -2 * math.pi * d / DIRS)
            render(os.path.join(OUT, f'{t}_{p}_{d}.png'))
    print('done', t)

def dog():
    reset(res=112, ortho=3.6, target_z=.6, samples=28, line=1.5)
    root = empty('root'); fur = M('main'); dk = M('dark')
    box('body', (.95, .38, .38), (0, 0, .62), fur, .12, root)
    nk = empty('neck', (.45, 0, .72), root)
    box('head', (.36, .3, .3), (.16, 0, .14), fur, .1, nk)
    box('snout', (.2, .18, .14), (.38, 0, .07), dk, .04, nk)
    box('nose', (.05, .07, .05), (.48, 0, .12), M('black'), 0, nk)
    for yy in (-.1, .1): box('ear', (.08, .08, .14), (.08, yy, .33), dk, .02, nk)
    tl = empty('tail', (-.48, 0, .74), root); box('tail', (.32, .07, .07), (-.14, 0, .06), dk, .02, tl); tl.rotation_euler = (0, math.radians(-35), 0)
    legs = {}
    for nm, x, y in (('FL', .34, .13), ('FR', .34, -.13), ('BL', -.34, .13), ('BR', -.34, -.13)):
        h = empty('h' + nm, (x, y, .52), root); box('leg', (.11, .11, .5), (0, 0, -.25), fur, .03, h); legs[nm] = h
    for p in ['idle', 'w0', 'w1', 'w2', 'w3']:
        sw = {'idle': 0, 'w0': 1, 'w1': 0, 'w2': -1, 'w3': 0}[p]; a = math.radians(26) * sw
        legs['FL'].rotation_euler = (0, a, 0); legs['BR'].rotation_euler = (0, a, 0)
        legs['FR'].rotation_euler = (0, -a, 0); legs['BL'].rotation_euler = (0, -a, 0)
        nk.rotation_euler = (0, math.radians(18 if p == 'idle' else 0), 0)
        for d in range(DIRS):
            root.rotation_euler = (0, 0, -2 * math.pi * d / DIRS)
            render(os.path.join(OUT, f'dog_{p}_{d}.png'))
    print('done dog')

def props():
    # one view each at 1 unit = 10 world px (same scale as containers)
    reset(res=192, ortho=9.0, target_z=1.0, samples=36, line=1.3)
    def clear():
        for o in list(bpy.data.objects):
            if o.type in ('MESH', 'EMPTY'): bpy.data.objects.remove(o, do_unlink=True)
    import bmesh
    # dome tent: half sphere squashed, tarp mask colour
    clear(); r = empty('root')
    t = sphere('tent', 1.0, (0, 0, 0), M('main'), (1.4, 1.0, .9), r)
    bpy.ops.object.select_all(action='DESELECT')
    box('cut', (4, 4, 2), (0, 0, -1.0), M('black'), 0, r).hide_render = True
    bv = t.modifiers.new('cut', 'BOOLEAN'); bv.object = bpy.data.objects['cut']; bv.operation = 'DIFFERENCE'
    box('door', (.05, .5, .55), (1.38, 0, .28), M('black'), .02, r)
    for yy in (-.6, .6): cyl('pole', .03, 2.4, (0, yy * .9, .4), M('steel'), (0, math.pi / 2, 0), r)
    box('tarp', (1.2, 1.6, .04), (-.9, 0, .02), M('dark'), .0, r)
    render(os.path.join(OUT, 'prop_tent.png'))
    # shopping cart piled with bags
    clear(); r = empty('root'); steel = M('lgrey')
    box('basket', (1.1, .7, .55), (0, 0, .85), steel, .02, r)
    for yy in (-.3, .3):
        cyl('wheelF', .08, .06, (.45, yy, .08), M('black'), (math.pi / 2, 0, 0), r); cyl('wheelB', .08, .06, (-.45, yy, .08), M('black'), (math.pi / 2, 0, 0), r)
        box('leg', (.04, .04, .6), (.45, yy, .4), steel, 0, r); box('leg', (.04, .04, .6), (-.45, yy, .4), steel, 0, r)
    box('handle', (.05, .8, .05), (-.62, 0, 1.2), M('dark'), .01, r)
    for i, (x, y, z, s) in enumerate([(.2, .1, 1.25, .32), (-.2, -.1, 1.3, .3), (0, .15, 1.5, .28), (.25, -.2, 1.45, .22)]):
        sphere('bag', s, (x, y, z), M('main') if i % 2 else M('black'), (1, 1, .85), r)
    render(os.path.join(OUT, 'prop_cart.png'))
    # burn barrel (fire is drawn live in the game)
    clear(); r = empty('root'); rust = mat('rust', (.33, .17, .08), .8, .3)
    cyl('drum', .45, 1.15, (0, 0, .58), rust, parent=r, verts=24)
    for z in (.25, .58, .9): cyl('ring', .47, .05, (0, 0, z), M('black'), parent=r, verts=24)
    cyl('ash', .4, .05, (0, 0, 1.12), mat('ember', (.9, .35, .08), .8, emit=(1, .4, .05), estr=3), parent=r, verts=24)
    render(os.path.join(OUT, 'prop_barrel.png'))
    # cardboard bed with a sleeping bag
    clear(); r = empty('root'); card = mat('card', (.55, .42, .26), .9)
    box('card', (2.1, 1.1, .05), (0, 0, .03), card, .0, r); box('card2', (.9, 1.0, .05), (.7, .1, .07), card, .0, r)
    box('bag', (1.7, .75, .22), (-.1, 0, .17), M('main'), .12, r); sphere('pillow', .25, (.8, 0, .25), M('dark'), (1.2, 1, .6), r)
    render(os.path.join(OUT, 'prop_bed.png'))
    # tarp lean-to against a wall
    clear(); r = empty('root')
    box('tarp', (1.8, .05, 1.4), (0, -.2, .55), M('main'), 0, r, rot=(math.radians(35), 0, 0))
    box('crate', (.5, .5, .4), (.6, .5, .2), mat('crate', (.4, .3, .18), .8), .02, r)
    box('bags', (.6, .4, .3), (-.5, .45, .15), M('black'), .1, r)
    render(os.path.join(OUT, 'prop_leanto.png'))
    print('done props')

todo = ONLY or ['bum', 'sitter', 'dog', 'props']
for t in todo:
    if t in ('bum', 'sitter'): people(t)
    elif t == 'dog': dog()
    elif t == 'props': props()
