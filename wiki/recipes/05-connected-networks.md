
# Recipe: Connected Networks

Create dynamic network visualizations by connecting dots and shapes with lines, showing relationships and flow.

---

## Visual Result

![Network visualization with connected nodes and lines](./_images/05-connected-networks/01_basic_network.svg)

Networks show connections and relationships between elements.

---

## Why This Works

Network visualizations tap into our intuition about relationships and connections. By representing data points as nodes (dots) and their relationships as edges (lines), you create compositions that suggest meaning beyond decoration. The human eye naturally follows lines between points, creating implicit flow and narrative.

The visual impact comes from:

- **Implied relationships**: Lines suggest connections, even when abstract
- **Visual flow**: Eyes follow connection paths across the composition
- **Density variation**: Sparse and dense regions create rhythm and focus
- **Layering depth**: Nodes in front, connections behind creates spatial hierarchy

!!! tip "When to Use This Technique"
    Choose connected networks when you want:

    - Work that suggests data, science, or technology themes
    - Complex compositions that reward close examination
    - Visual metaphors for communication, community, or systems
    - Dynamic layouts where every element relates to others
    - High contrast between foreground nodes and background structure

---

## The Pattern

**Key Idea**: Connect cells to their neighbors using dynamic connections that update automatically.

```python
from pyfreeform import Connection

for cell in scene.grid:
    # Add dot
    dot = cell.add_dot(radius=3, color=cell.color)

    # Connect to right neighbor
    if cell.right:
        right_dot = cell.right.add_dot(radius=3, color=cell.right.color)

        # Create connection that updates automatically
        connection = Connection(
            start=dot,
            end=right_dot,
            style={"color": "gray", "width": 1}
        )
        scene.add(connection)
```

---

## Complete Example

```python
from pyfreeform import Scene, Palette, Connection

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()
scene.background = colors.background

# Create nodes (dots)
dots = {}
for cell in scene.grid:
    if cell.brightness > 0.4:  # Only bright cells
        dot = cell.add_dot(
            radius=2 + cell.brightness * 3,  # Size varies
            color=colors.primary,
            z_index=10
        )
        dots[(cell.row, cell.col)] = dot

# Create connections between neighbors
for cell in scene.grid:
    if (cell.row, cell.col) not in dots:
        continue

    dot1 = dots[(cell.row, cell.col)]

    # Connect to right neighbor
    if cell.right and (cell.right.row, cell.right.col) in dots:
        dot2 = dots[(cell.right.row, cell.right.col)]

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 0.5, "z_index": 0}
        )
        scene.add(connection)

    # Connect to bottom neighbor
    if cell.bottom and (cell.bottom.row, cell.bottom.col) in dots:
        dot2 = dots[(cell.bottom.row, cell.bottom.col)]

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 0.5, "z_index": 0}
        )
        scene.add(connection)

scene.save("connected_network.svg")
```

---

## Connection Variations

### Distance-Based Connections

Connect only nearby dots:

```python
import math

# Create all dots
dots = []
for cell in scene.grid:
    if cell.brightness > 0.5:
        dot = cell.add_dot(radius=3, color=colors.primary)
        dots.append((dot, cell))

# Connect dots within distance threshold
max_distance = 3  # cells

for i, (dot1, cell1) in enumerate(dots):
    for dot2, cell2 in dots[i+1:]:
        # Calculate distance
        dr = cell1.row - cell2.row
        dc = cell1.col - cell2.col
        distance = math.sqrt(dr*dr + dc*dc)

        if distance <= max_distance:
            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 1}
            )
            scene.add(connection)
```

![Network with connections that fade based on distance](./_images/05-connected-networks/02_distance_based.svg)

### Radial Connections

Connect all dots to a central hub:

```python
# Find center cell
center = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]
hub_dot = center.add_dot(radius=5, color=colors.accent)

# Connect all other bright cells to hub
for cell in scene.grid:
    if cell == center:
        continue

    if cell.brightness > 0.6:
        outer_dot = cell.add_dot(radius=2, color=colors.primary)

        connection = Connection(
            start=hub_dot,
            end=outer_dot,
            style={"color": colors.line, "width": 0.5}
        )
        scene.add(connection)
```

![All dots connect to a central hub node](./_images/05-connected-networks/03_radial_hub.svg)

### Conditional Connections

Connect based on brightness similarity:

```python
for cell in scene.grid:
    if cell.brightness < 0.4:
        continue

    dot1 = cell.add_dot(radius=3, color=cell.color)

    # Connect to right neighbor if similar brightness
    if cell.right and abs(cell.brightness - cell.right.brightness) < 0.2:
        dot2 = cell.right.add_dot(radius=3, color=cell.right.color)

        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 1}
        )
        scene.add(connection)
```

