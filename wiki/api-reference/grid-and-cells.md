# Grid & Cells

A `Grid` divides the scene into rows and columns of `Cell` objects. Each cell is a creative unit with image data, position helpers, and the full set of [builder methods](drawing.md).

!!! info "See also"
    For grid creation patterns, see [Scenes and Grids](../guide/01-scenes-and-grids.md). For cell usage, see [Working with Cells](../guide/02-working-with-cells.md).

---

## Grid Construction

| Constructor | Description |
|---|---|
| `Grid(cols, rows, cell_size=None, cell_width=None, cell_height=None)` | Manual grid |
| `Grid.from_image(image, cols=None, rows=None, cell_size=10, ...)` | Grid sized to image |

## Grid Properties

| Property | Type | Description |
|---|---|---|
| `grid.num_columns` | `int` | Number of columns |
| `grid.num_rows` | `int` | Number of rows |
| `grid.cell_width` | `float` | Cell width in pixels |
| `grid.cell_height` | `float` | Cell height in pixels |
| `grid.cell_size` | `(float, float)` | `(cell_width, cell_height)` tuple |
| `grid.pixel_width` | `float` | Total width = num_columns * cell_width |
| `grid.pixel_height` | `float` | Total height = num_rows * cell_height |
| `grid.origin` | `Coord` | Top-left corner position |
| `grid.source_image` | `Image \| None` | Original source image (if from_image) |

## Cell Access

| Operation | Description |
|---|---|
| `grid[row, col]` | Access by (row, col) index |
| `grid.get(row, col)` | Safe access -- returns `Cell` or `None` if out of bounds |
| `grid.cells` | All cells as a flat list (row by row, left to right) |
| `for cell in grid:` | Iterate row-by-row, left-to-right |
| `len(grid)` | Total number of cells |
| `grid.cell_at_pixel(x, y)` | Get cell at pixel position (or None) |

## Row & Column Access

| Method | Returns | Description |
|---|---|---|
| `grid.row(i)` | `list[Cell]` | All cells in row i |
| `grid.column(i)` | `list[Cell]` | All cells in column i |
| `grid.rows` | `Iterator[list[Cell]]` | Iterate over all rows |
| `grid.columns` | `Iterator[list[Cell]]` | Iterate over all columns |

## Region Selection

| Method | Returns | Description |
|---|---|---|
| `grid.region(row_start, row_end, col_start, col_end)` | `Iterator[Cell]` | Rectangular region |
| `grid.border(thickness=1)` | `Iterator[Cell]` | Cells on the grid border |

## Cell Merging (CellGroup)

| Method | Returns | Description |
|---|---|---|
| `grid.merge(start, end)` | `CellGroup` | Merge region into single surface. Both args are `(row, col)` tuples, both inclusive. Default: `start=(0, 0)`, `end=(num_rows-1, num_columns-1)`. Example: `merge((0, 0), (2, 2))` selects a 3x3 block. |
| `grid.merge_row(i)` | `CellGroup` | Merge full row |
| `grid.merge_col(i)` | `CellGroup` | Merge full column |

A `CellGroup` is a virtual surface -- it has all the same `add_*` builder methods as a Cell, and averaged data properties from its constituent cells.

## Pattern Selection

| Method | Description |
|---|---|
| `grid.every(n, offset=0)` | Every Nth cell (linear count) |
| `grid.checkerboard("black" \| "white")` | Checkerboard pattern |
| `grid.where(predicate)` | Filter by lambda: `grid.where(lambda c: c.brightness > 0.5)` |
| `grid.diagonal(direction="down", offset=0)` | Main or offset diagonals |

## Data Loading

```python
grid.load_layer(name, source, mode="value")
```

Modes: `"value"` (raw), `"normalized"` (0-1), `"hex"` (color string). Normally handled automatically by `Scene.from_image()`.

---

## The Cell

`Cell` extends Surface -- it inherits all 12 [builder methods](drawing.md) plus has image data, position helpers, and neighbor access.

### Typed Data Properties (from loaded image)

| Property | Type | Default | Description |
|---|---|---|---|
| `cell.brightness` | `float` | `0.5` | 0.0 (black) to 1.0 (white) |
| `cell.color` | `str` | `"#808080"` | Hex color string |
| `cell.rgb` | `(int, int, int)` | `(128, 128, 128)` | RGB tuple (0-255 each) |
| `cell.alpha` | `float` | `1.0` | 0.0 (transparent) to 1.0 (opaque) |
| `cell.data` | `dict` | `{}` | Raw data dict for custom layers |

### Position Properties (inherited from Surface)

| Property | Type | Description |
|---|---|---|
| `cell.x`, `cell.y` | `float` | Top-left corner |
| `cell.width`, `cell.height` | `float` | Cell dimensions |
| `cell.bounds` | `(x, y, w, h)` | Bounding tuple |
| `cell.center` | `Coord` | Center position |
| `cell.top_left` | `Coord` | Top-left corner |
| `cell.top_right` | `Coord` | Top-right corner |
| `cell.bottom_left` | `Coord` | Bottom-left corner |
| `cell.bottom_right` | `Coord` | Bottom-right corner |

### Grid Position

| Property | Type | Description |
|---|---|---|
| `cell.row` | `int` | Row index (0-based) |
| `cell.col` | `int` | Column index (0-based) |
| `cell.grid` | `Grid` | Parent grid |
| `cell.normalized_position` | `RelCoord` | `RelCoord(rx, ry)` normalized to 0.0-1.0 within grid |

### Neighbors

| Property | Returns | Direction |
|---|---|---|
| `cell.above` | `Cell \| None` | North |
| `cell.below` | `Cell \| None` | South |
| `cell.left` | `Cell \| None` | West |
| `cell.right` | `Cell \| None` | East |
| `cell.above_left` | `Cell \| None` | Northwest |
| `cell.above_right` | `Cell \| None` | Northeast |
| `cell.below_left` | `Cell \| None` | Southwest |
| `cell.below_right` | `Cell \| None` | Southeast |
| `cell.neighbors` | `dict[str, Cell \| None]` | 4 cardinal directions |
| `cell.neighbors_all` | `dict[str, Cell \| None]` | All 8 directions |

!!! warning "Neighbor properties return Cells, not positions"
    `cell.left`, `cell.right`, `cell.above`, `cell.below` return `Cell | None`, **not** position coordinates. Use `cell.center`, `cell.top_left`, etc. for positions.

### Sub-Cell Image Sampling

For finer-grained access to the original source image within a cell's area:

| Method | Returns | Description |
|---|---|---|
| `cell.sample_image(rx, ry)` | `(int, int, int)` | RGB at relative position within cell |
| `cell.sample_brightness(rx, ry)` | `float` | Brightness at relative position |
| `cell.sample_hex(rx, ry)` | `str` | Hex color at relative position |

Where `rx` and `ry` are 0.0-1.0 within the cell (0.5, 0.5 = center).

### Utility

| Method | Returns | Description |
|---|---|---|
| `cell.distance_to(other)` | `float` | Pixel distance to Cell, Coord, or tuple |
