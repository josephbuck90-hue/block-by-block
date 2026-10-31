# Block by Block characters: every unit type + pedestrian, 8 headings x 6 poses (idle, walk x4, attack).
# Masks: green (0,1,0) = gang main colour, magenta (1,0,1) = gang dark colour, blue (0,0,1) = skin.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from blib import reset, mat, box, cyl, sphere, empty, render

OUT = sys.argv[sys.argv.index('--out') + 1]
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
os.makedirs(OUT, exist_ok=True)
DIRS = 8
POSES = ['idle', 'w0', 'w1', 'w2', 'w3', 'atk']

def M(n):
    tbl = {
        'main': ((0, 1, 0), .5), 'dark': ((1, 0, 1), .5), 'skin': ((0, 0, 1), .6),
        'black': ((.035, .035, .04), .6), 'shoe': ((.03, .03, .035), .5), 'white': ((.85, .85, .83), .6),
        'grey': ((.5, .52, .55), .55), 'lgrey': ((.68, .7, .73), .55), 'steel': ((.3, .31, .33), .35),
        'wood': ((.42, .25, .12), .7), 'gold': ((.85, .65, .18), .3), 'vest': ((.13, .14, .16), .6),
        'olive': ((.24, .26, .17), .7), 'navy': ((.06, .08, .14), .6), 'coat': ((.1, .1, .12), .6),
        'brown': ((.36, .24, .14), .7), 'tank': ((.28, .3, .2), .6), 'glass': ((.4, .7, .9), .1),
        'snitch': ((.3, .31, .34), .65), 'jeans': ((.12, .16, .26), .7),
    }
    if n == 'fire': return mat('fire', (1, .55, .1), .5, emit=(1, .5, .1), estr=6)
    rgb, r = tbl[n]
    metal = .6 if n in ('steel', 'gold') else 0
    return mat(n, rgb, r, metal)

# type spec: torso, torso2 (overlay), pants, hat, weapon, size tweaks
SPEC = {
    'runner':  dict(torso='lgrey', stripe='main', pants='grey', hat='cap', weapon='none', pack='brown', shoe='white'),
    'thug':    dict(torso='main', arms='skin', pants='black', hat='bandana', weapon='bat', w=1.08),
    'shooter': dict(torso='main', pants='black', hat='hood', weapon='pistol'),
    'enforcer':dict(torso='dark', over='vest', stripe='main', pants='black', hat='beanie', weapon='shotgun', w=1.1),
    'slinger': dict(torso='main', shirt='white', chain='gold', pants='black', hat='shades', weapon='dual'),
    'hitman':  dict(torso='coat', long=True, tie='main', pants='black', hat='fedora', weapon='rifle'),
    'brute':   dict(torso='main', arms='skin', pants='brown', hat='bald', weapon='hammer', w=1.18),
    'torcher': dict(torso='main', pants='black', hat='gasmask', weapon='molotov', pack='tank'),
    'scrapper':dict(torso='dark', stripe2='white', collar='main', pants='black', hat='headband', weapon='chain', shoe='white'),
    'gunner':  dict(torso='dark', over='vest', stripe='main', pants='black', hat='capback', weapon='smg', w=1.05),
    'snitch':  dict(torso='snitch', badge='main', pants='jeans', hat='flat', weapon='pistol'),
    'officer': dict(torso='main', belt='black', pants='dark', hat='police', weapon='pistol'),
    'guard':   dict(torso='olive', pants='black', hat='beanie', weapon='pistol'),
    'swat':    dict(torso='navy', over='vest', pants='navy', hat='helmet', weapon='rifle', w=1.08),
    'boss':    dict(torso='dark', shirt='white', tie='main', chain='gold', pants='black', hat='bossfedora', weapon='goldpistol', w=1.04),
    'ped':     dict(torso='main', pants='dark', hat='hair', weapon='none'),
}

TWO_HANDED = {'shotgun', 'rifle', 'smg'}
MELEE = {'bat', 'hammer', 'chain'}

