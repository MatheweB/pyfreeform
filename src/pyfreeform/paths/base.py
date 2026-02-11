"""PathShape - Concrete base class for built-in path shapes."""

from __future__ import annotations

import math

from ..core.coord import Coord


class PathShape:
    """Concrete base for built-in path shapes with shared arc_length and SVG rendering.

    Subclasses must implement ``point_at(t)`` and ``angle_at(t)``.
    """

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        raise NotImplementedError

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        raise NotImplementedError

    def arc_length(self, samples: int = 200) -> float:
        """Approximate arc length via polyline sampling."""
        total = 0.0
        prev = self.point_at(0.0)
        for i in range(1, samples + 1):
            curr = self.point_at(i / samples)
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            total += math.sqrt(dx * dx + dy * dy)
            prev = curr
        return total

    def to_svg_path_d(self, segments: int = 64) -> str:
        """SVG path ``d`` attribute using smooth cubic Bezier curves."""
        from ..core.bezier import fit_cubic_beziers

        beziers = fit_cubic_beziers(self, segments, closed=False)
        if not beziers:
            return ""
        p0 = beziers[0][0]
        parts = [f"M {p0.x} {p0.y}"]
        for _, cp1, cp2, p3 in beziers:
            parts.append(f" C {cp1.x} {cp1.y} {cp2.x} {cp2.y} {p3.x} {p3.y}")
        return "".join(parts)
