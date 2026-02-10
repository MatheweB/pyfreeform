"""Curve - A quadratic Bezier curve entity."""

from __future__ import annotations

import math
from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike, RelCoord
from ..core.stroked_path_mixin import StrokedPathMixin


class Curve(StrokedPathMixin, Entity):
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
        x2: float = 1,
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
        self._end = Coord(x2, y2)
        self._relative_end: RelCoord | None = None
        self._curvature = float(curvature)
        self.width = float(width)
        self._color = Color(color)
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)
        self._control: Coord | None = None  # Calculated lazily

    @classmethod
    def from_points(
        cls,
        start: CoordLike,
        end: CoordLike,
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
            start = Coord(*start)
        if isinstance(end, tuple):
            end = Coord(*end)
        return cls(start.x, start.y, end.x, end.y, curvature, width, color, z_index,
                   cap, start_cap, end_cap, opacity)

    @property
    def start(self) -> Coord:
        """The starting point."""
        return self.position

    @property
    def end(self) -> Coord:
        """The ending point (resolved from relative fraction if set)."""
        if self._relative_end is not None:
            result = self._resolve_relative(*self._relative_end)
            if result is not None:
                return result
        return self._end

    @end.setter
    def end(self, value: CoordLike) -> None:
        if isinstance(value, tuple):
            value = Coord(*value)
        self._end = value
        self._relative_end = None
        self._control = None  # Invalidate cached control point

    def _to_pixel_mode(self) -> None:
        """Resolve both endpoints to pixels."""
        if self._relative_end is not None or self._relative_at is not None or self._along_path is not None:
            current_end = self.end
            super()._to_pixel_mode()
            self._end = current_end
            self._relative_end = None
            self._control = None
        else:
            super()._to_pixel_mode()

    @property
    def curvature(self) -> float:
        """The curvature amount."""
        return self._curvature

    @curvature.setter
    def curvature(self, value: float) -> None:
        self._curvature = float(value)
        self._control = None  # Invalidate cached control point

    @property
    def control(self) -> Coord:
        """
        The Bezier control point.

        Calculated from curvature: perpendicular to the line at its midpoint,
        offset by curvature * half the line length.
        """
        if self._control is None:
            self._control = self._calculate_control()
        return self._control

    def _calculate_control(self) -> Coord:
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

        return Coord(mid.x + perp_x * offset, mid.y + perp_y * offset)

    @property
    def color(self) -> str:
        """The stroke color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors."""
        return ["start", "center", "end", "control"]

    def anchor(self, name: str = "center") -> Coord:
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

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the curve.

        This is the key method for positioning elements along curves!

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Coord on the curve at parameter t.

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

        return Coord(x, y)

    def arc_length(self, segments: int = 100) -> float:
        """
        Approximate the arc length of the curve by sampling.

        Args:
            segments: Number of line segments to approximate with.

        Returns:
            Approximate arc length in pixels.
        """
        total = 0.0
        prev = self.point_at(0)
        for i in range(1, segments + 1):
            curr = self.point_at(i / segments)
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            total += math.sqrt(dx * dx + dy * dy)
            prev = curr
        return total

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t on the curve.

        Uses the derivative of the quadratic Bezier formula.

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Angle in degrees.
        """
        p0 = self.start
        p1 = self.control
        p2 = self.end

        # Derivative of quadratic Bezier: B'(t) = 2(1-t)(P1-P0) + 2t(P2-P1)
        dx = 2 * (1 - t) * (p1.x - p0.x) + 2 * t * (p2.x - p1.x)
        dy = 2 * (1 - t) * (p1.y - p0.y) + 2 * t * (p2.y - p1.y)

        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this quadratic Bezier curve."""
        s, c, e = self.start, self.control, self.end
        return f"M {s.x} {s.y} Q {c.x} {c.y} {e.x} {e.y}"

    @staticmethod
    def _quad_bezier_bounds(
        p0x: float, p0y: float,
        p1x: float, p1y: float,
        p2x: float, p2y: float,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of a quadratic Bezier (P0, P1=control, P2).

        Per axis the extremum is at ``t = (P0 - P1) / (P0 - 2P1 + P2)``.
        O(1), no sampling.
        """
        min_x, max_x = min(p0x, p2x), max(p0x, p2x)
        min_y, max_y = min(p0y, p2y), max(p0y, p2y)
        # X-axis extremum
        denom = p0x - 2 * p1x + p2x
        if abs(denom) > 1e-12:
            t = (p0x - p1x) / denom
            if 0 < t < 1:
                v = (1 - t) ** 2 * p0x + 2 * (1 - t) * t * p1x + t * t * p2x
                if v < min_x:
                    min_x = v
                if v > max_x:
                    max_x = v
        # Y-axis extremum
        denom = p0y - 2 * p1y + p2y
        if abs(denom) > 1e-12:
            t = (p0y - p1y) / denom
            if 0 < t < 1:
                v = (1 - t) ** 2 * p0y + 2 * (1 - t) * t * p1y + t * t * p2y
                if v < min_y:
                    min_y = v
                if v > max_y:
                    max_y = v
        return (min_x, min_y, max_x, max_y)

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Exact bounding box of this quadratic Bezier curve.

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.
        """
        p0, p1, p2 = self.start, self.control, self.end
        b = Curve._quad_bezier_bounds(p0.x, p0.y, p1.x, p1.y, p2.x, p2.y)
        if visual:
            half = self.width / 2
            b = (b[0] - half, b[1] - half, b[2] + half, b[3] + half)
        return b

    def _rotated_bounds(
        self, angle: float, *, visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this curve rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        p0, p1, p2 = self.start, self.control, self.end
        b = Curve._quad_bezier_bounds(
            p0.x * cos_a - p0.y * sin_a, p0.x * sin_a + p0.y * cos_a,
            p1.x * cos_a - p1.y * sin_a, p1.x * sin_a + p1.y * cos_a,
            p2.x * cos_a - p2.y * sin_a, p2.x * sin_a + p2.y * cos_a,
        )
        if visual:
            half = self.width / 2
            b = (b[0] - half, b[1] - half, b[2] + half, b[3] + half)
        return b

    def _move_by(self, dx: float = 0, dy: float = 0) -> Curve:
        """
        Move the curve by an offset, updating both endpoints.

        Args:
            dx: Horizontal offset.
            dy: Vertical offset.

        Returns:
            self, for method chaining.
        """
        if self._relative_end is not None:
            # Adjust end fractions in tandem with start
            ref = self._reference or self._cell
            if ref is not None:
                from ..core.entity import Entity as _Entity
                if isinstance(ref, _Entity):
                    min_x, min_y, max_x, max_y = ref.bounds()
                    ref_w, ref_h = max_x - min_x, max_y - min_y
                else:
                    ref_w, ref_h = ref._width, ref._height
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                erx, ery = self._relative_end
                self._relative_end = RelCoord(erx + drx, ery + dry)
            self._control = None
            return super()._move_by(dx, dy)
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        self._end = Coord(self._end.x + dx, self._end.y + dy)
        self._control = None
        return self

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Curve:
        """
        Rotate the curve around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: curve midpoint).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self.point_at(0.5)
        elif isinstance(origin, tuple):
            origin = Coord(*origin)

        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        def rotate_point(p: Coord) -> Coord:
            dx = p.x - origin.x
            dy = p.y - origin.y
            return Coord(
                dx * cos_a - dy * sin_a + origin.x,
                dx * sin_a + dy * cos_a + origin.y,
            )

        self._position = rotate_point(self.start)
        self._end = rotate_point(self.end)
        self._relative_at = None
        self._along_path = None
        self._relative_end = None
        self._control = None
        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Curve:
        """
        Scale the curve around a point.

        Args:
            factor: Scale factor (1.0 = no change).
            origin: Center of scaling (default: curve midpoint).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self.point_at(0.5)
        elif isinstance(origin, tuple):
            origin = Coord(*origin)

        new_start = Coord(
            origin.x + (self.start.x - origin.x) * factor,
            origin.y + (self.start.y - origin.y) * factor,
        )
        new_end = Coord(
            origin.x + (self.end.x - origin.x) * factor,
            origin.y + (self.end.y - origin.y) * factor,
        )

        self._position = new_start
        self._end = new_end
        self._relative_at = None
        self._along_path = None
        self._relative_end = None
        self._control = None
        return self

    def to_svg(self) -> str:
        """Render to SVG path element (quadratic Bezier)."""
        s = self.start
        c = self.control
        e = self.end
        svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()

        parts = [
            f'<path d="M {s.x} {s.y} Q {c.x} {c.y} {e.x} {e.y}" '
            f'fill="none" stroke="{self.color}" stroke-width="{self.width}" '
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
            f"Curve(({self.start.x}, {self.start.y}) -> ({self.end.x}, {self.end.y}), "
            f"curvature={self._curvature}, color={self.color!r})"
        )
