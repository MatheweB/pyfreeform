"""Path - Renders any Pathable as a smooth SVG path using cubic Bézier approximation."""

from __future__ import annotations

import math
from ..color import Color
from ..core.entity import Entity
from ..core.coord import Coord, CoordLike
from ..core.pathable import Pathable
from ..core.stroked_path_mixin import StrokedPathMixin
from ..core.bezier import (
    fit_cubic_beziers as _fit_cubic_beziers,
    eval_cubic as _eval_cubic,
    eval_cubic_derivative as _eval_cubic_derivative,
)
from ..paths import Wave, Spiral, Lissajous, Zigzag


class Path(StrokedPathMixin, Entity):
    """
    Renders any Pathable as a smooth SVG ``<path>`` using cubic Bézier curves.

    This bridges the gap between the Pathable protocol (which only defines
    ``point_at(t)``) and actual SVG rendering. Pass in a Wave, Spiral,
    Lissajous, or any custom Pathable and get a smooth, stroked (and
    optionally filled) SVG curve.

    The algorithm samples the pathable and fits cubic Bézier segments using
    Hermite interpolation, giving C1 continuity (matching tangents) at every
    joint.

    For closed paths, the last segment wraps back to the first point with
    continuous smoothness — no visible seam.

    Attributes:
        closed: Whether this is a closed path.
        segments: Number of cubic Bézier segments used.
        start_t: Start parameter on the source pathable.
        end_t: End parameter on the source pathable.

    Anchors:
        - "start": The first point (t=0)
        - "center": The midpoint (t=0.5)
        - "end": The last point (t=1, or same as start if closed)

    Examples:
        >>> from pyfreeform import Path, Coord
        >>> # Render a custom Wave path:
        >>> wave = Wave(start=Coord(0, 50), end=Coord(200, 50), amplitude=20, frequency=3)
        >>> path = Path(wave, width=2, color="blue")
        >>> scene.add(path)

        >>> # Closed Lissajous with fill:
        >>> liss = Lissajous(center=Coord(100, 100), a=3, b=2, delta=math.pi/2, size=80)
        >>> path = Path(liss, closed=True, color="navy", fill="lightblue", width=1.5)

        >>> # Sub-path (arc) of an ellipse:
        >>> ellipse = Ellipse(100, 100, rx=50, ry=30)
        >>> arc = Path(ellipse, start_t=0.0, end_t=0.25, color="red", width=2)

        >>> # In a cell:
        >>> spiral = Spiral(center=cell.center, start_radius=5, end_radius=40, turns=3)
        >>> cell.add_path(spiral, color="red", width=1)
    """

    # Built-in path shapes (for IDE visibility)
    Wave = Wave
    Spiral = Spiral
    Lissajous = Lissajous
    Zigzag = Zigzag

    DEFAULT_SEGMENTS = 64
    DEFAULT_WIDTH = 1
    DEFAULT_COLOR = "black"
    DEFAULT_CAP = "round"

    def __init__(
        self,
        pathable: Pathable,
        *,
        segments: int = DEFAULT_SEGMENTS,
        closed: bool = False,
        start_t: float = 0.0,
        end_t: float = 1.0,
        width: float = DEFAULT_WIDTH,
        color: str | tuple[int, int, int] = DEFAULT_COLOR,
        fill: str | tuple[int, int, int] | None = None,
        z_index: int = 0,
        cap: str = DEFAULT_CAP,
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
    ) -> None:
        """
        Create a Path from a Pathable.

        Args:
            pathable: Any object implementing ``point_at(t)``.
            segments: Number of cubic Bézier segments to approximate with.
                      Higher = smoother but more SVG data. 64 is good for most
                      curves; use 128+ for very detailed spirals.
            closed: If True, the path closes smoothly back to the start and
                    SVG ``Z`` is appended. Enables ``fill``.
            start_t: Start parameter on the pathable (0.0-1.0). Use with
                     ``end_t`` to render a sub-section of the path.
            end_t: End parameter on the pathable (0.0-1.0). Use with
                   ``start_t`` to render a sub-section (arc) of any path.
            width: Stroke width in pixels.
            color: Stroke color.
            fill: Fill color for closed paths (ignored if not closed).
            z_index: Layer ordering (higher = on top).
            cap: Cap style for both ends ("round", "square", "butt", "arrow").
            start_cap: Override cap for start only.
            end_cap: Override cap for end only.
            opacity: Overall opacity (0.0 transparent to 1.0 opaque).
            fill_opacity: Override fill opacity (defaults to ``opacity``).
            stroke_opacity: Override stroke opacity (defaults to ``opacity``).
        """
        # Compute the first point for Entity's position
        first_point = pathable.point_at(start_t)
        super().__init__(first_point.x, first_point.y, z_index)

        self._closed = closed
        self._start_t = float(start_t)
        self._end_t = float(end_t)
        self.segments = segments
        self.width = float(width)
        self._color = Color(color)
        self._fill = Color(fill) if fill is not None else None
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)
        self.fill_opacity = fill_opacity
        self.stroke_opacity = stroke_opacity

        # Compute cubic Bézier segments from the pathable
        self._bezier_segments = _fit_cubic_beziers(
            pathable, segments, closed, start_t, end_t
        )

    @property
    def closed(self) -> bool:
        """Whether this is a closed path."""
        return self._closed

    @property
    def color(self) -> str:
        """The stroke color as a hex string."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: str | tuple[int, int, int]) -> None:
        self._color = Color(value)

    @property
    def fill(self) -> str | None:
        """The fill color as a hex string, or None."""
        if self._fill is None:
            return None
        return self._fill.to_hex()

    @fill.setter
    def fill(self, value: str | tuple[int, int, int] | None) -> None:
        self._fill = Color(value) if value is not None else None

    @property
    def anchor_names(self) -> list[str]:
        """Available anchors."""
        return ["start", "center", "end"]

    def anchor(self, name: str = "center") -> Coord:
        """Get anchor point by name."""
        if name == "start":
            return self.point_at(0.0)
        elif name == "center":
            return self.point_at(0.5)
        elif name == "end":
            return self.point_at(1.0)
        raise ValueError(f"Path has no anchor '{name}'. Available: {self.anchor_names}")

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the path.

        Evaluates the stored cubic Bézier segments at parameter ``t``.

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Coord on the path at parameter t.
        """
        n = len(self._bezier_segments)
        if n == 0:
            return self.position

        t = max(0.0, min(1.0, t))

        if t >= 1.0:
            seg = self._bezier_segments[-1]
            return seg[3]

        segment_t = t * n
        idx = int(segment_t)
        if idx >= n:
            idx = n - 1
        local_t = segment_t - idx

        return _eval_cubic(*self._bezier_segments[idx], local_t)

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t.

        Uses the derivative of the cubic Bézier formula.

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Angle in degrees.
        """
        n = len(self._bezier_segments)
        if n == 0:
            return 0.0

        t = max(0.0, min(1.0, t))

        if t >= 1.0:
            seg = self._bezier_segments[-1]
            dx, dy = _eval_cubic_derivative(*seg, 1.0)
        else:
            segment_t = t * n
            idx = int(segment_t)
            if idx >= n:
                idx = n - 1
            local_t = segment_t - idx
            seg = self._bezier_segments[idx]
            dx, dy = _eval_cubic_derivative(*seg, local_t)

        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def arc_length(self, samples: int = 200) -> float:
        """
        Approximate the total arc length by sampling each Bézier segment.

        Distributes *samples* evenly across all cubic Bézier segments and
        sums the polyline chord lengths — accurate for smooth curves with
        enough samples per segment.

        Args:
            samples: Total number of evaluation points distributed across
                     all Bézier segments.

        Returns:
            Approximate arc length in pixels.
        """
        n_segs = len(self._bezier_segments)
        if n_segs == 0:
            return 0.0
        per_seg = max(1, samples // n_segs)
        total = 0.0
        for seg in self._bezier_segments:
            prev = seg[0]
            for i in range(1, per_seg + 1):
                curr = _eval_cubic(*seg, i / per_seg)
                dx = curr.x - prev.x
                dy = curr.y - prev.y
                total += math.sqrt(dx * dx + dy * dy)
                prev = curr
        return total

    def to_svg_path_d(self) -> str:
        """Return the SVG path ``d`` attribute string."""
        if not self._bezier_segments:
            return ""

        p0 = self._bezier_segments[0][0]
        parts = [f"M {p0.x} {p0.y}"]

        for _, cp1, cp2, p3 in self._bezier_segments:
            parts.append(f" C {cp1.x} {cp1.y} {cp2.x} {cp2.y} {p3.x} {p3.y}")

        if self._closed:
            parts.append(" Z")

        return "".join(parts)

    @staticmethod
    def _cubic_axis_extrema(p0: float, p1: float, p2: float, p3: float) -> list[float]:
        """Critical t-values where one axis of a cubic Bezier is extremal.

        Solves B'(t)=0 for the quadratic derivative. Returns roots in (0,1).
        """
        # B'(t) = 3[a(1-t)² + 2b(1-t)t + ct²]  where a=P1-P0, b=P2-P1, c=P3-P2
        # Expanding: At² + Bt + C = 0
        a = p1 - p0
        b = p2 - p1
        c = p3 - p2
        A = a - 2 * b + c
        B = 2 * (b - a)
        C = a
        roots: list[float] = []
        if abs(A) < 1e-12:
            # Linear: Bt + C = 0
            if abs(B) > 1e-12:
                t = -C / B
                if 0 < t < 1:
                    roots.append(t)
        else:
            disc = B * B - 4 * A * C
            if disc >= 0:
                sd = math.sqrt(disc)
                for sign in (-1, 1):
                    t = (-B + sign * sd) / (2 * A)
                    if 0 < t < 1:
                        roots.append(t)
        return roots

    @staticmethod
    def _cubic_segment_bounds(
        p0x: float, p0y: float, p1x: float, p1y: float,
        p2x: float, p2y: float, p3x: float, p3y: float,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of one cubic Bezier segment. O(1)."""
        min_x, max_x = min(p0x, p3x), max(p0x, p3x)
        min_y, max_y = min(p0y, p3y), max(p0y, p3y)
        for t in Path._cubic_axis_extrema(p0x, p1x, p2x, p3x):
            mt = 1 - t
            v = mt * mt * mt * p0x + 3 * mt * mt * t * p1x + 3 * mt * t * t * p2x + t * t * t * p3x
            if v < min_x:
                min_x = v
            if v > max_x:
                max_x = v
        for t in Path._cubic_axis_extrema(p0y, p1y, p2y, p3y):
            mt = 1 - t
            v = mt * mt * mt * p0y + 3 * mt * mt * t * p1y + 3 * mt * t * t * p2y + t * t * t * p3y
            if v < min_y:
                min_y = v
            if v > max_y:
                max_y = v
        return (min_x, min_y, max_x, max_y)

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        """Exact bounding box (solves cubic Bezier extrema per segment).

        Args:
            visual: If True, expand by stroke width / 2 to reflect
                    the rendered extent.
        """
        if not self._bezier_segments:
            return (self.position.x, self.position.y,
                    self.position.x, self.position.y)

        min_x = min_y = math.inf
        max_x = max_y = -math.inf
        for p0, cp1, cp2, p3 in self._bezier_segments:
            sb = Path._cubic_segment_bounds(
                p0.x, p0.y, cp1.x, cp1.y, cp2.x, cp2.y, p3.x, p3.y,
            )
            if sb[0] < min_x: min_x = sb[0]
            if sb[1] < min_y: min_y = sb[1]
            if sb[2] > max_x: max_x = sb[2]
            if sb[3] > max_y: max_y = sb[3]
        if visual:
            half = self.width / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def _rotated_bounds(
        self, angle: float, *, visual: bool = False,
    ) -> tuple[float, float, float, float]:
        """Exact AABB of this path rotated by *angle* degrees around origin."""
        if angle == 0:
            return self.bounds(visual=visual)
        if not self._bezier_segments:
            rad = math.radians(angle)
            cos_a, sin_a = math.cos(rad), math.sin(rad)
            px = self.position.x * cos_a - self.position.y * sin_a
            py = self.position.x * sin_a + self.position.y * cos_a
            return (px, py, px, py)

        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)

        def _rot(x: float, y: float) -> tuple[float, float]:
            return x * cos_a - y * sin_a, x * sin_a + y * cos_a

        min_x = min_y = math.inf
        max_x = max_y = -math.inf
        for p0, cp1, cp2, p3 in self._bezier_segments:
            r0 = _rot(p0.x, p0.y)
            r1 = _rot(cp1.x, cp1.y)
            r2 = _rot(cp2.x, cp2.y)
            r3 = _rot(p3.x, p3.y)
            sb = Path._cubic_segment_bounds(
                r0[0], r0[1], r1[0], r1[1], r2[0], r2[1], r3[0], r3[1],
            )
            if sb[0] < min_x: min_x = sb[0]
            if sb[1] < min_y: min_y = sb[1]
            if sb[2] > max_x: max_x = sb[2]
            if sb[3] > max_y: max_y = sb[3]
        if visual:
            half = self.width / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def _move_by(self, dx: float = 0, dy: float = 0) -> Path:
        """
        Move the path by an offset.

        Args:
            dx: Horizontal offset.
            dy: Vertical offset.

        Returns:
            self, for method chaining.
        """
        self._position = Coord(self._position.x + dx, self._position.y + dy)
        self._bezier_segments = [
            (
                Coord(p0.x + dx, p0.y + dy),
                Coord(cp1.x + dx, cp1.y + dy),
                Coord(cp2.x + dx, cp2.y + dy),
                Coord(p3.x + dx, p3.y + dy),
            )
            for p0, cp1, cp2, p3 in self._bezier_segments
        ]
        return self

    def rotate(self, angle: float, origin: CoordLike | None = None) -> Path:
        """
        Rotate the path around a point.

        Args:
            angle: Rotation angle in degrees (counterclockwise).
            origin: Center of rotation (default: path midpoint).

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

        def rot(p: Coord) -> Coord:
            dx = p.x - origin.x
            dy = p.y - origin.y
            return Coord(
                dx * cos_a - dy * sin_a + origin.x,
                dx * sin_a + dy * cos_a + origin.y,
            )

        self._bezier_segments = [
            (rot(p0), rot(cp1), rot(cp2), rot(p3))
            for p0, cp1, cp2, p3 in self._bezier_segments
        ]
        if self._bezier_segments:
            self._position = self._bezier_segments[0][0]
        return self

    def scale(self, factor: float, origin: CoordLike | None = None) -> Path:
        """
        Scale the path around a point.

        Args:
            factor: Scale factor (1.0 = no change).
            origin: Center of scaling (default: path midpoint).

        Returns:
            self, for method chaining.
        """
        if origin is None:
            origin = self.point_at(0.5)
        elif isinstance(origin, tuple):
            origin = Coord(*origin)

        def sc(p: Coord) -> Coord:
            return Coord(
                origin.x + (p.x - origin.x) * factor,
                origin.y + (p.y - origin.y) * factor,
            )

        self._bezier_segments = [
            (sc(p0), sc(cp1), sc(cp2), sc(p3))
            for p0, cp1, cp2, p3 in self._bezier_segments
        ]
        if self._bezier_segments:
            self._position = self._bezier_segments[0][0]
        return self

    def to_svg(self) -> str:
        """Render to SVG path element."""
        if not self._bezier_segments:
            return ""

        svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()

        segs = self._bezier_segments

        parts_d = [f"M {segs[0][0].x} {segs[0][0].y}"]
        for _, cp1, cp2, p3 in segs:
            parts_d.append(f" C {cp1.x} {cp1.y} {cp2.x} {cp2.y} {p3.x} {p3.y}")
        if self._closed:
            parts_d.append(" Z")
        d_attr = "".join(parts_d)

        # Fill
        if self._closed and self._fill is not None:
            fill_attr = self._fill.to_hex()
        else:
            fill_attr = "none"

        parts = [
            f'<path d="{d_attr}" '
            f'fill="{fill_attr}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}" stroke-linejoin="round"'
        ]

        if marker_attrs:
            parts.append(marker_attrs)

        # Opacity handling
        eff_fill_opacity = self.fill_opacity if self.fill_opacity is not None else self.opacity
        eff_stroke_opacity = self.stroke_opacity if self.stroke_opacity is not None else self.opacity
        if eff_fill_opacity < 1.0:
            parts.append(f' fill-opacity="{eff_fill_opacity}"')
        if eff_stroke_opacity < 1.0:
            parts.append(f' stroke-opacity="{eff_stroke_opacity}"')

        parts.append(" />")
        return "".join(parts)

    def __repr__(self) -> str:
        kind = "closed" if self._closed else "open"
        return (
            f"Path({kind}, {len(self._bezier_segments)} segments, "
            f"color={self.color!r})"
        )

