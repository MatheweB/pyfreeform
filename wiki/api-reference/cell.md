
# Cell API Reference

The `Cell` class represents a single unit in a grid - the fundamental building block for placing art elements.

---

## Overview

!!! info "What Cells Provide"
    Cells provide:

    - **Typed data access**: `cell.brightness`, `cell.color` instead of dict lookups
    - **Builder methods**: `cell.add_dot()`, `cell.add_line()` for easy element creation
    - **Position helpers**: Named positions like "center", "top_left", etc.
    - **Neighbor access**: `cell.right`, `cell.below` for cross-cell operations

![Cell Overview](./_images/cell/example1-named-positions.svg)

---

## Class Definition

```python
class Cell:
    """A cell within a grid."""

    def __init__(
        self,
        grid: Grid,
        row: int,
        col: int,
        x: float,
        y: float,
        width: float,
        height: float
    )
```

**Note**: Cells are typically created by `Grid`, not directly instantiated.

---

## Properties

### Position and Dimensions

```python
cell.row: int           # Row index (0-based)
cell.col: int           # Column index (0-based)
cell.x: float           # X coordinate of top-left corner
cell.y: float           # Y coordinate of top-left corner
cell.width: float       # Cell width in pixels
cell.height: float      # Cell height in pixels
cell.bounds: tuple      # (x, y, width, height)
```

**Example**:
```python
for cell in scene.grid:
    print(f"Cell [{cell.row}, {cell.col}] at ({cell.x}, {cell.y})")
    print(f"  Size: {cell.width} x {cell.height}")
```

### Image Data

```python
cell.brightness: float        # 0.0 (black) to 1.0 (white)
cell.color: str              # Hex color "#rrggbb"
cell.rgb: tuple[int, int, int]  # (r, g, b) where each is 0-255
cell.alpha: float            # 0.0 (transparent) to 1.0 (opaque)
```

**Example**:
```python
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(color=cell.color, radius=5)

    r, g, b = cell.rgb
    is_reddish = r > g and r > b
```

### Named Positions

```python
cell.top_left: Point
cell.top_right: Point
cell.bottom_left: Point
cell.bottom_right: Point
cell.center: Point
cell.top: Point         # Top center
cell.bottom: Point      # Bottom center
cell.left: Point        # Left center
cell.right: Point       # Right center
```

![Named positions](./_images/cell/example1-named-positions.svg)

### Neighbor Access

!!! tip "Easy Neighbor Access"
    Access neighboring cells directly - perfect for creating connections and patterns.

#### Cardinal Directions (4-way)

```python
cell.above: Cell | None        # North
cell.below: Cell | None        # South
cell.left: Cell | None         # West
cell.right: Cell | None        # East
```

#### Diagonal Directions (8-way)

```python
cell.above_left: Cell | None   # Northwest
cell.above_right: Cell | None  # Northeast
cell.below_left: Cell | None   # Southwest
cell.below_right: Cell | None  # Southeast
```

#### Neighbor Collections

```python
cell.neighbors: dict[str, Cell | None]
# Returns: {"above": Cell, "below": Cell, "left": Cell, "right": Cell}
# Only cardinal directions (4-way)

cell.neighbors_all: dict[str, Cell | None]
# Returns all 8 neighbors including diagonals
# Keys: "above", "below", "left", "right",
#       "above_left", "above_right", "below_left", "below_right"
```

**Examples**:

```python
# Connect to right neighbor
for cell in scene.grid:
    if cell.right:
        dot1 = cell.add_dot(radius=3)
        dot2 = cell.right.add_dot(radius=3)
        Connection(start=dot1, end=dot2)

# Connect diagonals
for cell in scene.grid:
    if cell.below_right:
        dot1 = cell.add_dot(at="bottom_right", radius=2)
        dot2 = cell.below_right.add_dot(at="top_left", radius=2)
        Connection(start=dot1, end=dot2)

# Iterate all neighbors
for cell in scene.grid:
    for direction, neighbor in cell.neighbors_all.items():
        if neighbor and neighbor.brightness > cell.brightness:
            # Connect to brighter neighbors
            Connection(
                start=cell.add_dot(radius=2),
                end=neighbor.add_dot(radius=2)
            )
```

