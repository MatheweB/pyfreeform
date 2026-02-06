"""Cell - A region in a grid that can contain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..core.point import Point
from ..core.entity import Entity
from ..core.pathable import Pathable

if TYPE_CHECKING:
    from .grid import Grid
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


# Named positions within a cell
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


class Cell:
    """
    A cell within a grid - the fundamental unit for placing art elements.
    
    Cells provide:
    - **Typed data access**: `cell.brightness`, `cell.color` instead of dict lookups
    - **Builder methods**: `cell.add_dot()`, `cell.add_line()` for easy element creation
    - **Position helpers**: Named positions like "center", "top_left", etc.
    - **Neighbor access**: `cell.right`, `cell.below` for cross-cell operations
    
    Basic usage:
        >>> for cell in scene.grid:
        ...     # Typed access to image data
        ...     if cell.brightness > 0.5:
        ...         cell.add_dot(color=cell.color)
    
    Builder methods:
        >>> cell.add_dot(radius=4, color="red")
        >>> cell.add_line(start="top_left", end="bottom_right")
        >>> cell.add_diagonal(direction="up")  # SW to NE
        >>> cell.add_fill(color="blue")
        >>> cell.add_border(color="gray")
    
    Attributes:
        row: Row index (0-based)
        col: Column index (0-based)
        brightness: Normalized brightness 0.0-1.0 (from loaded image)
        color: Hex color string (from loaded image)
        rgb: RGB tuple (0-255 each)
        alpha: Transparency 0.0-1.0
    """
    
    def __init__(
        self,
        grid: Grid,
        row: int,
        col: int,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> None:
        """
        Create a cell (typically called by Grid, not directly).
        
        Args:
            grid: The parent grid.
            row: Row index.
            col: Column index.
            x, y: Top-left corner in pixels.
            width, height: Cell dimensions in pixels.
        """
        self._grid = grid
        self._row = row
        self._col = col
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._entities: list[Entity] = []
        self._data: dict[str, Any] = {}
    
    # =========================================================================
    # TYPED DATA PROPERTIES
    # These replace cell.data["key"] with cell.property
    # =========================================================================
    
    @property
    def brightness(self) -> float:
        """
        Normalized brightness from 0.0 (black) to 1.0 (white).
        
        Calculated from loaded image data. Returns 0.5 if no image loaded.
        
        Example:
            >>> t = cell.brightness  # Use directly for positioning
            >>> dot_pos = line.point_at(t)
        """
        raw = self._data.get("brightness")
        if raw is None:
            return 0.5
        # Normalize to 0-1 if stored as 0-255
        if isinstance(raw, (int, float)) and raw > 1:
            return float(raw) / 255.0
        return float(raw)
    
    @property
    def color(self) -> str:
        """
        Hex color string from loaded image (e.g., "#ff5733").
        
        Returns "#808080" (gray) if no image loaded.
        
        Example:
            >>> cell.add_dot(color=cell.color)
        """
        return self._data.get("color", "#808080")
    
    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        RGB color as tuple of integers (0-255 each).
        
        Returns (128, 128, 128) if no image loaded.
        
        Example:
            >>> r, g, b = cell.rgb
            >>> is_reddish = r > g and r > b
        """
        stored = self._data.get("rgb")
        if stored is not None:
            return stored
        # Try to derive from hex color
        hex_color = self._data.get("color")
        if hex_color and hex_color.startswith("#") and len(hex_color) == 7:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b)
        return (128, 128, 128)
    
    @property
    def alpha(self) -> float:
        """
        Transparency from 0.0 (transparent) to 1.0 (opaque).
        
        Returns 1.0 if no alpha data loaded.
        """
        raw = self._data.get("alpha")
        if raw is None:
            return 1.0
        if isinstance(raw, (int, float)) and raw > 1:
            return float(raw) / 255.0
        return float(raw)
    
    @property
    def data(self) -> dict[str, Any]:
        """
        Raw data dictionary (for custom data or backwards compatibility).
        
        Prefer typed properties (brightness, color, etc.) for standard data.
        """
        return self._data
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    
    @property
    def grid(self) -> Grid:
        """The parent grid."""
        return self._grid
    
    @property
    def row(self) -> int:
        """Row index (0-based)."""
        return self._row
    
    @property
    def col(self) -> int:
        """Column index (0-based)."""
        return self._col
    
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
        """Cell width in pixels."""
        return self._width
    
    @property
    def height(self) -> float:
        """Cell height in pixels."""
        return self._height
    
    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """Bounds as (x, y, width, height)."""
        return (self._x, self._y, self._width, self._height)
    
    @property
    def entities(self) -> list[Entity]:
        """Entities placed in this cell."""
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
            pos: Either a (rx, ry) tuple where 0-1 maps to cell bounds,
                 or a named position like "center", "top_left", etc.
        
        Returns:
            Absolute pixel position as Point.
        """
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
        """Check if a point is within this cell's bounds."""
        return (
            self._x <= point.x <= self._x + self._width and
            self._y <= point.y <= self._y + self._height
        )
    
    # =========================================================================
    # BUILDER METHODS
    # Convenient ways to add entities to this cell
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
        style: DotStyle | None = None,
    ) -> Dot:
        """
        Add a dot to this cell.

        Position can be specified in three ways:
        1. `at`: Named position or relative coordinates within cell
        2. `along` + `t`: Position along a path (t=0 is start, t=1 is end)
        3. Defaults to cell center

        Args:
            at: Position within cell ("center", "top_left", or (rx, ry) tuple)
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
        
        # Apply style if provided
        if style:
            radius = style.radius
            color = style.color
            z_index = style.z_index
        
        # Determine position
        if along is not None and t is not None:
            position = along.point_at(t)
        else:
            position = self.relative_to_absolute(at)
        
        dot = Dot(position.x, position.y, radius=radius, color=color, z_index=z_index)
        dot.cell = self
        self._entities.append(dot)
        return dot
    
    def add_line(
        self,
        *,
        start: Position = "center",
        end: Position = "center",
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        style: LineStyle | None = None,
    ) -> Line:
        """
        Add a line to this cell.

        Args:
            start: Starting position within cell
            end: Ending position within cell
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
        """
        from ..entities.line import Line

        if style:
            width = style.width
            color = style.color
            z_index = style.z_index
            cap = style.cap
            start_cap = style.start_cap
            end_cap = style.end_cap

        start_pos = self.relative_to_absolute(start)
        end_pos = self.relative_to_absolute(end)

        line = Line.from_points(
            start_pos, end_pos,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap,
        )
        line.cell = self
        self._entities.append(line)
        return line
    
    def add_diagonal(
        self,
        *,
        start: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "bottom_left",
        end: Literal["top_left", "top_right", "bottom_left", "bottom_right"] = "top_right",
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        style: LineStyle | None = None,
    ) -> Line:
        """
        Add a diagonal line across this cell.

        This is a convenience method that delegates to add_line() with corner positions.
        For maximum clarity, you can also use add_line(start=..., end=...) directly.

        Args:
            start: Starting corner (default: "bottom_left")
            end: Ending corner (default: "top_right")
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
            start=start, end=end,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap, style=style,
        )

    def add_curve(
        self,
        *,
        start: Position = "bottom_left",
        end: Position = "top_right",
        curvature: float = 0.5,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        style: LineStyle | None = None,
    ) -> Curve:
        """
        Add a curved line to this cell.

        Curves are quadratic Bezier curves. The curvature parameter controls
        how much the curve bows away from a straight line.

        The key feature: use `along=curve, t=value` with add_dot() to position
        dots along the curve, just like with lines!

        Args:
            start: Starting position within cell
            end: Ending position within cell
            curvature: How much the curve bows (-1 to 1, 0 = straight)
                       Positive = bows left, Negative = bows right
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

        start_pos = self.relative_to_absolute(start)
        end_pos = self.relative_to_absolute(end)

        curve = Curve.from_points(
            start_pos, end_pos,
            curvature=curvature,
            width=width, color=color, z_index=z_index, cap=cap,
            start_cap=start_cap, end_cap=end_cap,
        )
        curve.cell = self
        self._entities.append(curve)
        return curve

    def add_ellipse(
        self,
        *,
        at: Position = "center",
        rx: float | None = None,
        ry: float | None = None,
        rotation: float = 0,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        style: ShapeStyle | None = None,
    ) -> Ellipse:
        """
        Add an ellipse to this cell.

        Ellipses support parametric positioning just like lines and curves.
        Use `cell.add_dot(along=ellipse, t=...)` to position dots around
        the ellipse perimeter.

        Args:
            at: Position within cell (center of ellipse)
            rx: Horizontal radius (default: 40% of cell width)
            ry: Vertical radius (default: 40% of cell height)
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

            >>> # Rotated ellipse
            >>> ellipse = cell.add_ellipse(rx=20, ry=10, rotation=45, fill="coral")

            >>> # Using ShapeStyle
            >>> style = ShapeStyle(color="coral", stroke="navy", stroke_width=2)
            >>> ellipse = cell.add_ellipse(style=style)
        """
        from ..entities.ellipse import Ellipse

        if style:
            fill = style.color
            stroke = style.stroke
            stroke_width = style.stroke_width
            z_index = style.z_index

        position = self.relative_to_absolute(at)

        # Auto-scale to cell if not specified
        if rx is None:
            rx = self._width * 0.4
        if ry is None:
            ry = self._height * 0.4

        ellipse = Ellipse(
            position.x, position.y,
            rx=rx, ry=ry, rotation=rotation,
            fill=fill, stroke=stroke, stroke_width=stroke_width,
            z_index=z_index,
        )
        ellipse.cell = self
        self._entities.append(ellipse)
        return ellipse

    def add_polygon(
        self,
        vertices: list[tuple[float, float]],
        *,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        rotation: float = 0,
        style: ShapeStyle | None = None,
    ) -> Polygon:
        """
        Add a polygon to this cell.

        Vertices are specified in relative coordinates (0-1), where
        (0,0) is top-left and (1,1) is bottom-right of the cell.

        Args:
            vertices: List of (x, y) tuples in relative coordinates.
                      Use shape helpers like hexagon(), star() for common shapes.
            fill: Fill color (None for transparent)
            stroke: Stroke color (None for no stroke)
            stroke_width: Stroke width in pixels
            z_index: Layer order
            rotation: Rotation in degrees (around polygon center)
            style: ShapeStyle object (overrides fill/stroke/stroke_width/z_index)

        Returns:
            The created Polygon entity.

        Examples:
            >>> # Custom triangle
            >>> cell.add_polygon([(0.5, 0.1), (0.9, 0.9), (0.1, 0.9)], fill="red")

            >>> # Using shape helpers
            >>> from pyfreeform import shapes
            >>> cell.add_polygon(shapes.hexagon(), fill="purple")
            >>> cell.add_polygon(shapes.star(points=6), fill="gold")
        """
        from ..entities.polygon import Polygon

        if style:
            fill = style.color
            stroke = style.stroke
            stroke_width = style.stroke_width
            z_index = style.z_index

        # Convert relative vertices to absolute
        absolute_vertices = [self.relative_to_absolute(v) for v in vertices]

        polygon = Polygon(
            absolute_vertices,
            fill=fill,
            stroke=stroke,
            stroke_width=stroke_width,
            z_index=z_index,
        )

        if rotation != 0:
            polygon.rotate(rotation)

        polygon.cell = self
        self._entities.append(polygon)
        return polygon
    
    def add_text(
        self,
        content: str,
        *,
        at: Position = "center",
        font_size: float | None = None,
        color: str = "black",
        font_family: str = "sans-serif",
        bold: bool = False,
        italic: bool = False,
        text_anchor: str = "middle",
        baseline: str = "middle",
        rotation: float = 0,
        z_index: int = 0,
        style: TextStyle | None = None,
    ) -> Text:
        """
        Add text to this cell.

        Args:
            content: The text string to display.
            at: Position within cell ("center", "top_left", or (rx, ry) tuple).
            font_size: Font size in pixels (default: cell height * 0.6).
            color: Text color.
            font_family: Font family - "serif", "sans-serif", "monospace",
                        or a specific font name.
            bold: Bold text.
            italic: Italic text.
            text_anchor: Horizontal alignment: "start" (left), "middle", "end" (right).
            baseline: Vertical alignment: "auto", "middle", "hanging" (top).
            rotation: Rotation in degrees around the text position.
            z_index: Layer order (higher = on top).
            style: TextStyle object (overrides individual params).

        Returns:
            The created Text entity.

        Examples:
            >>> cell.add_text("A")  # Centered letter
            >>> cell.add_text("Label", at="top", font_size=10)
            >>> cell.add_text("42", font_family="monospace", color="lime")
            >>> cell.add_text("Bold!", bold=True)
        """
        from ..entities.text import Text

        if style:
            if style.font_size != 16:  # Only override if explicitly set (non-default)
                font_size = style.font_size
            color = style.color
            font_family = style.font_family
            bold = style.bold
            italic = style.italic
            text_anchor = style.text_anchor
            baseline = style.baseline
            rotation = style.rotation
            z_index = style.z_index

        position = self.relative_to_absolute(at)

        # Default font size based on cell height
        if font_size is None:
            font_size = self._height * 0.6

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
        )
        text.cell = self
        self._entities.append(text)
        return text
    
    def add_fill(
        self,
        *,
        color: str = "black",
        opacity: float = 1.0,
        z_index: int = 0,
        style: FillStyle | None = None,
    ) -> Rect:
        """
        Fill this cell with a rectangle.

        Args:
            color: Fill color
            opacity: Fill opacity (0.0 transparent to 1.0 opaque)
            z_index: Layer order
            style: FillStyle object

        Returns:
            The created Rect entity.

        Example:
            >>> cell.add_fill(color=cell.color)  # Fill with image color
            >>> cell.add_fill(color="blue", opacity=0.5)  # Semi-transparent
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
        rect.cell = self
        self._entities.append(rect)
        return rect
    
    def add_border(
        self,
        *,
        color: str = "#cccccc",
        width: float = 0.5,
        z_index: int = 0,
        style: BorderStyle | None = None,
    ) -> Rect:
        """
        Add a border around this cell.
        
        Args:
            color: Stroke color
            width: Stroke width
            z_index: Layer order
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
        
        rect = Rect(
            self._x, self._y, self._width, self._height,
            fill=None, stroke=color, stroke_width=width, z_index=z_index
        )
        rect.cell = self
        self._entities.append(rect)
        return rect
    
    # =========================================================================
    # ENTITY PLACEMENT (Original API)
    # =========================================================================
    
    def place(
        self,
        entity: Entity,
        at: Position = "center",
    ) -> Entity:
        """
        Place an existing entity in this cell.
        
        For creating and placing in one step, use add_dot(), add_line(), etc.
        
        Args:
            entity: The entity to place.
            at: Position within cell - relative coords or named position.
        
        Returns:
            The placed entity (for chaining).
        """
        position = self.relative_to_absolute(at)
        entity.position = position
        entity.cell = self
        self._entities.append(entity)
        return entity
    
    def remove(self, entity: Entity) -> bool:
        """Remove an entity from this cell."""
        if entity in self._entities:
            self._entities.remove(entity)
            entity.cell = None
            return True
        return False
    
    def clear(self) -> None:
        """Remove all entities from this cell."""
        for entity in self._entities:
            entity.cell = None
        self._entities.clear()
    
    # =========================================================================
    # NEIGHBORS
    # =========================================================================
    
    @property
    def above(self) -> Cell | None:
        """Cell above this one (north), or None if at edge."""
        if self._row > 0:
            return self._grid[self._row - 1, self._col]
        return None
    
    @property
    def below(self) -> Cell | None:
        """Cell below this one (south), or None if at edge."""
        if self._row < self._grid.rows - 1:
            return self._grid[self._row + 1, self._col]
        return None
    
    @property
    def left(self) -> Cell | None:
        """Cell to the left (west), or None if at edge."""
        if self._col > 0:
            return self._grid[self._row, self._col - 1]
        return None
    
    @property
    def right(self) -> Cell | None:
        """Cell to the right (east), or None if at edge."""
        if self._col < self._grid.cols - 1:
            return self._grid[self._row, self._col + 1]
        return None

    @property
    def above_left(self) -> Cell | None:
        """Cell diagonally above-left (northwest), or None if at edge."""
        if self._row > 0 and self._col > 0:
            return self._grid[self._row - 1, self._col - 1]
        return None

    @property
    def above_right(self) -> Cell | None:
        """Cell diagonally above-right (northeast), or None if at edge."""
        if self._row > 0 and self._col < self._grid.cols - 1:
            return self._grid[self._row - 1, self._col + 1]
        return None

    @property
    def below_left(self) -> Cell | None:
        """Cell diagonally below-left (southwest), or None if at edge."""
        if self._row < self._grid.rows - 1 and self._col > 0:
            return self._grid[self._row + 1, self._col - 1]
        return None

    @property
    def below_right(self) -> Cell | None:
        """Cell diagonally below-right (southeast), or None if at edge."""
        if self._row < self._grid.rows - 1 and self._col < self._grid.cols - 1:
            return self._grid[self._row + 1, self._col + 1]
        return None

    @property
    def neighbors(self) -> dict[str, Cell | None]:
        """All neighbors as a dict (cardinal directions only)."""
        return {
            "above": self.above,
            "below": self.below,
            "left": self.left,
            "right": self.right,
        }

    @property
    def neighbors_all(self) -> dict[str, Cell | None]:
        """All 8 neighbors including diagonals."""
        return {
            "above": self.above,
            "below": self.below,
            "left": self.left,
            "right": self.right,
            "above_left": self.above_left,
            "above_right": self.above_right,
            "below_left": self.below_left,
            "below_right": self.below_right,
        }
    
    def __repr__(self) -> str:
        return f"Cell(row={self._row}, col={self._col}, brightness={self.brightness:.2f})"
