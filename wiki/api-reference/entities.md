# Entities

All entities inherit from `Entity` and share common capabilities. Each entity type adds its own geometry, anchors, and behavior.

!!! info "See also"
    For creative examples of each entity type, see [Drawing with Entities](../guide/03-drawing-with-entities.md).

---

::: pyfreeform.Entity
    options:
      heading_level: 2
      members:
        - position
        - x
        - y
        - at
        - binding
        - rotation
        - scale_factor
        - rotation_center
        - z_index
        - cell
        - connections
        - data
        - bounds
        - offset_from
        - move_to_cell
        - rotate
        - scale
        - fit_to_cell
        - fit_within
        - connect
        - anchor
        - anchor_names
        - place_beside

---

::: pyfreeform.Dot
    options:
      heading_level: 2
      members:
        - __init__
        - radius
        - color
        - relative_radius
        - anchor_names
        - bounds

!!! warning "Uses `color=`, not `fill=`"

=== "Builder Method (relative)"

    ```python
    dot = cell.add_dot(at="center", radius=0.1, color="coral")  # 10% of cell
    ```

=== "Constructor (pixels)"

    ```python
    dot = Dot(100, 200, radius=10, color="coral")
    scene.place(dot)
    ```

---

::: pyfreeform.Line
    options:
      heading_level: 2
      members:
        - __init__
        - from_points
        - start
        - end
        - width
        - color
        - length
        - set_endpoints
        - arc_length
        - angle_at
        - point_at
        - to_svg_path_d
        - anchor_names

Cap values: `"round"`, `"square"`, `"butt"`, `"arrow"`, `"arrow_in"`

---

::: pyfreeform.Curve
    options:
      heading_level: 2
      members:
        - __init__
        - from_points
        - start
        - end
        - width
        - color
        - curvature
        - control
        - arc_length
        - angle_at
        - point_at
        - to_svg_path_d
        - anchor_names

!!! info "See also"
    See [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md) for Bezier curve techniques.

---

::: pyfreeform.Ellipse
    options:
      heading_level: 2
      members:
        - __init__
        - at_center
        - fill
        - stroke
        - stroke_width
        - rx
        - ry
        - relative_rx
        - relative_ry
        - point_at_angle
        - arc_length
        - angle_at
        - point_at
        - to_svg_path_d
        - anchor_names

!!! warning "Uses `fill=`, not `color=`"
    `fill_opacity` and `stroke_opacity` override `opacity` for independent control.

=== "Builder Method (relative)"

    ```python
    ellipse = cell.add_ellipse(rx=0.3, ry=0.2, fill="steelblue")  # 30%/20% of cell
    ```

=== "Constructor (pixels)"

    ```python
    ellipse = Ellipse(200, 150, rx=60, ry=40, fill="steelblue")
    scene.place(ellipse)
    ```

---

::: pyfreeform.Polygon
    options:
      heading_level: 2
      members:
        - __init__
        - fill
        - stroke
        - stroke_width
        - vertices
        - relative_vertices
        - triangle
        - square
        - diamond
        - hexagon
        - star
        - regular_polygon
        - squircle
        - rounded_rect
        - anchor_names

!!! warning "Uses `fill=`, not `color=`"

### Entity-Reference Vertices

Vertices can be static coordinates **or** entity references:

| Vertex type | Example | Behavior |
|---|---|---|
| `(x, y)` tuple or `Coord` | `(50, 100)` | Static — moves with polygon transforms |
| `Entity` | `Point(50, 100)` | Reactive — tracks entity's `.position` |
| `(Entity, "anchor")` | `(rect, "top_right")` | Reactive — tracks entity's named anchor |

Entity-reference vertices are resolved at render time. When the referenced entity moves, the polygon deforms automatically.

!!! warning "Transforms and entity vertices"
    `polygon.rotate()` and `polygon.scale()` only affect static (Coord) vertices. Entity-reference vertices follow their entity, not polygon transforms.

!!! info "See also"
    For all shape classmethods and polygon techniques, see [Shapes and Polygons](../guide/06-shapes-and-polygons.md).

---

::: pyfreeform.Rect
    options:
      heading_level: 2
      members:
        - __init__
        - at_center
        - fill
        - stroke
        - stroke_width
        - width
        - height
        - rotation
        - relative_width
        - relative_height
        - anchor_names

!!! warning "Uses `fill=`, not `color=`"
    `x, y` is the top-left corner. Use `Rect.at_center()` to position by center. Anchors are rotation-aware.

=== "Builder Method (relative)"

    ```python
    rect = cell.add_rect(width=0.8, height=0.4, fill="navy")  # 80%/40% of cell
    ```

=== "Constructor (pixels)"

    ```python
    rect = Rect(50, 50, width=160, height=80, fill="navy")
    scene.place(rect)
    ```

---

::: pyfreeform.Text
    options:
      heading_level: 2
      members:
        - __init__
        - content
        - font_size
        - color
        - bold
        - italic
        - font_family
        - relative_font_size
        - has_textpath
        - set_textpath
        - fit_to_cell
        - anchor_names

!!! warning "font_size: pixels in constructor, fraction in builder"
    `Text(x, y, content, font_size=16)` uses **pixels**. `cell.add_text(content, font_size=0.25)` uses **fraction of surface height** (0.25 = 25%).

!!! info "See also"
    See [Text and Typography](../guide/07-text-and-typography.md) for text layout and textpath examples.

---

::: pyfreeform.Path
    options:
      heading_level: 2
      members:
        - __init__
        - fill
        - closed
        - color
        - arc_length
        - angle_at
        - point_at
        - to_svg_path_d
        - anchor_names

Uses Hermite-to-cubic-Bezier fitting with C1 continuity — no sharp corners between segments. Use `start_t`/`end_t` to render a portion of any path.

!!! info "See also"
    See [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md) for path rendering techniques.

---

::: pyfreeform.EntityGroup
    options:
      heading_level: 2
      members:
        - __init__
        - add
        - children
        - rotate
        - scale
        - rotation
        - scale_factor
        - opacity
        - fit_to_cell
        - bounds

SVG output: `<g transform="translate(x,y) rotate(r) scale(s)" opacity="o">` — children are never mutated.

!!! tip "EntityGroup vs CellGroup"
    `EntityGroup` inherits `Entity` — reusable composite shapes. `CellGroup` inherits `Surface` — merged multi-cell regions. Different purposes.

!!! info "See also"
    See [Transforms and Layout](../guide/08-transforms-and-layout.md) for EntityGroup composition patterns.

---

::: pyfreeform.Point
    options:
      heading_level: 2
      members:
        - __init__
        - anchor_names

Renders no SVG — used as a movable anchor for reactive polygon vertices or connection endpoints.

```python
# Reactive polygon with add_point
a = cell.add_point(at=(0.5, 0.1))
b = cell.add_point(at=(0.9, 0.9))
c = cell.add_point(at=(0.1, 0.9))
tri = Polygon([a, b, c], fill="coral")
b.at = (0.8, 0.3)  # triangle vertex moves with it
```

!!! info "See also"
    See [Reactive Polygons](../guide/06-shapes-and-polygons.md#reactive-polygons) for shared vertices and anchor tracking examples.
