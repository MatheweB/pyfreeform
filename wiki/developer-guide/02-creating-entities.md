# Creating Custom Entities

This guide walks through creating a custom entity by implementing the `Entity` abstract class. By the end, you will have built a fully functional `CrossHair` entity that integrates with the rendering pipeline, supports transforms, and works with `fit_to_cell()`.

## The Entity Contract

Every entity in PyFreeform extends the `Entity` ABC from `pyfreeform.core.entity`. The base class gives you positioning, movement, connections, and fitting for free. You provide the shape-specific logic.

### Required abstract methods

| Method | Purpose |
|---|---|
| `anchor_names` (property) | Return a `list[str]` of available anchor names |
| `anchor(name)` | Return a `Coord` for the given anchor name |
| `to_svg()` | Return an SVG element string (e.g., `<circle ... />`) |
| `bounds()` | Return `(min_x, min_y, max_x, max_y)` bounding box |

### Optional methods to override

| Method | When to override |
|---|---|
| `inner_bounds()` | Non-rectangular shapes -- return the largest axis-aligned rectangle fully inside the entity. Default: same as `bounds()`. Used by `fit_within()`. |
| `scale(factor, origin)` | If your entity has geometry beyond its position (radius, endpoints, vertices). The base implementation only scales the position. |
| `rotate(angle, origin)` | If your entity has geometry that should rotate (endpoints, vertices, internal angles). The base implementation only rotates the position. |
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

### Step 2: Implement anchor_names and anchor()

Anchors are named points on your entity that other entities can connect to or reference.

```python
@property
def anchor_names(self) -> list[str]:
    return ["center", "top", "bottom", "left", "right"]

def anchor(self, name: str = "center") -> Coord:
    if name == "center":
        return self.position
    elif name == "top":
        return Coord(self.x, self.y - self.size)
    elif name == "bottom":
        return Coord(self.x, self.y + self.size)
    elif name == "left":
        return Coord(self.x - self.size, self.y)
    elif name == "right":
        return Coord(self.x + self.size, self.y)
    raise ValueError(
        f"CrossHair has no anchor '{name}'. "
        f"Available: {self.anchor_names}"
    )
```

!!! tip "Anchor naming conventions"
    - Always include `"center"` -- connections default to it.
    - Use compass-style names for directional anchors: `"top"`, `"bottom"`, `"left"`, `"right"`.
    - For path-like entities, use `"start"`, `"center"`, `"end"`.

### Step 3: Implement bounds()

Return the axis-aligned bounding box as `(min_x, min_y, max_x, max_y)`. This is used by `fit_to_cell()`, `fit_within()`, and `place_beside()`.

```python
def bounds(self) -> tuple[float, float, float, float]:
    return (
        self.x - self.size,
        self.y - self.size,
        self.x + self.size,
        self.y + self.size,
    )
```

For the crosshair, `inner_bounds()` would be trivially small (the intersection point), so we leave the default which returns the same as `bounds()`.

### Step 4: Implement to_svg()

This is where your entity becomes visible. Return a valid SVG element string.

```python
def to_svg(self) -> str:
    # Horizontal arm
    h = (
        f'<line x1="{self.x - self.size}" y1="{self.y}" '
        f'x2="{self.x + self.size}" y2="{self.y}" '
        f'stroke="{self.color}" stroke-width="{self.width}" '
        f'stroke-linecap="round"'
    )
    # Vertical arm
    v = (
        f'<line x1="{self.x}" y1="{self.y - self.size}" '
        f'x2="{self.x}" y2="{self.y + self.size}" '
        f'stroke="{self.color}" stroke-width="{self.width}" '
        f'stroke-linecap="round"'
    )

    # Wrap in a group
    parts = [f'<g']
    if self.opacity < 1.0:
        parts.append(f' opacity="{self.opacity}"')
    parts.append(f'>{h} />{v} /></g>')
    return ''.join(parts)
```

!!! note "SVG output rules"
    - Return a **single** SVG element. Use `<g>` to group multiple sub-elements.
    - Only emit optional attributes (like `opacity`) when they differ from defaults.
    - The scene indents your output with `f"  {svg}"`, so do not add leading whitespace.

### Step 5: Implement scale() and rotate()

The base `Entity.scale()` and `Entity.rotate()` only move the position relative to an origin. If your entity has internal geometry (like `size`), you must override these methods.

```python
def scale(
    self,
    factor: float,
    origin: Coord | tuple[float, float] | None = None,
) -> CrossHair:
    # Scale the internal geometry
    self.size *= factor
    self.width *= factor

    # Also scale position relative to origin (if given)
    if origin is not None:
        super().scale(factor, origin)

    return self

def rotate(
    self,
    angle: float,
    origin: Coord | tuple[float, float] | None = None,
) -> CrossHair:
    # For a crosshair, rotation doesn't change the + shape
    # (it's symmetric), but we still rotate the position.
    if origin is not None:
        super().rotate(angle, origin)
    return self
```

!!! tip "The scale/rotate pattern"
    1. **Scale internal geometry** (radius, size, endpoints, vertices).
    2. **Call `super().scale(factor, origin)`** to handle position scaling.
    3. Return `self` for method chaining.

    For entities with rotation-sensitive geometry (like Line, Polygon), override `rotate()` to transform all internal points. See `Line.rotate()` for a full example.

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

    def anchor(self, name: str = "center") -> Coord:
        if name == "center":
            return self.position
        elif name == "top":
            return Coord(self.x, self.y - self.size)
        elif name == "bottom":
            return Coord(self.x, self.y + self.size)
        elif name == "left":
            return Coord(self.x - self.size, self.y)
        elif name == "right":
            return Coord(self.x + self.size, self.y)
        raise ValueError(
            f"CrossHair has no anchor '{name}'. "
            f"Available: {self.anchor_names}"
        )

    def bounds(self) -> tuple[float, float, float, float]:
        return (
            self.x - self.size,
            self.y - self.size,
            self.x + self.size,
            self.y + self.size,
        )

    def scale(
        self,
        factor: float,
        origin: Coord | tuple[float, float] | None = None,
    ) -> CrossHair:
        self.size *= factor
        self.width *= factor
        if origin is not None:
            super().scale(factor, origin)
        return self

    def rotate(
        self,
        angle: float,
        origin: Coord | tuple[float, float] | None = None,
    ) -> CrossHair:
        if origin is not None:
            super().rotate(angle, origin)
        return self

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
ch1.connect(ch2, shape=Line(), start_anchor="right", end_anchor="left",
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
- [ ] `anchor()` raises `ValueError` for unknown names
- [ ] `bounds()` returns `(min_x, min_y, max_x, max_y)`
- [ ] `to_svg()` returns a single SVG element (use `<g>` for multiple)
- [ ] `scale()` scales internal geometry **and** calls `super().scale()`
- [ ] `rotate()` handles internal geometry if shape is asymmetric
- [ ] Opacity attributes are only emitted when not equal to 1.0
- [ ] `__repr__` is implemented for debugging
- [ ] Works with `cell.add()` and `fit_to_cell()`

!!! tip "The simplest built-in entity: Point"
    For a minimal real-world example, look at `pyfreeform/entities/point.py`. The `Point` entity renders nothing (`to_svg()` returns `""`) and exists purely as a movable positional anchor. It has a single `"center"` anchor, zero-size bounds, and no internal geometry to scale or rotate. Its primary use is as a reactive vertex for `Polygon` — see [Reactive Polygons](../guide/06-shapes-and-polygons.md#reactive-polygons).
