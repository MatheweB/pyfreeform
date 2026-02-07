
# Entities API Reference

Complete reference for all entity types: Dot, Line, Curve, Ellipse, Polygon, Text, Rect, and EntityGroup.

---

## Entity Base Class

All entities inherit from the `Entity` abstract base class.

```python
class Entity(ABC):
    """Base class for all drawable elements."""

    @abstractmethod
    def to_svg(self) -> str:
        """Generate SVG representation."""

    @abstractmethod
    def anchor(self, name: str) -> Point:
        """Get named anchor point."""

    @property
    @abstractmethod
    def anchor_names(self) -> list[str]:
        """Available anchor point names."""

    @property
    @abstractmethod
    def bounds(self) -> tuple[float, float, float, float]:
        """Bounding box as (x, y, width, height)."""

    @property
    def z_index(self) -> int:
        """Layer order (higher = on top)."""
```

---

## Dot

Simple circle for point-based art.

```python
class Dot(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float = 5,
        color: str = "black",
        z_index: int = 0,
        opacity: float = 1.0
    )
```

**Properties**:
```python
dot.position: Point      # Center (x, y)
dot.x: float            # X coordinate
dot.y: float            # Y coordinate
dot.radius: float       # Radius in pixels (default 5)
dot.color: str          # Fill color
dot.opacity: float      # 0.0-1.0
dot.z_index: int        # Layer order
```

**Anchors**: `["center"]`

**Example**:
```python
dot = Dot(x=100, y=200, radius=5, color="#ff5733")
scene.add(dot)

# Or via cell
cell.add_dot(radius=5, color=cell.color)
```

![Dot Entity Example](./_images/entities/example1-dot.svg)

![Dot Anchors](./_images/entities/example9-dot-anchors.svg)

---

## Line

Straight line between two points.

```python
class Line(Entity, Pathable):
    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0
    )
```

**Properties**:
```python
line.start: Point        # Start point
line.end: Point          # End point
line.color: str          # Stroke color
line.width: float        # Stroke width
line.cap: str            # Default cap: "round", "square", "butt", "arrow"
line.start_cap: str      # Override cap for start end
line.end_cap: str        # Override cap for end end
line.opacity: float      # 0.0-1.0
line.z_index: int        # Layer order
```

**Anchors**: `["start", "center", "end"]`

**Pathable**: `line.point_at(t)` - Get point at parameter t (0-1)

**Example**:
```python
line = Line(x1=0, y1=0, x2=100, y2=100, color="blue", width=2)

# Position dot along line
cell.add_dot(along=line, t=0.5, radius=3)
```

![Line Entity Example](./_images/entities/example2-line.svg)

![Line Anchors](./_images/entities/example10-line-anchors.svg)

---

## Curve

Quadratic Bézier curve.

```python
class Curve(Entity, Pathable):
    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        curvature: float = 0.5,
        width: float = 1,
        color: str = "black",
        z_index: int = 0,
        cap: str = "round",
        start_cap: str | None = None,
        end_cap: str | None = None,
        opacity: float = 1.0
    )
```

**Properties**:
```python
curve.start: Point       # Start point
curve.end: Point         # End point
curve.control: Point     # Control point (calculated)
curve.curvature: float   # Bow amount (-1 to 1)
curve.color: str         # Stroke color
curve.width: float       # Stroke width
curve.cap: str           # Default cap: "round", "square", "butt", "arrow"
curve.start_cap: str     # Override cap for start end
curve.end_cap: str       # Override cap for end end
curve.opacity: float     # 0.0-1.0
curve.z_index: int       # Layer order
```

**Anchors**: `["start", "center", "end", "control"]`

**Pathable**: `curve.point_at(t)` - Get point on curve at parameter t (0-1)

**Mathematics**:
```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂

Where:
  P₀ = start point
  P₁ = control point
  P₂ = end point
  t ∈ [0,1]
```

**Example**:
```python
curve = Curve(x1=0, y1=100, x2=100, y2=0, curvature=0.5, color="red")

# Position along curve
for i in range(5):
    t = i / 4
    cell.add_dot(along=curve, t=t, radius=2)
```

