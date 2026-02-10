"""Line - A line segment entity between two points."""

from __future__ import annotations

import math

from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike, RelCoord
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
        >>> line = Line.from_points(Coord(0, 0), Coord(100, 100))
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
        x2: float = 1,
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
        self._end_offset = Coord(x2 - x1, y2 - y1)
        self._relative_end: RelCoord | None = None
        self.width = float(width)
        self._color = Color(color)
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)

    @classmethod
    def from_points(
        cls,
        start: CoordLike,
        end: CoordLike,
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
            start = Coord(*start)
        if isinstance(end, tuple):
            end = Coord(*end)
        return cls(start.x, start.y, end.x, end.y, width, color, z_index, cap,
                   start_cap, end_cap, opacity)

    @property
    def start(self) -> Coord:
        """The starting point (same as position)."""
        return self.position

    @property
    def end(self) -> Coord:
        """The ending point (resolved from relative fraction if set)."""
        if self._relative_end is not None:
            result = self._resolve_relative(*self._relative_end)
            if result is not None:
                return result
        return self.position + self._end_offset

    @end.setter
    def end(self, value: CoordLike) -> None:
        """Set the ending point (clears relative binding)."""
        if isinstance(value, tuple):
            value = Coord(*value)
        self._end_offset = value - self.position
        self._relative_end = None

    def _to_pixel_mode(self) -> None:
        """Resolve both endpoints to pixels."""
        if self._relative_end is not None or self._relative_at is not None or self._along_path is not None:
            current_end = self.end
            super()._to_pixel_mode()
            self._end_offset = current_end - self._position
            self._relative_end = None
        else:
            super()._to_pixel_mode()

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

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name."""
        if name == "start":
            return self.start
        elif name == "center":
            return self.start.midpoint(self.end)
        elif name == "end":
            return self.end
        raise ValueError(f"Line has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the line.

        Args:
            t: Parameter from 0 (start) to 1 (end).
               Values outside 0-1 extrapolate beyond the line.

        Returns:
            Coord at that position along the line.
        """
        return self.start.lerp(self.end, t)

    def arc_length(self) -> float:
        """Return the length of the line segment."""
        return self.length

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

    def _move_to(self, x: float | Coord, y: float | None = None) -> Line:
        """
        Move the line's start point to a new position.

        The end point moves to maintain the same relative offset.

        Args:
            x: X coordinate, or a Coord.
            y: Y coordinate (required if x is not a Coord).

        Returns:
            self, for method chaining.
        """
        # Call parent implementation
        super()._move_to(x, y)
        return self

    def set_endpoints(
        self,
        start: CoordLike,
        end: CoordLike,
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
            start = Coord(*start)
        if isinstance(end, tuple):
            end = Coord(*end)

        self._position = start
        self._end_offset = end - start
        self._relative_at = None
        self._along_path = None
        self._relative_end = None
        return self

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Line:
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
            origin = Coord(*origin)

        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Rotate both endpoints
        start = self.start
        end = self.end

        def rotate_point(p: Coord) -> Coord:
            dx = p.x - origin.x
            dy = p.y - origin.y
            return Coord(
                dx * cos_a - dy * sin_a + origin.x,
                dx * sin_a + dy * cos_a + origin.y,
            )

        new_start = rotate_point(start)
        new_end = rotate_point(end)

        self._position = new_start
        self._end_offset = new_end - new_start
        self._relative_at = None
        self._along_path = None
        self._relative_end = None
        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Line:
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
            origin = Coord(*origin)

        start = self.start
        end = self.end

        new_start = Coord(
            origin.x + (start.x - origin.x) * factor,
            origin.y + (start.y - origin.y) * factor,
        )
        new_end = Coord(
            origin.x + (end.x - origin.x) * factor,
            origin.y + (end.y - origin.y) * factor,
        )

        self._position = new_start
        self._end_offset = new_end - new_start
        self._relative_at = None
        self._along_path = None
        self._relative_end = None
        return self

    def _move_by(self, dx: float = 0, dy: float = 0) -> Line:
        """Move both endpoints by a pixel offset."""
        if self._relative_end is not None:
            # Adjust end fractions in tandem with start
            ref = self._reference or self._cell
            if ref is not None:
                if isinstance(ref, Entity):
                    min_x, min_y, max_x, max_y = ref.bounds()
                    ref_w, ref_h = max_x - min_x, max_y - min_y
                else:
                    ref_w, ref_h = ref._width, ref._height
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                erx, ery = self._relative_end
                self._relative_end = RelCoord(erx + drx, ery + dry)
        return super()._move_by(dx, dy)

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
