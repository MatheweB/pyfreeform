
# Entities

Entities are the visual elements you draw in PyFreeform - dots, lines, curves, ellipses, polygons, text, and more. Understanding the entity system unlocks the full creative power of the library.

---

## What is an Entity?

An **Entity** is any drawable object in your artwork. All entities share common behavior but have type-specific properties.

Think of entities as the building blocks of your art - like shapes in a vector editor, but with powerful positioning and connection capabilities.

---

## Entity Types

PyFreeform provides these built-in entity types:

| Entity | Description | Use For |
|--------|-------------|---------|
| **[Dot](../entities/01-dots.md)** | Filled circle | Points, pixels, particles |
| **[Line](../entities/02-lines.md)** | Straight path | Connections, grids, structure |
| **[Curve](../entities/03-curves.md)** | Bézier curve | Organic flows, smooth paths |
| **[Ellipse](../entities/04-ellipses.md)** | Oval or circle | Radial elements, orbits |
| **[Polygon](../entities/05-polygons.md)** | Custom shape | Geometric forms, icons |
| **[Text](../entities/06-text.md)** | Typography | Labels, titles, annotations |
| **[Rect](../entities/07-rectangles.md)** | Rectangle | Backgrounds, borders, boxes |
| **[EntityGroup](../entities/08-entity-groups.md)** | Composite shape | Custom stamps, reusable patterns |

Each type has detailed documentation - see the [Entities section](../entities/01-dots.md).

![Entity Types Overview](./_images/03-entities/01-entity-types-overview.svg)

---

## Common Entity Behavior

All entities share these fundamental properties and methods:

### Position

Every entity has a position (x, y coordinates):

```python
entity.position     # Point(x, y)
entity.x            # X coordinate
entity.y            # Y coordinate
```

![Entity Position](./_images/03-entities/02-entity-position.svg)

### Movement

Move entities absolutely or relatively:

```python
# Absolute positioning
entity.move_to(100, 200)
entity.move_to(Point(100, 200))

# Relative offset
entity.move_by(dx=10, dy=-5)
entity.translate(10, -5)  # Same as move_by
```

![Entity Movement](./_images/03-entities/03-entity-movement.svg)

### Transforms

Rotate, scale, and transform entities:

```python
# Rotation (degrees, counterclockwise)
entity.rotate(45)
entity.rotate(30, origin=Point(100, 100))

# Scaling
entity.scale(2.0)              # Double size
entity.scale(0.5, origin=center)  # Half size around point
```

![Entity Rotation](./_images/03-entities/04-entity-rotation.svg)
![Entity Scaling](./_images/03-entities/05-entity-scaling.svg)

See [Transforms](../advanced-concepts/04-transforms.md) for details.

### Layering

Control render order with z-index:

```python
entity.z_index = 0    # Default layer
entity.z_index = 10   # Render on top
entity.z_index = -5   # Render below
```

![Entity Z-Index](./_images/03-entities/06-entity-z-index.svg)

Higher z-index values render on top. See [Layering](05-layering.md).

### Anchors

Access named reference points on entities:

```python
# Get anchor point
center = entity.anchor("center")

# List available anchors
names = entity.anchor_names

# Example: Connect via anchors
line_start = line.anchor("start")
line_end = line.anchor("end")
```

See [Anchor System](../advanced-concepts/01-anchor-system.md) for details.

### Bounds

Get the bounding box:

```python
min_x, min_y, max_x, max_y = entity.bounds()
```

### Cell Association

When created via cell methods, entities know their cell:

```python
entity.cell  # The cell that contains this entity (or None)
```

### Custom Data

Store arbitrary data on entities:

```python
entity.data["category"] = "important"
entity.data["weight"] = 0.8

# Later
if entity.data.get("category") == "important":
    entity.scale(1.5)
```

---

## Creating Entities

### Via Cell Methods (Recommended)

!!! tip "Easiest Way to Create Entities"
    The easiest way - cells handle positioning automatically:

```python
for cell in scene.grid:
    # Returns the created entity
    dot = cell.add_dot(radius=5, color="red")
    line = cell.add_line(start="top_left", end="bottom_right")
    curve = cell.add_curve(curvature=0.5)
```

![Creating via Cell Methods](./_images/03-entities/07-create-via-cell-methods.svg)

Entities are automatically added to the scene.

### Direct Construction

For precise control or non-grid artwork:

```python
from pyfreeform import Dot, Line, Curve

# Create entities
dot = Dot(x=100, y=200, radius=10, color="coral")
line = Line(x1=0, y1=0, x2=800, y2=600, color="gray")
curve = Curve(x1=100, y1=100, x2=400, y2=300, curvature=0.5)

# Add to scene
scene.add(dot)
scene.add(line)
scene.add(curve)
```

![Direct Entity Construction](./_images/03-entities/08-create-direct-construction.svg)

---

## Entity Lifecycle

1. **Creation** - Entity is instantiated
2. **Positioning** - Set initial position
3. **Styling** - Apply visual properties
4. **Transformation** - Rotate, scale, move (optional)
5. **Connection** - Link to other entities (optional)
6. **Rendering** - SVG generation during save

---

## Working with Entities

### Store References

Keep references for later manipulation:

```python
# Store entities for later
dots = []
for cell in scene.grid:
    dot = cell.add_dot(color="red", radius=3)
    dots.append(dot)

# Transform later
for dot in dots:
    dot.scale(1.5)
```

![Storing Entity References](./_images/03-entities/09-store-references.svg)

### Group Entities

Use Python lists for organization, or `EntityGroup` for reusable composite shapes:

```python
# Python lists for ad-hoc grouping
bright_dots = []
dark_dots = []

for cell in scene.grid:
    dot = cell.add_dot(color=cell.color)

    if cell.brightness > 0.5:
        bright_dots.append(dot)
    else:
        dark_dots.append(dot)

# Bulk operations
for dot in bright_dots:
    dot.scale(1.2)
```

![Grouping Entities](./_images/03-entities/10-group-entities.svg)

For reusable composite shapes, use `EntityGroup`:

```python
from pyfreeform import EntityGroup, Dot

flower = EntityGroup()
flower.add(Dot(0, 0, radius=10, color="coral"))
# ... add more children relative to (0, 0)

cell.place(flower)          # Place like any entity
flower.fit_to_cell(0.75)    # Auto-scale to fit
```

See [Entity Groups](../entities/08-entity-groups.md) and [Groups Example](../examples/intermediate/groups.md).

### Query Entities

Access all entities in a scene:

```python
# All entities
for entity in scene.entities:
    print(f"{type(entity).__name__} at ({entity.x}, {entity.y})")

# Filter by type
dots = [e for e in scene.entities if isinstance(e, Dot)]
lines = [e for e in scene.entities if isinstance(e, Line)]
```

### Connect Entities

Link entities through anchor points:

```python
dot1 = cell1.add_dot(color="red")
dot2 = cell2.add_dot(color="blue")

# Create connection
connection = dot1.connect(
    dot2,
    start_anchor="center",
    end_anchor="center",
    style={"width": 2, "color": "gray"}
)
```

Connections automatically update when entities move!

See [Connections](../advanced-concepts/02-connections.md).

---

## Entity-Specific Features

Each entity type has unique capabilities:

### Dots
- Simple filled circles
- Radius and color control
- Perfect for point-based art

```python
dot = cell.add_dot(radius=5, color="coral")
```

![Dots](./_images/03-entities/17-entity-specific-dots.svg)

### Lines
- Straight paths between points
- Parametric positioning with `point_at(t)`
- Width and color styling

```python
line = cell.add_line(start="top_left", end="bottom_right", width=2)
point = line.point_at(0.5)  # Midpoint
```

![Lines](./_images/03-entities/18-entity-specific-lines.svg)

### Curves
- Smooth Bézier curves
- Curvature parameter (-1 to 1)
- Parametric positioning along curve

```python
curve = cell.add_curve(curvature=0.5, color="blue")
cell.add_dot(along=curve, t=0.5)
```

![Curves](./_images/03-entities/19-entity-specific-curves.svg)

### Ellipses
- Ovals and circles
- Rotation support
- Parametric positioning around perimeter

```python
ellipse = cell.add_ellipse(rx=15, ry=10, rotation=45)
cell.add_dot(along=ellipse, t=0.25)
```

### Polygons
- Custom vertices
- Built-in shape helpers (triangle, hexagon, star, etc.)
- Fill and stroke styling

```python
from pyfreeform import shapes
cell.add_polygon(shapes.hexagon(), fill="purple")
```

![Polygons](./_images/03-entities/20-entity-specific-polygons.svg)

### Text
- Typography and labels
- Font control
- Alignment options

```python
cell.add_text("Hello", font_size=16, color="white")
```

### Rectangles
- Boxes with fill and stroke
- Useful for backgrounds and borders

```python
cell.add_fill(color="lightgray")  # Fills entire cell
```

See individual entity pages for complete details.

---

## Parametric Positioning

