# 🎨 PyFreeform v0.2

A minimalist, art-focused Python drawing library with intuitive object-oriented design.

## Quick Start

Create dot art from an image in 5 lines:

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    cell.add_dot(color=cell.color)

scene.save("art.svg")
```

## Installation

```bash
pip install pyfreeform
```

## Core Concepts

### Scene

The container for your artwork. Create from an image or with an empty grid:

```python
# From image (loads color/brightness data into cells)
scene = Scene.from_image("photo.jpg", grid_size=40, cell_size=10)

# Empty grid
scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
```

### Cells

Cells have **typed properties** - no more magic dictionary keys:

```python
for cell in scene.grid:
    cell.brightness   # 0.0 to 1.0 (not 0-255!)
    cell.color        # "#ff5733" hex string
    cell.rgb          # (255, 87, 51) tuple
```

### Builder Methods

Cells have convenient builder methods:

```python
cell.add_dot(radius=0.4, color="red")
cell.add_line(start="top_left", end="bottom_right")
cell.add_diagonal(direction="up")  # SW to NE
cell.add_curve(curvature=0.5)      # Bézier curve
cell.add_polygon(vertices, fill="blue")
cell.add_fill(color="blue")
cell.add_border(color="gray")
```

### Positioning Dots Along Lines & Curves

The killer feature - position dots parametrically:

```python
line = cell.add_diagonal(direction="up")
cell.add_dot(along=line, t=cell.brightness)
# t=0: dot at line start
# t=1: dot at line end

# Works with curves too!
curve = cell.add_curve(curvature=0.5)
cell.add_dot(along=curve, t=cell.brightness)
```

### Curves

Quadratic Bézier curves for organic, flowing shapes:

```python
# curvature: 0 = straight, positive = bow left, negative = bow right
curve = cell.add_curve(
    start="bottom_left",
    end="top_right",
    curvature=0.5,
)

# Dots slide along curves just like lines!
cell.add_dot(along=curve, t=cell.brightness)
```

### Ellipses

Ellipses with parametric positioning:

```python
# Basic ellipse
ellipse = cell.add_ellipse(rx=15, ry=10, rotation=45, fill="coral")

# Position dots around ellipse perimeter
cell.add_dot(along=ellipse, t=cell.brightness)

# Direct angle-based positioning
point = ellipse.point_at_angle(90)  # Top of ellipse
```

### Pathable Protocol

Any object with `point_at(t)` works with `along=` - a unified interface for all paths:

```python
# Built-in pathables: Line, Curve, Ellipse
line = cell.add_line(start="left", end="right")
curve = cell.add_curve(curvature=0.5)
ellipse = cell.add_ellipse(rx=15, ry=10)

# All work the same way!
cell.add_dot(along=line, t=0.5)
cell.add_dot(along=curve, t=0.5)
cell.add_dot(along=ellipse, t=0.5)

# Create custom paths:
class Spiral:
    def point_at(self, t: float) -> Point:
        # Your parametric equations here
        angle = t * 2 * math.pi * 3
        radius = t * 20
        return Point(center.x + radius * cos(angle),
                     center.y + radius * sin(angle))

spiral = Spiral()
cell.add_dot(along=spiral, t=0.5)  # Works!
```

### Polygons & Shapes

Custom polygons and built-in shape helpers:

```python
from pyfreeform import shapes

# Built-in shapes (all return vertex lists)
cell.add_polygon(shapes.triangle(), fill="red")
cell.add_polygon(shapes.hexagon(), fill="purple")
cell.add_polygon(shapes.star(points=5), fill="gold")
cell.add_polygon(shapes.squircle(n=4), fill="blue")  # iOS icon shape!
cell.add_polygon(shapes.rounded_rect(corner_radius=0.2), fill="green")

# Custom polygon from any vertices
cell.add_polygon([(0.1, 0.2), (0.9, 0.1), (0.5, 0.9)], fill="orange")
```

Available shapes: `triangle`, `square`, `diamond`, `hexagon`, `star`, `regular_polygon`, `squircle`, `rounded_rect`

### Transforms

Rotate, scale, and translate entities:

```python
# Rotation (degrees, counterclockwise)
polygon.rotate(45)
line.rotate(30, origin=cell.center)

# Scaling
dot.scale(2.0)      # Double the radius
polygon.scale(0.5)  # Half size

# Translation
entity.translate(dx=10, dy=20)
```

### Constraining Shapes to Cells

Automatically fit shapes within cell bounds - handles rotation and works with all entity types:

```python
# Create shapes freely, then auto-constrain
for cell in scene.grid:
    # Create a large ellipse - don't worry about size!
    ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)

    # Auto-fit to 85% of cell (handles rotation automatically)
    ellipse.fit_to_cell(0.85)