![Connections between dots with similar brightness](./_images/05-connected-networks/06_similarity_based.svg)

---

## Advanced Techniques

### Weighted Connections

Vary line width based on relationship strength:

```python
# Width based on average brightness
avg_brightness = (cell.brightness + cell.right.brightness) / 2
width = 0.5 + avg_brightness * 2  # 0.5 to 2.5

connection = Connection(
    start=dot1,
    end=dot2,
    style={"width": width, "color": colors.line}
)
```

![Weighted connections with varying line width](./_images/05-connected-networks/04_weighted_connections.svg)

### Curved Connections

Use curves instead of straight lines:

```python
# Add curve between dots
curve = cell.add_curve(
    start=dot1.position,
    end=dot2.position,
    curvature=0.3,
    color=colors.line,
    width=1
)
```

### Multi-Layer Networks

Create different connection types on different layers:

```python
# Strong connections (high brightness)
if cell.brightness > 0.7 and cell.right and cell.right.brightness > 0.7:
    Connection(
        start=dot1,
        end=dot2,
        style={"color": colors.accent, "width": 2, "z_index": 5}
    )

# Weak connections (medium brightness)
elif cell.brightness > 0.4:
    Connection(
        start=dot1,
        end=dot2,
        style={"color": colors.line, "width": 0.5, "z_index": 0}
    )
```

![Multiple connection layers with strong and weak links](./_images/05-connected-networks/07_multi_layer.svg)

---

## Tips

### Layer Connections Below Nodes

Always put connections on a lower z-index:

```python
# Connections first (background)
connection = Connection(start=dot1, end=dot2, style={"z_index": 0})

# Dots second (foreground)
dot = cell.add_dot(..., z_index=10)
```

### Vary Width for Depth

```python
# Closer connections = thicker
width = 1.0 - (distance / max_distance) * 0.5  # 0.5 to 1.0

connection = Connection(
    start=dot1,
    end=dot2,
    style={"width": width, "color": colors.line}
)
```

### Threshold for Clarity

Don't connect everything - use thresholds:

```python
# Only connect bright areas
if cell.brightness > 0.5 and neighbor.brightness > 0.5:
    # Create connection
```

### Diagonal Connections

```python
# Connect to all 8 neighbors
neighbors = [
    cell.right, cell.left,
    cell.top, cell.bottom,
    cell.top_left, cell.top_right,
    cell.bottom_left, cell.bottom_right
]

for neighbor in neighbors:
    if neighbor and should_connect(cell, neighbor):
        # Create connection
```

![Diagonal connections linking nodes across the grid](./_images/05-connected-networks/05_diagonal_connections.svg)

![Sparse network with fewer connections between bright nodes](./_images/05-connected-networks/08_sparse_network.svg)

---

## Parameter Tuning Guide

### Choosing Connection Thresholds

The threshold determines which cells get connected. Too low creates a sparse network; too high creates an overwhelming web.

```python
# Very sparse (only brightest cells)
if cell.brightness > 0.8:
    dot = cell.add_dot(radius=3, color=colors.primary)

# Medium density (balanced)
if cell.brightness > 0.5:
    dot = cell.add_dot(radius=3, color=colors.primary)

# Dense network (most cells)
if cell.brightness > 0.3:
    dot = cell.add_dot(radius=3, color=colors.primary)
```

!!! tip "Finding the Right Density"
    Start with `brightness > 0.5` for a balanced network. Preview the result, then adjust:

    - If too cluttered: increase threshold (0.6, 0.7)
    - If too sparse: decrease threshold (0.4, 0.3)
    - For high-contrast images: use lower thresholds
    - For low-contrast images: use higher thresholds

### Distance-Based Connection Radius

Control how far apart nodes can be while still connecting:

```python
# Close connections only (tight clusters)
max_distance = 2  # cells

# Medium range (balanced)
max_distance = 4  # cells

# Long-range connections (web-like)
max_distance = 8  # cells
```

!!! info "Distance vs Grid Size"
    Scale your max_distance with your grid size:

    - 10x10 grid: use max_distance = 2-3
    - 20x20 grid: use max_distance = 3-5
    - 40x40 grid: use max_distance = 5-8

### Line Width Strategies