![Neighbor Access Example](./_images/cell/example2-neighbor-access.svg)

---

## Builder Methods

### add_dot()

```python
def add_dot(
    self,
    at: Position = "center",
    radius: float = 3,
    color: str = "black",
    style: DotStyle | None = None,
    z_index: int = 0,
    along: Pathable | None = None,
    t: float | None = None
) -> Dot
```

**Parameters**:
- `at`: Position ("center", "top_left", etc.) or (rx, ry) tuple
- `radius`: Dot radius in pixels
- `color`: Fill color
- `style`: Optional DotStyle object
- `z_index`: Layer order
- `along`: Optional path to position along
- `t`: Parameter 0-1 along path

**Example**:
```python
# Simple dot at center
cell.add_dot(radius=5, color="red")

# Dot at custom position
cell.add_dot(at="top_left", radius=3, color="blue")

# Along a curve
curve = cell.add_curve(curvature=0.5)
cell.add_dot(along=curve, t=0.5, radius=4)
```

![Add dot examples](./_images/cell/example3-add-dot.svg)

### add_line()

```python
def add_line(
    self,
    start: Position = "left",
    end: Position = "right",
    color: str = "black",
    width: float = 1,
    style: LineStyle | None = None,
    z_index: int = 0
) -> Line
```

**Example**:
```python
# Horizontal line
cell.add_line(start="left", end="right")

# Diagonal line
cell.add_line(start="bottom_left", end="top_right", width=2)

# Custom positions
cell.add_line(start=(0.2, 0.2), end=(0.8, 0.8), color="blue")
```

![Add line examples](./_images/cell/example4-add-line.svg)

### add_curve()

```python
def add_curve(
    self,
    start: Position = "left",
    end: Position = "right",
    curvature: float = 0.5,
    color: str = "black",
    width: float = 1,
    style: LineStyle | None = None,
    z_index: int = 0
) -> Curve
```

**Example**:
```python
# Simple curve
curve = cell.add_curve(curvature=0.5, color="blue")

# Custom endpoints
cell.add_curve(
    start="bottom_left",
    end="top_right",
    curvature=0.3,
    width=2
)
```

![Add curve examples](./_images/cell/example5-add-curve.svg)

### add_ellipse()

!!! warning "Use fill= not color="
    Ellipses use `fill=` for the fill color, not `color=`. This is consistent with SVG standards.

```python
def add_ellipse(
    self,
    at: Position = "center",
    rx: float = 10,
    ry: float = 10,
    rotation: float = 0,
    fill: str | None = "black",
    stroke: str | None = None,
    stroke_width: float = 1,
    z_index: int = 0
) -> Ellipse
```

**Example**:
```python
# Circle
cell.add_ellipse(rx=10, ry=10, fill="red")

# Oval
cell.add_ellipse(rx=15, ry=8, rotation=45, fill="blue")
```

![Add ellipse examples](./_images/cell/example6-add-ellipse.svg)

### add_polygon()

!!! warning "Use fill= not color="
    Polygons use `fill=` for the fill color, not `color=`. This is consistent with SVG standards.

```python
def add_polygon(
    self,
    vertices: list[tuple[float, float]],
    fill: str | None = "black",
    stroke: str | None = None,
    stroke_width: float = 1,
    z_index: int = 0
) -> Polygon
```

**Example**:
```python
from pyfreeform import shapes

# Built-in shapes
cell.add_polygon(shapes.hexagon(), fill="green")
cell.add_polygon(shapes.star(5), fill="gold")

# Custom vertices (relative 0-1)
triangle = [(0.5, 0), (1, 1), (0, 1)]
cell.add_polygon(triangle, fill="orange")
```

![Add polygon examples](./_images/cell/example7-add-polygon.svg)

### add_text()

```python
def add_text(
    self,
    content: str,
    at: Position = "center",
    font_size: float = 16,
    color: str = "black",
    font_family: str = "sans-serif",
    text_anchor: Literal["start", "middle", "end"] = "middle",
    baseline: str = "middle",
    rotation: float = 0,
    z_index: int = 0
) -> Text
```

