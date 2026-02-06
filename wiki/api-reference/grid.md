
# Grid API Reference

The `Grid` class provides a 2D collection of `Cell` objects with convenient iteration and access patterns.

---

## Overview

Grids organize cells into rows and columns, providing:
- **Simple iteration**: `for cell in grid`
- **Index access**: `grid[row, col]`
- **Selection methods**: `grid.where()`, `grid.border()`, `grid.checkerboard()`
- **Neighbor relationships**: Automatic connection between adjacent cells

![Grid Structure](./_images/grid/example1-simple-iteration.svg)

---

## Class Definition

```python
class Grid:
    """2D grid of cells."""

    def __init__(
        self,
        rows: int,
        cols: int,
        cell_width: float,
        cell_height: float,
        x_offset: float = 0,
        y_offset: float = 0
    )
```

**Note**: Grids are typically created via `Scene.with_grid()` or `Scene.from_image()`.

---

## Properties

```python
grid.rows: int          # Number of rows
grid.cols: int          # Number of columns
grid.cell_width: float  # Width of each cell
grid.cell_height: float # Height of each cell
grid.width: float       # Total grid width
grid.height: float      # Total grid height
```

**Example**:
```python
print(f"Grid size: {grid.rows} rows × {grid.cols} cols")
print(f"Cell size: {grid.cell_width} × {grid.cell_height}")
print(f"Total dimensions: {grid.width} × {grid.height}")
```

---

## Iteration

### Simple Iteration

```python
for cell in grid:
    # Iterates left-to-right, top-to-bottom
    cell.add_dot(radius=3, color=cell.color)
```

![Simple Grid Iteration](./_images/grid/example1-simple-iteration.svg)

### Index Access

```python
# Get specific cell
cell = grid[0, 0]        # Top-left
cell = grid[5, 10]       # Row 5, column 10

# Negative indexing works
cell = grid[-1, -1]      # Bottom-right
```

![Index Access Example](./_images/grid/example2-index-access.svg)

### Row and Column Access

```python
# Get entire row
row_cells = grid.row(2)  # All cells in row 2

# Get entire column
col_cells = grid.column(5)  # All cells in column 5
```

**Example**:
```python
# Highlight first row
for cell in grid.row(0):
    cell.add_fill(color="yellow")

# Highlight last column
for cell in grid.column(-1):
    cell.add_border(color="red", width=2)
```

![Row Access Example](./_images/grid/example3-row-access.svg)

![Column Access Example](./_images/grid/example4-column-access.svg)

---

## Selection Methods

### where()

Filter cells by predicate function.

```python
def where(self, predicate: Callable[[Cell], bool]) -> list[Cell]
```

**Example**:
```python
# Bright cells only
bright_cells = grid.where(lambda c: c.brightness > 0.7)

for cell in bright_cells:
    cell.add_dot(radius=5, color="gold")
```

![Where Method Example](./_images/grid/example5-where.svg)

### border()

Get cells along the grid edges.

```python
def border(self) -> list[Cell]
```

**Example**:
```python
for cell in grid.border():
    cell.add_border(color="white", width=2)
```

![Border Example](./_images/grid/example6-border.svg)

### checkerboard()

Get cells in checkerboard pattern.

```python
def checkerboard(self, offset: int = 0) -> list[Cell]
```

**Parameters**:
- `offset`: 0 for one pattern, 1 for inverted

**Example**:
```python
# Create checkerboard fill
for cell in grid.checkerboard(offset=0):
    cell.add_fill(color="black")

for cell in grid.checkerboard(offset=1):
    cell.add_fill(color="white")
```

![Checkerboard Pattern](./_images/grid/example7-checkerboard.svg)

### corners()

Get the four corner cells.

```python
def corners() -> list[Cell]
```

**Example**:
```python
for cell in grid.corners():
    cell.add_polygon(shapes.star(5), fill="gold")
```

![Corners Example](./_images/grid/example8-corners.svg)

---

## Common Patterns

### Full Grid Iteration

```python
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(radius=5, color=cell.color)
```

### Row-by-Row Processing

```python
for row_idx in range(scene.grid.rows):
    for cell in scene.grid.row(row_idx):
        # Process each row separately
        pass
```

![Row-by-Row Example](./_images/grid/example9-row-by-row.svg)

### Conditional Selection

```python
# Only edges
for cell in scene.grid.border():
    cell.add_border(color="gold", width=2)

# Bright areas only
bright = scene.grid.where(lambda c: c.brightness > 0.7)
for cell in bright:
    cell.add_dot(radius=5, color="yellow")
```

### Checkerboard Patterns

```python
# Black squares
for cell in grid.checkerboard(offset=0):
    cell.add_fill(color="black")

# White squares
for cell in grid.checkerboard(offset=1):
    cell.add_fill(color="white")
```

### Neighbor-Based Patterns

```python
for cell in grid:
    dot1 = cell.add_dot(radius=3)

    # Connect to right neighbor
    if cell.right:
        dot2 = cell.right.add_dot(radius=3)
        Connection(start=dot1, end=dot2)

    # Connect to below neighbor
    if cell.below:
        dot2 = cell.below.add_dot(radius=3)
        Connection(start=dot1, end=dot2)
```

### Distance from Center

```python
center_row = grid.rows // 2
center_col = grid.cols // 2

for cell in grid:
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = (dr*dr + dc*dc) ** 0.5

    # Use distance for sizing, coloring, etc.
    radius = 2 + (10 - distance) * 0.5
    cell.add_dot(radius=max(1, radius))
```

![Distance Pattern Example](./_images/grid/example10-distance-pattern.svg)

![Grid Properties](./_images/grid/example11-properties.svg)

![Combined Selections Example](./_images/grid/example12-combined.svg)

---

## See Also

- 📖 [Cell API](cell.md) - Individual cell operations
- 📖 [Scene API](scene.md) - Grid creation methods
- 📖 [Grid Selections Guide](../advanced-concepts/06-grid-selections.md)
- 🎯 [Grid Patterns Example](../examples/beginner/grid-patterns.md)

