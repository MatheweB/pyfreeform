"""CellGroup - A virtual surface spanning multiple grid cells."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..core.entity import Entity
from ..core.surface import Surface

if TYPE_CHECKING:
    from .cell import Cell
    from .grid import Grid


class CellGroup(Surface):
    """
    A virtual surface spanning multiple grid cells.

    CellGroup acts like a single large cell with merged bounds.
    It inherits all builder methods from Surface (add_dot, add_line,
    add_curve, etc.) and provides averaged data properties.

    Created via grid.merge(), not directly:

        >>> group = scene.grid.merge((0, 0), (0, 4))
        >>> group.add_fill(color=group.color)
        >>> group.add_text("Title", font_size=20)

    Attributes:
        brightness: Average brightness across constituent cells
        color: Average color across constituent cells
        rgb: Average RGB across constituent cells
        cells: The constituent Cell objects
    """

    def __init__(self, cells: list[Cell], grid: Grid) -> None:
        """
        Create a CellGroup from a list of cells.

        Typically called by Grid.merge(), not directly.

        Args:
            cells: The cells to merge into this group.
            grid: The parent grid.
        """
        if not cells:
            raise ValueError("CellGroup requires at least one cell")

        self._cells = cells
        self._grid = grid

        # Compute merged bounding box
        self._x = min(c.x for c in cells)
        self._y = min(c.y for c in cells)
        max_x = max(c.x + c.width for c in cells)
        max_y = max(c.y + c.height for c in cells)
        self._width = max_x - self._x
        self._height = max_y - self._y

        self._entities: list[Entity] = []

    # =========================================================================
    # AVERAGED DATA PROPERTIES
    # =========================================================================

    @property
    def brightness(self) -> float:
        """Average brightness across all constituent cells."""
        return sum(c.brightness for c in self._cells) / len(self._cells)

    @property
    def color(self) -> str:
        """Average color across all constituent cells as hex string."""
        r, g, b = self.rgb
        return f"#{r:02x}{g:02x}{b:02x}"

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Average RGB across all constituent cells."""
        n = len(self._cells)
        total_r = sum(c.rgb[0] for c in self._cells)
        total_g = sum(c.rgb[1] for c in self._cells)
        total_b = sum(c.rgb[2] for c in self._cells)
        return (round(total_r / n), round(total_g / n), round(total_b / n))

    @property
    def alpha(self) -> float:
        """Average alpha across all constituent cells."""
        return sum(c.alpha for c in self._cells) / len(self._cells)

    # =========================================================================
    # ACCESS
    # =========================================================================

    @property
    def cells(self) -> list[Cell]:
        """The constituent cells in this group."""
        return list(self._cells)

    @property
    def grid(self) -> Grid:
        """The parent grid."""
        return self._grid

    def __repr__(self) -> str:
        n = len(self._cells)
        return (
            f"CellGroup({n} cells, "
            f"{self._width:.0f}x{self._height:.0f}, "
            f"brightness={self.brightness:.2f})"
        )
