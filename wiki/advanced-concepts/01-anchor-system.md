
# Anchor System

Anchors are named reference points on entities that enable precise positioning and dynamic connections. They provide a robust, semantic way to reference specific locations on shapes without manual coordinate calculations.

## What are Anchors?

An **anchor** is a named point on an entity that you can reference programmatically. Instead of calculating coordinates manually, you simply ask for an anchor by name - like "center", "top_left", or "end" - and the system returns the exact position, accounting for the entity's current location, size, and transformations.

!!! info "Coordinate-Free Positioning"
    Anchors eliminate the need to track coordinates. Whether an entity has moved, rotated, or scaled, its anchors always return the correct current positions.

Every entity in PyFreeform has a set of anchors appropriate to its geometry. These anchors are **dynamic** - they update automatically when the entity changes.

### Anchor Points by Entity Type

Every entity has **anchors** - named points you can reference:

#### Dots
- `center`

![Dot anchor point](./_images/01-anchor-system/01-anchors-dot.svg)

Dots are simple circular entities with a single anchor at their center. This is the most common anchor point for connections.

#### Lines
- `start`, `center`, `end`

![Line anchor points](./_images/01-anchor-system/02-anchors-line.svg)

Lines provide anchors at both endpoints and the midpoint. Use these to attach additional entities or create connections at specific positions along the line.

#### Ellipses
- `center`, `right`, `top`, `left`, `bottom`

![Ellipse anchor points](./_images/01-anchor-system/03-anchors-ellipse.svg)

Ellipses have anchors at the center and at the four cardinal points on the perimeter. These anchors respect the ellipse's rotation, so `top` always refers to the topmost point in the current orientation.

!!! tip "Rotated Ellipses"
    When you rotate an ellipse, the cardinal anchors (`top`, `bottom`, `left`, `right`) rotate with it. They always refer to the actual visual position, not the original orientation.

#### Rectangles
- `center`, `top_left`, `top_right`, `bottom_left`, `bottom_right`, `top`, `bottom`, `left`, `right`

![Rectangle anchor points](./_images/01-anchor-system/04-anchors-rectangle.svg)

Rectangles offer the most comprehensive anchor set: all four corners, all four midpoints of edges, and the center. This makes rectangles ideal for creating complex connection patterns.

#### Polygons
- `center`, `v0`, `v1`, `v2`, ... (vertices)

![Polygon anchor points](./_images/01-anchor-system/05-anchors-polygon.svg)

Polygons provide anchors at each vertex, numbered sequentially starting from `v0`. The center anchor is the geometric centroid of all vertices.

!!! note "Vertex Numbering"
    Vertex anchors follow the order you specified when creating the polygon. `v0` is the first vertex, `v1` is the second, and so on.

#### Curves
- `start`, `center`, `end`, `control`

![Curve anchor points](./_images/01-anchor-system/06-anchors-curve.svg)

Quadratic Bézier curves expose four anchors: the two endpoints, the control point, and the midpoint of the curve (not the line between endpoints).

#### Text
- `center`

Text entities have a single anchor at their center point, similar to dots.

![All entity types with their anchor points](./_images/01-anchor-system/14-example-all-entity-types.svg)

## Using Anchors

The anchor system provides two main interfaces: retrieving anchor positions and listing available anchors.

### Getting Anchor Positions

Call the `anchor()` method on any entity with an anchor name to get a `Point` object:

```python
# Get anchor point
center = entity.anchor("center")
top_left = rect.anchor("top_left")
end_point = line.anchor("end")

# Point objects have x and y attributes
print(f"Center is at ({center.x}, {center.y})")

# Points are also subscriptable
x_coord = center[0]  # Same as center.x
y_coord = center[1]  # Same as center.y
```

![Getting anchor points from entities](./_images/01-anchor-system/07-using-anchors-get.svg)

!!! tip "Point Objects"
    The `Point` type is a `NamedTuple` with `x` and `y` fields. You can access coordinates via attributes (`point.x`) or subscripting (`point[0]`).

