# Drawing

`Surface` is the base class for `Cell`, `Scene`, and `CellGroup`. It provides **12 builder methods** that all work identically across these three surfaces. This is where creativity happens.

!!! info "See also"
    For creative examples of all builder methods, see [Drawing with Entities](../guide/03-drawing-with-entities.md).

---

## Named Positions

All `at` parameters accept named positions or `(rx, ry)` relative coordinates:

| Name | Relative | Description |
|---|---|---|
| `"center"` | `(0.5, 0.5)` | Center of surface |
| `"top_left"` | `(0.0, 0.0)` | Top-left corner |
| `"top_right"` | `(1.0, 0.0)` | Top-right corner |
| `"bottom_left"` | `(0.0, 1.0)` | Bottom-left corner |
| `"bottom_right"` | `(1.0, 1.0)` | Bottom-right corner |
| `"top"` | `(0.5, 0.0)` | Top center |
| `"bottom"` | `(0.5, 1.0)` | Bottom center |
| `"left"` | `(0.0, 0.5)` | Left center |
| `"right"` | `(1.0, 0.5)` | Right center |

??? warning "Type checking for `RelCoordLike`"
    The `RelCoordLike` type accepts:

    * A `Coords` object (e.g., `Coords(x=0.5, y=0.5)`)
    * A tuple `(rx, ry)`
    * **Exactly** one of the strings in `NAMED_POSITIONS` (like `"center"` or `"top_left"`)

    #### Why type checkers may complain

    If you assign a string indirectly, for example via a list or variable:

    ```python
    positions = ["center", "top_left", "bottom_right"]
    for pos in positions:
        scene.add_dot(at=pos)  # ⚠️ Type checker expects explicit strings
    ```

    … the checker cannot verify that `pos` matches a valid named position.

    #### How to fix

    Explicitly validate each value against `NAMED_POSITIONS`:

    ```python
    from pyfreeform.core import NAMED_POSITIONS

    positions = ["center", "top_left", "bottom_right"]
    for pos in positions:
        if pos in NAMED_POSITIONS:
            scene.add_dot(at=pos)  # ✅ safe
    ```

## Parametric Positioning: `along` / `t` / `align`

All builder methods (except `add_fill`, `add_border`) support parametric positioning:

- **`along`**: Any `Pathable` object (Line, Curve, Ellipse, Path, Connection, or custom)
- **`t`**: Parameter 0.0 (start) to 1.0 (end) along the path
- **`align`**: If `True`, rotate the entity to follow the path's tangent direction

!!! tip "Killer feature"
    This is PyFreeform's most powerful concept -- position any element along any path:
    ```python
    line = cell.add_diagonal()
    cell.add_dot(along=line, t=cell.brightness)  # Dot slides along diagonal
    ```
    See [Paths and Parametric Positioning](../guide/05-paths-and-parametric.md) for in-depth examples.

## Entity-Relative Positioning: `within`

All builder methods (except `add_fill`, `add_border`, `add_path`) support `within=`:

```python
rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
dot = cell.add_dot(within=rect, at="center", color="red")
```

When `within=` is set, all relative coordinates (`at`, `start`/`end`, `radius`, `rx`/`ry`, `width`/`height`) are resolved against the referenced entity's bounding box instead of the cell. This is reactive -- if the reference entity moves, dependent entities follow automatically.

## The `.at` Property

Every entity has a read/write `.at` property that returns a `RelCoord`:

```python
dot = cell.add_dot(at=(0.25, 0.75), color="red")
print(dot.at)       # RelCoord(0.25, 0.75)
print(dot.at.rx)    # 0.25
dot.at = (0.5, 0.5) # Reposition to center (plain tuples still accepted)
```

