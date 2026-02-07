
# Example: Polygon Gallery

**Difficulty**: ⭐ Beginner

Showcase all built-in polygon shapes with the shape helper library.

---

## What You'll Learn

- Using `shapes` module for built-in polygons
- Triangle, square, hexagon, star, diamond helpers
- Squircles and rounded rectangles
- Regular polygons with n sides

---

## Final Result

![All Shapes](../_images/polygon-gallery/04_all_shapes.svg)

### More Examples

| Basic Shapes | Stars | Regular Polygons | Complete Gallery |
|--------------|-------|------------------|------------------|
| ![Example 1](../_images/polygon-gallery/01_basic_shapes.svg) | ![Example 2](../_images/polygon-gallery/02_stars.svg) | ![Example 3](../_images/polygon-gallery/03_regular_polygons.svg) | ![Example 4](../_images/polygon-gallery/04_all_shapes.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.with_grid(cols=8, rows=6, cell_size=40)
colors = Palette.pastel()
scene.background = colors.background

# Define all shapes to showcase
shape_gallery = [
    (shapes.triangle(), "Triangle"),
    (shapes.square(), "Square"),
    (shapes.diamond(), "Diamond"),
    (shapes.hexagon(), "Hexagon"),
    (shapes.star(points=5), "Star 5"),
    (shapes.star(points=6), "Star 6"),
    (shapes.star(points=8), "Star 8"),
    (shapes.regular_polygon(5), "Pentagon"),
    (shapes.regular_polygon(7), "Heptagon"),
    (shapes.regular_polygon(8), "Octagon"),
    (shapes.squircle(n=4), "Squircle"),
    (shapes.rounded_rect(corner_radius=0.2), "Rounded"),
]

# Cycle through shapes
for i, cell in enumerate(scene.grid):
    shape_data, name = shape_gallery[i % len(shape_gallery)]

    # Add polygon
    cell.add_polygon(
        shape_data,
        fill=colors.primary if i % 2 == 0 else colors.secondary,
        stroke=colors.line,
        stroke_width=1
    )

    # Optional: Add label
    # cell.add_text(name, font_size=8, color=colors.line)

scene.save("polygon_gallery.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Import Shapes Module

```python
from pyfreeform import shapes
```

**What's happening:**
- `shapes` module contains helper functions
- Each function returns a list of vertices in relative coordinates (0-1)
- Vertices are automatically scaled to fit the cell

### Step 2: Basic Shapes

```python
# Simple shapes
triangle = shapes.triangle()       # 3 sides, pointing up
square = shapes.square()           # 4 sides, rotated 45°
diamond = shapes.diamond()         # 4 sides, aligned to axes
hexagon = shapes.hexagon()         # 6 sides, flat top

cell.add_polygon(triangle, fill="red")
```

**What's happening:**
- All shapes centered at (0.5, 0.5) by default
- `size=1.0` parameter makes them fill the cell
- Returns list of `(x, y)` tuples

### Step 3: Stars

```python
# Multi-pointed stars
star_5 = shapes.star(points=5)              # Classic 5-point
star_6 = shapes.star(points=6)              # 6-point
star_8 = shapes.star(points=8, inner_radius=0.3)  # 8-point, sharper

cell.add_polygon(star_5, fill="gold")
```

**What's happening:**
- `points`: Number of star points
- `inner_radius`: Ratio of inner to outer radius (0.3-0.5 works well)
- Default `inner_radius=0.4` creates balanced stars

**Star Geometry:**
```
points=5, inner=0.4     points=6, inner=0.3
     *                       *
   *   *                  *     *
  *     *                *       *
    * *                    *   *
                             *
```

### Step 4: Regular Polygons

```python
# Any number of sides
pentagon = shapes.regular_polygon(5)    # 5 sides
heptagon = shapes.regular_polygon(7)    # 7 sides
octagon = shapes.regular_polygon(8)     # 8 sides
decagon = shapes.regular_polygon(10)    # 10 sides

cell.add_polygon(octagon, fill="navy")
```

**What's happening:**
- `n_sides`: Any integer ≥ 3
- Vertices evenly distributed around circle
- First vertex at top (0°)

### Step 5: Advanced Shapes

```python
# Squircle (superellipse - iOS icon shape!)
squircle = shapes.squircle(n=4)  # n controls roundness

# Rounded rectangle
rounded = shapes.rounded_rect(corner_radius=0.2)

cell.add_polygon(squircle, fill="blue")
cell.add_polygon(rounded, fill="green")
```

**What's happening:**
- Squircle: smooth blend between circle and square
  - `n=2`: Circle
  - `n=4`: iOS-style squircle
  - `n=6+`: Approaches square
- Rounded rect: rectangle with circular corners
  - `corner_radius=0.1`: Subtle rounding
  - `corner_radius=0.3`: Very round

---

## Try It Yourself

### Experiment 1: Star Variations

```python
# Different point counts and inner radii
for i in range(5, 9):
    for inner in [0.3, 0.4, 0.5]:
        cell.add_polygon(
            shapes.star(points=i, inner_radius=inner),
            fill=colors.primary
        )
```

### Experiment 2: Size and Position

```python
# Smaller shapes, custom center
small_triangle = shapes.triangle(size=0.6, center=(0.5, 0.3))
cell.add_polygon(small_triangle, fill="red")

# Large hexagon
large_hex = shapes.hexagon(size=1.2)  # Extends beyond cell
cell.add_polygon(large_hex, fill="blue")
```

### Experiment 3: Squircle Progression

```python
# Show n parameter effect
for col, n in enumerate([2, 3, 4, 5, 6, 8]):
    cell = scene.grid[0, col]
    cell.add_polygon(
        shapes.squircle(n=n),
        fill=colors.primary
    )
    cell.add_text(f"n={n}", font_size=8)
```

### Experiment 4: Combination Patterns

```python
# Mix shapes based on position
for cell in scene.grid:
    if (cell.row + cell.col) % 3 == 0:
        shape = shapes.triangle()
    elif (cell.row + cell.col) % 3 == 1:
        shape = shapes.hexagon()
    else:
        shape = shapes.star(5)

    cell.add_polygon(shape, fill=colors.primary)
```

---

## All Shape Helpers

### Basic Shapes
- `triangle(size, center)` - Equilateral triangle
- `square(size, center)` - Square rotated 45°
- `diamond(size, center)` - Diamond (square aligned to axes)
- `hexagon(size, center)` - Regular hexagon

### Stars
- `star(points, size, inner_radius, center)` - Multi-pointed star

### Regular Polygons
- `regular_polygon(n_sides, size, center)` - Any n-sided polygon

### Advanced
- `squircle(size, n, center)` - Superellipse (iOS icon)
- `rounded_rect(size, corner_radius, center)` - Rounded rectangle

---

## Custom Shape Creation

Create your own shapes by defining vertices:

```python
# Custom arrow shape
arrow = [
    (0.5, 0.1),   # Top point
    (0.7, 0.4),   # Right wing
    (0.6, 0.4),   # Right inner
    (0.6, 0.9),   # Right bottom
    (0.4, 0.9),   # Left bottom
    (0.4, 0.4),   # Left inner
    (0.3, 0.4),   # Left wing
]

cell.add_polygon(arrow, fill="red")
```

---

## Related

- 📖 [Polygons Entity](../../entities/05-polygons.md) - Full documentation
- 📖 [Transforms](../../advanced-concepts/04-transforms.md) - Rotate and scale shapes
- 🎯 [Grid Patterns](grid-patterns.md) - Previous example
- 🎯 [Transforms Example](../intermediate/transforms.md) - Rotating polygons
- 🎨 [Geometric Patterns Recipe](../../recipes/04-geometric-patterns.md) - More ideas