### Listing Available Anchors

Every entity has an `anchor_names` property that returns a list of available anchor names:

```python
# List available anchors
rect = cell.add_fill(color="lightgray")
print(rect.anchor_names)
# Output: ['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right',
#          'top', 'bottom', 'left', 'right']

dot = cell.add_dot()
print(dot.anchor_names)
# Output: ['center']

polygon = cell.add_polygon([(0, 0), (50, 0), (50, 50)])
print(polygon.anchor_names)
# Output: ['center', 'v0', 'v1', 'v2']
```

This is especially useful for polygons, where the number of vertex anchors depends on how many vertices you created.

### Using Anchors in Connections

Anchors are fundamental to creating connections between entities:

```python
# Connect via anchors
dot1.connect(dot2, start_anchor="center", end_anchor="center")
```

![Getting anchor points and connecting via anchors](./_images/01-anchor-system/08-using-anchors-connect.svg)

The Connection API uses anchor names to determine where lines attach to entities. See the [Connections](02-connections.md) page for complete details.

## Why Anchors?

Anchors provide four key advantages over manual coordinate management:

### 1. Named References - No Manual Calculation

Without anchors, you'd need to calculate positions manually:

```python
# Without anchors (tedious and error-prone)
rect_x, rect_y, rect_w, rect_h = rect.bounds
center_x = rect_x + rect_w / 2
center_y = rect_y + rect_h / 2

# With anchors (simple and clear)
center = rect.anchor("center")
```

![Named references eliminate manual coordinate calculation](./_images/01-anchor-system/09-why-anchors-named-refs.svg)

!!! warning "Avoid Manual Calculations"
    Calculating positions manually is error-prone and breaks when entities change. Always prefer anchors when they're available.

### 2. Auto-Updating - Dynamic Behavior

Anchors always reflect the entity's current state. When an entity moves, rotates, or scales, its anchors update automatically:

```python
rect = cell.add_fill(color="lightgray")
top_left = rect.anchor("top_left")  # Returns Point(x=10, y=10)

# Move the rectangle
rect.move_by(50, 50)
top_left = rect.anchor("top_left")  # Now returns Point(x=60, y=60)
```

![Auto-updating connections when entities move](./_images/01-anchor-system/10-why-anchors-auto-updating.svg)

This auto-updating property is crucial for connections, which use anchors to track entity positions frame-by-frame.

### 3. Semantic Meaning - Clear Intent

Anchor names communicate intent directly in code. Compare these two approaches:

```python
# Unclear intent
pos = (entity.bounds[0] + entity.bounds[2], entity.bounds[1])

# Clear intent
pos = entity.anchor("top_right")
```

The second version is self-documenting - anyone reading the code immediately understands you want the top-right corner.

### 4. Transform-Aware - Rotation and Scaling

Anchors account for transformations. If you rotate a rectangle, its corner anchors rotate with it:

```python
rect = cell.add_rect(width=50, height=30, rotation=45, fill="lightgray")

# All anchors respect the rotation
top_left = rect.anchor("top_left")  # Actual top-left in rotated frame
center = rect.anchor("center")      # Always returns true center
```

![Transform-aware anchors track rotation and scaling](./_images/01-anchor-system/11-why-anchors-transform-aware.svg)

!!! info "Transform Inheritance"
    Anchors work correctly even with nested transformations. If a cell is rotated and the entity within it is also rotated, anchors account for both transformations.

## Anchors and Transforms

Anchors automatically incorporate all transformations applied to their entity:

### Position Transforms

When you move an entity, all its anchors move:

```python
line = cell.add_line(start="top_left", end="top_right")
print(line.anchor("start"))  # Point at top-left of cell

line.move_by(50, 50)
print(line.anchor("start"))  # Shifted by (50, 50)
```

### Rotation Transforms

Rotated entities have rotated anchors:

```python
rect = cell.add_rect(width=50, height=30, rotation=90, fill="lightgray")

# The "right" anchor is actually at the visual top after 90° rotation
right = rect.anchor("right")
```

