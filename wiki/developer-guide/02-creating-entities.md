# Creating Custom Entities

This guide walks through creating a custom entity by implementing the `Entity` abstract class. By the end, you will have built a fully functional `CrossHair` entity that integrates with the rendering pipeline, supports transforms, and works with `fit_to_cell()`.

## The Entity Contract

Every entity in PyFreeform extends the `Entity` ABC from `pyfreeform.core.entity`. The base class gives you positioning, movement, connections, and fitting for free. You provide the shape-specific logic.

### Required abstract methods

| Method | Purpose |
|---|---|
| `anchor_names` (property) | Return a `list[str]` of available anchor names |
| `_named_anchor(name)` | Return a `Coord` for the given anchor name |
| `to_svg()` | Return an SVG element string (e.g., `<circle ... />`) |
| `bounds()` | Return `(min_x, min_y, max_x, max_y)` bounding box |

### Optional methods to override

| Method | When to override |
|---|---|
| `inner_bounds()` | Non-rectangular shapes -- return the largest axis-aligned rectangle fully inside the entity. Default: same as `bounds()`. Used by `fit_within()`. |
| `rotated_bounds(angle, *, visual)` | If your entity has a tighter AABB under rotation than the default (which rotates 4 `bounds()` corners). Override with analytical formulas for curves, ellipses, or any entity with known extrema. Used by `EntityGroup.bounds()` for tight composite bounds. |
| `rotation_center` (property) | If the natural rotation/scale pivot isn't `self.position`. Override to return a `Coord` (e.g., Rect returns its center, Polygon returns its centroid). |
| `_move_by(dx, dy)` | If your entity stores absolute coordinates for sub-parts (e.g., Line stores `_end_offset`, Path stores Bezier segments). This is a private method -- users reposition entities via the `.at` property or `move_to_cell()`. |
| `get_required_markers()` | If your entity needs SVG `<marker>` definitions in `<defs>`. Return `list[tuple[str, str]]` of `(marker_id, marker_svg)`. |
| `get_required_paths()` | If your entity needs SVG `<path>` definitions in `<defs>` (used by textPath). Return `list[tuple[str, str]]` of `(path_id, path_svg)`. |

## Walkthrough: Building a CrossHair Entity

A crosshair is two perpendicular lines centered at a point, forming a `+` shape. It has a configurable size, color, and stroke width.

### Step 1: Define the class

```python
"""CrossHair - A crosshair marker entity."""

from __future__ import annotations

import math

from pyfreeform.core.entity import Entity
from pyfreeform.core.coord import Coord
from pyfreeform.color import Color


class CrossHair(Entity):
    """
    A crosshair (+) marker at a specific point.

    Anchors:
        - "center": The center point
        - "top": Top of the vertical arm
        - "bottom": Bottom of the vertical arm
        - "left": Left end of the horizontal arm
        - "right": Right end of the horizontal arm
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        size: float = 10,
        color: str = "black",
        width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
    ) -> None:
        super().__init__(x, y, z_index)  # (1)!
        self.size = float(size)   # Half-length of each arm
        self._color = Color(color)
        self.width = float(width)
        self.opacity = float(opacity)

    @property
    def color(self) -> str:
        return self._color.to_hex()

    @color.setter
    def color(self, value: str) -> None:
        self._color = Color(value)
```

1. Always call `super().__init__(x, y, z_index)`. This sets up `_position`, `_cell`, `_connections`, `_data`, and `_z_index`.

!!! warning "Always call `super().__init__`"
    The base `Entity.__init__` initializes critical internal state: position, cell reference, connections WeakSet, and data dict. Forgetting this call will cause `AttributeError` at runtime.

### Step 2: Implement anchor_names and _named_anchor()

Anchors are named points on your entity that other entities can connect to or reference. The base class provides a concrete `anchor(spec)` method that dispatches string names to your `_named_anchor()` implementation. Anchors must return **world-space** coordinates -- use `self._to_world_space()` to apply the entity's current rotation and scale transforms.

