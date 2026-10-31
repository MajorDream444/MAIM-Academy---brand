"""Comparison sheet: source crest beside each proposed reconstruction."""
import os
from PIL import Image, ImageDraw, ImageFont

V = 'v0.1'
PNG = 'out/review/png'
OUT = 'out/review/maim-academy_logo-comparison-sheet_{}.{}'
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans{}.ttf'
font = lambda s, b=False: ImageFont.truetype(F.format('-Bold' if b else ''), s)

BG, PANEL, LIGHT, INK, MUTED, GOLD = '#0E0E0E', '#1A1A1A', '#EFEBE0', '#F2EEE4', '#9A958A', '#D8AF55'
W, M, TILE, GAP = 2400, 70, 500, 30

src = Image.open('work/orig.png').convert('RGB')
cx, cy, R = 621.9, 607.9, 584
src_crop = src.crop((int(cx - R), int(cy - R), int(cx - R) + 2 * R, int(cy - R) + 2 * R))


def png(name, size):
    return Image.open(f'{PNG}/maim-academy_{name}_transparent_{size}px_{V}.png').convert('RGBA')


def tile(img, bg=PANEL, size=TILE):
    t = Image.new('RGB', (size, size), bg)
    im = img.copy()
    im.thumbnail((size - 40, size - 40), Image.LANCZOS)
    t.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im if im.mode == 'RGBA' else None)
    return t


rows = []   # (section title, note, [(image, caption)])

rows.append(('1  Full crest', 'Source raster at left. Vector versions use only circles and traced paths.', [
    (tile(src_crop), 'SOURCE  ·  metallic raster (reference)'),
    (tile(png('crest_metallic-presentation', 1024)), 'Presentation PNG  ·  source, background removed'),
    (tile(png('crest_metallic-vector', 1024)), 'Vector  ·  gradient "metallic"'),
    (tile(png('crest_flat-color', 1024)), 'Vector  ·  flat colour, full detail'),
]))
rows.append(('2  Print / single-colour', 'Simplified geometry: bevel slits closed, edges smoothed. Green band becomes a gap in one-colour.', [
    (tile(png('crest_simplified_flat-color', 1024)), 'Simplified  ·  flat colour'),
    (tile(png('crest_one-color-gold', 1024)), 'One colour  ·  Crown Gold #D8AF55'),
    (tile(png('crest_one-color-black', 1024), LIGHT), 'One colour  ·  black #050505'),
    (tile(png('crest_one-color-white', 1024)), 'One colour  ·  white'),
]))