**Example**:
```python
# Simple label
cell.add_text("Hello", font_size=12, color="white")

# Data display
value = f"{cell.brightness:.2f}"
cell.add_text(value, font_family="monospace", font_size=8)
```

![Add text examples](./_images/cell/example8-add-text.svg)

### add_rect() / add_fill() / add_border()

```python
# Generic rectangle
def add_rect(
    self,
    at: Position = "center",
    width: float | None = None,  # None = cell width
    height: float | None = None,  # None = cell height
    fill: str | None = "black",
    stroke: str | None = None,
    stroke_width: float = 1,
    z_index: int = 0
) -> Rect

# Shortcuts
def add_fill(
    self,
    color: str = "black",
    style: FillStyle | None = None,
    z_index: int = 0
) -> Rect

def add_border(
    self,
    color: str = "black",
    width: float = 1,
    style: BorderStyle | None = None,
    z_index: int = 0
) -> Rect
```

**Example**:
```python
# Fill entire cell
cell.add_fill(color="lightgray", z_index=0)

# Border around cell
cell.add_border(color="black", width=1)

# Custom rectangle (direct construction)
from pyfreeform import Rect
rect = Rect(
    x=cell.center.x - 15,
    y=cell.center.y - 10,
    width=30,
    height=20,
    fill="blue",
    stroke="navy",
    stroke_width=2
)
scene.add(rect)
```

![Fill and border examples](./_images/cell/example9-fill-border.svg)

### add_diagonal()

```python
def add_diagonal(
    self,
    direction: Literal["up", "down"] = "down",
    color: str = "black",
    width: float = 1,
    z_index: int = 0
) -> Line
```

Add a diagonal line across the cell.

**Parameters**:
- `direction`: "up" (SW to NE) or "down" (NW to SE)
- `color`: Line color
- `width`: Line width in pixels
- `z_index`: Layer order

**Example**:
```python
# Diagonal line from top-left to bottom-right
cell.add_diagonal(start="top_left", end="bottom_right", width=2, color="blue")

# Diagonal line from bottom-left to top-right
cell.add_diagonal(start="bottom_left", end="top_right", width=1, color="red")
```

![Cross and Diagonal Examples](./_images/cell/example10-cross-and-x.svg)

---

## Methods

### relative_to_absolute()

Convert relative (0-1) or named position to absolute pixels.

```python
def relative_to_absolute(self, pos: Position) -> Point
```

**Example**:
```python
# Named position
point = cell.relative_to_absolute("center")

# Relative coordinates
point = cell.relative_to_absolute((0.25, 0.75))
```

### absolute_to_relative()

Convert absolute pixel position to relative (0-1) coordinates.

```python
def absolute_to_relative(self, point: Point) -> tuple[float, float]
```

### contains()

Check if a point is inside this cell.

```python
def contains(self, point: Point) -> bool
```

---

## Common Patterns

### Conditional Elements

```python
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(radius=5, color=cell.color)
```

### Named Position Usage

```python
# Place dots at corners
for cell in scene.grid:
    cell.add_dot(at="top_left", radius=2, color="red")
    cell.add_dot(at="top_right", radius=2, color="blue")
    cell.add_dot(at="bottom_left", radius=2, color="green")
    cell.add_dot(at="bottom_right", radius=2, color="yellow")
```

### Neighbor Connections

```python
for cell in scene.grid:
    dot1 = cell.add_dot(radius=3)

    if cell.right:
        dot2 = cell.right.add_dot(radius=3)
        Connection(start=dot1, end=dot2)
```

### Layering

```python
# Background (z_index=0)
cell.add_fill(color="lightgray", z_index=0)

# Content (z_index=5)
cell.add_dot(radius=5, z_index=5)

# Border (z_index=10)
cell.add_border(color="black", width=1, z_index=10)
```

![Layering example](./_images/cell/example11-layering.svg)

![Complete Cell Example](./_images/cell/example12-complete.svg)

---

## See Also

- 📖 [Grid API](grid.md) - Parent grid container
- 📖 [Entities API](entities.md) - All entity types
- 📖 [Grids and Cells Guide](../fundamentals/02-grids-and-cells.md)
- 🎯 [Quick Start Example](../examples/beginner/quick-start.md)

