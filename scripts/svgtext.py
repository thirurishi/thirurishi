"""Turn text into SVG paths so the font shows correctly on GitHub (no web fonts needed)."""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

FONT_DIR = Path(__file__).resolve().parent.parent / "assets" / "fonts"
_cache = {}


def _font(weight):
    if weight not in _cache:
        f = TTFont(FONT_DIR / f"Orbitron-{weight}.ttf")
        _cache[weight] = (f, f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm)
    return _cache[weight]


def width(text, size, weight="Bold", spacing=0.0):
    f, gs, cmap, upem = _font(weight)
    s = size / upem
    w = 0
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        w += gs[g].width * s + spacing
    return w - spacing if text else 0


def path(text, size, x=0.0, y=0.0, weight="Bold", spacing=0.0, anchor="start"):
    """Return SVG path data for text. y is the baseline."""
    f, gs, cmap, upem = _font(weight)
    s = size / upem
    if anchor == "middle":
        x -= width(text, size, weight, spacing) / 2
    elif anchor == "end":
        x -= width(text, size, weight, spacing)
    pen = SVGPathPen(gs)
    cx = x
    for ch in text:
        g = cmap.get(ord(ch)) or cmap.get(ord("?"))
        tp = TransformPen(pen, (s, 0, 0, -s, cx, y))
        gs[g].draw(tp)
        cx += gs[g].width * s + spacing
    return pen.getCommands()
