"""Assemble MAIM Academy crest SVG variants from traced paths (work/paths.json).

All output is pure vector: <circle>/<path> plus linear gradients in the
metallic version. No <image>, no filters, no fonts.
"""
import json, os

P = json.load(open('work/paths.json'))
OUT = 'out/review/vector'
os.makedirs(OUT, exist_ok=True)
V = 'v0.1'

CX, CY = 621.9, 607.9
# tokens (tokens/README.md) + crest artwork reference
CROWN_GOLD = '#D8AF55'
MAIM_BLACK = '#050505'
CREST_GREEN = '#015D1B'      # artwork reference, unresolved as a UI token
WHITE = '#FFFFFF'

# ring geometry measured from source (radius px from fitted centre)
OUTER_RIM = (534.5, 580.0)
GREEN_BAND = (518.0, 531.0)
INNER_RIM = (502.0, 514.0)
DISK_R = 534.5
VB = 584                     # half-size of viewBox

GROUPS = ['book', 'braid', 'monogram', 'lettering', 'rule']


def ring(r0, r1, paint, id_=None):
    rid = f' id="{id_}"' if id_ else ''
    return (f'<circle{rid} cx="0" cy="0" r="{(r0 + r1) / 2:.2f}" fill="none" '
            f'stroke="{paint}" stroke-width="{r1 - r0:.2f}"/>')


def art(paint, simple=False, transform=f'translate({-CX} {-CY})'):
    sfx = '_simple' if simple else ''
    out = [f'<g id="artwork" transform="{transform}" fill="{paint}" fill-rule="evenodd">']
    for g in GROUPS:
        out.append(f'  <path id="{g}" d="{P[g + sfx]}"/>')
    out.append('</g>')
    return '\n'.join(out)


METAL_DEFS = '''<defs>
  <!-- Vector approximation of the metallic finish; artwork colours, not UI tokens -->
  <linearGradient id="gold-face" gradientUnits="userSpaceOnUse" x1="-420" y1="-480" x2="420" y2="480">
    <stop offset="0" stop-color="#FEF0A0"/>
    <stop offset="0.28" stop-color="#EABE58"/>
    <stop offset="0.55" stop-color="#AD802F"/>
    <stop offset="0.78" stop-color="#D9AE4E"/>
    <stop offset="1" stop-color="#835E1F"/>
  </linearGradient>
  <linearGradient id="gold-rim" gradientUnits="userSpaceOnUse" x1="-580" y1="-580" x2="580" y2="580">
    <stop offset="0" stop-color="#FEF7A5"/>
    <stop offset="0.22" stop-color="#C9993E"/>
    <stop offset="0.5" stop-color="#835E1F"/>
    <stop offset="0.74" stop-color="#EABE58"/>
    <stop offset="1" stop-color="#7A561C"/>
  </linearGradient>
  <linearGradient id="gold-rim-inner" gradientUnits="userSpaceOnUse" x1="500" y1="-500" x2="-500" y2="500">
    <stop offset="0" stop-color="#F5D77A"/>
    <stop offset="0.5" stop-color="#9C7229"/>
    <stop offset="1" stop-color="#E5BA55"/>
  </linearGradient>
</defs>'''


def svg(title, body, vb=VB, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-vb} {-vb} {2 * vb} {2 * vb}" '
            f'width="{2 * vb}" height="{2 * vb}">\n<title>{title}</title>\n{defs}\n{body}\n</svg>\n')


def crest(gold, gold_rim, gold_inner, simple, title, defs=''):
    body = '\n'.join([
        f'<circle id="disk" cx="0" cy="0" r="{DISK_R}" fill="{MAIM_BLACK}"/>',
        ring(*OUTER_RIM, gold_rim, 'outer-rim'),
        ring(*GREEN_BAND, CREST_GREEN, 'green-band'),
        ring(*INNER_RIM, gold_inner, 'inner-rim'),
        art(gold, simple),
    ])
    return svg(title, body, defs=defs)


def crest_one_color(paint, title):
    # knockout: disk transparent, green band becomes a gap between two rims
    body = '\n'.join([
        ring(*OUTER_RIM, paint, 'outer-rim'),
        ring(*INNER_RIM, paint, 'inner-rim'),
        art(paint, simple=True),
    ])
    return svg(title, body)


# ---- small-size mark: thick rings + enlarged monogram only ----
MK_VB = 512
MK_OUTER = (452, 512)
MK_GREEN = (420, 452)
MK_DISK = 452
MONO_C = (619.5, 391.5)      # monogram bbox centre in source px
MONO_S = 1.08


def mark(gold, title, one_color=False):
    tf = f'scale({MONO_S}) translate({-MONO_C[0]} {-MONO_C[1]})'
    mono = (f'<g id="artwork" transform="{tf}" fill="{gold}" fill-rule="evenodd">'
            f'<path id="monogram" d="{P["monogram_simple"]}"/></g>')
    if one_color:
        body = ring(*MK_OUTER, gold, 'outer-rim') + '\n' + mono
    else:
        body = '\n'.join([
            f'<circle id="disk" cx="0" cy="0" r="{MK_DISK}" fill="{MAIM_BLACK}"/>',
            ring(*MK_OUTER, gold, 'outer-rim'),
            ring(*MK_GREEN, CREST_GREEN, 'green-band'),
            mono,
        ])
    return svg(title, body, vb=MK_VB)


files = {
    f'maim-academy_crest_metallic-vector_transparent_{V}.svg':
        crest('url(#gold-face)', 'url(#gold-rim)', 'url(#gold-rim-inner)', False,
              'MAIM Academy crest — metallic vector (proposed)', METAL_DEFS),
    f'maim-academy_crest_flat-color_transparent_{V}.svg':
        crest(CROWN_GOLD, CROWN_GOLD, CROWN_GOLD, False,
              'MAIM Academy crest — flat colour, full detail (proposed)'),
    f'maim-academy_crest_simplified_flat-color_transparent_{V}.svg':
        crest(CROWN_GOLD, CROWN_GOLD, CROWN_GOLD, True,
              'MAIM Academy crest — simplified, flat colour (proposed)'),
    f'maim-academy_crest_one-color-gold_transparent_{V}.svg':
        crest_one_color(CROWN_GOLD, 'MAIM Academy crest — one colour, Crown Gold (proposed)'),
    f'maim-academy_crest_one-color-black_transparent_{V}.svg':
        crest_one_color(MAIM_BLACK, 'MAIM Academy crest — one colour, black (proposed)'),
    f'maim-academy_crest_one-color-white_transparent_{V}.svg':
        crest_one_color(WHITE, 'MAIM Academy crest — one colour, white (proposed)'),
    f'maim-academy_mark-small_flat-color_transparent_{V}.svg':
        mark(CROWN_GOLD, 'MAIM Academy small-size mark — flat colour (proposed)'),
    f'maim-academy_mark-small_one-color-gold_transparent_{V}.svg':
        mark(CROWN_GOLD, 'MAIM Academy small-size mark — one colour, gold (proposed)', True),
    f'maim-academy_mark-small_one-color-black_transparent_{V}.svg':
        mark(MAIM_BLACK, 'MAIM Academy small-size mark — one colour, black (proposed)', True),
    f'maim-academy_mark-small_one-color-white_transparent_{V}.svg':
        mark(WHITE, 'MAIM Academy small-size mark — one colour, white (proposed)', True),
}

for name, s in files.items():
    open(os.path.join(OUT, name), 'w').write(s)
    print(f'{len(s) // 1024:5d} KB  {name}')
