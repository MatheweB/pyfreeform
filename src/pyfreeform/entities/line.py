"""Line - A line segment entity between two points."""

from __future__ import annotations

from ..color import Color
from ..core.entity import Entity
from ..core.point import Point
from ..core.stroked_path_mixin import StrokedPathMixin


class Line(StrokedPathMixin, Entity):
    """
    A line segment between two points.

    Unlike connections (which link entities), a Line is a standalone
    entity with its own start and end points. Lines can be placed
    in cells and have other entities positioned along them.

    Attributes:
        position: The start point of the line
        end_offset: Offset from position to end point
        width: Stroke width
        color: Stroke color

    Anchors:
        - "start": The starting point
        - "center": The midpoint
        - "end": The ending point

    Examples:
        >>> line = Line(0, 0, 100, 100)  # From (0,0) to (100,100)
        >>> line = Line.from_points(Point(0, 0), Point(100, 100))
        >>> midpoint = line.anchor("center")
        >>> line = Line(0, 0, 100, 0, end_cap="arrow")  # Arrow at end
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
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        cap: str = DEFAULT_CAP,
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
    ) -> None:
        """
        Create a line from (x1, y1) to (x2, y2).

        Args:
            x1, y1: Starting point coordinates.
            x2, y2: Ending point coordinates.
            width: Stroke width in pixels.
            color: Stroke color (name, hex, or RGB tuple).
            z_index: Layer ordering (higher = on top).
            cap: Cap style for both ends ("round", "square", "butt", or "arrow").
            start_cap: Override cap for start end only.
            end_cap: Override cap for end end only.
            opacity: Opacity (0.0 transparent to 1.0 opaque).
        """
        super().__init__(x1, y1, z_index)
        self._end_offset = Point(x2 - x1, y2 - y1)
        self.width = float(width)
        self._color = Color(color)
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)

    @classmethod
    def from_points(
        cls,
        start: Point | tuple[float, float],
        end: Point | tuple[float, float],
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        cap: str = DEFAULT_CAP,
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
    ) -> Line:
        """
        Create a line from two points.

        Args:
            start: Starting point.
            end: Ending point.
            width: Stroke width.
            color: Stroke color.
            z_index: Layer ordering (higher = on top).
            cap: Cap style for both ends.
            start_cap: Override cap for start end only.
            end_cap: Override cap for end end only.
            opacity: Opacity (0.0 transparent to 1.0 opaque).

        Returns:
            A new Line entity.
        """
        if isinstance(start, tuple):
            start = Point(*start)
        if isinstance(end, tuple):
            end = Point(*end)
        return cls(start.x, start.y, end.x, end.y, width, color, z_index, cap,
                   start_cap, end_cap, opacity)

    @property
    def start(self) -> Point:
        """The starting point (same as position)."""
        return self.position

    @property
    def end(self) -> Point:
        """The ending point."""
        return self.position + self._end_offset

    @end.setter
    def end(self, value: Point | tuple[float, float]) -> None:
        """Set the ending point."""
        if isinstance(value, tuple):
            value = Point(*value)
        self._end_offset = value - self.position

    @property
    def color(self) -> str:
        """The stroke color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def length(self) -> float:
        """Length of the line."""
        return self.start.distance_to(self.end)

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: start, center, end."""
        return ["start", "center", "end"]

    def anchor(self, name: str = "center") -> Point:
        """Get anchor point by name."""
        if name == "start":
            return self.start
        elif name == "center":
            return self.start.midpoint(self.end)
        elif name == "end":
            return self.end
        raise ValueError(f"Line has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Point:
        """
        Get a point along the line.

        Args:
            t: Parameter from 0 (start) to 1 (end).
               Values outside 0-1 extrapolate beyond the line.

        Returns:
            Point at that position along the line.
        """
        return self.start.lerp(self.end, t)

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t.

        For a line, the angle is constant (same at every point).

        Args:
            t: Parameter (unused — angle is constant for lines).

        Returns:
            Angle in degrees.
        """
        import math

        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this line."""
        s, e = self.start, self.end
        return f"M {s.x} {s.y} L {e.x} {e.y}"

    def move_to(self, x: float | Point, y: float | None = None) -> Line:
        """
        Move the line's start point to a new position.

        The end point moves to maintain the same relative offset.

        Args:
            x: X coordinate, or a Point.
            y: Y coordinate (required if x is not a Point).

        Returns:
            self, for method chaining.
        """
        # Call parent implementation
        super().move_to(x, y)
        return self

    def set_endpoints(
        self,
        start: Point | tuple[float, float],
        end: Point | tuple[float, float],
    ) -> Line:
        """
        Set both endpoints of the line.

        Args:
            start: New starting point.
            end: New ending point.

        Returns:
            self, for method chaining.
        """
        if isinstance(start, tuple):
            start = Point(*start)
        if isinstance(end, tuple):
            end = Point(*end)

        self._position = start
        self._end_offset = end - start
        return self

    def rotate(self, angle: float, origin: Point | tuple[float, float] | None = None) -> Line:
        """
        Rotate the line around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: line center).

        Returns:
            self, for method chaining.
        """
        import math

        if origin is None:
            origin = self.anchor("center")
        elif isinstance(origin, tuple):
            origin = Point(*origin)

        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Rotate both endpoints
        start = self.start
        end = self.end

        def rotate_point(p: Point) -> Point:
            dx = p.x - origin.x
            dy = p.y - origin.y
            return Point(
                dx * cos_a - dy * sin_a + origin.x,
                dx * sin_a + dy * cos_a + origin.y,
            )

        new_start = rotate_point(start)
        new_end = rotate_point(end)

        self._position = new_start
        self._end_offset = new_end - new_start
        return self

    def scale(self, factor: float, origin: Point | tuple[float, float] | None = None) -> Line:
        """
        Scale the line around a point.

        Args:
            factor: Scale factor (1.0 = no change).
            origin: Center of scaling (default: line center).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self.anchor("center")
        elif isinstance(origin, tuple):
            origin = Point(*origin)

        start = self.start
        end = self.end

        new_start = Point(
            origin.x + (start.x - origin.x) * factor,
            origin.y + (start.y - origin.y) * factor,
        )
        new_end = Point(
            origin.x + (end.x - origin.x) * factor,
            origin.y + (end.y - origin.y) * factor,
        )

        self._position = new_start
        self._end_offset = new_end - new_start
        return self

    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box."""
        x1, y1 = self.start
        x2, y2 = self.end
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    def to_svg(self) -> str:
        """Render to SVG line element."""
        s = self.start
        e = self.end
        svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()

        parts = [
            f'<line x1="{s.x}" y1="{s.y}" '
            f'x2="{e.x}" y2="{e.y}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}"'
        ]

        if marker_attrs:
            parts.append(marker_attrs)

        if self.opacity < 1.0:
            parts.append(f' opacity="{self.opacity}"')

        parts.append(" />")
        return "".join(parts)

    def __repr__(self) -> str:
        return (
            f"Line(({self.start.x}, {self.start.y}) -> "
            f"({self.end.x}, {self.end.y}), width={self.width}, color={self.color!r})"
        )
