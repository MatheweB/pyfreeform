"""Pathable Protocol - Interface for parametric positioning."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from .coord import Coord


@runtime_checkable
class Pathable(Protocol):
    """
    Minimal protocol for parametric positioning.

    Any object implementing `point_at(t)` can be used with `cell.add_dot(along=...)`
    for parametric positioning. This is the only required method — custom path
    objects need only implement this to work with the positioning system.

    Example:
        Built-in pathable types include Line, Curve, and Ellipse:

        ```python
        line = cell.add_line(start="left", end="right")
        cell.add_dot(along=line, t=0.5)  # Dot at line midpoint
        ```

        Create custom paths by implementing point_at():

        ```python
        class Spiral:
            def point_at(self, t: float) -> Coord:
                angle = t * 2 * math.pi * 3  # 3 turns
                radius = t * 20
                return Coord(self.center.x + radius * cos(angle),
                            self.center.y + radius * sin(angle))

        spiral = Spiral(center=cell.center)
        cell.add_dot(along=spiral, t=0.5)  # Works!
        ```
    """

    def point_at(self, t: float) -> Coord:
        """
        Get a point at parameter t along the path.

        Args:
            t:  Parameter from 0.0 (start) to 1.0 (end).
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


@runtime_checkable
class FullPathable(Pathable, Protocol):
    """
    Extended protocol for paths with geometry queries.

    All built-in path entities (Line, Curve, Ellipse, Path) implement this.
    Use ``isinstance(obj, FullPathable)`` instead of ``hasattr`` checks
    for ``angle_at``, ``arc_length``, or ``to_svg_path_d``.
    """

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter *t*."""
        ...

    def arc_length(self) -> float:
        """Approximate arc length in pixels."""
        ...

    def to_svg_path_d(self) -> str:
        """SVG path ``d`` attribute string."""
        ...
