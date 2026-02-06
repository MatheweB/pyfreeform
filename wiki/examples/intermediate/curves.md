
# Example: Curves

**Difficulty**: ⭐ Intermediate

Create flowing compositions using quadratic Bézier curves with variable curvature.

---

## What You'll Learn

- Creating curves with `cell.add_curve()`
- Controlling curvature parameter
- Positioning dots along curves with `along=` and `t=`
- Brightness-driven parametric positioning

---

## Final Result

![Flowing Curves](../_images/curves/01_flowing_curves.svg)

### More Examples

| Flowing Curves | Varying Curvature | Multiple Dots |
|----------------|-------------------|---------------|
| ![Example 1](../_images/curves/01_flowing_curves.svg) | ![Example 2](../_images/curves/02_varying_curvature.svg) | ![Example 3](../_images/curves/03_multiple_dots.svg) |

---

## Step-by-Step Breakdown

### Step 1: Setup Scene

```python
from pyfreeform import Scene, Palette

# Load image and create grid
scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background
```

**What's happening:**
- `from_image()` creates a scene from an image
- Each cell gets brightness and color data from the image
- `grid_size=30` makes cells 30×30 pixels
- Ocean palette provides a cohesive color scheme

### Step 2: Create Curves

```python
for cell in scene.grid:
    # Only draw in medium brightness areas
    if 0.3 < cell.brightness < 0.7:
        # Create curve
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.5,  # Positive = bows left
            color=colors.line,
            width=1,
            z_index=1
        )
```

**What's happening:**
- Filter cells by brightness range (0.3 to 0.7)
- `add_curve()` creates a quadratic Bézier curve
- `start` and `end` use named positions
- `curvature=0.5` creates a moderate bow
- `z_index=1` places curve above background

**The Mathematics:**
```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂

Where:
  P₀ = start point (bottom_left)
  P₁ = control point (calculated from curvature)
  P₂ = end point (top_right)
  t ∈ [0,1]
```

### Step 3: Position Dot Along Curve

```python
        # Add dot positioned along the curve
        cell.add_dot(
            along=curve,
            t=cell.brightness,  # Brightness drives position (0-1)
            radius=2,
            color=colors.accent,
            z_index=2
        )
```

**What's happening:**
- `along=curve` tells the dot to position on the curve
- `t=cell.brightness` uses brightness (0-1) as the parameter
- Bright cells → dot near end of curve
- Dark cells → dot near start of curve
- `z_index=2` places dot on top of curve

**Visual Effect:**
```
Brightness: 0.2 → Dot at t=0.2 (20% along curve)
Brightness: 0.5 → Dot at t=0.5 (50% along curve)
Brightness: 0.8 → Dot at t=0.8 (80% along curve)
```

### Step 4: Save

```python
scene.save("flowing_curves.svg")
```

---

## Complete Code

```python
from pyfreeform import Scene, Palette

# Create scene from image
scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Only draw in certain brightness range
    if 0.3 < cell.brightness < 0.7:
        # Create curve
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.5,
            color=colors.line,
            width=1,
            z_index=1
        )

        # Add dot along curve, positioned by brightness
        cell.add_dot(
            along=curve,
            t=cell.brightness,
            radius=2,
            color=colors.accent,
            z_index=2
        )

scene.save("flowing_curves.svg")
```

---

## Try It Yourself

### Experiment 1: Vary Curvature

```python
# Negative curvature bows the other way
curve = cell.add_curve(curvature=-0.5, ...)

# Strong curvature creates dramatic bows
curve = cell.add_curve(curvature=1.0, ...)

# Straight line (no curve)
curve = cell.add_curve(curvature=0.0, ...)
```

### Experiment 2: Multiple Dots

```python
# Position 5 dots along the curve
for i in range(5):
    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0

    cell.add_dot(
        along=curve,
        t=t,
        radius=2,
        color=colors.accent
    )
```

### Experiment 3: Variable Curvature

```python
# Curvature varies across the grid
curvature = (cell.col / scene.grid.cols - 0.5) * 2  # -1 to 1

curve = cell.add_curve(
    curvature=curvature,  # Changes per cell
    color=colors.line
)
```

### Challenge: Flowing Wave

Create a wave pattern by varying curvature with a sine wave:

```python
import math

for cell in scene.grid:
    # Sine wave curvature
    phase = cell.col / scene.grid.cols * math.pi * 2
    curvature = math.sin(phase) * 0.5

    curve = cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color
    )
```

---

## Related

- 📖 [Curves Entity](../../entities/03-curves.md) - Curve documentation
- 📖 [Pathable Protocol](../../advanced-concepts/03-pathable-protocol.md) - Positioning along paths
- 🎨 [Bézier Mathematics](../../parametric-art/03-bezier-mathematics.md) - Mathematical deep dive
- 🎯 [Flowing Curves Recipe](../../recipes/03-flowing-curves.md) - More patterns

