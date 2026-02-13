"""PathShape - Concrete base class for built-in path shapes."""

from __future__ import annotations

from ..core.coord import Coord
from ..core.svg_utils import sample_arc_length


class PathShape:
    """Concrete base for built-in path shapes with shared arc_length and SVG rendering.

    Subclasses must implement ``point_at(t)`` and ``angle_at(t)``.
    Override ``is_closed`` to return ``True`` for shapes where
    ``point_at(0)`` and ``point_at(1)`` coincide (e.g. Lissajous).
    """

    @property
    def is_closed(self) -> bool:
        """Whether point_at(0) and point_at(1) coincide (closed loop)."""
        return False

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        raise NotImplementedError

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        raise NotImplementedError

    def arc_length(self, samples: int = 200) -> float:
        """Approximate arc length via polyline sampling."""
        return sample_arc_length(self.point_at, samples)

    def to_svg_path_d(self, segments: int = 64) -> str:
        """SVG path ``d`` attribute using smooth cubic Bezier curves."""
        from ..core.bezier import fit_cubic_beziers

        beziers = fit_cubic_beziers(self, segments, closed=self.is_closed)
        if not beziers:
            return ""
        p0 = beziers[0][0]
        parts = [f"M {p0.x} {p0.y}"]
        for _, cp1, cp2, p3 in beziers:
            parts.append(f" C {cp1.x} {cp1.y} {cp2.x} {cp2.y} {p3.x} {p3.y}")
        if self.is_closed:
            parts.append(" Z")
        return "".join(parts)
