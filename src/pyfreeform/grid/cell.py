"""Cell - A region in a grid that can contain entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ..core.entity import Entity
from ..core.surface import Surface, Position, NAMED_POSITIONS  # noqa: F401 — re-export

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
