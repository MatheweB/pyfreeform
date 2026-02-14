"""Connection - A link between two connectable objects that auto-updates."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Union

from ..color import Color, ColorLike, apply_brightness
from ..config.caps import CapName, collect_markers, svg_cap_and_marker_attrs
from ..config.styles import ConnectionStyle
from .bezier import curvature_control_point, eval_cubic, quadratic_to_cubic
from .coord import Coord
from .positions import AnchorSpec
from .svg_utils import opacity_attr, stroke_attrs

if TYPE_CHECKING:
    from ..entities.path import Path
    from .entity import Entity
    from .surface import Surface

Connectable = Union["Entity", "Surface"]


class Connection:
    """
    A connection between two connectable objects (entities or surfaces).

    Connections link any connectable objects together with a visible line
    by default. Use ``visible=False`` for invisible relationships.

    Attributes:
        start: The starting connectable object
        end: The ending connectable object
        start_anchor: Name of anchor on start object
        end_anchor: Name of anchor on end object
        data: Custom data dictionary

    Example:
        ```python
        dot1 = Dot(100, 100)
        dot2 = Dot(200, 200)
        # Visible straight line (default)
        conn = dot1.connect(dot2)
        # Styled line
        conn = dot1.connect(dot2, width=2, color="red")
        # Arc
        conn = dot1.connect(dot2, curvature=0.3)
        # Custom path
        conn = dot1.connect(dot2, path=Path.Wave())
        # Cell-to-cell connection
        conn = cell_a.connect(cell_b, color="red")
        # Entity-to-cell connection
        conn = dot.connect(cell, end_anchor="left")
        ```
    """

    def __init__(
        self,
        start: Connectable,
        end: Connectable,
        start_anchor: AnchorSpec = "center",
        end_anchor: AnchorSpec = "center",
        *,
        path: Path | None = None,
        curvature: float | None = None,
        visible: bool = True,
        width: float = 1,
        color: ColorLike = "black",
        z_index: int = 0,
        cap: CapName = "round",
        start_cap: CapName | None = None,
        end_cap: CapName | None = None,
        opacity: float = 1.0,
        color_brightness: float | None = None,
        style: ConnectionStyle | None = None,
        segments: int = 32,
    ) -> None:
        """
        Create a connection between two connectable objects.

        Args:
            start: The starting entity or surface.
            end: The ending entity or surface.
            start_anchor: Anchor name on start object.
            end_anchor: Anchor name on end object.
            path:   Custom path geometry (e.g. Path.Wave()). For simple arcs
                    use ``curvature`` instead.
            curvature:  Arc curvature (-1 to 1). Positive bows left,
                        negative bows right. Cannot be used with ``path``.
            visible: Whether the connection renders. Default True.
            width: Line width in pixels.
            color: Line color.
            z_index: Layer order (higher = on top).
            cap: Cap style for both ends ("round", "butt", "square").
            start_cap: Override cap for start end (e.g. "arrow").
            end_cap: Override cap for end end (e.g. "arrow").
            opacity: Opacity (0.0 transparent to 1.0 opaque).
            color_brightness: Brightness multiplier 0.0 (black) to 1.0 (unchanged).
            style: ConnectionStyle object (overrides individual params).
            segments: Number of Bézier segments for path rendering.
        """
        if curvature is not None and path is not None:
            raise ValueError(
                "Use 'curvature' for simple arcs or 'path' for custom paths, not both"
            )

        self._start = start
        self._end = end
        self._start_anchor = start_anchor
        self._end_anchor = end_anchor
        self._visible = visible

        # Style override (same pattern as add_dot, add_line, etc.)
        if style is not None:
            width = style.width
            color = style.color
            z_index = style.z_index
            cap = style.cap
            if style.start_cap is not None:
                start_cap = style.start_cap
            if style.end_cap is not None:
                end_cap = style.end_cap
            opacity = style.opacity
            if style.color_brightness is not None:
                color_brightness = style.color_brightness

        if color_brightness is not None:
            color = apply_brightness(color, color_brightness)
        self.width = float(width)
        self._color = Color(color)
        self._z_index = z_index
        self.cap = cap
        self.start_cap = start_cap
        self.end_cap = end_cap
        self.opacity = float(opacity)
        self._data: dict[str, Any] = {}

        # Geometry: line (default), curve (curvature=), or path (path=)
        self._curvature = curvature
        self._path = path
        self._shape_kind: str = "line"  # "line", "curve", "path"
        self._shape_beziers: list[tuple[Coord, Coord, Coord, Coord]] = []
        self._source_start: Coord | None = None
        self._source_end: Coord | None = None

        if path is not None:
            self._shape_kind = "path"
            self._source_start = path.point_at(0.0)
            self._source_end = path.point_at(1.0)
            _, self._shape_beziers = path.connection_data(segments)
        elif curvature is not None:
            self._shape_kind = "curve"
            # Normalized unit-chord bezier; affine-transformed to entity
            # positions at render time (same codepath as path=).
            self._source_start = Coord(0, 0)
            self._source_end = Coord(1, 0)
            control = curvature_control_point(
                self._source_start, self._source_end, curvature
            )
            self._shape_beziers = [
                quadratic_to_cubic(self._source_start, control, self._source_end)
            ]

        # Register with both entities
        start.add_connection(self)
        end.add_connection(self)

    @property
    def start(self) -> Connectable:
        """The starting connectable object."""
        return self._start

    @property
    def end(self) -> Connectable:
        """The ending connectable object."""
        return self._end

    @property
    def data(self) -> dict[str, Any]:
        """Custom data dictionary for this connection."""
        return self._data

    @property
    def start_anchor(self) -> AnchorSpec:
        """Anchor spec on start object."""
        return self._start_anchor

    @property
    def end_anchor(self) -> AnchorSpec:
        """Anchor spec on end object."""
        return self._end_anchor

    @property
    def start_point(self) -> Coord:
        """Current position of the start anchor (always up-to-date)."""
        return self._start.anchor(self._start_anchor)

    @property
    def end_point(self) -> Coord:
        """Current position of the end anchor (always up-to-date)."""
        return self._end.anchor(self._end_anchor)

    @property
    def color(self) -> str:
        """Line color."""
        return self._color.to_hex()

    @color.setter
    def color(self, value: ColorLike) -> None:
        self._color = Color(value)

    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._z_index

    @z_index.setter
    def z_index(self, value: int) -> None:
        self._z_index = value

    @property
    def visible(self) -> bool:
        """Whether this connection renders."""
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value

    @property
    def curvature(self) -> float | None:
        """Arc curvature, or None for straight/path."""
        return self._curvature

    @property
    def path(self):
        """The custom path geometry, or None."""
        return self._path

    @property
    def effective_start_cap(self) -> str:
        """Resolved cap for the start end."""
        return self.start_cap if self.start_cap is not None else self.cap

    @property
    def effective_end_cap(self) -> str:
        """Resolved cap for the end end."""
        return self.end_cap if self.end_cap is not None else self.cap

    def get_required_markers(self) -> list[tuple[str, str]]:
        """Collect SVG marker definitions needed by this connection's caps."""
        return collect_markers(self.cap, self.start_cap, self.end_cap, self.width, self.color)

    # --- Affine transform (source space → world space) ---

    def _compute_transform(self) -> tuple[float, float, float, Coord, Coord] | None:
        """
        Compute affine transform mapping source chord to entity chord.

        Returns:
            (scale, cos_r, sin_r, source_start, target_start) or None.
        """
        if self._source_start is None or self._source_end is None:
            return None

        ss, se = self._source_start, self._source_end
        A, B = self.start_point, self.end_point

        # Source chord
        src_dx, src_dy = se.x - ss.x, se.y - ss.y
        src_len = math.hypot(src_dx, src_dy)

        if src_len < 1e-9:
            return None

        # Target chord
        tgt_dx, tgt_dy = B.x - A.x, B.y - A.y
        tgt_len = math.hypot(tgt_dx, tgt_dy)

        scale = tgt_len / src_len

        # Rotation
        src_angle = math.atan2(src_dy, src_dx)
        tgt_angle = math.atan2(tgt_dy, tgt_dx)
        rot = tgt_angle - src_angle

        cos_r = math.cos(rot)
        sin_r = math.sin(rot)

        return (scale, cos_r, sin_r, ss, A)

    def _transform_point(self, p: Coord, xform: tuple[float, float, float, Coord, Coord]) -> Coord:
        """Transform a point from source space to world space."""
        scale, cos_r, sin_r, ss, A = xform
        dx = p.x - ss.x
        dy = p.y - ss.y
        rx = scale * (cos_r * dx - sin_r * dy)
        ry = scale * (sin_r * dx + cos_r * dy)
        return Coord(A.x + rx, A.y + ry)

    def point_at(self, t: float) -> Coord:
        """
        Get a point along the connection.

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Coord at that position along the connection.
        """
        if self._shape_kind == "line":
            return self.start_point.lerp(self.end_point, t)

        # Curve or path — evaluate beziers then affine-transform
        n = len(self._shape_beziers)
        t = max(0.0, min(1.0, t))

        if t >= 1.0:
            p = self._shape_beziers[-1][3]
        else:
            segment_t = t * n
            idx = int(segment_t)
            if idx >= n:
                idx = n - 1
            local_t = segment_t - idx
            p = eval_cubic(*self._shape_beziers[idx], local_t)

        xform = self._compute_transform()
        if xform is None:
            return self.start_point
        return self._transform_point(p, xform)

    def angle_at(self, t: float) -> float:
        """
        Get the tangent angle in degrees at parameter t.

        Args:
            t: Parameter from 0 (start) to 1 (end).

        Returns:
            Angle in degrees.
        """
        if self._shape_kind == "line":
            p1 = self.start_point
            p2 = self.end_point
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            if dx == 0 and dy == 0:
                return 0.0
            return math.degrees(math.atan2(dy, dx))

        # Numerical differentiation on transformed point_at
        epsilon = 1e-5
        t0 = max(0.0, t - epsilon)
        t1 = min(1.0, t + epsilon)
        p0 = self.point_at(t0)
        p1 = self.point_at(t1)
        dx = p1.x - p0.x
        dy = p1.y - p0.y
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def to_svg_path_d(self) -> str:
        """Return SVG path ``d`` attribute for this connection."""
        if self._shape_kind == "line":
            p1, p2 = self.start_point, self.end_point
            return f"M {p1.x} {p1.y} L {p2.x} {p2.y}"

        # Curve or path — transform stored beziers
        xform = self._compute_transform()
        if xform is None:
            p1 = self.start_point
            return f"M {p1.x} {p1.y} L {p1.x} {p1.y}"

        first = self._transform_point(self._shape_beziers[0][0], xform)
        parts = [f"M {first.x} {first.y}"]
        for _, cp1, cp2, p3 in self._shape_beziers:
            tcp1 = self._transform_point(cp1, xform)
            tcp2 = self._transform_point(cp2, xform)
            tp3 = self._transform_point(p3, xform)
            parts.append(f" C {tcp1.x} {tcp1.y} {tcp2.x} {tcp2.y} {tp3.x} {tp3.y}")
        return "".join(parts)

    def disconnect(self) -> None:
        """Remove this connection from both endpoints."""
        self._start.remove_connection(self)
        self._end.remove_connection(self)

    def to_svg(self) -> str:
        """Render connection as SVG element."""
        if not self._visible:
            return ""

        svg_cap, marker_attrs = svg_cap_and_marker_attrs(
            self.cap, self.start_cap, self.end_cap, self.width, self.color
        )

        if self._shape_kind == "line":
            p1 = self.start_point
            p2 = self.end_point
            return (
                f'<line x1="{p1.x}" y1="{p1.y}" x2="{p2.x}" y2="{p2.y}"'
                f"{stroke_attrs(self.color, self.width, svg_cap, marker_attrs)}"
                f"{opacity_attr(self.opacity)} />"
            )

        # Curve or path — render as <path>
        d_attr = self.to_svg_path_d()
        return (
            f'<path d="{d_attr}" fill="none"'
            f"{stroke_attrs(self.color, self.width, svg_cap, marker_attrs)}"
            f' stroke-linejoin="round"'
            f"{opacity_attr(self.opacity)} />"
        )

    def __repr__(self) -> str:
        if not self._visible:
            kind = "invisible"
        elif self._shape_kind == "path":
            kind = type(self._path).__name__
        elif self._shape_kind == "curve":
            kind = f"curve({self._curvature})"
        else:
            kind = "line"
        return (
            f"Connection({self._start!r} -> {self._end!r}, {kind}, "
            f"color={self.color!r}, width={self.width})"
        )
