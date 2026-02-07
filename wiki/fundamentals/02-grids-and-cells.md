
# Grids and Cells

Grids provide spatial organization for your artwork by dividing the canvas into cells. Think of grids like graph paper - each cell is a coordinate unit you can work with.

---

## Understanding Grids

A **Grid** is a 2D array of cells that organizes your canvas:

```
Grid (20 columns × 15 rows = 300 cells)
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│0│1│2│3│4│5│6│7│8│9│ ... each cell
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ ... can hold
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ ... entities and
├─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │ │ │ │ ... data
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘
```

---

## Why Use Grids?

Grids provide several powerful features:

### 1. Organization
Structured layout for systematic artwork

### 2. Image Mapping
Load image data into cells automatically

### 3. Easy Iteration
Simple loops over cells in patterns

### 4. Neighbor Access
Built-in access to adjacent cells

### 5. Position Helpers
Named positions within each cell

---

## Creating Grids

Grids are usually created automatically:

### Via Scene.from_image()

```python
scene = Scene.from_image("photo.jpg", grid_size=40)
grid = scene.grid  # Automatically created
```

![Grid created from image](./_images/02-grids-and-cells/create-via-from-image.svg)

### Via Scene.with_grid()

```python
scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
grid = scene.grid  # Automatically created
```

![Grid created with grid method](./_images/02-grids-and-cells/create-via-with-grid.svg)

### Manual Creation (Advanced)

```python
from pyfreeform import Grid

grid = Grid(
    cols=25,
    rows=20,
    cell_size=15,
    origin=(0, 0)  # Top-left corner
)
```

![Manually created grid](./_images/02-grids-and-cells/create-manual-grid.svg)

---

## Grid Properties

```python
# Dimensions
grid.cols          # Number of columns
grid.rows          # Number of rows

# Cell sizing
grid.cell_width    # Width of each cell (pixels)
grid.cell_height   # Height of each cell (pixels)
grid.cell_size     # Tuple: (width, height)

# Total dimensions
grid.pixel_width   # Total width (cols × cell_width)
grid.pixel_height  # Total height (rows × cell_height)

# Position
grid.origin        # Point at top-left corner

# Access
len(grid)          # Total cell count (cols × rows)
```

---

## Rectangle Cells

By default, cells are square (`cell_width == cell_height`). You can create rectangular cells for different artistic effects:

### Using cell_ratio

The simplest approach — multiply the base `cell_size` width:

```python
# Wide "domino" cells (2:1 ratio)
scene = Scene.from_image("photo.jpg", grid_size=40, cell_ratio=2.0)
# cell_width = 20, cell_height = 10 (with cell_size=10)

# Tall cells (0.5:1 ratio)
scene = Scene.from_image("photo.jpg", grid_size=40, cell_ratio=0.5)
# cell_width = 5, cell_height = 10
```

### Using explicit dimensions

For precise control:

```python
# Explicit cell width and height
scene = Scene.with_grid(cols=20, rows=30, cell_width=15, cell_height=8)

# Or mix with cell_size (cell_height defaults to cell_size)
scene = Scene.with_grid(cols=20, rows=30, cell_size=10, cell_width=20)
# cell_width = 20, cell_height = 10
```

### Priority rules

1. `cell_width` / `cell_height` (highest — explicit override)
2. `cell_ratio` (multiplies `cell_size` for width)
3. `cell_size` (base square size, default 10)

---

## Accessing Cells

### By Index

```python
# Access specific cell [row, col]
cell = grid[10, 5]  # Row 10, Column 5

# First cell (top-left)
cell = grid[0, 0]

# Last cell (bottom-right)
cell = grid[grid.rows - 1, grid.cols - 1]
```

![Accessing cells by index](./_images/02-grids-and-cells/access-by-index.svg)

Indices are zero-based: rows go from `0` to `rows-1`, columns from `0` to `cols-1`.

### Iteration

```python
# Iterate all cells (row by row, left to right)
for cell in grid:
    cell.add_dot(radius=3)

# With position info
for cell in grid:
    print(f"Cell at row {cell.row}, col {cell.col}")
```

![Iterating over cells](./_images/02-grids-and-cells/access-iteration.svg)

### Flat Access

```python
# Get all cells as flat list
cells = grid.cells  # List of all cells in row-major order
```

---

## Understanding Cells

A **Cell** is an individual unit in the grid. It's both a container and a workspace.

### Cell Coordinate System

Each cell has its own coordinate space:

```
Cell (20×20 pixels)
(0,0) top_left ──────── top (0.5, 0) ──────── top_right (1,0)
       │                                              │
       │                                              │
left   │              center (0.5, 0.5)              │ right
(0,0.5)│                                              │ (1,0.5)
       │                                              │
       │                                              │
(0,1)  ──────── bottom (0.5, 1) ──────── bottom_right (1,1)
   bottom_left
```

