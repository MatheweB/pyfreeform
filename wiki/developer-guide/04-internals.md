# Internal API Reference

This page documents PyFreeform's private and internal APIs -- the implementation details that power the public [API Reference](../api-reference/index.md). This is for contributors who need to understand *how* things work under the hood, not for end users.

!!! warning "Stability"
    Internal APIs are not covered by semantic versioning and may change between releases. If you find yourself reaching for something documented here from user code, consider whether the public API already provides what you need.

---

## Resolution Pipeline

Every entity's position is determined by a priority-based resolution system. When you access `entity.x` or `entity.y`, the position is lazily computed:

```
Priority: _along_path > _relative_at > _position (pixel fallback)
```

### `_resolve_position() -> Coord`

Returns the entity's resolved position based on the highest-priority binding:

1. **Path mode** (`_along_path` is set): Calls `along.point_at(t)` to get a position on the path
2. **Relative mode** (`_relative_at` is set): Calls `_resolve_relative(rx, ry)` against the reference frame
3. **Pixel mode** (fallback): Returns the stored `_position` directly

### `_resolve_relative(rx, ry) -> Coord | None`

Converts relative fractions (0.0-1.0) to absolute pixel coordinates using the entity's reference frame:

- If `_reference` is set (from `within=`), uses that entity's or surface's bounds
- Otherwise, uses the containing surface's bounds (`_surface`)
- Returns `None` if no reference frame is available

### `_resolve_to_absolute()`

"Bakes" the entity — converts all relative properties to absolute pixel values and clears the relative state. After baking, the entity no longer reacts to container changes and `entity.is_relative` becomes `False`.

The framework never calls this automatically. It exists as an explicit escape hatch for user code that needs fixed pixel values.

Subclasses override this to bake entity-specific relative properties (e.g., `_relative_vertices` for Polygon, `_relative_end` for Line/Curve).

### `_resolve_size(fraction, dimension) -> float | None`

Converts a relative size fraction to pixels. For example, `_resolve_size(0.05, 100)` returns `5.0`.

---

## Private Movement

### `_move_to(x, y) -> Entity`

Move the entity to absolute pixel coordinates. **Clears relative tracking** — sets `_relative_at = None`, `_along_path = None`. An absolute pixel position cannot be back-computed into a fraction (the reference frame may not exist), so setting one is always a mode switch.

### `_move_by(dx, dy) -> Entity`

Move the entity by a pixel offset. **Preserves what it can express as a delta**:

- **Relative mode**: converts the pixel delta to a fraction adjustment against the reference frame. The entity stays relative.
- **Along-path mode**: resolves the current path position, applies the offset, and exits to pixel mode. A 2D pixel offset cannot be expressed as a 1D path parameter `t`.
- **Pixel mode**: shifts `_position` directly.

Subclasses override `_move_by` to shift their geometry in tandem — Line/Curve shift their end fractions, Polygon shifts all vertex fractions.

### Why these are private

The public API for positioning is:

- `.at = (rx, ry)` for relative positioning
- `.position = Coord(x, y)` for pixel positioning
- `move_to_surface(surface, at=)` for moving between surfaces

`_move_to` and `_move_by` are used internally by transforms (`_orbit_around`, `_scale_around`) and fitting algorithms (`fit_within`). Because `_move_by` preserves relative state, orbiting or fitting an entity does not destroy its container-reactive behavior.

---

## Binding Internals

The `Binding` dataclass (`core/binding.py`) is a frozen, immutable snapshot of an entity's positioning configuration:

```python
@dataclass(frozen=True, slots=True)
class Binding:
    at: RelCoord | None = None
    reference: Surface | Entity | None = None
    along: Pathable | None = None
    t: float = 0.5
```

### How builders create bindings

When a Surface builder method (e.g., `add_dot(at=..., within=..., along=...)`) is called:

1. Builder resolves the `at` parameter to a `RelCoord` (or uses the default)
2. Builder creates the entity with pixel constructor
3. Builder sets `entity.binding = Binding(at=relcoord, reference=within_entity, along=path, t=t)`
4. The `binding` setter unpacks the dataclass into the entity's internal attributes:
   - `_relative_at = binding.at`
   - `_reference = binding.reference`
   - `_along_path = binding.along`
   - `_along_t = binding.t`

### Why Binding is not exported

`Binding` is not in `__init__.py`'s exports because users don't need to construct it. They set positioning through builder method parameters (`at=`, `within=`, `along=`, `t=`). The `.binding` property exists for inspection, not for user construction.

---

## ref_frame() Contract

Both `Entity` and `Surface` implement `ref_frame() -> tuple[float, float, float, float]`, returning `(x, y, width, height)`.

This method exists so the `within=` system can resolve relative coordinates uniformly against either an entity or a surface without `isinstance` checks:

