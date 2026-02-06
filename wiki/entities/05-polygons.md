
# Polygons

Polygons bring geometric shapes to your artwork. Create custom forms or use built-in helpers for triangles, hexagons, stars, squircles, and more.

---

## What is a Polygon?

A **Polygon** is a closed shape defined by vertices with:
- **Vertices** - List of points forming the shape
- **Fill** - Interior color
- **Stroke** - Border color (optional)
- **Centroid** - Center point (calculated automatically)

Polygons can have any number of vertices (minimum 3) and support both fill and stroke styling.

![Shape Gallery](./_images/05-polygons/01_shape_gallery.svg)

---

## Creating Polygons

### Via Cell Method with Shape Helpers

```python
from pyfreeform import shapes

# Built-in shapes (relative coordinates 0-1)
cell.add_polygon(shapes.triangle(), fill="red")
cell.add_polygon(shapes.square(), fill="blue")
cell.add_polygon(shapes.hexagon(), fill="purple")
cell.add_polygon(shapes.star(points=5), fill="gold")
cell.add_polygon(shapes.diamond(), fill="coral")

# Advanced shapes
cell.add_polygon(shapes.squircle(), fill="blue")  # iOS icon shape!
cell.add_polygon(shapes.rounded_rect(corner_radius=0.2), fill="green")
```

### Custom Vertices

```python
# Relative coordinates within cell (0-1)
triangle = [(0.5, 0), (1, 1), (0, 1)]  # Top center, bottom right, bottom left
cell.add_polygon(triangle, fill="orange")

# Or absolute coordinates
vertices = [(10, 10), (50, 10), (30, 50)]
polygon = Polygon(vertices, fill="blue")
scene.add(polygon)
```

---

## Built-In Shape Helpers

All helpers return vertex lists in relative coordinates (0-1):

### triangle(size=1.0, center=(0.5, 0.5))
Equilateral triangle pointing up.

### square(size=1.0, center=(0.5, 0.5))
Perfect square (45° rotated from rectangle).

### diamond(size=1.0, center=(0.5, 0.5))
Diamond shape (square rotated 45°).

### hexagon(size=1.0, center=(0.5, 0.5))
Regular hexagon with flat top.

### star(points=5, size=1.0, inner_radius=0.4, center=(0.5, 0.5))
Multi-pointed star.
- `points`: Number of star points (5, 6, 8, etc.)
- `inner_radius`: Ratio of inner to outer radius (0.3-0.5 works well)

### regular_polygon(n_sides, size=1.0, center=(0.5, 0.5))
Any regular polygon.
- `n_sides`: 5 = pentagon, 6 = hexagon, 7 = heptagon, 8 = octagon, etc.

### squircle(size=1.0, n=4, center=(0.5, 0.5))
Superellipse - the iOS icon shape!
- `n=2`: Circle
- `n=4`: Classic squircle (iOS icon)
- `n=6+`: Approaches rounded square

![Squircle Variations](./_images/05-polygons/03_squircle_variations.svg)

### rounded_rect(size=1.0, corner_radius=0.1, center=(0.5, 0.5))
Rectangle with rounded corners.
- `corner_radius`: 0=sharp, 0.3=very round

---

## The Mathematics of Squircles

Squircles use the **superellipse equation**:

```
|x/a|ⁿ + |y/b|ⁿ = 1

Where:
  a, b : Semi-axes (typically equal for squircles)
  n    : Exponent controlling shape

  n = 2  : Perfect circle (Pythagorean)
  n = 4  : Squircle (iOS-style)
  n → ∞  : Square with sharp corners
```

**Parametric form:**

```python
def sgn_pow(val, exp):
    """Signed power function."""
    return sign(val) × |val|^exp

For angle θ from 0 to 2π:
    x = sgn_pow(cos(θ), 2/n) × radius
    y = sgn_pow(sin(θ), 2/n) × radius
```

**Why it works:**
- Low n (like 2): Creates smooth circular curves
- High n (like 4): Creates smooth rounded squares
- The signed power preserves quadrant information

