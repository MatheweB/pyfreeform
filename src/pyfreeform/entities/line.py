"""Line - A line segment entity between two points."""

from __future__ import annotations

import math

from ..color import Color
from ..core.coord import Coord, CoordLike
from ..core.relcoord import RelCoord
from ..core.entity import Entity
from ..core.stroked_path_mixin import StrokedPathMixin


class Line(StrokedPathMixin, Entity):
    """
    A line segment between two points.

    Unlike connections (which link entities), a Line is a standalone
    entity with its own start and end points. Lines can be placed
    in cells and have other entities positioned along them.

    Attributes:
        position: The start point of the line
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

    @property
    def relative_start(self) -> RelCoord | None:
        """Relative start position (fraction of reference frame), or None."""
        return self._relative_at

    @relative_start.setter
    def relative_start(self, value: RelCoord | None) -> None:
        self._relative_at = value

    @property
    def relative_end(self) -> RelCoord | None:
        """Relative end position (fraction of reference frame), or None."""
        return self._relative_end

    @relative_end.setter
    def relative_end(self, value: RelCoord | None) -> None:
        self._relative_end = value

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
        start = Coord.coerce(start)
        end = Coord.coerce(end)
        return cls(
            start.x, start.y, end.x, end.y, width, color, z_index, cap, start_cap, end_cap, opacity
        )

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
        value = Coord.coerce(value)
        self._end_offset = value - self.position
        self._relative_end = None

    def _resolve_to_absolute(self) -> None:
        """Resolve relative start/end positions to absolute coordinates."""
        if (
            self._relative_end is not None
            or self._relative_at is not None
            or self._along_path is not None
        ):
            current_end = self.end
            super()._resolve_to_absolute()
            self._end_offset = current_end - self._position
            self._relative_end = None
        else:
            super()._resolve_to_absolute()

    @property
    def color(self) -> str:
        """The stroke color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def rotation_center(self) -> Coord:
        """Natural pivot for rotation/scale: line midpoint."""
        return self.start.midpoint(self.end)

    @property
    def length(self) -> float:
        """Length of the line (world space, accounts for scale)."""
        return self.start.distance_to(self.end) * self._scale_factor

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors: start, center, end."""
        return ["start", "center", "end"]

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name (world space)."""
        if name == "start":
            return self._to_world_space(self.start)
        if name == "center":
            return self._to_world_space(self.start.midpoint(self.end))
        if name == "end":
            return self._to_world_space(self.end)
        raise ValueError(f"Line has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the line (world space).

        Args:
            t:  Parameter from 0 (start) to 1 (end).
                Values outside 0-1 extrapolate beyond the line.

        Returns:
            Coord at that position along the line.
        """
        return self._to_world_space(self.start.lerp(self.end, t))

    def arc_length(self) -> float:
        """Return the length of the line segment."""
        return self.length

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t (world space).

        For a line, the angle is constant (same at every point).

        Args:
            t: Parameter (unused — angle is constant for lines).

        Returns:
            Angle in degrees.
        """
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        if dx == 0 and dy == 0:
            return self._rotation
        return math.degrees(math.atan2(dy, dx)) + self._rotation

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this line."""
        s, e = self.start, self.end
        return f"M {s.x} {s.y} L {e.x} {e.y}"

    def connection_data(self, segments: int = 32) -> tuple[str, list]:
        """Return shape kind and bezier data for Connection dispatch."""
        return ("line", [])

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
        start = Coord.coerce(start)
        end = Coord.coerce(end)

        self._position = start
        self._end_offset = end - start
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
                _, _, ref_w, ref_h = ref.ref_frame()
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                erx, ery = self._relative_end
                self._relative_end = RelCoord(erx + drx, ery + dry)
        super()._move_by(dx, dy)
        return self

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Get bounding box (world space, accounts for rotation and scale).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.
        """
        ws = self._to_world_space(self.start)
        we = self._to_world_space(self.end)
        min_x, min_y = min(ws.x, we.x), min(ws.y, we.y)
        max_x, max_y = max(ws.x, we.x), max(ws.y, we.y)
        if visual:
            half = self.width * self._scale_factor / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this line rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        ws = self._to_world_space(self.start)
        we = self._to_world_space(self.end)
        rx1 = ws.x * cos_a - ws.y * sin_a
        ry1 = ws.x * sin_a + ws.y * cos_a
        rx2 = we.x * cos_a - we.y * sin_a
        ry2 = we.x * sin_a + we.y * cos_a
        min_x, max_x = min(rx1, rx2), max(rx1, rx2)
        min_y, max_y = min(ry1, ry2), max(ry1, ry2)
        if visual:
            half = self.width * self._scale_factor / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        """Render to SVG line element (model-space coords + transform)."""
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

        transform = self._build_svg_transform()
        if transform:
            parts.append(transform)

        parts.append(" />")
        return "".join(parts)

    def __repr__(self) -> str:
        return (
            f"Line(({self.start.x}, {self.start.y}) -> "
            f"({self.end.x}, {self.end.y}), width={self.width}, color={self.color!r})"
        )
