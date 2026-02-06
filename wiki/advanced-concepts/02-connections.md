
# Connections

Connections create dynamic links between entities that automatically update when entities move. They form the foundation of data visualizations, network diagrams, and interactive graphics in PyFreeform.

## What is a Connection?

A **Connection** is a visual link between two entities that tracks their positions dynamically. Unlike static lines, connections use the anchor system to maintain their endpoints at specific locations on entities, even as those entities move, rotate, or transform.

![Basic connection between two entities](./_images/02-connections/01-what-is-connection-basic.svg)

Connections consist of three key components:

1. **Start entity** - The entity where the connection begins
2. **End entity** - The entity where the connection terminates
3. **Anchors** - Named points on each entity that define attachment locations

![Connection with labeled components: entities, anchors, and link](./_images/02-connections/02-what-is-connection-labeled.svg)

!!! info "Dynamic Behavior"
    The defining characteristic of connections is their dynamic nature. When either connected entity moves, the connection automatically redraws to maintain the link between the specified anchors.

## Creating Connections

### Basic Connection

The simplest way to create a connection is using the `Connection` constructor with start and end entities:

![Simple connection between two entities](./_images/02-connections/03-creating-connection-simple.svg)

```python
from pyfreeform import Connection

dot1 = cell1.add_dot(at=(20, 50), radius=5, color="red")
dot2 = cell2.add_dot(at=(80, 50), radius=5, color="blue")

# Create connection
connection = Connection(
    start=dot1,
    end=dot2,
    start_anchor="center",
    end_anchor="center"
)

# Add to scene
scene.add(connection)
```

!!! warning "Critical API Signature"
    The `Connection` constructor uses `style={"width": 2, "color": "red"}` as a dict parameter. It does NOT accept direct `width=`, `color=`, `opacity=`, or `z_index=` parameters in the constructor. Use the style dict or set properties after creation.

### Correct API: Using Style Dictionary

The proper way to style a connection at creation time is via the `style` parameter:

```python
from pyfreeform import Connection

dot1 = cell1.add_dot(color="red")
dot2 = cell2.add_dot(color="blue")

# CORRECT: Use style dict
connection = Connection(
    start=dot1,
    end=dot2,
    start_anchor="center",
    end_anchor="center",
    style={
        "width": 2,
        "color": "gray",
        "z_index": 0
    }
)

scene.add(connection)
```

![Creating a styled connection between two dots](./_images/02-connections/04-creating-connection-styled.svg)

### Setting Properties After Creation

You can also set connection properties after instantiation:

```python
connection = Connection(
    start=dot1,
    end=dot2
)

# Set properties directly
connection.width = 3
connection.color = "#ff6b6b"
connection.z_index = 5

scene.add(connection)
```

### Specifying Anchors

Anchors determine where on each entity the connection attaches. Different anchors create different visual effects:

```python
rect1 = cell1.add_rect(at=(20, 20), width=30, height=30)
rect2 = cell2.add_rect(at=(70, 70), width=30, height=30)

# Connect bottom-right of rect1 to top-left of rect2
connection = Connection(
    start=rect1,
    end=rect2,
    start_anchor="bottom_right",
    end_anchor="top_left",
    style={"width": 2, "color": "navy"}
)

scene.add(connection)
```

!!! tip "Default Anchors"
    If you don't specify `start_anchor` or `end_anchor`, both default to `"center"`.

## Auto-Updating Behavior

The power of connections lies in their automatic updates. When entities move, connections maintain their links without any manual intervention.

### How Auto-Updating Works

```python
# Create two dots and connect them
dot1 = cell1.add_dot(at=(20, 50), radius=5, color="red")
dot2 = cell2.add_dot(at=(80, 50), radius=5, color="blue")

connection = Connection(start=dot1, end=dot2)
scene.add(connection)

# Move the entities - connection updates automatically!
dot1.move_to(30, 40)
dot2.move_to(70, 60)
# No need to update the connection manually
```

![Connection automatically updates as entities move](./_images/02-connections/05-auto-updating-positions.svg)

### Frame-by-Frame Updates

Connections recalculate their endpoints every time the scene renders. This means:

- Moving entities during animation automatically updates connections
- Rotating entities updates anchor positions, which updates connections
- Transformations applied to cells propagate to entities and then to connections

![Step-by-step demonstration of auto-updating connections](./_images/02-connections/06-auto-updating-demonstration.svg)