From [polygon.py](https://github.com/pyfreeform/pyfreeform/blob/main/src/pyfreeform/entities/polygon.py) implementation.

---

## Properties

```python
polygon.vertices     # List of Point objects
polygon.position     # Centroid (center of mass)
polygon.fill         # Fill color
polygon.stroke       # Stroke color
polygon.stroke_width # Border width
polygon.z_index      # Layer order
```

### Centroid Calculation

The position is automatically calculated as the centroid:

```
centroid_x = Σ(vertex_x) / vertex_count
centroid_y = Σ(vertex_y) / vertex_count
```

---

## Anchors

```python
polygon.anchor_names  # ["center", "v0", "v1", "v2", ...]

polygon.anchor("center")  # Centroid
polygon.anchor("v0")      # First vertex
polygon.anchor("v1")      # Second vertex
# etc.
```

---

## Common Patterns

### Pattern 1: Shape Gallery

```python
from pyfreeform import shapes, Palette

scene = Scene.with_grid(cols=8, rows=6, cell_size=20)
colors = Palette.pastel()

shape_grid = [
    shapes.triangle(),
    shapes.square(),
    shapes.diamond(),
    shapes.hexagon(),
    shapes.star(5),
    shapes.star(6),
    shapes.star(8),
    shapes.regular_polygon(7)
]

for i, cell in enumerate(scene.grid):
    shape_idx = i % len(shape_grid)
    cell.add_polygon(shape_grid[shape_idx], fill=colors.primary)
```

![Polygon Gallery](./_images/05-polygons/01_shape_gallery.svg)

### Pattern 2: Rotating Shapes

```python
for cell in scene.grid:
    # Rotation based on position
    rotation = (cell.row + cell.col) * 15

    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)
    poly.rotate(rotation)
```

![Rotating Shapes](./_images/05-polygons/02_rotating_shapes.svg)

### Pattern 3: Conditional Shapes

```python
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_polygon(shapes.hexagon(), fill="gold")
    elif cell.brightness > 0.4:
        cell.add_polygon(shapes.diamond(), fill="silver")
    else:
        cell.add_polygon(shapes.triangle(), fill="bronze")
```

![Conditional Shapes](./_images/05-polygons/04_conditional_shapes.svg)

### Pattern 4: Custom Star Burst

```python
# Create custom star shape
def custom_star(points=8):
    vertices = []
    for i in range(points * 2):
        angle = -90 + i * 180 / points  # Start from top
        r = 0.8 if i % 2 == 0 else 0.3  # Alternate radii
        x = 0.5 + r * math.cos(math.radians(angle))
        y = 0.5 + r * math.sin(math.radians(angle))
        vertices.append((x, y))
    return vertices

cell.add_polygon(custom_star(8), fill="orange")
```

![Custom Star Burst](./_images/05-polygons/05_custom_star_burst.svg)

---

## Transforms

Polygons support rotation and scaling:

```python
poly = cell.add_polygon(shapes.hexagon(), fill="purple")

# Rotate around centroid
poly.rotate(45)

# Rotate around custom point
poly.rotate(30, origin=cell.top_left)

# Scale from centroid
poly.scale(1.5)

# Scale from custom point
poly.scale(0.8, origin=cell.center)
```

---

## Styling

```python
# Fill only
cell.add_polygon(shapes.star(5), fill="gold")

# Stroke only
cell.add_polygon(shapes.hexagon(), fill=None, stroke="navy", stroke_width=2)

# Both fill and stroke
cell.add_polygon(
    shapes.diamond(),
    fill="lightblue",
    stroke="darkblue",
    stroke_width=1
)
```

---

## Complete Example

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Distance from center
    dx = cell.col - 7.5
    dy = cell.row - 7.5
    distance = (dx*dx + dy*dy) ** 0.5

    # Choose shape by distance
    if distance < 3:
        shape = shapes.squircle(n=4)
        color = colors.primary
    elif distance < 6:
        shape = shapes.hexagon()
        color = colors.secondary
    else:
        shape = shapes.triangle()
        color = colors.accent

    # Create polygon
    poly = cell.add_polygon(shape, fill=color)

    # Rotate based on angle from center
    angle = math.degrees(math.atan2(dy, dx))
    poly.rotate(angle)

scene.save("polygon_pattern.svg")
```

![Complete Polygon Example](./_images/05-polygons/06_complete_example.svg)

---

## Tips

### Use Shape Helpers

They handle the math for you:
```python
# Easy
cell.add_polygon(shapes.star(6), fill="gold")

# vs Manual (tedious)
vertices = [(calculate x, calculate y) for each point]
```

### Experiment with Squircles

The n parameter creates interesting variations:
```python
for n in [2, 3, 4, 5, 6]:
    cell.add_polygon(shapes.squircle(n=n), fill="blue")
```

### Combine with Rotation

Rotating polygons creates dynamic effects:
```python
poly = cell.add_polygon(shapes.hexagon())
poly.rotate((cell.row + cell.col) * 15)
```

---

## See Also

- 📖 [Text](06-text.md) - Typography
- 📖 [Transforms](../advanced-concepts/04-transforms.md) - Rotation and scaling
- 🎯 [Polygon Gallery](../examples/beginner/polygon-gallery.md)
- 🎯 [Transforms Example](../examples/intermediate/transforms.md)

