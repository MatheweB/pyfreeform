"""Shared SVG rendering utilities."""

from __future__ import annotations

import math
from collections.abc import Callable

from .coord import Coord


def shape_opacity_attrs(
    opacity: float, fill_opacity: float | None, stroke_opacity: float | None
) -> str:
    """Build SVG fill-opacity/stroke-opacity attribute string for shapes."""
    eff_fill = fill_opacity if fill_opacity is not None else opacity
    eff_stroke = stroke_opacity if stroke_opacity is not None else opacity
    parts: list[str] = []
    if eff_fill < 1.0:
        parts.append(f' fill-opacity="{eff_fill}"')
    if eff_stroke < 1.0:
        parts.append(f' stroke-opacity="{eff_stroke}"')
    return "".join(parts)


def sample_arc_length(
    point_at_fn: Callable[[float], Coord], samples: int = 200
) -> float:
    """Approximate arc length by summing chord lengths over point_at samples."""
    total = 0.0
    prev = point_at_fn(0.0)
    for i in range(1, samples + 1):
        curr = point_at_fn(i / samples)
        dx = curr.x - prev.x
        dy = curr.y - prev.y
        total += math.sqrt(dx * dx + dy * dy)
        prev = curr
    return total
