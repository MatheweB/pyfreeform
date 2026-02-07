"""Surface - Base class for any rectangular region that can contain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from .point import Point
from .entity import Entity
from .pathable import Pathable
from .tangent import get_angle_at

if TYPE_CHECKING:
    from ..entities.dot import Dot
    from ..entities.line import Line
    from ..entities.rect import Rect
    from ..entities.curve import Curve
    from ..entities.ellipse import Ellipse
    from ..entities.polygon import Polygon
    from ..entities.text import Text
    from ..config.styles import (
        DotStyle, LineStyle, FillStyle, BorderStyle,
        ShapeStyle, TextStyle,
    )


# Named positions within a surface (relative coordinates)
NAMED_POSITIONS: dict[str, tuple[float, float]] = {
    "center": (0.5, 0.5),
    "top_left": (0.0, 0.0),
    "top_right": (1.0, 0.0),
    "bottom_left": (0.0, 1.0),
    "bottom_right": (1.0, 1.0),
    "top": (0.5, 0.0),
    "bottom": (0.5, 1.0),
    "left": (0.0, 0.5),
    "right": (1.0, 0.5),
}

# Position type for method signatures
Position = tuple[float, float] | Literal[
    "center", "top_left", "top_right", "bottom_left", "bottom_right",
    "top", "bottom", "left", "right"
]


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
    def top_left(self) -> Point:
        """Top-left corner position."""
        return Point(self._x, self._y)

    @property
    def top_right(self) -> Point:
        """Top-right corner position."""
        return Point(self._x + self._width, self._y)

    @property
    def bottom_left(self) -> Point:
        """Bottom-left corner position."""
        return Point(self._x, self._y + self._height)

    @property
    def bottom_right(self) -> Point:
        """Bottom-right corner position."""
        return Point(self._x + self._width, self._y + self._height)

    @property
    def center(self) -> Point:
        """Center position."""
        return Point(
            self._x + self._width / 2,
            self._y + self._height / 2
        )

    def relative_to_absolute(self, pos: Position) -> Point:
        """
        Convert relative position to absolute pixels.

        Args:
            pos: Either a (rx, ry) tuple where 0-1 maps to surface bounds,
                a named position like "center", "top_left", etc.,
                or a Point (already absolute — passed through unchanged).

        Returns:
            Absolute pixel position as Point.
        """
        if isinstance(pos, Point):
            return pos

        if isinstance(pos, str):
            if pos not in NAMED_POSITIONS:
                raise ValueError(
                    f"Unknown position '{pos}'. "
                    f"Available: {list(NAMED_POSITIONS.keys())}"
                )
            pos = NAMED_POSITIONS[pos]

        rx, ry = pos
        return Point(
            self._x + rx * self._width,
            self._y + ry * self._height
        )

    def absolute_to_relative(self, point: Point) -> tuple[float, float]:
        """Convert absolute position to relative (0-1) coordinates."""
        rx = (point.x - self._x) / self._width if self._width > 0 else 0
        ry = (point.y - self._y) / self._height if self._height > 0 else 0
        return (rx, ry)

    def contains(self, point: Point) -> bool:
        """Check if a point is within this surface's bounds."""
        return (
            self._x <= point.x <= self._x + self._width and
            self._y <= point.y <= self._y + self._height
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
    ) -> tuple[Point, float]:
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

    # =========================================================================
    # BUILDER METHODS
    # =========================================================================

    def add_dot(
        self,
        *,
        at: Position = "center",
        along: Pathable | None = None,
        t: float | None = None,
        radius: float = 5,
        color: str = "black",
        z_index: int = 0,
        opacity: float = 1.0,
        style: DotStyle | None = None,
    ) -> Dot:
        """
        Add a dot to this surface.

        Position can be specified in three ways:
        1. `at`: Named position or relative coordinates
        2. `along` + `t`: Position along a path (t=0 is start, t=1 is end)
        3. Defaults to center

        Args:
            at: Position ("center", "top_left", or (rx, ry) tuple)
            along: Any Pathable object (Line, Curve, Ellipse, or custom path)
            t: Position along the path (0.0 to 1.0)
            radius: Dot radius in pixels
            color: Fill color
            z_index: Layer order (higher = on top)
            style: DotStyle object (overrides individual params)

        Returns:
            The created Dot entity.

        Examples:
            >>> cell.add_dot()  # Centered, default style
            >>> cell.add_dot(color="red", radius=6)
            >>> cell.add_dot(at="top_left")
            >>> cell.add_dot(at=(0.25, 0.75))  # 25% across, 75% down

            >>> # Works with any Pathable object
            >>> line = cell.add_diagonal()
            >>> cell.add_dot(along=line, t=cell.brightness)

            >>> curve = cell.add_curve()
            >>> cell.add_dot(along=curve, t=0.5)

            >>> ellipse = cell.add_ellipse(rx=15, ry=10)
            >>> cell.add_dot(along=ellipse, t=cell.brightness)
        """
        from ..entities.dot import Dot

        if style:
            radius = style.radius
            color = style.color
            z_index = style.z_index
            opacity = style.opacity

        if along is not None:
            position, _ = self._resolve_along(along, t, False, 0)
        else:
            position = self.relative_to_absolute(at)

        dot = Dot(position.x, position.y, radius=radius, color=color, z_index=z_index,
                  opacity=opacity)
        self._register_entity(dot)
        return dot

    def add_line(
        self,
        *,
        start: Position = "center",
        end: Position = "center",
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

        start_pos = self.relative_to_absolute(start)
        end_pos = self.relative_to_absolute(end)

        line = Line.from_points(
            start_pos, end_pos,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap, opacity=opacity,
        )

        if along is not None:
            target, rotation = self._resolve_along(along, t, align, 0)
            midpoint = line.anchor("center")
            line.move_by(target.x - midpoint.x, target.y - midpoint.y)
            if align:
                line.rotate(rotation, origin=target)

        self._register_entity(line)
        return line

    def add_diagonal(
        self,
        *,
        start: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "bottom_left",
        end: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "top_right",
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
            start=start, end=end, along=along, t=t, align=align,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap, opacity=opacity, style=style,
        )

    def add_curve(
        self,
        *,
        start: Position = "bottom_left",
        end: Position = "top_right",
        curvature: float = 0.5,
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
        Add a curved line to this surface.

        Curves are quadratic Bezier curves. The curvature parameter controls
        how much the curve bows away from a straight line.

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

        start_pos = self.relative_to_absolute(start)
        end_pos = self.relative_to_absolute(end)

        curve = Curve.from_points(
            start_pos, end_pos,
            curvature=curvature,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap, opacity=opacity,
        )

        if along is not None:
            target, rotation = self._resolve_along(along, t, align, 0)
            midpoint = curve.point_at(0.5)
            curve.move_by(target.x - midpoint.x, target.y - midpoint.y)
            if align:
                curve.rotate(rotation, origin=target)

        self._register_entity(curve)
        return curve

    def add_ellipse(
        self,
        *,
        at: Position = "center",
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
            rx: Horizontal radius (default: 40% of surface width)
            ry: Vertical radius (default: 40% of surface height)
            rotation: Rotation in degrees (counterclockwise)
            fill: Fill color (None for transparent)
            stroke: Stroke color (None for no stroke)
            stroke_width: Stroke width in pixels
            z_index: Layer order
            style: ShapeStyle object (overrides fill/stroke/stroke_width/z_index)

        Returns:
            The created Ellipse entity.

        Examples:
            >>> ellipse = cell.add_ellipse(rx=15, ry=10)
            >>> cell.add_dot(along=ellipse, t=cell.brightness)
            >>> # Place ellipse along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_ellipse(rx=5, ry=3, along=curve, t=0.5, align=True)
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

        if along is not None:
            position, rotation = self._resolve_along(along, t, align, rotation)
        else:
            position = self.relative_to_absolute(at)

        if rx is None:
            rx = self._width * 0.4
        if ry is None:
            ry = self._height * 0.4

        ellipse = Ellipse(
            position.x, position.y,
            rx=rx, ry=ry, rotation=rotation,
            fill=fill, stroke=stroke, stroke_width=stroke_width,
            z_index=z_index, opacity=opacity,
            fill_opacity=fill_opacity, stroke_opacity=stroke_opacity,
        )
        self._register_entity(ellipse)
        return ellipse

    def add_polygon(
        self,
        vertices: list[tuple[float, float]],
        *,
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
                        Use shape helpers like hexagon(), star() for common shapes.
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
            >>> from pyfreeform import shapes
            >>> cell.add_polygon(shapes.hexagon(), fill="purple")
            >>> # Place polygon along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_polygon(shapes.hexagon(), along=curve, t=0.5, align=True)
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

        absolute_vertices = [self.relative_to_absolute(v) for v in vertices]

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
            polygon.move_by(target.x - center.x, target.y - center.y)
            if effective_rotation != 0:
                polygon.rotate(effective_rotation, origin=target)
        elif rotation != 0:
            polygon.rotate(rotation)

        self._register_entity(polygon)
        return polygon

    def add_text(
        self,
        content: str,
        *,
        at: Position = "center",
        along: Pathable | None = None,
        t: float | None = None,
        align: bool = False,
        font_size: float | None = None,
        color: str = "black",
        font_family: str = "sans-serif",
        bold: bool = False,
        italic: bool = False,
        text_anchor: str = "left",
        baseline: str = "middle",
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
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
        along the path using SVG ``<textPath>`` (Phase 6).

        Args:
            content: The text string to display.
            at: Position ("center", "top_left", or (rx, ry) tuple).
            along: Path to position or warp text along.
            t: Parameter on the path (0.0 to 1.0). If omitted with
               ``along``, text warps along the full path.
            align: Rotate text to follow path tangent (only with ``t``).
            font_size: Font size in pixels. When omitted, auto-sizes to
                25% of the surface's smallest dimension. For textPath
                mode, auto-sizes to fill the path (bounded by 25%).
            color: Text color.
            font_family: Font family.
            bold: Bold text.
            italic: Italic text.
            text_anchor: Horizontal alignment: "start", "middle", "end".
            baseline: Vertical alignment: "auto", "middle", "hanging".
            rotation: Rotation in degrees around the text position.
            z_index: Layer order (higher = on top).
            start_offset: Where text begins on the path, 0.0–1.0
                (textPath mode only). Default 0.0 = start of path.
            end_offset: Where text ends on the path, 0.0–1.0
                (textPath mode only). Default 1.0 = end of path.
            style: TextStyle object (overrides individual params).

        Returns:
            The created Text entity.

        Examples:
            >>> cell.add_text("A")  # Centered letter
            >>> cell.add_text("Label", at="top", font_size=10)
            >>> # Position text along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_text("Hi", along=curve, t=0.5, align=True)
            >>> # Warp text along a curve (textPath)
            >>> cell.add_text("Hello World", along=curve)
            >>> # Warp along middle 60% of the path
            >>> cell.add_text("Partial", along=curve, start_offset=0.2, end_offset=0.8)
        """
        from ..entities.text import Text

        if style:
            if style.font_size != 16:
                font_size = style.font_size
            color = style.color
            font_family = style.font_family
            bold = style.bold
            italic = style.italic
            text_anchor = style.text_anchor
            baseline = style.baseline
            rotation = style.rotation
            z_index = style.z_index
            opacity = style.opacity

        # Resolve position
        is_textpath = along is not None and t is None
        if along is not None and t is not None:
            position, rotation = self._resolve_along(along, t, align, rotation)
        elif along is not None:
            # TextPath warp mode — position at path midpoint (used as fallback)
            position, rotation = self._resolve_along(along, 0.5, align, rotation)
        else:
            position = self.relative_to_absolute(at)

        # Compute the span fraction for textPath mode
        span = end_offset - start_offset

        # Auto-size font when not explicitly set
        if font_size is None:
            surface_bound = min(self._width, self._height)
            if is_textpath and hasattr(along, 'arc_length'):
                # Size to fill the spanned portion of the path
                arc_len = along.arc_length() * span
                chars = max(len(content), 1)
                font_size = arc_len / (chars * 0.6)
                # Bound by 25% of the surface
                font_size = min(font_size, surface_bound * 0.25)
            else:
                font_size = surface_bound * 0.25

        text = Text(
            position.x, position.y,
            content=content,
            font_size=font_size,
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

        # TextPath warp mode: along provided without t
        if is_textpath:
            if not hasattr(along, 'to_svg_path_d'):
                raise TypeError(
                    f"Text warping requires a path with to_svg_path_d(), "
                    f"but {type(along).__name__} does not have one."
                )
            import itertools
            _textpath_counter = getattr(self, '_textpath_counter', None)
            if _textpath_counter is None:
                _textpath_counter = itertools.count()
                self._textpath_counter = _textpath_counter
            path_id = f"textpath-{next(_textpath_counter)}"
            # Compute text_length from the spanned portion of the path
            text_length = None
            if hasattr(along, 'arc_length'):
                text_length = along.arc_length() * span
            svg_start_offset = f"{start_offset * 100:.1f}%"
            text.set_textpath(path_id, along.to_svg_path_d(),
                              start_offset=svg_start_offset,
                              text_length=text_length)

        self._register_entity(text)
        return text

    def add_rect(
        self,
        *,
        at: Position = "center",
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
            width: Rectangle width in pixels (default: 60% of surface width).
            height: Rectangle height in pixels (default: 60% of surface height).
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
            >>> rect = cell.add_rect(width=30, height=20, rotation=45)
            >>> # Place rect along a curve
            >>> curve = cell.add_curve()
            >>> cell.add_rect(width=10, height=5, along=curve, t=0.5, align=True)
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

        if along is not None:
            center_pos, rotation = self._resolve_along(along, t, align, rotation)
        else:
            center_pos = self.relative_to_absolute(at)

        if width is None:
            width = self._width * 0.6
        if height is None:
            height = self._height * 0.6

        top_left_x = center_pos.x - width / 2
        top_left_y = center_pos.y - height / 2

        rect = Rect(
            top_left_x, top_left_y,
            width=width, height=height,
            fill=fill, stroke=stroke, stroke_width=stroke_width,
            rotation=rotation, opacity=opacity, z_index=z_index,
            fill_opacity=fill_opacity, stroke_opacity=stroke_opacity,
        )
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
            self._x, self._y, self._width, self._height,
            fill=color, stroke=None, opacity=opacity, z_index=z_index
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

        rect = Rect(
            self._x, self._y, self._width, self._height,
            fill=None, stroke=color, stroke_width=width, z_index=z_index,
            opacity=opacity,
        )
        self._register_entity(rect)
        return rect

    # =========================================================================
    # ENTITY MANAGEMENT
    # =========================================================================

    def place(
        self,
        entity: Entity,
        at: Position = "center",
    ) -> Entity:
        """
        Place an existing entity in this surface.

        For creating and placing in one step, use add_dot(), add_line(), etc.

        Args:
            entity: The entity to place.
            at: Position - relative coords or named position.

        Returns:
            The placed entity (for chaining).
        """
        position = self.relative_to_absolute(at)
        entity.position = position
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