def build(t):
    sp = SPEC[t]; wk = sp.get('w', 1.0) * 1.1
    root = empty('root')
    parts = {}
    sk = sp.get('shoe', 'shoe')
    # legs (pivot at hips)
    for side, y in (('L', .17), ('R', -.17)):
        hip = empty('hip' + side, (0, y * wk, .78), root)
        box('leg', (.27, .25 * wk, .72), (0, 0, -.36), M(sp['pants']), .04, hip)
        box('shoe', (.38, .27 * wk, .14), (.06, 0, -.73), M(sk), .03, hip)
        parts['hip' + side] = hip
    # pelvis + torso
    box('pelvis', (.4, .58 * wk, .26), (0, 0, 1.05), M(sp['pants']), .05, root)
    tl = .95 if sp.get('long') else .8
    box('torso', (.42, .68 * wk, .82), (0, 0, 1.56), M(sp['torso']), .09, root)
    if sp.get('long'):
        box('coattail', (.46, .7 * wk, .6), (-.01, 0, 1.0), M(sp['torso']), .06, root)
    if sp.get('over'):
        box('vest', (.47, .72 * wk, .6), (0, 0, 1.6), M(sp['over']), .07, root)
        for yy in (-.17, .17): box('pouch', (.08, .14, .14), (.25, yy * wk, 1.42), M('grey'), .02, root)
    if sp.get('stripe'):
        box('stripe', (.48, .74 * wk, .1), (0, 0, 1.72), M(sp['stripe']), .02, root)
    if sp.get('stripe2'):
        for yy in (-.36, .36): box('st2', (.44, .04, .8), (0, yy * wk, 1.56), M(sp['stripe2']), 0, root)
    if sp.get('collar'):
        box('collar', (.44, .7 * wk, .1), (0, 0, 1.95), M(sp['collar']), .02, root)
    if sp.get('shirt'):
        box('shirt', (.04, .2, .55), (.215, 0, 1.68), M(sp['shirt']), 0, root)
    if sp.get('tie'):
        box('tie', (.04, .08, .42), (.24, 0, 1.68), M(sp['tie']), 0, root)
    if sp.get('chain'):
        box('chain', (.05, .26, .05), (.235, 0, 1.82), M(sp['chain']), .01, root)
    if sp.get('badge'):
        box('badge', (.04, .1, .1), (.225, -.18, 1.8), M(sp['badge']), 0, root)
    if sp.get('belt'):
        box('belt', (.45, .7 * wk, .08), (0, 0, 1.2), M(sp['belt']), .01, root)
        box('badge', (.04, .1, .1), (.225, .16, 1.8), M('gold'), 0, root)
    if sp.get('pack') == 'brown':
        box('pack', (.24, .5, .55), (-.32, 0, 1.6), M('brown'), .07, root)
    if sp.get('pack') == 'tank':
        for yy in (-.13, .13): cyl('tank', .13, .62, (-.33, yy, 1.58), M('tank'), parent=root)
    # head
    head = empty('head', (0, 0, 2.2), root)
    hat = sp['hat']
    sphere('head', .27, (0, 0, 0), M('skin'), (1, .92, 1.08), head)
    if hat not in ('gasmask', 'hood', 'helmet'):
        box('eye', (.02, .05, .05), (.26, -.09, .03), M('black'), 0, head)
        box('eye', (.02, .05, .05), (.26, .09, .03), M('black'), 0, head)
    if hat == 'cap':
        sphere('cap', .285, (0, 0, .06), M('main'), (1, 1, .62), head); box('brim', (.22, .34, .04), (.24, 0, .1), M('main'), .02, head)
    elif hat == 'capback':
        sphere('cap', .285, (0, 0, .06), M('dark'), (1, 1, .62), head); box('brim', (.22, .34, .04), (-.24, 0, .1), M('dark'), .02, head)
        box('logo', (.03, .1, .07), (.27, 0, .13), M('main'), 0, head)
    elif hat == 'bandana':
        sphere('band', .29, (0, 0, .06), M('main'), (1, 1, .66), head); box('knot', (.16, .07, .12), (-.33, 0, .03), M('main'), .02, head)
    elif hat == 'hood':
        sphere('hood', .34, (-.04, 0, .02), M('main'), (1, 1, 1.05), head)
        box('face', (.04, .26, .3), (.29, 0, -.01), M('skin'), .03, head)
        box('eye', (.02, .05, .05), (.315, -.07, .03), M('black'), 0, head); box('eye', (.02, .05, .05), (.315, .07, .03), M('black'), 0, head)
    elif hat == 'beanie':
        sphere('beanie', .29, (0, 0, .07), M('black'), (1, 1, .7), head); box('band', (.5, .58, .06), (0, 0, .02), M('main'), .02, head)
    elif hat == 'shades':
        sphere('hair', .285, (-.02, 0, .05), M('black'), (1, 1, .7), head); box('shades', (.05, .44, .08), (.26, 0, .04), M('black'), .01, head)
    elif hat == 'fedora' or hat == 'bossfedora':
        c = 'white' if hat == 'bossfedora' else 'coat'
        cyl('brim', .42, .04, (0, 0, .2), M(c), parent=head); cyl('crown', .25, .26, (0, 0, .33), M(c), parent=head)
        cyl('band', .255, .07, (0, 0, .25), M('main'), parent=head)
        if hat == 'bossfedora': box('cigar', (.2, .04, .04), (.34, -.06, -.1), M('brown'), 0, head)
    elif hat == 'bald':
        box('beard', (.06, .3, .12), (.25, 0, -.14), M('black'), .02, head)
    elif hat == 'gasmask':
        sphere('mask', .29, (0, 0, 0), M('grey'), (1, 1, 1.05), head)
        for yy in (-.1, .1): cyl('lens', .07, .04, (.26, yy, .06), M('glass'), (0, math.pi / 2, 0), head)
        cyl('filter', .1, .16, (.32, 0, -.12), M('black'), (0, math.pi / 2, 0), head)
    elif hat == 'headband':
        sphere('hair', .285, (-.02, 0, .05), M('black'), (1, 1, .7), head); box('hb', (.56, .58, .07), (0, 0, .08), M('main'), .02, head)
    elif hat == 'flat':
        sphere('flat', .3, (.03, 0, .12), M('grey'), (1.1, 1, .45), head)
    elif hat == 'police':
        cyl('cap', .27, .14, (0, 0, .2), M('dark'), parent=head); box('peak', (.18, .34, .04), (.24, 0, .13), M('black'), .02, head)
        box('cbadge', (.03, .07, .07), (.27, 0, .22), M('gold'), 0, head)
    elif hat == 'helmet':
        sphere('helmet', .32, (0, 0, .05), M('navy'), (1, 1, .85), head); box('visor', (.06, .4, .14), (.27, 0, 0), M('glass'), .02, head)
    elif hat == 'hair':
        sphere('hair', .285, (-.03, 0, .06), M('brown'), (1, 1, .72), head)
    # arms (pivot at shoulders)
    arm_m = M(sp.get('arms', sp.get('over') and sp['torso'] or sp['torso']))
    if sp.get('long'): arm_m = M(sp['torso'])
    for side, y in (('L', .43), ('R', -.43)):
        sh = empty('sh' + side, (0, y * wk, 1.88), root)
        box('arm', (.17, .17, .7), (0, 0, -.33), arm_m, .04, sh)
        sphere('hand', .1, (0, 0, -.7), M('skin'), parent=sh)
        hand = empty('hand' + side, (0, 0, -.7), sh)
        parts['sh' + side] = sh; parts['hand' + side] = hand
    # weapon in the right hand; hand-local: weapon points along -Z of the arm when the arm is raised forward
    w = sp['weapon']; hr = parts['handR']
    def gun(length, thick, m='black', extra=None, h=None):
        h = h or hr
        box('gun', (thick, thick * 1.2, length), (0, 0, -length / 2 + .05), M(m), .01, h)
        box('grip', (.07, .08, .14), (-.1, 0, -.02), M(m), 0, h)
    if w == 'pistol': gun(.32, .09)
    if w == 'goldpistol': gun(.34, .1, 'gold')
    if w == 'dual': gun(.32, .09); gun(.32, .09, h=parts['handL'])
    if w == 'shotgun': gun(.95, .1, 'steel'); box('stock', (.12, .1, .3), (0, 0, .2), M('wood'), .02, hr)
    if w == 'rifle': gun(1.2, .08, 'black'); box('scope', (.08, .08, .28), (.1, 0, -.4), M('steel'), .02, hr)
    if w == 'smg': gun(.6, .12, 'black'); box('mag', (.18, .06, .07), (.12, 0, -.2), M('steel'), 0, hr)
    if w == 'bat': cyl('bat', .055, 1.0, (0, 0, -.45), M('wood'), parent=hr)
    if w == 'hammer':
        cyl('handle', .045, 1.15, (0, 0, -.5), M('wood'), parent=hr); box('head', (.24, .24, .42), (0, 0, -1.08), M('steel'), .03, hr, rot=(math.pi / 2, 0, 0))
    if w == 'molotov':
        cyl('bottle', .07, .26, (0, 0, -.12), M('olive'), parent=hr); sphere('flame', .08, (0, 0, -.3), M('fire'), (1, 1, 1.5), hr)
    if w == 'chain':
        for i in range(6): sphere('link', .05, (0, 0, -.12 * i - .05), M('lgrey'), parent=hr)
    for o in root.children:
        if not o.name.startswith('hip'): o.location.z -= .22
    head.scale = (1.12, 1.12, 1.12)
    return root, parts, w