![Curve Entity Example](./_images/entities/example3-curve.svg)

---

## Ellipse

Ellipse or circle with rotation support.

```python
class Ellipse(Entity, Pathable):
    def __init__(
        self,
        x: float,
        y: float,
        rx: float,
        ry: float,
        rotation: float = 0,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None
    )
```

**Properties**:
```python
ellipse.position: Point  # Center
ellipse.x: float         # Center X
ellipse.y: float         # Center Y
ellipse.rx: float        # Horizontal radius
ellipse.ry: float        # Vertical radius
ellipse.rotation: float  # Rotation in degrees
ellipse.fill: str        # Fill color
ellipse.stroke: str      # Stroke color
ellipse.stroke_width: float
ellipse.opacity: float   # Overall opacity (0.0-1.0)
ellipse.fill_opacity: float   # Fill opacity override
ellipse.stroke_opacity: float # Stroke opacity override
ellipse.z_index: int
```

**Anchors**: `["center", "right", "top", "left", "bottom"]`

**Pathable**:
- `ellipse.point_at(t)` - Get point at parameter t (0-1) around perimeter
- `ellipse.point_at_angle(degrees)` - Get point at specific angle

**Mathematics**:
```
Unrotated:
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)

With rotation θ:
x'(t) = x(t)cos(θ) - y(t)sin(θ) + cx
y'(t) = x(t)sin(θ) + y(t)cos(θ) + cy
```

**Example**:
```python
# Circle
ellipse = Ellipse(x=100, y=100, rx=20, ry=20, fill="blue")

# Rotated oval
ellipse = Ellipse(x=100, y=100, rx=30, ry=15, rotation=45, fill="green")

# Position dots around perimeter
for i in range(8):
    t = i / 8
    cell.add_dot(along=ellipse, t=t, radius=2)
```

![Ellipse Entity Example](./_images/entities/example4-ellipse.svg)

---

## Polygon

Custom polygon defined by vertices.

```python
class Polygon(Entity):
    def __init__(
        self,
        vertices: list[tuple[float, float]] | list[Point],
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None
    )
```

**Properties**:
```python
polygon.vertices: list[Point]  # Vertex points
polygon.position: Point        # Centroid (center of mass)
polygon.fill: str
polygon.stroke: str
polygon.stroke_width: float
polygon.opacity: float         # Overall opacity (0.0-1.0)
polygon.fill_opacity: float    # Fill opacity override
polygon.stroke_opacity: float  # Stroke opacity override
polygon.z_index: int
```

**Anchors**: `["center", "v0", "v1", "v2", ...]` - One anchor per vertex

**Methods**:
```python
polygon.rotate(angle: float, origin: Point | None = None)
polygon.scale(factor: float, origin: Point | None = None)
```

**Shape Helpers**:
```python
from pyfreeform import shapes

shapes.triangle()                      # Equilateral triangle
shapes.square()                        # Perfect square
shapes.diamond()                       # Diamond shape
shapes.hexagon()                       # Regular hexagon
shapes.star(points=5, inner_radius=0.4)  # Multi-pointed star
shapes.regular_polygon(n_sides=8)      # Any regular polygon
shapes.squircle(n=4)                   # iOS icon shape!
shapes.rounded_rect(corner_radius=0.2) # Rounded rectangle
```

**Example**:
```python
from pyfreeform import shapes

# Built-in shapes (relative coords 0-1)
cell.add_polygon(shapes.hexagon(), fill="purple")
cell.add_polygon(shapes.star(5), fill="gold")

# Custom vertices (absolute coords)
triangle = [Point(10, 10), Point(50, 10), Point(30, 50)]
poly = Polygon(vertices=triangle, fill="orange")
```

![Polygon Entity Example](./_images/entities/example5-polygon.svg)

![Polygon Shapes Example](./_images/entities/example6-polygon-shapes.svg)

---

## Text

Typography and labels.