---

## Cell Properties

### Position in Grid

```python
cell.row    # Row index (0 to rows-1)
cell.col    # Column index (0 to cols-1)
cell.grid   # Reference to parent grid
```

### Physical Dimensions

```python
cell.x         # Top-left x coordinate (pixels)
cell.y         # Top-left y coordinate (pixels)
cell.width     # Cell width (pixels)
cell.height    # Cell height (pixels)
cell.bounds    # Tuple: (x, y, width, height)
```

### Position Helpers (as Points)

```python
cell.center         # Point at center
cell.top_left       # Point at top-left corner
cell.top_right      # Point at top-right corner
cell.bottom_left    # Point at bottom-left corner
cell.bottom_right   # Point at bottom-right corner
```

![Cell position helpers](./_images/02-grids-and-cells/cell-position-helpers.svg)

These return `Point` objects you can use for positioning.

### Image Data (When Loaded)

```python
cell.brightness  # 0.0 to 1.0 (normalized)
cell.color       # Hex string "#rrggbb"
cell.rgb         # Tuple (r, g, b)
cell.alpha       # Transparency 0.0 to 1.0
```

Only available if grid was created from an image.

### Sub-Cell Image Sampling

When a grid is created from an image, you can sample the original image at any position within a cell — not just the center:

```python
# grid.source_image gives access to the original image
grid.source_image  # Image object or None

# Sample at a relative position within the cell
cell.sample_image(rx=0.5, ry=0.5)       # → (r, g, b) tuple at center
cell.sample_brightness(rx=0.0, ry=0.0)  # → float at top-left corner
cell.sample_hex(rx=1.0, ry=1.0)         # → "#rrggbb" at bottom-right
```

The `rx`/`ry` parameters use relative coordinates: `0.0` = left/top edge, `1.0` = right/bottom edge. Default is `0.5, 0.5` (center).

**Use cases:**

```python
for cell in scene.grid:
    # Sample 4 corners for a gradient effect
    tl = cell.sample_hex(0.0, 0.0)  # Top-left color
    tr = cell.sample_hex(1.0, 0.0)  # Top-right color
    bl = cell.sample_hex(0.0, 1.0)  # Bottom-left color
    br = cell.sample_hex(1.0, 1.0)  # Bottom-right color

    # Place dots at corners with sampled colors
    cell.add_dot(at="top_left", radius=3, color=tl)
    cell.add_dot(at="top_right", radius=3, color=tr)
    cell.add_dot(at="bottom_left", radius=3, color=bl)
    cell.add_dot(at="bottom_right", radius=3, color=br)
```

### Neighbor Access

```python
cell.above        # Cell above (None if edge)
cell.below        # Cell below (None if edge)
cell.left         # Cell to the left (None if edge)
cell.right        # Cell to the right (None if edge)

# Diagonals
cell.above_left   # Cell diagonally up-left
cell.above_right  # Cell diagonally up-right
cell.below_left   # Cell diagonally down-left
cell.below_right  # Cell diagonally down-right
```

![Cell neighbor access](./_images/02-grids-and-cells/cell-neighbors.svg)

Always check for `None` before using:

```python
if cell.right:
    cell.right.add_dot(color="red")
```

### Custom Data

```python
cell.data  # Dictionary for custom data

# Set custom values
cell.data["my_value"] = 42
cell.data["category"] = "important"

# Read later
if cell.data.get("category") == "important":
    cell.add_dot(color="gold")
```

### QoL Methods

#### distance_to

Calculate the pixel distance from this cell's center to another position:

```python
# Distance to another cell
d = cell.distance_to(other_cell)

# Distance to a Point or tuple
d = cell.distance_to(Point(100, 200))
d = cell.distance_to((100, 200))
```

Useful for radial effects:

```python
center_cell = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]

for cell in scene.grid:
    d = cell.distance_to(center_cell)
    radius = max(1, 8 - d * 0.05)
    cell.add_dot(radius=radius, color="coral")
```

#### normalized_position

Get the cell's position as `(nx, ny)` normalized to 0.0–1.0:

```python
nx, ny = cell.normalized_position
# (0.0, 0.0) = top-left cell
# (1.0, 1.0) = bottom-right cell
# (0.5, 0.5) = center cell
```

Useful for position-based gradients and effects:

```python
for cell in scene.grid:
    nx, ny = cell.normalized_position
    # Diagonal gradient
    brightness = (nx + ny) / 2
    gray = int(brightness * 255)
    cell.add_fill(color=f"rgb({gray},{gray},{gray})")
```

---

