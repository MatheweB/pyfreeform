# Entities

All entities inherit from `Entity` and share common capabilities. Each entity type adds its own geometry, anchors, and behavior.

!!! info "See also"
    For creative examples of each entity type, see [Drawing with Entities](../guide/03-drawing-with-entities.md).

---

## Entity Base Class

Every entity has these shared properties and methods.

### Properties

| Property | Description |
|---|---|
| `entity.position` | Current position (`Coord`) -- computed from relative coords if set |
| `entity.x`, `entity.y` | Position coordinates (lazily resolved) |
| `entity.at` | Read/write relative position as `RelCoord(rx, ry)`, or `None` if in absolute mode |
| `entity.rotation` | Accumulated rotation in degrees (default 0.0). Non-destructive -- stored, not baked. |
| `entity.scale_factor` | Accumulated scale multiplier (default 1.0). Non-destructive -- stored, not baked. |
| `entity.rotation_center` | `Coord` -- the natural pivot for rotation/scale. Default: entity position. Each type overrides with its natural center (Rect center, Polygon centroid, Line/Curve chord midpoint, etc.). |
| `entity.z_index` | Layer ordering (higher = on top) |
| `entity.cell` | Containing Surface (if placed) |
| `entity.connections` | Set of connections involving this entity |
| `entity.data` | Custom data dictionary |
| `entity.bounds(*, visual=False)` | Bounding box: `(min_x, min_y, max_x, max_y)`. Pass `visual=True` to include stroke width. |
| `entity.offset_from(anchor, dx, dy)` | Returns `Coord` at the named anchor position offset by `(dx, dy)` pixels. |

### Movement

| Method | Description |
|---|---|
| `entity.move_to_cell(cell, at="center")` | Move to position within a cell |

### Transforms

| Method | Description |
|---|---|
| `entity.rotate(angle, origin=None)` | Rotate in degrees (counterclockwise) |
| `entity.scale(factor, origin=None)` | Scale (2.0 = double size) |
| `entity.fit_to_cell(...)` | Auto-scale to fit within containing cell. See [Transforms](transforms.md). |
| `entity.fit_within(target, ...)` | Auto-scale to fit within another entity's inner bounds. See [Transforms](transforms.md). |

### Relationships