```python
class Text(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        content: str,
        font_size: float = 16,
        color: str = "black",
        font_family: str = "sans-serif",
        font_style: str = "normal",
        font_weight: str | int = "normal",
        bold: bool = False,
        italic: bool = False,
        text_anchor: Literal["start", "middle", "end"] = "middle",
        baseline: str = "middle",
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0
    )
```

**Properties**:
```python
text.position: Point     # Anchor point
text.x: float            # X coordinate
text.y: float            # Y coordinate
text.content: str        # Text string
text.font_size: float    # Size in pixels
text.color: str          # Text color
text.font_family: str    # Typeface
text.bold: bool          # Bold weight (sugar for font_weight)
text.italic: bool        # Italic style (sugar for font_style)
text.text_anchor: str    # Horizontal alignment
text.baseline: str       # Vertical alignment
text.rotation: float     # Degrees
text.opacity: float      # 0.0-1.0
text.z_index: int        # Layer order
```

**Anchors**: `["center"]`

**Example**:
```python
# Simple label
text = Text(x=100, y=100, content="Hello", font_size=24, color="white")

# Data display
value = f"{cell.brightness:.2f}"
cell.add_text(value, font_family="monospace", font_size=8)

# Rotated text
cell.add_text("Art", rotation=45, font_size=16)
```

![Text Entity Example](./_images/entities/example7-text.svg)

---

## Rect

Rectangle with fill and stroke.

```python
class Rect(Entity):
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        fill: str | None = "black",
        stroke: str | None = None,
        stroke_width: float = 1,
        rotation: float = 0,
        z_index: int = 0,
        opacity: float = 1.0,
        fill_opacity: float | None = None,
        stroke_opacity: float | None = None
    )
```

**Class Methods**:
```python
Rect.at_center(center, width, height, rotation=0, fill=, ...)
# Create a Rect centered at a point (instead of top-left positioned)
```

**Properties**:
```python
rect.position: Point     # Top-left corner
rect.x: float            # X coordinate
rect.y: float            # Y coordinate
rect.width: float        # Width
rect.height: float       # Height
rect.fill: str           # Fill color
rect.stroke: str         # Stroke color
rect.stroke_width: float
rect.rotation: float     # Rotation in degrees
rect.opacity: float      # Overall opacity (0.0-1.0)
rect.fill_opacity: float # Fill opacity override
rect.stroke_opacity: float # Stroke opacity override
rect.z_index: int
```

**Anchors**: `["center", "top_left", "top_right", "bottom_left", "bottom_right", "top", "bottom", "left", "right"]`

**Example**:
```python
# Background fill
cell.add_fill(color="lightgray", z_index=0)

# Border
cell.add_border(color="black", width=1)

# Custom rectangle
rect = Rect(x=50, y=50, width=100, height=60, fill="blue", stroke="navy", stroke_width=2)
```

![Rect Entity Example](./_images/entities/example8-rect.svg)

![Rect Anchors](./_images/entities/example11-rect-anchors.svg)

---

## EntityGroup

Reusable composite shape — bundle multiple entities into one.

```python
class EntityGroup(Entity):
    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        z_index: int = 0
    )
```

**Methods**:
```python
group.add(entity)       # Add a child entity (positioned relative to 0, 0)
group.scale(factor, origin=None)  # Scale the group
group.fit_to_cell(0.85) # Auto-scale to fit cell
```

**Properties**:
```python
group.children: list[Entity]  # Child entities (copy)
group.x: float                # X position
group.y: float                # Y position
group.z_index: int            # Layer order
```

**Anchors**: `["center"]`

**Example**:
```python
from pyfreeform import EntityGroup, Dot
import math

def make_flower(color="coral", petal_color="gold"):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=10, color=color))
    for i in range(8):
        angle = i * (2 * math.pi / 8)
        g.add(Dot(15 * math.cos(angle), 15 * math.sin(angle),
                   radius=6, color=petal_color))
    return g

# Place like any entity
cell.place(make_flower())
cell.add_entity(make_flower(color="blue"))
scene.add(make_flower().move_to(100, 100))
```

