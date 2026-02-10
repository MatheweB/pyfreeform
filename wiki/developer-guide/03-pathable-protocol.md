# The Pathable Protocol

The `Pathable` protocol is the foundation of parametric positioning in PyFreeform. Any object that implements `point_at(t)` can be used with the `along`/`t` system to position entities along arbitrary paths.

This guide covers the protocol, its optional methods, how the rendering pipeline converts pathables to smooth SVG, and a complete walkthrough of building a custom Lissajous curve pathable.

## The Protocol Definition

```python
from typing import Protocol, runtime_checkable
from pyfreeform.core.coord import Coord

@runtime_checkable
class Pathable(Protocol):
    def point_at(self, t: float) -> Coord:
        """Get a point at parameter t (0.0 to 1.0)."""
        ...
```

That is the entire required interface -- a single method. The protocol is `@runtime_checkable`, meaning `isinstance(obj, Pathable)` works at runtime.

### How `t` is interpreted

| `t` value | Meaning |
|---|---|
| `0.0` | Start of the path |
| `0.5` | Midpoint of the path |
| `1.0` | End of the path |

For closed paths (like ellipses), `t=0.0` and `t=1.0` return the same point. For open paths (like lines), they return opposite endpoints.

### Built-in pathable types

These entity types implement `point_at(t)` out of the box:

| Type | Path shape | Closed? |
|---|---|---|
| `Line` | Straight segment | No |
| `Curve` | Quadratic Bezier | No |
| `Ellipse` | Elliptical arc | Yes |
| `Path` | Any Pathable rendered as Bezier | Configurable |
| `Connection` | Straight segment between entities | No |

!!! tip "Point entities as connection endpoints"
    `Point` is an invisible entity with no visual output — ideal as a connection endpoint when you don't want a visible marker. Connections between Points still function as pathables, so you can position other entities along them with `along=conn, t=0.5`.

### Built-in path shapes

Four ready-to-use pathable classes are available as nested classes on `Path`:

| Shape | Description |
|---|---|
| `Path.Wave` | Sinusoidal wave between two points |
| `Path.Spiral` | Archimedean spiral expanding from center |
| `Path.Lissajous` | Parametric Lissajous curve |
| `Path.Zigzag` | Triangle wave between two points |

All four implement `point_at(t)`, `angle_at(t)`, `arc_length()`, and `to_svg_path_d()`. When called with no arguments, they default to normalized coordinate space — ideal for connection shapes.

## Optional Methods

Beyond `point_at(t)`, pathables can implement additional methods that unlock more features:

### `arc_length() -> float`

Returns the approximate total length of the path in pixels. Used by `add_text()` for auto-sizing font in textPath mode.

```python
def arc_length(self) -> float:
    """Approximate total arc length in pixels."""
    total = 0.0
    prev = self.point_at(0.0)
    for i in range(1, 101):
        curr = self.point_at(i / 100)
        total += prev.distance_to(curr)
        prev = curr
    return total
```

### `angle_at(t) -> float`

Returns the tangent angle in degrees at parameter `t`. Used by the `align=True` feature to rotate entities to follow the path direction. If not implemented, the system falls back to numeric differentiation via `tangent.get_angle_at()`.

```python
def angle_at(self, t: float) -> float:
    """Tangent angle in degrees at parameter t."""
    ...
```

!!! note "Numeric fallback"
    When `angle_at()` is not implemented, PyFreeform uses `get_angle_at()` from `core/tangent.py`, which computes the angle via finite differences on `point_at()`. This works well for smooth paths. Only implement `angle_at()` when you have an exact analytical formula or when the numeric fallback is insufficiently accurate.

### `to_svg_path_d() -> str`

Returns the SVG `d` attribute string for the path. Required for textPath warping (text that follows a curve). Without this method, `add_text(along=path)` will raise a `TypeError`.

```python
def to_svg_path_d(self) -> str:
    """SVG path d attribute string."""
    return f"M {self.start.x} {self.start.y} L {self.end.x} {self.end.y}"
```

## How the along/t System Works

When you write `cell.add_dot(along=curve, t=0.5)`, here is what happens internally:

```
cell.add_dot(along=curve, t=0.5)
    |
    |-- Surface._resolve_along(along, t, align=False, user_rotation=0)
    |   |-- position = along.point_at(0.5)     # Get position from pathable
    |   |-- return (position, 0)                # No rotation (align=False)
    |
    |-- Dot(position.x, position.y, ...)        # Create entity at that position
    |-- self._register_entity(dot)              # Register with surface
```

With `align=True`, the rotation step becomes:

```
Surface._resolve_along(along, t=0.5, align=True, user_rotation=0)
    |
    |-- position = along.point_at(0.5)
    |-- tangent_angle = get_angle_at(along, 0.5)  # From tangent.py
    |   |-- If along has angle_at(): use it directly
    |   |-- Otherwise: numeric diff via point_at(0.5 - eps) and point_at(0.5 + eps)
    |-- return (position, tangent_angle + user_rotation)
```

This works identically for `add_line()`, `add_curve()`, `add_ellipse()`, `add_polygon()`, `add_rect()`, and `add_text()` -- every builder method supports `along`/`t`/`align`.

## Walkthrough: Creating a Lissajous Curve Pathable

!!! note "This already exists as a built-in"
    `Path.Lissajous` provides a ready-to-use implementation of this exact curve. This walkthrough recreates it from scratch to teach the Pathable protocol step by step.

A Lissajous curve traces a parametric path defined by:

```
x(t) = A * sin(a*t + delta)
y(t) = B * sin(b*t)
```

where `a` and `b` control frequency, `delta` is the phase shift, and `A`/`B` control amplitude.

### Step 1: Implement point_at(t)

```python
import math
from pyfreeform.core.coord import Coord


class Lissajous:
    """A Lissajous curve pathable."""

    def __init__(
        self,
        center: Coord | tuple[float, float] = (0, 0),
        a: int = 3,
        b: int = 2,
        delta: float = math.pi / 2,
        size: float = 50,
    ) -> None:
        if isinstance(center, tuple):
            center = Coord(*center)
        self.center = center
        self.a = a            # Horizontal frequency
        self.b = b            # Vertical frequency
        self.delta = delta    # Phase shift
        self.size = size      # Amplitude (pixels)

    def point_at(self, t: float) -> Coord:  # (1)!
        """Get point at parameter t (0.0 to 1.0)."""
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Coord(x, y)
```

1. This single method is all that is required. The class now works with `add_dot(along=lissajous, t=0.5)`.

This is already a fully functional pathable. You can use it immediately:

```python
scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
liss = Lissajous(center=scene.grid[10][10].center, a=3, b=2, size=80)

for cell in scene.grid:
    cell.add_dot(along=liss, t=cell.brightness, color="coral", radius=0.15)
```

### Step 2: Add angle_at() for alignment

For entities to rotate and follow the curve direction, implement `angle_at()`:

```python
def angle_at(self, t: float) -> float:
    """Tangent angle in degrees at parameter t."""
    angle = t * 2 * math.pi
    # Derivatives of the parametric equations
    dx = self.size * self.a * math.cos(self.a * angle + self.delta) * 2 * math.pi
    dy = self.size * self.b * math.cos(self.b * angle) * 2 * math.pi
    if dx == 0 and dy == 0:
        return 0.0
    return math.degrees(math.atan2(dy, dx))
```

Now `align=True` uses the exact tangent rather than numeric approximation:

```python
curve_path = cell.add_curve()
# Small rectangles aligned to the Lissajous tangent
cell.add_rect(width=0.15, height=0.05, along=liss, t=0.25, align=True)
```

### Step 3: Add arc_length() for text sizing

```python
def arc_length(self, samples: int = 200) -> float:
    """Approximate arc length via polyline sampling."""
    total = 0.0
    prev = self.point_at(0.0)
    for i in range(1, samples + 1):
        curr = self.point_at(i / samples)
        dx = curr.x - prev.x
        dy = curr.y - prev.y
        total += math.sqrt(dx * dx + dy * dy)
        prev = curr
    return total
```

### Step 4: Add to_svg_path_d() for textPath support

For text to warp along the Lissajous curve, it needs an SVG path definition. The simplest approach is to sample points and emit line segments:

```python
def to_svg_path_d(self, samples: int = 200) -> str:
    """SVG path d attribute as a polyline approximation."""
    p0 = self.point_at(0.0)
    parts = [f"M {p0.x} {p0.y}"]
    for i in range(1, samples + 1):
        p = self.point_at(i / samples)
        parts.append(f" L {p.x} {p.y}")
    return "".join(parts)
```

!!! tip "Polyline vs Bezier"
    A polyline `to_svg_path_d()` works but produces large SVG. For a smoother and smaller result, use `add_path()` instead, which fits cubic Beziers via Hermite interpolation. The `to_svg_path_d()` method is mainly needed for `textPath` support.

## How add_path() Converts Pathables to Smooth SVG

When you call `cell.add_path(lissajous)`, the `Path` entity converts your pathable into smooth cubic Bezier curves. Here is the algorithm:

### Hermite-to-Bezier interpolation