| Method | Description |
|---|---|
| `entity.connect(other, style, start_anchor, end_anchor)` | Create a Connection. Anchors accept `AnchorSpec` (string, tuple, or `RelCoord`). |
| `entity.anchor(spec)` | Get anchor point by name, `RelCoord`, or `(rx, ry)` tuple. See [AnchorSpec](types.md#the-anchorspec-type). |
| `entity.anchor_names` | List of available anchor names |
| `entity.place_beside(other, side="right", gap=0)` | Position beside another entity using bounding boxes |

---

## Dot

**A filled circle.** The simplest entity.

```python
Dot(x=0, y=0, radius=5, color="black", z_index=0, opacity=1.0)
```

- **Anchors**: `"center"`
- **`color=`** parameter (not `fill=`)
- **Properties**: `radius`, `color` (read/write)

---

## Line

**A line segment between two points.** Implements the Pathable protocol.

```python
Line(x1, y1, x2, y2, width=1, color="black", z_index=0, cap="round",
     start_cap=None, end_cap=None, opacity=1.0)
Line.from_points(start, end, ...)
```

- **Anchors**: `"start"`, `"center"`, `"end"`
- **Pathable**: `line.point_at(t)` returns a point along the line
- **Properties**: `start`, `end`, `width`, `color`, `length` (read/write except `length`)
- **Methods**: `set_endpoints(start, end)`, `arc_length()`, `angle_at(t)`, `to_svg_path_d()`
- Cap values: `"round"`, `"square"`, `"butt"`, `"arrow"`, `"arrow_in"`

---

## Curve

**A smooth curve between two points.** Implements the Pathable protocol.

```python
Curve(x1, y1, x2, y2, curvature=0.5, width=1, color="black", z_index=0,
      cap="round", start_cap=None, end_cap=None, opacity=1.0)
Curve.from_points(start, end, curvature=0.5, ...)
```

- **Anchors**: `"start"`, `"center"`, `"end"`, `"control"`
- **Pathable**: `curve.point_at(t)` returns a point along the Bezier curve
- **Curvature**: 0 = straight, positive = bows left, negative = bows right, typical range -1 to 1
- **Properties**: `start`, `end`, `width`, `color`, `curvature`, `control` (read/write except `control`)
- **Methods**: `arc_length()`, `angle_at(t)`, `to_svg_path_d()`

See [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md) for Bezier curve techniques.

---

## Ellipse

**An ellipse (oval).** Implements the Pathable protocol.

```python
Ellipse(x, y, rx=10, ry=10, rotation=0, fill="black", stroke=None,
        stroke_width=1, z_index=0, opacity=1.0, fill_opacity=None, stroke_opacity=None)
Ellipse.at_center(center, rx, ry, ...)
```

- **Anchors**: `"center"`, `"right"`, `"top"`, `"left"`, `"bottom"`
- **Pathable**: `ellipse.point_at(t)` -- t=0 rightmost, t=0.25 top, t=0.5 left, t=0.75 bottom
- **`fill=`** parameter (not `color=`)
- **Dual opacity**: `fill_opacity` and `stroke_opacity` override `opacity`
- **Properties**: `fill`, `stroke`, `stroke_width`, `rx`, `ry` (read/write)
- **Methods**: `point_at_angle(degrees)`, `arc_length()`, `angle_at(t)`, `to_svg_path_d()`

---

## Polygon

**A closed polygon from vertices.** Includes shape classmethods for common shapes.

```python
Polygon(vertices, fill="black", stroke=None, stroke_width=1, z_index=0,
        opacity=1.0, fill_opacity=None, stroke_opacity=None)
```

- **Anchors**: `"center"` + `"v0"`, `"v1"`, `"v2"`, ...
- **`fill=`** parameter (not `color=`)
- **Dual opacity**: `fill_opacity` and `stroke_opacity`
- **Properties**: `fill`, `stroke`, `stroke_width`, `vertices` (read/write)
- Position is the center of the shape (average of all vertices)

### Entity-Reference Vertices

Vertices can be static coordinates **or** entity references:

| Vertex type | Example | Behavior |
|---|---|---|
| `(x, y)` tuple or `Coord` | `(50, 100)` | Static -- moves with polygon transforms |
| `Entity` | `Point(50, 100)` | Reactive -- tracks entity's `.position` |
| `(Entity, "anchor")` | `(rect, "top_right")` | Reactive -- tracks entity's named anchor |

Entity-reference vertices are resolved at render time. When the referenced entity moves, the polygon deforms automatically.

!!! warning "Transforms and entity vertices"
    `polygon.rotate()` and `polygon.scale()` only affect static (Coord) vertices. Entity-reference vertices follow their entity, not polygon transforms.

!!! info "See also"
    For all shape classmethods and polygon techniques, see [Shapes and Polygons](../guide/06-shapes-and-polygons.md).

### Shape Classmethods

All return `list[tuple[float, float]]` in relative coordinates (0-1), ready for `add_polygon()`:

| Method | Description |
|---|---|
| `Polygon.triangle(size=1.0, center=(0.5, 0.5))` | Equilateral triangle (pointing up) |
| `Polygon.square(size=0.8, center=(0.5, 0.5))` | Axis-aligned square |
| `Polygon.diamond(size=0.8, center=(0.5, 0.5))` | Rotated square (45 degrees) |
| `Polygon.hexagon(size=0.8, center=(0.5, 0.5))` | Regular hexagon |
| `Polygon.star(points=5, size=0.8, inner_ratio=0.4, center=(0.5, 0.5))` | Star with N points |
| `Polygon.regular_polygon(sides, size=0.8, center=(0.5, 0.5))` | Regular N-gon |
| `Polygon.squircle(size=0.8, center=(0.5, 0.5), n=4, points=32)` | Superellipse (n=2 circle, n=4 squircle) |
| `Polygon.rounded_rect(size=0.8, center=(0.5, 0.5), corner_radius=0.2, points_per_corner=8)` | Rectangle with rounded corners |

---

## Rect

**A rectangle with optional rotation.**

```python
Rect(x, y, width, height, fill="black", stroke=None, stroke_width=1,
     rotation=0, z_index=0, opacity=1.0, fill_opacity=None, stroke_opacity=None)
Rect.at_center(center, width, height, rotation=0, ...)
```

- **Anchors**: `"center"`, `"top_left"`, `"top_right"`, `"bottom_left"`, `"bottom_right"`, `"top"`, `"bottom"`, `"left"`, `"right"`
- **`fill=`** parameter (not `color=`)
- **Dual opacity**: `fill_opacity` and `stroke_opacity`
- `x, y` is top-left corner; `Rect.at_center()` positions by center
- Rotation: stored as `rotation` attribute, emits SVG `transform="rotate()"`
- **Properties**: `fill`, `stroke`, `stroke_width`, `width`, `height`, `rotation` (read/write)
- Rotation-aware anchors (anchors account for rotation angle)

---

## Text

**A text label with rich formatting.**

??? note "Expand full constructor"

    ```python
    Text(x=0, y=0, content="", font_size=16, color="black",
         font_family="sans-serif", font_style="normal", font_weight="normal",
         bold=False, italic=False, text_anchor="middle", baseline="middle",
         rotation=0, z_index=0, opacity=1.0)
    ```

- **`font_size`** in the constructor is **pixels** (16 = 16px). In `add_text()`, it's a **fraction** of surface height (0.25 = 25%).
- **Anchors**: `"center"`
- **`color=`** parameter
- **Properties**: `content`, `font_size`, `color`, `bold`, `italic`, `font_family` (read/write)
- **Sugar**: `bold=True` sets `font_weight="bold"`, `italic=True` sets `font_style="italic"`
- **Text alignment**: `text_anchor` = `"start"` / `"middle"` / `"end"`, `baseline` = `"auto"` / `"middle"` / `"hanging"` / etc.
- **Rotation**: `rotation` attribute, SVG `transform="rotate()"`
- **Bounds**: Uses Pillow for accurate font measurement; heuristic fallback
- **`fit_to_cell(fraction)`**: Scales font up or down so text fills the cell at `fraction` (like `EntityGroup.fit_to_cell`)
- **`text.has_textpath`**: Read-only `bool` -- `True` if the text renders along a path (textPath mode)
- **TextPath**: `text.set_textpath(path_id, path_d, start_offset, text_length)` for warping along paths

See [Text and Typography](../guide/07-text-and-typography.md) for text layout and textpath examples.

---

## Path

**Renders any Pathable as a smooth SVG path.** Implements the Pathable protocol itself.

??? note "Expand full constructor"

    ```python
    Path(
        pathable,           # Any object with point_at(t)
        *,
        segments=64,        # Number of cubic Bezier segments
        closed=False,       # Close path smoothly (enables fill)
        start_t=0.0,        # Start parameter (for arcs/sub-paths)
        end_t=1.0,          # End parameter (for arcs/sub-paths)
        width=1,            # Stroke width
        color="black",      # Stroke color
        fill=None,          # Fill color (only if closed)
        z_index=0,
        cap="round",
        start_cap=None,
        end_cap=None,
        opacity=1.0,
        fill_opacity=None,
        stroke_opacity=None,
    )
    ```

- **Anchors**: `"start"`, `"center"`, `"end"`
- **Pathable**: `path.point_at(t)` evaluates the stored Bezier segments
- **Algorithm**: Smooth curve fitting -- no sharp corners between segments (Hermite-to-cubic-Bezier with C1 continuity)
- **Sub-paths**: Use `start_t`/`end_t` to render a portion of any path (e.g., quarter of an ellipse)
- **Properties**: `fill`, `closed` (read/write)
- **Methods**: `arc_length()`, `angle_at(t)`, `to_svg_path_d()`

See [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md) for path rendering techniques.

---

## EntityGroup

**A reusable composite entity.** Children positioned relative to (0,0), rendered as SVG `<g>`.

```python
EntityGroup(x=0, y=0, z_index=0, opacity=1.0)
```

- **`group.add(entity)`**: Add child (positioned relative to local origin)
- **`group.children`**: List of children (copy)
- **`group.rotate(angle, origin=None)`**: Accumulate rotation (degrees). With `origin`, also orbits position.
- **`group.scale(factor, origin=None)`**: Accumulate scale factor.
- **`group.rotation`**: Read/write `float` -- current accumulated rotation angle in degrees.
- **`group.scale_factor`**: Read/write `float` -- current cumulative scale factor.
- **`group.opacity`**: Group-level opacity (applies to entire `<g>` element)
- **Placement**: `cell.add(group)` -- centers in cell
- **Fitting**: `group.fit_to_cell(fraction)` -- auto-scales to fit cell bounds
- **SVG**: `<g transform="translate(x,y) rotate(r) scale(s)" opacity="o">` -- children never mutated
- **Reuse**: Wrap creation in a factory function; each call returns new instance

!!! tip "EntityGroup vs CellGroup"
    `EntityGroup` inherits `Entity` and is used for reusable composite shapes. `CellGroup` inherits `Surface` and represents merged multi-cell regions. They serve different purposes.

See [Transforms and Layout](../guide/08-transforms-and-layout.md) for EntityGroup composition patterns.

---

## Point

**An invisible positional entity.** Renders no SVG -- used as a movable anchor for reactive polygon vertices or connection endpoints.

```python
# Direct constructor (pixel coordinates)
Point(x=0, y=0, z_index=0)

# Builder method (relative coordinates -- preferred)
point = cell.add_point(at=(0.25, 0.75))
```

- **Anchors**: `"center"`
- **SVG output**: None (empty string)
- **Bounds**: Zero-size at position
- **Key use**: Pass to `Polygon()` as a vertex -- the polygon tracks the Point's position at render time

```python
# Reactive polygon with add_point
a = cell.add_point(at=(0.5, 0.1))
b = cell.add_point(at=(0.9, 0.9))
c = cell.add_point(at=(0.1, 0.9))
tri = Polygon([a, b, c], fill="coral")
b.at = (0.8, 0.3)  # triangle vertex moves with it
```

See [Reactive Polygons](../guide/06-shapes-and-polygons.md#reactive-polygons) for shared vertices and anchor tracking examples.
