"""Shared SVG rendering utilities."""

from __future__ import annotations

_SVG_SIG_FIGS = 6


def svg_num(v: float) -> str:
    """Format a float for SVG output, rounded to significant figures.

    Strips floating-point noise (e.g. ``12.000000000000002`` → ``"12"``)
    while preserving all meaningful precision.
    """
    text = f"{v:.{_SVG_SIG_FIGS}g}"
    if "e" in text or "E" in text:
        # Avoid scientific notation in SVG attributes
        return f"{float(text):.{_SVG_SIG_FIGS}f}".rstrip("0").rstrip(".")
    return text



def xml_escape(text: str) -> str:
    """Escape special XML characters for safe embedding in SVG."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def opacity_attr(opacity: float) -> str:
    """Build SVG ``opacity`` attribute string (empty when fully opaque)."""
    if opacity < 1.0:
        return f' opacity="{svg_num(opacity)}"'
    return ""


def fill_stroke_attrs(
    fill: str | None, stroke: str | None, stroke_width: float | None
) -> str:
    """Build SVG fill/stroke attribute string for shape elements."""
    parts: list[str] = []
    if fill:
        parts.append(f' fill="{fill}"')
    else:
        parts.append(' fill="none"')
    if stroke:
        parts.append(f' stroke="{stroke}" stroke-width="{svg_num(stroke_width)}"')
    return "".join(parts)


def stroke_attrs(
    color: str, width: float, svg_cap: str, marker_attrs: str = ""
) -> str:
    """Build SVG stroke attribute string for stroked paths (lines, curves)."""
    return (
        f' stroke="{color}" stroke-width="{svg_num(width)}" '
        f'stroke-linecap="{svg_cap}"{marker_attrs}'
    )


def shape_opacity_attrs(
    opacity: float, fill_opacity: float | None, stroke_opacity: float | None
) -> str:
    """Build SVG fill-opacity/stroke-opacity attribute string for shapes."""
    eff_fill = fill_opacity if fill_opacity is not None else opacity
    eff_stroke = stroke_opacity if stroke_opacity is not None else opacity
    parts: list[str] = []
    if eff_fill < 1.0:
        parts.append(f' fill-opacity="{svg_num(eff_fill)}"')
    if eff_stroke < 1.0:
        parts.append(f' stroke-opacity="{svg_num(eff_stroke)}"')
    return "".join(parts)
