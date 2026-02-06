
# Ellipses

Ellipses bring rotatable ovals and circles to your artwork with powerful parametric positioning. Perfect for radial compositions, orbits, and dynamic rotations.

---

## What is an Ellipse?

An **Ellipse** is an oval or circle entity defined by:
- **Center** - Position (x, y)
- **rx** - Horizontal radius (half-width)
- **ry** - Vertical radius (half-height)
- **Rotation** - Angle in degrees
- **Fill** - Interior color
- **Stroke** - Border color (optional)

Ellipses support parametric positioning around their perimeter, making them powerful for creating radial patterns and animations.

![Circles vs Ellipses](./_images/04-ellipses/01_circles_vs_ellipses.svg)

---

## The Mathematics Behind Ellipses

### Parametric Ellipse Equations

An ellipse is defined parametrically by these equations:

**Unrotated ellipse:**

```
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)

Where:
  t ∈ [0,1]  : Parameter around the ellipse
  rx         : Horizontal radius
  ry         : Vertical radius
  t=0        : Right side (0°)
  t=0.25     : Top (90°)
  t=0.5      : Left side (180°)
  t=0.75     : Bottom (270°)
  t=1        : Back to right (360°)
```

**With rotation θ (in radians):**

```
x'(t) = x(t)·cos(θ) - y(t)·sin(θ) + cx
y'(t) = x(t)·sin(θ) + y(t)·cos(θ) + cy

Where:
  θ  : Rotation angle
  cx : Center x coordinate
  cy : Center y coordinate
```

**Full formula with rotation:**

```
x'(t) = cx + rx·cos(2πt)·cos(θ) - ry·sin(2πt)·sin(θ)
y'(t) = cy + rx·cos(2πt)·sin(θ) + ry·sin(2πt)·cos(θ)
```

### Alternative: Angle-Based Positioning

You can also specify positions by angle in degrees:

```
angle_rad = angle_deg × π/180

x = rx × cos(angle_rad)
y = ry × sin(angle_rad)

# Then apply rotation transformation
```

### In PyFreeform Code

