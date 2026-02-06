
# Entity System

How entities work internally.

## Entity Base Class

All entities inherit from `Entity`:

```python
class Entity(ABC):
    def __init__(self, x, y, z_index=0):
        self._position = Point(x, y)
        self._z_index = z_index
        self._connections = WeakSet()
        self._cell = None
        self.data = {}
    
    # Abstract methods (must implement)
    @abstractmethod
    def anchor(self, name: str) -> Point:
        """Get anchor point by name."""
        pass
    
    @property
    @abstractmethod
    def anchor_names(self) -> list[str]:
        """List available anchors."""
        pass
    
    @abstractmethod
    def to_svg(self) -> str:
        """Render to SVG."""
        pass
    
    @abstractmethod
    def bounds(self) -> tuple[float, float, float, float]:
        """Get bounding box."""
        pass
```

![Visual representation of entity properties: position, z-index, and metadata](./_images/02-entity-system/01-entity-properties-visual.svg)

![Anchor points on different entity types](./_images/02-entity-system/02-abstract-methods-anchors.svg)

## Entity Lifecycle

1. **Construction** - `__init__`
2. **Registration** - Added to scene/cell
3. **Transformation** - rotate/scale/move
4. **Rendering** - `to_svg()` called
5. **Cleanup** - Weak references prevent leaks

![Entity lifecycle stages from construction to cleanup](./_images/02-entity-system/03-entity-lifecycle.svg)

![Transformation examples: original, rotated, scaled, and combined](./_images/02-entity-system/04-lifecycle-transformation.svg)

## Weak References

Entities use `WeakSet` for connections to prevent memory leaks. When an entity is deleted, its connections are automatically cleaned up.

![Weak references explanation: how WeakSet prevents memory leaks between entities](./_images/02-entity-system/05-weak-references-explanation.svg)

## Bounds Method

The `bounds()` method returns a bounding box `(min_x, min_y, max_x, max_y)` used for hit testing, layout, and rendering optimization.

![Bounds method visual: bounding boxes for different entity types](./_images/02-entity-system/06-bounds-method-visual.svg)

## Entity Inheritance

All built-in entities follow the same inheritance pattern from the base `Entity` class, implementing the required abstract methods.

![Entity inheritance pattern showing how built-in types extend the base class](./_images/02-entity-system/07-entity-inheritance-pattern.svg)

## Opacity

Every entity supports an `opacity` parameter (0.0 transparent to 1.0 opaque). Shape entities (Rect, Ellipse, Polygon) additionally support `fill_opacity` and `stroke_opacity` for independent control over fill and stroke transparency.

```python
# Simple opacity — affects the whole entity
cell.add_dot(radius=10, color="coral", opacity=0.5)
cell.add_line(start="left", end="right", color="navy", opacity=0.3)
cell.add_text("Ghost", font_size=14, color="black", opacity=0.4)

# Shape opacity — one value controls both fill and stroke
cell.add_ellipse(rx=20, ry=15, fill="blue", stroke="black", opacity=0.6)

# Independent fill/stroke opacity — override when needed
cell.add_rect(
    width=40, height=30,
    fill="red", stroke="black", stroke_width=2,
    opacity=1.0,            # default
    fill_opacity=0.4,       # translucent fill
    stroke_opacity=1.0,     # solid border
)
```

![Opacity across entity types: overlapping translucent shapes](./_images/02-entity-system/08-opacity-showcase.svg)

## See Also
- [Creating Entities](03-creating-entities.md)
- [Entities](../fundamentals/03-entities.md)
