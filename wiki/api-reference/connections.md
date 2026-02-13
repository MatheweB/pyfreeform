# Connections & Paths

Connections link entities and surfaces together. The Pathable protocol lets you position anything along any curve.

!!! info "See also"
    For connection patterns and anchor techniques, see [Connections and Anchors](../guide/09-connections-and-anchors.md). For parametric positioning, see [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md).

---

## Connections

**Links between connectable objects** (entities or surfaces) that auto-update when endpoints move. Connections are **visible by default** as a straight line. Use `curvature=` for arcs, `path=` for custom paths, or `visible=False` for invisible relationships.

`Connectable = Entity | Surface` -- the type alias for anything that can be a connection endpoint.

```python
Connection(start, end, start_anchor="center", end_anchor="center",  # AnchorSpec
           visible=True, curvature=None, path=None, style=None, segments=32)
```

Or via the entity/surface method:
```python
connection = entity1.connect(
    entity2,
    style=ConnectionStyle(...),
    start_anchor="center",
    end_anchor="center",
    curvature=0.3,      # or path=Path(pathable), or visible=False
    segments=32,
)
```

### Geometry Options

| Mode | SVG Output | Notes |
|---|---|---|
| *(default)* | `<line>` element | Straight connection |
| `curvature=0.3` | Single cubic Bezier `<path>` | Arc; curvature controls bow direction and amount |
| `path=Path(pathable)` | Fitted Bezier `<path>` | Any Pathable -- wave, spiral, custom shape |
| `visible=False` | Nothing (`to_svg()` returns `""`) | Pure relationship -- supports `point_at(t)` |

!!! info "Coordinates are auto-mapped"
    For `curvature=`, the arc is built in normalized unit-chord space. For `path=`, the path geometry is pre-computed. Both are automatically stretched and rotated (affine transform) to connect the actual anchor positions at render time.

### Connection Details

- **`start_anchor`** and **`end_anchor`** accept `AnchorSpec`: string names (`"center"`, `"top_left"`), `RelCoord`, or `(rx, ry)` tuples
- **`style`** accepts `ConnectionStyle` or `dict` with `width`, `color`, `z_index`, `cap` keys
- **`start`** and **`end`** accept any `Connectable` (Entity or Surface)
- **`data`**: `dict[str, Any]` -- custom data dictionary for storing metadata on the connection
- **`visible=False`** = invisible -- `point_at(t)` still works (linear interpolation between anchors)
- **`curvature`** and **`path`** are mutually exclusive -- passing both raises `ValueError`
- **`segments`** controls Bezier fitting resolution for `path=` (default 32; ignored for line/curve)
- Connections auto-collect from their endpoints -- any connection involving an entity or surface in the scene is automatically included at render time
- Supports [cap system](styling.md#cap-system) (arrow, arrow_in, custom) on all visible shapes
- Closed paths (`Path(pathable, closed=True)`) cannot be used as connection paths -- raises `ValueError`

### Connection Properties

| Property/Method | Description |
|---|---|
| `conn.start`, `conn.end` | The connected objects (Entity or Surface) |
| `conn.start_point`, `conn.end_point` | Current pixel positions of anchors (`Coord`). Updates when endpoints move. |
| `conn.visible` | Read/write -- whether the connection renders |
| `conn.color`, `conn.z_index` | Read/write appearance |
| `conn.point_at(t)` | Position along the connection (0.0 = start, 1.0 = end). Works even when `visible=False`. |
| `conn.disconnect()` | Remove from both endpoints and scene |

---

## The Pathable Protocol

The `Pathable` protocol defines a single method:

```python
class Pathable:
    def point_at(self, t: float) -> Coord
```

Where `t` ranges from 0.0 (start) to 1.0 (end). This enables the `along`/`t` parametric positioning system used in all [builder methods](drawing.md#parametric-positioning-along--t--align).

### Built-in Pathables

| Entity | Description |
|---|---|
| `Line` | Linear interpolation from start to end |
| `Curve` | Smooth curve with adjustable bow |
| `Ellipse` | Parametric ellipse (t=0 right, t=0.25 top, t=0.5 left, t=0.75 bottom) |
| `Path` | Evaluates stored cubic Bezier segments |
| `Connection` | Dynamic path between entities |

### Optional Pathable Methods

These methods enable additional features when present:

| Method / Property | Used By | Description |
|---|---|---|
| `arc_length()` | `add_text(along=)` | Total path length for text sizing |
| `angle_at(t)` | `get_angle_at()` | Tangent angle for alignment |
| `to_svg_path_d()` | `add_text(along=)` | SVG path for `<textPath>` warping |
| `is_closed` | `to_svg_path_d()` | Whether start and end coincide (closed loop) |

### Built-in Path Shapes

Ready-to-use pathable classes, accessible as nested classes on `Path`. All four inherit from `PathShape` (`pyfreeform.paths.base`), which provides shared `arc_length()` and `to_svg_path_d()` implementations -- subclasses only need to implement `point_at(t)` and `angle_at(t)`.

| Shape | Description | Closed? | Parameters |
|---|---|---|---|
| `Path.Wave(start, end, amplitude, frequency)` | Sinusoidal wave | No | Defaults to `(0,0)->(1,0)`, `amplitude=0.15`, `frequency=2` |
| `Path.Spiral(center, start_radius, end_radius, turns)` | Archimedean spiral | No | Defaults to center `(0,0)`, `start_radius=0`, `end_radius=50`, `turns=3` |
| `Path.Lissajous(center, a, b, delta, size)` | Lissajous curve | **Yes** | Defaults to center `(0,0)`, `a=3`, `b=2`, `delta=pi/2`, `size=50` |
| `Path.Zigzag(start, end, teeth, amplitude)` | Triangle wave | No | Defaults to `(0,0)->(1,0)`, `teeth=5`, `amplitude=0.12` |

All four implement the full Pathable interface: `point_at(t)`, `angle_at(t)`, `arc_length()`, `to_svg_path_d()`, and the `is_closed` property.

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