Returns `None` if the entity was created with pixel coordinates (via `place()` or direct constructor). See [RelCoord](types.md#the-relcoord-type) for details.

## Relative Sizing Properties

Builder methods store sizing as **fractions** of the reference frame. These are accessible as read/write properties on each entity:

| Entity | Property | Builder default | Description |
|---|---|---|---|
| Dot | `relative_radius` | `0.05` | Fraction of min(width, height) |
| Line | `relative_start`, `relative_end` | varies | Start/end as `RelCoord` fractions |
| Curve | `relative_start`, `relative_end` | varies | Start/end as `RelCoord` fractions |
| Ellipse | `relative_rx`, `relative_ry` | `0.4` | Fraction of surface width/height |
| Rect | `relative_width`, `relative_height` | `0.6` | Fraction of surface width/height |
| Text | `relative_font_size` | `0.25` | Fraction of surface height |
| Polygon | `relative_vertices` | varies | List of `RelCoord` vertex positions |

These return `None` when the entity is in absolute mode (constructed directly or after a transform resolves them). Setting them switches the entity back to relative mode for that dimension.

!!! note "Sizing vs geometry"
    Relative **sizing** (radius, rx/ry, width/height, font_size) is unaffected by transforms -- rotation doesn't change how big something is relative to its cell. Relative **geometry** (vertices, start/end) encodes positions that transforms convert to absolute values. After a transform resolves an entity, builder methods won't overwrite those concrete values.

## Surface Anchors, Connections, and Data

All surfaces (Cell, Scene, CellGroup) support anchors, connections, and custom data:

| Method/Property | Description |
|---|---|
| `surface.anchor(spec)` | Anchor position by name, `RelCoord`, or `(rx, ry)` tuple. See [AnchorSpec](types.md#the-anchorspec-type). |
| `surface.anchor_names` | List of available anchor names |
| `surface.connect(other, ..., start_anchor, end_anchor)` | Create a connection. Anchors accept `AnchorSpec`. |
| `surface.connections` | Set of connections where this surface is an endpoint |
| `surface.data` | Custom data dictionary |
| `surface.contains(point)` | Whether a `Coord` is within the surface bounds |
| `surface.relative_to_absolute(pos)` | Convert relative position (named string, tuple, or `RelCoord`) to pixel `Coord` |
| `surface.absolute_to_relative(point)` | Convert pixel `Coord` to `RelCoord` (0.0--1.0) |

---

## Builder Reference

### `add_dot`

```python
add_dot(*, at, within, along, t, radius=0.05, color="black", z_index=0, opacity=1.0, style=DotStyle)
```

Creates a filled circle. `radius` is a fraction of the cell's smaller dimension (0.05 = 5%). Default position: center.

### `add_line`

```python
add_line(*, start, end, within, along, t, align, width=1, color="black", z_index=0,
         cap="round", start_cap, end_cap, opacity=1.0, style=LineStyle)
```

Creates a line segment. Default: center to center (zero-length).

### `add_diagonal`

```python
add_diagonal(*, start="bottom_left", end="top_right", within, along, t, align, width=1,
             color="black", z_index=0, cap="round", start_cap, end_cap,
             opacity=1.0, style=LineStyle)
```

Convenience for corner-to-corner lines. Delegates to `add_line()`.

### `add_curve`

```python
add_curve(*, start="bottom_left", end="top_right", curvature=0.5, within, along, t, align,
          width=1, color="black", z_index=0, cap="round", start_cap, end_cap,
          opacity=1.0, style=LineStyle)
```

Creates a smooth curve between two points. `curvature` controls how much it bows: 0 = straight, positive = bows left, negative = bows right (relative to the direction from start to end).

### `add_path`

??? note "Expand full signature"

    ```python
    add_path(pathable, *, segments=64, closed=False, start_t=0.0, end_t=1.0,
             width=1, color="black", fill=None, z_index=0, cap="round",
             start_cap, end_cap, opacity=1.0, fill_opacity, stroke_opacity,
             style=LineStyle)
    ```

Renders any Pathable as a smooth SVG `<path>` using cubic Bezier approximation. Supports arcs via `start_t`/`end_t`, closed paths with fill, and dual opacity.

### `add_ellipse`

??? note "Expand full signature"

    ```python
    add_ellipse(*, at, within, along, t, align, rx, ry, rotation=0, fill="black",
                stroke=None, stroke_width=1, z_index=0, opacity=1.0,
                fill_opacity, stroke_opacity, style=ShapeStyle)
    ```

Creates an ellipse. Default radii: 40% of surface dimensions. The ellipse itself is a Pathable -- you can position other elements along it.

### `add_polygon`

??? note "Expand full signature"

    ```python
    add_polygon(vertices, *, within, along, t, align, fill="black", stroke=None,
                stroke_width=1, z_index=0, opacity=1.0, fill_opacity,
                stroke_opacity, rotation=0, style=ShapeStyle)
    ```

Creates a polygon from relative-coordinate vertices (0-1). Use `Polygon.hexagon()`, `Polygon.star()`, etc. for common shapes. See [Shapes and Polygons](../guide/06-shapes-and-polygons.md) for shape classmethods.

### `add_rect`

??? note "Expand full signature"

    ```python
    add_rect(*, at, within, along, t, align, width, height, rotation=0, fill="black",
             stroke=None, stroke_width=1, opacity=1.0, fill_opacity,
             stroke_opacity, z_index=0, style=ShapeStyle)
    ```

Creates a rectangle. `at` specifies the **center** position. Default size: 60% of surface.

### `add_text`

??? note "Expand full signature"

    ```python
    add_text(content, *, at, within, along, t, align, font_size, color="black",
             font_family="sans-serif", bold=False, italic=False, text_anchor,
             baseline="middle", rotation=0, z_index=0, opacity=1.0,
             fit=False, start_offset=0.0, end_offset=1.0, style=TextStyle)
    ```

Creates text. `font_size` is a fraction of the surface height (0.25 = 25% of cell height). Default: 0.25.

**`fit=True`**: Shrink `font_size` so the rendered text fits within the cell width. Never upsizes -- `font_size` acts as a ceiling. Ignored in path modes (`along=`).

Two modes with `along`:

- **`along` + `t`**: Position text at a point on the path, optionally align to tangent.
- **`along` without `t`**: Warp text along the path using SVG `<textPath>` (auto-sizes font to fill path).

See [Text and Typography](../guide/07-text-and-typography.md) for text layout techniques.

### `add_fill`

```python
add_fill(*, color="black", opacity=1.0, z_index=0, style=FillStyle)
```

Fill the entire surface with a solid color.

### `add_border`

```python
add_border(*, color="#cccccc", width=0.5, z_index=0, opacity=1.0, style=BorderStyle)
```

Add a stroke-only border around the surface.

### `add_point`

```python
add_point(*, at, within, along, t, z_index=0)
```

Creates an invisible positional anchor. Points render nothing -- use them as reactive `Polygon` vertices, connection endpoints, or `within=` reference positions.

---

## Entity Management

### `add`

```python
add(entity, at="center")
```

Add an existing entity to this surface with relative positioning. The entity is moved to the resolved `at` position. Works for any entity type including `EntityGroup`.

### `place` (advanced)

```python
place(entity)
```

Place an entity at its current absolute pixel position. Unlike `add()`, this does **not** reposition the entity -- it is registered exactly where it already is.

!!! note
    Most of the time you want `add()`. Use `place()` only when you've already positioned an entity at exact pixel coordinates and want to register it with a surface without moving it.

### `remove`

```python
remove(entity) -> bool
```

Remove an entity from this surface. Returns `True` if found.

### `clear`

```python
clear()
```

Remove all entities from this surface.
