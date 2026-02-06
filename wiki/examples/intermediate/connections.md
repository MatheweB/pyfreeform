
# Example: Connections

**Difficulty**: ⭐ Intermediate

Create network visualizations by connecting dots with dynamic Connection entities.

---

## What You'll Learn

- Creating Connection entities between dots
- Distance-based connection filtering
- Opacity fading with distance
- Layering connections below nodes

---

## Final Result

![Network](../_images/connections/01_network.svg)

### More Examples

| Network | Distance Fade | Hub and Spoke |
|---------|---------------|---------------|
| ![Example 1](../_images/connections/01_network.svg) | ![Example 2](../_images/connections/02_distance_fade.svg) | ![Example 3](../_images/connections/03_hub_spoke.svg) |

---

## Step-by-Step Breakdown

### Step 1: Setup and Create Nodes

```python
from pyfreeform import Scene, Palette, Connection
import math

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()
scene.background = colors.background

# Create dots (nodes) and store them
dots = []
for cell in scene.grid:
    if cell.brightness > 0.4:  # Only bright cells
        dot = cell.add_dot(
            radius=2 + cell.brightness * 3,  # Size varies: 2-5px
            color=colors.primary,
            z_index=10  # On top
        )
        # Store dot with its cell for distance calculation
        dots.append((dot, cell))
```

**What's happening:**
- Filter cells by brightness threshold (> 0.4)
- Create dots with size based on brightness
- `z_index=10` ensures dots appear on top of connections
- Store `(dot, cell)` tuples for later distance calculations

### Step 2: Connect Nearby Dots

```python
max_distance = 3  # Maximum distance in cells

for i, (dot1, cell1) in enumerate(dots):
    for dot2, cell2 in dots[i+1:]:  # Only check each pair once
        # Calculate distance between cells
        dr = cell1.row - cell2.row
        dc = cell1.col - cell2.col
        distance = math.sqrt(dr*dr + dc*dc)

        if distance <= max_distance:
            # Create connection
            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5}
            )
            scene.add(connection)
```

**What's happening:**
- `enumerate(dots)` gives us index `i`
- `dots[i+1:]` skips already-checked pairs (avoid duplicates)
- Calculate Euclidean distance: `√(Δrow² + Δcol²)`
- Only connect if distance ≤ 3 cells
- Connection style uses a dict with `"color"` and `"width"` keys

**The Mathematics:**
```
distance = √((row₁ - row₂)² + (col₁ - col₂)²)

Example:
Cell A: (5, 10)
Cell B: (7, 12)

Δrow = 5 - 7 = -2
Δcol = 10 - 12 = -2
distance = √((-2)² + (-2)²) = √8 ≈ 2.83 cells
```

### Step 3: Add Distance-Based Opacity

```python
        if distance <= max_distance:
            # Fade opacity with distance
            opacity = 1 - (distance / max_distance)

            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5}
            )
            scene.add(connection)
```

**What's happening:**
- `opacity = 1 - (distance / max_distance)` creates linear fade
- Close dots (distance=0): opacity = 1.0 (fully opaque)
- Far dots (distance=3): opacity = 0.0 (fully transparent)
- Creates depth perception

**Opacity Formula:**
```
opacity = 1 - (d / d_max)

Examples with max_distance=3:
d=0.5: opacity = 1 - 0.5/3 = 0.83
d=1.5: opacity = 1 - 1.5/3 = 0.50
d=2.5: opacity = 1 - 2.5/3 = 0.17
d=3.0: opacity = 1 - 3.0/3 = 0.00
```

---

## Complete Code

```python
from pyfreeform import Scene, Palette, Connection
import math

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()
scene.background = colors.background

# Create all dots
dots = []
for cell in scene.grid:
    if cell.brightness > 0.4:
        dot = cell.add_dot(
            radius=2 + cell.brightness * 3,
            color=colors.primary,
            z_index=10
        )
        dots.append((dot, cell))

# Connect nearby dots
max_distance = 3

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
                style={"color": colors.line, "width": 0.5}
            )
            scene.add(connection)

scene.save("network.svg")
```

---

## Try It Yourself

### Experiment 1: Vary Connection Distance

```python
# Tighter network
max_distance = 2

# Sparser network
max_distance = 5

# Very dense
max_distance = 10
```

### Experiment 2: Width Based on Distance

```python
if distance <= max_distance:
    # Closer = thicker lines
    width = (1 - distance / max_distance) * 2  # 0 to 2
    opacity = 1 - (distance / max_distance)

    connection = Connection(
        start=dot1,
        end=dot2,
        style={"width": width}
    )
```

### Experiment 3: Hub-and-Spoke Pattern

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
            style={"color": colors.line, "width": 1}
        )
        scene.add(connection)
```

### Challenge: Grid Network

Create a structured grid network:

```python
for cell in scene.grid:
    dot1 = cell.add_dot(radius=2, z_index=10)

    # Connect to right neighbor
    if cell.right:
        dot2 = cell.right.add_dot(radius=2, z_index=10)
        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 0.5}
        )
        scene.add(connection)

    # Connect to below neighbor
    if cell.below:
        dot2 = cell.below.add_dot(radius=2, z_index=10)
        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 0.5}
        )
        scene.add(connection)
```

---

## Related

- 📖 [Connections API](../../api-reference/connections.md) - Full API reference
- 📖 [Connections Guide](../../advanced-concepts/02-connections.md) - Detailed usage
- 🎯 [Connected Networks Recipe](../../recipes/05-connected-networks.md) - More patterns
- 📖 [Layering Guide](../../fundamentals/05-layering.md) - Z-index system

