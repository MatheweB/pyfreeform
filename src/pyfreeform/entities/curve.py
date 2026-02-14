"""Curve - A quadratic Bezier curve entity."""

from __future__ import annotations

import math

from ..color import Color
from ..core.bezier import curvature_control_point, quadratic_to_cubic
from ..core.coord import Coord, CoordLike
from ..core.relcoord import RelCoord
from ..config.caps import CapName, collect_markers, svg_cap_and_marker_attrs
from ..core.entity import Entity
from ..core.bezier import sample_arc_length
from ..core.svg_utils import opacity_attr, stroke_attrs


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

    Example:
        ```python
        curve = Curve(0, 100, 100, 0, curvature=0.5)
        midpoint = curve.point_at(0.5)  # Point on the curve

        # In a cell:
        curve = cell.add_curve(start="bottom_left", end="top_right", curvature=0.3)
        cell.add_dot(along=curve, t=cell.brightness)

        # With arrow cap:
        curve = Curve(0, 100, 100, 0, curvature=0.5, end_cap="arrow")
        ```
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
        cap: CapName = DEFAULT_CAP,
        start_cap: CapName | None = None,
        end_cap: CapName | None = None,
        opacity: float = 1.0,
    ) -> None:
        """
        Create a curve from (x1, y1) to (x2, y2).

        Args:
            x1, y1: Starting point coordinates.
            x2, y2: Ending point coordinates.
            curvature:  How much the curve bows away from straight.
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
        curvature: float = 0.5,
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        z_index: int = 0,
        cap: CapName = DEFAULT_CAP,
        start_cap: CapName | None = None,
        end_cap: CapName | None = None,
        opacity: float = 1.0,
    ) -> Curve:
        """Create a curve from two points."""
        start = Coord.coerce(start)
        end = Coord.coerce(end)
        return cls(
            start.x,
            start.y,
            end.x,
            end.y,
            curvature,
            width,
            color,
            z_index,
            cap,
            start_cap,
            end_cap,
            opacity,
        )

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
        value = Coord.coerce(value)
        self._end = value
        self._relative_end = None
        self._control = None  # Invalidate cached control point

    def _resolve_to_absolute(self) -> None:
        """Resolve relative start/end positions to absolute coordinates."""
        if (
            self._relative_end is not None
            or self._relative_at is not None
            or self._along_path is not None
        ):
            current_end = self.end
            super()._resolve_to_absolute()
            self._end = current_end
            self._relative_end = None
            self._control = None
        else:
            super()._resolve_to_absolute()

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
        return curvature_control_point(self.start, self.end, self._curvature)

    @property
    def color(self) -> str:
        """The stroke color as a string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def rotation_center(self) -> Coord:
        """Natural pivot for rotation/scale: chord midpoint."""
        return self.start.midpoint(self.end)

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors."""
        return ["start", "center", "end", "control"]

    def _named_anchor(self, name: str) -> Coord:
        """Get anchor point by name (world space)."""
        if name == "start":
            return self._to_world_space(self.start)
        if name == "center":
            return self.point_at(0.5)
        if name == "end":
            return self._to_world_space(self.end)
        if name == "control":
            return self._to_world_space(self.control)
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
            ```python
            curve = cell.add_curve(curvature=0.5)
            cell.add_dot(along=curve, t=0.5)  # Dot at curve midpoint
            ```
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

        return self._to_world_space(Coord(x, y))

    def arc_length(self, segments: int = 100) -> float:
        """
        Approximate the arc length of the curve by sampling.

        Args:
            segments: Number of line segments to approximate with.

        Returns:
            Approximate arc length in pixels.
        """
        return sample_arc_length(self.point_at, segments)

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
        return math.degrees(math.atan2(dy, dx)) + self._rotation

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this quadratic Bezier curve."""
        s, c, e = self.start, self.control, self.end
        return f"M {s.x} {s.y} Q {c.x} {c.y} {e.x} {e.y}"

    def connection_data(self, segments: int = 32) -> tuple[str, list]:
        """Return shape kind and bezier data for Connection dispatch."""
        return ("curve", [quadratic_to_cubic(self.start, self.control, self.end)])

    @staticmethod
    def _quad_bezier_bounds(
        p0x: float,
        p0y: float,
        p1x: float,
        p1y: float,
        p2x: float,
        p2y: float,
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
        """Exact bounding box of this quadratic Bezier curve (world space).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.
        """
        p0, p1, p2 = self.start, self.control, self.end
        if self._rotation != 0 or self._scale_factor != 1.0:
            p0 = self._to_world_space(p0)
            p1 = self._to_world_space(p1)
            p2 = self._to_world_space(p2)
        b = Curve._quad_bezier_bounds(p0.x, p0.y, p1.x, p1.y, p2.x, p2.y)
        if visual:
            half = self.width * self._scale_factor / 2
            b = (b[0] - half, b[1] - half, b[2] + half, b[3] + half)
        return b

    def rotated_bounds(
        self,
        angle: float,
        *,
        visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this curve rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        p0, p1, p2 = self.start, self.control, self.end
        if self._rotation != 0 or self._scale_factor != 1.0:
            p0 = self._to_world_space(p0)
            p1 = self._to_world_space(p1)
            p2 = self._to_world_space(p2)
        b = Curve._quad_bezier_bounds(
            p0.x * cos_a - p0.y * sin_a,
            p0.x * sin_a + p0.y * cos_a,
            p1.x * cos_a - p1.y * sin_a,
            p1.x * sin_a + p1.y * cos_a,
            p2.x * cos_a - p2.y * sin_a,
            p2.x * sin_a + p2.y * cos_a,
        )
        if visual:
            half = self.width * self._scale_factor / 2
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
                _, _, ref_w, ref_h = ref.ref_frame()
                drx = dx / ref_w if ref_w > 0 else 0
                dry = dy / ref_h if ref_h > 0 else 0
                erx, ery = self._relative_end
                self._relative_end = RelCoord(erx + drx, ery + dry)
            self._control = None
            super()._move_by(dx, dy)
            return self
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        self._end = Coord(self._end.x + dx, self._end.y + dy)
        self._control = None
        return self

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return self.start_cap if self.start_cap is not None else self.cap

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return self.end_cap if self.end_cap is not None else self.cap

    def get_required_markers(self) -> list[tuple[str, str]]:
        """Collect SVG marker definitions needed by this curve's caps."""
        return collect_markers(self.cap, self.start_cap, self.end_cap, self.width, self.color)

    def to_svg(self) -> str:
        """Render to SVG path element (quadratic Bezier)."""
        s = self.start
        c = self.control
        e = self.end
        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            self.cap, self.start_cap, self.end_cap, self.width, self.color
        )
        return (
            f'<path d="M {s.x} {s.y} Q {c.x} {c.y} {e.x} {e.y}"'
            f' fill="none"'
            f"{stroke_attrs(self.color, self.width, svg_cap, marker_attrs)}"
            f"{opacity_attr(self.opacity)}"
            f"{self._build_svg_transform()} />"
        )

    def __repr__(self) -> str:
        return (
            f"Curve(({self.start.x}, {self.start.y}) -> ({self.end.x}, {self.end.y}), "
            f"curvature={self._curvature}, color={self.color!r})"
        )
