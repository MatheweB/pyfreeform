"""Lissajous - Lissajous curve path."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike


class Lissajous:
    """
    Lissajous curve: ``x = size * sin(a*t + delta)``, ``y = size * sin(b*t)``.

    A closed curve when ``a/b`` is rational. Common ratios:

    - ``a=3, b=2`` — figure-eight variant
    - ``a=1, b=2`` — parabola-like
    - ``a=5, b=4`` — complex knot

    Examples:
        Standalone closed path::

            liss = Lissajous(center=(200, 200), a=3, b=2, size=80)
            scene.add_path(liss, closed=True, fill="lightblue", color="navy")

        Connection shape::

            liss = Lissajous(a=3, b=2, size=50)
            conn = dot_a.connect(dot_b, shape=Path(liss, end_t=0.99))

        Position dots along curve::

            liss = Lissajous(center=cell.center, size=60)
            cell.add_dot(along=liss, t=cell.brightness, color="coral")
    """

    def __init__(
        self,
        center: CoordLike = (0, 0),
        a: int = 3,
        b: int = 2,
        delta: float = math.pi / 2,
        size: float = 50,
    ) -> None:
        if isinstance(center, tuple):
            center = Coord(*center)
        self.center: Coord = center
        self.a = a
        self.b = b
        self.delta = delta
        self.size = size

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Coord(x, y)

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        angle = t * 2 * math.pi
        dx = self.size * self.a * math.cos(self.a * angle + self.delta) * 2 * math.pi
        dy = self.size * self.b * math.cos(self.b * angle) * 2 * math.pi
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

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
        """SVG path ``d`` attribute using smooth cubic Bézier curves."""
        from ..core.bezier import fit_cubic_beziers

        beziers = fit_cubic_beziers(self, segments, closed=False)
        if not beziers:
            return ""
        p0 = beziers[0][0]
        parts = [f"M {p0.x} {p0.y}"]
        for _, cp1, cp2, p3 in beziers:
            parts.append(f" C {cp1.x} {cp1.y} {cp2.x} {cp2.y} {p3.x} {p3.y}")
        return "".join(parts)

    def __repr__(self) -> str:
        return (
            f"Lissajous(center={self.center}, a={self.a}, b={self.b}, "
            f"delta={self.delta:.4f}, size={self.size})"
        )
