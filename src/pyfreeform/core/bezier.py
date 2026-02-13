"""Parametric curve utilities.

Includes arc-length sampling, Bézier fitting (Hermite interpolation
with C1 continuity), curvature helpers, and degree elevation.

Used by the Path entity, Curve entity, Ellipse, and shaped Connections.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import TYPE_CHECKING

from .coord import Coord

if TYPE_CHECKING:
    from .pathable import Pathable


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


def tangent_at(
    pathable: Pathable, t: float, closed: bool, epsilon: float = 1e-5
) -> tuple[float, float]:
    """Compute the tangent vector (dx/dt, dy/dt) via numerical differentiation."""
    if closed:
        # For closed paths, wrap around instead of clamping
        t0 = (t - epsilon) % 1.0
        t1 = (t + epsilon) % 1.0
        p0 = pathable.point_at(t0)
        p1 = pathable.point_at(t1)
        dt = 2 * epsilon
    else:
        t0 = max(0.0, t - epsilon)
        t1 = min(1.0, t + epsilon)
        p0 = pathable.point_at(t0)
        p1 = pathable.point_at(t1)
        dt = t1 - t0

    if dt == 0:
        return (0.0, 0.0)
    return ((p1.x - p0.x) / dt, (p1.y - p0.y) / dt)


def fit_cubic_beziers(
    pathable: Pathable,
    segments: int,
    closed: bool,
    start_t: float = 0.0,
    end_t: float = 1.0,
) -> list[tuple[Coord, Coord, Coord, Coord]]:
    """
    Fit cubic Bézier segments to a Pathable using Hermite interpolation.

    For each segment, the tangent at each endpoint is used to compute
    control points, giving C1 continuity at every joint.

    Args:
        pathable: The source path.
        segments: Number of Bézier segments.
        closed: Whether to close the path smoothly.
        start_t: Start parameter on the pathable (0.0-1.0).
        end_t: End parameter on the pathable (0.0-1.0).

    Returns:
        List of (p0, cp1, cp2, p3) tuples.
    """
    if segments < 1:
        segments = 1

    t_span = end_t - start_t

    if closed and start_t == 0.0 and end_t == 1.0:
        # Full closed path: sample N points, wrap last segment
        n = segments
        t_values = [i / n for i in range(n)]
        points = [pathable.point_at(t) for t in t_values]
        tangents = [tangent_at(pathable, t, closed=True) for t in t_values]

        result = []
        for i in range(n):
            j = (i + 1) % n
            dt = 1.0 / n

            p0 = points[i]
            p3 = points[j]
            tx0, ty0 = tangents[i]
            tx3, ty3 = tangents[j]

            # Hermite-to-Bézier: scale tangent by dt/3
            cp1 = Coord(p0.x + tx0 * dt / 3, p0.y + ty0 * dt / 3)
            cp2 = Coord(p3.x - tx3 * dt / 3, p3.y - ty3 * dt / 3)
            cp1, cp2 = clamp_control_points(p0, cp1, cp2, p3)
            result.append((p0, cp1, cp2, p3))

        return result

    # Open path (or sub-range of a closed path)
    n = segments
    t_values = [start_t + (i / n) * t_span for i in range(n + 1)]
    points = [pathable.point_at(t) for t in t_values]
    tangents = [tangent_at(pathable, t, closed=False) for t in t_values]

    result = []
    for i in range(n):
        dt = t_span / n

        p0 = points[i]
        p3 = points[i + 1]
        tx0, ty0 = tangents[i]
        tx3, ty3 = tangents[i + 1]

        cp1 = Coord(p0.x + tx0 * dt / 3, p0.y + ty0 * dt / 3)
        cp2 = Coord(p3.x - tx3 * dt / 3, p3.y - ty3 * dt / 3)
        cp1, cp2 = clamp_control_points(p0, cp1, cp2, p3)
        result.append((p0, cp1, cp2, p3))

    return result


def clamp_control_points(
    p0: Coord,
    cp1: Coord,
    cp2: Coord,
    p3: Coord,
    max_ratio: float = 0.75,
) -> tuple[Coord, Coord]:
    """
    Clamp control point offsets to a fraction of the chord length.

    For well-behaved curves the offset is ~chord/3, so 0.75 is generous.
    This prevents pathological blowup when the parametric tangent is
    near-infinite (e.g. superellipse corners with n > 2).
    """
    chord_sq = (p3.x - p0.x) ** 2 + (p3.y - p0.y) ** 2
    if chord_sq == 0:
        return cp1, cp2
    max_dist_sq = chord_sq * max_ratio * max_ratio

    # Clamp cp1 distance from p0
    dx1, dy1 = cp1.x - p0.x, cp1.y - p0.y
    d1_sq = dx1 * dx1 + dy1 * dy1
    if d1_sq > max_dist_sq and d1_sq > 0:
        s = math.sqrt(max_dist_sq / d1_sq)
        cp1 = Coord(p0.x + dx1 * s, p0.y + dy1 * s)

    # Clamp cp2 distance from p3
    dx2, dy2 = cp2.x - p3.x, cp2.y - p3.y
    d2_sq = dx2 * dx2 + dy2 * dy2
    if d2_sq > max_dist_sq and d2_sq > 0:
        s = math.sqrt(max_dist_sq / d2_sq)
        cp2 = Coord(p3.x + dx2 * s, p3.y + dy2 * s)

    return cp1, cp2


def curvature_control_point(
    start: Coord, end: Coord, curvature: float
) -> Coord:
    """
    Compute a quadratic Bézier control point from a curvature value.

    The control point sits at the midpoint of *start*→*end*, offset
    perpendicularly by ``curvature × half_chord_length``.

    Args:
        start: Start of the chord.
        end: End of the chord.
        curvature: How much the curve bows (-1 to 1 typical).
                   Positive = left (counterclockwise), negative = right.

    Returns:
        The quadratic Bézier control point.
    """
    mid_x = (start.x + end.x) / 2
    mid_y = (start.y + end.y) / 2

    if curvature == 0:
        return Coord(mid_x, mid_y)

    dx = end.x - start.x
    dy = end.y - start.y
    length = math.hypot(dx, dy)

    if length == 0:
        return Coord(mid_x, mid_y)

    perp_x = -dy / length
    perp_y = dx / length
    offset = curvature * length * 0.5

    return Coord(mid_x + perp_x * offset, mid_y + perp_y * offset)


def quadratic_to_cubic(
    p0: Coord, control: Coord, p2: Coord
) -> tuple[Coord, Coord, Coord, Coord]:
    """
    Exact degree elevation: quadratic Bézier → cubic Bézier.

    Args:
        p0: Start point.
        control: Quadratic control point.
        p2: End point.

    Returns:
        (P0, CP1, CP2, P2) cubic Bézier tuple.
    """
    cp1 = Coord(
        p0.x + 2 / 3 * (control.x - p0.x),
        p0.y + 2 / 3 * (control.y - p0.y),
    )
    cp2 = Coord(
        p2.x + 2 / 3 * (control.x - p2.x),
        p2.y + 2 / 3 * (control.y - p2.y),
    )
    return (p0, cp1, cp2, p2)


def eval_cubic(p0: Coord, cp1: Coord, cp2: Coord, p3: Coord, t: float) -> Coord:
    """Evaluate a cubic Bézier at parameter t."""
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    t2 = t * t
    t3 = t2 * t

    x = mt3 * p0.x + 3 * mt2 * t * cp1.x + 3 * mt * t2 * cp2.x + t3 * p3.x
    y = mt3 * p0.y + 3 * mt2 * t * cp1.y + 3 * mt * t2 * cp2.y + t3 * p3.y
    return Coord(x, y)


def eval_cubic_derivative(
    p0: Coord, cp1: Coord, cp2: Coord, p3: Coord, t: float
) -> tuple[float, float]:
    """Evaluate the derivative of a cubic Bézier at parameter t."""
    mt = 1 - t
    mt2 = mt * mt
    t2 = t * t

    # B'(t) = 3(1-t)²(P1-P0) + 6(1-t)t(P2-P1) + 3t²(P3-P2)
    dx = 3 * mt2 * (cp1.x - p0.x) + 6 * mt * t * (cp2.x - cp1.x) + 3 * t2 * (p3.x - cp2.x)
    dy = 3 * mt2 * (cp1.y - p0.y) + 6 * mt * t * (cp2.y - cp1.y) + 3 * t2 * (p3.y - cp2.y)
    return (dx, dy)
