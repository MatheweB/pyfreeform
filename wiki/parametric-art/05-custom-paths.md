
# Custom Paths

Create your own parametric paths by implementing `point_at(t)`.

## The Pathable Protocol

```python
from pyfreeform.core.point import Point

class MyPath:
    def point_at(self, t: float) -> Point:
        """Return point at parameter t (0 to 1)."""
        # Your math here
        return Point(x, y)
```

That's it! Render it as a smooth SVG curve with `Path`, or position entities along it with `along=`:

```python
path = MyPath()
cell.add_path(path, color="blue", width=2)          # Smooth SVG curve
cell.add_path(path, closed=True, fill="lightblue")   # Closed + filled
cell.add_dot(along=path, t=0.5)                      # Position dot at midpoint
```

![The Pathable protocol concept showing any class with point_at can be rendered with Path()](./_images/05-custom-paths/01-pathable-concept.svg)

## Example 1: Archimedean Spiral

```python
import math
from pyfreeform.core.point import Point

class Spiral:
    def __init__(self, center, start_r, end_r, turns):
        self.center = center
        self.start_r = start_r
        self.end_r = end_r
        self.turns = turns
    
    def point_at(self, t: float) -> Point:
        # Angle increases with t
        angle = t * self.turns * 2 * math.pi
        
        # Radius grows linearly
        radius = self.start_r + (self.end_r - self.start_r) * t
        
        # Polar to Cartesian
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        
        return Point(x, y)
```

**Math:**
```
r(θ) = a + bθ

Where:
  θ = t × turns × 2π
  r = start_r + (end_r - start_r) × t
```

![Archimedean spiral with labeled start and end points](./_images/05-custom-paths/02-spiral-basic.svg)

![Spiral variations with different turn counts and radii](./_images/05-custom-paths/03-spiral-variations.svg)

![Spiral path with dots positioned along it](./_images/05-custom-paths/04-spiral-with-dots.svg)

## Example 2: Sinusoidal Wave

```python
class Wave:
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency
    
    def point_at(self, t: float) -> Point:
        # Base line
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        
        # Wave oscillation
        wave = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        y = base_y + wave
        
        return Point(x, y)
```

**Math:**
```
x(t) = x₀ + (x₁ - x₀) × t
y(t) = y₀ + (y₁ - y₀) × t + A·sin(ω·t)

Where:
  A : Amplitude
  ω : Angular frequency (2π × frequency)
```

![Sinusoidal wave path with labeled amplitude](./_images/05-custom-paths/05-wave-basic.svg)

![Wave variations with different amplitudes and frequencies](./_images/05-custom-paths/06-wave-variations.svg)

## Example 3: Lissajous Curve

```python
class Lissajous:
    def __init__(self, center, a, b, delta, size):
        self.center = center
        self.a = a  # X frequency
        self.b = b  # Y frequency
        self.delta = delta  # Phase difference
        self.size = size
    
    def point_at(self, t: float) -> Point:
        angle = t * 2 * math.pi
        
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        
        return Point(x, y)
```

**Math:**
```
x(t) = A·sin(a·t + δ)
y(t) = B·sin(b·t)

Where:
  a, b : Frequency ratios
  δ    : Phase difference
  
Famous ratios:
  a:b = 1:1 (δ=0)  → Circle
  a:b = 1:2 (δ=0)  → Figure-8
  a:b = 3:2 (δ=π/2)→ Three-leaf clover
```

![Lissajous curve with 3:2 frequency ratio](./_images/05-custom-paths/07-lissajous-basic.svg)

![Lissajous variations with different frequency ratios and phase offsets](./_images/05-custom-paths/08-lissajous-variations.svg)

## Usage

```python
# Create paths and render as smooth SVG curves
spiral = Spiral(cell.center, 0, 15, 3)
cell.add_path(spiral, color="navy", width=1.5)

lissajous = Lissajous(cell.center, 3, 2, math.pi/2, 10)
cell.add_path(lissajous, closed=True, color="navy", fill="lightblue")

# You can also position dots along them
for i in range(15):
    t = i / 14
    cell.add_dot(along=lissajous, t=t, radius=2)
```

![A smooth Lissajous curve rendered with Path and dots positioned along it](./_images/05-custom-paths/13-usage-example.svg)

## More Ideas

**Superellipse:**
```python
def point_at(self, t):
    angle = t * 2 * math.pi
    x = self.size * self.sgn_pow(math.cos(angle), 2/self.n)
    y = self.size * self.sgn_pow(math.sin(angle), 2/self.n)
    return Point(self.center.x + x, self.center.y + y)
```

**Epitrochoid:**
```python
def point_at(self, t):
    angle = t * self.full_rotations * 2 * math.pi
    x = (R+r)*math.cos(angle) - d*math.cos((R+r)/r * angle)
    y = (R+r)*math.sin(angle) - d*math.sin((R+r)/r * angle)
```

![Epitrochoid curve showing spirograph-like pattern](./_images/05-custom-paths/10-epitrochoid.svg)

**Hypotrochoid:**
```python
def point_at(self, t):
    angle = t * self.full_rotations * 2 * math.pi
    x = (R-r)*math.cos(angle) + d*math.cos((R-r)/r * angle)
    y = (R-r)*math.sin(angle) - d*math.sin((R-r)/r * angle)
```

![Hypotrochoid curve showing inner spirograph pattern](./_images/05-custom-paths/11-hypotrochoid.svg)

**Butterfly Curve:**
```python
def point_at(self, t):
    angle = t * 12 * math.pi
    r = math.exp(math.sin(angle)) - 2*math.cos(4*angle) + math.sin(angle/12)**5
    x = r * math.cos(angle)
    y = r * math.sin(angle)
```

![Butterfly curve showing the complex organic shape](./_images/05-custom-paths/12-butterfly-curve.svg)

![Superellipse variations with different n values from diamond to rounded square](./_images/05-custom-paths/09-superellipse.svg)

## See Also
- [Custom Paths Example](../examples/advanced/custom-paths.md)
- [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