```

**Dynamic sizing with image data:**

```python
for cell in scene.grid:
    # Create ellipse with any rotation
    ellipse = cell.add_ellipse(
        rx=100,
        ry=60,
        rotation=(cell.row + cell.col) * 15,
        fill=cell.color
    )

    # Brightness controls final size: 30% to 100% of cell
    scale = 0.3 + cell.brightness * 0.7
    ellipse.fit_to_cell(scale)
```

**Works for all entity types:**

```python
# Dots
dot = cell.add_dot(radius=0.9).fit_to_cell(0.9)

# Text
text = cell.add_text("Hi", font_size=200).fit_to_cell(0.8)

# Polygons
star = cell.add_polygon(vertices=huge_star).fit_to_cell(0.75)
```

**Positioning control:**

```python
# Recenter in cell (default)
ellipse.fit_to_cell(0.8, recenter=True)

# Keep at current position
ellipse.fit_to_cell(0.8, recenter=False)
```

The `fit_to_cell()` method automatically:
- Calculates the entity's bounding box
- Accounts for rotation and complex shapes
- Scales the entity to fit within the cell
- Optionally centers it in the cell

### Palettes

Pre-built color schemes for consistent aesthetics:

```python
from pyfreeform import Palette

colors = Palette.midnight()  # Dark blue theme
colors = Palette.sunset()    # Warm oranges
colors = Palette.ocean()     # Cool blues
colors = Palette.neon()      # Vibrant colors

scene.background = colors.background
cell.add_dot(color=colors.accent)
```

### Utilities

```python
from pyfreeform import map_range

# Map brightness (0-1) to rotation (0-360)
rotation = map_range(cell.brightness, 0, 1, 0, 360)

# Map brightness to radius (2-10)
radius = map_range(cell.brightness, 0, 1, 2, 10)
```

### Z-Index (Layering)

Control what renders on top:

```python
cell.add_border(z_index=0)    # Bottom layer
cell.add_diagonal(z_index=1)  # Middle layer
cell.add_dot(z_index=2)       # Top layer
```

### Grid Selection

Iterate over specific patterns:

```python
# Rows and columns
for cell in scene.grid.row(0):        # Top row
for cell in scene.grid.column(0):     # Left column

# Patterns
for cell in scene.grid.checkerboard("black"):
for cell in scene.grid.border(thickness=2):
for cell in scene.grid.every(n=3):    # Every 3rd cell

# Conditional
for cell in scene.grid.where(lambda c: c.brightness > 0.7):
```

### Cross-Cell Connections

Elements don't have to stay in their cells:

```python
dot1 = cell.add_dot(color="red")
dot2 = cell.right.add_dot(color="blue")

connection = dot1.connect(dot2, style={"width": 2, "color": "gray"})
scene.add(connection)
```

## Complete Example

```python
from pyfreeform import Scene, Palette, shapes

# Configuration
colors = Palette.midnight()
Z_BORDER, Z_CURVE, Z_DOT = 0, 1, 2

# Create scene
scene = Scene.from_image("photo.jpg", grid_size=30)
scene.background = colors.background

# Build art
for cell in scene.grid:
    cell.add_border(color=colors.grid, z_index=Z_BORDER)
    
    # Curves in medium-brightness areas
    if 0.3 < cell.brightness < 0.7:
        curve = cell.add_curve(curvature=0.4, color=colors.line, z_index=Z_CURVE)
        cell.add_dot(along=curve, t=cell.brightness, color=colors.accent, z_index=Z_DOT)
    
    # Hexagons in bright areas
    elif cell.brightness > 0.7:
        cell.add_polygon(shapes.hexagon(), fill=colors.primary, z_index=Z_CURVE)

