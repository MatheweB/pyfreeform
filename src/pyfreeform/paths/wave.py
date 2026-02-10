"""Wave - Sinusoidal wave path between two points."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike


class Wave:
    """
    Sinusoidal wave between two points.

    Generates a sine oscillation along the Y-axis relative to the
    baseline from ``start`` to ``end``.

    When ``start`` and ``end`` are omitted, defaults to normalized
    ``(0, 0) -> (1, 0)`` space — ideal for connection shapes.

    Examples:
        Standalone path::

            wave = Wave(start=(50, 100), end=(550, 100), amplitude=40, frequency=4)
            scene.add_path(wave, width=2, color="blue")

        Connection shape::

            wave = Wave(amplitude=0.15, frequency=3)
            conn = dot_a.connect(dot_b, shape=Path(wave), style=style)

        In a cell::

            wave = Wave(start=cell.top_left, end=cell.bottom_right, amplitude=5)
            cell.add_path(wave, width=1, color="red")
    """

    def __init__(
        self,
        start: CoordLike = (0, 0),
        end: CoordLike = (1, 0),
        amplitude: float = 0.15,
        frequency: float = 2,
    ) -> None:
        if isinstance(start, tuple):
            start = Coord(*start)
        if isinstance(end, tuple):
            end = Coord(*end)
        self.start: Coord = start
        self.end: Coord = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        y = base_y + self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        return Coord(x, y)

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        dx = self.end.x - self.start.x
        base_dy = self.end.y - self.start.y
        wave_dy = (
            self.amplitude
            * self.frequency
            * 2
            * math.pi
            * math.cos(t * self.frequency * 2 * math.pi)
        )
        if dx == 0 and (base_dy + wave_dy) == 0:
            return 0.0
        return math.degrees(math.atan2(base_dy + wave_dy, dx))

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
            f"Wave(start={self.start}, end={self.end}, "
            f"amplitude={self.amplitude}, frequency={self.frequency})"
        )
