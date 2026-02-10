"""Grid - A structured grid of cells for organizing entities."""

from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, Callable

from ..core.coord import Coord
from .cell import Cell
from .cell_group import CellGroup

if TYPE_CHECKING:
    from ..image import Image, Layer


class Grid:
    """
    A grid of cells that provides structure for placing entities.
    
    Grids divide space into cells, making it easy to create patterns,
    load image data, and organize entities spatially.
    
    Attributes:
        rows: Number of rows
        cols: Number of columns
        cell_width: Width of each cell in pixels
        cell_height: Height of each cell in pixels
        pixel_width: Total width in pixels
        pixel_height: Total height in pixels
    
    Examples:
        >>> grid = Grid(cols=20, rows=20, cell_size=10)
        >>> cell = grid[5, 10]  # Access by [row, col]
        >>> cell.add(Dot(color="red"))
        
        >>> # Load image data into cells
        >>> grid.load_layer("brightness", image["brightness"])
        >>> for cell in grid:
        ...     brightness = cell.data["brightness"]
    """
    
    def __init__(
        self,
        cols: int,
        rows: int,
        cell_size: float | None = None,
        cell_width: float | None = None,
        cell_height: float | None = None,
        origin: tuple[float, float] = (0, 0),
    ) -> None:
        """
        Create a grid.
        
        Args:
            cols: Number of columns.
            rows: Number of rows.
            cell_size: Size for square cells (sets both width and height).
            cell_width: Cell width (overrides cell_size).
            cell_height: Cell height (overrides cell_size).
            origin: Top-left corner of the grid in pixels.
        """
        if cell_size is None and cell_width is None and cell_height is None:
            raise ValueError("Must specify cell_size or cell_width/cell_height")
        
        self._cols = cols
        self._rows = rows
        self._cell_width = cell_width or cell_size or 10
        self._cell_height = cell_height or cell_size or 10
        self._origin = Coord(*origin)
        self._source_image: Image | None = None

        # Create cells
        self._cells: list[list[Cell]] = []
        self._cell_groups: list[CellGroup] = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                x = self._origin.x + col * self._cell_width
                y = self._origin.y + row * self._cell_height
                cell = Cell(
                    grid=self,
                    row=row,
                    col=col,
                    x=x,
                    y=y,
                    width=self._cell_width,
                    height=self._cell_height,
                )
                row_cells.append(cell)
            self._cells.append(row_cells)
    
    @classmethod
    def from_image(
        cls,
        image: Image,
        cols: int | None = None,
        rows: int | None = None,
        cell_size: float = 10,
        cell_ratio: float = 1.0,
        cell_width: float | None = None,
        cell_height: float | None = None,
        origin: tuple[float, float] = (0, 0),
        load_layers: bool = True,
    ) -> Grid:
        """
        Create a grid sized to match an image.

        Args:
            image: Source image (will be resized to match grid).
            cols: Number of columns (calculates rows from aspect ratio).
                  If None and rows is also None, derives both from image
                  dimensions and cell size (fit-grid-to-image mode).
            rows: Number of rows (calculates cols from aspect ratio).
            cell_size: Base size of each cell in pixels.
            cell_ratio: Width-to-height ratio (e.g., 2.0 for domino cells).
            cell_width: Explicit cell width (overrides cell_size and cell_ratio).
            cell_height: Explicit cell height (overrides cell_size).
            origin: Top-left corner of the grid.
            load_layers: Whether to load image data into cells.

        Returns:
            A new Grid with image data loaded into cells.
        """
        # Resolve cell dimensions
        if cell_width is not None or cell_height is not None:
            cw = float(cell_width or cell_size)
            ch = float(cell_height or cell_size)
        elif cell_ratio != 1.0:
            cw = cell_size * cell_ratio
            ch = float(cell_size)
        else:
            cw = float(cell_size)
            ch = float(cell_size)

        # Calculate grid dimensions from image aspect ratio
        if cols is not None and rows is not None:
            pass  # Use both as provided
        elif cols is not None:
            aspect = image.height / image.width
            rows = max(1, int(cols * aspect))
        elif rows is not None:
            aspect = image.width / image.height
            cols = max(1, int(rows * aspect))
        else:
            # Fit grid to image: derive cols/rows from image dimensions
            cols = max(1, round(image.width / cw))
            rows = max(1, round(image.height / ch))

        # Create grid
        grid = cls(
            cols=cols,
            rows=rows,
            cell_width=cw,
            cell_height=ch,
            origin=origin,
        )
        
        # Load image data
        if load_layers:
            # Resize image to match grid dimensions
            resized = image.resize(cols, rows)
            
            # Load standard layers
            grid.load_layer("color", resized, mode="hex")
            grid.load_layer("brightness", resized["brightness"], mode="normalized")
            if resized.has_alpha:
                grid.load_layer("alpha", resized["alpha"], mode="normalized")

        # Store source image reference for sub-cell sampling
        grid._source_image = image

        return grid
    
    # --- Properties ---
    
    @property
    def cols(self) -> int:
        """Number of columns."""
        return self._cols
    
    @property
    def rows(self) -> int:
        """Number of rows."""
        return self._rows
    
    @property
    def cell_width(self) -> float:
        """Width of each cell in pixels."""
        return self._cell_width
    
    @property
    def cell_height(self) -> float:
        """Height of each cell in pixels."""
        return self._cell_height
    
    @property
    def cell_size(self) -> tuple[float, float]:
        """Cell size as (width, height)."""
        return (self._cell_width, self._cell_height)
    
    @property
    def pixel_width(self) -> float:
        """Total width in pixels."""
        return self._cols * self._cell_width
    
    @property
    def pixel_height(self) -> float:
        """Total height in pixels."""
        return self._rows * self._cell_height
    
    @property
    def origin(self) -> Coord:
        """Top-left corner of the grid."""
        return self._origin

    @property
    def source_image(self) -> Image | None:
        """The original source image (if created via from_image), or None."""
        return self._source_image
    
    # --- Cell access ---
    
    def __getitem__(self, key: tuple[int, int]) -> Cell:
        """
        Access cell by (row, col) index.
        
        Args:
            key: Tuple of (row, col).
        
        Returns:
            The Cell at that position.
        
        Raises:
            IndexError: If row or col is out of bounds.
        """
        row, col = key
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError(
                f"Cell ({row}, {col}) out of bounds for "
                f"grid of size {self._rows}x{self._cols}"
            )
        return self._cells[row][col]
    
    def __iter__(self) -> Iterator[Cell]:
        """Iterate over all cells (row by row, left to right)."""
        for row in self._cells:
            for cell in row:
                yield cell
    
    def __len__(self) -> int:
        """Total number of cells."""
        return self._rows * self._cols
    
    def cell_at(self, x: float, y: float) -> Cell | None:
        """
        Get the cell containing a pixel position.
        
        Args:
            x, y: Pixel coordinates.
        
        Returns:
            The Cell at that position, or None if outside grid.
        """
        # Calculate cell indices
        col = int((x - self._origin.x) / self._cell_width)
        row = int((y - self._origin.y) / self._cell_height)
        
        if 0 <= row < self._rows and 0 <= col < self._cols:
            return self._cells[row][col]
        return None
    
    # --- Layer data ---
    
    def load_layer(
        self,
        name: str,
        source: Layer | Image,
        mode: str = "value",
    ) -> None:
        """
        Load layer data from an image or layer into cell data.
        
        Args:
            name: Key to store data under in cell.data.
            source: A Layer or Image to sample from.
            mode: How to store values:
                  "value" - Store raw numeric value
                  "normalized" - Store value / 255 (0-1 range)
                  "hex" - Store hex color string (requires Image source)
        """
        # Handle Image source
        from ..image import Image as ImageClass, Layer as LayerClass
        
        if isinstance(source, ImageClass):
            image = source
            # Resize to match grid if needed
            if image.width != self._cols or image.height != self._rows:
                image = image.resize(self._cols, self._rows)
            
            for row in range(self._rows):
                for col in range(self._cols):
                    cell = self._cells[row][col]
                    if mode == "hex":
                        cell.data[name] = image.hex_at(col, row)
                    elif mode == "normalized":
                        r, g, b = image.rgb_at(col, row)
                        cell.data[name] = (r + g + b) / (3 * 255)
                    else:
                        cell.data[name] = image.rgb_at(col, row)
        
        elif isinstance(source, LayerClass):
            layer = source
            # Sample layer at each cell position
            for row in range(self._rows):
                for col in range(self._cols):
                    # Map grid coords to layer coords
                    lx = int(col * layer.width / self._cols)
                    ly = int(row * layer.height / self._rows)
                    lx = min(lx, layer.width - 1)
                    ly = min(ly, layer.height - 1)
                    
                    value = layer[lx, ly]
                    cell = self._cells[row][col]
                    
                    if mode == "normalized":
                        cell.data[name] = value / 255.0
                    else:
                        cell.data[name] = value
        
        else:
            raise TypeError(f"Expected Layer or Image, got {type(source)}")
    
    # --- Utility methods ---
    
    def all_entities(self) -> list:
        """Get all entities in all cells and cell groups."""
        entities = []
        for cell in self:
            entities.extend(cell.entities)
        for group in self._cell_groups:
            entities.extend(group.entities)
        return entities

    def clear(self) -> None:
        """Clear all entities from all cells and cell groups."""
        for cell in self:
            cell.clear()
        for group in self._cell_groups:
            group.clear()
        self._cell_groups.clear()
    
    # =========================================================================
    # ROW AND COLUMN ACCESS
    # =========================================================================
    
    def row(self, index: int) -> list[Cell]:
        """
        Get all cells in a specific row.
        
        Args:
            index: Row index (0-based).
        
        Returns:
            List of cells in that row (left to right).
        
        Example:
            >>> for cell in grid.row(0):  # Top row
            ...     cell.add_dot(color="red")
        """
        if not 0 <= index < self._rows:
            raise IndexError(f"Row {index} out of bounds (0-{self._rows - 1})")
        return list(self._cells[index])
    
    def column(self, index: int) -> list[Cell]:
        """
        Get all cells in a specific column.
        
        Args:
            index: Column index (0-based).
        
        Returns:
            List of cells in that column (top to bottom).
        
        Example:
            >>> for cell in grid.column(0):  # Left column
            ...     cell.add_dot(color="blue")
        """
        if not 0 <= index < self._cols:
            raise IndexError(f"Column {index} out of bounds (0-{self._cols - 1})")
        return [self._cells[row][index] for row in range(self._rows)]
    
    @property
    def all_rows(self) -> Iterator[list[Cell]]:
        """
        Iterate over all rows (as lists of cells).
        
        Example:
            >>> for row_idx, row in enumerate(grid.all_rows):
            ...     for cell in row:
            ...         cell.add_dot(color="red" if row_idx % 2 == 0 else "blue")
        """
        for row in self._cells:
            yield list(row)
    
    @property
    def all_columns(self) -> Iterator[list[Cell]]:
        """
        Iterate over all columns (as lists of cells).
        
        Example:
            >>> for col_idx, col in enumerate(grid.all_columns):
            ...     for cell in col:
            ...         cell.add_dot(radius=0.02 * (col_idx + 1))
        """
        for col in range(self._cols):
            yield [self._cells[row][col] for row in range(self._rows)]
    
    # =========================================================================
    # REGION SELECTION
    # =========================================================================
    
    def region(
        self,
        row_start: int = 0,
        row_end: int | None = None,
        col_start: int = 0,
        col_end: int | None = None,
    ) -> Iterator[Cell]:
        """
        Iterate over cells in a rectangular region.
        
        Args:
            row_start: Starting row (inclusive, default 0).
            row_end: Ending row (exclusive, default all rows).
            col_start: Starting column (inclusive, default 0).
            col_end: Ending column (exclusive, default all columns).
        
        Yields:
            Cells in the region (row by row).
        
        Example:
            >>> # Top-left quarter
            >>> for cell in grid.region(row_end=grid.rows//2, col_end=grid.cols//2):
            ...     cell.add_fill(color="blue")
        """
        if row_end is None:
            row_end = self._rows
        if col_end is None:
            col_end = self._cols
        
        row_start = max(0, row_start)
        row_end = min(self._rows, row_end)
        col_start = max(0, col_start)
        col_end = min(self._cols, col_end)
        
        for row in range(row_start, row_end):
            for col in range(col_start, col_end):
                yield self._cells[row][col]
    
    def border(self, thickness: int = 1) -> Iterator[Cell]:
        """
        Iterate over cells on the grid border.
        
        Args:
            thickness: Border thickness in cells (default 1).
        
        Yields:
            Cells on the border.
        
        Example:
            >>> for cell in grid.border():
            ...     cell.add_fill(color="gray")
        """
        for cell in self:
            r, c = cell.row, cell.col
            on_border = (
                r < thickness or  # Top edge
                r >= self._rows - thickness or  # Bottom edge
                c < thickness or  # Left edge
                c >= self._cols - thickness  # Right edge
            )
            if on_border:
                yield cell
    
    # =========================================================================
    # CELL MERGING
    # =========================================================================

    def merge(
        self,
        start: tuple[int, int] = (0, 0),
        end: tuple[int, int] | None = None,
    ) -> CellGroup:
        """
        Merge a rectangular region of cells into a single virtual surface.

        The returned CellGroup acts like a single large cell — it has all
        the same builder methods (add_dot, add_line, add_curve, etc.) and
        averaged data properties (brightness, color, rgb).

        Both corners are **inclusive** — ``merge((0, 0), (2, 2))`` selects
        a 3×3 block (rows 0-2, cols 0-2).

        Args:
            start: Top-left corner as ``(row, col)``, inclusive. Default ``(0, 0)``.
            end: Bottom-right corner as ``(row, col)``, inclusive.
                 Default ``(rows-1, cols-1)`` (entire grid).

        Returns:
            A CellGroup spanning the selected region.

        Examples:
            >>> header = grid.merge((0, 0), (1, grid.cols - 1))
            >>> header.add_fill(color="#333")
            >>> header.add_text("Title", font_size=16, color="white")

            >>> single = grid.merge((3, 3), (3, 3))  # one cell
            >>> block = grid.merge((0, 0), (2, 2))    # 3×3 block
        """
        if end is None:
            end = (self._rows - 1, self._cols - 1)

        row_start, col_start = start
        row_end, col_end = end

        # Convert inclusive end to exclusive end for region()
        cells = list(self.region(row_start, row_end + 1, col_start, col_end + 1))
        if not cells:
            raise ValueError(
                f"No cells in region start={start}, end={end}"
            )
        group = CellGroup(cells, grid=self)
        self._cell_groups.append(group)
        return group

    def merge_row(self, index: int) -> CellGroup:
        """
        Merge an entire row into a single virtual surface.

        Args:
            index: Row index (0-based).

        Returns:
            A CellGroup spanning the full row.

        Example:
            >>> top = grid.merge_row(0)
            >>> top.add_fill(color="navy")
            >>> top.add_text("Header", font_size=14, color="white")
        """
        return self.merge((index, 0), (index, self._cols - 1))

    def merge_col(self, index: int) -> CellGroup:
        """
        Merge an entire column into a single virtual surface.

        Args:
            index: Column index (0-based).

        Returns:
            A CellGroup spanning the full column.

        Example:
            >>> sidebar = grid.merge_col(0)
            >>> sidebar.add_fill(color="gray")
        """
        return self.merge((0, index), (self._rows - 1, index))

    # =========================================================================
    # PATTERN SELECTION
    # =========================================================================
    
    def every(self, n: int, offset: int = 0) -> Iterator[Cell]:
        """
        Iterate over every Nth cell.
        
        Cells are numbered left-to-right, top-to-bottom.
        
        Args:
            n: Select every Nth cell.
            offset: Starting offset (default 0).
        
        Yields:
            Every Nth cell.
        
        Example:
            >>> # Checkerboard pattern (every 2nd cell)
            >>> for cell in grid.every(2):
            ...     cell.add_fill(color="black")
        """
        for i, cell in enumerate(self):
            if (i - offset) % n == 0:
                yield cell
    
    def checkerboard(self, color: str = "black") -> Iterator[Cell]:
        """
        Iterate over checkerboard pattern cells.
        
        Args:
            color: "black" for dark squares, "white" for light squares.
        
        Yields:
            Cells in the checkerboard pattern.
        
        Example:
            >>> for cell in grid.checkerboard("black"):
            ...     cell.add_fill(color="#333")
        """
        target_parity = 0 if color == "black" else 1
        for cell in self:
            if (cell.row + cell.col) % 2 == target_parity:
                yield cell
    
    def where(self, predicate: Callable[[Cell], bool]) -> Iterator[Cell]:
        """
        Iterate over cells matching a condition.
        
        Args:
            predicate: Function that takes a Cell and returns True/False.
        
        Yields:
            Cells where predicate returns True.
        
        Examples:
            >>> # Bright cells
            >>> for cell in grid.where(lambda c: c.brightness > 0.7):
            ...     cell.add_dot(radius=0.3)
            
            >>> # Top half
            >>> for cell in grid.where(lambda c: c.row < grid.rows // 2):
            ...     cell.add_fill(color="blue")
        """
        for cell in self:
            if predicate(cell):
                yield cell
    
    def diagonal(self, direction: str = "down", offset: int = 0) -> Iterator[Cell]:
        """
        Iterate over cells on a diagonal.
        
        Args:
            direction: "down" for top-left to bottom-right,
                      "up" for bottom-left to top-right.
            offset: Diagonal offset (0 = main diagonal).
        
        Yields:
            Cells on the diagonal.
        
        Example:
            >>> for cell in grid.diagonal():
            ...     cell.add_dot(color="red")
        """
        if direction == "down":
            # Top-left to bottom-right
            for i in range(max(self._rows, self._cols)):
                r, c = i, i + offset
                if 0 <= r < self._rows and 0 <= c < self._cols:
                    yield self._cells[r][c]
        else:
            # Bottom-left to top-right
            for i in range(max(self._rows, self._cols)):
                r, c = self._rows - 1 - i, i + offset
                if 0 <= r < self._rows and 0 <= c < self._cols:
                    yield self._cells[r][c]
    
    def __repr__(self) -> str:
        return (
            f"Grid({self._cols}x{self._rows}, "
            f"cell_size=({self._cell_width}, {self._cell_height}))"
        )
