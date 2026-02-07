
# Example: Parametric Paths

**Difficulty**: ⭐⭐⭐ Advanced

Master the unified parametric interface that works across Lines, Curves, and Ellipses.

---

## What You'll Learn

- The Pathable protocol
- Unified `point_at(t)` interface
- Positioning entities along any path type
- Comparing different path behaviors
- Creating path-driven artwork

---

## Final Result

![Unified Interface](../_images/parametric-paths/01_unified_interface.svg)

### More Examples

| Unified Interface | Path Comparison |
|-------------------|-----------------|
| ![Example 1](../_images/parametric-paths/01_unified_interface.svg) | ![Example 2](../_images/parametric-paths/02_path_comparison.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette
import math

scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
colors = Palette.midnight()
scene.background = colors.background

# Demonstrate all three path types in parallel
start_row = 3
path_spacing = 5

# Path 1: Line (Linear interpolation)
for col in range(5, 15):
    cell = scene.grid[start_row, col]

    if col == 5:  # First cell
        line = cell.add_line(
            start="left",
            end=(9.5, 0.5),  # Extend to right edge of last cell
            color=colors.line,
            width=2,
            z_index=0
        )

    # Position dots along line
    t = (col - 5) / 9
    cell.add_dot(
        along=line,
        t=t,
        radius=4,
        color=colors.primary,
        z_index=5
    )

# Path 2: Curve (Bézier interpolation)
for col in range(5, 15):
    cell = scene.grid[start_row + path_spacing, col]

    if col == 5:  # First cell
        curve = cell.add_curve(
            start="left",
            end=(9.5, 0.5),
            curvature=0.8,  # Strong curve
            color=colors.line,
            width=2,
            z_index=0
        )

    # Position dots along curve
    t = (col - 5) / 9
    cell.add_dot(
        along=curve,
        t=t,
        radius=4,
        color=colors.secondary,
        z_index=5
    )

# Path 3: Ellipse (Circular/orbital interpolation)
center_cell = scene.grid[start_row + path_spacing * 2, 10]
ellipse = center_cell.add_ellipse(
    rx=center_cell.width * 4,
    ry=center_cell.height * 2.5,
    rotation=0,
    fill=None,
    stroke=colors.line,
    stroke_width=2,
    z_index=0
)

# Position dots around ellipse
for i in range(8):
    t = i / 8
    point = ellipse.point_at(t)

    from pyfreeform import Dot
    dot = Dot(
        x=point.x,
        y=point.y,
        radius=4,
        color=colors.accent,
        z_index=5
    )
    scene.add(dot)

# Add labels
from pyfreeform import Text
labels = [
    (10, start_row + 1, "Linear Path (Line)"),
    (10, start_row + path_spacing + 1, "Curved Path (Bézier)"),
    (10, start_row + path_spacing * 2 + 3, "Orbital Path (Ellipse)"),
]

for col, row, label in labels:
    text = Text(
        x=scene.grid[row, col].center.x,
        y=scene.grid[row, col].center.y,
        content=label,
        font_size=8,
        color=colors.line,
        font_family="sans-serif",
        text_anchor="middle",
        z_index=10
    )
    scene.add(text)

scene.save("parametric_paths.svg")
```

---

## The Pathable Protocol

All path entities implement `point_at(t)`:

```python
# Works with Lines
point = line.point_at(0.5)  # Midpoint

# Works with Curves
point = curve.point_at(0.5)  # Midpoint along curve

# Works with Ellipses
point = ellipse.point_at(0.5)  # Left side (180°)

# Same interface, different behaviors!
```

**Key Insight:** The parameter `t ∈ [0, 1]` is universal, but what it means varies by path type.

---

## Path-Specific Behaviors

### Line: Linear Interpolation

```python
line = cell.add_line(start="left", end="right")

# t=0.0 → start point (left)
# t=0.5 → exact midpoint
# t=1.0 → end point (right)

# Formula: P(t) = start + (end - start) × t
```

**Uniform distribution:** Equal spacing in t gives equal spatial spacing.

### Curve: Bézier Interpolation

```python
curve = cell.add_curve(start="left", end="right", curvature=0.5)

# t=0.0 → start point
# t=0.5 → NOT the visual midpoint!
# t=1.0 → end point

# Formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
```

**Non-uniform distribution:** Equal spacing in t does NOT give equal spatial spacing due to Bézier mathematics.

### Ellipse: Angular Interpolation

```python
ellipse = cell.add_ellipse(rx=15, ry=10)

# t=0.0   → right (0°)
# t=0.25  → top (90°)
# t=0.5   → left (180°)
# t=0.75  → bottom (270°)
# t=1.0   → back to right (360°)

# Angle = t × 360°
```

**Circular distribution:** t maps to angle around perimeter.

---

## Positioning Patterns

### Pattern 1: Uniform t Spacing

```python
# Same code, different visual results
for path in [line, curve, ellipse]:
    for i in range(10):
        t = i / 9
        cell.add_dot(along=path, t=t, radius=3, color=colors.primary)

# Line: Evenly spaced dots
# Curve: Clustered near control point
# Ellipse: Evenly spaced by angle
```

### Pattern 2: Brightness-Driven Position

```python
for cell in scene.grid:
    curve = cell.add_curve(start="left", end="right", curvature=0.5)

    # Brightness controls position
    cell.add_dot(
        along=curve,
        t=cell.brightness,  # 0.0 to 1.0
        radius=4,
        color=colors.primary
    )
```

### Pattern 3: Multi-Path Comparison

```python
def compare_paths(cell):
    """Show same t values on different paths."""
    line = cell.add_line(start="top", end="bottom", color="gray")
    curve = cell.add_curve(start="left", end="right", curvature=0.5, color="blue")

    # Same t values
    for i in range(5):
        t = i / 4

        # Different positions!
        cell.add_dot(along=line, t=t, radius=2, color="red")
        cell.add_dot(along=curve, t=t, radius=2, color="yellow")
```

---

## Try It Yourself

### Experiment 1: Path Morphing

```python
# Gradually increase curvature
for col, curvature in enumerate([0, 0.2, 0.4, 0.6, 0.8, 1.0]):
    cell = scene.grid[5, col]

    curve = cell.add_curve(
        start="bottom",
        end="top",
        curvature=curvature,
        color=colors.line
    )

    # Same t values, different paths
    for i in range(5):
        t = i / 4
        cell.add_dot(along=curve, t=t, radius=3, color=colors.primary)
```

### Experiment 2: Ellipse Orbits

```python
# Dots orbiting at different rates
center_cell = scene.grid[10, 10]

for radius_mult in [0.5, 0.75, 1.0, 1.25]:
    ellipse = center_cell.add_ellipse(
        rx=center_cell.width * radius_mult,
        ry=center_cell.height * radius_mult
    )

    # Different speeds by changing t increment
    for i in range(int(radius_mult * 8)):
        t = i / (radius_mult * 8)
        cell.add_dot(along=ellipse, t=t, radius=2, color=colors.primary)
```

### Experiment 3: All Paths, All Positions

```python
paths = [
    line,
    curve,
    ellipse
]

for path_idx, path in enumerate(paths):
    for t_idx in range(10):
        t = t_idx / 9

        # Position varies by path type
        point = path.point_at(t)

        dot = Dot(
            x=point.x,
            y=point.y,
            radius=3,
            color=colors.primary if path_idx == 0 else
                  colors.secondary if path_idx == 1 else
                  colors.accent
        )
        scene.add(dot)
```

---

## Advanced: Custom Paths

You can create custom paths by implementing `point_at(t)`:

```python
class SpiralPath:
    def __init__(self, center, max_radius, turns):
        self.center = center
        self.max_radius = max_radius
        self.turns = turns

    def point_at(self, t):
        """Spiral outward as t increases."""
        angle = t * self.turns * 2 * math.pi
        radius = t * self.max_radius

        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)

        return Point(x, y)

# Use like any other path
spiral = SpiralPath(center=cell.center, max_radius=50, turns=3)
cell.add_dot(along=spiral, t=0.5, radius=4)  # Works!
```

---

## Related

- 📖 [Pathable Protocol](../../advanced-concepts/03-pathable-protocol.md) - Technical details
- 📖 [Lines](../../entities/02-lines.md) - Linear paths
- 📖 [Curves](../../entities/03-curves.md) - Bézier paths
- 📖 [Ellipses](../../entities/04-ellipses.md) - Circular paths
- 🎯 [Custom Paths Example](custom-paths.md) - Spirals, waves, Lissajous
- 🎨 [Parametric Art Guide](../../parametric-art/01-what-is-parametric.md) - Math background

[← Back: Showcase](showcase.md) | [Home](../../index.md) | [Examples Index](../index.md)