!!! info "Performance Consideration"
    Auto-updating is efficient for typical visualizations. However, with hundreds of connections, rendering may slow down. See the Performance section below for optimization strategies.

### What Triggers Updates

Connections update when:

1. **Entity position changes** - Via `move()`, `move_to()`, or position updates
2. **Entity transformation changes** - Rotation, scaling, or other transforms
3. **Anchor recalculation** - When the entity's anchor positions change
4. **Scene render** - Connections are recomputed during each render cycle

## Connection Styling

Connections support multiple styling options to control their appearance.

### Available Style Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `width` | `float` | Line thickness in pixels | `1.0` |
| `color` | `str` | Line color (hex, rgb, or named) | `"black"` |
| `z_index` | `int` | Rendering layer (higher = on top) | `0` |

!!! note "Style Dictionary Keys"
    When using the `style` parameter in the constructor, use these exact key names: `"width"`, `"color"`, `"z_index"`.

### Color Variations

```python
# Different color formats
connection1 = Connection(start=e1, end=e2, style={"color": "red"})
connection2 = Connection(start=e3, end=e4, style={"color": "#3498db"})
connection3 = Connection(start=e5, end=e6, style={"color": "rgb(255, 99, 71)"})
```

![Different connection colors and styling options](./_images/02-connections/07-styling-colors.svg)

### Width Variations

```python
# Thin connection
thin_conn = Connection(
    start=dot1, end=dot2,
    style={"width": 1, "color": "gray"}
)

# Medium connection
medium_conn = Connection(
    start=dot3, end=dot4,
    style={"width": 3, "color": "blue"}
)

# Thick connection
thick_conn = Connection(
    start=dot5, end=dot6,
    style={"width": 6, "color": "red"}
)
```

![Connection width variations](./_images/02-connections/08-styling-widths.svg)

### Z-Index Layering

Use `z_index` to control rendering order:

```python
# Background connection (drawn first)
background_conn = Connection(
    start=e1, end=e2,
    style={"width": 10, "color": "lightgray", "z_index": 0}
)

# Foreground connection (drawn on top)
foreground_conn = Connection(
    start=e3, end=e4,
    style={"width": 2, "color": "red", "z_index": 10}
)
```

!!! tip "Z-Index Strategy"
    Use low `z_index` values (0-5) for connections to keep them behind entities. Use negative values for background grids or guides.

### Modifying Style After Creation

You can change connection properties at any time:

```python
connection = Connection(start=dot1, end=dot2)
scene.add(connection)

# Later, change the style
connection.width = 4
connection.color = "purple"
connection.z_index = 15
```

## The Pathable Interface

Connections implement the **Pathable** interface, which means they support the `point_at(t)` method. This allows you to position entities at any point along the connection.

### Positioning Along Connections

The `point_at(t)` method takes a parameter `t` between 0.0 and 1.0:

- `t=0.0` returns the start point
- `t=0.5` returns the midpoint
- `t=1.0` returns the end point

```python
connection = Connection(start=dot1, end=dot2)
scene.add(connection)

# Position a dot at the midpoint
midpoint = connection.point_at(0.5)
cell.add_dot(at=midpoint, radius=4, color="orange", z_index=10)

# Position a dot at 25% along the connection
quarter_point = connection.point_at(0.25)
cell.add_dot(at=quarter_point, radius=3, color="green", z_index=10)
```

!!! info "Linear Interpolation"
    Connections use linear interpolation between start and end points. The `point_at()` method returns a point that lies on the straight line between the two anchors.

### Multiple Points Along a Connection

```python
connection = Connection(start=rect1, end=rect2)
scene.add(connection)

# Add markers at regular intervals
for i in range(11):  # 0%, 10%, 20%, ..., 100%
    t = i / 10
    point = connection.point_at(t)
    cell.add_dot(at=point, radius=2, color="blue", z_index=10)
```

### Dynamic Pathable Elements

Since connections update automatically, elements positioned along them also update:

```python
connection = Connection(start=dot1, end=dot2)
scene.add(connection)

# This dot will stay at the midpoint even as dot1 and dot2 move
# (Note: this requires re-querying point_at() each frame)
midpoint = connection.point_at(0.5)
marker = cell.add_dot(at=midpoint, radius=3, color="yellow")
```

!!! warning "Pathable Caching"
    If you cache the result of `point_at()`, it won't update when the connection changes. For dynamic positioning, query `point_at()` each time you need the current position.

