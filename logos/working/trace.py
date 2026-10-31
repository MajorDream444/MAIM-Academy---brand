"""Trace the MAIM Academy crest interior into grouped vector paths.

Output: work/paths.json  {group: [svg path d, ...]}, coordinates in source px (1254 canvas).
"""
import json, sys
import numpy as np, cv2, potrace

SRC = sys.argv[1] if len(sys.argv) > 1 else 'work/orig.png'
UP = 3                      # upsample factor for smoother curves
CX, CY = 621.9, 607.9       # fitted crest centre

im = cv2.imread(SRC)
v = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)[..., 2]
H, W = v.shape
vu = cv2.resize(v, (W * UP, H * UP), interpolation=cv2.INTER_CUBIC)
vu = cv2.GaussianBlur(vu, (0, 0), 1.2 * UP / 2)
yy, xx = np.mgrid[:H * UP, :W * UP]
rr = np.hypot(xx / UP - CX, yy / UP - CY)
mask = ((vu > 70) & (rr < 497)).astype(np.uint8)

# label at source resolution so group rules use source coordinates
n, lab, st, cen = cv2.connectedComponentsWithStats(mask, 8)

def group_of(x, y, w, h, area):
    """Classify a component by its source-px bbox."""
    if area < 40 * UP * UP:
        return None                       # specks / texture noise
    cyc = y + h / 2
    if y < 200 and h > 300:
        return 'monogram'
    if 585 <= y and y + h <= 770 and 390 <= x and x + w <= 860:
        return 'braid'
    if 600 <= y < 680 and 490 <= x <= 600:
        return 'braid'                    # small fragments under the monogram
    if cyc > 1015:
        return 'rule'
    if y >= 860 and h > 90:
        return 'lettering'
    return 'book'

groups = {}
for i in range(1, n):
    x, y, w, h, a = st[i]
    g = group_of(x / UP, y / UP, w / UP, h / UP, a)
    if g:
        groups.setdefault(g, []).append(i)

def disk(r):
    r = max(1, int(round(r * UP)))
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def fill_small_holes(m, max_area, grow=0, close=0, smooth=0):
    """Close bevel slits, fill interior holes < max_area (source px^2),
    optionally dilate, then smooth edges (blur + re-threshold)."""
    m = m.astype(np.uint8)
    if close:
        m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, disk(close))
    inv = 1 - m
    k, hl, hs, _ = cv2.connectedComponentsWithStats(inv, 4)
    for j in range(1, k):
        x, y, w, h, a = hs[j]
        touches_edge = x == 0 or y == 0 or x + w == m.shape[1] or y + h == m.shape[0]
        if not touches_edge and a < max_area * UP * UP:
            m[hl == j] = 1
    if grow:
        m = cv2.dilate(m, disk(grow))
    if smooth:
        m = (cv2.GaussianBlur(m.astype(np.float32), (0, 0), smooth * UP) > 0.5).astype(np.uint8)
    return m.astype(bool)

SIMPLIFY = {   # group -> (max hole area to fill, dilation px, slit-close px, smooth px)
    'monogram': (500, 1.5, 2.5, 1.5),  # keep D bowl + M loops, drop bevel slits
    'braid': (40, 0.5, 1.0, 1.0),      # keep the woven-crown structure, drop specks
    'book': (150, 1, 1.5, 1),          # keep main page lines, drop hairline breaks
    'lettering': (120, 0, 3, 1.5),     # counters of A/D survive; bevel nicks close
    'rule': (60, 0, 1.5, 1),
}

out = {}
jobs = []
for g, ids in groups.items():
    m = np.isin(lab, ids)
    jobs.append((g, m))
    jobs.append((g + '_simple', fill_small_holes(m, *SIMPLIFY[g])))

for g, m in jobs:
    bm = potrace.Bitmap(~m)     # potracer treats True as paper, so invert: artwork = ink
    plist = bm.trace(turdsize=6 * UP, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                     alphamax=1.0, opticurve=True, opttolerance=0.25)
    ds = []
    for curve in plist:
        f = lambda p: f'{p.x / UP:.2f},{p.y / UP:.2f}'
        d = [f'M{f(curve.start_point)}']
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f'L{f(seg.c)}L{f(seg.end_point)}')
            else:
                d.append(f'C{f(seg.c1)} {f(seg.c2)} {f(seg.end_point)}')
        d.append('Z')
        ds.append(''.join(d))
    # one compound path per group, even-odd handles holes (page lines, weave)
    out[g] = ' '.join(ds)
    print(g, 'subpaths', len(ds))

json.dump(out, open('work/paths.json', 'w'))
