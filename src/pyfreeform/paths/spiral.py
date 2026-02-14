"""Spiral - Archimedean spiral path."""

from __future__ import annotations

import math

from ..core.coord import Coord, CoordLike
from .base import PathShape


class Spiral(PathShape):
    """
    Archimedean spiral expanding outward from center.

    The spiral makes ``turns`` revolutions while the radius grows
    linearly from ``start_radius`` to ``end_radius``.

    Example:
        Standalone path::

            spiral = Spiral(center=(200, 200), end_radius=80, turns=4)
            scene.add_path(spiral, width=1.5, color="coral")

        In a cell::

            spiral = Spiral(center=cell.center, end_radius=40, turns=3)
            cell.add_dot(along=spiral, t=cell.brightness, color="coral")

        Closed path with fill::

            spiral = Spiral(center=(200, 200), end_radius=60, turns=5)
            scene.add_path(spiral, closed=True, fill="lightblue", color="navy")
    """

    def __init__(
        self,
        center: CoordLike = (0, 0),
        start_radius: float = 0,
        end_radius: float = 50,
        turns: float = 3,
    ) -> None:
        self.center = Coord.coerce(center)
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.turns = turns

    def point_at(self, t: float) -> Coord:
        """Get point at parameter *t* (0.0 to 1.0)."""
        angle = t * self.turns * 2 * math.pi
        radius = self.start_radius + (self.end_radius - self.start_radius) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Coord(x, y)

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        angle = t * self.turns * 2 * math.pi
        omega = self.turns * 2 * math.pi
        radius = self.start_radius + (self.end_radius - self.start_radius) * t
        dr = self.end_radius - self.start_radius

        # dx/dt and dy/dt via product rule
        dx = dr * math.cos(angle) - radius * omega * math.sin(angle)
        dy = dr * math.sin(angle) + radius * omega * math.cos(angle)
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def __repr__(self) -> str:
        return (
            f"Spiral(center={self.center}, start_radius={self.start_radius}, "
            f"end_radius={self.end_radius}, turns={self.turns})"
        )