## Cell Builder Methods

Cells provide convenient methods to add entities:

### Dots

```python
cell.add_dot(
    at="center",           # Or (rx, ry) relative coords
    radius=5,
    color="red",
    z_index=0,
    style=None             # Or DotStyle object
)

# Position along a path
cell.add_dot(
    along=line_or_curve,
    t=0.5,                # Parameter 0-1
    radius=3
)
```

### Lines

```python
cell.add_line(
    start="top_left",      # Named or (rx, ry)
    end="bottom_right",
    width=1,
    color="black",
    style=None
)

# Diagonals
cell.add_diagonal(start="top_left", end="bottom_right")  # or start="bottom_left", end="top_right"
```

### Curves

```python
cell.add_curve(
    start="bottom_left",
    end="top_right",
    curvature=0.5,        # -1 to 1
    width=1,
    color="black"
)
```

### Shapes

```python
# Fill entire cell
cell.add_fill(
    color="black",
    z_index=0
)

# Border around cell
cell.add_border(
    color="#cccccc",
    width=0.5
)

cell.add_ellipse(
    at="center",
    rx=10,
    ry=8,
    rotation=0,
    fill="coral"
)

cell.add_polygon(
    vertices,             # List of (x, y) tuples
    fill="purple",
    stroke=None
)
```

### Text

```python
cell.add_text(
    content="Hello",
    at="center",
    font_size=14,
    color="black",
    font_family="sans-serif"
)
```

### Styling

```python
cell.add_fill(color="lightgray")
cell.add_border(color="black", width=1)
```

---

## Named Positions

When adding entities, you can use named positions:

```python
# These are equivalent
cell.add_dot(at="center")
cell.add_dot(at=(0.5, 0.5))

# Available names
positions = [
    "center",        # (0.5, 0.5)
    "top_left",      # (0, 0)
    "top_right",     # (1, 0)
    "bottom_left",   # (0, 1)
    "bottom_right",  # (1, 1)
    "top",           # (0.5, 0)
    "bottom",        # (0.5, 1)
    "left",          # (0, 0.5)
    "right",         # (1, 0.5)
]
```

![Cell named positions](./_images/02-grids-and-cells/cell-named-positions.svg)

Or use relative coordinates (0-1 range):

```python
cell.add_dot(at=(0.25, 0.75))  # 25% from left, 75% from top
cell.add_dot(at=(0.8, 0.2))    # 80% from left, 20% from top
```

---

## Grid Iteration Patterns

### Basic Iteration

```python
for cell in grid:
    cell.add_dot(color="red")
```

![Basic iteration pattern](./_images/02-grids-and-cells/pattern-basic-iteration.svg)

### With Position Logic

```python
for cell in grid:
    # Center cross pattern
    if cell.row == grid.rows // 2 or cell.col == grid.cols // 2:
        cell.add_dot(color="blue", radius=5)
```

![Position logic pattern](./_images/02-grids-and-cells/pattern-position-logic.svg)

### Using Neighbors

```python
for cell in grid:
    # Draw only if neighbor is bright
    if cell.right and cell.right.brightness > 0.7:
        cell.add_line(start="right", end="right", color="white")
```

![Using neighbors pattern](./_images/02-grids-and-cells/pattern-using-neighbors.svg)

### Edge Detection

```python
for cell in grid:
    # Detect if on edge
    is_edge = (
        cell.row == 0 or
        cell.row == grid.rows - 1 or
        cell.col == 0 or
        cell.col == grid.cols - 1
    )

    if is_edge:
        cell.add_border(color="black", width=2)
```

![Edge detection pattern](./_images/02-grids-and-cells/pattern-edge-detection.svg)

---

## Grid Selection Methods

Grids provide powerful selection methods for creating patterns:

### Rows and Columns

```python
# Specific row
for cell in grid.row(0):          # Top row
    cell.add_fill(color="red")

# Specific column
for cell in grid.column(5):       # 6th column
    cell.add_fill(color="blue")
```

| Specific Row | Specific Column |
|--------------|-----------------|
| ![Selecting a specific row](./_images/02-grids-and-cells/selection-specific-row.svg) | ![Selecting a specific column](./_images/02-grids-and-cells/selection-specific-column.svg) |

### Patterns

```python
# Checkerboard
for cell in grid.checkerboard("black"):  # or "white"
    cell.add_fill(color="gray")

# Border
for cell in grid.border(thickness=2):
    cell.add_border(color="black", width=1)

# Every nth cell
for cell in grid.every(n=3):     # Every 3rd cell
    cell.add_dot(color="gold", radius=5)
```

