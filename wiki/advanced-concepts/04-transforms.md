
# Transforms

Transform entities with rotation, scaling, and translation.

## Rotation

```python
# Rotate around entity center
entity.rotate(45)  # degrees, counterclockwise

# Rotate around custom point
entity.rotate(30, origin=Point(100, 100))
```

![Basic rotation at 0, 15, 30, and 45 degrees](./_images/04-transforms/01-rotation-basic.svg)

![Progressive rotation with increasing angles](./_images/04-transforms/02-rotation-progressive.svg)

![Rotation around a custom origin point](./_images/04-transforms/03-rotation-custom-origin.svg)

![Full circle rotation demonstrating 360 degrees](./_images/04-transforms/04-rotation-full-circle.svg)

**Math:**
```
x' = (x - ox) × cos(θ) - (y - oy) × sin(θ) + ox
y' = (x - ox) × sin(θ) + (y - oy) × cos(θ) + oy
```

## Scaling

```python
# Scale uniformly
entity.scale(2.0)  # Double size

# Scale from custom origin
entity.scale(0.5, origin=cell.center)
```

![Uniform scaling at 0.5x, 0.75x, 1.0x, and 1.5x](./_images/04-transforms/05-scaling-basic.svg)

![Progressive scaling with increasing factors](./_images/04-transforms/06-scaling-progressive.svg)

![Scaling from a custom origin point](./_images/04-transforms/07-scaling-custom-origin.svg)

## Translation

```python
# Relative movement
entity.move_by(dx=10, dy=-5)
entity.translate(10, -5)  # Same as move_by

# Absolute positioning
entity.move_to(100, 200)
entity.move_to(Point(100, 200))
```

![Relative movement with increasing dx offsets](./_images/04-transforms/08-translation-relative.svg)

![Absolute positioning with move_to](./_images/04-transforms/09-translation-absolute.svg)

![Translation patterns showing various movement strategies](./_images/04-transforms/10-translation-patterns.svg)

## Method Chaining

```python
entity.rotate(45).scale(1.5).move_by(10, 10)
```

![Method chaining: rotate, scale, and move combined](./_images/04-transforms/11-chaining-basic.svg)

![Complex method chaining with multiple transform operations](./_images/04-transforms/12-chaining-complex.svg)

## Examples

```python
# Distance-based rotation
for cell in scene.grid:
    dx = cell.col - center_col
    dy = cell.row - center_row
    distance = (dx*dx + dy*dy) ** 0.5
    rotation = distance * 10
    
    poly = cell.add_polygon(Polygon.hexagon())
    poly.rotate(rotation)
```

![Distance-based rotation pattern with hexagons](./_images/04-transforms/13-example-distance-based-rotation.svg)

![Wave rotation pattern across a grid](./_images/04-transforms/14-example-wave-rotation.svg)

![Spiral scale pattern radiating from center](./_images/04-transforms/15-example-spiral-scale.svg)

![Combined transforms: rotation, scaling, and translation together](./_images/04-transforms/16-example-combined-transforms.svg)

![Side-by-side comparison of all transform types](./_images/04-transforms/17-example-transform-comparison.svg)

## See Also
- [Transforms Example](../examples/intermediate/transforms.md)
- [Entities](../fundamentals/03-entities.md)
