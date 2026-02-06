
# Connections API Reference

The `Connection` class creates dynamic lines between entities that automatically update when entities move.

---

## Overview

Connections provide automatic linking between entities:
- **Dynamic updates**: Line automatically follows entities
- **Visual relationships**: Show connections in network diagrams
- **Layer control**: Place connections behind or in front of entities

![Basic Connections](./_images/connections/example1-basic.svg)

![Multiple Connections](./_images/connections/example2-multiple.svg)

---

## Class Definition

```python
class Connection(Entity):
    def __init__(
        self,
        start: Entity,
        end: Entity,
        start_anchor: str = "center",
        end_anchor: str = "center",
        style: dict[str, Any] | None = None
    )
```

**Parameters**:
- `start`: First entity to connect
- `end`: Second entity to connect
- `start_anchor`: Anchor point name on start entity
- `end_anchor`: Anchor point name on end entity
- `style`: `ConnectionStyle`, or dict with keys `"width"`, `"color"`, `"z_index"`

---

## Properties

```python
connection.start: Entity         # First connected entity
connection.end: Entity           # Second connected entity
connection.start_anchor: str     # Anchor name on start entity
connection.end_anchor: str       # Anchor name on end entity
connection.color: str            # Line color (set via style or property)
connection.width: float          # Line width (set via style or property)
connection.z_index: int          # Layer order (set via style or property)
```

**Dynamic Properties** (recalculated on access):
```python
connection.start_point: Point    # Current position of start_anchor
connection.end_point: Point      # Current position of end_anchor
```

---

## Basic Usage

### Connect Two Dots

```python
# Create two dots
dot1 = cell.add_dot(at="left", radius=5, color="red")
dot2 = cell.add_dot(at="right", radius=5, color="blue")

# Connect them
connection = Connection(
    start=dot1,
    end=dot2,
    style={"color": "gray", "width": 1, "z_index": 0}  # Behind the dots
)
scene.add(connection)
```

![Connection Properties](./_images/connections/example5-properties.svg)

### Connect to Neighbors

```python
for cell in scene.grid:
    dot1 = cell.add_dot(radius=3, color=cell.color, z_index=10)

    # Connect to right neighbor
    if cell.right:
        dot2 = cell.right.add_dot(radius=3, color=cell.right.color, z_index=10)

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": "gray", "width": 0.5, "z_index": 0}  # Connections in background
        )
        scene.add(connection)
```

![Grid Neighbor Connections](./_images/connections/example4-grid-neighbors.svg)

---

## Using Anchors

Different anchor points create different connection styles:

```python
# Create rectangle (fills entire cell)
rect = cell.add_fill(color="blue")

# Dot at different anchor points
dot_top = Dot(x=100, y=100, radius=3)
dot_right = Dot(x=150, y=100, radius=3)

# Connect from specific anchors
Connection(
    start=rect,
    end=dot_top,
    start_anchor="top",      # Top edge of rectangle
    end_anchor="center",     # Center of dot
    style={"color": "yellow", "width": 2}
)

Connection(
    start=rect,
    end=dot_right,
    start_anchor="right",    # Right edge of rectangle
    end_anchor="center",
    style={"color": "green", "width": 2}
)
```

![Anchor Connections](./_images/connections/example3-anchors.svg)

---

## Common Patterns

![Connection Colors](./_images/connections/example9-colors.svg)

### Network Graph

```python
import math

# Create all nodes
dots = []
for cell in scene.grid:
    if cell.brightness > 0.5:
        dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
        dots.append((dot, cell))

# Connect nearby dots
max_distance = 3  # cells

for i, (dot1, cell1) in enumerate(dots):
    for dot2, cell2 in dots[i+1:]:
        # Calculate distance
        dr = cell1.row - cell2.row
        dc = cell1.col - cell2.col
        distance = math.sqrt(dr*dr + dc*dc)

        if distance <= max_distance:
            # Fade with distance
            opacity = 1 - (distance / max_distance)

            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5, "z_index": 0}
            )
            scene.add(connection)
```

![Network Graph](./_images/connections/example6-network.svg)

### Hub-and-Spoke

```python
# Central hub
center = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]
hub = center.add_dot(radius=8, color=colors.accent, z_index=20)

# Spokes to bright cells
for cell in scene.grid:
    if cell == center:
        continue

    if cell.brightness > 0.7:
        spoke = cell.add_dot(radius=3, color=colors.primary, z_index=10)

        connection = Connection(
            start=hub,
            end=spoke,
            style={"color": colors.line, "width": 1, "z_index": 0}
        )
        scene.add(connection)
```

![Hub-and-Spoke Pattern](./_images/connections/example7-hub-spoke.svg)

![Connection Layering](./_images/connections/example8-layering.svg)

![Complete Connections Example](./_images/connections/example10-complete.svg)

---

## Using ConnectionStyle

Instead of raw dicts, use the typed `ConnectionStyle` class:

```python
from pyfreeform.config import ConnectionStyle

# Define a reusable style
style = ConnectionStyle(width=2, color="gray", z_index=0)

# Use with Connection
connection = Connection(dot1, dot2, style=style)

# Or with entity.connect()
connection = dot1.connect(dot2, style=style)

# Builder methods for variations
thick = style.with_width(4)
red = style.with_color("red")
```

> **Backward compatible:** Plain dicts like `{"width": 2, "color": "gray"}` still work.

---

## See Also

- 📖 [Connections Guide](../advanced-concepts/02-connections.md) - Detailed usage guide
- 📖 [Style Objects](../color-and-style/03-style-objects.md) - All style classes
- 📖 [Entities API](entities.md) - All entity types
- 📖 [Layering Guide](../fundamentals/05-layering.md) - Z-index system
- 🎯 [Connected Networks Recipe](../recipes/05-connected-networks.md) - Network patterns
- 🎯 [Connections Example](../examples/intermediate/connections.md) - Step-by-step tutorial

