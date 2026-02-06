
# Recipe: Rotating Shapes

Create dynamic, spiraling compositions using rotation transforms on polygons and ellipses.

---

## Visual Result

![Rotating hexagons and stars with varying angles](./_images/06-rotating-shapes/08_multi_shape_rotation.svg)

Rotation creates dynamic, flowing patterns across your artwork.

---

## Why This Works

Rotation breaks the static grid and adds motion to your compositions. Even though the shapes themselves are fixed in the final SVG, rotated shapes imply movement, direction, and energy. Our eyes naturally follow rotational patterns, creating visual flow across the canvas.

The technique works because:

- **Implied motion**: Rotation suggests spinning, flowing, or orbiting
- **Breaks monotony**: Aligned shapes feel static; rotated shapes feel alive
- **Mathematical beauty**: Rotation formulas create emergent spiral and wave patterns
- **Visual complexity**: Simple shapes become interesting through varied orientation
- **Depth illusion**: Rotation creates pseudo-3D effects on a 2D plane

!!! tip "When to Use This Technique"
    Choose rotation when you want:

    - Dynamic, energetic compositions that suggest movement
    - Visual interest from simple shapes (even squares become interesting)
    - Flow and direction across your artwork
    - Organic, natural patterns (spirals appear everywhere in nature)
    - Mathematical elegance (rotation formulas are simple yet powerful)

---

## The Pattern

**Key Idea**: Rotate shapes based on their position in the grid to create spiraling or wave-like effects.

```python
from pyfreeform import shapes

for cell in scene.grid:
    # Create shape
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Rotate based on position
    angle = (cell.row + cell.col) * 15  # degrees
    poly.rotate(angle)
```

![Hexagons with diagonal position-based rotation](./_images/06-rotating-shapes/05_diagonal_rotation.svg)

---

## Complete Example

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.from_image("photo.jpg", grid_size=25)
colors = Palette.ocean()
scene.background = colors.background

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

        # Rotation varies across grid
        angle = (cell.row * 20 + cell.col * 15) % 360
        poly.rotate(angle)

scene.save("rotating_shapes.svg")
```

---

## Rotation Patterns

### Linear Progression

Rotation increases steadily:

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Increases left to right, top to bottom
    angle = (cell.row * scene.grid.cols + cell.col) * 5
    poly.rotate(angle)
```

![Squares with progressive rotation from left to right](./_images/06-rotating-shapes/01_linear_progression.svg)

### Radial Pattern

Shapes point toward/away from center:

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

    poly.rotate(angle)
```

![Triangles pointing toward and away from center](./_images/06-rotating-shapes/02_radial_pattern.svg)

### Spiral Pattern

Create a vortex effect:

```python
for cell in scene.grid:
    # Distance from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = math.sqrt(dr*dr + dc*dc)

    # Angle from center
    angle = math.degrees(math.atan2(dr, dc))

    # Rotation combines angle + distance
    rotation = angle + distance * 30

    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)
    poly.rotate(rotation)
```

![Vortex spiral rotation effect with hexagons](./_images/06-rotating-shapes/03_spiral_pattern.svg)

### Brightness-Driven Rotation

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.star(5), fill=cell.color)

    # Bright cells rotate more
    angle = cell.brightness * 360  # 0° to 360°
    poly.rotate(angle)
```

![Stars with rotation driven by brightness levels](./_images/06-rotating-shapes/04_brightness_driven.svg)

### Wave Rotation

```python
import math

for cell in scene.grid:
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Sine wave rotation
    angle = math.sin(cell.col / scene.grid.cols * math.pi * 2) * 90
    poly.rotate(angle)
```

![Wave-based rotation creating sinusoidal angle variation](./_images/06-rotating-shapes/06_wave_rotation.svg)

---

## Rotating Ellipses

Ellipses show rotation dramatically:

```python
for cell in scene.grid:
    # Create elongated ellipse
    ellipse = cell.add_ellipse(
        rx=12,
        ry=6,
        fill=cell.color
    )

    # Rotation based on position
    angle = (cell.row + cell.col) * 20
    ellipse.rotation = angle  # Direct property assignment
```

![Elongated ellipses rotating at different angles](./_images/06-rotating-shapes/07_rotating_ellipses.svg)

---

## Advanced Techniques

### Rotate Around Custom Origin

Rotate around a point other than the center:

```python
poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

# Rotate around top-left corner instead of center
poly.rotate(45, origin=cell.top_left)
```

### Continuous Rotation Animation

For animation loops (if exporting frames):

```python
frame = 0  # Animation frame number

for cell in scene.grid:
    poly = cell.add_polygon(shapes.star(5), fill=cell.color)

    # Rotation changes per frame
    base_angle = (cell.row + cell.col) * 15
    animation_angle = frame * 2  # Rotates 2° per frame

    poly.rotate(base_angle + animation_angle)
```

### Combined Rotation and Scale

```python
poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

# Rotate
poly.rotate(45)

# Then scale (scale happens after rotation)
poly.scale(0.8)
```

### Multiple Shapes, Different Rotations

```python
# Background shape - slow rotation
bg = cell.add_polygon(
    shapes.hexagon(size=1.0),
    fill=colors.primary,
    z_index=0
)
bg.rotate((cell.row + cell.col) * 10)

# Foreground shape - fast rotation
fg = cell.add_polygon(
    shapes.star(5, size=0.6),
    fill=colors.accent,
    z_index=10
)
fg.rotate((cell.row + cell.col) * 45)
```

![Alternating rotation directions creating dynamic pattern](./_images/06-rotating-shapes/09_alternating_rotation.svg)

---

## Tips

### Keep Rotation Smooth

Use small increments for smooth progression:

```python
# Smooth: 5-15 degrees per cell
angle = (cell.row + cell.col) * 10

# Too jumpy: 45+ degrees per cell
angle = (cell.row + cell.col) * 90  # Avoid unless intentional
```

![Stepped rotation with only four discrete angles](./_images/06-rotating-shapes/10_stepped_rotation.svg)

![Concentric rotation with angle increasing from center outward](./_images/06-rotating-shapes/11_concentric_rotation.svg)

### Modulo for Patterns

Use modulo to create repeating cycles:

```python
# Repeats every 360 degrees
angle = ((cell.row + cell.col) * 30) % 360
```

### Combine Patterns

Layer multiple rotation strategies:

```python
# Base angle from position
base = (cell.row + cell.col) * 15

# Add brightness variation
variation = cell.brightness * 45

# Final rotation
poly.rotate(base + variation)
```

![Complex rotation pattern combining position, distance, and brightness](./_images/06-rotating-shapes/12_complex_pattern.svg)

---

## Parameter Tuning Guide

### Choosing Rotation Increment

The rotation increment determines how quickly angles change across the grid:

```python
# Subtle change (smooth, gentle progression)
angle = (cell.row + cell.col) * 5  # 5° per cell

# Medium change (balanced, visible pattern)
angle = (cell.row + cell.col) * 15  # 15° per cell

# Rapid change (dramatic, chaotic)
angle = (cell.row + cell.col) * 45  # 45° per cell
```

!!! tip "Finding the Right Increment"
    Start with 10-20 degrees for balanced results. Preview and adjust:

    - Too subtle (< 5°): Pattern barely visible, looks accidental
    - Just right (10-20°): Clear pattern, smooth transitions
    - Too jumpy (> 30°): Chaotic, hard to see overall flow

### Rotation Direction: Additive vs Multiplicative

```python
# Additive (diagonal stripes)
angle = (cell.row + cell.col) * 15
# Creates diagonal progression NW to SE

# Multiplicative (grid pattern)
angle = (cell.row * cell.col) * 5
# Creates more complex, less linear patterns

# Row-only (horizontal bands)
angle = cell.row * 20
# Each row has same rotation; columns differ by row

# Column-only (vertical bands)
angle = cell.col * 20
# Each column has same rotation; rows differ by column
```

### Radial Rotation Parameters

```python
import math

center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    dr = cell.row - center_row
    dc = cell.col - center_col

    # Factor 1: Base angle (direction from center)
    base_angle = math.degrees(math.atan2(dr, dc))

    # Factor 2: Distance multiplier (spiral tightness)
    distance = math.sqrt(dr*dr + dc*dc)
    spiral_factor = 30  # Adjust: 10=loose, 50=tight

    # Combined rotation
    angle = base_angle + distance * spiral_factor
    poly.rotate(angle)
```

!!! info "Spiral Factor Guidelines"
    - `10-20`: Loose spiral, barely noticeable
    - `20-40`: Balanced spiral, clear vortex effect
    - `40-60`: Tight spiral, dramatic swirl
    - `60+`: Very tight, can look repetitive