### Scale Transforms

Scaled entities have appropriately scaled anchor positions:

```python
rect = cell.add_rect(width=50, height=30, fill="lightgray")
rect.scale(1.5)  # Anchors move outward with the scaled dimensions
top_right = rect.anchor("top_right")
```

## Practical Use Cases

### Use Case 1: Precise Positioning

Position new entities relative to existing ones without calculating coordinates:

```python
# Position a dot at the end of a line
line = cell.add_line(start="top_left", end="bottom_right")
line_end = line.anchor("end")
cell.add_dot(at=line_end, radius=5, color="red")
```

![Positioning a dot relative to an anchor point](./_images/01-anchor-system/12-example-position-relative.svg)

### Use Case 2: Connecting Entities

Create dynamic connections between specific points on entities:

```python
# Connect a fill rect's corner to a dot center
rect = cell1.add_fill(color="lightgray")
dot = cell2.add_dot()
connection = rect.connect(dot, start_anchor="bottom_right", end_anchor="center")
```

![Dynamic connection between a rectangle and dot via anchors](./_images/01-anchor-system/13-example-dynamic-connections.svg)

### Use Case 3: Building Compound Shapes

Combine multiple entities precisely using anchors:

```python
# Create a flag: tall rectangle as pole
pole = cell.add_rect(width=5, height=80, fill="brown")
pole_top = pole.anchor("top")

# Position flag triangle at top of pole
flag = cell.add_polygon(
    vertices=[
        (0.4, 0.1),
        (0.9, 0.2),
        (0.4, 0.3)
    ],
    fill="red"
)
```

### Use Case 4: Grid Alignment

Align entities to grid positions using cell anchors:

```python
for row in range(3):
    for col in range(3):
        cell = scene.grid[row, col]

        # Place dots at corners using named positions
        cell.add_dot(at="top_left", radius=3, color="blue")
        cell.add_dot(at="top_right", radius=3, color="blue")
        cell.add_dot(at="bottom_left", radius=3, color="blue")
        cell.add_dot(at="bottom_right", radius=3, color="blue")
```

### Use Case 5: Pathable Interface Integration

Use anchors with the Pathable interface to position elements along connections:

```python
from pyfreeform import Connection

rect1 = cell1.add_fill(color="lightgray")
rect2 = cell2.add_fill(color="lightgray")

connection = Connection(
    start=rect1,
    end=rect2,
    start_anchor="right",
    end_anchor="left"
)
scene.add(connection)

# Position a dot at the midpoint of the connection
midpoint = connection.point_at(0.5)
cell.add_dot(at=midpoint, radius=4, color="orange")
```

## Common Patterns

### Pattern: Corner Decoration

Add visual elements at entity corners:

```python
rect = cell.add_rect(width=80, height=60, fill=None, stroke="black", stroke_width=1)

# Add dots at all four corners
for anchor_name in ["top_left", "top_right", "bottom_left", "bottom_right"]:
    corner = rect.anchor(anchor_name)
    cell.add_dot(at=corner, radius=4, color="red", z_index=10)
```

### Pattern: Edge Midpoints

Place entities at the midpoints of rectangle edges:

```python
rect = cell.add_rect(width=80, height=60, fill=None, stroke="black", stroke_width=1)

# Add dots at edge midpoints
for anchor_name in ["top", "bottom", "left", "right"]:
    midpoint = rect.anchor(anchor_name)
    cell.add_dot(at=midpoint, radius=4, color="blue", z_index=10)
```

### Pattern: Polygon Vertex Markers

Highlight vertices of a polygon:

```python
polygon = cell.add_polygon(
    vertices=[(20, 20), (80, 30), (70, 70), (30, 60)],
    fill="lightblue",
    stroke="navy"
)

# Mark each vertex
for anchor_name in polygon.anchor_names:
    if anchor_name.startswith("v"):  # Vertex anchors
        vertex_pos = polygon.anchor(anchor_name)
        cell.add_dot(at=vertex_pos, radius=5, color="red", z_index=10)
```

