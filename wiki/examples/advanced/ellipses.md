
# Example: Ellipses

**Difficulty**: 🚀 Advanced

Master parametric ellipse mathematics with rotation, orbital positioning, and radial compositions.

---

## What You'll Learn

- Parametric ellipse equations
- Rotation matrices and transformations
- `point_at(t)` and `point_at_angle()` methods
- Creating radial/orbital compositions
- Auto-fitting rotated ellipses with `fit_to_cell()`

---

## Final Result

![Radial Ellipses](../_images/ellipses/01_radial_ellipses.svg)

### More Examples

| Radial Ellipses | Orbital Rings | Parametric Dots |
|-----------------|---------------|-----------------|
| ![Example 1](../_images/ellipses/01_radial_ellipses.svg) | ![Example 2](../_images/ellipses/02_orbital_rings.svg) | ![Example 3](../_images/ellipses/03_parametric_dots.svg) |

---

## Step-by-Step Breakdown

### Step 1: Setup

```python
from pyfreeform import Scene, Palette
import math

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

# Calculate grid center
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2
```

### Step 2: Create Rotating Ellipses

```python
for cell in scene.grid:
    # Calculate position relative to center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = math.sqrt(dr*dr + dc*dc)
    angle = math.degrees(math.atan2(dr, dc))

    # Size based on brightness
    scale = 0.3 + cell.brightness * 0.7

    # Create rotated ellipse pointing toward/away from center
    ellipse = cell.add_ellipse(
        rx=15,
        ry=8,
        rotation=angle,  # Points radially
        fill=cell.color,
        z_index=1
    )

    # Auto-fit to cell (handles rotation automatically)
    ellipse.fit_to_cell(scale)
```

**What's happening:**
- `atan2(dr, dc)` calculates angle from center to cell
- `rotation=angle` makes ellipse point radially outward
- `fit_to_cell(scale)` constrains ellipse within cell bounds
- Even though rotated, `fit_to_cell()` calculates correct bounding box

**The Mathematics - Angle Calculation:**
```
angle = atan2(Δy, Δx)

Example:
Center: (10, 10)
Cell: (15, 20)

Δy = 15 - 10 = 5
Δx = 20 - 10 = 10

angle = atan2(5, 10) ≈ 0.464 rad ≈ 26.6°
```

### Step 3: Position Dots on Ellipse Perimeter

```python
    # Add dot on ellipse perimeter
    cell.add_dot(
        along=ellipse,
        t=cell.brightness,  # Position based on brightness
        radius=2,
        color=colors.accent,
        z_index=2
    )
```

**What's happening:**
- `along=ellipse` uses ellipse's parametric equation
- `t=cell.brightness` maps brightness (0-1) to position around perimeter
- Bright cells → dots near t=1.0 (back to start)
- Dark cells → dots near t=0.0 (start position)

**Parametric Ellipse Formula:**
```
Unrotated ellipse:
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)

With rotation θ (in radians):
x'(t) = cx + x(t)cos(θ) - y(t)sin(θ)
y'(t) = cy + x(t)sin(θ) + y(t)cos(θ)

Where:
  cx, cy = center coordinates
  rx, ry = horizontal/vertical radii
  θ = rotation angle in radians
  t ∈ [0, 1]

Parameter mapping:
t=0.0  → 0°   (right side)
t=0.25 → 90°  (top)
t=0.5  → 180° (left side)
t=0.75 → 270° (bottom)
t=1.0  → 360° (back to right)
```

### Step 4: Alternative - Using Angles Directly

```python
    # Create ellipse
    ellipse = cell.add_ellipse(rx=15, ry=10, rotation=45)

    # Position dots at specific angles
    dot_0 = ellipse.point_at_angle(0)    # Right
    dot_90 = ellipse.point_at_angle(90)  # Top
    dot_180 = ellipse.point_at_angle(180)  # Left
    dot_270 = ellipse.point_at_angle(270)  # Bottom

    # Add dots at these positions
    scene.add(Dot(x=dot_0.x, y=dot_0.y, radius=2))
    scene.add(Dot(x=dot_90.x, y=dot_90.y, radius=2))
```

---

