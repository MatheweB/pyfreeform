"""Zigzag - Triangle wave path between two points."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike
from .base import PathShape


class Zigzag(PathShape):
    """
    Triangle wave (zigzag) between two points.

    Generates a zigzag pattern along the Y-axis relative to the
    baseline from ``start`` to ``end``.

    When ``start`` and ``end`` are omitted, defaults to normalized
    ``(0, 0) -> (1, 0)`` space — ideal for connection shapes.

    Example:
        Standalone path::

            zz = Zigzag(start=(50, 100), end=(550, 100), teeth=8, amplitude=20)
            scene.add_path(zz, width=2, color="orange")

        Connection path::

            zz = Zigzag(teeth=6, amplitude=0.12)
            conn = dot_a.connect(dot_b, path=Path(zz), style=style)
    """

    def __init__(
        self,
        start: CoordLike = (0, 0),
        end: CoordLike = (1, 0),
        teeth: int = 5,
        amplitude: float = 0.12,
    ) -> None:
        self.start = Coord.coerce(start)
        self.end = Coord.coerce(end)
        self.teeth = teeth
        self.amplitude = amplitude

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t

        # Triangle wave
        phase = t * self.teeth * 2
        frac = phase - int(phase)
        if int(phase) % 2 == 0:
            y_offset = self.amplitude * (2 * frac - 1)
        else:
            y_offset = self.amplitude * (1 - 2 * frac)

        return Coord(x, base_y + y_offset)

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        dx = self.end.x - self.start.x
        base_dy = self.end.y - self.start.y

        # Triangle wave derivative: constant slope, alternating sign
        phase = t * self.teeth * 2
        slope = self.amplitude * 2 * self.teeth * 2
        wave_dy = slope if int(phase) % 2 == 0 else -slope

        if dx == 0 and (base_dy + wave_dy) == 0:
            return 0.0
        return math.degrees(math.atan2(base_dy + wave_dy, dx))

    def __repr__(self) -> str:
        return (
            f"Zigzag(start={self.start}, end={self.end}, "
            f"teeth={self.teeth}, amplitude={self.amplitude})"
        )
