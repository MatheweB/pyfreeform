
# Recipe: Geometric Patterns

Create stunning geometric compositions using polygons, shape helpers, and pattern-based positioning.

---

## Visual Result

![Geometric Patterns](./_images/04-geometric-patterns/01_hexagon_grid.svg)

Geometric patterns create structured, mathematical beauty.

---

## Why This Works

Geometric patterns leverage our brain's natural ability to recognize order and symmetry. By using mathematical formulas to determine shape placement, rotation, and color, you create compositions that feel intentional yet complex. The `shapes` module provides battle-tested polygon vertices that tile perfectly, while position-based logic ensures every cell follows a consistent rule.

The visual power comes from:

- **Predictable variation**: Every cell differs, but follows the same rule
- **Mathematical harmony**: Patterns emerge from simple formulas
- **Visual rhythm**: Repetition creates familiarity; variation maintains interest
- **Emergent complexity**: Simple rules create sophisticated results

!!! tip "When to Use This Technique"
    Choose geometric patterns when you want:

    - Clean, modern aesthetics with mathematical precision
    - Structured compositions that feel orderly yet dynamic
    - Work that scales well (patterns look good at any grid size)
    - Fast rendering (shapes are computationally efficient)
    - Easy customization (change one formula, transform the entire piece)

---

## The Pattern

**Key Idea**: Use shape helpers and conditional logic to create repeating geometric forms.

```python
from pyfreeform import shapes

# Alternate shapes in checkerboard
for cell in scene.grid:
    if (cell.row + cell.col) % 2 == 0:
        cell.add_polygon(shapes.hexagon(), fill=colors.primary)
    else:
        cell.add_polygon(shapes.star(5), fill=colors.secondary)
```

![Checkerboard of alternating hexagons and stars](./_images/04-geometric-patterns/02_alternating_shapes.svg)

---

## Complete Example

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.with_grid(cols=20, rows=20, cell_size=25)
colors = Palette.sunset()
scene.background = colors.background

# Define shape library
shape_types = [
    shapes.triangle(),
    shapes.hexagon(),
    shapes.diamond(),
    shapes.star(5),
    shapes.squircle(n=4)
]

for cell in scene.grid:
    # Choose shape based on position pattern
    shape_idx = (cell.row + cell.col) % len(shape_types)
    shape = shape_types[shape_idx]

    # Color based on distance from center
    dr = cell.row - 10
    dc = cell.col - 10
    distance = (dr*dr + dc*dc) ** 0.5

    if distance < 5:
        color = colors.primary
    elif distance < 10:
        color = colors.secondary
    else:
        color = colors.accent

    # Create polygon
    poly = cell.add_polygon(shape, fill=color)

    # Rotate based on position
    angle = (cell.row * cell.col) * 15
    poly.rotate(angle)

scene.save("geometric_patterns.svg")
```

![Mix of geometric shapes with distance-based coloring](./_images/04-geometric-patterns/12_mixed_geometry.svg)

---

## Pattern Variations

### Concentric Rings

```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = int((dr*dr + dc*dc) ** 0.5)

    # Different shape per ring
    if distance % 3 == 0:
        cell.add_polygon(shapes.hexagon(), fill=colors.primary)
    elif distance % 3 == 1:
        cell.add_polygon(shapes.triangle(), fill=colors.secondary)
    else:
        cell.add_polygon(shapes.diamond(), fill=colors.accent)
```

![Concentric Rings](./_images/04-geometric-patterns/03_concentric_rings.svg)

!!! info "Understanding Distance Calculations"
    The distance formula `sqrt(dr*dr + dc*dc)` comes from the Pythagorean theorem. It calculates the Euclidean distance from each cell to the center, allowing you to create circular patterns on a rectangular grid. Converting to `int()` creates discrete rings instead of smooth gradients.

### Diagonal Stripes

```python
for cell in scene.grid:
    diagonal = (cell.row + cell.col) % 4

    if diagonal == 0:
        cell.add_polygon(shapes.square(), fill=colors.primary)
    elif diagonal == 1:
        cell.add_polygon(shapes.hexagon(), fill=colors.secondary)
    elif diagonal == 2:
        cell.add_polygon(shapes.star(6), fill=colors.accent)
    # diagonal == 3: leave empty
```

![Diagonal stripes with shape variations](./_images/04-geometric-patterns/04_diagonal_stripes.svg)

### Brightness-Responsive Shapes

```python
scene = Scene.from_image("photo.jpg", grid_size=20)

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_polygon(shapes.star(5), fill="gold")
    elif cell.brightness > 0.4:
        cell.add_polygon(shapes.hexagon(), fill="silver")
    elif cell.brightness > 0.2:
        cell.add_polygon(shapes.diamond(), fill="bronze")
    else:
        cell.add_polygon(shapes.triangle(), fill="darkgray")
```

---

## Advanced Techniques

### Rotating Squircles

```python
# iOS icon-style shapes with rotation
for cell in scene.grid:
    rotation = (cell.row + cell.col) * 30

    poly = cell.add_polygon(
        shapes.squircle(n=4),  # iOS icon shape
        fill=cell.color
    )
    poly.rotate(rotation)