def pose(parts, w, p):
    import math as m
    hl, hrp, sl, sr = parts['hipL'], parts['hipR'], parts['shL'], parts['shR']
    for o in (hl, hrp, sl, sr): o.rotation_euler = (0, 0, 0)
    swing = {'idle': 0, 'w0': 1, 'w1': 0, 'w2': -1, 'w3': 0, 'atk': 0}[p]
    lg = m.radians(28) * swing
    hl.rotation_euler = (0, lg, 0); hrp.rotation_euler = (0, -lg, 0)
    # arms: rotation about Y; -90deg points the arm forward (+X)
    if w in ('none',):
        sl.rotation_euler = (0, -lg * .8, 0); sr.rotation_euler = (0, lg * .8, 0)
    elif w in MELEE:
        if p == 'atk':
            sr.rotation_euler = (0, m.radians(-80), 0)              # swing forward
        else:
            sr.rotation_euler = (m.radians(-15), m.radians(-160), 0)  # weapon raised over the shoulder
        sl.rotation_euler = (0, -lg * .8, 0)
    elif w == 'molotov':
        sr.rotation_euler = (0, m.radians(-150 if p != 'atk' else -60), 0)
        sl.rotation_euler = (0, -lg * .8, 0)
    else:
        aim = m.radians(-88 if p != 'atk' else -100)
        sr.rotation_euler = (0, aim, 0)
        if w in TWO_HANDED:
            sl.rotation_euler = (m.radians(-28), aim + m.radians(8), 0)
        elif w == 'dual':
            sl.rotation_euler = (0, aim, 0)
        else:
            sl.rotation_euler = (0, -lg * .8, 0)

types = ONLY or list(SPEC)
for t in types:
    reset(res=112, ortho=3.6, target_z=1.15, samples=28, line=1.5)
    root, parts, w = build(t)
    for p in POSES:
        pose(parts, w, p)
        for d in range(DIRS):
            th = 2 * math.pi * d / DIRS
            root.rotation_euler = (0, 0, -th)
            render(os.path.join(OUT, f'{t}_{p}_{d}.png'))
    print('done', t)
