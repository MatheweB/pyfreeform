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

!!! warning "Type checking for `RelCoordLike`"
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

Returns `None` if the entity was created with pixel coordinates (via `place()` or direct constructor). See [RelCoord](types.md#pyfreeform.RelCoord) for details.

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
| `surface.connect(other, ..., start_anchor, end_anchor)` | Create a connection. Anchors accept AnchorSpec. |
| `surface.connections` | Set of connections where this surface is an endpoint |
| `surface.data` | Custom data dictionary |
| `surface.contains(point)` | Whether a `Coord` is within the surface bounds |
| `surface.relative_to_absolute(pos)` | Convert relative position (named string, tuple, or `RelCoord`) to pixel `Coord` |

---

::: pyfreeform.Surface
    options:
      heading_level: 2
      members:
        - add_dot
        - add_line
        - add_diagonal
        - add_curve
        - add_path
        - add_ellipse
        - add_polygon
        - add_rect
        - add_text
        - add_fill
        - add_border
        - add_point
        - add
        - place
        - remove
        - clear

!!! note
    Most of the time you want `add()`. Use `place()` only when you've already positioned an entity at exact pixel coordinates and want to register it with a surface without moving it.
