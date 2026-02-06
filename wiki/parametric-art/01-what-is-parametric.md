
# What is Parametric Art?

Parametric art uses mathematical functions to define positions, creating smooth, flowing compositions. Rather than thinking about art as placing elements at fixed coordinates, parametric art describes motion along paths using a single parameter that drives position.

## The Core Insight

Think of parametric positioning like following directions on a journey:

**Cartesian approach:** "Go to the point where x=5 and y=3"
- You jump directly to a fixed coordinate
- Like using GPS coordinates

**Parametric approach:** "Start here, travel 50% of the way along this path"
- You describe movement along a route
- Like following a trail with mile markers

This shift from "where" to "how far along" is the parametric mindset.

!!! tip "The Journey Metaphor"
    Imagine walking along a mountain trail. The Cartesian approach would be: "Stand at latitude 45.123, longitude -122.456." The parametric approach would be: "Walk 2.5 miles from the trailhead." Both get you to the same place, but parametric thinking describes position as progress along a path.

## Parametric vs Cartesian

**Cartesian (y = f(x)):**
```
y = x² + 2x + 1
```
Limited to functions - one y for each x. This means you can't draw circles, loops, or vertical lines naturally.

![Cartesian limitation showing one y value per x](./_images/01-what-is-parametric/01-cartesian-limitation.svg)

The fundamental limitation: for every x value, there can only be one y value. Try to draw a circle with `y = f(x)` and you'll fail - the left and right sides of the circle have the same x but different y values.

**Parametric (x = f(t), y = g(t)):**
```
x(t) = r × cos(t)
y(t) = r × sin(t)
```
Parameter t controls both x and y independently - can create any curve! A circle becomes trivial, and complex paths become as easy as straight lines.

![Parametric circle showing how parametric equations can create curves impossible in Cartesian form](./_images/01-what-is-parametric/02-parametric-circle.svg)

!!! note "Mathematical Freedom"
    With parametric equations, x and y are both functions of an independent parameter t. This means:

    - No vertical line test limitation
    - Can have multiple y values for same x
    - Can have multiple x values for same y
    - Can create closed loops, spirals, and complex curves
    - Can describe position on any curve imaginable

## The t Parameter: The Heart of Parametric Positioning

The parameter `t` is your position along a path. In PyFreeform, `t` is normalized to range from 0 to 1:

- `t=0.0`: Start of path (0% progress)
- `t=0.25`: Quarter way along (25% progress)
- `t=0.5`: Midpoint (50% progress)
- `t=0.75`: Three-quarters along (75% progress)
- `t=1.0`: End of path (100% progress)

This normalization means the same `t` values work for any path type - a line, curve, ellipse, or connection all use the same 0-to-1 scale.

```python
# Position dot at parameter t along a curve
curve = cell.add_curve(curvature=0.5)
cell.add_dot(along=curve, t=0.75, radius=5, color="red")
```

### How t Works on Different Path Types

The beauty of parametric positioning is that `t` has intuitive meaning regardless of path complexity.

**On a straight line:**

![The t parameter on a line showing positions from t=0 to t=1](./_images/01-what-is-parametric/03-t-parameter-line.svg)

Linear interpolation: `t=0.5` is exactly halfway between start and end points.

**On a curved path:**

![The t parameter on a curve showing positions from t=0 to t=1](./_images/01-what-is-parametric/04-t-parameter-curve.svg)

`t=0.5` is the parametric midpoint - not necessarily the geometric midpoint by arc length, but the point where the Bezier parameter equals 0.5.

**On an ellipse:**

![The t parameter on an ellipse showing positions from t=0 to t=1](./_images/01-what-is-parametric/05-t-parameter-ellipse.svg)

`t` maps to angle: `t=0` starts at the rightmost point, `t=0.25` is top, `t=0.5` is left, `t=0.75` is bottom, and `t=1.0` completes the loop back to the start.

!!! info "The Pathable Protocol"
    In PyFreeform, any object that implements the Pathable protocol can be used with `along=`. The protocol requires one method:

    ```python
    def point_at(self, t: float) -> Point:
        """Return the (x, y) position at parameter t."""
    ```

    Built-in Pathable types: `Line`, `Curve`, `Ellipse`, `Connection`

### The `along=` Pattern in PyFreeform

PyFreeform's API uses `along=` to specify parametric positioning:

```python
# Create a path
line = cell.add_line()

# Position elements along the path
cell.add_dot(along=line, t=0.0, radius=5, color="blue")   # Start
cell.add_dot(along=line, t=0.5, radius=5, color="green")  # Middle
cell.add_dot(along=line, t=1.0, radius=5, color="red")    # End
```

