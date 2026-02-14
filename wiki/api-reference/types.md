# Types & Utilities

Core types used throughout PyFreeform, plus utility functions for common operations.

---

::: pyfreeform.Coord
    options:
      heading_level: 2
      members:
        - x
        - y
        - distance_to
        - midpoint
        - lerp
        - normalized
        - dot
        - rotated
        - clamped
        - rounded
        - as_tuple
        - coerce

Supports arithmetic — addition, subtraction, scalar multiply/divide, negation:

```python
a = Coord(100, 200)
b = Coord(50, 50)

a + b       # Coord(150, 250)
a - b       # Coord(50, 150)
a * 2       # Coord(200, 400)
a / 2       # Coord(50.0, 100.0)
-a          # Coord(-100, -200)
a[0], a[1]  # 100, 200 (subscript access)
```

---

::: pyfreeform.RelCoord
    options:
      heading_level: 2
      members:
        - rx
        - ry
        - lerp
        - clamped
        - as_tuple
        - coerce

Fields are `rx`, `ry` (not `x`, `y`) to distinguish from pixel `Coord`. Supports the same arithmetic as `Coord`:

```python
a = RelCoord(0.2, 0.3)
b = RelCoord(0.1, 0.1)

a + b   # RelCoord(0.3, 0.4)
a - b   # RelCoord(0.1, 0.2)
a * 2   # RelCoord(0.4, 0.6)
rx, ry = a  # destructuring works
```

### Where RelCoord Appears

| API | Usage |
|---|---|
| `entity.at` | Returns `RelCoord` (or `None` if in absolute mode) |
| `add_*(..., at=)` | Accepts `RelCoord`, plain tuple, or named position string |
| `cell.normalized_position` | Returns `RelCoord` (cell position within grid, 0.0–1.0) |
| `surface.absolute_to_relative(point)` | Returns `RelCoord` |

!!! tip "Plain tuples work too"
    All APIs that accept `RelCoord` also accept plain `(rx, ry)` tuples. Returned values are `RelCoord` instances with named fields and helper methods.

---

## AnchorSpec {: #the-anchorspec-type }

`AnchorSpec` is the type accepted by `entity.anchor()`, `surface.anchor()`, and the `start_anchor`/`end_anchor` parameters of `connect()`. It unifies three forms:

| Form | Example | Description |
|---|---|---|
| `str` | `"center"`, `"top_right"`, `"v0"` | Named anchor (entity-specific) |
| `tuple[float, float]` | `(0.7, 0.3)` | Relative coordinate within bounding box |
| `RelCoord` | `RelCoord(0.7, 0.3)` | Same as tuple, with named fields |

For **entities**, tuples/RelCoords resolve against the axis-aligned bounding box. `Rect` overrides this to use local coordinate space (rotation-aware). For **surfaces**, they resolve against the surface's rectangular region.

```python
rect.anchor("top_right")           # Named anchor
rect.anchor((0.7, 0.3))            # 70% across, 30% down
dot.connect(rect, end_anchor="left") # In connections
```

---

::: pyfreeform.Image
    options:
      heading_level: 2
      members:
        - load
        - from_pil
        - width
        - height
        - has_alpha
        - rgb_at
        - hex_at
        - rgba_at
        - alpha_at
        - size
        - resize
        - fit
        - quantize
        - downscale

!!! info "See also"
    For image-to-art workflows, see [Image to Art](../recipes/01-image-to-art.md).

---

::: pyfreeform.Layer
    options:
      heading_level: 2
      members:
        - width
        - height

A single-channel grayscale array. Access values with `layer[x, y]` (returns 0–255).

---

## Utility Functions

::: pyfreeform.map_range

```python
radius = map_range(cell.brightness, 0, 1, 2, 10)
# brightness 0.0 → radius 2, brightness 1.0 → radius 10

# Swap output range to reverse direction
radius = map_range(cell.brightness, 0, 1, 10, 2)  # dark = big, bright = small
```

::: pyfreeform.get_angle_at

::: pyfreeform.display