See [Entity Groups guide](../entities/08-entity-groups.md) for full details.

---

## Common Properties and Methods

All entities support these properties:

```python
entity.z_index: int      # Layer order (higher = on top)
entity.position: Point   # Reference position (varies by type)
entity.bounds: tuple     # Bounding box (x, y, width, height)
entity.cell: Cell | None # The cell containing this entity (if any)
```

### Movement Methods

```python
entity.move_to(x, y)     # Move to absolute position
entity.move_by(dx, dy)   # Move relative to current position
entity.move_to_cell(cell, at="center")  # Move to position within cell
```

### Transform Methods

```python
entity.rotate(angle, origin=None)  # Rotate around origin
entity.scale(factor, origin=None)  # Scale around origin
```

See [Transforms Guide](../advanced-concepts/04-transforms.md) for details.

### Relative Positioning Methods

```python
entity.offset_from(anchor_name: str, dx: float = 0, dy: float = 0) -> Point
```

Get a point offset from a named anchor. Useful for placing labels or related elements near an entity.

**Parameters**:
- `anchor_name`: Named anchor on the entity (e.g., "center", "top", "end")
- `dx`, `dy`: Pixel offsets from the anchor

**Example**:
```python
dot = cell.add_dot(radius=8, color="red")
label_pos = dot.offset_from("center", dx=0, dy=-15)
# Use label_pos to place a text label above the dot
```

```python
entity.place_beside(other: Entity, side: str = "right", gap: float = 5) -> Entity
```

Position this entity beside another entity using bounding boxes.

**Parameters**:
- `other`: The reference entity to position beside
- `side`: Which side — "left", "right", "above", "below"
- `gap`: Pixel gap between entities

**Returns**: self (for method chaining)

**Example**:
```python
dot1 = cell.add_dot(radius=8, color="red")
dot2 = cell.add_dot(radius=8, color="blue")
dot2.place_beside(dot1, side="right", gap=10)
```

### fit_to_cell()

Automatically scale and position entity to fit within its cell bounds.

```python
def fit_to_cell(self, scale: float = 1.0, recenter: bool = True) -> Entity
```

**Parameters**:
- `scale`: Percentage of cell to fill (0.0-1.0). Default 1.0 = fill entire cell
- `recenter`: If True, center entity in cell after scaling. Default True

**Returns**: self (for method chaining)

**How it works**:
1. Calculates the entity's bounding box (handles rotation automatically)
2. Scales the entity to fit within the specified percentage of the cell
3. Optionally recenters the entity within the cell

**Example**:
```python
# Create large ellipse and auto-fit to cell
ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45)
ellipse.fit_to_cell(0.85)  # Scale to 85% of cell size

# Create rotated polygon and fit
from pyfreeform import shapes
poly = cell.add_polygon(shapes.star(5), fill="gold")
poly.rotate(30, cell.center)  # Rotate first
poly.fit_to_cell(0.9)         # Then auto-fit

# Without recentering (keeps current position)
entity.fit_to_cell(0.8, recenter=False)
```

**Use cases**:
- Ensuring shapes don't overlap cell boundaries
- Creating consistent sizing across grid cells
- Auto-constraining after rotation or transforms

See [Fit to Cell Guide](../advanced-concepts/05-fit-to-cell.md) for more examples.

![All Entity Types](./_images/entities/example12-all-entities.svg)

---

## See Also

- 📖 [Dots](../entities/01-dots.md) - Dot entity guide
- 📖 [Lines](../entities/02-lines.md) - Line entity guide
- 📖 [Curves](../entities/03-curves.md) - Curve mathematics
- 📖 [Ellipses](../entities/04-ellipses.md) - Ellipse mathematics
- 📖 [Polygons](../entities/05-polygons.md) - Polygon shapes
- 📖 [Text](../entities/06-text.md) - Text typography
- 📖 [Rectangles](../entities/07-rectangles.md) - Rectangle guide
- 📖 [Entity Groups](../entities/08-entity-groups.md) - Reusable composite shapes

