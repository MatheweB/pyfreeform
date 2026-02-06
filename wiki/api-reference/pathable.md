
# Pathable Protocol API Reference

The `Pathable` protocol defines a unified interface for positioning elements along paths.

---

## Overview

Any entity that implements `Pathable` can be used with the `along=` parameter:
- **Line**: Linear interpolation
- **Curve**: Quadratic Bézier curve
- **Ellipse**: Parametric ellipse perimeter
- **Custom paths**: Spirals, waves, Lissajous curves

![Pathable Overview](./_images/pathable/example1-line-point-at.svg)

---

## Protocol Definition

```python
class Pathable(Protocol):
    """Protocol for entities that support parametric positioning."""

    def point_at(self, t: float) -> Point:
        """
        Get point at parameter t along the path.

        Args:
            t: Parameter from 0.0 (start) to 1.0 (end)

        Returns:
            Point at that position along the path
        """
        ...
```

---

## Built-in Pathable Entities

### Line

Linear interpolation between start and end.

```python
line = Line(x1=0, y1=0, x2=100, y2=100)

# Get points along line
point_0 = line.point_at(0.0)    # (0, 0) - start
point_25 = line.point_at(0.25)  # (25, 25)
point_50 = line.point_at(0.5)   # (50, 50) - midpoint
point_100 = line.point_at(1.0)  # (100, 100) - end
```

![Along Line Example](./_images/pathable/example4-along-line.svg)

**Formula**:
```
P(t) = P₀ + t(P₁ - P₀)
     = (1-t)P₀ + tP₁

Where:
  P₀ = start point
  P₁ = end point
  t ∈ [0, 1]
```

### Curve

Quadratic Bézier curve.

```python
curve = Curve(x1=0, y1=100, x2=100, y2=0, curvature=0.5)

# Get points along curve
for i in range(5):
    t = i / 4
    point = curve.point_at(t)
```

![Curve Point At Example](./_images/pathable/example2-curve-point-at.svg)

![Along Curve Example](./_images/pathable/example5-along-curve.svg)

**Formula**:
```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂

Where:
  P₀ = start point
  P₁ = control point
  P₂ = end point
  t ∈ [0, 1]
```

### Ellipse

Parametric ellipse with rotation support.

```python
ellipse = Ellipse(x=100, y=100, rx=30, ry=20, rotation=45)

# Get points around perimeter
point_0 = ellipse.point_at(0.0)    # Right (0°)
point_25 = ellipse.point_at(0.25)  # Top (90°)
point_50 = ellipse.point_at(0.5)   # Left (180°)
point_75 = ellipse.point_at(0.75)  # Bottom (270°)

# Or use angle directly
point_45 = ellipse.point_at_angle(45)  # 45° from right
```

![Ellipse Point At Example](./_images/pathable/example3-ellipse-point-at.svg)

![Along Ellipse Example](./_images/pathable/example6-along-ellipse.svg)

**Formula**:
```
Unrotated:
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)

With rotation θ:
x'(t) = x(t)cos(θ) - y(t)sin(θ) + cx
y'(t) = x(t)sin(θ) + y(t)cos(θ) + cy

Where:
  rx, ry = horizontal/vertical radii
  cx, cy = center coordinates
  θ = rotation in radians
  t ∈ [0, 1] maps to [0°, 360°]
```

---

## Using with `along=` Parameter

All `cell.add_*` methods that create dots support the `along=` parameter:

```python
# Create path
path = cell.add_curve(curvature=0.5, color="gray")

# Position dot along path
cell.add_dot(
    along=path,
    t=0.5,
    radius=4,
    color="red"
)
```

**Example - Multiple dots along curve**:
```python
curve = cell.add_curve(
    start="left",
    end="right",
    curvature=0.5,
    color=colors.line
)

# Position 5 dots evenly along curve
for i in range(5):
    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0

    cell.add_dot(
        along=curve,
        t=t,
        radius=3,
        color=colors.accent
    )
```

![Varying Sizes Example](./_images/pathable/example7-varying-sizes.svg)

![Comparison Example](./_images/pathable/example8-comparison.svg)

![Complex Example](./_images/pathable/example9-complex.svg)

---

## Custom Pathable Classes

You can create custom paths by implementing the Pathable protocol. See full examples in the [Custom Paths guide](../parametric-art/05-custom-paths.md).

---

## See Also

- 📖 [Pathable Protocol Guide](../advanced-concepts/03-pathable-protocol.md) - Detailed usage
- 📖 [Parametric Art](../parametric-art/01-what-is-parametric.md) - Conceptual overview
- 📖 [Custom Paths](../parametric-art/05-custom-paths.md) - Creating custom paths
- 🎯 [Custom Paths Example](../examples/advanced/custom-paths.md) - Full examples

