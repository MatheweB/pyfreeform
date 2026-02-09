"""Pathable Protocol - Interface for parametric positioning."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from .coord import Coord


@runtime_checkable
class Pathable(Protocol):
    """
    Protocol for objects that support parametric positioning.

    Any object implementing `point_at(t)` can be used with `cell.add_dot(along=...)`
    for parametric positioning. This enables a unified interface for positioning
    entities along lines, curves, ellipses, and custom paths.

    The protocol is runtime-checkable, meaning you can use `isinstance(obj, Pathable)`
    to verify that an object implements the required method.

    Examples:
        Built-in pathable types include Line, Curve, and Ellipse:

        >>> line = cell.add_line(start="left", end="right")
        >>> cell.add_dot(along=line, t=0.5)  # Dot at line midpoint

        >>> curve = cell.add_curve(curvature=0.5)
        >>> cell.add_dot(along=curve, t=cell.brightness)  # Dot slides along curve

        >>> ellipse = cell.add_ellipse(rx=0.3, ry=0.2)
        >>> cell.add_dot(along=ellipse, t=0.25)  # Dot at top of ellipse

        Create custom paths by implementing point_at():

        >>> class Spiral:
        ...     def point_at(self, t: float) -> Coord:
        ...         angle = t * 2 * math.pi * 3  # 3 turns
        ...         radius = t * 20
        ...         return Coord(self.center.x + radius * cos(angle),
        ...                     self.center.y + radius * sin(angle))
        >>>
        >>> spiral = Spiral(center=cell.center)
        >>> cell.add_dot(along=spiral, t=0.5)  # Works!
    """

    def point_at(self, t: float) -> Coord:
        """
        Get a point at parameter t along the path.

        Args:
            t: Parameter from 0.0 (start) to 1.0 (end).
               For closed paths like ellipses, t=0 and t=1 are the same point.
               Values outside 0-1 may extrapolate or wrap depending on implementation.

        Returns:
            Coord at position t along the path.

        Note:
            The interpretation of t is path-specific:
            - Lines: Linear interpolation from start to end
            - Curves: Bézier parametric position
            - Ellipses: Parametric angle (t=0 at 0°, t=0.5 at 180°)
            - Custom paths: Any parametric function you define
        """
        ...