# small sizes: source downscaled vs crest vs mark, shown at true pixels and 4x
def size_strip(images, label_sizes):
    pad = 24
    cells = []
    for im, s in zip(images, label_sizes):
        big = im.resize((s * 4, s * 4), Image.NEAREST) if s <= 64 else im
        c = Image.new("RGB", (max(big.width, 90) + pad, 400), PANEL)
        c.paste(big, ((c.width - big.width) // 2, 20), big)
        c.paste(im, ((c.width - im.width) // 2, 20 + big.height + 14), im)
        ImageDraw.Draw(c).text((c.width // 2, 388), f'{s}px', fill=MUTED, font=font(18), anchor="ms")
        cells.append(c)
    w = sum(c.width for c in cells) + GAP * (len(cells) - 1)
    out = Image.new("RGB", (w, 400), PANEL)
    x = 0
    for c in cells:
        out.paste(c, (x, 0)); x += c.width + GAP
    return out

src_rgba = src_crop.convert('RGBA')
small = [64, 32, 16]
strip_src = size_strip([src_rgba.resize((s, s), Image.LANCZOS) for s in small], small)
strip_crest = size_strip([Image.open(f'work/prev/c{s}.png').convert('RGBA') for s in small], small)
strip_mark = size_strip([png('mark-small_flat-color', s) for s in small], small)
rows.append(('3  Small sizes', 'Shown 4x enlarged (pixelated) with true size beneath. The full crest fails below ~64px; the small mark is proposed for favicons, avatars and embroidery bases.', [
    (strip_src, 'SOURCE  ·  downscaled'),
    (strip_crest, 'Full crest vector'),
    (strip_mark, 'Small mark  ·  proposed'),
]))

# detail crops at 2x, source vs aligned vector
al_flat = Image.open('work/prev/aligned_maim-academy_crest_flat-color_transparent_v0.1.png').convert('RGB')
al_simp = Image.open('work/prev/aligned_maim-academy_crest_simplified_flat-color_transparent_v0.1.png').convert('RGB')
regions = [((420, 170, 700, 450), 'Monogram'), ((480, 590, 760, 780), 'Woven crown'), ((250, 860, 560, 1015), 'Lettering')]
detail = []
for (x0, y0, x1, y1), name in regions:
    for im, tag, k in ((src, 'source', 1), (al_flat, 'detailed trace', 2), (al_simp, 'simplified', 2)):
        c = im.crop((x0 * k, y0 * k, x1 * k, y1 * k))
        c = c.resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS)   # all shown at 2x
        detail.append((c, f'{name}  ·  {tag}'))

# ---- compose ----
def section_height(items, is_detail=False):
    return 90 + max(im.height for im, _ in items) + 50

blocks = rows
H = M + 170
for title, note, items in blocks:
    H += section_height(items) + 40
det_rows = [detail[i:i + 3] for i in range(0, len(detail), 3)]
H += 90 + sum(max(im.height for im, _ in r) + 70 for r in det_rows) + 230

sheet = Image.new('RGB', (W, H), BG)
d = ImageDraw.Draw(sheet)
d.text((M, M), 'MAIM ACADEMY  ·  Crest production package', fill=GOLD, font=font(46, True))
d.text((M, M + 66), f'Comparison sheet {V}  ·  status: IN REVIEW (not approved)  ·  prepared 2026-10-31 for founder review',
       fill=MUTED, font=font(24))
y = M + 170


def draw_items(items, y):
    x = M
    for im, cap in items:
        sheet.paste(im, (x, y))
        d.text((x, y + im.height + 14), cap, fill=INK, font=font(20))
        x += im.width + GAP
    return y + max(im.height for im, _ in items) + 50


for title, note, items in blocks:
    d.text((M, y), title, fill=INK, font=font(32, True))
    d.text((M, y + 46), note, fill=MUTED, font=font(21))
    y = draw_items(items, y + 90) + 40

d.text((M, y), '4  Detail at source scale', fill=INK, font=font(32, True))
d.text((M, y + 46), 'Auto-trace turns the metallic bevel shadows into engraved-style slits. A hand redraw is needed for final-quality monogram and serif edges.',
       fill=MUTED, font=font(21))
y += 90
for r in det_rows:
    x = M
    for im, cap in r:
        sheet.paste(im, (x, y))
        d.text((x, y + im.height + 12), cap, fill=INK, font=font(20))
        x += im.width + GAP
    y += max(im.height for im, _ in r) + 70

notes = [
    'Raster that remains: the Presentation PNG is the original artwork (texture, lighting, bevels) with only the background removed. No SVG embeds a raster.',
    'Approximations: metallic finish = 3 linear gradients; disk texture = flat MAIM Black; rings = measured circles; artwork = potrace auto-trace.',
    'No fonts used. ACADEMY is traced outlines from the artwork, so no font licence applies and the original typeface is still unidentified.',
    'Crest green #015D1B is the recorded artwork reference (sampled #00611C) and is not a UI token. Flat gold uses Crown Gold #D8AF55.',
]
for n in notes:
    d.text((M, y), '•  ' + n, fill=MUTED, font=font(20)); y += 34

sheet = sheet.crop((0, 0, W, y + M))
sheet.save(OUT.format(V, 'png'), optimize=True)
sheet.convert('RGB').save(OUT.format(V, 'pdf'), resolution=200)
print(sheet.size)
