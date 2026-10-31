# The Stroll: three women in going-out outfits. Same camera and masks as characters.py:
# green = top/dress colour, magenta = skirt/shorts colour, blue = skin.
# Poses: idle (hand on hip), w0-w3 walk, lean (talking at a car window). 8 headings each.
import sys, os, math, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
from blib import reset, mat, box, cyl, sphere, empty, render
from characters import M

OUT = sys.argv[sys.argv.index('--out') + 1]
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
os.makedirs(OUT, exist_ok=True)
DIRS = 8
POSES = os.environ.get('POSES','idle,w0,w1,w2,w3,lean').split(',')
r = math.radians

VARIANTS = {
    # crop top, mini skirt, heels, long straight hair, hoops
    'g0': dict(top='crop', bottom='skirt', feet='heels', hair='long', hoops=True),
    # tube top, short shorts, knee-high boots, big curls
    'g1': dict(top='tube', bottom='shorts', feet='boots', hair='curls', hoops=True),
    # short strapless dress, fur bolero, heels, long braids, handbag
    'g2': dict(top='dress', bottom='dress', feet='heels', hair='braids', fur=True, bag=True),
}

def torus(name, R, rr, loc, m, parent, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=rr, location=loc, rotation=rot, major_segments=16, minor_segments=6)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m); o.parent = parent; return o

def build(v):
    sp = VARIANTS[v]; skin = M('skin'); top = M('main'); bot = M('dark'); blk = M('black')
    root = empty('root'); parts = {}
    # legs, pivot at the hip
    for side, y in (('L', .15), ('R', -.15)):
        hip = empty('hip' + side, (0, y, .82), root)
        box('thigh', (.25, .25, .42), (0, 0, -.2), skin, .05, hip)
        if sp['feet'] == 'boots':
            box('boot', (.27, .27, .44), (0, 0, -.6), blk, .04, hip)
            box('sole', (.34, .26, .08), (.04, 0, -.8), blk, .02, hip)
        else:
            box('shin', (.22, .22, .4), (0, 0, -.58), skin, .05, hip)
            box('heel', (.32, .2, .08), (.05, 0, -.79), blk, .02, hip)
            box('spike', (.06, .07, .14), (-.06, 0, -.84), blk, 0, hip)
        parts['hip' + side] = hip
    spine = empty('spine', (0, 0, .9), root)
    # hips / lower clothing
    if sp['bottom'] == 'skirt':
        box('skirt', (.52, .64, .3), (0, 0, .1), bot, .05, spine)
    elif sp['bottom'] == 'shorts':
        box('shorts', (.48, .6, .18), (0, 0, .15), bot, .04, spine)
    else:
        box('dress', (.52, .64, .34), (0, 0, .1), top, .05, spine)
    # waist and chest
    if sp['top'] == 'dress':
        box('dressbody', (.44, .58, .5), (0, 0, .5), top, .07, spine)
    else:
        box('waist', (.38, .52, .26), (0, 0, .38), skin, .06, spine)
        box('belt', (.42, .56, .05), (0, 0, .26), blk, .01, spine) if sp['bottom'] == 'shorts' else None
    hgt = .26 if sp['top'] == 'crop' else .22
    box('top', (.46, .64, hgt), (.01, 0, .64), top, .07, spine)
    box('bust', (.12, .5, .14), (.2, 0, .64), top, .05, spine)
    # bare shoulders and neck
    if sp['top'] == 'crop':
        box('shoulders', (.4, .66, .14), (0, 0, .82), skin, .05, spine)
        for yy in (-.18, .18): box('strap', (.38, .06, .1), (0, yy, .8), top, 0, spine)
    else:
        box('shoulders', (.38, .66, .16), (0, 0, .81), skin, .05, spine)
    cyl('neck', .1, .14, (0, 0, .94), skin, parent=spine)
    if sp.get('fur'):
        box('fur', (.5, .76, .26), (-.03, 0, .78), M('white'), .1, spine)
    # head
    head = empty('head', (0, 0, 1.18), spine)
    sphere('head', .25, (0, 0, 0), skin, (1, .92, 1.08), head)
    box('eye', (.02, .05, .05), (.24, -.08, .03), blk, 0, head); box('eye', (.02, .05, .05), (.24, .08, .03), blk, 0, head)
    box('lips', (.02, .1, .04), (.235, 0, -.11), mat('lips', (.45, .08, .12), .4), 0, head)
    h = sp['hair']; hair = blk
    if h == 'long':
        sphere('hair', .265, (-.05, 0, .07), hair, (.95, 1.04, .78), head)
        box('hairback', (.14, .54, .56), (-.18, 0, -.22), hair, .05, head)
    elif h == 'curls':
        sphere('hair', .33, (-.12, 0, .1), hair, (.9, 1.05, .9), head)
    elif h == 'braids':
        sphere('hair', .265, (-.05, 0, .07), hair, (.95, 1.04, .78), head)
        for yy in (-.12, -.04, .04, .12): box('braid', (.08, .08, .62), (-.2, yy*1.2, -.28), hair, .02, head)
    if sp.get('hoops'):
        for yy in (-.25, .25): torus('hoop', .07, .016, (0, yy, -.1), M('gold'), head, (math.pi / 2, 0, 0))
    # arms, pivot at the shoulder
    for side, y in (('L', .4), ('R', -.4)):
        sh = empty('sh' + side, (0, y, .82), spine)
        if sp.get('fur'): box('sleeve', (.22, .22, .26), (0, 0, -.1), M('white'), .06, sh)
        box('upper', (.16, .16, .34), (0, 0, -.16), skin, .04, sh)
        el = empty('el' + side, (0, 0, -.32), sh)
        box('fore', (.15, .15, .3), (0, 0, -.15), skin, .04, el)
        sphere('hand', .09, (0, 0, -.33), skin, parent=el)
        if side == 'R': box('bangle', (.18, .18, .04), (0, 0, -.25), M('gold'), .01, el)
        parts['sh' + side] = sh; parts['el' + side] = el
    if sp.get('bag'):
        box('bag', (.14, .3, .24), (0, .1, -.48), bot, .03, parts['elL'])
        box('bagstrap', (.02, .02, .14), (0, .07, -.32), blk, 0, parts['elL'])
    return root, parts, spine, head