### Modulo for Repeating Patterns

```python
# Without modulo: continuous rotation (can exceed 360°)
angle = (cell.row + cell.col) * 15

# With modulo: repeating cycle
angle = ((cell.row + cell.col) * 15) % 360

# With modulo: limited discrete angles
angle = ((cell.row + cell.col) * 90) % 360  # Only 0°, 90°, 180°, 270°
```

!!! warning "Modulo 360 Usually Unnecessary"
    SVG rotation automatically wraps angles beyond 360°, so `% 360` is optional. Use it when you need explicit angle ranges for conditional logic.

---

## Common Pitfalls

### Pitfall 1: Rotating Before Storing Reference

```python
# ❌ WRONG - Can't rotate without storing polygon
cell.add_polygon(shapes.hexagon(), fill=colors.primary)
# ... now what? Can't rotate it

# ✅ CORRECT - Store reference first
poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)
poly.rotate(45)
```

### Pitfall 2: Ellipse Rotation Syntax Confusion

```python
# ❌ WRONG - Not all entities have .rotate() method
ellipse = cell.add_ellipse(rx=12, ry=6, fill=colors.primary)
ellipse.rotate(45)  # May not work for ellipses

# ✅ CORRECT - Use rotation parameter for ellipses
ellipse = cell.add_ellipse(
    rx=12,
    ry=6,
    rotation=45,  # Direct parameter
    fill=colors.primary
)

# ✅ ALSO CORRECT - Direct property assignment
ellipse = cell.add_ellipse(rx=12, ry=6, fill=colors.primary)
ellipse.rotation = 45
```

### Pitfall 3: Forgetting Import for Math Functions

```python
# ❌ WRONG - atan2 and sqrt not defined
angle = math.degrees(math.atan2(dr, dc))  # NameError

# ✅ CORRECT - Import math module
import math

angle = math.degrees(math.atan2(dr, dc))
distance = math.sqrt(dr*dr + dc*dc)
```

### Pitfall 4: Rotation Order with Multiple Transforms

```python
# Order matters! Transforms apply in sequence

# Rotate THEN scale (shape rotates, then shrinks in place)
poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)
poly.rotate(45)
poly.scale(0.8)  # Scales around already-rotated shape

# Scale THEN rotate (shape shrinks, then rotates)
poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)
poly.scale(0.8)
poly.rotate(45)  # Rotates the scaled shape
```

!!! info "Transform Order"
    Generally, rotate first, then scale. This keeps scaling uniform in x and y directions. Scaling before rotation can cause unexpected elongation in rotated coordinate space.

### Pitfall 5: Integer Division in Center Calculation

```python
# ❌ POTENTIALLY WRONG - Float division
center_row = scene.grid.rows / 2  # 10.0 or 10.5

# ✅ CORRECT - Integer floor division
center_row = scene.grid.rows // 2  # Always integer: 10

# Center calculation for radial patterns
dr = cell.row - center_row
dc = cell.col - center_col
```

---

## Best Practices

### 1. Store Center Once for Radial Patterns

```python
# Calculate once before loop
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    dr = cell.row - center_row
    dc = cell.col - center_col
    # Use dr, dc for angle/distance calculations
```

### 2. Combine Rotation with Brightness for Responsive Art

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.star(5), fill=cell.color)

    # Base rotation from position
    base_angle = (cell.row + cell.col) * 15

    # Vary by brightness
    brightness_variation = cell.brightness * 45  # 0° to 45°

    poly.rotate(base_angle + brightness_variation)
```

### 3. Use Smaller Increments for Smooth Patterns

```python
# Smooth, organic flow
angle = (cell.row + cell.col) * 8

# Discrete, stepped rotation (also interesting!)
angle = ((cell.row + cell.col) * 45) % 180  # Only 0°, 45°, 90°, 135°
```

### 4. Preview with Simple Shapes First

```python
# Develop with fast-rendering squares
poly = cell.add_polygon(shapes.square(), fill=cell.color)

# Once pattern works, switch to complex shapes
poly = cell.add_polygon(shapes.star(8), fill=cell.color)
```

### 5. Layer Multiple Rotations

```python
# Background: slow rotation
bg = cell.add_polygon(
    shapes.hexagon(size=1.0),
    fill=colors.primary,
    z_index=0
)
bg.rotate((cell.row + cell.col) * 10)

