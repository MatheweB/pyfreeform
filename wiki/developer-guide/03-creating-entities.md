
# Creating Custom Entities

Tutorial: Build your own entity type.

## Minimal Entity

```python
from pyfreeform.core.entity import Entity
from pyfreeform.core.point import Point
from pyfreeform import Color

class Star(Entity):
    """5-pointed star entity."""
    
    def __init__(self, x, y, size=20, color="gold", z_index=0):
        super().__init__(x, y, z_index)
        self.size = size
        self._color = Color(color)
    
    @property
    def anchor_names(self) -> list[str]:
        return ["center"] + [f"point{i}" for i in range(5)]
    
    def anchor(self, name: str) -> Point:
        if name == "center":
            return self.position
        # Calculate point positions...
        # (implementation details)
        raise ValueError(f"Unknown anchor: {name}")
    
    def bounds(self) -> tuple[float, float, float, float]:
        # Return (min_x, min_y, max_x, max_y)
        return (
            self.x - self.size,
            self.y - self.size,
            self.x + self.size,
            self.y + self.size
        )
    
    def to_svg(self) -> str:
        # Generate SVG path for star
        return f'<path d="..." fill="{self._color.to_hex()}" />'
```

![Custom Star entity rendered at different sizes](./_images/03-creating-entities/01-custom-star-entity.svg)

![Star entity anchor points: center and 5 outer points](./_images/03-creating-entities/02-star-entity-anchors.svg)

## Usage

```python
star = Star(100, 100, size=30, color="gold")
scene.add(star)
```

![Custom Star entity used in a grid pattern alongside built-in entities](./_images/03-creating-entities/03-using-custom-entity.svg)

![Transformations applied to custom entity: original, rotated, scaled, combined](./_images/03-creating-entities/04-custom-entity-transformations.svg)

## Built-in vs Custom Entities

PyFreeform provides several built-in entity types. Custom entities follow the same pattern but add your own rendering logic.

![Comparison of built-in entity types versus custom entities](./_images/03-creating-entities/05-builtin-vs-custom.svg)

## Implementation Requirements

Every custom entity must implement four abstract methods: `anchor()`, `anchor_names`, `bounds()`, and `to_svg()`.

![Implementation requirements checklist for custom entities](./_images/03-creating-entities/06-implementation-requirements.svg)

## Entity Integration

Custom entities integrate seamlessly with scenes, grids, connections, and the `along=` positioning system.

![Custom entity integration with the PyFreeform ecosystem](./_images/03-creating-entities/07-entity-integration.svg)

## Creating Custom Caps

PyFreeform's cap system is extensible via a registry. Built-in caps like `"round"`, `"square"`, and `"butt"` use native SVG `stroke-linecap`. Marker-based caps like `"arrow"` use SVG `<marker>` elements, and you can register your own.

### How It Works

1. Write a function that generates an SVG `<marker>` element
2. Call `register_cap(name, generator)` to register it
3. Use it like any other cap: `cell.add_line(end_cap="my_cap")`

The Scene automatically collects and deduplicates markers at render time.

### Example: Diamond Cap

```python
from pyfreeform import register_cap

def _diamond_marker(marker_id: str, color: str, size: float) -> str:
    """Generate a diamond-shaped marker."""
    return (
        f'<marker id="{marker_id}" viewBox="0 0 10 10" '
        f'refX="5" refY="5" '
        f'markerWidth="{size}" markerHeight="{size}" '
        f'orient="auto-start-reverse">'
        f'<polygon points="5,0 10,5 5,10 0,5" fill="{color}" />'
        f'</marker>'
    )

register_cap("diamond", _diamond_marker)

# Now use it
cell.add_line(start="left", end="right", end_cap="diamond")
```

### Generator Function Signature

```python
def my_cap(marker_id: str, color: str, size: float) -> str:
```

- `marker_id`: Unique ID for the `<marker>` element (generated automatically)
- `color`: Hex color string matching the line's stroke color
- `size`: Marker size in pixels (typically `3 * stroke_width`)

The function must return a complete `<marker>...</marker>` SVG string.

### Key SVG Attributes

- `orient="auto-start-reverse"` makes one definition work for both `marker-start` and `marker-end`
- `refX`/`refY` control where the marker attaches to the line endpoint
- `viewBox` defines the coordinate space for the marker's content
- `markerWidth`/`markerHeight` control the rendered size

### Where Caps Live

The cap registry is in `pyfreeform/config/caps.py`. See the built-in `_arrow_marker` function for a reference implementation.

## See Also
- [Entity System](02-entity-system.md)
- [Pathable Protocol](04-pathable-protocol.md)
