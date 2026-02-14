"""Cell - A region in a grid that can contain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..core.coord import Coord
from ..core.relcoord import RelCoord
from ..core.entity import Entity
from ..core.surface import Surface

if TYPE_CHECKING:
    from .grid import Grid


class Cell(Surface):
    """
    A cell within a grid - the fundamental unit for placing art elements.

    Cells provide:
    - **Typed data access**: `cell.brightness`, `cell.color` instead of dict lookups
    - **Builder methods**: `cell.add_dot()`, `cell.add_line()` for easy element creation
        (inherited from Surface)
    - **Position helpers**: Named positions like "center", "top_left", etc.
        (inherited from Surface)
    - **Neighbor access**: `cell.right`, `cell.below` for cross-cell operations

    Basic usage:
        ```python
        for cell in scene.grid:
            # Typed access to image data
            if cell.brightness > 0.5:
                cell.add_dot(color=cell.color)
        ```

    Builder methods:
        ```python
        cell.add_dot(radius=0.4, color="red")
        cell.add_line(start="top_left", end="bottom_right")
        cell.add_diagonal(direction="up")  # SW to NE
        cell.add_fill(color="blue")
        cell.add_border(color="gray")
        ```

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
            x: Top-left corner x in pixels.
            y: Top-left corner y in pixels.
            width: Cell width in pixels.
            height: Cell height in pixels.
        """
        self._grid = grid
        self._row = row
        self._col = col
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._entities: list[Entity] = []
        self._connections: set = set()
        self._data: dict[str, Any] = {}

    # =========================================================================
    # TYPED DATA PROPERTIES
    # These replace cell.data["key"] with cell.property
    # =========================================================================

    @property
    def brightness(self) -> float:
        """
        Area-averaged brightness from 0.0 (black) to 1.0 (white).

        Derived from the LANCZOS-resampled image (one pixel per cell),
        so each value represents the weighted average of all source pixels
        that fall within this cell's region. This smooths harsh transitions
        — e.g. a cell straddling a black/white border reads ~0.5.

        For single-pixel sampling without averaging, use ``sample_brightness()``.

        Returns 0.5 if no image is loaded.

        Example:
            ```python
            cell.add_dot(radius=0.02 + 0.08 * cell.brightness)
            ```
        """
        raw = self._data.get("brightness")
        return float(raw) if raw is not None else 0.5

    @property
    def color(self) -> str:
        """
        Area-averaged hex color from the resampled image (e.g., "#ff5733").

        Derived from the LANCZOS-resampled image (one pixel per cell),
        so it represents the blended color of all source pixels in this
        cell's region. Borders between contrasting colors will blend.

        For single-pixel sampling without averaging, use ``sample_hex()``.

        Returns "#808080" (gray) if no image is loaded.

        Example:
            ```python
            cell.add_dot(color=cell.color)
            ```
        """
        return self._data.get("color", "#808080")

    @property
    def rgb(self) -> tuple[int, int, int]:
        """
        Area-averaged RGB color as a tuple of integers (0-255 each).

        Derived from the LANCZOS-resampled image (one pixel per cell).
        Each channel is the weighted average of source pixels in this
        cell's region.

        For single-pixel sampling without averaging, use ``sample_image()``.

        Returns (128, 128, 128) if no image is loaded.

        Example:
            ```python
            r, g, b = cell.rgb
            is_reddish = r > g and r > b
            ```
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
        Area-averaged transparency from 0.0 (transparent) to 1.0 (opaque).

        Derived from the LANCZOS-resampled image (one pixel per cell),
        so it represents the blended alpha of all source pixels in this
        cell's region.

        Returns 1.0 if no alpha data is loaded.
        """
        raw = self._data.get("alpha")
        return float(raw) if raw is not None else 1.0

    @property
    def data(self) -> dict[str, Any]:
        """
        Raw data dictionary (for custom data or backwards compatibility).

        Prefer typed properties (brightness, color, etc.) for standard data.
        """
        return self._data

    # =========================================================================
    # BASIC PROPERTIES (Cell-specific; position/bounds from Surface)
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
        if self._row < self._grid.num_rows - 1:
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
        if self._col < self._grid.num_columns - 1:
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
        if self._row > 0 and self._col < self._grid.num_columns - 1:
            return self._grid[self._row - 1, self._col + 1]
        return None

    @property
    def below_left(self) -> Cell | None:
        """Cell diagonally below-left (southwest), or None if at edge."""
        if self._row < self._grid.num_rows - 1 and self._col > 0:
            return self._grid[self._row + 1, self._col - 1]
        return None

    @property
    def below_right(self) -> Cell | None:
        """Cell diagonally below-right (southeast), or None if at edge."""
        if self._row < self._grid.num_rows - 1 and self._col < self._grid.num_columns - 1:
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

    # =========================================================================
    # QOL METHODS
    # =========================================================================

    def distance_to(self, other: Cell | Entity | Coord | tuple[float, float]) -> float:
        """
        Euclidean pixel distance from this cell's center to another position.

        Accepts: Cell (uses center), Coord, or (x, y) tuple.
        Entity positions work too — just pass entity.anchor("center") or
        entity.position.

        Args:
            other: A Cell, Coord, or (x, y) tuple.

        Returns:
            Distance in pixels.
        """

        if isinstance(other, Cell):
            target = other.center
        elif isinstance(other, Coord):
            target = other
        elif isinstance(other, Entity):
            target = Coord(other.x, other.y)
        elif isinstance(other, tuple):
            target = Coord(*other)
        else:
            raise TypeError(f"Expected Cell, Coord, Entity, or tuple, got {type(other).__name__}")
        return self.center.distance_to(target)

    @property
    def normalized_position(self) -> RelCoord:
        """
        (col, row) normalized to 0.0-1.0 within the grid.

        Useful for position-based gradients and effects.

        Returns:
            RelCoord(rx, ry) where both are in [0.0, 1.0].
        """
        cols = self._grid.num_columns
        rows = self._grid.num_rows
        nx = self._col / (cols - 1) if cols > 1 else 0.0
        ny = self._row / (rows - 1) if rows > 1 else 0.0
        return RelCoord(nx, ny)

    # =========================================================================
    # SUB-CELL IMAGE SAMPLING
    # =========================================================================

    def sample_image(self, rx: float = 0.5, ry: float = 0.5) -> tuple[int, int, int]:
        """
        Read a single pixel from the original source image (no averaging).

        Unlike ``rgb`` (which comes from the resampled, area-averaged image),
        this reads one pixel at full resolution. This preserves sharp edges
        — a cell on a black/white border returns pure black or pure white
        depending on where the sample point falls.

        Args:
            rx: Horizontal position within cell (0.0 = left edge, 1.0 = right edge).
            ry: Vertical position within cell (0.0 = top edge, 1.0 = bottom edge).

        Returns:
            RGB tuple (0-255 each).

        Raises:
            ValueError: If the grid was not created from an image.
        """
        image = self._grid.source_image
        if image is None:
            raise ValueError("Grid was not created from an image — no source image to sample")
        px = int(min(max(0, (self._col + rx) * image.width / self._grid.num_columns), image.width - 1))
        py = int(min(max(0, (self._row + ry) * image.height / self._grid.num_rows), image.height - 1))
        return image.rgb_at(px, py)

    def sample_brightness(self, rx: float = 0.5, ry: float = 0.5) -> float:
        """
        Read brightness of a single pixel from the original source image.

        Unlike ``brightness`` (which is area-averaged from the resampled image),
        this reads one pixel at full resolution. Useful for images with sharp
        transitions where averaging would produce unwanted intermediate values.

        Args:
            rx: Horizontal position within cell (0.0 = left edge, 1.0 = right edge).
            ry: Vertical position within cell (0.0 = top edge, 1.0 = bottom edge).

        Returns:
            Brightness value 0.0 (black) to 1.0 (white).
        """
        r, g, b = self.sample_image(rx, ry)
        return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

    def sample_hex(self, rx: float = 0.5, ry: float = 0.5) -> str:
        """
        Read hex color of a single pixel from the original source image.

        Unlike ``color`` (which is area-averaged from the resampled image),
        this reads one pixel at full resolution.

        Args:
            rx: Horizontal position within cell (0.0 = left edge, 1.0 = right edge).
            ry: Vertical position within cell (0.0 = top edge, 1.0 = bottom edge).

        Returns:
            Hex color string (e.g., "#ff5733").
        """
        r, g, b = self.sample_image(rx, ry)
        return f"#{r:02x}{g:02x}{b:02x}"

    def __repr__(self) -> str:
        return f"Cell(row={self._row}, col={self._col}, brightness={self.brightness:.2f})"