```python
@property
def anchor_names(self) -> list[str]:
    return ["center", "top", "bottom", "left", "right"]

def _named_anchor(self, name: str) -> Coord:
    if name == "center":
        return self._to_world_space(self.position)
    elif name == "top":
        return self._to_world_space(Coord(self.x, self.y - self.size))
    elif name == "bottom":
        return self._to_world_space(Coord(self.x, self.y + self.size))
    elif name == "left":
        return self._to_world_space(Coord(self.x - self.size, self.y))
    elif name == "right":
        return self._to_world_space(Coord(self.x + self.size, self.y))
    raise ValueError(
        f"CrossHair has no anchor '{name}'. "
        f"Available: {self.anchor_names}"
    )
```

!!! note "anchor() vs _named_anchor()"
    External callers always use `entity.anchor(spec)`, which accepts strings, `RelCoord`, and `(rx, ry)` tuples (the `AnchorSpec` type). Your entity only implements `_named_anchor(name)` for string names — the base class handles RelCoord/tuple dispatch via `_anchor_from_relcoord()`, which resolves against the entity's bounding box by default.

!!! tip "Anchor naming conventions"
    - Always include `"center"` -- connections default to it.
    - Use compass-style names for directional anchors: `"top"`, `"bottom"`, `"left"`, `"right"`.
    - For path-like entities, use `"start"`, `"center"`, `"end"`.

### Step 3: Implement bounds()

Return the axis-aligned bounding box as `(min_x, min_y, max_x, max_y)`. This is used by `fit_to_cell()`, `fit_within()`, and `place_beside()`.

The `visual` keyword argument controls whether stroke width is included. When `visual=False` (the default), return pure geometric bounds. When `visual=True`, expand by `stroke_width / 2` so that `fit_to_cell` can account for the visual extent of stroked entities.

Bounds must be in **world space** -- multiply geometry dimensions by `self._scale_factor` to account for accumulated scale transforms:

```python
def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
    s = self._scale_factor
    scaled_size = self.size * s
    min_x = self.x - scaled_size
    min_y = self.y - scaled_size
    max_x = self.x + scaled_size
    max_y = self.y + scaled_size
    if visual:
        half = self.width * s / 2
        min_x -= half
        min_y -= half
        max_x += half
        max_y += half
    return (min_x, min_y, max_x, max_y)
```

For the crosshair, `inner_bounds()` would be very small (just the intersection point), so we leave the default which returns the same as `bounds()`.

!!! tip "Tight rotated bounds via `rotated_bounds()`"
    The default `rotated_bounds(angle)` rotates the four corners of `bounds()` — correct but can overestimate for curved or circular shapes. If your entity has analytical formulas for tighter bounds at arbitrary angles (e.g., Bezier extrema, ellipse extents), override this method. Tight child bounds cascade into tight `EntityGroup.bounds()` automatically.

### Step 4: Implement to_svg()

This is where your entity becomes visible. Return a valid SVG element string.

```python
def to_svg(self) -> str:
    # Horizontal arm (model-space coordinates)
    h = (
        f'<line x1="{self.x - self.size}" y1="{self.y}" '
        f'x2="{self.x + self.size}" y2="{self.y}" '
        f'stroke="{self.color}" stroke-width="{self.width}" '
        f'stroke-linecap="round" />'
    )
    # Vertical arm (model-space coordinates)
    v = (
        f'<line x1="{self.x}" y1="{self.y - self.size}" '
        f'x2="{self.x}" y2="{self.y + self.size}" '
        f'stroke="{self.color}" stroke-width="{self.width}" '
        f'stroke-linecap="round" />'
    )

    # Wrap in a group with transform
    parts = ['<g']
    if self.opacity < 1.0:
        parts.append(f' opacity="{self.opacity}"')
    transform = self._build_svg_transform()  # (1)!
    if transform:
        parts.append(transform)
    parts.append(f'>{h}{v}</g>')
    return ''.join(parts)
```

1. `_build_svg_transform()` returns a `transform="..."` attribute string when rotation or scale are non-identity, or an empty string otherwise.