```

![iOS icon-style squircles with rotation](./_images/04-geometric-patterns/07_squircle_pattern.svg)

### Nested Shapes

```python
# Large background shape
cell.add_polygon(
    shapes.hexagon(size=1.0),
    fill=colors.primary,
    z_index=0
)

# Smaller foreground shape
cell.add_polygon(
    shapes.star(5, size=0.6),
    fill=colors.accent,
    z_index=10
)
```

![Nested shapes with hexagon background and star foreground](./_images/04-geometric-patterns/08_nested_shapes.svg)

### Custom Star Variations

```python
# Multi-pointed stars
for cell in scene.grid:
    points = 5 + (cell.row % 4)  # 5, 6, 7, or 8 points

    cell.add_polygon(
        shapes.star(points=points, inner_radius=0.4),
        fill=cell.color
    )
```

![Stars with varying point counts across rows](./_images/04-geometric-patterns/06_star_variations.svg)

---

## Tips

### Balance Complexity

Don't overcrowd - leave some cells empty:

```python
for cell in scene.grid:
    # Only fill 60% of cells
    if cell.brightness > 0.4:
        cell.add_polygon(shapes.hexagon(), fill=cell.color)
```

### Use Consistent Sizing

Scale shapes proportionally:

```python
poly = cell.add_polygon(shapes.star(5), fill=colors.primary)
poly.scale(0.85)  # Slightly smaller than cell
```

![Hexagons with varying sizes based on distance from center](./_images/04-geometric-patterns/09_size_variations.svg)

### Combine with Rotation

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.diamond(), fill=cell.color)

    # Rotate based on position
    angle = (cell.row * 45 + cell.col * 30) % 360
    poly.rotate(angle)
```

![Shapes with position-based rotation](./_images/04-geometric-patterns/05_rotating_shapes.svg)

### Triangle Tessellation

```python
for cell in scene.grid:
    rotation = 0 if (cell.row + cell.col) % 2 == 0 else 180
    poly = cell.add_polygon(shapes.triangle(), fill=cell.color)
    poly.rotate(rotation)
```

![Triangle tessellation with alternating rotations](./_images/04-geometric-patterns/10_triangle_tessellation.svg)

### Diamond Pattern

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.diamond(), fill=cell.color)
    poly.scale(0.8 + cell.brightness * 0.2)
```

![Diamond pattern with brightness-based scaling](./_images/04-geometric-patterns/11_diamond_pattern.svg)

---

## Parameter Tuning Guide

### Choosing the Right Modulo Value

The modulo operator (`%`) creates repeating cycles. Here's how to choose the right value:

```python
# Small modulo = frequent repetition
(cell.row + cell.col) % 2  # Alternates every cell (checkerboard)

# Medium modulo = moderate variety
(cell.row + cell.col) % 4  # 4 different states

# Large modulo = more variety before repetition
(cell.row + cell.col) % 8  # 8 different states
```

!!! tip "Finding the Sweet Spot"
    Start with `% 3` or `% 4` for a balanced pattern. Too small (like `% 2`) can feel too regular; too large (like `% 12`) may not show clear patterns at typical grid sizes (20x20).

### Shape Size and Scaling

Control how much of each cell the shape fills:

```python
# Default: shapes fill most of the cell
cell.add_polygon(shapes.hexagon(), fill=color)

# Smaller: more whitespace
poly = cell.add_polygon(shapes.hexagon(), fill=color)
poly.scale(0.7)  # 70% of cell size

# Overlapping: shapes extend beyond cell boundaries
poly = cell.add_polygon(shapes.hexagon(), fill=color)
poly.scale(1.2)  # 120% of cell size - creates overlap
```

!!! warning "Overlap Considerations"
    Scaling shapes above 1.0 causes them to overlap neighboring cells. This can create interesting effects, but may obscure patterns. Use `z_index` carefully to control which shapes appear on top.

### Color Distribution Strategies

Different approaches to assigning colors:

```python
# Strategy 1: Position-based (creates stripes/regions)
if (cell.row + cell.col) % 2 == 0:
    color = colors.primary
else:
    color = colors.secondary

# Strategy 2: Distance-based (creates concentric zones)
distance = ((cell.row - center_row)**2 + (cell.col - center_col)**2) ** 0.5
if distance < 5:
    color = colors.primary
elif distance < 10:
    color = colors.secondary
else:
    color = colors.accent

# Strategy 3: Image-based (responsive to source image)
color = cell.color  # Uses sampled color from source image
```

---

## Common Pitfalls

### Pitfall 1: Using `color=` Instead of `fill=`

```python
# ❌ WRONG - add_polygon uses fill=, not color=
cell.add_polygon(shapes.hexagon(), color=colors.primary)

