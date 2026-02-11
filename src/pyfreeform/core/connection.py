"""Connection - A link between two entities that auto-updates."""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from .coord import Coord, CoordLike
from .stroked_path_mixin import StrokedPathMixin
from .bezier import fit_cubic_beziers, eval_cubic

if TYPE_CHECKING:
    from .entity import Entity
    from ..entities.line import Line
    from ..entities.curve import Curve
    from ..entities.path import Path


class Connection(StrokedPathMixin):
    """
    A connection between two entities.

    Connections link entities together. By default, connections are invisible
    — they represent a relationship without rendering anything. Pass a
    ``shape`` to give the connection a visual form.

    Attributes:
        start: The starting entity
        end: The ending entity
        start_anchor: Name of anchor on start entity
        end_anchor: Name of anchor on end entity
        style: Visual style properties (width, color, etc.)
        shape: The visual shape (Line, Curve, Path) or None for invisible

    Examples:
        >>> dot1 = Dot(100, 100)
        >>> dot2 = Dot(200, 200)
        >>> # Invisible relationship
        >>> conn = dot1.connect(dot2)
        >>> # Visible straight line
        >>> conn = dot1.connect(dot2, shape=Line(), style={"width": 2, "color": "red"})
        >>> # Visible arc
        >>> conn = dot1.connect(dot2, shape=Curve(curvature=0.3))
    """

    DEFAULT_STYLE = {
        "width": 1,
        "color": "black",
        "z_index": 0,
        "cap": "round",
    }

    def __init__(
        self,
        start: Entity,
        end: Entity,
        start_anchor: str = "center",
        end_anchor: str = "center",
        style: Any = None,
        shape: Line | Curve | Path | None = None,
        segments: int = 32,
    ) -> None:
        """
        Create a connection between two entities.

        Args:
            start: The starting entity.
            end: The ending entity.
            start_anchor: Anchor name on start entity.
            end_anchor: Anchor name on end entity.
            style: ConnectionStyle object or dict with "width", "color",
                   "z_index" keys.
            shape: Visual shape for the connection. None = invisible,
                   Line() = straight line, Curve() = arc, Path(...) = custom.
            segments: Number of Bézier segments for shape rendering.
        """
        from ..config.styles import ConnectionStyle
        from ..entities.path import Path as PathEntity

        self._start = start
        self._end = end
        self._start_anchor = start_anchor
        self._end_anchor = end_anchor
        if isinstance(style, ConnectionStyle):
            self._style = {**self.DEFAULT_STYLE, **style.to_dict()}
        else:
            self._style = {**self.DEFAULT_STYLE, **(style or {})}

        # Shape support
        from ..entities.line import Line as LineEntity
        from ..entities.curve import Curve as CurveEntity

        self._shape = shape
        self._shape_kind: str = "none"  # "none", "line", "curve", "path"
        self._shape_beziers: list[tuple[Coord, Coord, Coord, Coord]] = []
        self._source_start: Coord | None = None
        self._source_end: Coord | None = None

        if shape is not None:
            # Guard against closed paths
            if isinstance(shape, PathEntity) and shape.closed:
                raise ValueError(
                    "Closed paths cannot be used as connection shapes. "
                    "Use Path(pathable, start_t=0, end_t=0.25) for an arc."
                )
            self._source_start = shape.point_at(0.0)
            self._source_end = shape.point_at(1.0)

            if isinstance(shape, LineEntity):
                # Line: no bezier fitting needed — just affine on 2 endpoints
                self._shape_kind = "line"
            elif isinstance(shape, CurveEntity):
                # Curve: exact quadratic→cubic conversion (1 segment)
                self._shape_kind = "curve"
                P0 = shape.start
                Q = shape.control
                P2 = shape.end
                # Exact degree elevation: quadratic→cubic
                CP1 = Coord(P0.x + 2/3 * (Q.x - P0.x), P0.y + 2/3 * (Q.y - P0.y))
                CP2 = Coord(P2.x + 2/3 * (Q.x - P2.x), P2.y + 2/3 * (Q.y - P2.y))
                self._shape_beziers = [(P0, CP1, CP2, P2)]
            else:
                # Path: sample and fit cubic beziers
                self._shape_kind = "path"
                self._shape_beziers = fit_cubic_beziers(
                    shape, segments, closed=False
                )

        # Register with both entities
        start.add_connection(self)
        end.add_connection(self)

    @property
    def start(self) -> Entity:
        """The starting entity."""
        return self._start

    @property
    def end(self) -> Entity:
        """The ending entity."""
        return self._end

    @property
    def start_anchor(self) -> str:
        """Name of anchor on start entity."""
        return self._start_anchor

    @property
    def end_anchor(self) -> str:
        """Name of anchor on end entity."""
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
    def style(self) -> dict[str, Any]:
        """Visual style properties."""
        return self._style

    @property
    def width(self) -> float:
        """Line width."""
        return self._style.get("width", 1)

    @width.setter
    def width(self, value: float) -> None:
        self._style["width"] = value

    @property
    def color(self) -> str:
        """Line color."""
        return self._style.get("color", "black")

    @color.setter
    def color(self, value: str) -> None:
        self._style["color"] = value

    @property
    def z_index(self) -> int:
        """Layer ordering (higher values render on top)."""
        return self._style.get("z_index", 0)

    @z_index.setter
    def z_index(self, value: int) -> None:
        self._style["z_index"] = value

    @property
    def cap(self) -> str:
        """Cap style for both ends."""
        return self._style.get("cap", "round")

    @cap.setter
    def cap(self, value: str) -> None:
        self._style["cap"] = value

    @property
    def start_cap(self) -> str | None:
        """Override cap for the start end, or None."""
        return self._style.get("start_cap")

    @start_cap.setter
    def start_cap(self, value: str | None) -> None:
        self._style["start_cap"] = value

    @property
    def end_cap(self) -> str | None:
        """Override cap for the end end, or None."""
        return self._style.get("end_cap")

    @end_cap.setter
    def end_cap(self, value: str | None) -> None:
        self._style["end_cap"] = value

    @property
    def opacity(self) -> float:
        """Opacity (0.0 transparent to 1.0 opaque)."""
        return self._style.get("opacity", 1.0)

    @opacity.setter
    def opacity(self, value: float) -> None:
        self._style["opacity"] = value

    @property
    def shape(self):
        """The visual shape, or None for invisible."""
        return self._shape

    # --- Affine transform (shape space → world space) ---

    def _compute_transform(self) -> tuple[float, float, float, Coord, Coord] | None:
        """
        Compute affine transform mapping shape source chord to entity chord.

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
        """Transform a point from shape space to world space."""
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
        if self._shape_kind in ("none", "line"):
            # Invisible or straight line: lerp between entity endpoints
            return self.start_point.lerp(self.end_point, t)

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
        if self._shape_kind in ("none", "line"):
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
        if self._shape_kind in ("none", "line"):
            p1, p2 = self.start_point, self.end_point
            return f"M {p1.x} {p1.y} L {p2.x} {p2.y}"

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
        """Remove this connection from both entities."""
        self._start.remove_connection(self)
        self._end.remove_connection(self)

    def to_svg(self) -> str:
        """Render connection as SVG element."""
        if self._shape is None:
            return ""

        if self._shape_kind == "line":
            # Line shape — render as <line>, no bezier overhead
            p1 = self.start_point
            p2 = self.end_point
            svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()
            parts = [
                f'<line x1="{p1.x}" y1="{p1.y}" '
                f'x2="{p2.x}" y2="{p2.y}" '
                f'stroke="{self.color}" stroke-width="{self.width}" '
                f'stroke-linecap="{svg_cap}"'
            ]
            if marker_attrs:
                parts.append(marker_attrs)
            if self.opacity < 1.0:
                parts.append(f' opacity="{self.opacity}"')
            parts.append(" />")
            return "".join(parts)

        # Shaped connection — render as <path>
        d_attr = self.to_svg_path_d()
        svg_cap, marker_attrs = self._svg_cap_and_marker_attrs()

        parts = [
            f'<path d="{d_attr}" '
            f'fill="none" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="{svg_cap}" stroke-linejoin="round"'
        ]

        if marker_attrs:
            parts.append(marker_attrs)

        if self.opacity < 1.0:
            parts.append(f' opacity="{self.opacity}"')

        parts.append(" />")
        return "".join(parts)

    def __repr__(self) -> str:
        shape_str = type(self._shape).__name__ if self._shape else "invisible"
        return (
            f"Connection({self._start!r} -> {self._end!r}, "
            f"shape={shape_str}, style={self._style})"
        )
