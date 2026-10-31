# Shipping container, long along game x. 1 unit = 10 world px. Green = recolour mask.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bpy
from blib import reset, mat, box, empty, render

OUT = sys.argv[sys.argv.index('--out') + 1]
os.makedirs(OUT, exist_ok=True)
L, W, H = 6.0, 2.8, 2.05
reset(res=192, ortho=9.0, target_z=H/2, samples=40, line=1.3)
paint = mat('mask', (0, 0.82, 0), 0.55)
trim = mat('trim', (0.06, 0.065, 0.07), 0.6)
steel = mat('steel', (0.35, 0.36, 0.38), 0.5, 0.6)
root = empty('root')
box('shell', (L, W, H), (0, 0, H/2), paint, 0.05, root)
# corrugation ribs on both long sides and the roof
n = 22
for i in range(n):
    x = -L/2 + 0.2 + i * (L - 0.4) / (n - 1)
    for s in (-1, 1):
        box('rib', (0.09, 0.06, H - 0.22), (x, s * (W/2 + 0.02), H/2), paint, 0.0, root)
    box('rrib', (0.09, W - 0.2, 0.05), (x, 0, H + 0.02), paint, 0.0, root)
# corner posts and rails
for sx in (-1, 1):
    for sy in (-1, 1):
        box('post', (0.16, 0.16, H + 0.02), (sx * (L/2 - 0.06), sy * (W/2 - 0.06), H/2), trim, 0.01, root)
    box('rail', (0.12, W, 0.14), (sx * (L/2 - 0.06), 0, H - 0.04), trim, 0.01, root)
    box('rail', (0.12, W, 0.14), (sx * (L/2 - 0.06), 0, 0.07), trim, 0.01, root)
# door end (+x): two doors with lock bars
for sy in (-1, 1):
    box('door', (0.05, W/2 - 0.14, H - 0.3), (L/2 + 0.02, sy * (W/4), H/2), paint, 0.0, root)
    for k in (-0.35, 0.35):
        box('bar', (0.06, 0.05, H - 0.4), (L/2 + 0.06, sy * (W/4) + k * 0.6, H/2), steel, 0.0, root)
# a white stencil panel on the long side
box('label', (1.0, 0.03, 0.28), (-1.6, -(W/2 + 0.06), H - 0.45), mat('label', (0.85, 0.85, 0.82), 0.6), 0.0, root)
render(os.path.join(OUT, 'container.png'))
print('done')