```python
# Inside Surface._get_ref_frame():
if within is not None:
    return within.ref_frame()  # Works for both Entity and Surface
return self.ref_frame()        # Fallback to this surface
```

For entities, `ref_frame()` returns the bounding box. For surfaces, it returns `(x, y, width, height)`.

---

## Registration Lifecycle

### `_register_entity(entity)`

Called by every builder method and by `add()`/`place()`. Performs:

1. Appends entity to `_entities` list
2. Sets `entity.surface = self` (back-reference)

### `add_connection(connection)` / `remove_connection(connection)`

Bookkeeping methods called by `Connection.__init__()` and `Connection.disconnect()`. They add/remove the connection from the surface's `_connections` dict (used as an insertion-ordered set). Users never call these directly -- they use `connect()` to create connections and `disconnect()` to remove them.

---

## Abstract Method Contracts

These methods must be implemented by every Entity subclass. They are listed in the [Architecture Overview](01-architecture.md) but documented in detail here.

### `to_svg() -> str`

Return an SVG element string. Must:

- Use model-space coordinates (not world-space)
- Include `_build_svg_transform()` in the element's `transform` attribute for rotation/scale
- Return an empty string for invisible entities (like Point)

### `bounds(*, visual=False) -> tuple[float, float, float, float]`

Return `(min_x, min_y, max_x, max_y)` in world space (after applying rotation and scale). When `visual=True`, include stroke width in the bounds.

### `_named_anchor(name: str) -> Coord`

Return the anchor point for a given name in world space. Called by the concrete `anchor(spec)` method on the base class. Must handle all names listed in `anchor_names`.

### `inner_bounds() -> tuple[float, float, float, float]`

Return the largest inscribed rectangle as `(min_x, min_y, max_x, max_y)`. Used by `fit_within()` to determine the target region. Default: same as `bounds()`.

### `rotated_bounds(angle, *, visual=False) -> tuple[float, float, float, float]`

Return the tight axis-aligned bounding box of this entity rotated by `angle` degrees around the origin. Used by `EntityGroup.bounds()` to compute tight group bounds from its children.

---

## Entity Internal State

Key internal attributes on every entity:

| Attribute | Type | Description |
|---|---|---|
| `_position` | `Coord` | Absolute pixel position (fallback when no relative binding) |
| `_surface` | `Surface \| None` | Containing surface back-reference |
| `_relative_at` | `RelCoord \| None` | Relative position within reference frame |
| `_reference` | `Surface \| Entity \| None` | Reference frame override (from `within=`) |
| `_along_path` | `Pathable \| None` | Path to follow (from `along=`) |
| `_along_t` | `float` | Parameter on path (0.0-1.0) |
| `_resolving` | `bool` | Guard against circular reference loops |
| `_rotation` | `float` | Accumulated rotation in degrees |
| `_scale_factor` | `float` | Accumulated scale multiplier |
| `_z_index` | `int` | Layer ordering |
| `_connections` | `dict[Connection, None]` | Connections involving this entity (insertion-ordered) |
| `_data` | `dict[str, Any]` | Custom user data |

### Entity-specific relative sizing

| Entity | Attribute | Description |
|---|---|---|
| Dot | `_relative_radius` | Fraction of min(surface width, height) |
| Line, Curve | `_relative_end` | End position as `RelCoord` |
| Rect | `_relative_width`, `_relative_height` | Fractions of surface dimensions |
| Ellipse | `_relative_rx`, `_relative_ry` | Fractions of surface dimensions |
| Text | `_relative_font_size` | Fraction of surface height |
| Polygon | `_relative_vertices` | List of `RelCoord` vertex positions |

### Surface internal state

| Attribute | Type | Description |
|---|---|---|
| `_x`, `_y` | `float` | Top-left corner position |
| `_width`, `_height` | `float` | Dimensions in pixels |
| `_entities` | `list[Entity]` | Contained entities |
| `_connections` | `dict[Connection, None]` | Connections with this surface as endpoint (insertion-ordered) |
| `_data` | `dict[str, Any]` | Custom user data |

---

## SVG Transform Helpers

### `_build_svg_transform() -> str`

Builds the SVG `transform` attribute string from the entity's accumulated rotation and scale:

```
transform="rotate(angle, cx, cy) scale(factor)"
```

Where `(cx, cy)` is the entity's `rotation_center`.

### `_to_world_space(model_point) -> Coord`

Transforms a point from model space to world space by applying scale then rotation around `rotation_center`. Used by `anchor()` and `bounds()` to return world-space coordinates.

### `_orbit_around(angle, origin) -> None`

Rotates the entity's position around an external origin point. Used by `rotate(angle, origin=...)`.

### `_scale_around(factor, origin) -> None`

Scales the entity's distance from an external origin point. Used by `scale(factor, origin=...)`.