scene.save("art.svg")
```

## Examples

The `examples/` folder contains:

| Example | Description |
|---------|-------------|
| `01_quick_start.py` | Simplest possible dot art |
| `02_custom_dots.py` | Customized styling with Palette |
| `03_diagonal.py` | Diagonal lines with sliding dots |
| `04_patterns.py` | Grid patterns and selections |
| `05_connections.py` | Cross-cell connections |
| `06_advanced.py` | Combining techniques |
| `07_curves.py` | Bézier curves with parametric dots |
| `08_transforms.py` | Rotation and scaling |
| `09_polygons.py` | Shape helpers gallery |
| `10_showcase.py` | All features combined |
| `11_groups.py` | Working with element groups |
| `12_text.py` | Text labels and typography |
| `13_text_showcase.py` | Advanced text features |
| `14_ellipses.py` | Ellipses with parametric positioning |
| `15_parametric_paths.py` | Unified Pathable interface |
| `16_custom_paths.py` | Custom parametric path implementations |

## Documentation

Full documentation is available in the [**PyFreeform Wiki**](wiki/):

- **[Getting Started](wiki/getting-started/)** - Installation and your first artwork
- **[Fundamentals](wiki/fundamentals/)** - Core concepts and API
- **[Examples Gallery](wiki/examples/)** - 16 documented examples with breakdowns
- **[API Reference](wiki/api-reference/)** - Complete technical documentation
- **[Parametric Art](wiki/parametric-art/)** - Mathematical deep dives with equations
- **[Recipes](wiki/recipes/)** - Common patterns and practical use cases
- **[Color & Style](wiki/color-and-style/)** - Palettes and styling guide
- **[Advanced Concepts](wiki/advanced-concepts/)** - Transforms, connections, and more
- **[Developer Guide](wiki/developer-guide/)** - Extend the library with custom entities

**Start here:** [wiki/index.md](wiki/index.md) for guided navigation based on your goals.

## API Reference

### Scene

| Method | Description |
|--------|-------------|
| `Scene.from_image(path, grid_size, cell_size)` | Create from image |
| `Scene.with_grid(cols, rows, cell_size)` | Create empty grid |
| `scene.grid` | Access the primary grid |
| `scene.save(path)` | Save to SVG |

### Cell

| Property | Type | Description |
|----------|------|-------------|
| `cell.brightness` | `float` | 0.0-1.0 normalized brightness |
| `cell.color` | `str` | Hex color from image |
| `cell.rgb` | `tuple` | (r, g, b) values |
| `cell.row`, `cell.col` | `int` | Grid position |
| `cell.above/below/left/right` | `Cell` | Neighbors |

| Method | Description |
|--------|-------------|
| `add_dot(radius, color, z_index)` | Add a dot |
| `add_dot(along=path, t=0.5)` | Position along any Pathable (Line, Curve, Ellipse) |
| `add_line(start, end, width, color)` | Add a line |
| `add_diagonal(start="bottom_left", end="top_right")` | Add diagonal line |
| `add_curve(curvature, width, color)` | Add Bézier curve |
| `add_ellipse(rx, ry, rotation, fill, stroke)` | Add an ellipse |
| `add_polygon(vertices, fill, stroke)` | Add polygon |
| `add_fill(color)` | Fill cell |
| `add_border(color, width)` | Add border |

### Ellipse

| Property | Type | Description |
|----------|------|-------------|
| `rx` | `float` | Horizontal radius |
| `ry` | `float` | Vertical radius |
| `rotation` | `float` | Rotation in degrees |

| Method | Description |
|--------|-------------|
| `point_at(t)` | Parametric position (t=0 to 1) |
| `point_at_angle(angle)` | Position at angle in degrees |

### Pathable Protocol

Objects implementing `point_at(t: float) -> Point` can be used with `along=`.

Built-in pathables: `Line`, `Curve`, `Ellipse`

Create custom paths by implementing `point_at()` - see `examples/16_custom_paths.py` for examples.

### Shape Helpers

```python
from pyfreeform import shapes

shapes.triangle(size=0.8)
shapes.square(size=0.8)
shapes.diamond(size=0.8)
shapes.hexagon(size=0.8)
shapes.star(points=5, size=0.8, inner_ratio=0.4)
shapes.regular_polygon(sides=8, size=0.8)
shapes.squircle(size=0.8, n=4)  # n=2 circle, n=4 squircle, n=8 rounded square
shapes.rounded_rect(size=0.8, corner_radius=0.2)
```

### Palette

Pre-built palettes: `midnight`, `sunset`, `ocean`, `forest`, `monochrome`, `paper`, `neon`, `pastel`

Properties: `background`, `primary`, `secondary`, `accent`, `line`, `grid`

## License

MIT License - see [LICENSE](./LICENSES/LICENSE) for details.

## Acknowledgments

This project depends on the following open source libraries:

- [NumPy](https://numpy.org/) - BSD-3-Clause License
- [Pillow](https://python-pillow.org/) - MIT-CMU License

See [Numpy-BSD-clause.txt](./LICENSES/third_party/Numpy-BSD-clause.txt) and [Numpy-BSD-clause.txt](./LICENSES/third_party/Pillow-MIT-CMU.txt) for full license texts.

---

Made with ❤️ for artists and creative coders.
