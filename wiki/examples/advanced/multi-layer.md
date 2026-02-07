
# Example: Multi-Layer Composition

**Difficulty**: ⭐⭐⭐ Advanced

Master complex compositions by layering multiple visual elements with precise z-index control.

---

## What You'll Learn

- Multi-layer composition techniques
- Strategic z-index management
- Combining multiple entity types
- Background, middleground, and foreground patterns
- Creating depth with layering

---

## Final Result

![Layered Composition](../_images/multi-layer/01_layered_composition.svg)

### More Examples

| Layered Composition | Depth Effect | Complex Layering |
|---------------------|--------------|------------------|
| ![Example 1](../_images/multi-layer/01_layered_composition.svg) | ![Example 2](../_images/multi-layer/02_depth_effect.svg) | ![Example 3](../_images/multi-layer/03_complex_layering.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, Connection, Text
import math

scene = Scene.from_image("photo.jpg", grid_size=25)
colors = Palette.midnight()
scene.background = colors.background

# Layer 1: Grid structure (z_index=0)
for cell in scene.grid:
    cell.add_border(color=colors.grid, width=0.5, z_index=0)

# Layer 2: Background fills based on brightness (z_index=1-3)
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_fill(style=FillStyle(color=colors.primary, opacity=0.1), z_index=1)
    elif cell.brightness > 0.4:
        cell.add_fill(style=FillStyle(color=colors.secondary, opacity=0.1), z_index=2)

# Layer 3: Large background ellipses (z_index=5)
for cell in scene.grid.where(lambda c: c.brightness > 0.6 and (c.row + c.col) % 5 == 0):
    ellipse = cell.add_ellipse(
        rx=cell.width * 1.5,
        ry=cell.height * 1.5,
        fill=colors.primary,
        z_index=5
    )

# Layer 4: Network connections (z_index=10)
# Store dots for connections
network_dots = []
for cell in scene.grid.where(lambda c: c.brightness > 0.5):
    dot = cell.add_dot(
        radius=3 + cell.brightness * 5,
        color=colors.primary,
        z_index=20  # Above connections
    )
    network_dots.append((dot, cell))

# Create connections between nearby dots
for i, (dot1, cell1) in enumerate(network_dots):
    for dot2, cell2 in network_dots[i+1:i+4]:  # Connect to next 3
        dr = cell1.row - cell2.row
        dc = cell1.col - cell2.col
        distance = math.sqrt(dr*dr + dc*dc)

        if distance < 4:
            opacity = 1 - (distance / 4)
            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5, "z_index": 10}  # Behind dots
            )
            scene.add(connection)

# Layer 5: Highlight rings on bright nodes (z_index=25)
for dot, cell in network_dots:
    if cell.brightness > 0.8:
        highlight = cell.add_ellipse(
            rx=dot.radius + 3,
            ry=dot.radius + 3,
            fill=None,
            stroke=colors.accent,
            stroke_width=1.5,
            z_index=25  # Above main dots
        )

# Layer 6: Small accent dots on nodes (z_index=30)
for dot, cell in network_dots:
    if cell.brightness > 0.7:
        accent = cell.add_dot(
            radius=dot.radius * 0.3,
            color=colors.background,
            z_index=30  # On top of main dots
        )

# Layer 7: Text labels (z_index=50)
# Only label very bright nodes
label_count = 0
for dot, cell in network_dots:
    if cell.brightness > 0.85 and label_count < 5:
        label = Text(
            x=cell.center.x,
            y=cell.center.y - dot.radius - 8,
            content=f"N{label_count+1}",
            font_size=9,
            color=colors.line,
            font_family="monospace",
            text_anchor="middle",
            z_index=50  # Always on top
        )
        scene.add(label)
        label_count += 1