```python
# Constant width (uniform appearance)
style = {"width": 1, "color": colors.line}

# Distance-based width (creates depth)
width = 2.0 - (distance / max_distance)  # Thicker when closer
style = {"width": width, "color": colors.line}

# Brightness-based width (highlights important nodes)
avg_brightness = (cell1.brightness + cell2.brightness) / 2
width = 0.5 + avg_brightness * 1.5  # 0.5 to 2.0
style = {"width": width, "color": colors.line}
```

### Node Size Variation

Make important nodes larger:

```python
# Uniform size (egalitarian)
dot = cell.add_dot(radius=3, color=colors.primary)

# Brightness-based size (emphasizes bright areas)
radius = 2 + cell.brightness * 4  # 2 to 6
dot = cell.add_dot(radius=radius, color=colors.primary)

# Connection count-based size (hub detection)
# (Requires tracking connections per node)
```

---

## Common Pitfalls

### Pitfall 1: Wrong Connection Style Syntax

```python
# ❌ WRONG - Connection doesn't take direct parameters
connection = Connection(
    start=dot1,
    end=dot2,
    width=2,          # Not valid!
    color="red"       # Not valid!
)

# ✅ CORRECT - Use style dict
connection = Connection(
    start=dot1,
    end=dot2,
    style={"width": 2, "color": "red"}
)
```

!!! warning "Style Must Be a Dictionary"
    Unlike most PyFreeform entities, `Connection` requires a `style` dictionary. Direct parameters like `width=` or `color=` will be silently ignored or cause errors.

### Pitfall 2: Creating Duplicate Connections

```python
# ❌ WRONG - Creates connection twice (A→B and B→A)
for cell in scene.grid:
    for other_cell in scene.grid:
        if should_connect(cell, other_cell):
            # Creates duplicate when cell and other_cell swap
            Connection(start=cell_dot, end=other_dot, ...)

# ✅ CORRECT - Only connect once
for i, cell in enumerate(scene.grid):
    for other_cell in list(scene.grid)[i+1:]:  # Only cells after current
        if should_connect(cell, other_cell):
            Connection(start=cell_dot, end=other_dot, ...)
```

### Pitfall 3: Not Using Z-Index for Layering

```python
# ❌ WRONG - Connections may appear on top of dots
dot = cell.add_dot(radius=3, color=colors.primary)
connection = Connection(start=dot1, end=dot2, style={"color": "red"})

# ✅ CORRECT - Connections behind, dots in front
connection = Connection(
    start=dot1,
    end=dot2,
    style={"color": "red", "z_index": 0}  # Background
)
dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)  # Foreground
```

### Pitfall 4: Forgetting to Store Dot References

```python
# ❌ WRONG - Can't connect dots we don't have references to
for cell in scene.grid:
    cell.add_dot(radius=3, color=colors.primary)
    # How do we connect these later?

# ✅ CORRECT - Store dots in a dictionary
dots = {}
for cell in scene.grid:
    if cell.brightness > 0.5:
        dot = cell.add_dot(radius=3, color=colors.primary)
        dots[(cell.row, cell.col)] = dot

# Now we can connect them
for (row, col), dot1 in dots.items():
    # ... find neighbors and connect
```

### Pitfall 5: Using `cell.below` Instead of `cell.bottom`

```python
# ❌ WRONG - No such attribute
if cell.below:
    # This will cause AttributeError

# ✅ CORRECT - Use cell.bottom
if cell.bottom:
    dot2 = dots.get((cell.bottom.row, cell.bottom.col))
    if dot2:
        Connection(start=dot1, end=dot2, ...)
```

!!! warning "Neighbor Attribute Names"
    Cell neighbors are: `cell.left`, `cell.right`, `cell.above`, `cell.bottom` (NOT `cell.top` or `cell.below`).

---

## Best Practices

### 1. Always Layer Connections Below Nodes

```python
# Create all connections first (z_index: 0)
for cell in scene.grid:
    if cell.right and should_connect(cell, cell.right):
        Connection(
            start=dots[cell],
            end=dots[cell.right],
            style={"color": colors.line, "width": 1, "z_index": 0}
        )

# Then create nodes on top (z_index: 10)
for cell in scene.grid:
    dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
```

### 2. Use Dictionaries to Track Nodes

```python
# Index by position for easy neighbor lookup
dots = {}

for cell in scene.grid:
    if should_create_node(cell):
        dot = cell.add_dot(radius=3, color=colors.primary)
        dots[(cell.row, cell.col)] = dot

# Easy neighbor access
for (row, col), dot in dots.items():
    # Check right neighbor
    right_key = (row, col + 1)
    if right_key in dots:
        Connection(start=dot, end=dots[right_key], ...)
```