def pose(parts, spine, head, p):
    hl, hr, sl, sr, el, er = parts['hipL'], parts['hipR'], parts['shL'], parts['shR'], parts['elL'], parts['elR']
    for o in (hl, hr, sl, sr, el, er, spine, head): o.rotation_euler = (0, 0, 0)
    if p == 'idle':   # weight on one leg, hand on the hip
        hl.rotation_euler = (r(-4), 0, 0); hr.rotation_euler = (r(-10), r(-8), 0)
        spine.rotation_euler = (r(5), 0, 0)
        sr.rotation_euler = (r(-38), r(-10), 0); er.rotation_euler = (r(85), 0, 0)
        sl.rotation_euler = (r(-4), r(6), 0)
        head.rotation_euler = (r(-4), 0, r(8))
    elif p in ('w0', 'w1', 'w2', 'w3'):
        sw = {'w0': 1, 'w1': 0, 'w2': -1, 'w3': 0}[p]
        hl.rotation_euler = (0, r(24) * sw, 0); hr.rotation_euler = (0, -r(24) * sw, 0)
        sl.rotation_euler = (0, -r(20) * sw, 0); sr.rotation_euler = (0, r(20) * sw, 0)
        el.rotation_euler = (0, r(-15), 0); er.rotation_euler = (0, r(-15), 0)
        spine.rotation_euler = (r(3) * sw, 0, 0)
    elif p == 'lean':  # bent toward a car window, one forearm resting forward
        spine.rotation_euler = (0, r(28), 0); head.rotation_euler = (0, r(-12), 0)
        hl.rotation_euler = (0, r(-6), 0); hr.rotation_euler = (r(-6), r(4), 0)
        sr.rotation_euler = (0, r(-70), 0); er.rotation_euler = (0, r(-40), 0)
        sl.rotation_euler = (r(38), r(10), 0); el.rotation_euler = (r(-85), 0, 0)

meta = {}
for v in (ONLY or list(VARIANTS)):
    reset(res=224, ortho=3.6, target_z=1.15, samples=28, line=1.6)
    ls = bpy.context.scene.view_layers[0].freestyle_settings.linesets[0]; ls.select_crease = False; ls.select_border = False
    root, parts, spine, head = build(v)
    turn = empty('turn'); root.parent = turn
    sc = bpy.context.scene
    o = world_to_camera_view(sc, sc.camera, Vector((0, 0, 0)))
    meta['origin'] = [o.x * 224, (1 - o.y) * 224]
    for p in POSES:
        pose(parts, spine, head, p)
        for d in [int(x) for x in os.environ.get('DIRSEL','0,1,2,3,4,5,6,7').split(',')]:
            turn.rotation_euler = (0, 0, -2 * math.pi * d / DIRS)
            render(os.path.join(OUT, f'{v}_{p}_{d}.png'))
    print('done', v)
json.dump(meta, open(os.path.join(OUT, 'origin.json'), 'w'))
