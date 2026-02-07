
# Curves

Curves bring organic, flowing shapes to your artwork using quadratic Bézier mathematics. Perfect for smooth paths, flowing compositions, and natural-looking connections.

---

## What is a Curve?

A **Curve** is a smooth, parametric path defined by:
- **Start point** - Beginning of the curve
- **End point** - End of the curve
- **Control point** - Determines the curve's bow (calculated from curvature)
- **Curvature** - How much the curve bows away from a straight line

Curves use quadratic Bézier mathematics to create smooth, controllable paths.

---

## The Mathematics Behind Curves

### Quadratic Bézier Formula

PyFreeform curves use the quadratic Bézier equation:

```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂

Where:
  t ∈ [0,1]  : Parameter along the curve
  P₀         : Start point
  P₁         : Control point
  P₂         : End point
```

**Expanded form:**

```
x(t) = (1-t)²·x₀ + 2(1-t)t·x₁ + t²·x₂
y(t) = (1-t)²·y₀ + 2(1-t)t·y₁ + t²·y₂
```

**How it works:**
- At `t=0`: B(0) = P₀ (start point)
- At `t=0.5`: B(0.5) = midpoint influenced by control point
- At `t=1`: B(1) = P₂ (end point)

The control point P₁ "pulls" the curve toward it, creating the smooth bow.

![Curvature Comparison](./_images/03-curves/01_curvature_comparison.svg)

### Control Point Calculation

The control point is calculated from the **curvature parameter**:

```
1. midpoint = (P₀ + P₂) / 2

2. direction = P₂ - P₀
   length = ||direction||

3. perpendicular = rotate(direction, 90°)
   normalized_perp = perpendicular / length

4. offset = curvature × length × 0.5

5. control = midpoint + normalized_perp × offset
```

