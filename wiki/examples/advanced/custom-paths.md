
# Example: Custom Paths

**Difficulty**: 🚀 Advanced

Create custom parametric paths by implementing the Pathable protocol: spirals, waves, and Lissajous curves.

---

## What You'll Learn

- Implementing the Pathable protocol
- Archimedean spiral mathematics (`r(θ) = a + bθ`)
- Sinusoidal wave equations
- Lissajous curve parametric equations
- Polar to Cartesian coordinate conversion

---

## Final Result

![All Custom Paths](../_images/custom-paths/04_all_paths.svg)

### More Examples

| Spirals | Waves | Lissajous | All Paths |
|---------|-------|-----------|-----------|
| ![Example 1](../_images/custom-paths/01_spirals.svg) | ![Example 2](../_images/custom-paths/02_waves.svg) | ![Example 3](../_images/custom-paths/03_lissajous.svg) | ![Example 4](../_images/custom-paths/04_all_paths.svg) |

---

## Implementing Custom Paths

### The Pathable Protocol

Any class can become a path by implementing `point_at(t)`:

```python
from pyfreeform.core.pathable import Pathable
from pyfreeform.core.point import Point

class MyPath(Pathable):
    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0 to 1)."""
        # Your mathematics here
        x = calculate_x(t)
        y = calculate_y(t)
        return Point(x, y)
```

---

## Example 1: Archimedean Spiral

### The Mathematics

```
Polar form:
r(θ) = a + bθ

Where:
  a = starting radius
  b = spacing between turns
  θ = angle (radians)

Parametric form (for t ∈ [0,1]):
θ(t) = t × turns × 2π
r(t) = t × max_radius

Cartesian conversion:
x(t) = cx + r(t)·cos(θ(t))
y(t) = cy + r(t)·sin(θ(t))
```

### Implementation

```python
import math
from pyfreeform.core.pathable import Pathable
from pyfreeform.core.point import Point

class Spiral(Pathable):
    """Archimedean spiral: r(θ) = a + bθ"""

    def __init__(
        self,
        center: Point,
        max_radius: float,
        turns: float = 2
    ):
        self.center = center
        self.max_radius = max_radius
        self.turns = turns

    def point_at(self, t: float) -> Point:
        # t maps to angle from 0 to turns*2π
        angle = t * self.turns * 2 * math.pi

        # Radius grows linearly with t
        radius = t * self.max_radius

        # Convert polar to Cartesian
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)

        return Point(x, y)
```

### Usage

```python
from pyfreeform import Scene, Palette

scene = Scene.with_grid(cols=15, rows=15, cell_size=30)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    # Create spiral path
    spiral = Spiral(
        center=cell.center,
        max_radius=12,
        turns=3
    )

    # Render as a smooth SVG curve
    cell.add_path(spiral, color=colors.primary, width=1.5)
```

**Visual Result:**
```
t=0.0  → radius=0,   angle=0°     → center
t=0.25 → radius=3,   angle=180°   → 1/4 turn out
t=0.5  → radius=6,   angle=360°   → 1/2 turn out
t=0.75 → radius=9,   angle=540°   → 3/4 turn out
t=1.0  → radius=12,  angle=720°   → full spiral
```

---

## Example 2: Sinusoidal Wave

### The Mathematics

```
Wave equation:
y = A·sin(ωx + φ)

Where:
  A = amplitude (wave height)
  ω = angular frequency (cycles per unit)
  φ = phase shift

Parametric form (for t ∈ [0,1]):
x(t) = x₀ + t·(x₁ - x₀)
y(t) = y_baseline + A·sin(t·frequency·2π)

Where:
  (x₀, y₀) = start point
  (x₁, y₁) = end point
  y_baseline = linear interpolation from y₀ to y₁
```

### Implementation

```python
class Wave(Pathable):
    """Sinusoidal wave: y = A·sin(ωx + φ)"""

    def __init__(
        self,
        start: Point,
        end: Point,
        amplitude: float,
        frequency: float = 2
    ):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t: float) -> Point:
        # Linear x progression
        x = self.start.x + t * (self.end.x - self.start.x)

        # Baseline y (linear interpolation)
        baseline_y = self.start.y + t * (self.end.y - self.start.y)

        # Add sine wave oscillation
        wave_offset = self.amplitude * math.sin(
            t * self.frequency * 2 * math.pi
        )

        y = baseline_y + wave_offset

        return Point(x, y)
```

### Usage

```python
for cell in scene.grid:
    wave = Wave(
        start=cell.top_left,
        end=cell.top_right,
        amplitude=8,
        frequency=3  # 3 complete waves
    )

    # Render as a smooth SVG curve
    cell.add_path(wave, color=colors.accent, width=1)
```

---

## Example 3: Lissajous Curves

### The Mathematics

```
Lissajous equations:
x(t) = A·sin(at + δ)
y(t) = B·sin(bt)

Where:
  A, B = amplitudes
  a, b = frequency ratios (integers create closed curves)
  δ = phase shift
  t ∈ [0, 2π]

Common patterns:
a=1, b=2, δ=0     : Figure-8
a=3, b=2, δ=π/2   : Trefoil knot
a=5, b=4, δ=π/4   : Complex star
```