!!! info "Powerful Feature: Position Along Paths"
    One of PyFreeform's most powerful features is positioning entities along paths:

```python
# Create a path (line, curve, or ellipse)
line = cell.add_line(start="left", end="right")

# Position dot along the path
# t=0 is start, t=1 is end, t=0.5 is midpoint
cell.add_dot(along=line, t=0.5, radius=3)

# Use cell data to drive position
cell.add_dot(along=line, t=cell.brightness)
```

![Parametric Line](./_images/03-entities/11-parametric-line.svg)
![Parametric Curve](./_images/03-entities/12-parametric-curve.svg)
![Parametric Ellipse](./_images/03-entities/13-parametric-ellipse.svg)

This works with:
- **Lines** - Linear interpolation
- **Curves** - Bézier parametric position
- **Ellipses** - Position around perimeter
- **Custom paths** - Any object with `point_at(t)` method

See [Parametric Art](../parametric-art/01-what-is-parametric.md) for the mathematical foundations.

---

## Entity Patterns

### Pattern 1: Data-Driven Sizing

```python
for cell in scene.grid:
    # Size based on brightness
    radius = 2 + cell.brightness * 8
    cell.add_dot(radius=radius, color=cell.color)
```

![Data-Driven Sizing](./_images/03-entities/14-pattern-data-driven-sizing.svg)

### Pattern 2: Conditional Types

```python
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_ellipse(rx=10, ry=8, fill=cell.color)
    elif cell.brightness > 0.4:
        cell.add_curve(curvature=0.5, color=cell.color)
    else:
        cell.add_dot(radius=2, color=cell.color)
```

![Conditional Entity Types](./_images/03-entities/15-pattern-conditional-types.svg)

### Pattern 3: Progressive Transformation

```python
dots = []
for cell in scene.grid:
    dot = cell.add_dot(radius=5, color="red")
    dots.append(dot)

# Apply progressive rotation
for i, dot in enumerate(dots):
    angle = (i / len(dots)) * 360
    dot.rotate(angle)
```

![Progressive Transformation](./_images/03-entities/16-pattern-progressive-transformation.svg)

---

## Entity Methods Reference

Common to all entities:

```python
# Position
entity.move_to(x, y)
entity.move_by(dx, dy)
entity.translate(dx, dy)
entity.move_to_cell(cell, at="center")

# Transform
entity.rotate(angle, origin=None)
entity.scale(factor, origin=None)

# Fitting
entity.fit_to_cell(scale=1.0, recenter=True)

# Anchors
entity.anchor(name)
entity.anchor_names

# Bounds
entity.bounds()

# Connections
entity.connect(other, start_anchor, end_anchor, style)

# Rendering
entity.to_svg()
```

---

## Tips and Best Practices

!!! tip "Use Cell Methods"
    They're simpler and handle positioning automatically:

```python
# Prefer this
cell.add_dot(radius=5)

# Over this
dot = Dot(cell.center.x, cell.center.y, radius=5)
scene.add(dot)
```

### Store References When Needed

If you'll manipulate entities later, keep references:

```python
dots = []
for cell in scene.grid:
    dot = cell.add_dot(color="red")
    dots.append(dot)  # Keep reference
```

### Use Z-Index for Layering

Control what renders on top:

```python
cell.add_fill(color="gray", z_index=0)      # Background
cell.add_line(start="left", end="right", z_index=1)
cell.add_dot(radius=5, z_index=2)           # Foreground
```

### Leverage Parametric Positioning

Position along paths for smooth, flowing compositions:

```python
curve = cell.add_curve(curvature=0.5)
for i in range(5):
    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0
    cell.add_dot(along=curve, t=t, radius=2)
```

---

## Next Steps

- **Explore styling**: [Styling](04-styling.md)
- **Learn layering**: [Layering](05-layering.md)
- **Deep dive on specific entities**: [Entities Section](../entities/01-dots.md)
- **Try parametric art**: [Parametric Art](../parametric-art/01-what-is-parametric.md)

---

## See Also

- 📖 [Styling](04-styling.md) - Colors and visual properties
- 📖 [Layering](05-layering.md) - Z-index system
- 📖 [Dots](../entities/01-dots.md) - Simple circles
- 📖 [Lines](../entities/02-lines.md) - Straight paths
- 📖 [Curves](../entities/03-curves.md) - Bézier curves with math
- 📖 [Entity Groups](../entities/08-entity-groups.md) - Reusable composite shapes
- 🎯 [Quick Start Example](../examples/beginner/quick-start.md)
- 🔍 [Entities API Reference](../api-reference/entities.md)

