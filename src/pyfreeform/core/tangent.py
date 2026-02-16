"""Tangent angle utilities for Pathable objects."""

from __future__ import annotations

import math

from .coord import Coord
from .pathable import FullPathable, Pathable


def get_angle_at(path: Pathable, t: float, epsilon: float = 1e-5) -> float:
    """
    Get tangent angle in degrees at parameter t along a path.

    If path implements ``FullPathable``, uses ``angle_at()`` directly.
    Otherwise falls back to numeric differentiation.

    Args:
        path: Any Pathable object.
        t: Parameter from 0.0 to 1.0.
        epsilon: Step size for numeric differentiation.

    Returns:
        Angle in degrees (0 = rightward, 90 = downward in SVG coords).
    """
    if isinstance(path, FullPathable):
        return path.angle_at(t)

    # Numeric differentiation fallback
    t0 = max(0.0, t - epsilon)
    t1 = min(1.0, t + epsilon)
    if t0 == t1:
        return 0.0

    p0 = path.point_at(t0)
    p1 = path.point_at(t1)
    dx = p1.x - p0.x
    dy = p1.y - p0.y

    if dx == 0 and dy == 0:
        return 0.0

    return math.degrees(math.atan2(dy, dx))


def perpendicular_shift(
    position: Coord,
    tangent_degrees: float,
    amount: float,
) -> Coord:
    """Shift a position perpendicular to a path. Negative = above.

    Direction-independent: the result is the same regardless of whether
    the path travels left-to-right or right-to-left.

    The perpendicular normal to tangent angle *a* is ``(-sin a, cos a)``.
    If the tangent points leftward (``cos a < 0``), the normal is flipped
    so that negative *amount* always means "above" (toward smaller *y*).
    """
    rad = math.radians(tangent_degrees)
    s, c = math.sin(rad), math.cos(rad)
    sign = 1 if c >= 0 else -1
    return Coord(
        position.x - amount * abs(s) * sign,
        position.y + amount * abs(c),
    )
