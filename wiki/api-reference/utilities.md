
# Utilities API Reference

Helper functions, shape builders, and utility classes.

---

## Shape Helpers

The `Polygon` class provides pre-built polygon vertices via classmethods.

```python
from pyfreeform import Polygon
```

All shape helpers return vertex lists in relative coordinates (0-1), perfect for use with `cell.add_polygon()`.

### triangle()

```python
def triangle(size: float = 1.0, center: tuple[float, float] = (0.5, 0.5)) -> list[tuple[float, float]]
```

Equilateral triangle pointing up.

**Example**:
```python
cell.add_polygon(Polygon.triangle(), fill="red")
cell.add_polygon(Polygon.triangle(size=0.8), fill="blue")
```

![Basic Shapes Example](./_images/utilities/example1-basic-shapes.svg)

### square()

```python
def square(size: float = 1.0, center: tuple[float, float] = (0.5, 0.5)) -> list[tuple[float, float]]
```

Perfect square (45° rotated from rectangle).

### diamond()

```python
def diamond(size: float = 1.0, center: tuple[float, float] = (0.5, 0.5)) -> list[tuple[float, float]]
```

Diamond shape (square rotated 45°).

### hexagon()

```python
def hexagon(size: float = 1.0, center: tuple[float, float] = (0.5, 0.5)) -> list[tuple[float, float]]
```

Regular hexagon with flat top.

**Example**:
```python
cell.add_polygon(Polygon.hexagon(), fill="purple")
```

### star()

```python
def star(
    points: int = 5,
    size: float = 1.0,
    inner_radius: float = 0.4,
    center: tuple[float, float] = (0.5, 0.5)
) -> list[tuple[float, float]]
```

Multi-pointed star.

**Parameters**:
- `points`: Number of star points (5, 6, 8, etc.)
- `inner_radius`: Ratio of inner to outer radius (0.3-0.5 works well)

**Example**:
```python
cell.add_polygon(Polygon.star(5), fill="gold")
cell.add_polygon(Polygon.star(8, inner_radius=0.3), fill="silver")
```

![Stars Example](./_images/utilities/example2-stars.svg)

![Star Inner Radius Variations](./_images/utilities/example3-star-radius.svg)

### regular_polygon()

```python
def regular_polygon(
    n_sides: int,
    size: float = 1.0,
    center: tuple[float, float] = (0.5, 0.5)
) -> list[tuple[float, float]]
```

Any regular polygon.

**Example**:
```python
# Pentagon
cell.add_polygon(Polygon.regular_polygon(5), fill="blue")

# Octagon
cell.add_polygon(Polygon.regular_polygon(8), fill="green")
```

![Regular Polygons Example](./_images/utilities/example4-regular-polygons.svg)

### squircle()

```python
def squircle(
    size: float = 1.0,
    n: float = 4,
    center: tuple[float, float] = (0.5, 0.5)
) -> list[tuple[float, float]]
```

Superellipse - the iOS icon shape!

**Parameters**:
- `n`: Exponent controlling shape
  - `n=2`: Circle
  - `n=4`: Classic squircle (iOS icon)
  - `n=6+`: Approaches rounded square

**Mathematics**:
```
|x/a|ⁿ + |y/b|ⁿ = 1

Where:
  n = 2  : Perfect circle
  n = 4  : Squircle
  n → ∞  : Square
```

**Example**:
```python
# iOS icon shape
cell.add_polygon(Polygon.squircle(n=4), fill="blue")

# Variations
for i, n in enumerate([2, 3, 4, 5, 6]):
    cell.add_polygon(Polygon.squircle(n=n), fill=colors[i])
```

![Squircle Example](./_images/utilities/example5-squircle.svg)

### rounded_rect()

```python
def rounded_rect(
    size: float = 1.0,
    corner_radius: float = 0.1,
    center: tuple[float, float] = (0.5, 0.5)
) -> list[tuple[float, float]]
```

Rectangle with rounded corners.

**Parameters**:
- `corner_radius`: 0=sharp, 0.3=very round

![Rounded Rectangle Example](./_images/utilities/example6-rounded-rect.svg)

![Shape Sizes Example](./_images/utilities/example10-shape-sizes.svg)

![All Shapes Gallery](./_images/utilities/example11-all-shapes.svg)

---

## Point Class

```python
class Point:
    """Immutable 2D point with math operations."""

    def __init__(self, x: float, y: float)
```

The Point class is the foundation of all positioning in PyFreeform. It's an immutable coordinate with powerful math operations.

**Properties**:
```python
point.x: float  # Horizontal coordinate
point.y: float  # Vertical coordinate
```

### Arithmetic Operations

Points support standard math operations:

```python
from pyfreeform.core.point import Point

p1 = Point(100, 50)
p2 = Point(20, 30)

# Addition (vector addition)
p3 = p1 + p2  # Point(120, 80)

# Subtraction (vector subtraction)
p3 = p1 - p2  # Point(80, 20)

# Scalar multiplication
p3 = p1 * 2   # Point(200, 100)
p3 = 2 * p1   # Point(200, 100)

# Scalar division
p3 = p1 / 2   # Point(50, 25)

# Negation
p3 = -p1      # Point(-100, -50)
```

### Geometric Methods

#### distance_to()

```python
def distance_to(self, other: Point) -> float
```

Calculate Euclidean distance to another point.

**Example**:
```python
p1 = Point(0, 0)
p2 = Point(100, 100)
distance = p1.distance_to(p2)  # 141.42
```

#### lerp()

```python
def lerp(self, other: Point, t: float) -> Point
```

Linear interpolation between two points.

**Parameters**:
- `other`: Target point
- `t`: Interpolation factor (0 = self, 1 = other)

**Example**:
```python
p1 = Point(0, 0)
p2 = Point(100, 100)

# Halfway between
mid = p1.lerp(p2, 0.5)  # Point(50, 50)

# Quarter way
quarter = p1.lerp(p2, 0.25)  # Point(25, 25)

# Extrapolate beyond
beyond = p1.lerp(p2, 1.5)  # Point(150, 150)
```

#### midpoint()

```python
def midpoint(self, other: Point) -> Point
```

Return the midpoint between two points (shorthand for `lerp(other, 0.5)`).

**Example**:
```python
p1 = Point(0, 0)
p2 = Point(100, 100)
mid = p1.midpoint(p2)  # Point(50, 50)
```

#### normalized()

```python
def normalized(self) -> Point
```

Return a unit vector (length = 1) pointing in the same direction.

**Example**:
```python
p = Point(3, 4)
unit = p.normalized()  # Point(0.6, 0.8)
# Length is now 1.0
```

#### dot()

```python
def dot(self, other: Point) -> float
```

Calculate dot product (treats points as vectors).

**Example**:
```python
p1 = Point(3, 4)
p2 = Point(1, 2)
result = p1.dot(p2)  # 11.0 (3*1 + 4*2)
```

#### rotated()

```python
def rotated(self, angle: float, origin: Point | None = None) -> Point
```

Rotate point around an origin.

**Parameters**:
- `angle`: Rotation angle in **radians** (counter-clockwise)
- `origin`: Center of rotation (default: Point(0, 0))

**Example**:
```python
import math

p = Point(100, 0)

# Rotate 90° around origin
rotated = p.rotated(math.pi / 2)  # Point(0, 100)

# Rotate around custom origin
origin = Point(50, 50)
rotated = p.rotated(math.pi / 4, origin)
```

#### clamped()

```python
def clamped(self, min_x: float, min_y: float, max_x: float, max_y: float) -> Point
```

Return point clamped to bounds.

**Example**:
```python
p = Point(150, -50)
clamped = p.clamped(0, 0, 100, 100)  # Point(100, 0)
```

#### rounded()

```python
def rounded(self, decimals: int = 0) -> Point
```

Return point with coordinates rounded.

**Example**:
```python
p = Point(3.14159, 2.71828)
rounded = p.rounded(2)  # Point(3.14, 2.72)
rounded_int = p.rounded()  # Point(3, 3)
```

#### as_tuple()

```python
def as_tuple(self) -> tuple[float, float]
```

Convert to plain tuple.

**Example**:
```python
p = Point(10, 20)
t = p.as_tuple()  # (10, 20)
```

### Complete Example

```python
from pyfreeform.core.point import Point
import math

# Create points
start = Point(0, 0)
end = Point(100, 100)

# Basic operations
direction = (end - start).normalized()  # Unit vector
halfway = start.midpoint(end)

# Rotate around center
center = Point(50, 50)
rotated = end.rotated(math.pi / 4, center)

# Distance and interpolation
dist = start.distance_to(end)
quarter = start.lerp(end, 0.25)
```

---

## Utility Functions

### map_range()

```python
def map_range(
    value: float,
    in_min: float = 0,
    in_max: float = 1,
    out_min: float = 0,
    out_max: float = 1,
    clamp: bool = False
) -> float
```

Map a value from one range to another - essential for creative coding!

**Parameters**:
- `value`: The input value to map
- `in_min`: Input range minimum (default: 0)
- `in_max`: Input range maximum (default: 1)
- `out_min`: Output range minimum (default: 0)
- `out_max`: Output range maximum (default: 1)
- `clamp`: If True, clamp result to output range

**Returns**: The mapped value

