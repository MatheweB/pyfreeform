
# Example: Showcase

**Difficulty**: ⭐⭐⭐ Advanced

Integrate multiple PyFreeform features into a single comprehensive artwork: parametric paths, transforms, connections, layering, and more.

---

## What You'll Learn

- Combining multiple entity types
- Integrated feature usage
- Complex composition techniques
- Real-world artwork patterns

---

## Final Result

![Comprehensive](../_images/showcase/01_comprehensive.svg)

### More Examples

| Comprehensive | All Features |
|---------------|--------------|
| ![Example 1](../_images/showcase/01_comprehensive.svg) | ![Example 2](../_images/showcase/02_all_features.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette, Connection, Text, shapes
from pyfreeform.config import FillStyle
import math

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()
scene.background = colors.background

# Feature 1: Grid patterns with selections
for cell in scene.grid.checkerboard():
    cell.add_fill(style=FillStyle(color=colors.grid, opacity=0.1), z_index=0)

for cell in scene.grid.border():
    cell.add_border(color=colors.line, width=1.5, z_index=1)

# Feature 2: Parametric positioning along curves
for row in range(0, scene.grid.rows, 5):
    for col in range(0, scene.grid.cols - 5, 5):
        cell_start = scene.grid[row, col]
        cell_end = scene.grid[row, col + 5]

        # Create flowing curve
        curve = Curve.from_points(
            start=cell_start.center,
            end=cell_end.center,
            curvature=0.5,
            color=colors.line,
            width=1.5,
            z_index=5
        )
        scene.add(curve)

        # Dots along curve
        for i in range(6):
            t = i / 5
            dot = Dot(
                x=curve.point_at(t).x,
                y=curve.point_at(t).y,
                radius=3 + i * 0.5,
                color=colors.primary if i % 2 == 0 else colors.secondary,
                z_index=10
            )
            scene.add(dot)

# Feature 3: Rotating polygons
for cell in scene.grid.where(lambda c: c.brightness > 0.7 and (c.row + c.col) % 4 == 0):
    angle = (cell.row * 20 + cell.col * 30) % 360

    poly = cell.add_polygon(
        shapes.hexagon(size=0.8),
        fill=colors.accent,
        stroke=colors.line,
        stroke_width=1,
        z_index=15
    )
    poly.rotate(angle)

# Feature 4: Connected network
network_nodes = []
for cell in scene.grid.where(lambda c: c.brightness > 0.6):
    node = cell.add_dot(
        radius=4 + cell.brightness * 4,
        color=colors.primary,
        z_index=20
    )
    network_nodes.append((node, cell))

for i, (node1, cell1) in enumerate(network_nodes):
    for node2, cell2 in network_nodes[i+1:i+3]:
        connection = Connection(
            start=node1,
            end=node2,
            style={"color": colors.line, "width": 0.5, "z_index": 12}
        )
        scene.add(connection)

# Feature 5: Ellipses with parametric dots
for cell in scene.grid.where(lambda c: (c.row + c.col) % 7 == 0):
    ellipse = cell.add_ellipse(
        rx=cell.width * 0.4,
        ry=cell.height * 0.4,
        rotation=(cell.row * 15) % 360,
        fill=None,
        stroke=colors.secondary,
        stroke_width=1,
        z_index=8
    )

    # Dot on ellipse
    cell.add_dot(
        along=ellipse,
        t=cell.brightness,
        radius=3,
        color=colors.accent,
        z_index=18
    )

# Feature 6: Text labels and titles
title = Text(
    x=scene.width // 2,
    y=30,
    content="Generative Showcase",
    font_size=24,
    color=colors.primary,
    font_family="sans-serif",
    text_anchor="middle",
    z_index=50
)
scene.add(title)

# Feature legend
legend = Text(
    x=20,
    y=scene.height - 10,
    content="Paths | Transforms | Networks | Typography",
    font_size=9,
    color=colors.text,
    font_family="monospace",
    text_anchor="start",
    z_index=50
)
scene.add(legend)

scene.save("showcase.svg")
```

---

## Features Demonstrated

### 1. Grid Selections
- `checkerboard()` for alternating pattern
- `border()` for frame effect
- `where()` for custom conditions

### 2. Parametric Paths
- Curves with `point_at(t)`
- Dots positioned along paths
- Ellipses as paths

### 3. Transforms
- Polygon rotation
- Angle calculations from position
- Dynamic orientation

### 4. Connections
- Network visualization
- Distance-based linking
- Opacity for depth

### 5. Layering
- Strategic z-index use (0-50)
- Background to foreground
- Text always on top

### 6. Typography
- Title overlay
- Legend/caption
- Multiple font sizes

---

## Try It Yourself

Modify the showcase to emphasize different features or create your own comprehensive example combining techniques from across the documentation.

---

## Related

- 🎯 [Multi-Layer Example](multi-layer.md) - Layering depth
- 🎯 [Parametric Paths Example](parametric-paths.md) - Path features
- 📖 All fundamental guides and entity documentation