This pattern works identically for all path types:

```python
# Same code pattern, different path types
curve = cell.add_curve(curvature=0.8)
cell.add_dot(along=curve, t=0.5, radius=5, color="blue")

ellipse = cell.add_ellipse(at=(50, 50), rx=30, ry=20)
cell.add_dot(along=ellipse, t=0.5, radius=5, color="blue")

connection = Connection(start_cell, end_cell, "right", "left")
cell.add_dot(along=connection, t=0.5, radius=5, color="blue")
```

![Code visualization showing how parametric positioning works in practice](./_images/01-what-is-parametric/06-code-visualization.svg)

!!! tip "Unified Interface"
    The `along=` pattern creates a unified interface for positioning. Once you learn `cell.add_dot(along=path, t=value)`, you can position dots on any curve type without learning different APIs.

## Why Parametric for Generative Art?

Parametric positioning is particularly powerful for generative and data-driven art:

### 1. Smooth Motion and Natural Interpolation

When you animate or transition between states, parametric equations give you smooth, continuous motion:

```python
# Animate a dot sliding along a curve
for t in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    cell.add_dot(along=curve, t=t, radius=3, color="blue")
```

The mathematics handles the interpolation - no need to manually calculate intermediate positions.

### 2. Complex Curves Made Simple

Circles, ellipses, spirals, and Lissajous figures are trivial with parametric equations:

```python
# A circle in parametric form
x(t) = cx + r × cos(2π × t)
y(t) = cy + r × sin(2π × t)

# A Lissajous figure (3:2 frequency ratio)
x(t) = rx × sin(3 × 2π × t)
y(t) = ry × sin(2 × 2π × t)
```

These curves are difficult or impossible in Cartesian form but natural in parametric form.

### 3. Data-Driven Positioning

Here's where parametric positioning becomes powerful for generative art: you can map data to the `t` parameter.

**Example: Brightness-driven positioning**

```python
for cell in grid:
    # Use cell brightness (0.0 to 1.0) as the t parameter
    t = cell.brightness

    # Position a dot along a diagonal based on brightness
    diagonal = cell.add_diagonal(start="bottom-left", end="top-right")
    cell.add_dot(along=diagonal, t=t, radius=8, color="black")
```

Dark cells (brightness near 0.0) position dots at the start of the diagonal.
Bright cells (brightness near 1.0) position dots at the end.
Gray cells position dots proportionally in between.

This creates a smooth visual gradient where the dot's position directly encodes the brightness data.

!!! note "The Brightness → t Pattern"
    The pattern of mapping `cell.brightness` to `t` is fundamental in PyFreeform:

    ```python
    t = cell.brightness  # 0.0 (dark) to 1.0 (bright)
    cell.add_dot(along=path, t=t, ...)
    ```

    This creates a direct visual encoding: data value controls position along path.

**Example: Evenly spaced elements**

```python
# Place 5 dots evenly along a curve
num_dots = 5
for i in range(num_dots):
    t = i / (num_dots - 1)  # 0.0, 0.25, 0.5, 0.75, 1.0
    cell.add_dot(along=curve, t=t, radius=4, color="red")
```

### 4. Unified Interface Across Path Types

The same positioning code works for all path types:

```python
# This function works with ANY Pathable object
def distribute_dots(path, count, color):
    for i in range(count):
        t = i / (count - 1)
        cell.add_dot(along=path, t=t, radius=5, color=color)

# Works identically for all these types
distribute_dots(cell.add_line(), 5, "blue")
distribute_dots(cell.add_curve(curvature=0.8), 5, "blue")
distribute_dots(cell.add_ellipse(at=(50, 50), rx=30, ry=20), 5, "blue")
```

This polymorphism means you can write generic positioning logic that works with any curve.

## Parametric Math in PyFreeform

Every path type in PyFreeform implements parametric equations under the hood. When you call `path.point_at(t)`, the library evaluates these equations:

### Line: Linear Interpolation

**Formula:**
```
P(t) = start + (end - start) × t
```

**Meaning:** Start at the `start` point, then move a fraction `t` of the way toward the `end` point.

- `t=0.0`: P(0) = start + (end - start) × 0 = start
- `t=0.5`: P(0.5) = start + (end - start) × 0.5 = midpoint
- `t=1.0`: P(1) = start + (end - start) × 1 = end

![Line formula visualization showing P(t) = start + (end - start) * t](./_images/01-what-is-parametric/07-line-formula.svg)

### Curve: Quadratic Bézier