## Connection Properties

After creating a connection, you can read and modify several properties:

### Read/Write Properties

```python
connection = Connection(start=e1, end=e2)

# Read properties
print(connection.width)      # Current line width
print(connection.color)      # Current color
print(connection.z_index)    # Current z-index

# Modify properties
connection.width = 5
connection.color = "navy"
connection.z_index = 20
```

### Read-Only Properties

```python
# Get the current start and end points
start_pos = connection.start_point  # Point object
end_pos = connection.end_point      # Point object

print(f"Connection runs from ({start_pos.x}, {start_pos.y}) to ({end_pos.x}, {end_pos.y})")
```

!!! note "Start/End Points vs Entities"
    `start_point` and `end_point` return the current anchor positions (Point objects), not the entities themselves.

## Advanced Patterns

### Pattern: Connect Neighbors

Create a grid of connected entities by linking each to its right neighbor:

```python
from pyfreeform import Connection

for cell in scene.grid:
    dot = cell.add_dot(at=cell.center, radius=4, color="red", z_index=10)

    if cell.right:
        right_dot = cell.right.add_dot(at=cell.right.center, radius=4, color="red", z_index=10)
        connection = Connection(
            start=dot,
            end=right_dot,
            style={"width": 1, "color": "gray", "z_index": 0}
        )
        scene.add(connection)
```

![Grid of dots connected to their right neighbors](./_images/02-connections/10-pattern-connect-neighbors.svg)

### Pattern: Highlight Connections

Connect specific entities based on criteria:

```python
from pyfreeform import Connection

bright_dots = []
for cell in scene.grid.where(lambda c: c.brightness > 0.7):
    dot = cell.add_dot(at=cell.center, radius=5, color="yellow", z_index=10)
    bright_dots.append(dot)

# Connect bright dots sequentially
for i in range(len(bright_dots) - 1):
    connection = Connection(
        start=bright_dots[i],
        end=bright_dots[i+1],
        style={"width": 2, "color": "orange", "z_index": 5}
    )
    scene.add(connection)
```

![Bright dots connected sequentially with highlight connections](./_images/02-connections/11-pattern-highlight-connections.svg)

### Pattern: Radial Connections

Create a hub-and-spoke pattern with connections radiating from a central entity:

```python
import math

# Central entity
center_dot = cell.add_dot(at=(50, 50), radius=6, color="red", z_index=10)

# Outer entities
outer_dots = []
num_spokes = 8
radius = 40

for i in range(num_spokes):
    angle = (2 * math.pi * i) / num_spokes
    x = 50 + radius * math.cos(angle)
    y = 50 + radius * math.sin(angle)

    outer_dot = cell.add_dot(at=(x, y), radius=4, color="blue", z_index=10)
    outer_dots.append(outer_dot)

    # Create connection from center to this outer dot
    connection = Connection(
        start=center_dot,
        end=outer_dot,
        style={"width": 2, "color": "gray", "z_index": 0}
    )
    scene.add(connection)
```

![Radial connections emanating from a central entity](./_images/02-connections/12-pattern-radial-connections.svg)

### Pattern: Sequential Chain

Connect a list of entities in order:

```python
entities = [dot1, dot2, dot3, dot4, dot5]

for i in range(len(entities) - 1):
    connection = Connection(
        start=entities[i],
        end=entities[i + 1],
        style={"width": 2, "color": "navy", "z_index": 0}
    )
    scene.add(connection)
```

![Sequential chain of connected entities](./_images/02-connections/13-pattern-sequential-chain.svg)

### Pattern: Cross Connections

Create a mesh by connecting entities both horizontally and vertically:

```python
# Horizontal connections
for row_idx in range(scene.grid.rows):
    row = scene.grid.row(row_idx)
    for i in range(len(row) - 1):
        dot1 = row[i].add_dot(at=row[i].center, radius=3, color="blue", z_index=10)
        dot2 = row[i+1].add_dot(at=row[i+1].center, radius=3, color="blue", z_index=10)

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"width": 1, "color": "lightgray", "z_index": 0}
        )
        scene.add(connection)

# Vertical connections
for col_idx in range(scene.grid.cols):
    col = scene.grid.column(col_idx)
    for i in range(len(col) - 1):
        dot1 = col[i].add_dot(at=col[i].center, radius=3, color="blue", z_index=10)
        dot2 = col[i+1].add_dot(at=col[i+1].center, radius=3, color="blue", z_index=10)

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"width": 1, "color": "lightgray", "z_index": 0}
        )
        scene.add(connection)
```