### Pattern: Curve Control Point Visualization

Show the control point of a Bézier curve:

```python
curve = cell.add_curve(
    start="left",
    end="right",
    curvature=0.8,
    color="blue",
    width=2
)

# Visualize control point
control_pos = curve.anchor("control")
cell.add_dot(at=control_pos, radius=4, color="red", z_index=10)

# Draw lines from endpoints to control point
cell.add_line(start=curve.anchor("start"), end=control_pos,
              color="gray", width=1, z_index=5)
cell.add_line(start=curve.anchor("end"), end=control_pos,
              color="gray", width=1, z_index=5)
```

### Pattern: Radial Layout

Position entities radially around a central anchor:

```python
import math

center_dot = cell.add_dot(at=(50, 50), radius=5, color="black")
center_pos = center_dot.anchor("center")

# Create 8 dots in a circle around the center
num_dots = 8
radius = 30

for i in range(num_dots):
    angle = (2 * math.pi * i) / num_dots
    x = center_pos.x + radius * math.cos(angle)
    y = center_pos.y + radius * math.sin(angle)

    outer_dot = cell.add_dot(at=(x, y), radius=4, color="blue")

    # Connect to center
    center_dot.connect(outer_dot)
```

## API Reference

### Entity.anchor(name: str) -> Point

Returns the position of the named anchor as a `Point` object.

**Parameters:**
- `name` (str): The anchor name (e.g., "center", "top_left", "v0")

**Returns:**
- `Point`: A named tuple with `x` and `y` fields

**Raises:**
- `ValueError`: If the anchor name doesn't exist for this entity type

**Example:**
```python
rect = cell.add_fill(color="lightgray")
center = rect.anchor("center")
print(f"Center: ({center.x}, {center.y})")
```

### Entity.anchor_names -> list[str]

Property that returns a list of all available anchor names for this entity.

**Returns:**
- `list[str]`: List of anchor name strings

**Example:**
```python
polygon = cell.add_polygon([(0, 0), (50, 0), (25, 50)])
print(polygon.anchor_names)  # ['center', 'v0', 'v1', 'v2']
```

## Complete Anchor Reference

| Entity Type | Available Anchors |
|------------|-------------------|
| **Dot** | `center` |
| **Line** | `start`, `center`, `end` |
| **Curve** | `start`, `center`, `end`, `control` |
| **Ellipse** | `center`, `right`, `top`, `left`, `bottom` |
| **Rect** | `center`, `top_left`, `top_right`, `bottom_left`, `bottom_right`, `top`, `bottom`, `left`, `right` |
| **Polygon** | `center`, `v0`, `v1`, `v2`, ... (one per vertex) |
| **Text** | `center` |

!!! note "Cell Anchors"
    Cells themselves don't have anchors, but you can access cell bounds through the `cell.bounds` property, which returns `(x, y, width, height)`.

## Troubleshooting

### Invalid Anchor Name

```python
rect = cell.add_fill(color="lightgray")
pos = rect.anchor("middle")  # ValueError: No anchor named 'middle'
```

**Solution:** Use `entity.anchor_names` to see available anchors for the entity type.

### Anchors Not Updating

If anchors seem stuck after transformations:

1. Ensure you're calling `anchor()` after the transformation, not caching the result before
2. Check that the entity is properly added to a cell
3. Verify the entity isn't being recreated (which would reset its position)

### Point vs Tuple Confusion

Anchors return `Point` objects, not plain tuples:

```python
pos = rect.anchor("center")

# These work
x = pos.x
y = pos.y
x, y = pos  # Unpacking works

# This also works (subscripting)
x = pos[0]
y = pos[1]
```

## See Also
- [Connections](02-connections.md) - Dynamic links using anchors
- [Entities](../fundamentals/03-entities.md) - All entity types and their properties
- [Pathable Interface](../api-reference/pathable.md) - Positioning along paths and connections