# Foreground: fast rotation
fg = cell.add_polygon(
    shapes.star(5, size=0.6),
    fill=colors.accent,
    z_index=10
)
fg.rotate((cell.row + cell.col) * 45)
```

!!! tip "Contrasting Rotation Speeds"
    Layering shapes with different rotation rates creates visual depth. Slow background rotation provides structure; fast foreground rotation adds dynamism.

---

## Advanced Techniques

### Wave-Based Rotation with Phase Control

```python
import math

phase_shift = 0  # Adjust for different wave patterns

for cell in scene.grid:
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Sine wave rotation across columns
    phase = (cell.col / scene.grid.cols * math.pi * 2) + phase_shift
    angle = math.sin(phase) * 90  # -90° to +90°

    poly.rotate(angle)
```

!!! info "Phase Shift Effects"
    - `phase_shift = 0`: Wave starts at center
    - `phase_shift = math.pi/2`: Wave starts at peak
    - `phase_shift = math.pi`: Wave starts inverted

### Fibonacci Spiral

```python
import math

golden_ratio = 1.618034

for i, cell in enumerate(scene.grid):
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Fibonacci spiral angle
    angle = i * golden_ratio * 137.5  # Golden angle in degrees
    poly.rotate(angle)
```

### Distance-Based Rotation Speed

```python
# Center rotates slowly, edges rotate rapidly
distance = math.sqrt(dr*dr + dc*dc)
max_distance = math.sqrt((scene.grid.rows/2)**2 + (scene.grid.cols/2)**2)

# Normalize distance to 0-1
normalized_distance = distance / max_distance

# Apply to rotation
base_angle = math.degrees(math.atan2(dr, dc))
speed_factor = 10 + normalized_distance * 50  # 10 near center, 60 at edges

poly.rotate(base_angle + distance * speed_factor)
```

### Alternating Clockwise/Counter-Clockwise

```python
# Checkerboard of rotation directions
if (cell.row + cell.col) % 2 == 0:
    # Clockwise
    angle = (cell.row + cell.col) * 15
else:
    # Counter-clockwise
    angle = -(cell.row + cell.col) * 15

poly.rotate(angle)
```

### Row/Column Wave Interference

```python
import math

for cell in scene.grid:
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Horizontal wave
    row_wave = math.sin(cell.row / scene.grid.rows * math.pi * 2) * 45

    # Vertical wave
    col_wave = math.cos(cell.col / scene.grid.cols * math.pi * 2) * 45

    # Combined interference pattern
    angle = row_wave + col_wave

    poly.rotate(angle)
```

---

## Troubleshooting Rotation Issues

### Problem: Rotation looks random, no clear pattern

**Solution**: Your increment is too large or formula too complex.

```python
# Simplify to diagonal pattern first
angle = (cell.row + cell.col) * 10

# Once working, add complexity incrementally
```

### Problem: Shapes rotating beyond cell boundaries overlap badly

**Solution**: Scale shapes down before rotating.

```python
poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)
poly.scale(0.8)  # Shrink first
poly.rotate(angle)  # Then rotate
```

### Problem: Spiral pattern has no visible "center"

**Solution**: Check your center calculation.

```python
# Ensure center is truly the midpoint
center_row = scene.grid.rows // 2  # Not rows / 2
center_col = scene.grid.cols // 2  # Not cols / 2

# Debug: print center coordinates
print(f"Center: ({center_row}, {center_col})")
```

### Problem: Ellipses not rotating

**Solution**: Use `rotation=` parameter or `.rotation` property.

```python
# ❌ This might not work
ellipse = cell.add_ellipse(rx=12, ry=6, fill=colors.primary)
ellipse.rotate(45)

# ✅ This works
ellipse = cell.add_ellipse(rx=12, ry=6, rotation=45, fill=colors.primary)
```

---

## See Also

- 📖 [Transforms](../advanced-concepts/04-transforms.md) - Rotation, scale, translate
- 📖 [Polygons](../entities/05-polygons.md) - Shapes to rotate
- 📖 [Ellipses](../entities/04-ellipses.md) - Ellipse rotation
- 🎯 [Transforms Example](../examples/intermediate/transforms.md) - Detailed rotation examples

