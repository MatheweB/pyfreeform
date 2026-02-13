# Types & Utilities

Core types used throughout PyFreeform, plus utility functions for common operations.

---

## The Coord Type

```python
from pyfreeform import Coord
```

`Coord` is a `NamedTuple` with `x` and `y` fields. Subscriptable: `point[0]`, `point[1]`.

| Method | Description |
|---|---|
| `Coord(x, y)` | Create a point |
| `point.x`, `point.y` | Access coordinates |
| `point[0]`, `point[1]` | Subscript access |
| `point.distance_to(other)` | Euclidean distance |
| `point.midpoint(other)` | Midpoint between two points |
| `point.lerp(other, t)` | Linear interpolation |
| `point.normalized()` | Unit vector in same direction (zero vector if length is 0) |
| `point.dot(other)` | Dot product with another coord (as 2D vectors) |
| `point.rotated(angle, origin=None)` | Rotate around origin. `angle` is in **radians**. Default origin: `(0, 0)` |
| `point.clamped(min_x, min_y, max_x, max_y)` | Return coord clamped to bounds |
| `point.rounded(decimals=0)` | Round coordinates to N decimal places |
| `point.as_tuple()` | Return as plain `(float, float)` |
| `Coord.coerce(value)` | Convert `(x, y)` tuple or Coord-like to `Coord` |
| `point + Coord(dx, dy)` | Addition |
| `point - Coord(dx, dy)` | Subtraction |

---

## The RelCoord Type

```python
from pyfreeform import RelCoord
```

`RelCoord` is a `NamedTuple` with `rx` and `ry` fields representing **relative fractions** (0.0--1.0) within a surface. It is the type returned by `.at` and used throughout the relative-positioning system.

Like `Coord`, it is subscriptable (`rc[0]`, `rc[1]`) and destructurable:

```python
rc = RelCoord(0.25, 0.75)
rx, ry = rc          # destructure
print(rc.rx, rc.ry)  # named access
print(rc[0], rc[1])  # index access
```

### Arithmetic

`RelCoord` supports the same arithmetic operators as `Coord`:

```python
a = RelCoord(0.2, 0.3)
b = RelCoord(0.1, 0.1)

a + b   # RelCoord(0.3, 0.4)
a - b   # RelCoord(0.1, 0.2)
a * 2   # RelCoord(0.4, 0.6)
a / 2   # RelCoord(0.1, 0.15)
-a      # RelCoord(-0.2, -0.3)
```

### Methods

| Method | Description |
|---|---|
| `RelCoord(rx, ry)` | Create a relative coordinate |
| `rc.rx`, `rc.ry` | Access fractions |
| `rc[0]`, `rc[1]` | Subscript access |
| `rc.lerp(other, t)` | Linear interpolation |
| `rc.clamped(min_rx=0, min_ry=0, max_rx=1, max_ry=1)` | Clamp to valid range (default 0.0--1.0) |
| `rc.as_tuple()` | Return as plain `(float, float)` |
| `RelCoord.coerce(value)` | Convert `(rx, ry)` tuple or RelCoord-like to `RelCoord` |

### Where RelCoord Appears

| API | Usage |
|---|---|
| `entity.at` | Returns `RelCoord` (or `None` if in absolute mode) |
| `add_*(..., at=)` | Accepts `RelCoord`, plain tuple, or named position string |
| `cell.normalized_position` | Returns `RelCoord` (cell position within grid, 0.0--1.0) |
| `surface.absolute_to_relative(point)` | Returns `RelCoord` |

!!! tip "Plain tuples work too"
    All APIs that accept `RelCoord` also accept plain `(rx, ry)` tuples. The difference is that returned values are `RelCoord` instances with named fields and helper methods.

---

## The AnchorSpec Type {: #the-anchorspec-type }

```python
from pyfreeform import AnchorSpec  # str | RelCoord | tuple[float, float]
```

`AnchorSpec` is the type accepted by `entity.anchor()`, `surface.anchor()`, and the `start_anchor`/`end_anchor` parameters of `connect()` and `Connection`. It unifies three forms:

| Form | Example | Description |
|---|---|---|
| `str` | `"center"`, `"top_right"`, `"v0"` | Named anchor (entity-specific) |
| `tuple[float, float]` | `(0.7, 0.3)` | Relative coordinate within bounding box |
| `RelCoord` | `RelCoord(0.7, 0.3)` | Same as tuple, with named fields |

For **entities**, tuples/RelCoords resolve against the entity's axis-aligned bounding box by default. `Rect` overrides this to use local coordinate space (rotation-aware). For **surfaces** (Cell, Scene, CellGroup), they resolve against the surface's rectangular region.

```python
# Named anchor
rect.anchor("top_right")

# Arbitrary position -- 70% across, 30% down
rect.anchor((0.7, 0.3))

# In connections
dot.connect(rect, end_anchor=(0.0, 0.5))
cell_a.connect(cell_b, start_anchor=(1.0, 0.5), end_anchor=(0.0, 0.5))
```

---

## Image Processing

### Image Class

```python
from pyfreeform import Image
image = Image.load("photo.jpg")
```

| Method/Property | Description |
|---|---|
| `Image.load(path)` | Load from file |
| `Image.from_pil(pil_image)` | Create from PIL Image |
| `image.width`, `image.height` | Dimensions |
| `image.has_alpha` | Whether image has alpha channel |
| `image["brightness"]` | Get brightness Layer |
| `image["red"]`, `["green"]`, `["blue"]`, `["alpha"]` | Channel layers |
| `image.rgb_at(x, y)` | RGB at pixel position |
| `image.hex_at(x, y)` | Hex color at pixel position |
| `image.rgba_at(x, y)` | RGBA at pixel position as `(r, g, b, a)` tuple |
| `image.alpha_at(x, y)` | Alpha at pixel position as float (0.0--1.0) |
| `image.size` | Image size as `(width, height)` tuple |
| `image.resize(width, height)` | Resize image |
| `image.fit(max_dim)` | Fit within max dimension |
| `image.quantize(levels)` | Reduce to N levels |
| `image.downscale(factor)` | Downscale by factor |

!!! info "See also"
    For image-to-art workflows, see [Image to Art](../recipes/01-image-to-art.md).

### Layer Class

A single-channel grayscale array (used for brightness, individual color channels, etc.):

| Property/Method | Description |
|---|---|
| `layer.width`, `layer.height` | Dimensions |
| `layer[x, y]` | Value at position (0-255) |

---

## Utility Functions

### `map_range(value, in_min=0, in_max=1, out_min=0, out_max=1, clamp=False)`

Convert a value from one range to another -- like converting between units. If brightness goes from 0 to 1 but you want a radius between 2 and 10:

```python
from pyfreeform import map_range

radius = map_range(cell.brightness, 0, 1, 2, 10)
# brightness 0.0 -> radius 2
# brightness 0.5 -> radius 6
# brightness 1.0 -> radius 10

# Swap the output range to reverse the direction
radius = map_range(cell.brightness, 0, 1, 10, 2)   # dark = big, bright = small

# Works with any range -- here, pixel position (0-800) to rotation (0-360)
rotation = map_range(cell.center.x, 0, 800, 0, 360)
```

Set `clamp=True` to keep the result within the output range even if the input is outside its range.

### `get_angle_at(pathable, t)`

Compute the tangent angle at parameter `t` on a Pathable.

```python
from pyfreeform import get_angle_at
angle = get_angle_at(curve, 0.5)  # Angle in degrees at midpoint
```

### `display(scene_or_svg)`

Display an SVG in the current environment (Jupyter notebook, etc.).