**In code** (from [curve.py:134-157](https://github.com/pyfreeform/pyfreeform/blob/main/src/pyfreeform/entities/curve.py)):

```python
def _calculate_control(self) -> Point:
    # Midpoint of start and end
    mid = self.start.midpoint(self.end)

    if self.curvature == 0:
        return mid  # Straight line

    # Vector from start to end
    dx = self.end.x - self.start.x
    dy = self.end.y - self.start.y
    length = sqrt(dx**2 + dy**2)

    # Perpendicular vector (rotate 90° counterclockwise)
    perp_x = -dy / length
    perp_y = dx / length

    # Offset by curvature * half the length
    offset = self.curvature * length * 0.5

    return Point(
        mid.x + perp_x * offset,
        mid.y + perp_y * offset
    )
```

![Control Point Visualization](./_images/03-curves/02_control_point_visualization.svg)

### Curvature Parameter

!!! note "Understanding Curvature"
    The `curvature` parameter controls the bow:

    ```
    curvature = 0     : Straight line (no curve)
    curvature > 0     : Bows to the left (when facing end point)
    curvature < 0     : Bows to the right
    curvature = ±1    : Standard bow (common range: -1 to 1)
    ```

**Visual examples:**

```
curvature = 0       curvature = 0.5      curvature = -0.5
(straight)          (left bow)           (right bow)

P₀ ────── P₂       P₀           P₂      P₀           P₂
                        ╲       ╱              ╲   ╱
                         ╲     ╱                ╲ ╱
                          ╲   ╱                  ╳
                           ╲ ╱                  ╱ ╲
                            P₁                 ╱   ╲
                                              P₁
```

---

## Creating Curves

### Via Cell Method (Recommended)

```python
# Basic curve
cell.add_curve(
    start="bottom_left",
    end="top_right",
    curvature=0.5,
    color="blue",
    width=2
)

# Curve from relative coordinates
cell.add_curve(
    start=(0.2, 0.8),
    end=(0.8, 0.2),
    curvature=0.5
)
```

### Direct Construction

```python
from pyfreeform import Curve

# From coordinates
curve = Curve(x1=0, y1=100, x2=100, y2=0, curvature=0.5)

# From points
from pyfreeform.core.point import Point
curve = Curve.from_points(
    start=Point(0, 100),
    end=Point(100, 0),
    curvature=0.5
)

scene.add(curve)
```

---

## Properties

```python
curve.start        # Start point (Point object)
curve.end          # End point (Point object)
curve.control      # Control point (calculated)
curve.curvature    # Curvature amount
curve.color        # Stroke color
curve.width        # Stroke width
curve.z_index      # Layer order
```

### Modifying Properties

```python
curve = cell.add_curve(curvature=0.5, color="blue")

# Change curvature
curve.curvature = -0.5  # Flip the bow

# Change endpoints
curve.end = Point(200, 300)

# Change styling
curve.color = "red"
curve.width = 3
```

---

## Parametric Positioning

!!! tip "The Killer Feature"
    Position elements along the curve:

```python
# Create curve
curve = cell.add_curve(
    start="left",
    end="right",
    curvature=0.5
)

# Get point at parameter t (0 to 1)
point = curve.point_at(0.5)  # Midpoint of curve

# Position dots along curve
for i in range(5):
    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0
    cell.add_dot(
        along=curve,
        t=t,
        radius=3,
        color="red"
    )
```

**Mathematical implementation:**

```python
def point_at(self, t: float) -> Point:
    """Get point on curve at parameter t."""
    p0, p1, p2 = self.start, self.control, self.end

    mt = 1 - t
    mt2 = mt * mt    # (1-t)²
    t2 = t * t        # t²

    # Quadratic Bézier formula
    x = mt2 * p0.x + 2 * mt * t * p1.x + t2 * p2.x
    y = mt2 * p0.y + 2 * mt * t * p1.y + t2 * p2.y

    return Point(x, y)
```

---

## Anchors

Curves provide these anchor points:

```python
curve.anchor_names  # ["start", "center", "end", "control"]

curve.anchor("start")    # Start point
curve.anchor("center")   # Midpoint (t=0.5)
curve.anchor("end")      # End point
curve.anchor("control")  # Control point (off the curve)
```

---

## Common Patterns

### Pattern 1: Brightness-Driven Positioning

```python
for cell in scene.grid:
    curve = cell.add_curve(
        start="bottom_left",
        end="top_right",
        curvature=0.5,
        color="gray"
    )

    # Dot slides along curve based on brightness
    cell.add_dot(
        along=curve,
        t=cell.brightness,  # 0.0 to 1.0
        radius=4,
        color="red"
    )
```

![Brightness-Driven Curves](./_images/03-curves/03_brightness_driven.svg)

### Pattern 2: Variable Curvature

```python
for cell in scene.grid:
    # Curvature varies across the grid
    curvature = (cell.col / scene.grid.cols - 0.5) * 2  # -1 to 1

    curve = cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color
    )
```

Creates a flowing wave pattern across the grid.

![Variable Curvature](./_images/03-curves/04_variable_curvature.svg)

### Pattern 3: Multiple Dots Along Curve

```python
for cell in scene.grid:
    if cell.brightness > 0.4:
        curve = cell.add_curve(curvature=0.5, color="lightgray")

        # Position multiple dots
        for i in range(5):
            t = i / 4
            cell.add_dot(
                along=curve,
                t=t,
                radius=2,
                color="coral"
            )
```

![Multiple Dots Along Curve](./_images/03-curves/05_multiple_dots_along_curve.svg)

### Pattern 4: Connecting Cells

```python
for cell in scene.grid:
    if cell.right:  # Has neighbor to the right
        # Curve from this cell to neighbor
        curve = Curve.from_points(
            start=cell.center,
            end=cell.right.center,
            curvature=0.3,
            color="blue",
            width=1
        )
        scene.add(curve)
```

---

## Mathematical Exploration

### Visualizing the Bézier Formula

The quadratic Bézier is a weighted average of three points:

```
At t=0.0:  All weight on P₀ (start)
At t=0.25: Mostly P₀, some P₁, little P₂
At t=0.5:  Balanced blend (closer to P₁)
At t=0.75: Mostly P₂, some P₁, little P₀
At t=1.0:  All weight on P₂ (end)
```

**Weight distribution:**

```python
# Weights at t=0.5
(1-0.5)² = 0.25       # Weight on P₀ (start)
2(1-0.5)(0.5) = 0.50  # Weight on P₁ (control)
(0.5)² = 0.25         # Weight on P₂ (end)
# Total = 1.0
```

### Derivatives (Advanced)

The first derivative gives the tangent (velocity) along the curve:

```
B'(t) = 2(1-t)(P₁ - P₀) + 2t(P₂ - P₁)
```

Useful for:
- Computing normals (perpendicular directions)
- Arc length approximation
- Velocity-based animations

### Arc Length (Advanced)

The exact arc length requires numerical integration. Approximation:

```python
def approximate_length(curve, segments=10):
    length = 0
    prev = curve.point_at(0)

    for i in range(1, segments + 1):
        t = i / segments
        curr = curve.point_at(t)
        length += prev.distance_to(curr)
        prev = curr

    return length
```

---

## Styling Curves

```python
from pyfreeform.config import LineStyle

# Create reusable style
style = LineStyle(
    width=2,
    color="navy",
    cap="round"  # "round", "square", or "butt"
)

cell.add_curve(
    start="left",
    end="right",
    curvature=0.5,
    style=style
)
```

---

## Complete Example

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Only in medium brightness areas
    if 0.3 < cell.brightness < 0.7:
        # Curvature driven by brightness
        curvature = (cell.brightness - 0.5) * 2  # -0.4 to 0.4

        # Create curve
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            color=colors.line,
            width=1,
            z_index=1
        )

        # Add dots along curve
        for i in range(3):
            t = i / 2  # 0, 0.5, 1.0
            cell.add_dot(
                along=curve,
                t=t,
                radius=2,
                color=colors.accent,
                z_index=2
            )

scene.save("flowing_curves.svg")
```

![Complete Example](./_images/03-curves/06_complete_example.svg)

---

## Tips and Best Practices

!!! tip "Keep Curvature in Range"
    Keep curvature in the -1 to 1 range for natural-looking curves:

```python
# Good - natural curves
curvature = 0.5

# Extreme - can create loops or sharp bends
curvature = 3.0
```

### Use with Image Data

Brightness makes great parametric drivers:

```python
curve = cell.add_curve(curvature=0.5)
cell.add_dot(along=curve, t=cell.brightness)  # Smooth distribution
```

### Visualize Control Points

For debugging, show the control point:

```python
curve = cell.add_curve(curvature=0.5, color="blue")
control = curve.anchor("control")
cell.add_dot(at=control, radius=2, color="red", z_index=10)
```

### Combine with Straight Lines

Mix curves and lines for variety:

```python
if cell.brightness > 0.5:
    cell.add_curve(curvature=0.5)
else:
    cell.add_line(start="left", end="right")
```

---

## Next Steps

- **Explore ellipses**: [Ellipses](04-ellipses.md) - More parametric math
- **Learn the protocol**: [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
- **Deep dive**: [Bézier Mathematics](../parametric-art/03-bezier-mathematics.md)
- **See examples**: [Curves Example](../examples/intermediate/curves.md)

---

!!! tip "Curves as Paths and Along Paths"
    Curves implement the **Pathable** protocol — use them as paths for `along=` positioning.
    Curves can also be **placed along** other paths: `cell.add_curve(along=path, t=0.5, align=True)`.
    See [Positioning Along Paths](../parametric-art/02-positioning-along-paths.md).

## See Also

- 📖 [Ellipses](04-ellipses.md) - Parametric ellipse equations
- 📖 [Lines](02-lines.md) - Straight paths
- 📖 [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
- 🎨 [Bézier Mathematics](../parametric-art/03-bezier-mathematics.md)
- 🎯 [Curves Example](../examples/intermediate/curves.md)
- 🎯 [Parametric Paths Example](../examples/advanced/parametric-paths.md)
- 🔍 [Curve API Reference](../api-reference/entities.md#curve)