scene.save("multi_layer.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Plan Your Layers

**Z-Index Strategy:**
```
z =  0: Grid structure (subtle background)
z =  1-3: Fill layers (varying opacity)
z =  5: Large decorative shapes
z = 10: Connection lines
z = 20: Main content (dots, shapes)
z = 25: Highlights on content
z = 30: Accents and details
z = 50: Text and labels (always on top)
```

**Key principle:** Reserve ranges for different element types

### Step 2: Background Layers (z=0-5)

```python
# Subtle grid (z=0)
for cell in scene.grid:
    cell.add_border(color=colors.grid, width=0.5, z_index=0)

# Conditional fills (z=1-3)
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_fill(style=FillStyle(color=colors.primary, opacity=0.1), z_index=1)
    elif cell.brightness > 0.4:
        cell.add_fill(style=FillStyle(color=colors.secondary, opacity=0.1), z_index=2)
    else:
        cell.add_fill(style=FillStyle(color=colors.accent, opacity=0.05), z_index=3)

# Large decorative shapes (z=5)
for cell in scene.grid.where(lambda c: (c.row + c.col) % 6 == 0):
    cell.add_ellipse(
        rx=cell.width * 2,
        ry=cell.height * 2,
        fill=colors.primary,
        z_index=5
    )
```

**What's happening:**
- Lowest z-index for most subtle elements
- Opacity keeps background from overwhelming
- Large shapes provide visual interest without dominating

### Step 3: Connection Layer (z=10)

```python
# Connections behind nodes
network_dots = []
for cell in scene.grid.where(lambda c: c.brightness > 0.5):
    dot = cell.add_dot(radius=5, color=colors.primary, z_index=20)
    network_dots.append((dot, cell))

# Create connections (z=10, behind dots at z=20)
for i, (dot1, cell1) in enumerate(network_dots):
    for dot2, cell2 in network_dots[i+1:]:
        # Distance calc and connection creation...
        connection = Connection(
            start=dot1,
            end=dot2,
            style={"color": colors.line, "width": 0.5, "z_index": 10}  # Behind dots
        )
        scene.add(connection)
```

**What's happening:**
- Connections at z=10
- Dots at z=20
- Creates clear visual hierarchy: connections recede, dots pop

### Step 4: Main Content Layer (z=20)

```python
# Primary visual elements
for cell in scene.grid:
    if cell.brightness > 0.6:
        # Main dots
        dot = cell.add_dot(
            radius=3 + cell.brightness * 5,
            color=colors.primary,
            z_index=20
        )
    elif cell.brightness > 0.3:
        # Secondary shapes
        cell.add_polygon(
            shapes.hexagon(size=0.7),
            fill=colors.secondary,
            z_index=20
        )
```

**What's happening:**
- Main content at consistent z-index (20)
- This is the "subject" of your artwork
- Should be visually dominant

### Step 5: Highlight Layer (z=25-30)

```python
# Highlights on selected elements
for dot, cell in network_dots:
    if cell.brightness > 0.8:
        # Glow ring (z=25)
        highlight = cell.add_ellipse(
            rx=dot.radius + 3,
            ry=dot.radius + 3,
            fill=None,
            stroke=colors.accent,
            stroke_width=2,
            z_index=25
        )

        # Bright center (z=30)
        center = cell.add_dot(
            radius=dot.radius * 0.3,
            color="white",
            opacity=0.8,
            z_index=30
        )
```

**What's happening:**
- Highlights above main content
- Create focus and depth
- Used sparingly for impact

### Step 6: Text Layer (z=50+)

```python
# Always on top
for i, (dot, cell) in enumerate(important_nodes):
    label = Text(
        x=cell.center.x,
        y=cell.center.y - 15,
        content=f"Node {i+1}",
        font_size=10,
        color=colors.line,
        z_index=50  # Above everything
    )
    scene.add(label)
```

**What's happening:**
- Text always on top (z=50+)
- Must be readable, so highest z-index
- Consider text shadows at z=49 for contrast

---

## Try It Yourself

### Experiment 1: Five-Layer Depth

```python
# 1. Far background (z=0)
scene.background = colors.background
for cell in scene.grid.checkerboard():
    cell.add_fill(style=FillStyle(color=colors.grid, opacity=0.1), z_index=0)

# 2. Mid background (z=10)
for cell in scene.grid.where(lambda c: c.brightness > 0.6):
    cell.add_ellipse(rx=20, ry=20, fill=colors.secondary, z_index=10)

# 3. Content layer (z=20)
for cell in scene.grid:
    cell.add_dot(radius=2 + cell.brightness * 6, color=colors.primary, z_index=20)

# 4. Foreground accents (z=30)
for cell in scene.grid.where(lambda c: c.brightness > 0.8):
    cell.add_dot(radius=2, color=colors.accent, z_index=30)

# 5. Labels (z=50)
title = Text(x=scene.width//2, y=20, content="Title", font_size=24, z_index=50)
scene.add(title)
```

### Experiment 2: Atmospheric Depth

```python
# Simulate depth with size and opacity
layers = [
    (0, 0.2, 12, 0.3),   # Far: z=0, opacity=0.2, size=12, blur effect via opacity
    (10, 0.4, 8, 0.5),   # Mid-far: z=10
    (20, 0.6, 6, 0.7),   # Mid
    (30, 0.8, 4, 0.9),   # Near
    (40, 1.0, 3, 1.0),   # Very near
]

for z, opacity_mult, size_base, opacity_base in layers:
    for cell in scene.grid.where(lambda c: c.brightness > 0.4):
        cell.add_dot(
            radius=size_base * (0.5 + cell.brightness * 0.5),
            color=colors.primary,
            opacity=opacity_base * opacity_mult,
            z_index=z
        )
```

### Experiment 3: Layered Network

```python
# Background mesh (z=0)
for cell in scene.grid:
    if cell.right:
        line = Line.from_points(cell.center, cell.right.center, width=0.5, color=colors.grid)
        scene.add(line)
        line.z_index = 0

# Main connections (z=10)
# ... create primary network ...

# Nodes (z=20)
# ... create dots ...

# Selected path highlight (z=25)
# ... highlight specific connections ...

# Labels (z=50)
# ... add text ...
```

---

## Layer Management Best Practices

### 1. Use Z-Index Ranges

```python
# Reserve ranges for categories
BACKGROUND_RANGE = (0, 10)      # z=0 to z=9
CONNECTIONS_RANGE = (10, 20)    # z=10 to z=19
CONTENT_RANGE = (20, 30)        # z=20 to z=29
HIGHLIGHTS_RANGE = (30, 40)     # z=30 to z=39
UI_RANGE = (50, 100)            # z=50+
```

### 2. Opacity for Subtle Layers

```python
# Transparent background shapes don't overpower
background = cell.add_ellipse(rx=30, ry=30, fill=colors.primary, z_index=5)

# Solid foreground shapes stand out
foreground = cell.add_dot(radius=5, color=colors.accent, z_index=20)
```

### 3. Test Your Layers

```python
# Temporarily isolate layers to check their effect
def render_layer_only(target_z):
    """Render only entities at specific z-index."""
    for entity in scene.entities:
        if entity.z_index != target_z:
            entity.opacity = 0.1  # Dim other layers
```

---

## Related

- 📖 [Layering Guide](../../fundamentals/05-layering.md) - Z-index system
- 📖 [Styling](../../fundamentals/04-styling.md) - Opacity control
- 🎯 [Connections Example](../intermediate/connections.md) - Network patterns
- 🎯 [Groups Example](../intermediate/groups.md) - Entity organization
- 🎯 [Showcase Example](showcase.md) - Integrated features

