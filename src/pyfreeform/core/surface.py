"""Surface - Base class for any rectangular region that can contain entities."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Literal

from .binding import Binding
from .coord import Coord
from .relcoord import RelCoord
from .pathable import FullPathable, Pathable
from .tangent import get_angle_at
from .positions import Position, NAMED_POSITIONS

if TYPE_CHECKING:
    from ..config.styles import (
        BorderStyle,
        DotStyle,
        FillStyle,
        LineStyle,
        ShapeStyle,
        TextStyle,
    )
    from ..entities.curve import Curve
    from ..entities.dot import Dot
    from ..entities.ellipse import Ellipse
    from ..entities.line import Line
    from ..entities.path import Path
    from ..entities.point import Point
    from ..entities.polygon import Polygon
    from ..entities.rect import Rect
    from ..entities.text import Text
    from .entity import Entity


class Surface:
    """
    Base class for any rectangular region that can contain entities.

    Provides builder methods (add_dot, add_line, add_curve, etc.),
    position resolution (named positions, relative coordinates),
    and entity management.

    Subclasses must set these attributes in __init__:
        _x: float       — top-left X coordinate
        _y: float       — top-left Y coordinate
        _width: float   — width in pixels
        _height: float  — height in pixels
        _entities: list  — entity storage

    Implemented by: Cell, Scene, CellGroup
    """

    # Declared for type checkers; set by subclass __init__
    _x: float
    _y: float
    _width: float
    _height: float
    _entities: list[Entity]

    # =========================================================================
    # PROPERTIES
    # =========================================================================

    @property
    def x(self) -> float:
        """X coordinate of top-left corner."""
        return self._x

    @property
    def y(self) -> float:
        """Y coordinate of top-left corner."""
        return self._y

    @property
    def width(self) -> float:
        """Width in pixels."""
        return self._width

    @property
    def height(self) -> float:
        """Height in pixels."""
        return self._height

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """Bounds as (x, y, width, height)."""
        return (self._x, self._y, self._width, self._height)

    @property
    def entities(self) -> list[Entity]:
        """Entities placed in this surface."""
        return list(self._entities)

    # =========================================================================
    # POSITION HELPERS
    # =========================================================================

    @property
    def top_left(self) -> Coord:
        """Top-left corner position."""
        return Coord(self._x, self._y)

    @property
    def top_right(self) -> Coord:
        """Top-right corner position."""
        return Coord(self._x + self._width, self._y)

    @property
    def bottom_left(self) -> Coord:
        """Bottom-left corner position."""
        return Coord(self._x, self._y + self._height)

    @property
    def bottom_right(self) -> Coord:
        """Bottom-right corner position."""
        return Coord(self._x + self._width, self._y + self._height)

    @property
    def center(self) -> Coord:
        """Center position."""
        return Coord(self._x + self._width / 2, self._y + self._height / 2)

    def relative_to_absolute(self, pos: Position) -> Coord:
        """
        Convert relative position to absolute pixels.

        Args:
            pos: Either a (rx, ry) tuple where 0-1 maps to surface bounds,
                a named position like "center", "top_left", etc.,
                or a Coord (already absolute -- passed through unchanged).

        Returns:
            Absolute pixel position as Coord.
        """
        if isinstance(pos, Coord):
            return pos

        if isinstance(pos, str):
            if pos not in NAMED_POSITIONS:
                raise ValueError(
                    f"Unknown position '{pos}'. Available: {list(NAMED_POSITIONS.keys())}"
                )
            pos = NAMED_POSITIONS[pos]

        rx, ry = pos
        return Coord(self._x + rx * self._width, self._y + ry * self._height)

    def absolute_to_relative(self, point: Coord) -> RelCoord:
        """Convert absolute position to relative (0-1) coordinates."""
        rx = (point.x - self._x) / self._width if self._width > 0 else 0
        ry = (point.y - self._y) / self._height if self._height > 0 else 0
        return RelCoord(rx, ry)

    def contains(self, point: Coord) -> bool:
        """Check if a point is within this surface's bounds."""
        return (
            self._x <= point.x <= self._x + self._width
            and self._y <= point.y <= self._y + self._height
        )

    # =========================================================================
    # ENTITY REGISTRATION
    # =========================================================================

    def _register_entity(self, entity: Entity) -> None:
        """Register an entity with this surface. Override for custom behavior."""
        entity.cell = self
        self._entities.append(entity)

    def _resolve_along(
        self,
        along: Pathable,
        t: float | None,
        align: bool,
        user_rotation: float,
    ) -> tuple[Coord, float]:
        """
        Compute position and effective rotation from along/t/align params.

        Args:
            along: Path to position along.
            t: Parameter on the path (defaults to 0.5).
            align: Whether to rotate to follow path tangent.
            user_rotation: User-supplied rotation offset.

        Returns:
            (position, effective_rotation) tuple.
        """
        if t is None:
            t = 0.5
        position = along.point_at(t)
        if align:
            tangent_angle = get_angle_at(along, t)
            return position, tangent_angle + user_rotation
        return position, user_rotation

    def ref_frame(self) -> tuple[float, float, float, float]:
        """Return (x, y, width, height) of this surface.

        Provides a unified interface for both Entity and Surface,
        eliminating the need for isinstance checks when resolving
        relative coordinates.
        """
        return (self._x, self._y, self._width, self._height)

    def _get_ref_frame(self, within: Entity | None) -> tuple[float, float, float, float]:
        """Get (x, y, width, height) of the reference frame."""
        if within is not None:
            return within.ref_frame()
        return self.ref_frame()

    def _resolve_at(
        self,
        at: Position,
        ref_x: float,
        ref_y: float,
        ref_w: float,
        ref_h: float,
    ) -> tuple[Coord, RelCoord]:
        """Resolve a named/relative position to absolute pixels and RelCoord.

        Args:
            at: A named position string, RelCoord, or (rx, ry) tuple.
            ref_x, ref_y, ref_w, ref_h: Reference frame bounds.

        Returns:
            (absolute_position, relative_coord) pair.
        """
        if isinstance(at, str):
            if at not in NAMED_POSITIONS:
                raise ValueError(f"Invalid named position: '{at}'")
            at = NAMED_POSITIONS[at]
        rc = RelCoord.coerce(at)
        return Coord(ref_x + rc.rx * ref_w, ref_y + rc.ry * ref_h), rc

    # =========================================================================
    # BUILDER METHODS
    # =========================================================================

    def add_dot(
        self,
        *,
        at: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        radius: float = 0.05,
        color: str = "black",
        z_index: int = 0,
        opacity: float = 1.0,
        style: DotStyle | None = None,
    ) -> Dot:
        """
        Add a dot to this surface.

        Args:
            at: Position ("center", "top_left", or (rx, ry) tuple).
            within: Size/position relative to another entity's bounds.
            along: Path to position the dot along.
            t: Parameter on the path (0.0 to 1.0).
            radius: Dot radius as fraction of the smaller surface
                    dimension. 0.05 = 5% of min(width, height).
            color: Fill color.
            z_index: Layer order (higher = on top).
            opacity: Opacity (0.0 transparent to 1.0 opaque).
            style: DotStyle object (overrides individual params).

        Returns:
            The created Dot entity.

        Examples:
            >>> cell.add_dot()  # Centered, default style
            >>> cell.add_dot(color="red", radius=0.1)
            >>> cell.add_dot(at="top_left")
            >>> cell.add_dot(at=(0.25, 0.75))  # 25% across, 75% down
            >>> cell.add_dot(along=line, t=0.5)  # Midpoint of a line
        """
        from ..entities.dot import Dot

        if style:
            color = style.color
            z_index = style.z_index
            opacity = style.opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)
        ref_min = min(ref_w, ref_h)
        pixel_radius = radius * ref_min if ref_min > 0 else radius

        if along is not None:
            position, _ = self._resolve_along(along, t, False, 0)
            dot = Dot(
                position.x,
                position.y,
                radius=pixel_radius,
                color=color,
                z_index=z_index,
                opacity=opacity,
            )
            dot.binding = Binding(along=along, t=t if t is not None else 0.5, reference=within)
        else:
            position, at_rc = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)
            dot = Dot(
                position.x,
                position.y,
                radius=pixel_radius,
                color=color,
                z_index=z_index,
                opacity=opacity,
            )
            dot.binding = Binding(at=at_rc, reference=within)

        dot.relative_radius = radius
        self._register_entity(dot)
        return dot

    def add_line(
        self,
        *,
        start: Position = "center",
        end: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
        style: LineStyle | None = None,
    ) -> Line:
        """
        Add a line to this surface.

        When ``along`` is provided, the line's midpoint is repositioned
        onto the path at parameter ``t``. If ``align=True``, the line
        is also rotated to follow the path's tangent direction.

        Args:
            start: Starting position
            end: Ending position
            along: Path to position the line's midpoint along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            align: Rotate line to follow path tangent
            width: Stroke width in pixels
            color: Stroke color
            z_index: Layer order
            cap: Cap style for both ends ("round", "square", "butt", or "arrow")
            start_cap: Override cap for start end only
            end_cap: Override cap for end end only
            style: LineStyle object (overrides individual params)

        Returns:
            The created Line entity.

        Examples:
            >>> cell.add_line(start="top_left", end="bottom_right")
            >>> cell.add_line(start="left", end="right", end_cap="arrow")
            >>> # Position along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_line(start=(0,0), end=(20,0), along=curve, t=0.5, align=True)
        """
        from ..entities.line import Line

        if style:
            width = style.width
            color = style.color
            z_index = style.z_index
            cap = style.cap
            start_cap = style.start_cap
            end_cap = style.end_cap
            opacity = style.opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)
        if isinstance(start, str):
            start = NAMED_POSITIONS[start]
        if isinstance(end, str):
            end = NAMED_POSITIONS[end]
        start_pos = Coord(ref_x + start[0] * ref_w, ref_y + start[1] * ref_h)
        end_pos = Coord(ref_x + end[0] * ref_w, ref_y + end[1] * ref_h)

        line = Line.from_points(
            start_pos,
            end_pos,
            width=width,
            color=color,
            z_index=z_index,
            cap=cap,
            start_cap=start_cap,
            end_cap=end_cap,
            opacity=opacity,
        )

        if along is not None:
            target, rotation = self._resolve_along(along, t, align, 0)
            midpoint = line.anchor("center")
            dx, dy = target.x - midpoint.x, target.y - midpoint.y
            line = Line.from_points(
                Coord(start_pos.x + dx, start_pos.y + dy),
                Coord(end_pos.x + dx, end_pos.y + dy),
                width=width,
                color=color,
                z_index=z_index,
                cap=cap,
                start_cap=start_cap,
                end_cap=end_cap,
                opacity=opacity,
            )
            if align:
                line.rotate(rotation, origin=target)
            else:
                line._resolve_to_absolute()

        if not line.is_resolved:
            line.relative_start = RelCoord.coerce(start)
            line.relative_end = RelCoord.coerce(end)
        line.binding = Binding(reference=within)
        self._register_entity(line)
        return line

    def add_diagonal(
        self,
        *,
        start: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "bottom_left",
        end: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "top_right",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
        style: LineStyle | None = None,
    ) -> Line:
        """
        Add a diagonal line across this surface.

        Convenience method that delegates to add_line() with corner positions.

        Args:
            start: Starting corner (default: "bottom_left")
            end: Ending corner (default: "top_right")
            along: Path to position the line's midpoint along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            align: Rotate line to follow path tangent
            width: Stroke width
            color: Stroke color
            z_index: Layer order
            cap: Cap style for both ends
            start_cap: Override cap for start end only
            end_cap: Override cap for end end only
            style: LineStyle object

        Returns:
            The created Line entity.

        Examples:
            >>> line = cell.add_diagonal()  # Bottom-left to top-right (SW to NE)
            >>> line = cell.add_diagonal(start="top_left", end="bottom_right")  # NW to SE
            >>> cell.add_dot(along=line, t=cell.brightness)  # Dot slides along
        """
        return self.add_line(
            start=start,
            end=end,
            within=within,
            along=along,
            t=t,
            align=align,
            width=width,
            color=color,
            z_index=z_index,
            cap=cap,
            start_cap=start_cap,
            end_cap=end_cap,
            opacity=opacity,
            style=style,
        )

    def add_curve(
        self,
        *,
        start: Position = "bottom_left",
        end: Position = "top_right",
        curvature: float = 0.5,
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
        style: LineStyle | None = None,
    ) -> Curve:
        """
        Add a smooth curve between two points.

        The ``curvature`` parameter controls how much the curve bows
        away from a straight line.

        When ``along`` is provided, the curve's midpoint is repositioned
        onto the path at parameter ``t``. If ``align=True``, the curve
        is also rotated to follow the path's tangent direction.

        Args:
            start: Starting position
            end: Ending position
            curvature:  How much the curve bows (-1 to 1, 0 = straight)
                        Positive = bows left, Negative = bows right
            along: Path to position the curve's midpoint along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            align: Rotate curve to follow path tangent
            width: Stroke width in pixels
            color: Stroke color
            z_index: Layer order
            cap: Cap style for both ends ("round", "square", "butt", or "arrow")
            start_cap: Override cap for start end only
            end_cap: Override cap for end end only
            style: LineStyle object (overrides width/color/z_index/cap)

        Returns:
            The created Curve entity.

        Examples:
            >>> curve = cell.add_curve(curvature=0.5)  # Gentle bow
            >>> curve = cell.add_curve(curvature=-0.8, end_cap="arrow")
            >>> cell.add_dot(along=curve, t=cell.brightness)  # Dot slides along!
        """
        from ..entities.curve import Curve

        if style:
            width = style.width
            color = style.color
            z_index = style.z_index
            cap = style.cap
            start_cap = style.start_cap
            end_cap = style.end_cap
            opacity = style.opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)
        if isinstance(start, str):
            start = NAMED_POSITIONS[start]
        if isinstance(end, str):
            end = NAMED_POSITIONS[end]
        start_pos = Coord(ref_x + start[0] * ref_w, ref_y + start[1] * ref_h)
        end_pos = Coord(ref_x + end[0] * ref_w, ref_y + end[1] * ref_h)

        curve = Curve.from_points(
            start_pos,
            end_pos,
            curvature=curvature,
            width=width,
            color=color,
            z_index=z_index,
            cap=cap,
            start_cap=start_cap,
            end_cap=end_cap,
            opacity=opacity,
        )

        if along is not None:
            target, rotation = self._resolve_along(along, t, align, 0)
            midpoint = curve.point_at(0.5)
            dx, dy = target.x - midpoint.x, target.y - midpoint.y
            curve = Curve.from_points(
                Coord(start_pos.x + dx, start_pos.y + dy),
                Coord(end_pos.x + dx, end_pos.y + dy),
                curvature=curvature,
                width=width,
                color=color,
                z_index=z_index,
                cap=cap,
                start_cap=start_cap,
                end_cap=end_cap,
                opacity=opacity,
            )
            if align:
                curve.rotate(rotation, origin=target)
            else:
                curve._resolve_to_absolute()

        if not curve.is_resolved:
            curve.relative_start = RelCoord.coerce(start)
            curve.relative_end = RelCoord.coerce(end)
        curve.binding = Binding(reference=within)
        self._register_entity(curve)
        return curve

    def add_path(
        self,
        pathable: Pathable,
        *,
        segments: int = 64,
        closed: bool = False,
        start_t: float = 0.0,
        end_t: float = 1.0,
        width: float = 1,
        color: str = "black",
        fill: str | None = None,
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
        style: LineStyle | None = None,
    ) -> Path:
        """
        Add a smooth path rendered from any Pathable.

        Takes any object with a ``point_at(t)`` method (Wave, Spiral,
        Lissajous, or your own custom class) and renders it as a smooth
        SVG path using cubic Bézier approximation.

        Supports both open and closed paths. Closed paths can be filled.
        Use ``start_t`` and ``end_t`` to render a sub-section (arc) of
        any pathable.

        Args:
            pathable: Any object implementing ``point_at(t)``.
            segments: Number of cubic Bézier segments (higher = smoother).
            closed: Close the path smoothly back to start.
            start_t: Start parameter on the pathable (0.0-1.0).
            end_t: End parameter on the pathable (0.0-1.0).
            width: Stroke width in pixels.
            color: Stroke color.
            fill: Fill color for closed paths (ignored if not closed).
            z_index: Layer order.
            cap: Cap style for both ends ("round", "square", "butt", "arrow").
            start_cap: Override cap for start only.
            end_cap: Override cap for end only.
            opacity: Overall opacity.
            fill_opacity: Override fill opacity.
            stroke_opacity: Override stroke opacity.
            style: LineStyle object (overrides width/color/z_index/cap).

        Returns:
            The created Path entity.

        Examples:
            >>> wave = Wave(start=cell.center, end=cell.right_center, amplitude=10, frequency=3)
            >>> cell.add_path(wave, color="blue", width=2)
            >>> # Arc of an ellipse (quarter circle):
            >>> ellipse = cell.add_ellipse(rx=0.4, ry=0.4)
            >>> cell.add_path(ellipse, start_t=0.0, end_t=0.25, color="red")
        """
        from ..entities.path import Path

        if style:
            width = style.width
            color = style.color
            z_index = style.z_index
            cap = style.cap
            start_cap = style.start_cap
            end_cap = style.end_cap
            opacity = style.opacity

        path = Path(
            pathable,
            segments=segments,
            closed=closed,
            start_t=start_t,
            end_t=end_t,
            width=width,
            color=color,
            fill=fill,
            z_index=z_index,
            cap=cap,
            start_cap=start_cap,
            end_cap=end_cap,
            opacity=opacity,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
        )

        self._register_entity(path)
        return path

    def add_ellipse(
        self,
        *,
        at: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        rx: float | None = None,
        ry: float | None = None,
        rotation: float = 0,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
        style: ShapeStyle | None = None,
    ) -> Ellipse:
        """
        Add an ellipse to this surface.

        Ellipses support parametric positioning just like lines and curves.
        Use ``along`` + ``t`` to place the ellipse center on a path.
        Use ``align=True`` to rotate the ellipse to follow the tangent.

        Args:
            at: Position (center of ellipse)
            along: Path to position the ellipse center along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            align: Rotate ellipse to follow path tangent
            rx: Horizontal radius as fraction of surface width (default 0.4)
            ry: Vertical radius as fraction of surface height (default 0.4)
            rotation: Rotation in degrees (counterclockwise)
            fill: Fill color (None for transparent)
            stroke: Stroke color (None for no stroke)
            stroke_width: Stroke width in pixels
            z_index: Layer order
            style: ShapeStyle object (overrides fill/stroke/stroke_width/z_index)

        Returns:
            The created Ellipse entity.

        Examples:
            >>> ellipse = cell.add_ellipse(rx=0.3, ry=0.2)
            >>> cell.add_dot(along=ellipse, t=cell.brightness)
            >>> # Place ellipse along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_ellipse(rx=0.1, ry=0.06, along=curve, t=0.5, align=True)
        """
        from ..entities.ellipse import Ellipse

        if style:
            fill = style.color
            stroke = style.stroke
            stroke_width = style.stroke_width
            z_index = style.z_index
            opacity = style.opacity
            fill_opacity = style.fill_opacity
            stroke_opacity = style.stroke_opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)

        at_coord: RelCoord | None = None
        if along is not None:
            position, rotation = self._resolve_along(along, t, align, rotation)
        else:
            position, at_coord = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)

        if rx is None:
            rx = 0.4
        if ry is None:
            ry = 0.4
        rx_px = rx * ref_w
        ry_px = ry * ref_h

        ellipse = Ellipse(
            position.x,
            position.y,
            rx=rx_px,
            ry=ry_px,
            rotation=rotation,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            z_index=z_index,
            opacity=opacity,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
        )

        if along is not None:
            ellipse.binding = Binding(along=along, t=t if t is not None else 0.5, reference=within)
        else:
            ellipse.binding = Binding(at=at_coord, reference=within)

        ellipse.relative_rx = rx
        ellipse.relative_ry = ry
        self._register_entity(ellipse)
        return ellipse

    def add_polygon(
        self,
        vertices: list[tuple[float, float]],
        *,
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
        rotation: float = 0,
        style: ShapeStyle | None = None,
    ) -> Polygon:
        """
        Add a polygon to this surface.

        Vertices are specified in relative coordinates (0-1), where
        (0,0) is top-left and (1,1) is bottom-right of the surface.

        When ``along`` is provided, the polygon's centroid is repositioned
        onto the path at parameter ``t``. If ``align=True``, the polygon
        is rotated to follow the path's tangent direction.

        Args:
            vertices:   List of (x, y) tuples in relative coordinates.
                        Use Polygon.hexagon(), Polygon.star() for common shapes.
            along: Path to position the polygon's centroid along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            align: Rotate polygon to follow path tangent
            fill: Fill color (None for transparent)
            stroke: Stroke color (None for no stroke)
            stroke_width: Stroke width in pixels
            z_index: Layer order
            rotation: Rotation in degrees (around polygon center)
            style: ShapeStyle object (overrides fill/stroke/stroke_width/z_index)

        Returns:
            The created Polygon entity.

        Examples:
            >>> cell.add_polygon([(0.5, 0.1), (0.9, 0.9), (0.1, 0.9)], fill="red")
            >>> from pyfreeform.entities.polygon import Polygon
            >>> cell.add_polygon(Polygon.hexagon(), fill="purple")
            >>> # Place polygon along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_polygon(Polygon.hexagon(), along=curve, t=0.5, align=True)
        """
        from ..entities.polygon import Polygon

        if style:
            fill = style.color
            stroke = style.stroke
            stroke_width = style.stroke_width
            z_index = style.z_index
            opacity = style.opacity
            fill_opacity = style.fill_opacity
            stroke_opacity = style.stroke_opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)
        absolute_vertices = [Coord(ref_x + v[0] * ref_w, ref_y + v[1] * ref_h) for v in vertices]

        polygon = Polygon(
            absolute_vertices,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            z_index=z_index,
            opacity=opacity,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
        )

        if along is not None:
            target, effective_rotation = self._resolve_along(along, t, align, rotation)
            center = polygon.position
            dx, dy = target.x - center.x, target.y - center.y
            shifted_verts = [Coord(v.x + dx, v.y + dy) for v in absolute_vertices]
            polygon = Polygon(
                shifted_verts,
                fill=fill,
                stroke=stroke,
                stroke_width=stroke_width,
                z_index=z_index,
                opacity=opacity,
                fill_opacity=fill_opacity,
                stroke_opacity=stroke_opacity,
            )
            if effective_rotation != 0:
                polygon.rotate(effective_rotation, origin=target)
            else:
                polygon._resolve_to_absolute()
        elif rotation != 0:
            polygon.rotate(rotation)

        if not polygon.is_resolved:
            polygon.relative_vertices = [RelCoord.coerce(v) for v in vertices]
        polygon.binding = Binding(reference=within)
        self._register_entity(polygon)
        return polygon

    def add_text(
        self,
        content: str,
        *,
        at: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        font_size: float | None = None,
        color: str = "black",
        font_family: str = "sans-serif",
        bold: bool = False,
        italic: bool = False,
        text_anchor: str | None = None,
        baseline: str = "middle",
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
        fit: bool = False,
        start_offset: float = 0.0,
        end_offset: float = 1.0,
        style: TextStyle | None = None,
    ) -> Text:
        """
        Add text to this surface.

        When ``along`` is provided with ``t``, the text is positioned at
        that point on the path. If ``align=True``, the text is rotated
        to follow the path's tangent.

        When ``along`` is provided without ``t``, the text is warped
        along the path using SVG ``<textPath>``.

        Args:
            content: The text string to display.
            at: Position ("center", "top_left", or (rx, ry) tuple).
            along: Path to position or warp text along.
            t:  Parameter on the path (0.0 to 1.0). If omitted with
                ``along``, text warps along the full path.
            align: Rotate text to follow path tangent (only with ``t``).
            font_size: Font size as fraction of surface height (e.g. 0.25
                = 25% of cell height). When omitted, defaults to 0.25.
                For textPath mode, auto-sizes to fill the path.
            color: Text color.
            font_family: Font family.
            bold: Bold text.
            italic: Italic text.
            text_anchor: Horizontal alignment: "start", "middle", "end".
            baseline: Vertical alignment: "auto", "middle", "hanging".
            rotation: Rotation in degrees around the text position.
            z_index: Layer order (higher = on top).
            fit: If True, shrink font_size so the rendered text fits
                within the cell width. Never upsizes — font_size is a ceiling.
            start_offset: Where text begins on the path, 0.0-1.0
                (textPath mode only). Default 0.0 = start of path.
            end_offset: Where text ends on the path, 0.0-1.0
                (textPath mode only). Default 1.0 = end of path.
            style: TextStyle object (overrides individual params).

        Returns:
            The created Text entity.

        Examples:
            >>> cell.add_text("A")  # Centered letter
            >>> cell.add_text("Label", at="top", font_size=0.15)
            >>> # Position text along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_text("Hi", along=curve, t=0.5, align=True)
            >>> # Warp text along a curve (textPath)
            >>> cell.add_text("Hello World", along=curve)
            >>> # Warp along middle 60% of the path
            >>> cell.add_text("Partial", along=curve, start_offset=0.2, end_offset=0.8)
        """
        from ..entities.text import Text, _measure_text_width

        if style:
            color = style.color
            font_family = style.font_family
            bold = style.bold
            italic = style.italic
            text_anchor = style.text_anchor
            baseline = style.baseline
            rotation = style.rotation
            z_index = style.z_index
            opacity = style.opacity

        # Resolve text_anchor default based on mode
        is_textpath = along is not None and t is None
        if text_anchor is None:
            text_anchor = "start" if is_textpath else "middle"
        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)

        at_coord: RelCoord | None = None
        if along is not None and t is not None:
            position, rotation = self._resolve_along(along, t, align, rotation)
        elif along is not None:
            # TextPath warp mode — position at path midpoint (used as fallback)
            position, rotation = self._resolve_along(along, 0.5, align, rotation)
        else:
            position, at_coord = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)

        # Compute the span fraction for textPath mode
        span = end_offset - start_offset

        # Resolve font_size: fraction of reference height → pixels
        if font_size is None:
            if is_textpath and (along is not None) and isinstance(along, FullPathable):
                # Auto-size to fill the spanned portion of the path
                arc_len = along.arc_length() * span
                chars = max(len(content), 1)
                pixel_font_size = arc_len / (chars * 0.6)
                pixel_font_size = min(pixel_font_size, ref_h * 0.25)
                rel_font_size = pixel_font_size / ref_h if ref_h > 0 else 0.25
            else:
                rel_font_size = 0.25
                pixel_font_size = rel_font_size * ref_h if ref_h > 0 else 0.25
        else:
            rel_font_size = font_size
            pixel_font_size = font_size * ref_h if ref_h > 0 else font_size

        # fit=True: shrink font so text fits within the cell width (never upsize)
        # Ignored in path modes — path length is the constraint, not cell width.
        if fit and along is None and ref_w > 0 and content:
            font_weight = "bold" if bold else "normal"
            font_style = "italic" if italic else "normal"
            width_at_1px = _measure_text_width(
                content,
                1.0,
                font_family,
                font_weight,
                font_style,
            )
            if width_at_1px > 0:
                max_from_width = ref_w / width_at_1px
                if max_from_width < pixel_font_size:
                    pixel_font_size = max_from_width
                    rel_font_size = pixel_font_size / ref_h if ref_h > 0 else rel_font_size

        text = Text(
            position.x,
            position.y,
            content=content,
            font_size=pixel_font_size,
            color=color,
            font_family=font_family,
            bold=bold,
            italic=italic,
            text_anchor=text_anchor,
            baseline=baseline,
            rotation=rotation,
            z_index=z_index,
            opacity=opacity,
        )

        text.relative_font_size = rel_font_size
        if along is not None and t is not None:
            text.binding = Binding(along=along, t=t, reference=within)
        elif at_coord is not None:
            text.binding = Binding(at=at_coord, reference=within)
        elif within is not None:
            # textpath mode (along without t): stays pixel, but track reference
            text.binding = Binding(reference=within)

        # TextPath warp mode: along provided without t
        if is_textpath and (along is not None):
            if not isinstance(along, FullPathable):
                raise TypeError(
                    f"Text warping requires a FullPathable (with to_svg_path_d()), "
                    f"but {type(along).__name__} does not implement it."
                )
            _textpath_counter = getattr(self, "_textpath_counter", None)
            if _textpath_counter is None:
                _textpath_counter = itertools.count()
                self._textpath_counter = _textpath_counter
            path_id = f"textpath-{next(_textpath_counter)}"
            # Compute text_length from the spanned portion of the path
            text_length = None
            if isinstance(along, FullPathable):
                text_length = along.arc_length() * span
            svg_start_offset = f"{start_offset * 100:.1f}%"
            text.set_textpath(
                path_id,
                along.to_svg_path_d(),
                start_offset=svg_start_offset,
                text_length=text_length,
            )

        self._register_entity(text)
        return text

    def add_rect(
        self,
        *,
        at: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        width: float | None = None,
        height: float | None = None,
        rotation: float = 0,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None,
        z_index: int = 0,
        style: ShapeStyle | None = None,
    ) -> Rect:
        """
        Add a rectangle to this surface.

        The ``at`` parameter specifies where the CENTER of the rectangle
        will be placed, consistent with add_ellipse().

        When ``along`` is provided, the rectangle center is repositioned
        onto the path at parameter ``t``. If ``align=True``, the rectangle
        is rotated to follow the path's tangent direction.

        For full-surface fills use add_fill(). For borders use add_border().

        Args:
            at: Position of rectangle center.
            along: Path to position the rectangle center along.
            t: Parameter on the path (0.0 to 1.0, default 0.5).
            align: Rotate rectangle to follow path tangent.
            width: Rectangle width as fraction of surface width (default 0.6).
            height: Rectangle height as fraction of surface height (default 0.6).
            rotation: Rotation in degrees (counterclockwise).
            fill: Fill color (None for transparent).
            stroke: Stroke color (None for no stroke).
            stroke_width: Stroke width in pixels.
            opacity: Opacity for both fill and stroke (0.0-1.0).
            fill_opacity: Override opacity for fill only.
            stroke_opacity: Override opacity for stroke only.
            z_index: Layer order (higher = on top).
            style: ShapeStyle object.

        Returns:
            The created Rect entity.

        Examples:
            >>> rect = cell.add_rect(fill="coral")
            >>> rect = cell.add_rect(width=0.5, height=0.4, rotation=45)
            >>> # Place rect along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_rect(width=0.2, height=0.1, along=curve, t=0.5, align=True)
        """
        from ..entities.rect import Rect

        if style:
            fill = style.color
            stroke = style.stroke
            stroke_width = style.stroke_width
            z_index = style.z_index
            opacity = style.opacity
            fill_opacity = style.fill_opacity
            stroke_opacity = style.stroke_opacity

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)

        if along is not None:
            center_pos, rotation = self._resolve_along(along, t, align, rotation)
            center_rx, center_ry = 0.5, 0.5
        else:
            center_pos, at_rc = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)
            center_rx, center_ry = at_rc

        if width is None:
            width = 0.6
        if height is None:
            height = 0.6
        width_px = width * ref_w
        height_px = height * ref_h

        top_left_x = center_pos.x - width_px / 2
        top_left_y = center_pos.y - height_px / 2

        rect = Rect(
            top_left_x,
            top_left_y,
            width=width_px,
            height=height_px,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            rotation=rotation,
            opacity=opacity,
            z_index=z_index,
            fill_opacity=fill_opacity,
            stroke_opacity=stroke_opacity,
        )

        if along is None:
            rect.binding = Binding(
                at=RelCoord(center_rx - width / 2, center_ry - height / 2), reference=within
            )
        elif within is not None:
            rect.binding = Binding(reference=within)

        rect.relative_width = width
        rect.relative_height = height
        self._register_entity(rect)
        return rect

    def add_fill(
        self,
        *,
        color: str = "black",
        opacity: float = 1.0,
        z_index: int = 0,
        style: FillStyle | None = None,
    ) -> Rect:
        """
        Fill this surface with a rectangle.

        Args:
            color: Fill color
            opacity: Fill opacity (0.0 transparent to 1.0 opaque)
            z_index: Layer order
            style: FillStyle object

        Returns:
            The created Rect entity.

        Example:
            >>> cell.add_fill(color=cell.color)
            >>> cell.add_fill(color="blue", opacity=0.5)
        """
        from ..entities.rect import Rect

        if style:
            color = style.color
            opacity = style.opacity
            z_index = style.z_index

        rect = Rect(
            self._x,
            self._y,
            self._width,
            self._height,
            fill=color,
            stroke=None,
            opacity=opacity,
            z_index=z_index,
        )
        self._register_entity(rect)
        return rect

    def add_border(
        self,
        *,
        color: str = "#cccccc",
        width: float = 0.5,
        z_index: int = 0,
        opacity: float = 1.0,
        style: BorderStyle | None = None,
    ) -> Rect:
        """
        Add a border around this surface.

        Args:
            color: Stroke color
            width: Stroke width
            z_index: Layer order
            opacity: Opacity (0.0 transparent to 1.0 opaque)
            style: BorderStyle object

        Returns:
            The created Rect entity.

        Example:
            >>> cell.add_border(color=palette.grid)
        """
        from ..entities.rect import Rect

        if style:
            color = style.color
            width = style.width
            z_index = style.z_index
            opacity = style.opacity

        half = width / 2
        rect = Rect(
            self._x + half,
            self._y + half,
            self._width - width,
            self._height - width,
            fill=None,
            stroke=color,
            stroke_width=width,
            z_index=z_index,
            opacity=opacity,
        )
        self._register_entity(rect)
        return rect

    def add_point(
        self,
        *,
        at: Position = "center",
        within: Entity | None = None,
        along: Pathable | None = None,
        t: float | None = None,
        z_index: int = 0,
    ) -> Point:
        """
        Add an invisible point to this surface.

        Points render nothing — they exist purely as positional anchors.
        Use them as reactive Polygon vertices, connection endpoints, or
        reference positions for ``within=``.

        Args:
            at: Position ("center", "top_left", or (rx, ry) tuple)
            within: Size/position relative to another entity's bounds
            along: Path to position the point along
            t: Parameter on the path (0.0 to 1.0, default 0.5)
            z_index: Layer order

        Returns:
            The created Point entity.

        Examples:
            >>> p = cell.add_point(at=(0.25, 0.75))
            >>> p = cell.add_point(at="top_left")
            >>> # Reactive polygon vertex
            >>> a = cell.add_point(at=(0.5, 0.1))
            >>> b = cell.add_point(at=(0.9, 0.9))
            >>> c = cell.add_point(at=(0.1, 0.9))
            >>> tri = Polygon([a, b, c], fill="coral")
        """
        from ..entities.point import Point

        ref_x, ref_y, ref_w, ref_h = self._get_ref_frame(within)

        if along is not None:
            position, _ = self._resolve_along(along, t, False, 0)
            point = Point(position.x, position.y, z_index=z_index)
            point.binding = Binding(along=along, t=t if t is not None else 0.5, reference=within)
        else:
            position, at_rc = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)
            point = Point(position.x, position.y, z_index=z_index)
            point.binding = Binding(at=at_rc, reference=within)

        self._register_entity(point)
        return point

    # =========================================================================
    # ENTITY MANAGEMENT
    # =========================================================================

    def add(
        self,
        entity: Entity,
        at: Position = "center",
    ) -> Entity:
        """
        Add an existing entity to this surface with relative positioning.

        The entity is moved to the resolved ``at`` position.
        For creating and adding in one step, use add_dot(), add_line(), etc.

        Args:
            entity: The entity to add.
            at: Position - relative coords or named position.

        Returns:
            The added entity (for chaining).
        """
        ref_x, ref_y, ref_w, ref_h = self.ref_frame()
        position, at_rc = self._resolve_at(at, ref_x, ref_y, ref_w, ref_h)
        entity.position = position
        entity.binding = Binding(at=at_rc)
        self._register_entity(entity)
        return entity

    def place(self, entity: Entity) -> Entity:
        """
        Place an entity at its current absolute pixel position (escape hatch).

        Unlike ``add()``, this does NOT reposition the entity — it is
        registered exactly where it already is.

        Args:
            entity: The entity to place.

        Returns:
            The placed entity (for chaining).
        """
        self._register_entity(entity)
        return entity

    def remove(self, entity: Entity) -> bool:
        """Remove an entity from this surface."""
        if entity in self._entities:
            self._entities.remove(entity)
            entity.cell = None
            return True
        return False

    def clear(self) -> None:
        """Remove all entities from this surface."""
        for entity in self._entities:
            entity.cell = None
        self._entities.clear()
