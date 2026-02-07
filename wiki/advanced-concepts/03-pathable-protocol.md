
# Pathable Protocol

The Pathable protocol provides a unified interface for positioning elements along any path.

## What is Pathable?

Any object with a `point_at(t)` method is **Pathable**:

```python
from typing import Protocol
from pyfreeform.core.point import Point

class Pathable(Protocol):
    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0.0 to 1.0) along path."""
        ...
```

![Pathable protocol concept showing points along a path at different t values](./_images/03-pathable-protocol/01-what-is-pathable-concept.svg)

## Built-In Pathables

- **Line** - Linear interpolation

![Line pathable with point_at markers along its length](./_images/03-pathable-protocol/03-builtin-line.svg)

- **Curve** - Bézier parametric position

![Curve pathable with point_at markers along the Bézier path](./_images/03-pathable-protocol/04-builtin-curve.svg)

- **Ellipse** - Position around perimeter

![Ellipse pathable with point_at markers around the perimeter](./_images/03-pathable-protocol/05-builtin-ellipse.svg)

![Built-in pathables: Line, Curve, and Ellipse with point_at markers](./_images/03-pathable-protocol/02-what-is-pathable-interface.svg)

## Using Pathables

```python
# Works with any pathable!
line = cell.add_line(start="left", end="right")
curve = cell.add_curve(curvature=0.5)
ellipse = cell.add_ellipse(rx=15, ry=10)

# Unified interface
cell.add_dot(along=line, t=0.5)
cell.add_dot(along=curve, t=0.5)
cell.add_dot(along=ellipse, t=0.5)
```

![Unified interface placing dots along line, curve, and ellipse at t=0.5](./_images/03-pathable-protocol/06-using-pathables-unified.svg)

![Distributing multiple elements along a pathable](./_images/03-pathable-protocol/07-using-pathables-distribution.svg)

## Creating Custom Paths

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
        angle = t * self.turns * 2 * math.pi
        radius = self.start_r + (self.end_r - self.start_r) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Point(x, y)

# Use it!
spiral = Spiral(cell.center, 0, 15, 3)
cell.add_dot(along=spiral, t=0.5)
```

![Custom spiral path created with the Pathable protocol](./_images/03-pathable-protocol/08-custom-spiral.svg)

![Custom wave path](./_images/03-pathable-protocol/09-custom-wave.svg)

![Custom heart path](./_images/03-pathable-protocol/10-custom-heart.svg)

![Custom Lissajous path](./_images/03-pathable-protocol/11-custom-lissajous.svg)

![Comparison of custom paths: Spiral, Wave, Heart, and Lissajous](./_images/03-pathable-protocol/12-custom-paths-comparison.svg)

## Practical Example

![Practical example of distributing entities along custom paths](./_images/03-pathable-protocol/13-practical-example-distribution.svg)

## Tangent Angles

Every built-in Pathable has an `angle_at(t)` method returning the tangent angle in degrees:

```python
line = Line(0, 0, 100, 0)
line.angle_at(0.5)    # 0.0 (pointing right)

curve = Curve(0, 100, 100, 0, curvature=0.5)
curve.angle_at(0.0)   # Angle at start
curve.angle_at(1.0)   # Angle at end
```

For custom Pathables without `angle_at()`, use `get_angle_at()` which falls back to numeric differentiation:

```python
from pyfreeform import get_angle_at

angle = get_angle_at(my_custom_path, t=0.5)
```

This powers the `align=True` feature in `add_dot`, `add_rect`, `add_text`, etc.

## SVG Path Data

Pathables with `to_svg_path_d()` can be used for text warping via SVG `<textPath>`:

```python
curve = cell.add_curve(curvature=0.5)
curve.to_svg_path_d()  # "M 0 100 Q 50 0 100 100"

# Text warps along the curve
cell.add_text("Hello!", along=curve)  # No t= → textPath mode
```

Built-in paths (Line, Curve, Ellipse, Connection) all implement `to_svg_path_d()`.

## See Also
- [Custom Paths](../parametric-art/05-custom-paths.md) - Examples
- [Curves](../entities/03-curves.md) - Bezier math
- [Ellipses](../entities/04-ellipses.md) - Parametric ellipses
- [Positioning Along Paths](../parametric-art/02-positioning-along-paths.md) - along= for all entities