```
For each segment i from 0 to N-1:
    1. Sample the pathable at t_i and t_{i+1}
    2. Compute tangent vectors at both points (via numeric differentiation)
    3. Convert Hermite form to Bezier control points:
       cp1 = p0 + tangent_0 * dt/3
       cp2 = p3 - tangent_1 * dt/3
    4. Clamp control points to prevent blowup (max 75% of chord length)
```

The result is C1-continuous -- tangent directions match at every joint, giving a visually smooth curve with no kinks.

### For closed paths

Closed paths wrap the last segment back to the first point. The tangent computation uses modular arithmetic (`t % 1.0`) so the seam is invisible:

```python
# From path.py
if closed and start_t == 0.0 and end_t == 1.0:
    t_values = [i / n for i in range(n)]  # N points, no duplicate endpoint
    # Last segment: points[N-1] -> points[0], with wrapping tangents
    for i in range(n):
        j = (i + 1) % n  # Wraps back to 0
```

### Sub-paths (arcs)

Use `start_t` and `end_t` to render only a portion of any pathable:

```python
# Render just the first quarter of a Lissajous curve
cell.add_path(liss, start_t=0.0, end_t=0.25, color="red", width=2)

# Render an arc of an ellipse
ellipse = cell.add_ellipse(rx=0.4, ry=0.3)
cell.add_path(ellipse, start_t=0.0, end_t=0.5, color="blue")
```

## Complete Lissajous Pathable

```python
"""Lissajous - A Lissajous curve pathable."""

import math
from pyfreeform.core.coord import Coord


class Lissajous:
    """
    A Lissajous curve: x = A*sin(a*t + delta), y = B*sin(b*t).

    This is a closed curve when a/b is rational. Common ratios:
        a=3, b=2 -> figure-eight variant
        a=1, b=2 -> parabola-like
        a=5, b=4 -> complex knot
    """

    def __init__(
        self,
        center: Coord | tuple[float, float] = (0, 0),
        a: int = 3,
        b: int = 2,
        delta: float = math.pi / 2,
        size: float = 50,
    ) -> None:
        if isinstance(center, tuple):
            center = Coord(*center)
        self.center = center
        self.a = a
        self.b = b
        self.delta = delta
        self.size = size

    def point_at(self, t: float) -> Coord:
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Coord(x, y)

    def angle_at(self, t: float) -> float:
        angle = t * 2 * math.pi
        dx = self.size * self.a * math.cos(self.a * angle + self.delta) * 2 * math.pi
        dy = self.size * self.b * math.cos(self.b * angle) * 2 * math.pi
        if dx == 0 and dy == 0:
            return 0.0
        return math.degrees(math.atan2(dy, dx))

    def arc_length(self, samples: int = 200) -> float:
        total = 0.0
        prev = self.point_at(0.0)
        for i in range(1, samples + 1):
            curr = self.point_at(i / samples)
            dx = curr.x - prev.x
            dy = curr.y - prev.y
            total += math.sqrt(dx * dx + dy * dy)
            prev = curr
        return total

    def to_svg_path_d(self, samples: int = 200) -> str:
        p0 = self.point_at(0.0)
        parts = [f"M {p0.x} {p0.y}"]
        for i in range(1, samples + 1):
            p = self.point_at(i / samples)
            parts.append(f" L {p.x} {p.y}")
        return "".join(parts)
```

## Using It in Practice

### Position dots along a Lissajous curve

```python
from pyfreeform import Scene, Coord

scene = Scene(400, 400, background="#1a1a2e")
liss = Lissajous(center=Coord(200, 200), a=3, b=2, size=150)

# Render the curve itself
scene.add_path(liss, closed=True, color="#334155", width=1)

# Place 50 dots along it
for i in range(50):
    t = i / 50
    scene.add_dot(along=liss, t=t, color="coral", radius=0.01)

scene.save("lissajous.svg")
```

### Render as a filled closed path

```python
scene.add_path(
    liss,
    closed=True,
    color="navy",
    fill="lightblue",
    width=1.5,
    opacity=0.8,
)
```

### Warp text along a Lissajous curve

```python
scene.add_text(
    "Hello Lissajous! ",
    along=liss,
    color="white",
    font_size=0.035,
)
```

## Protocol Summary

| Method | Required? | Enables |
|---|---|---|
| `point_at(t) -> Coord` | **Yes** | `along=`/`t=` positioning for all builder methods |
| `angle_at(t) -> float` | No | Exact tangent for `align=True` (fallback: numeric diff) |
| `arc_length() -> float` | No | Auto font sizing for textPath mode |
| `to_svg_path_d() -> str` | No | textPath warping (`add_text(along=...)` without `t`) |

The minimum viable pathable is a class with a single `point_at(t)` method. Everything else is optional and adds capabilities incrementally.
