
# Transforms API Reference

Polygon transforms for rotation, scaling, and translation.

---

## Overview

Polygons support geometric transformations:
- **rotate()**: Rotate around a point
- **scale()**: Enlarge or shrink
- **translate()**: Move to new position

![Transform Comparison](./_images/transforms/example1-rotate-basic.svg)

---

## rotate()

Rotate a polygon around a point.

```python
def rotate(
    self,
    angle: float,
    origin: Point | None = None
) -> None
```

**Parameters**:
- `angle`: Rotation angle in degrees (positive = counterclockwise)
- `origin`: Point to rotate around (default: polygon's centroid)

**Example**:
```python
poly = cell.add_polygon(shapes.hexagon(), fill="blue")

# Rotate around centroid (default)
poly.rotate(45)

# Rotate around custom point
poly.rotate(30, origin=cell.top_left)
```

![Rotate Basic Example](./_images/transforms/example1-rotate-basic.svg)

![Rotate Origin Example](./_images/transforms/example2-rotate-origin.svg)

**Rotation Matrix**:
```
[x']   [cos(θ)  -sin(θ)] [x - ox]   [ox]
[y'] = [sin(θ)   cos(θ)] [y - oy] + [oy]

Where:
  θ = angle in radians
  (ox, oy) = origin point
  (x, y) = original vertex
  (x', y') = rotated vertex
```

---

## scale()

Scale a polygon by a factor.

```python
def scale(
    self,
    factor: float,
    origin: Point | None = None
) -> None
```

**Parameters**:
- `factor`: Scale factor (1.0 = no change, 2.0 = double size, 0.5 = half size)
- `origin`: Point to scale from (default: polygon's centroid)

**Example**:
```python
poly = cell.add_polygon(shapes.star(5), fill="gold")

# Enlarge by 50%
poly.scale(1.5)

# Shrink to 80%
poly.scale(0.8)

# Scale from custom point
poly.scale(1.2, origin=cell.center)
```

![Scale Basic Example](./_images/transforms/example3-scale-basic.svg)

![Scale Origin Example](./_images/transforms/example4-scale-origin.svg)

**Scale Transformation**:
```
x' = ox + (x - ox) × factor
y' = oy + (y - oy) × factor

Where:
  (ox, oy) = origin point
  (x, y) = original vertex
  (x', y') = scaled vertex
```

---

## translate()

Move a polygon by an offset.

```python
def translate(
    self,
    dx: float,
    dy: float
) -> None
```

**Parameters**:
- `dx`: Horizontal offset in pixels
- `dy`: Vertical offset in pixels

**Example**:
```python
poly = cell.add_polygon(shapes.diamond(), fill="purple")

# Move right and down
poly.translate(dx=10, dy=20)

# Move left and up
poly.translate(dx=-5, dy=-10)
```

![Translate Example](./_images/transforms/example5-translate.svg)

---

## Combining Transforms

Transforms can be chained together:

```python
poly = cell.add_polygon(shapes.hexagon(), fill="coral")

# Rotate, then scale, then translate
poly.rotate(45)
poly.scale(1.2)
poly.translate(dx=5, dy=5)
```

![Combined Transforms Example](./_images/transforms/example6-combined.svg)

**Important**: Order matters!
- Rotate → Scale: Rotates, then scales in rotated orientation
- Scale → Rotate: Scales, then rotates the scaled shape

---

## Common Patterns

### Position-Based Rotation

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)

    # Rotation based on position
    angle = (cell.row + cell.col) * 15
    poly.rotate(angle)
```

![Position Rotation Example](./_images/transforms/example7-position-rotation.svg)

### Radial Rotation

```python
import math

center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    poly = cell.add_polygon(shapes.triangle(), fill=cell.color)

    # Point toward center
    dr = cell.row - center_row
    dc = cell.col - center_col
    angle = math.degrees(math.atan2(dr, dc))

    poly.rotate(angle)
```

![Radial Rotation Example](./_images/transforms/example8-radial-rotation.svg)

### Brightness-Based Scaling

```python
for cell in scene.grid:
    poly = cell.add_polygon(shapes.star(5), fill=cell.color)

    # Bright = bigger, dark = smaller
    scale_factor = 0.5 + cell.brightness * 0.5  # 0.5 to 1.0
    poly.scale(scale_factor)
```

![Brightness Scaling Example](./_images/transforms/example9-brightness-scaling.svg)

![Complex Transform Pattern](./_images/transforms/example10-complex.svg)

### Rotation Animation

For animation frames:

```python
frame = 0  # Current frame number

for cell in scene.grid:
    poly = cell.add_polygon(shapes.squircle(n=4), fill=cell.color)

    # Rotation increases each frame
    angle = frame * 6  # 6° per frame
    poly.rotate(angle)
```

---

## Tips

### Rotate Around Specific Points

```python
# Rotate around top-left corner
poly.rotate(45, origin=cell.top_left)

# Rotate around cell center (not polygon center)
poly.rotate(45, origin=cell.center)
```

### Scale Before Rotation

For symmetrical results:

```python
# Scale first, then rotate
poly.scale(1.5)
poly.rotate(45)

# vs

# Rotate first, then scale
poly.rotate(45)
poly.scale(1.5)  # Scales in rotated orientation
```

![Order Matters Example](./_images/transforms/example11-order-matters.svg)

### Constrain to Cell

After transforms, use fit_to_cell() to ensure polygon stays within bounds:

```python
poly = cell.add_polygon(shapes.hexagon(), fill=cell.color)
poly.rotate(45)
poly.scale(1.5)

# Constrain to 90% of cell
poly.fit_to_cell(0.9)
```

---

## See Also

- 📖 [Transforms Guide](../advanced-concepts/04-transforms.md) - Detailed usage
- 📖 [Polygons](../entities/05-polygons.md) - Polygon entity
- 📖 [fit_to_cell Guide](../advanced-concepts/05-fit-to-cell.md) - Auto-constraining
- 🎯 [Rotating Shapes Recipe](../recipes/06-rotating-shapes.md) - Rotation patterns
- 🎯 [Transforms Example](../examples/intermediate/transforms.md) - Step-by-step tutorial