![Cross connections between entities in a grid](./_images/02-connections/14-pattern-cross-connections.svg)

### Pattern: Different Anchors

Leverage different anchor points for visual variety:

```python
rect1 = cell1.add_rect(at=(20, 50), width=30, height=30, fill="lightblue")
rect2 = cell2.add_rect(at=(70, 50), width=30, height=30, fill="lightcoral")

# Connect different corners
connection1 = Connection(
    start=rect1,
    end=rect2,
    start_anchor="top_right",
    end_anchor="top_left",
    style={"width": 2, "color": "red", "z_index": 0}
)
scene.add(connection1)

connection2 = Connection(
    start=rect1,
    end=rect2,
    start_anchor="bottom_right",
    end_anchor="bottom_left",
    style={"width": 2, "color": "blue", "z_index": 0}
)
scene.add(connection2)
```

![Connections using different anchor points on entities](./_images/02-connections/15-pattern-different-anchors.svg)

## Network Diagrams

Connections excel at creating network visualizations:

### Simple Network

```python
# Create nodes
nodes = []
for i in range(5):
    angle = (2 * math.pi * i) / 5
    x = 50 + 35 * math.cos(angle)
    y = 50 + 35 * math.sin(angle)

    node = cell.add_dot(at=(x, y), radius=6, color="navy", z_index=10)
    nodes.append(node)

# Connect each node to the next (circular)
for i in range(len(nodes)):
    connection = Connection(
        start=nodes[i],
        end=nodes[(i + 1) % len(nodes)],
        style={"width": 2, "color": "gray", "z_index": 0}
    )
    scene.add(connection)
```

### Weighted Network

Use connection width to represent edge weights:

```python
# edges = [(node_idx1, node_idx2, weight), ...]
edges = [(0, 1, 3), (1, 2, 1), (2, 3, 5), (3, 0, 2)]

for start_idx, end_idx, weight in edges:
    connection = Connection(
        start=nodes[start_idx],
        end=nodes[end_idx],
        style={
            "width": weight,
            "color": "gray",
            "z_index": 0
        }
    )
    scene.add(connection)
```

### Directed Network

For directed edges, you might position arrow markers using the Pathable interface:

```python
connection = Connection(start=node1, end=node2, style={"width": 2, "color": "navy"})
scene.add(connection)

# Position an arrow near the end (90% along the connection)
arrow_pos = connection.point_at(0.9)

# You'd need to calculate angle and create a small polygon for the arrowhead
# (Implementation details depend on your specific requirements)
```

## Performance Considerations

### Connection Count

The number of connections directly impacts rendering performance:

- **0-50 connections**: Negligible performance impact
- **50-200 connections**: Minimal impact, should run smoothly
- **200-500 connections**: Noticeable but acceptable for most use cases
- **500+ connections**: May cause slowdowns, consider optimization strategies

!!! warning "Performance Threshold"
    If you're creating more than 500 connections, consider whether you truly need all of them visible, or if you can use sampling, filtering, or progressive rendering.

### Optimization Strategies

#### 1. Use Z-Index Wisely

Keep connections on a low z-index layer to avoid overdraw:

```python
# Good: connections behind entities
connection = Connection(start=e1, end=e2, style={"z_index": -1})

# Avoid: connections in front of many entities (causes more rendering work)
connection = Connection(start=e1, end=e2, style={"z_index": 100})
```

#### 2. Filter Connections by Visibility

Only create connections for visible or important relationships:

```python
# Only connect if entities are close enough
max_distance = 100

for i, e1 in enumerate(entities):
    for e2 in entities[i+1:]:
        p1 = e1.anchor("center")
        p2 = e2.anchor("center")
        distance = math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

        if distance < max_distance:
            connection = Connection(start=e1, end=e2, style={"width": 1, "color": "gray"})
            scene.add(connection)
```

#### 3. Batch Connection Creation

Create all connections before adding them to the scene:

```python
connections = []

for i in range(len(nodes) - 1):
    conn = Connection(start=nodes[i], end=nodes[i+1])
    connections.append(conn)

# Add all at once
for conn in connections:
    scene.add(conn)
```

#### 4. Consider Alternatives for Dense Networks

For very dense networks, consider:

- Drawing only a sample of connections
- Using color or opacity to de-emphasize less important connections
- Creating a static background layer for some connections
- Using visual aggregation instead of individual connections

## Troubleshooting

### Connection Not Appearing

If a connection doesn't render:

1. **Check you added it to the scene**: `scene.add(connection)`
2. **Verify entities exist**: Both start and end entities must be valid
3. **Check z-index**: Connection might be behind other elements
4. **Inspect color**: Connection color might match the background

```python
# Debug: print connection properties
print(f"Start: {connection.start_point}")
print(f"End: {connection.end_point}")
print(f"Width: {connection.width}")
print(f"Color: {connection.color}")
print(f"Z-index: {connection.z_index}")
```

### Connection Not Updating

If a connection doesn't follow entity movement:

1. **Ensure entities are properly added to cells**: Entities must be part of the scene hierarchy
2. **Check if entity positions are actually changing**: Print positions before/after movement
3. **Verify anchors are valid**: Invalid anchors might cause silent failures

### Invalid Anchor Error

```python
connection = Connection(
    start=dot,
    end=rect,
    start_anchor="top_left",  # Error: dots don't have "top_left"
    end_anchor="center"
)
```

**Solution:** Use `entity.anchor_names` to verify available anchors:

```python
print(dot.anchor_names)   # ['center']
print(rect.anchor_names)  # ['center', 'top_left', 'top_right', ...]

# Correct version
connection = Connection(
    start=dot,
    end=rect,
    start_anchor="center",
    end_anchor="top_left"
)
```

### Style Not Applied

If you use direct parameters instead of the style dict, they'll be ignored:

```python
# WRONG: These parameters don't exist
connection = Connection(
    start=e1,
    end=e2,
    width=3,        # Ignored!
    color="red"     # Ignored!
)

# CORRECT: Use style dict
connection = Connection(
    start=e1,
    end=e2,
    style={"width": 3, "color": "red"}
)

# Or set properties after creation
connection = Connection(start=e1, end=e2)
connection.width = 3
connection.color = "red"
```

## API Reference

### Connection Constructor

```python
Connection(
    start: Entity,
    end: Entity,
    start_anchor: str = "center",
    end_anchor: str = "center",
    style: dict[str, Any] | None = None
)
```

**Parameters:**

- `start` (Entity): The starting entity
- `end` (Entity): The ending entity
- `start_anchor` (str, optional): Anchor name on start entity (default: "center")
- `end_anchor` (str, optional): Anchor name on end entity (default: "center")
- `style` (dict, optional): Style dictionary with keys: `"width"`, `"color"`, `"z_index"`

**Style Dictionary Keys:**

| Key | Type | Description | Default |
|-----|------|-------------|---------|
| `"width"` | `float` | Line width in pixels | `1.0` |
| `"color"` | `str` | Line color | `"black"` |
| `"z_index"` | `int` | Rendering layer | `0` |

**Returns:** Connection object

**Example:**
```python
connection = Connection(
    start=dot1,
    end=dot2,
    start_anchor="center",
    end_anchor="center",
    style={"width": 2, "color": "#3498db", "z_index": 5}
)
scene.add(connection)
```

### Connection.width

Read/write property for line width.

```python
connection.width = 5
print(connection.width)  # 5
```

### Connection.color

Read/write property for line color.

```python
connection.color = "red"
print(connection.color)  # "red"
```

### Connection.z_index

Read/write property for rendering layer.

```python
connection.z_index = 10
print(connection.z_index)  # 10
```

### Connection.start_point

Read-only property returning the current start anchor position as a Point.

```python
start = connection.start_point
print(f"Start: ({start.x}, {start.y})")
```

### Connection.end_point

Read-only property returning the current end anchor position as a Point.

```python
end = connection.end_point
print(f"End: ({end.x}, {end.y})")
```

### Connection.point_at(t: float) -> Point

Returns a point at position `t` along the connection (Pathable interface).

**Parameters:**

- `t` (float): Position from 0.0 (start) to 1.0 (end)

**Returns:** Point object at the specified position

**Example:**
```python
midpoint = connection.point_at(0.5)
quarter = connection.point_at(0.25)
```

## See Also
- [Anchor System](01-anchor-system.md) - Named reference points on entities
- [Entities](../fundamentals/03-entities.md) - All entity types that can be connected
- [Pathable Interface](../api-reference/pathable.md) - Positioning along paths and connections
- [Examples](../examples/intermediate/connections.md) - More connection examples