# ✅ CORRECT
cell.add_polygon(shapes.hexagon(), fill=colors.primary)
```

!!! warning "Parameter Names Matter"
    Different entity types use different parameter names. Polygons and ellipses use `fill=`, while dots, lines, and text use `color=`. Check the [API Reference](../api-reference/cell.md) when in doubt.

### Pitfall 2: Forgetting to Store Shapes for Transforms

```python
# ❌ WRONG - can't rotate without storing reference
cell.add_polygon(shapes.star(5), fill=color)
# ... how do we rotate this?

# ✅ CORRECT - store reference to transform
poly = cell.add_polygon(shapes.star(5), fill=color)
poly.rotate(45)
poly.scale(0.8)
```

### Pitfall 3: Integer Division Issues

```python
# ❌ WRONG - integer division truncates
center_row = scene.grid.rows / 2  # Could be 10.0

# ✅ CORRECT - floor division for cell indexing
center_row = scene.grid.rows // 2  # Always an integer: 10
```

### Pitfall 4: Overcomplicated Shape Selection

```python
# ❌ TOO COMPLEX - hard to predict pattern
shape_idx = (cell.row * 7 + cell.col * 3 + cell.row * cell.col) % 5

# ✅ SIMPLER - easier to understand and debug
shape_idx = (cell.row + cell.col) % 5
```

!!! tip "Start Simple, Add Complexity"
    Begin with simple formulas like `(cell.row + cell.col) % N` to understand the pattern, then add complexity incrementally. Test after each change.

---

## Best Practices

### 1. Create a Shape Library

Define shapes once, reuse many times:

```python
# Define library at the top
SHAPES = {
    'triangle': shapes.triangle(),
    'square': shapes.square(),
    'hexagon': shapes.hexagon(),
    'star': shapes.star(5),
    'diamond': shapes.diamond()
}

# Use throughout your code
for cell in scene.grid:
    shape_name = ['triangle', 'hexagon', 'star'][cell.row % 3]
    cell.add_polygon(SHAPES[shape_name], fill=cell.color)
```

### 2. Balance Variety and Cohesion

```python
# Too uniform (boring)
for cell in scene.grid:
    cell.add_polygon(shapes.hexagon(), fill=colors.primary)

# Too chaotic (overwhelming)
for cell in scene.grid:
    shape = random.choice(all_shapes)
    color = random.choice(all_colors)
    cell.add_polygon(shape, fill=color)

# Balanced (interesting but cohesive)
for cell in scene.grid:
    shape_idx = (cell.row + cell.col) % 3
    shape = [shapes.triangle(), shapes.hexagon(), shapes.diamond()][shape_idx]
    color = cell.color  # Consistent color scheme
    cell.add_polygon(shape, fill=color)
```

### 3. Use Consistent Z-Index Layers

```python
# Background layer
cell.add_polygon(shapes.hexagon(), fill=colors.primary, z_index=0)

# Middle layer
cell.add_polygon(shapes.star(5, size=0.6), fill=colors.secondary, z_index=5)

# Foreground layer
cell.add_dot(radius=2, color=colors.accent, z_index=10)
```

### 4. Test at Multiple Grid Sizes

```python
# Test small (quick iteration)
scene = Scene.with_grid(cols=10, rows=10, cell_size=30)

# Test medium (typical output)
scene = Scene.with_grid(cols=20, rows=20, cell_size=25)

# Test large (final quality)
scene = Scene.with_grid(cols=40, rows=40, cell_size=20)
```

!!! info "Performance Consideration"
    Patterns with many overlapping shapes can take longer to render. If performance is slow, reduce grid size during development and increase for final output.

---

## Advanced Tips

### Combining Multiple Patterns

Layer different pattern types for complex effects:

```python
for cell in scene.grid:
    # Pattern 1: Distance-based shape selection
    distance = ((cell.row - 10)**2 + (cell.col - 10)**2) ** 0.5
    if distance < 5:
        shape = shapes.star(5)
    else:
        shape = shapes.hexagon()

    # Pattern 2: Diagonal rotation
    rotation = (cell.row + cell.col) * 15

    # Pattern 3: Brightness-based color
    poly = cell.add_polygon(shape, fill=cell.color)
    poly.rotate(rotation)
```

### Creating Custom Shape Sequences

```python
# Fibonacci-inspired sequence
fib = [1, 1, 2, 3, 5, 8]
for cell in scene.grid:
    idx = (cell.row + cell.col) % len(fib)
    points = fib[idx]

    cell.add_polygon(shapes.star(points), fill=cell.color)
```

### Negative Space Patterns

```python
# Only fill certain cells, leave others empty
for cell in scene.grid:
    # Only fill if both row and col are even
    if cell.row % 2 == 0 and cell.col % 2 == 0:
        cell.add_polygon(shapes.hexagon(), fill=colors.primary)
    # Creates a sparse, airy pattern
```

---

## See Also

- 📖 [Polygons](../entities/05-polygons.md) - Shape helpers and mathematics
- 📖 [Transforms](../advanced-concepts/04-transforms.md) - Rotation and scaling
- 🎯 [Polygon Gallery](../examples/beginner/polygon-gallery.md) - Shape showcase
- 🎯 [Transforms Example](../examples/intermediate/transforms.md) - Rotation patterns