## Complete Code

```python
from pyfreeform import Scene, Palette
import math

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.ocean()
scene.background = colors.background

center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    # Calculate position relative to center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = math.sqrt(dr*dr + dc*dc)
    angle = math.degrees(math.atan2(dr, dc))

    # Size based on brightness
    scale = 0.3 + cell.brightness * 0.7

    # Create rotated ellipse pointing toward/away from center
    ellipse = cell.add_ellipse(
        rx=15,
        ry=8,
        rotation=angle,
        fill=cell.color,
        z_index=1
    )
    ellipse.fit_to_cell(scale)

    # Add dot on ellipse perimeter
    cell.add_dot(
        along=ellipse,
        t=cell.brightness,
        radius=2,
        color=colors.accent,
        z_index=2
    )

scene.save("radial_ellipses.svg")
```

---

## Try It Yourself

### Experiment 1: Orbital Rings

Create concentric orbital rings:

```python
# Distance-based rotation
rotation = distance * 30  # Spins faster farther from center

ellipse = cell.add_ellipse(
    rx=12,
    ry=6,
    rotation=rotation,
    fill=cell.color
)
```

### Experiment 2: Multiple Dots Around Perimeter

```python
ellipse = cell.add_ellipse(rx=15, ry=10)

# Position 8 dots evenly around perimeter
for i in range(8):
    t = i / 8

    cell.add_dot(
        along=ellipse,
        t=t,
        radius=2,
        color=colors.accent
    )
```

### Experiment 3: Eccentricity Variation

```python
# Eccentricity based on distance from center
e = min(distance / 10, 0.9)  # 0 to 0.9

# Calculate radii for desired eccentricity
# For ellipse: e = √(1 - (ry/rx)²)
rx = 15
ry = rx * math.sqrt(1 - e*e)

ellipse = cell.add_ellipse(
    rx=rx,
    ry=ry,
    rotation=angle,
    fill=cell.color
)
```

### Challenge: Lissajous Pattern

Create Lissajous curves using multiple rotating ellipses:

```python
# Create invisible guide ellipse
guide = cell.add_ellipse(
    rx=12,
    ry=8,
    rotation=0,
    fill=None,
    stroke=None
)

# Position multiple dots in Lissajous pattern
for i in range(20):
    t = i / 20

    # Lissajous parameters
    a = 3  # Frequency ratio
    b = 2
    delta = math.pi / 2  # Phase shift

    # Custom t parameter
    liss_t = (math.sin(a * t * 2 * math.pi + delta) + 1) / 2

    cell.add_dot(
        along=guide,
        t=liss_t,
        radius=1,
        color=colors.primary
    )
```

---

## Mathematical Deep Dive

### Rotation Matrix

The 2D rotation transformation:

```
[x']   [cos(θ)  -sin(θ)] [x]
[y'] = [sin(θ)   cos(θ)] [y]

Expanded:
x' = x·cos(θ) - y·sin(θ)
y' = x·sin(θ) + y·cos(θ)
```

This is how PyFreeform rotates ellipse points.

### Eccentricity

The eccentricity measures how "stretched" an ellipse is:

```
e = √(1 - (b/a)²)   where a > b

e = 0     : Perfect circle (rx == ry)
0 < e < 1 : Ellipse
e = 1     : Parabola (theoretical limit)

Example:
rx = 15, ry = 8
e = √(1 - (8/15)²) = √(1 - 0.284) = √0.716 ≈ 0.846
```

### Arc Length

The exact perimeter requires an elliptic integral. Ramanujan's approximation:

```
P ≈ π[3(a+b) - √((3a+b)(a+3b))]

Where:
  a = rx (semi-major axis)
  b = ry (semi-minor axis)
```

---

## Related

- 📖 [Ellipses Entity](../../entities/04-ellipses.md) - Ellipse documentation
- 📖 [Ellipse Mathematics](../../parametric-art/04-ellipse-mathematics.md) - Mathematical deep dive
- 📖 [Pathable Protocol](../../advanced-concepts/03-pathable-protocol.md) - Parametric positioning
- 📖 [Transforms](../../advanced-concepts/04-transforms.md) - Rotation details