From [ellipse.py](https://github.com/pyfreeform/pyfreeform/blob/main/src/pyfreeform/entities/ellipse.py):

```python
def point_at(self, t: float) -> Point:
    """Get point at parameter t (0 to 1) around ellipse."""
    # Convert t to angle (0 to 2π)
    angle = t * 2 * math.pi

    # Unrotated ellipse point
    x = self.rx * math.cos(angle)
    y = self.ry * math.sin(angle)

    # Apply rotation if needed
    if self.rotation != 0:
        rot_rad = math.radians(self.rotation)
        cos_r = math.cos(rot_rad)
        sin_r = math.sin(rot_rad)

        # Rotation matrix
        x_rot = x * cos_r - y * sin_r
        y_rot = x * sin_r + y * cos_r

        x, y = x_rot, y_rot

    # Translate to center
    return Point(self.position.x + x, self.position.y + y)


def point_at_angle(self, degrees: float) -> Point:
    """Get point at specific angle in degrees."""
    # Convert angle to radians
    angle_rad = math.radians(degrees)

    # Same as above but using direct angle
    x = self.rx * math.cos(angle_rad)
    y = self.ry * math.sin(angle_rad)

    # Apply rotation...
    # (same rotation logic)
```

---

## Creating Ellipses

### Via Cell Method (Recommended)

```python
# Circle (rx == ry)
cell.add_ellipse(rx=10, ry=10, fill="coral")

# Oval (rx != ry)
cell.add_ellipse(rx=15, ry=8, fill="blue")

# Rotated ellipse
cell.add_ellipse(
    rx=15,
    ry=8,
    rotation=45,  # degrees
    fill="purple"
)
```

![Rotation Angles](./_images/04-ellipses/02_rotation_angles.svg)

```python
# With stroke
cell.add_ellipse(
    rx=12,
    ry=12,
    fill="lightblue",
    stroke="navy",
    stroke_width=2
)
```

### Direct Construction

```python
from pyfreeform import Ellipse

# At specific position
ellipse = Ellipse(x=100, y=200, rx=20, ry=15, rotation=30)

# At center point
from pyfreeform.core.point import Point
ellipse = Ellipse.at_center(
    center=Point(100, 200),
    rx=20,
    ry=15,
    rotation=30
)

scene.add(ellipse)
```

---

## Properties

```python
ellipse.position    # Center point (Point object)
ellipse.x           # Center x coordinate
ellipse.y           # Center y coordinate
ellipse.rx          # Horizontal radius
ellipse.ry          # Vertical radius
ellipse.rotation    # Rotation in degrees
ellipse.fill        # Fill color
ellipse.stroke      # Stroke color (or None)
ellipse.stroke_width  # Stroke width
ellipse.z_index     # Layer order
```

### Modifying Properties

```python
ellipse = cell.add_ellipse(rx=15, ry=10)

# Change size
ellipse.rx = 20
ellipse.ry = 12

# Rotate
ellipse.rotation = 45

# Change colors
ellipse.fill = "coral"
ellipse.stroke = "darkred"
ellipse.stroke_width = 2
```

---

## Parametric Positioning

Position elements around the ellipse perimeter:

### Using Parameter t (0 to 1)

```python
ellipse = cell.add_ellipse(rx=15, ry=10)

# Position dots around ellipse
for i in range(8):
    t = i / 8  # 0, 0.125, 0.25, ..., 0.875
    cell.add_dot(
        along=ellipse,
        t=t,
        radius=2,
        color="red"
    )
```

![Parametric Positioning](./_images/04-ellipses/03_parametric_positioning.svg)

### Using Direct Angles

```python
ellipse = cell.add_ellipse(rx=15, ry=10, rotation=30)

# Position at specific angles
point_0 = ellipse.point_at_angle(0)    # Right
point_90 = ellipse.point_at_angle(90)  # Top
point_180 = ellipse.point_at_angle(180)  # Left
point_270 = ellipse.point_at_angle(270)  # Bottom
```

### Relationship Between t and Angle

```
t = 0    → angle = 0°   (right)
t = 0.25 → angle = 90°  (top)
t = 0.5  → angle = 180° (left)
t = 0.75 → angle = 270° (bottom)
t = 1.0  → angle = 360° (back to right)

angle_degrees = t × 360
```

---

## Anchors

Ellipses provide cardinal direction anchors:

```python
ellipse.anchor_names  # ["center", "right", "top", "left", "bottom"]

ellipse.anchor("center")  # Center point
ellipse.anchor("right")   # Rightmost point (0°)
ellipse.anchor("top")     # Topmost point (90°)
ellipse.anchor("left")    # Leftmost point (180°)
ellipse.anchor("bottom")  # Bottommost point (270°)
```

These automatically account for rotation!

---

## Common Patterns

### Pattern 1: Brightness-Sized Ellipses

```python
for cell in scene.grid:
    # Size based on brightness
    scale = 0.3 + cell.brightness * 0.7  # 30% to 100%

    ellipse = cell.add_ellipse(
        rx=cell.width * 0.4,
        ry=cell.height * 0.4,
        fill=cell.color
    )

    # Fit to cell with dynamic size
    ellipse.fit_to_cell(scale)
```

![Brightness-Sized Ellipses](./_images/04-ellipses/04_brightness_sized_ellipses.svg)

### Pattern 2: Rotating Ellipses

```python
for cell in scene.grid:
    # Rotation based on position
    rotation = (cell.row + cell.col) * 15  # degrees

    ellipse = cell.add_ellipse(
        rx=12,
        ry=8,
        rotation=rotation,
        fill=cell.color
    )
```

Creates a spiral rotation pattern across the grid.

![Rotating Ellipses](./_images/04-ellipses/05_rotating_ellipses.svg)

### Pattern 3: Orbiting Dots

```python
for cell in scene.grid:
    if cell.brightness > 0.5:
        # Create ellipse path
        ellipse = cell.add_ellipse(
            rx=10,
            ry=8,
            rotation=45,
            fill=None,  # Invisible path
            stroke="lightgray",
            stroke_width=0.5
        )

        # Position dot along ellipse based on brightness
        cell.add_dot(
            along=ellipse,
            t=cell.brightness,
            radius=3,
            color="red"
        )
```

![Orbiting Dots](./_images/04-ellipses/06_orbiting_dots.svg)

### Pattern 4: Radial Composition

```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    # Distance from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = (dr*dr + dc*dc) ** 0.5

    # Angle from center
    angle = math.atan2(dr, dc) * 180 / math.pi

    # Create rotated ellipse
    ellipse = cell.add_ellipse(
        rx=8,
        ry=5,
        rotation=angle,  # Points toward center
        fill=cell.color
    )
```

![Radial Composition](./_images/04-ellipses/07_radial_composition.svg)

---

## Mathematical Exploration

### Eccentricity

The eccentricity measures how "stretched" an ellipse is:

```
e = sqrt(1 - (ry/rx)²)   when rx > ry

e = 0     : Perfect circle (rx == ry)
0 < e < 1 : Ellipse
e = 1     : Parabola (theoretical limit)
```

**In PyFreeform:**

```python
def eccentricity(ellipse):
    if ellipse.rx == ellipse.ry:
        return 0  # Circle

    a = max(ellipse.rx, ellipse.ry)  # Semi-major axis
    b = min(ellipse.rx, ellipse.ry)  # Semi-minor axis

    return math.sqrt(1 - (b/a)**2)
```

### Perimeter Approximation

The exact perimeter of an ellipse requires an elliptic integral. Ramanujan's approximation:

```
P ≈ π[3(a+b) - sqrt((3a+b)(a+3b))]

Where:
  a = rx (semi-major axis)
  b = ry (semi-minor axis)
```

**Implementation:**

```python
def approximate_perimeter(ellipse):
    a, b = ellipse.rx, ellipse.ry
    h = ((a - b)**2) / ((a + b)**2)

    # Ramanujan's first approximation
    return math.pi * (a + b) * (1 + 3*h / (10 + math.sqrt(4 - 3*h)))
```

### Area

The exact area is simple:

```
A = π × rx × ry
```

**For circles:** `A = πr²` (special case where rx = ry = r)

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

---

## Auto-Fitting to Cells

Ellipses support automatic constraining:

```python
for cell in scene.grid:
    # Create large ellipse
    ellipse = cell.add_ellipse(
        rx=100,  # Way too large
        ry=60,
        rotation=45,
        fill=cell.color
    )

    # Auto-fit to 85% of cell
    # Handles rotation automatically!
    ellipse.fit_to_cell(0.85)
```

The `fit_to_cell()` method:
1. Calculates the rotated bounding box
2. Finds the scale factor to fit within the cell
3. Scales both rx and ry proportionally
4. Optionally recenters in the cell

---

## Circles vs. Ellipses

A circle is just an ellipse where rx == ry:

```python
# These are equivalent
circle = cell.add_ellipse(rx=10, ry=10)  # rx == ry
circle = cell.add_ellipse(rx=10, ry=10, rotation=0)  # Rotation doesn't matter
```

**Tip:** For circles, rotation has no visual effect.

---

## Complete Example

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
    distance = (dr*dr + dc*dc) ** 0.5
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

![Complete Radial Example](./_images/04-ellipses/08_complete_radial_example.svg)

---

## Tips and Best Practices

### Use fit_to_cell() for Rotated Ellipses

It handles the rotated bounding box automatically:

```python
ellipse = cell.add_ellipse(rx=20, ry=10, rotation=45)
ellipse.fit_to_cell(0.85)  # Perfect fit despite rotation
```

### Brightness for Dynamic Rotation

```python
rotation = cell.brightness * 360  # 0° to 360°
ellipse = cell.add_ellipse(rx=15, ry=8, rotation=rotation)
```

### Invisible Paths

Use ellipses as paths without drawing them:

```python
path = cell.add_ellipse(
    rx=12,
    ry=12,
    fill=None,
    stroke=None
)
cell.add_dot(along=path, t=0.25)  # Path guides position
```

### Combine with Image Data

Let brightness drive position:

```python
ellipse = cell.add_ellipse(rx=15, ry=10)
cell.add_dot(along=ellipse, t=cell.brightness)  # Smooth distribution
```

---

## Next Steps

- **Explore polygons**: [Polygons](05-polygons.md)
- **Learn more math**: [Ellipse Mathematics](../parametric-art/04-ellipse-mathematics.md)
- **See examples**: [Ellipses Example](../examples/advanced/ellipses.md)
- **Pathable protocol**: [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)

---

## See Also

- 📖 [Curves](03-curves.md) - Bézier curves
- 📖 [Polygons](05-polygons.md) - Geometric shapes
- 🎨 [Ellipse Mathematics](../parametric-art/04-ellipse-mathematics.md)
- 🎨 [Parametric Art](../parametric-art/01-what-is-parametric.md)
- 🎯 [Ellipses Example](../examples/advanced/ellipses.md)
- 🎯 [Parametric Paths Example](../examples/advanced/parametric-paths.md)
- 🔍 [Ellipse API Reference](../api-reference/entities.md#ellipse)