**Formula:**
```
B(t) = (1-t)² P₀ + 2(1-t)t P₁ + t² P₂
```

**Meaning:** A weighted blend of three control points (start P₀, control P₁, end P₂) where the weights are polynomial functions of t.

- `t=0.0`: B(0) = 1·P₀ + 0·P₁ + 0·P₂ = P₀ (start point)
- `t=0.5`: B(0.5) = 0.25·P₀ + 0.5·P₁ + 0.25·P₂ (blend of all three)
- `t=1.0`: B(1) = 0·P₀ + 0·P₁ + 1·P₂ = P₂ (end point)

The control point P₁ pulls the curve but isn't on the curve itself.

![Quadratic Bezier curve formula showing B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂](./_images/01-what-is-parametric/08-curve-formula.svg)

!!! info "Bernstein Polynomial Basis"
    The Bézier curve formula uses Bernstein polynomials as basis functions:

    - B₀(t) = (1-t)² - weight for start point
    - B₁(t) = 2(1-t)t - weight for control point
    - B₂(t) = t² - weight for end point

    These always sum to 1, creating a convex combination (weighted average) of control points.

### Ellipse: Trigonometric Parametrization

**Formula:**
```
x(t) = cx + rx × cos(2π × t)
y(t) = cy + ry × sin(2π × t)
```

**Meaning:** Trace around an ellipse centered at (cx, cy) with radii rx and ry as t goes from 0 to 1.

- `t=0.0`: (cx + rx, cy) - rightmost point
- `t=0.25`: (cx, cy + ry) - topmost point
- `t=0.5`: (cx - rx, cy) - leftmost point
- `t=0.75`: (cx, cy - ry) - bottommost point
- `t=1.0`: (cx + rx, cy) - back to start (full loop)

![Ellipse formula visualization showing x(t) = rx*cos(2*pi*t), y(t) = ry*sin(2*pi*t)](./_images/01-what-is-parametric/09-ellipse-formula.svg)

!!! note "Angle vs Parameter"
    The `2π × t` factor converts the 0-to-1 parameter range into 0-to-2π radians (0-to-360 degrees). So `t=0.25` corresponds to 90 degrees, `t=0.5` to 180 degrees, etc.

## Real-World Example: Brightness-Driven Sliding Dots

Let's see how all these concepts combine in a practical example:

```python
from pyfreeform import Scene, Grid

# Create a scene with a 5x5 grid
scene = Scene()
grid = Grid(scene, rows=5, cols=5, cell_size=100)

# Load an image to get brightness values
grid.load_source_image("photo.jpg")

# For each cell, position a dot based on brightness
for cell in grid:
    # Create a diagonal line across the cell
    line = cell.add_line()

    # Map brightness (0.0 to 1.0) to position along line
    t = cell.brightness

    # Dark cells → dot near start (t=0)
    # Bright cells → dot near end (t=1)
    cell.add_dot(along=line, t=t, radius=12, color="red")

scene.save_svg("brightness_sliding_dots.svg")
```

This creates a visual encoding where:
- The darker a region in the source image, the closer the dot is to the start of the diagonal
- The brighter a region, the closer the dot is to the end
- Medium brightness results in dots positioned in the middle

The parametric approach makes this trivial: `t = cell.brightness` directly maps data to position.

## Real-World Example: Evenly Distributed Elements

Parametric positioning makes it easy to distribute elements evenly:

```python
# Create a curved path
curve = cell.add_curve(curvature=0.7)

# Place 8 dots evenly along the curve
num_dots = 8
for i in range(num_dots):
    t = i / (num_dots - 1)  # 0.0, 0.143, 0.286, ..., 1.0
    cell.add_dot(along=curve, t=t, radius=6, color="blue")
```

The same pattern works for any number of elements on any path type - the parametric math handles the spacing automatically.

## From Parametric Positioning to Deeper Math

This introduction covered the what and why of parametric art. The rest of this section dives deeper:

- **Positioning Along Paths** explores advanced techniques for using `t` values
- **Bézier Mathematics** breaks down the cubic Bézier formula and its properties
- **Trigonometric Patterns** shows how to create spirals, roses, and oscillations
- **Algorithmic Composition** demonstrates using parametric math for complex generative systems

The key insight to take forward: parametric art describes position as a function of progress along a path. This single idea - mapping `t` to position - unlocks smooth motion, complex curves, data-driven layouts, and elegant compositional patterns.

## See Also
- [Positioning Along Paths](02-positioning-along-paths.md)
- [Bézier Mathematics](03-bezier-mathematics.md)