!!! note "SVG output rules"
    - Return a **single** SVG element. Use `<g>` to group multiple sub-elements.
    - Only emit optional attributes (like `opacity`) when they differ from defaults.
    - Use **model-space** coordinates in SVG (unrotated, unscaled). The `_build_svg_transform()` helper emits the SVG `transform` attribute that applies rotation and scale at render time.
    - The scene indents your output with `f"  {svg}"`, so do not add leading whitespace.

### Step 5: Use the SVG transform in to_svg()

The base class provides **non-destructive transforms** -- `rotate()` and `scale()` accumulate `self._rotation` and `self._scale_factor` without modifying your entity's geometry. The SVG renderer applies these via a `transform` attribute.

**You do NOT need to override `rotate()` or `scale()`** -- the base class handles everything. Just include `_build_svg_transform()` in your `to_svg()` output (shown above in Step 4, full example below).

!!! tip "Non-destructive transform system"
    - `entity.rotate(45)` → stores `_rotation += 45`, no geometry changes
    - `entity.scale(2)` → stores `_scale_factor *= 2`, no geometry changes
    - `entity.rotate(45, origin)` → orbits position around origin + stores rotation
    - `_build_svg_transform()` emits `transform="translate(...) rotate(...) scale(...) translate(...)"` in SVG
    - `_to_world_space(point)` converts model-space points to world-space (for `anchor()` and `bounds()`)
    - `rotation_center` property controls the pivot point (default: `self.position`)

## Complete CrossHair Entity

Here is the full implementation:

```python
"""CrossHair - A crosshair marker entity."""

from __future__ import annotations

from pyfreeform.core.entity import Entity
from pyfreeform.core.coord import Coord
from pyfreeform.color import Color


class CrossHair(Entity):
    """A crosshair (+) marker at a specific point."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        size: float = 10,
        color: str = "black",
        width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
    ) -> None:
        super().__init__(x, y, z_index)
        self.size = float(size)
        self._color = Color(color)
        self.width = float(width)
        self.opacity = float(opacity)

    @property
    def color(self) -> str:
        return self._color.to_hex()

    @color.setter
    def color(self, value: str) -> None:
        self._color = Color(value)

    @property
    def anchor_names(self) -> list[str]:
        return ["center", "top", "bottom", "left", "right"]

    def _named_anchor(self, name: str) -> Coord:
        if name == "center":
            return self._to_world_space(self.position)
        elif name == "top":
            return self._to_world_space(Coord(self.x, self.y - self.size))
        elif name == "bottom":
            return self._to_world_space(Coord(self.x, self.y + self.size))
        elif name == "left":
            return self._to_world_space(Coord(self.x - self.size, self.y))
        elif name == "right":
            return self._to_world_space(Coord(self.x + self.size, self.y))
        raise ValueError(
            f"CrossHair has no anchor '{name}'. "
            f"Available: {self.anchor_names}"
        )

    def bounds(self, *, visual: bool = False) -> tuple[float, float, float, float]:
        s = self._scale_factor
        scaled_size = self.size * s
        min_x = self.x - scaled_size
        min_y = self.y - scaled_size
        max_x = self.x + scaled_size
        max_y = self.y + scaled_size
        if visual:
            half = self.width * s / 2
            min_x -= half
            min_y -= half
            max_x += half
            max_y += half
        return (min_x, min_y, max_x, max_y)

    def to_svg(self) -> str:
        h = (
            f'<line x1="{self.x - self.size}" y1="{self.y}" '
            f'x2="{self.x + self.size}" y2="{self.y}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="round" />'
        )
        v = (
            f'<line x1="{self.x}" y1="{self.y - self.size}" '
            f'x2="{self.x}" y2="{self.y + self.size}" '
            f'stroke="{self.color}" stroke-width="{self.width}" '
            f'stroke-linecap="round" />'
        )
        parts = ['<g']
        if self.opacity < 1.0:
            parts.append(f' opacity="{self.opacity}"')
        transform = self._build_svg_transform()
        if transform:
            parts.append(transform)
        parts.append(f'>{h}{v}</g>')
        return ''.join(parts)

    def __repr__(self) -> str:
        return f"CrossHair({self.x}, {self.y}, size={self.size})"
```

## Using Your Custom Entity

Custom entities work with all placement and fitting APIs:

```python
from pyfreeform import Scene

scene = Scene.with_grid(cols=10, rows=10, cell_size=30)

for cell in scene.grid:
    ch = CrossHair(size=20, color="coral", width=1.5)
    cell.add(ch)                 # Centers in cell
    ch.fit_to_cell(0.8)          # Scales to 80% of cell

scene.save("crosshairs.svg")
```

Connections work too:

```python
ch1 = CrossHair(100, 100, size=15, color="navy")
ch2 = CrossHair(200, 150, size=15, color="navy")
scene.place(ch1, ch2)

# Connect right anchor of ch1 to left anchor of ch2
ch1.connect(ch2, start_anchor="right", end_anchor="left",
            style={"color": "gray", "width": 1})
```

## Adding SVG Definitions

If your entity needs SVG `<marker>` or `<path>` definitions in `<defs>`, implement the optional methods:

```python
def get_required_markers(self) -> list[tuple[str, str]]:
    """Return (marker_id, marker_svg) tuples."""
    marker_id = f"crosshair-dot-{self.color.lstrip('#')}"
    marker_svg = (
        f'<marker id="{marker_id}" viewBox="0 0 4 4" '
        f'refX="2" refY="2" markerWidth="4" markerHeight="4">'
        f'<circle cx="2" cy="2" r="2" fill="{self.color}" />'
        f'</marker>'
    )
    return [(marker_id, marker_svg)]
```

The scene rendering pipeline automatically discovers and deduplicates these definitions.

## Checklist for New Entities

Before considering your entity complete, verify:

- [ ] `super().__init__(x, y, z_index)` is called in `__init__`
- [ ] `anchor_names` includes `"center"`
- [ ] `_named_anchor()` uses `_to_world_space()` and raises `ValueError` for unknown names
- [ ] `bounds()` returns world-space `(min_x, min_y, max_x, max_y)` using `self._scale_factor`
- [ ] `to_svg()` returns a single SVG element (use `<g>` for multiple) with `_build_svg_transform()`
- [ ] `rotation_center` overridden if the natural pivot isn't `self.position`
- [ ] Opacity attributes are only emitted when not equal to 1.0
- [ ] `__repr__` is implemented for debugging
- [ ] Works with `cell.add()` and `fit_to_cell()`

!!! tip "Shape entities with fill/stroke opacity"
    If your entity has both `fill` and `stroke` with independent opacity (like Rect, Ellipse, Polygon), use the shared `shape_opacity_attrs(opacity, fill_opacity, stroke_opacity)` helper from `pyfreeform.core.svg_utils` in your `to_svg()`. It returns the correct `fill-opacity`/`stroke-opacity` SVG attribute string, emitting nothing when opacity is 1.0.

!!! tip "The simplest built-in entity: Point"
    For a minimal real-world example, look at `pyfreeform/entities/point.py`. The `Point` entity renders nothing (`to_svg()` returns `""`) and exists purely as a movable positional anchor. It has a single `"center"` anchor, zero-size bounds, and no internal geometry to scale or rotate. Its primary use is as a reactive vertex for `Polygon` — see [Reactive Polygons](../guide/06-shapes-and-polygons.md#reactive-polygons).

## Creating Custom Path Shapes

If you want to create a new parametric path (like Wave, Spiral, etc.), inherit from `PathShape` in `pyfreeform.paths.base`. You only need to implement `point_at(t)` and `angle_at(t)` — the base class provides `arc_length()` and `to_svg_path_d()` for free:

```python
from pyfreeform.paths.base import PathShape
from pyfreeform.core.coord import Coord, CoordLike

class MyShape(PathShape):
    def __init__(self, center: CoordLike = (0, 0), ...) -> None:
        self.center = Coord.coerce(center)
        ...

    def point_at(self, t: float) -> Coord:
        """Get point at parameter t (0.0 to 1.0)."""
        ...

    def angle_at(self, t: float) -> float:
        """Tangent angle in degrees at parameter t."""
        ...
```

The shape can then be used with `add_path()`, as a connection shape, or with `along=`/`t=` positioning — anywhere a Pathable is accepted.