### 3. Start with Grid Neighbors, Then Add Distance

```python
# Phase 1: Create basic grid connections (simple)
for cell in scene.grid:
    if cell.right:
        # Connect to right
    if cell.bottom:
        # Connect to bottom

# Phase 2: Add distance-based connections (complex)
for i, (dot1, cell1) in enumerate(dots):
    for dot2, cell2 in dots[i+1:]:
        distance = calculate_distance(cell1, cell2)
        if distance <= max_distance:
            # Create connection
```

### 4. Use Opacity for Visual Depth

```python
# Fade distant connections
opacity = 1.0 - (distance / max_distance) * 0.7  # 0.3 to 1.0

connection = Connection(
    start=dot1,
    end=dot2,
    style={"color": colors.line, "width": 1, "opacity": opacity}
)
```

!!! tip "Subtle Opacity Works Best"
    Don't fade connections below 0.3 opacity - they become invisible and add no value. Keep minimum opacity around 0.3-0.4 for best results.

---

## Advanced Techniques

### Hub Detection

Create visual emphasis on highly connected nodes:

```python
# Count connections per node
connection_count = {}
for (row, col), dot in dots.items():
    connection_count[(row, col)] = 0

# Track connections
for cell in scene.grid:
    if cell.right and both_in_dots:
        connection_count[(cell.row, cell.col)] += 1
        connection_count[(cell.right.row, cell.right.col)] += 1

# Make hubs larger and different color
for (row, col), dot in dots.items():
    count = connection_count[(row, col)]
    if count >= 4:  # Hub threshold
        # Redraw as larger, accented dot
        cell = scene.grid[row, col]
        cell.add_dot(radius=5, color=colors.accent, z_index=15)
```

### Conditional Connection Styling

Different connection types for different relationships:

```python
# Strong connection (similar brightness)
if abs(cell1.brightness - cell2.brightness) < 0.2:
    style = {"width": 2, "color": colors.accent, "z_index": 5}

# Weak connection (different brightness)
else:
    style = {"width": 0.5, "color": colors.line, "z_index": 0}

Connection(start=dot1, end=dot2, style=style)
```

### Triangle Clusters

Connect sets of three nearby nodes to create mesh patterns:

```python
# Find all triangles (sets of 3 mutually connected nodes)
for (r1, c1), dot1 in dots.items():
    for (r2, c2), dot2 in dots.items():
        for (r3, c3), dot3 in dots.items():
            if all_within_distance([dot1, dot2, dot3], max_distance=3):
                # Create triangle
                Connection(start=dot1, end=dot2, ...)
                Connection(start=dot2, end=dot3, ...)
                Connection(start=dot3, end=dot1, ...)
```

### Direction-Based Coloring

```python
import math

# Calculate angle between nodes
dr = cell2.row - cell1.row
dc = cell2.col - cell1.col
angle = math.degrees(math.atan2(dr, dc))

# Color based on direction
if -45 <= angle < 45:  # Rightward
    color = colors.primary
elif 45 <= angle < 135:  # Downward
    color = colors.secondary
else:  # Leftward or upward
    color = colors.accent

Connection(start=dot1, end=dot2, style={"color": color, "width": 1})
```

---

## Performance Optimization

### Limit Connection Checks

Distance-based connections require checking every pair of nodes (O(n²)). For large grids, this becomes slow.

```python
# ❌ SLOW - Checks all pairs
for dot1 in dots:
    for dot2 in dots:
        if distance(dot1, dot2) <= max_distance:
            Connection(...)

# ✅ FASTER - Use spatial bucketing
from collections import defaultdict

# Group nodes by region
regions = defaultdict(list)
region_size = 5  # cells

for (row, col), dot in dots.items():
    region_key = (row // region_size, col // region_size)
    regions[region_key].append((row, col, dot))

# Only check within and adjacent regions
for region_key, nodes in regions.items():
    adjacent_regions = get_adjacent_regions(region_key)
    for other_region_key in adjacent_regions:
        # Check connections only between nearby nodes
```

!!! info "When to Optimize"
    For grids under 30x30 with moderate connection thresholds, basic O(n²) checking is fine. Optimize only if rendering takes more than a few seconds.

---

## See Also

- 📖 [Connections](../advanced-concepts/02-connections.md) - Dynamic entity links
- 📖 [Dots](../entities/01-dots.md) - Creating nodes
- 📖 [Lines](../entities/02-lines.md) - Straight connections
- 📖 [Curves](../entities/03-curves.md) - Curved connections
- 🎯 [Connections Example](../examples/intermediate/connections.md) - Detailed breakdown