**Example**:
```python
from pyfreeform import map_range

# Map brightness (0-1) to rotation (0-360)
for cell in scene.grid:
    rotation = map_range(cell.brightness, 0, 1, 0, 360)
    cell.add_text("A", rotation=rotation)

# Map brightness to radius (small when dark, large when bright)
for cell in scene.grid:
    radius = map_range(cell.brightness, 0, 1, 2, 10)
    cell.add_dot(radius=radius)

# Inverse mapping (bright = small, dark = large)
for cell in scene.grid:
    radius = map_range(cell.brightness, 0, 1, 10, 2)
    cell.add_dot(radius=radius)

# With clamping to prevent out-of-range values
size = map_range(value, 0, 100, 10, 50, clamp=True)
```

**Note**: You can also use Python math directly:
```python
rotation = cell.brightness * 360
radius = 2 + cell.brightness * 8
```

But `map_range()` reads more clearly and handles edge cases.

### display()

```python
def display(target: Scene | str | Path) -> None
```

Display an SVG in your default web browser - perfect for quick previews!

**Parameters**:
- `target`: Either a Scene object to render, or a path to an existing SVG file

**Example**:
```python
from pyfreeform import Scene, display

# Create and display a scene
scene = Scene.from_image("photo.jpg", grid_size=40)
for cell in scene.grid:
    cell.add_dot(color=cell.color, radius=5)

display(scene)  # Opens in browser immediately

# Or display an existing file
scene.save("artwork.svg")
display("artwork.svg")  # Opens the saved file
```

**Use cases**:
- Quick preview without saving
- Iterative development workflow
- Opening saved SVG files

---

## Color Utilities

### hex_to_rgb()

```python
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]
```

Convert hex color to RGB tuple.

**Example**:
```python
r, g, b = hex_to_rgb("#ff5733")
# (255, 87, 51)
```

### rgb_to_hex()

```python
def rgb_to_hex(r: int, g: int, b: int) -> str
```

Convert RGB to hex color.

**Example**:
```python
hex_color = rgb_to_hex(255, 87, 51)
# "#ff5733"
```

---

## Named Colors

PyFreeform supports all standard CSS/SVG named colors:

```python
cell.add_dot(color="red")
cell.add_dot(color="blue")
cell.add_dot(color="green")
cell.add_dot(color="coral")
cell.add_dot(color="gold")
cell.add_dot(color="crimson")
# ... and 140+ more
```

![Named Colors Example](./_images/utilities/example9-named-colors.svg)

Full list: `aliceblue`, `antiquewhite`, `aqua`, `aquamarine`, `azure`, `beige`, `bisque`, `black`, `blanchedalmond`, `blue`, `blueviolet`, `brown`, `burlywood`, `cadetblue`, `chartreuse`, `chocolate`, `coral`, `cornflowerblue`, `cornsilk`, `crimson`, `cyan`, and many more.

---

## Palette System

Built-in color schemes:

```python
from pyfreeform import Palette

# Available palettes
colors = Palette.midnight()  # Dark blues and purples
colors = Palette.sunset()    # Warm oranges and pinks
colors = Palette.ocean()     # Cool blues and teals
colors = Palette.forest()    # Earth greens and browns
colors = Palette.pastel()    # Soft pastels
colors = Palette.neon()      # Bright neon colors
colors = Palette.monochrome()  # Grayscale
colors = Palette.paper()     # Light, paper-like theme
```

![Palettes Example](./_images/utilities/example7-palettes.svg)

**Palette Properties**:
```python
colors.background: str  # Background color
colors.primary: str     # Main color
colors.secondary: str   # Secondary color
colors.accent: str      # Accent/highlight color
colors.line: str        # Line/stroke color
colors.grid: str        # Grid color
```

![Palette Properties Example](./_images/utilities/example8-palette-properties.svg)

**Example**:
```python
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(color=colors.accent)
    else:
        cell.add_dot(color=colors.primary)
```

---

## Style Objects

Reusable style configurations.

### DotStyle

```python
from pyfreeform.config import DotStyle

style = DotStyle(
    radius=5,
    color="red",
    opacity=0.8
)

cell.add_dot(style=style)
```

### LineStyle

```python
from pyfreeform.config import LineStyle

style = LineStyle(
    width=2,
    color="blue",
    cap="round",  # "round", "square", or "butt"
    opacity=1.0
)

cell.add_line(style=style)
```

### FillStyle

```python
from pyfreeform.config import FillStyle

style = FillStyle(
    color="lightgray",
    opacity=0.5
)

cell.add_fill(style=style)
```

### BorderStyle

```python
from pyfreeform.config import BorderStyle

style = BorderStyle(
    width=1,
    color="black",
    opacity=1.0
)

cell.add_border(style=style)
```

![Style Objects Example](./_images/utilities/example12-style-objects.svg)

---

## See Also

- 📖 [Polygons Guide](../entities/05-polygons.md) - Shape usage
- 📖 [Color System Guide](../color-and-style/01-color-system.md) - Color formats
- 📖 [Palettes Guide](../color-and-style/02-palettes.md) - All palettes
- 📖 [Style Objects Guide](../color-and-style/03-style-objects.md) - Reusable styles

