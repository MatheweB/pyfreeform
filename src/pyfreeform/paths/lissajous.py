"""Lissajous - Lissajous curve path."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike
from .base import PathShape


class Lissajous(PathShape):
    """
    Lissajous curve: ``x = size * sin(a*t + delta)``, ``y = size * sin(b*t)``.

    A closed curve (``is_closed = True``) when ``a/b`` is rational.
    Common ratios:

    - ``a=3, b=2`` — figure-eight variant
    - ``a=1, b=2`` — parabola-like
    - ``a=5, b=4`` — complex knot

    Because this is a closed loop, using it directly as a connection shape
    will raise ``ValueError``. Use ``start_t``/``end_t`` to take an arc::

        arc = Path(Lissajous(), start_t=0, end_t=0.5)
        dot_a.connect(dot_b, path=arc)

    Example:
        Standalone closed path::

            liss = Lissajous(center=(200, 200), a=3, b=2, size=80)
            scene.add_path(liss, closed=True, fill="lightblue", color="navy")

        Connection via arc::

            liss = Lissajous(a=3, b=2, size=50)
            conn = dot_a.connect(dot_b, path=Path(liss, start_t=0, end_t=0.5))

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
        self.center = Coord.coerce(center)
        self.a = a
        self.b = b
        self.delta = delta
        self.size = size

    @property
    def is_closed(self) -> bool:
        """Lissajous curves are closed loops."""
        return True

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

    def __repr__(self) -> str:
        return (
            f"Lissajous(center={self.center}, a={self.a}, b={self.b}, "
            f"delta={self.delta:.4f}, size={self.size})"
        )