| Checkerboard | Border | Every Nth |
|--------------|--------|-----------|
| ![Checkerboard selection](./_images/02-grids-and-cells/selection-checkerboard.svg) | ![Border selection](./_images/02-grids-and-cells/selection-border.svg) | ![Every nth cell](./_images/02-grids-and-cells/selection-every-nth.svg) |

### Conditional (where)

```python
# Custom predicate
for cell in grid.where(lambda c: c.brightness > 0.7):
    cell.add_dot(color="yellow", radius=7)

# Multiple conditions
for cell in grid.where(lambda c: c.row < 10 and c.col > 10):
    cell.add_fill(color="lightblue")
```

### Regions

```python
# Rectangular region
for cell in grid.region(
    row_start=5, row_end=15,
    col_start=5, col_end=15
):
    cell.add_fill(color="pink")
```

See [Grid Selections](../advanced-concepts/06-grid-selections.md) for more patterns.

---

## Common Patterns

### Pattern 1: Checkerboard

```python
for i, cell in enumerate(grid):
    if (cell.row + cell.col) % 2 == 0:
        cell.add_fill(color="black")
    else:
        cell.add_fill(color="white")
```

![Checkerboard pattern](./_images/02-grids-and-cells/common-pattern-checkerboard.svg)

### Pattern 2: Radial Gradient

```python
center_row = grid.rows // 2
center_col = grid.cols // 2

for cell in grid:
    # Distance from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = (dr*dr + dc*dc) ** 0.5

    # Size based on distance
    max_dist = (center_row**2 + center_col**2) ** 0.5
    size = 2 + (1 - distance / max_dist) * 8

    cell.add_dot(radius=size, color="coral")
```

![Radial gradient pattern](./_images/02-grids-and-cells/common-pattern-radial.svg)

### Pattern 3: Wave

```python
import math

for cell in grid:
    # Sinusoidal wave
    wave = math.sin(cell.col / grid.cols * math.pi * 2)

    # Y position based on wave
    y = 0.5 + wave * 0.3  # Range: 0.2 to 0.8

    cell.add_dot(at=(0.5, y), radius=3, color="blue")
```

![Wave pattern](./_images/02-grids-and-cells/common-pattern-wave.svg)

---

## Tips and Best Practices

### Grid Size Affects Performance

- `20×20 = 400 cells` - Fast, abstract
- `40×40 = 1,600 cells` - Balanced (recommended)
- `60×60 = 3,600 cells` - Detailed, slower
- `100×100 = 10,000 cells` - Very detailed, slow

### Use Neighbor Access Safely

Always check for `None`:

```python
if cell.right:
    # Safe to use cell.right
    pass
```

### Cell Methods are Convenient

Instead of creating entities manually:

```python
# Verbose
dot = Dot(cell.center.x, cell.center.y, radius=5)
scene.add(dot)

# Better
cell.add_dot(radius=5)
```

### Combine with Image Data

When available, cell image data drives compelling visuals:

```python
for cell in grid:
    # Size and color from image
    size = 2 + cell.brightness * 8
    cell.add_dot(radius=size, color=cell.color)
```

---

## Entity Positioning Helpers

Entities have methods for relative positioning — useful when building complex compositions:

### offset_from

Get a point offset from any anchor:

```python
dot = cell.add_dot(radius=5, color="coral")

# Get a point 10px to the right of the dot's center
label_pos = dot.offset_from("center", dx=10, dy=0)
```

This is sugar for `entity.anchor(name) + Point(dx, dy)`.

### place_beside

Position one entity next to another using bounding boxes:

```python
rect1 = scene.add(Rect.at_center(Point(200, 200), 50, 30, fill="coral"))
rect2 = scene.add(Rect.at_center(Point(0, 0), 50, 30, fill="blue"))

# Place rect2 to the right of rect1 with 10px gap
rect2.place_beside(rect1, side="right", gap=10)
```

Valid sides: `"right"`, `"left"`, `"above"`, `"below"`. Centers are aligned on the perpendicular axis (e.g., `"right"` aligns vertical centers).

---

## Next Steps

- **Learn about entities**: [Entities](03-entities.md)
- **Explore styling**: [Styling](04-styling.md)
- **See grid patterns**: [Grid Selections](../advanced-concepts/06-grid-selections.md)
- **Try an example**: [Grid Patterns](../examples/beginner/grid-patterns.md)

---

## See Also

- 📖 [Scenes](01-scenes.md) - The canvas container
- 📖 [Entities](03-entities.md) - Things you draw in cells
- 🎯 [Grid Patterns Example](../examples/beginner/grid-patterns.md)
- 🎯 [Quick Start Example](../examples/beginner/quick-start.md)
- 🔍 [Grid API Reference](../api-reference/grid.md)
- 🔍 [Cell API Reference](../api-reference/cell.md)