### Implementation

```python
class Lissajous(Pathable):
    """Lissajous curve: x = A·sin(at + δ), y = B·sin(bt)"""

    def __init__(
        self,
        center: Point,
        size: float,
        a: float = 3,
        b: float = 2,
        delta: float = 0
    ):
        self.center = center
        self.size = size
        self.a = a  # Frequency ratio x
        self.b = b  # Frequency ratio y
        self.delta = delta  # Phase shift

    def point_at(self, t: float) -> Point:
        # t maps to angle [0, 2π]
        angle = t * 2 * math.pi

        # Lissajous equations
        x = self.center.x + self.size * math.sin(
            self.a * angle + self.delta
        )
        y = self.center.y + self.size * math.sin(
            self.b * angle
        )

        return Point(x, y)
```

### Usage

```python
for cell in scene.grid:
    # Different patterns based on position
    a = 3
    b = 2
    delta = (cell.col / scene.grid.cols) * math.pi

    lissajous = Lissajous(
        center=cell.center,
        size=12,
        a=a,
        b=b,
        delta=delta
    )

    # Render as a smooth closed SVG curve
    cell.add_path(lissajous, closed=True, color=colors.primary, width=0.8)
```

**Pattern Examples:**
```
a=1, b=1, δ=0     : Circle
a=1, b=2, δ=0     : Figure-8 (vertical)
a=2, b=1, δ=0     : Figure-8 (horizontal)
a=3, b=2, δ=π/2   : Trefoil knot
a=5, b=4, δ=0     : Five-petal flower
```

---

## Complete Example

```python
from pyfreeform import Scene, Palette
from pyfreeform.core.point import Point
import math

# [Include Spiral, Wave, and Lissajous class definitions above]

scene = Scene.with_grid(cols=15, rows=15, cell_size=30)
colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Choose path based on column
    third = scene.grid.cols // 3

    if cell.col < third:
        # Spiral pattern
        path = Spiral(
            center=cell.center,
            max_radius=12,
            turns=2 + cell.brightness
        )
        cell.add_path(path, color=colors.primary, width=1)

    elif cell.col < third * 2:
        # Wave pattern
        freq = 2 + cell.row % 3
        path = Wave(
            start=cell.top_left,
            end=cell.bottom_left,
            amplitude=6,
            frequency=freq
        )
        cell.add_path(path, color=colors.accent, width=1)

    else:
        # Lissajous pattern (closed)
        path = Lissajous(
            center=cell.center,
            size=10,
            a=3,
            b=2,
            delta=cell.brightness * math.pi
        )
        cell.add_path(path, closed=True, color=colors.primary, width=0.8)

scene.save("custom_paths.svg")
```

---

## Try It Yourself

### Experiment 1: Logarithmic Spiral

```python
class LogSpiral(Pathable):
    """Logarithmic spiral: r = a·e^(bθ)"""

    def __init__(self, center: Point, a: float, b: float, turns: float = 2):
        self.center = center
        self.a = a
        self.b = b
        self.turns = turns

    def point_at(self, t: float) -> Point:
        angle = t * self.turns * 2 * math.pi
        radius = self.a * math.exp(self.b * angle)

        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)

        return Point(x, y)
```

### Experiment 2: Rose Curve

```python
class Rose(Pathable):
    """Rose curve: r = a·sin(k·θ)"""

    def __init__(self, center: Point, radius: float, k: int = 5):
        self.center = center
        self.radius = radius
        self.k = k  # Number of petals (if odd) or 2k (if even)

    def point_at(self, t: float) -> Point:
        angle = t * 2 * math.pi
        r = self.radius * abs(math.sin(self.k * angle))

        x = self.center.x + r * math.cos(angle)
        y = self.center.y + r * math.sin(angle)

        return Point(x, y)
```

### Challenge: Hypotrochoid

Implement a hypotrochoid (spirograph pattern):

```python
class Hypotrochoid(Pathable):
    """Hypotrochoid: spirograph pattern"""

    def __init__(self, center: Point, R: float, r: float, d: float):
        self.center = center
        self.R = R  # Radius of fixed circle
        self.r = r  # Radius of rolling circle
        self.d = d  # Distance of pen from rolling circle center

    def point_at(self, t: float) -> Point:
        theta = t * 2 * math.pi

        x = self.center.x + (self.R - self.r) * math.cos(theta) + \
            self.d * math.cos((self.R - self.r) / self.r * theta)

        y = self.center.y + (self.R - self.r) * math.sin(theta) - \
            self.d * math.sin((self.R - self.r) / self.r * theta)

        return Point(x, y)
```

---

## Related

- 📖 [Pathable Protocol Guide](../../advanced-concepts/03-pathable-protocol.md) - Protocol details
- 📖 [Pathable API](../../api-reference/pathable.md) - API reference
- 📖 [Custom Paths Guide](../../parametric-art/05-custom-paths.md) - More examples
- 📖 [Mathematical Reference](../../parametric-art/06-mathematical-reference.md) - All equations

