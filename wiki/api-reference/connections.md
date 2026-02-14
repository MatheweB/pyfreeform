# Connections & Paths

Connections link entities and surfaces together. The Pathable protocol lets you position anything along any curve.

!!! info "See also"
    For connection patterns and anchor techniques, see [Connections and Anchors](../guide/09-connections-and-anchors.md). For parametric positioning, see [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md).

---

::: pyfreeform.Connection
    options:
      heading_level: 2
      members:
        - __init__
        - start
        - end
        - start_anchor
        - end_anchor
        - start_point
        - end_point
        - data
        - visible
        - color
        - z_index
        - curvature
        - path
        - effective_start_cap
        - effective_end_cap
        - point_at
        - angle_at
        - disconnect

Or via the entity/surface shorthand:

```python
connection = entity1.connect(entity2, style=ConnectionStyle(...), curvature=0.3)
```

### Geometry Options

| Mode | SVG Output | Notes |
|---|---|---|
| *(default)* | `<line>` element | Straight connection |
| `curvature=0.3` | Single cubic Bezier `<path>` | Arc; curvature controls bow direction and amount |
| `path=Path(pathable)` | Fitted Bezier `<path>` | Any Pathable -- wave, spiral, custom shape |
| `visible=False` | Nothing (`to_svg()` returns `""`) | Pure relationship -- `point_at(t)` still works |

!!! info "Coordinates are auto-mapped"
    For `curvature=`, the arc is built in normalized unit-chord space. For `path=`, the path geometry is pre-computed. Both are automatically stretched and rotated (affine transform) to connect the actual anchor positions at render time.

---

## The Pathable Protocol

The `Pathable` protocol defines a single required method:

```python
class Pathable:
    def point_at(self, t: float) -> Coord
```

Where `t` ranges from 0.0 (start) to 1.0 (end). This enables the `along`/`t` parametric positioning system used in all [builder methods](drawing.md#parametric-positioning-along-t-align).

### Built-in Pathables

| Entity | Description |
|---|---|
| `Line` | Linear interpolation from start to end |
| `Curve` | Smooth curve with adjustable bow |
| `Ellipse` | Parametric ellipse (t=0 right, t=0.25 top, t=0.5 left, t=0.75 bottom) |
| `Path` | Evaluates stored cubic Bezier segments |
| `Connection` | Dynamic path between entities |

### Optional Pathable Methods

| Method / Property | Used By | Description |
|---|---|---|
| `arc_length()` | `add_text(along=)` | Total path length for text sizing |
| `angle_at(t)` | `get_angle_at()` | Tangent angle for alignment |
| `to_svg_path_d()` | `add_text(along=)` | SVG path for `<textPath>` warping |
| `is_closed` | `to_svg_path_d()` | Whether start and end coincide (closed loop) |

### Built-in Path Shapes

Ready-to-use pathable classes, accessible as nested classes on `Path`. All implement `point_at(t)`, `angle_at(t)`, `arc_length()`, `to_svg_path_d()`, and the `is_closed` property.

::: pyfreeform.paths.wave.Wave
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.paths.spiral.Spiral
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.paths.lissajous.Lissajous
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.paths.zigzag.Zigzag
    options:
      heading_level: 4
      show_root_full_path: false

```python
# As a standalone path
spiral = Path.Spiral(center=cell.center, end_radius=40, turns=3)
cell.add_path(spiral, width=1.5, color="coral")

# As a connection path (open shapes work directly)
wave = Path.Wave(amplitude=0.15, frequency=3)
conn = dot_a.connect(dot_b, path=Path(wave), style=style)

# Closed shapes need start_t/end_t to create an arc for connections
liss_arc = Path(Path.Lissajous(size=50), start_t=0, end_t=0.5)
conn = dot_a.connect(dot_b, path=liss_arc)
```

### Custom Pathables

Any object with `point_at(t: float) -> Coord` works as a path. See the [Pathable Protocol](../developer-guide/03-pathable-protocol.md) for a full walkthrough of creating custom paths.
