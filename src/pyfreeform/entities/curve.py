"""Curve - A quadratic Bezier curve entity."""

from __future__ import annotations

import math
from ..color import Color
from ..config.caps import DEFAULT_ARROW_SCALE, get_marker, is_marker_cap
from ..core.entity import Entity
from ..core.point import Point


class Curve(Entity):
    """
    A quadratic Bezier curve between two points.

    Curves add organic, flowing shapes to your art. The `curvature` parameter
    controls how much the curve bows away from a straight line.

    The key feature: use `point_at(t)` to position other elements along the curve,
    just like with lines!

    Attributes:
        start: Starting point
        end: Ending point
        curvature: How much the curve bows (-1 to 1, 0 = straight)
        control: The Bezier control point (calculated from curvature)

    Anchors:
        - "start": The starting point
        - "center": The midpoint of the curve (at t=0.5)
        - "end": The ending point
        - "control": The control point

    Examples:
        >>> curve = Curve(0, 100, 100, 0, curvature=0.5)
        >>> midpoint = curve.point_at(0.5)  # Point on the curve

        >>> # In a cell:
        >>> curve = cell.add_curve(start="bottom_left", end="top_right", curvature=0.3)
        >>> cell.add_dot(along=curve, t=cell.brightness)

        >>> # With arrow cap:
        >>> curve = Curve(0, 100, 100, 0, curvature=0.5, end_cap="arrow")
    """

    DEFAULT_WIDTH = 1
    DEFAULT_COLOR = "black"
    DEFAULT_CAP = "round"

    def __init__(
        self,
        x1: float = 0,
        y1: float = 0,
        x2: float = 0,
        y2: float = 0,
        curvature: float = 0.5,
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        cap: str = DEFAULT_CAP,
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
    ) -> None:
        """
        Create a curve from (x1, y1) to (x2, y2).

        Args:
            x1, y1: Starting point coordinates.
            x2, y2: Ending point coordinates.
            curvature: How much the curve bows away from straight.
                       0 = straight line
                       Positive = bows to the left (when facing end)
                       Negative = bows to the right
                       Typical range: -1 to 1
            width: Stroke width in pixels.
            color: Stroke color.
            z_index: Layer ordering (higher = on top).
            cap: Cap style for both ends ("round", "square", "butt", or "arrow").
            start_cap: Override cap for start end only.
            end_cap: Override cap for end end only.
            opacity: Opacity (0.0 transparent to 1.0 opaque).
        """
        super().__init__(x1, y1, z_index)
        self._end = Point(x2, y2)
        self._curvature = float(curvature)
        self.width = float(width)
        self._color = Color(color)
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)
        self._control: Point | None = None  # Calculated lazily

    @classmethod
    def from_points(
        cls,
        start: Point | tuple[float, float],
        end: Point | tuple[float, float],
        curvature: float = 0.5,
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        cap: str = DEFAULT_CAP,
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
    ) -> Curve:
        """Create a curve from two points."""
        if isinstance(start, tuple):
            start = Point(*start)
        if isinstance(end, tuple):
            end = Point(*end)
        return cls(start.x, start.y, end.x, end.y, curvature, width, color, z_index,
                   cap, start_cap, end_cap, opacity)

    @property
    def start(self) -> Point:
        """The starting point."""
        return self.position

    @property
    def end(self) -> Point:
        """The ending point."""
        return self._end

    @end.setter
    def end(self, value: Point | tuple[float, float]) -> None:
        if isinstance(value, tuple):
            value = Point(*value)
        self._end = value
        self._control = None  # Invalidate cached control point

    @property
    def curvature(self) -> float:
        """The curvature amount."""
        return self._curvature

    @curvature.setter
    def curvature(self, value: float) -> None:
        self._curvature = float(value)
        self._control = None  # Invalidate cached control point

    @property
    def control(self) -> Point:
        """
        The Bezier control point.

        Calculated from curvature: perpendicular to the line at its midpoint,
        offset by curvature * half the line length.
        """
        if self._control is None:
            self._control = self._calculate_control()
        return self._control

    def _calculate_control(self) -> Point:
        """Calculate control point from curvature."""
        # Midpoint of the line
        mid = self.start.midpoint(self.end)

        if self._curvature == 0:
            return mid

        # Vector from start to end
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        length = math.sqrt(dx * dx + dy * dy)

        if length == 0:
            return mid

        # Perpendicular vector (rotated 90 degrees counterclockwise)
        perp_x = -dy / length
        perp_y = dx / length

        # Offset by curvature * half the length
        offset = self._curvature * length * 0.5

        return Point(mid.x + perp_x * offset, mid.y + perp_y * offset)

    @property
    def color(self) -> str:
        """The stroke color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return self.start_cap if self.start_cap is not None else self.cap

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return self.end_cap if self.end_cap is not None else self.cap

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors."""
        return ["start", "center", "end", "control"]

    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "start":
            return self.start
        elif name == "center":
            return self.point_at(0.5)
        elif name == "end":
            return self.end
        elif name == "control":
            return self.control
        raise ValueError(f"Curve has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Point:
        """
        Get a point along the curve.

        This is the key method for positioning elements along curves!

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Point on the curve at parameter t.

        Example:
            >>> curve = cell.add_curve(curvature=0.5)
            >>> cell.add_dot(along=curve, t=0.5)  # Dot at curve midpoint
        """
        # Quadratic Bezier formula: B(t) = (1-t)^2 P0 + 2(1-t)t P1 + t^2 P2
        p0 = self.start
        p1 = self.control
        p2 = self.end

        mt = 1 - t  # (1 - t)
        mt2 = mt * mt  # (1 - t)^2
        t2 = t * t  # t^2

        x = mt2 * p0.x + 2 * mt * t * p1.x + t2 * p2.x
        y = mt2 * p0.y + 2 * mt * t * p1.y + t2 * p2.y

        return Point(x, y)

    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box (approximate - includes control point)."""
        points = [self.start, self.control, self.end]
        min_x = min(p.x for p in points)
        min_y = min(p.y for p in points)
        max_x = max(p.x for p in points)
        max_y = max(p.y for p in points)
        return (min_x, min_y, max_x, max_y)

    def get_required_markers(self) -> list[tuple[str, str]]:
        """
        Collect SVG marker definitions needed by this curve's caps.

        Returns:
            List of (marker_id, marker_svg) tuples.
        """
        markers: list[tuple[str, str]] = []
        size = self.width * DEFAULT_ARROW_SCALE
        for cap_name in (self.effective_start_cap, self.effective_end_cap):
            result = get_marker(cap_name, self.color, size)
            if result is not None:
                markers.append(result)
        return markers

    def to_svg(self) -> str:
        """Render to SVG path element (quadratic Bezier)."""
        s = self.start
        c = self.control
        e = self.end
        sc = self.effective_start_cap
        ec = self.effective_end_cap
        has_marker_start = is_marker_cap(sc)
        has_marker_end = is_marker_cap(ec)

        # Use "butt" linecap when markers are present
        if has_marker_start or has_marker_end:
            svg_cap = "butt"
        else:
            svg_cap = self.cap

        parts = [
            f'<path d="M {s.x} {s.y} Q {c.x} {c.y} {e.x} {e.y}" '
            f'fill="none" stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}"'
        ]

        size = self.width * DEFAULT_ARROW_SCALE
        if has_marker_start:
            from ..config.caps import make_marker_id
            mid = make_marker_id(sc, self.color, size)
            parts.append(f' marker-start="url(#{mid})"')
        if has_marker_end:
            from ..config.caps import make_marker_id
            mid = make_marker_id(ec, self.color, size)
            parts.append(f' marker-end="url(#{mid})"')

        if self.opacity < 1.0:
            parts.append(f' opacity="{self.opacity}"')

        parts.append(" />")
        return "".join(parts)

    def __repr__(self) -> str:
        return (
            f"Curve(({self.start.x}, {self.start.y}) -> ({self.end.x}, {self.end.y}), "
            f"curvature={self._curvature}, color={self.color!r})"
        )
