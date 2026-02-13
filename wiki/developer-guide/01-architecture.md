# Architecture Overview

This page covers the internal structure of PyFreeform -- how modules are organized, how entities relate to surfaces, and how SVG rendering works end to end.

## Module Structure

```
pyfreeform/
  core/           # Foundational abstractions
    entity.py       # Entity ABC -- base for all drawable objects
    surface.py      # Surface base class -- Cell, Scene, CellGroup
    binding.py      # Binding dataclass -- immutable positioning config
    pathable.py     # Pathable protocol -- point_at(t) interface
    connection.py   # Connection -- reactive link between entities
    coord.py        # Coord (x, y) NamedTuple
    relcoord.py     # RelCoord (rx, ry) NamedTuple
    tangent.py      # Tangent angle utilities for pathables
    stroked_path_mixin.py  # Shared cap/marker logic

  entities/       # Concrete entity implementations
    dot.py          # Dot (circle)
    line.py         # Line (segment between two points)
    curve.py        # Curve (quadratic Bezier)
    ellipse.py      # Ellipse (with parametric support)
    rect.py         # Rect (rectangle with rotation)
    polygon.py      # Polygon (arbitrary vertices, entity-reference vertices)
    text.py         # Text (with textPath support)
    path.py         # Path (renders any Pathable as smooth SVG)
    point.py        # Point (invisible positional anchor)
    entity_group.py # EntityGroup (composite entity)

  scene/          # Top-level container
    scene.py        # Scene -- owns grids, entities, rendering

  grid/           # Spatial organization
    grid.py         # Grid -- rows x cols of cells
    cell.py         # Cell -- extends Surface, has image data
    cell_group.py   # CellGroup -- multi-cell region

  paths/          # Built-in path shapes (Pathable implementations)
    base.py         # PathShape base class (shared arc_length, to_svg_path_d)
    wave.py         # Wave (sinusoidal wave between two points)
    spiral.py       # Spiral (Archimedean spiral)
    lissajous.py    # Lissajous (parametric Lissajous curve)
    zigzag.py       # Zigzag (triangle wave between two points)

  config/         # Configuration and extensibility
    styles.py       # Style dataclasses (DotStyle, LineStyle, etc.)
    caps.py         # Cap registry (arrow markers, custom caps)
    palette.py      # Color palette utilities

  image/          # Image loading and processing
    image.py        # Image loader
    layer.py        # Layer abstraction (color, brightness, alpha)
    resize.py       # Image resizing utilities

  color.py        # Color parsing and conversion
  display.py      # Jupyter/notebook display helpers
```

## The Surface Protocol

`Surface` is the base class that provides entity management and builder methods. Three classes extend it:

```
Surface (base)
  |-- Scene       # Top-level SVG document, owns grids and connections
  |-- Cell        # Single grid cell, has image data (color, brightness)
  |-- CellGroup   # Rectangular selection of cells
```

### What Surface provides

Every Surface has a rectangular region (`_x`, `_y`, `_width`, `_height`) and a list of entities (`_entities`). It provides:

| Capability | Methods |
|---|---|
| **Position resolution** | `relative_to_absolute()`, `absolute_to_relative()`, named positions ("center", "top_left", etc.) |
| **Builder methods** | `add_dot()`, `add_line()`, `add_curve()`, `add_ellipse()`, `add_polygon()`, `add_rect()`, `add_text()`, `add_path()`, `add_fill()`, `add_border()` |
| **Entity management** | `add()`, `place()`, `remove()`, `clear()` |
| **Parametric positioning** | `_resolve_along()` -- resolves `along`/`t`/`align` params for any builder |

### Subclass responsibilities

Subclasses must initialize these attributes in `__init__`:

```python
class Cell(Surface):
    def __init__(self, ...):
        self._x = ...       # top-left X
        self._y = ...       # top-left Y
        self._width = ...   # width in pixels
        self._height = ...  # height in pixels
        self._entities = [] # entity storage
```

!!! note "Surface vs Entity"
    `Surface` and `Entity` are independent hierarchies. A Surface **contains** entities (composition). An Entity **references** its containing surface via `entity.cell`. The `EntityGroup` is the one entity that also contains other entities, but it does so through SVG `<g>` transforms, not through the Surface protocol.

## Entity Class Hierarchy

`Entity` is the abstract base for everything that can be drawn:

```
Entity (ABC)
  |-- Dot              # Simple circle
  |-- Line             # Segment, has StrokedPathMixin
  |-- Curve            # Quadratic Bezier, has StrokedPathMixin
  |-- Ellipse          # Oval with parametric support
  |-- Rect             # Rectangle with rotation
  |-- Polygon          # Arbitrary vertices (static or entity-reference)
  |-- Text             # Text with optional textPath
  |-- Path             # Renders any Pathable, has StrokedPathMixin
  |-- Point            # Invisible positional anchor
  |-- EntityGroup      # Composite entity (children in <g>)
```

### What Entity provides

Every entity has:

- **Position** (`_position: Coord`) -- the entity's reference point
- **Z-index** (`_z_index: int`) -- layer ordering for rendering
- **Cell reference** (`_cell: Surface | None`) -- back-reference to container
- **Connections** (`_connections: WeakSet`) -- tracked via weak references
- **Movement** -- private `_move_to()` / `_move_by()` for pixel movement; public API is `.position`, `.at`, and `move_to_cell()`
- **Binding** -- `.binding` property accepts a `Binding` dataclass (from `core/binding.py`) for relative positioning configuration
- **Resolved state** -- `.is_resolved` is `True` after a transform with `origin` converts relative properties to absolute values. This is a one-way door — builder methods check it to avoid overwriting concrete values.
- **Transforms** -- `rotate(angle, origin)` and `scale(factor, origin)` are **non-destructive**: they accumulate `_rotation` and `_scale_factor` without modifying geometry. With `origin`, `_resolve_to_absolute()` converts relative properties first, then orbits/scales the position around the origin. SVG rendering applies transforms via `_build_svg_transform()`.
- **Transform properties** -- `.rotation` (degrees), `.scale_factor` (multiplier), `.rotation_center` (pivot point — default: position; overridden per entity type)
- **World-space helpers** -- `_to_world_space(point)` applies scale then rotation around `rotation_center`. Used by `anchor()` and `bounds()`.
- **Fitting** -- `fit_within()` scales to fit a target; `fit_to_cell()` delegates to `fit_within()` using the containing cell's bounds
- **Connectivity** -- `connect()`, `place_beside()`

### Abstract methods every entity must implement

```python
@property
@abstractmethod
def anchor_names(self) -> list[str]:
    """List available anchor names."""

@abstractmethod
def anchor(self, name: str) -> Coord:
    """Return anchor point by name."""

@abstractmethod
def to_svg(self) -> str:
    """Render to SVG element string."""

@abstractmethod
def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y). visual=True includes stroke width."""
```

### The StrokedPathMixin

Entities with stroked paths (Line, Curve, Path, Connection) share cap/marker logic through `StrokedPathMixin`:

```python
class Line(StrokedPathMixin, Entity):
    ...
```

The mixin provides:

- `effective_start_cap` / `effective_end_cap` -- resolves per-end overrides
- `get_required_markers()` -- returns SVG `<marker>` definitions needed for caps
- `_svg_cap_and_marker_attrs()` -- computes `stroke-linecap` and `marker-start`/`marker-end` attributes

## SVG Rendering Pipeline

When you call `scene.to_svg()` or `scene.save("art.svg")`, this pipeline executes:

```
scene.to_svg()
    |
    |-- 1. Write SVG header (<svg xmlns=... width=... height=...>)
    |
    |-- 2. Collect definitions (<defs>)
    |   |-- _collect_markers()    # Arrow caps, custom marker caps
    |   |-- _collect_path_defs()  # <path> elements for textPath
    |
    |-- 3. Render background (<rect width="100%" ...>)
    |
    |-- 4. Collect all renderables
    |   |-- Connections  -> (z_index, svg_string)
    |   |-- Entities     -> (z_index, svg_string)
    |   |   |-- scene._entities (direct entities)
    |   |   |-- grid.all_entities() for each grid
    |   |       |-- cell._entities for each cell
    |
    |-- 5. Sort by z_index (stable sort)
    |
    |-- 6. Render in sorted order
    |
    |-- 7. Close </svg>
```

### Step-by-step detail

**Step 2 -- Collecting definitions.** The scene walks every entity and connection looking for marker-based caps (like `"arrow"`) and textPath path definitions. This is how entities can inject shared SVG `<defs>` without duplication:

```python
def _collect_markers(self) -> dict[str, str]:
    markers: dict[str, str] = {}
    for entity in self.entities:
        if hasattr(entity, "get_required_markers"):
            for mid, svg in entity.get_required_markers():
                markers[mid] = svg  # dict deduplicates by ID
    # ... also checks connections
    return markers
```

**Step 4 -- Collecting entities.** The `scene.entities` property aggregates entities from all sources:

```python
@property
def entities(self) -> list[Entity]:
    result = list(self._entities)        # Direct scene entities
    for grid in self._grids:
        result.extend(grid.all_entities())  # All cell entities
    return result
```

**Step 5 -- Z-index sorting.** Python's `sort()` is stable, so entities with the same `z_index` preserve their insertion order:

```python
renderables.sort(key=lambda x: x[0])  # Sort by z_index
```

**Step 6 -- Rendering.** Each entity's `to_svg()` is called exactly once. The returned string is indented and appended to the output:

```python
for _, svg in renderables:
    lines.append(f"  {svg}")
```

### Marker deduplication

The cap system uses deterministic marker IDs based on cap name, color, and size. Two arrows with the same color and width share a single `<marker>` definition:

```python
# From config/caps.py
def make_marker_id(cap_name, color, size, *, for_start=False):
    clean = color.lstrip("#").lower()
    size_str = f"{size:.1f}".replace(".", "_")
    suffix = "-start" if for_start else ""
    return f"cap-{cap_name}-{clean}-{size_str}{suffix}"
```

!!! tip "Extending the pipeline"
    To add a new entity type that needs shared SVG definitions, implement `get_required_markers()` and/or `get_required_paths()` on your entity. The scene's rendering pipeline will automatically discover and deduplicate them.

## Key Design Decisions

### Composition over inheritance

Surfaces contain entities; entities reference their surface. There is no deep inheritance tree. The `StrokedPathMixin` adds cap behavior via mixin rather than a deeper class hierarchy.

### Weak references for connections

Entity connections use `WeakSet` so that deleting a connection does not require explicit cleanup on both entities:

```python
self._connections: WeakSet[Connection] = WeakSet()
```

### Connection geometry

Connections support three geometry modes controlled by constructor arguments:

- **Line** (default): No pre-computation. Rendered as a direct `<line>` between the live anchor positions.
- **`curvature=`**: A normalized bezier arc is built from shared utilities in `core/bezier.py` (`curvature_control_point` + `quadratic_to_cubic`). The same degree-elevation math is shared with the `Curve` entity — no duplication.
- **`path=`**: The pathable is sampled and fitted into smooth cubic segments via `fit_cubic_beziers()` in `core/bezier.py` (Hermite interpolation).

At render time, curve and path geometries are automatically stretched and rotated (affine transform) to connect the actual anchor endpoints. Pass `visible=False` to create an invisible connection — `to_svg()` returns an empty string but `point_at(t)` still works.

### Entity-reference vertices

Polygon vertices can be static `Coord` values or live entity references (`Entity` or `(Entity, "anchor_name")`). Internally, the Polygon stores a `_vertex_specs` list and resolves references at render time via `_resolve_vertex()`. This gives polygons reactive behavior — when a referenced entity moves, the polygon deforms automatically. The `Point` entity (which renders nothing) exists specifically to serve as an invisible positional anchor for these vertex references.

### Relative coordinate system

Surface builder methods accept named positions (`"center"`, `"top_left"`) or relative tuples `(rx, ry)` where `(0, 0)` is top-left and `(1, 1)` is bottom-right. This keeps cell-level code resolution-independent.

Internally, relative positions are stored as `RelCoord(rx, ry)` — a `NamedTuple` with `rx` and `ry` fields (see `core/relcoord.py`). The `.at` property on every entity returns and accepts `RelCoord` values. The `.binding` property accepts a `Binding` dataclass for full positioning configuration (relative position, path-following, reference entity). Users reposition entities through `.position`, `.at`, or `move_to_cell()` — low-level pixel movement (`_move_to`, `_move_by`) is private.

### Entity.cell back-reference

Every entity knows which surface it lives in via `entity.cell`. This enables `fit_to_cell()` to work without passing the cell explicitly:

```python
dot = cell.add_dot(radius=0.15)
dot.fit_to_cell(0.85)  # Knows its cell, scales to fit
```
