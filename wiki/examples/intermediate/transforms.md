
# Example: Transforms

**Difficulty**: ⭐ Intermediate

Create dynamic compositions using rotation and scaling transforms on polygons.

---

## What You'll Learn

- Rotating polygons with `poly.rotate()`
- Scaling shapes with `poly.scale()`
- Position-based rotation patterns
- Creating spiral and vortex effects

---

## Final Result

![Rotating Hexagons](../_images/transforms/01_rotating_hexagons.svg)

### More Examples

| Rotating Hexagons | Radial Rotation | Spiral Pattern |
|-------------------|-----------------|----------------|
| ![Example 1](../_images/transforms/01_rotating_hexagons.svg) | ![Example 2](../_images/transforms/02_radial_rotation.svg) | ![Example 3](../_images/transforms/03_spiral_pattern.svg) |

---

## Step-by-Step Breakdown

### Step 1: Setup

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.with_grid(cols=20, rows=20, cell_size=25)
colors = Palette.sunset()
scene.background = colors.background
```

**What's happening:**
- Create a grid without an image (pure geometric art)
- 20×20 grid with 25px cells = 500×500px scene
- Sunset palette for warm, vibrant colors

### Step 2: Create Rotating Polygons

```python
for cell in scene.grid:
    # Create hexagon
    poly = cell.add_polygon(
        shapes.hexagon(),
        fill=colors.primary
    )

    # Rotation based on grid position
    angle = (cell.row + cell.col) * 15  # degrees
    poly.rotate(angle)
```

**What's happening:**
- `shapes.hexagon()` creates a regular hexagon
- `cell.row + cell.col` increases from top-left to bottom-right
- Each step increases rotation by 15°
- Creates a progressive rotation pattern

**The Pattern:**
```
Row 0, Col 0: angle = 0°
Row 0, Col 1: angle = 15°
Row 1, Col 0: angle = 15°
Row 1, Col 1: angle = 30°
...
Row 19, Col 19: angle = 570° (= 210° mod 360°)
```

### Step 3: Add Brightness-Responsive Scaling

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.star(5), fill=cell.color)

    # Rotation
    angle = (cell.row * cell.col) * 10
    poly.rotate(angle)

    # Scale based on brightness
    scale_factor = 0.5 + cell.brightness * 0.5  # 0.5 to 1.0
    poly.scale(scale_factor)
```

**What's happening:**
- `cell.row * cell.col` creates a different pattern
- Multiplication creates more variation than addition
- `scale_factor` ranges from 0.5 (50%) to 1.0 (100%)
- Bright areas get larger shapes

### Step 4: Radial Rotation

```python
import math

center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    poly = cell.add_polygon(shapes.triangle(), fill=cell.color)

    # Calculate angle from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    angle = math.degrees(math.atan2(dr, dc))

    # Shapes point toward/away from center
    poly.rotate(angle)
```

**What's happening:**
- `atan2(dr, dc)` calculates angle from center to cell
- Returns radians, converted to degrees
- Creates a radial/sunburst pattern
- All shapes point toward or away from center

**The Mathematics:**
```
angle = atan2(Δy, Δx)

Where:
  Δy = cell.row - center_row
  Δx = cell.col - center_col

Result in radians: [-π, π]
Converted to degrees: [-180°, 180°]
```

---

## Complete Code

```python
from pyfreeform import Scene, Palette, shapes
import math

scene = Scene.from_image("photo.jpg", grid_size=25)
colors = Palette.ocean()
scene.background = colors.background

center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    if cell.brightness > 0.3:
        # Choose shape based on brightness
        if cell.brightness > 0.7:
            shape = shapes.star(5)
            color = colors.accent
        elif cell.brightness > 0.5:
            shape = shapes.hexagon()
            color = colors.primary
        else:
            shape = shapes.diamond()
            color = colors.secondary

        # Create polygon
        poly = cell.add_polygon(shape, fill=color)

        # Distance-based rotation
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr*dr + dc*dc)

        # Angle from center
        angle = math.degrees(math.atan2(dr, dc))

        # Rotation combines angle + distance
        rotation = angle + distance * 30
        poly.rotate(rotation)

scene.save("rotating_shapes.svg")
```

---

## Try It Yourself

### Experiment 1: Different Rotation Patterns

```python
# Linear progression
angle = (cell.row + cell.col) * 15

# Diagonal emphasis
angle = cell.row * 20 + cell.col * 15

# Multiplication (more variation)
angle = (cell.row * cell.col) * 5

# Checkerboard
if (cell.row + cell.col) % 2 == 0:
    angle = 45
else:
    angle = -45
```

### Experiment 2: Combine Rotation and Scale

```python
poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

# Rotate first
poly.rotate((cell.row + cell.col) * 15)

# Then scale
scale = 0.6 + cell.brightness * 0.4
poly.scale(scale)
```

### Experiment 3: Spiral Pattern

```python
# Distance from center
dr = cell.row - center_row
dc = cell.col - center_col
distance = math.sqrt(dr*dr + dc*dc)

# Angle from center
angle = math.degrees(math.atan2(dr, dc))

# Spiral: rotation increases with distance
rotation = angle + distance * 45

poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)
poly.rotate(rotation)
```

### Challenge: Vortex Effect

Create a swirling vortex:

```python
for cell in scene.grid:
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = math.sqrt(dr*dr + dc*dc)
    angle = math.degrees(math.atan2(dr, dc))

    # Vortex rotation (decreases with distance)
    rotation = angle - (20 - distance) * 40

    poly = cell.add_polygon(shapes.star(6), fill=cell.color)
    poly.rotate(rotation)

    # Scale decreases toward center
    scale = 0.3 + (distance / 15) * 0.7
    poly.scale(scale)
```

---

## Related

- 📖 [Transforms API](../../api-reference/transforms.md) - Full API reference
- 📖 [Polygons](../../entities/05-polygons.md) - Polygon shapes
- 🎯 [Rotating Shapes Recipe](../../recipes/06-rotating-shapes.md) - More patterns
- 🎯 [Geometric Patterns Recipe](../../recipes/04-geometric-patterns.md) - Shape ideas

