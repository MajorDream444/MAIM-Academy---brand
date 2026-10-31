# MAIM Academy crest — production package v0.1

**Status: in_review.** Everything under `review/` is a proposed reconstruction for founder review. Nothing here is approved, and nothing should move to `approved/` until Major Dream Williams records approval in `brand/ASSET_REGISTER.csv`.

Prepared 2026-10-31 from the supplied crest `sources/maim-academy_crest_source-metallic_black-bg_1254px_reference.png`.

## What is in the package

| Variant | Vector (SVG) | PNG sizes | Intended use (proposed) |
| --- | --- | --- | --- |
| Metallic presentation | — (raster, see below) | 1168 (native), 1024, 512, 256 | Hero placements, video, social where the full metallic look matters |
| Metallic vector | `crest_metallic-vector` | 2048, 1024, 512, 256 | Large digital use needing scalability; weaker than the presentation PNG |
| Flat colour, full detail | `crest_flat-color` | 2048, 1024, 512, 256 | Print, signage, merchandise, digital at ≥128 px |
| Simplified, flat colour | `crest_simplified_flat-color` | 2048, 1024, 512, 256 | Print at small physical sizes, learning documents |
| One colour (gold / black / white) | `crest_one-color-*` | 2048, 1024, 512, 256 | Foil, emboss, engraving, single-ink print, watermarks |
| Small mark, flat colour | `mark-small_flat-color` | 1024 → 16 | Favicon, app/profile avatars, embroidery base |
| Small mark, one colour | `mark-small_one-color-*` | 1024 → 16 | Single-ink small applications |
| Favicon | — | 16 / 32 / 64 `.ico` | Website favicon |

All PNGs are square with a transparent background. Filenames follow `maim-academy_<variant>_<background>_<size>px_v0.1`.

## Vector and raster audit

Every SVG was scanned for `<image>`, `data:` URIs, `<filter>`, `<pattern>`, `<text>` and font references. **None found.** Each SVG contains only `<circle>` rings and `<path>` elements, grouped as `disk`, `outer-rim`, `green-band`, `inner-rim`, and `artwork` → `book`, `braid`, `monogram`, `lettering`, `rule`.

**Raster that remains:** the metallic presentation PNG is the original artwork with only the background removed (circular alpha with a 2.5 px anti-aliased edge). Its texture, lighting, bevels and highlights are raster and cannot be made vector without a full illustration redraw.

**Approximations in the vectors:**

- Artwork shapes are an automatic trace (potrace) of the gold areas. The metallic bevel shadows become engraved-style slits and nicks in the detailed version. The simplified version closes most of them and smooths edges.
- The metallic look in `crest_metallic-vector` is three linear gradients sampled from the crest. It reads darker and flatter than the original; it is not a faithful conversion.
- The textured black disk is flat MAIM Black #050505.
- Rings are true circles measured from the source (centre 621.9, 607.9; outer rim r 534.5–580, green band r 518–531, inner rim r 502–514).

## Colours

- Flat gold: Crown Gold #D8AF55 (inherited token).
- Black: MAIM Black #050505 (inherited token).
- Green band: #015D1B, the recorded crest-green artwork reference (sampled from the source as #00611C). This remains an artwork colour, not a UI token, per `tokens/README.md`.
- Gradient stops in the metallic vector (#FEF0A0 … #7A561C) are artwork-only and must not become interface tokens.

## Fonts and licences

No fonts are used or required. "ACADEMY" is outlined traced artwork, so no font licence applies. The original typeface is still unidentified; if a matching licensed font is recovered from MAIM 00, the lettering should be rebuilt from it.

## Observations for review (not approved specifications)

- The full crest stops reading below roughly 64 px. The small mark stays legible at 32 px and is recognisable at 16 px.
- The one-colour small mark at 16 px has no fully opaque pixel because its ring is under 1 px wide. Use the flat-colour mark at 16 px, or approve a thicker-ring variant.
- Minimum sizes and clear space are still unresolved in `tokens/README.md`; the points above are evidence for that decision, not the decision.

## Recommended before approval

1. Founder visual review of each variant against the source using `review/maim-academy_logo-comparison-sheet_v0.1.pdf`.
2. Commission a hand redraw (clean Bézier) of the MD monogram and ACADEMY lettering if the engraved-trace edges are not acceptable at large sizes.
3. Embroidery: give the simplified crest or the small mark to an embroidery digitiser; the woven crown and page lines need stitch-specific simplification that a vector file alone does not provide.
4. Keep the metallic presentation PNG as the hero asset; treat the metallic vector as a fallback.

## Related flag

The supplied filament backdrop (`Gold_and_green_filament_backdrop.png`) is a mirrored camera variant — its text reads backwards. Per `templates/README.md` it should be stored and labelled explicitly as mirrored, with a normal-orientation counterpart. It is not part of this logo package.

## Reproducing

`working/trace.py` → `working/build.py` → `working/sheet.py` regenerate everything from the source PNG (Python 3, opencv, potracer, Pillow, rsvg-convert).
