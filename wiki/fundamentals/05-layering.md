
# Layering

Control what renders on top using PyFreeform's z-index layering system. Proper layering creates depth and visual hierarchy in your artwork.

---

## Understanding Z-Index

The **z-index** determines the rendering order of entities:

```
Higher z-index = Renders on top
Lower z-index = Renders below

z-index: 10  ← Top layer (rendered last)
z-index: 5
z-index: 1
z-index: 0   ← Default layer
z-index: -5
z-index: -10 ← Bottom layer (rendered first)
```

![Understanding Z-Index](./_images/05-layering/01-understanding-z-index.svg)

Think of z-index as layers in a stack - higher numbers sit on top of lower numbers.

---

## How Rendering Works

When you save a scene:

1. All entities are collected
2. Sorted by z-index (lowest to highest)
3. Rendered in order (background → foreground)
4. SVG elements appear in order in the output file

This means:
- **z-index: 0** (default) renders in the middle
- **z-index: -10** renders first (appears behind everything)
- **z-index: 10** renders last (appears on top of everything)

---

## Setting Z-Index

### During Creation

Pass `z_index` when creating entities:

```python
# Background layer
cell.add_fill(color="lightgray", z_index=0)

# Middle layer
cell.add_line(start="left", end="right", z_index=1)

# Foreground layer
cell.add_dot(radius=5, color="red", z_index=2)
```

![Setting Z-Index During Creation](./_images/05-layering/02-setting-z-index-during-creation.svg)

### After Creation

Modify z-index on existing entities:

```python
dot = cell.add_dot(radius=5)
dot.z_index = 10  # Move to top layer
```

![Setting Z-Index After Creation](./_images/05-layering/03-setting-z-index-after-creation.svg)

### With Style Objects

Include z-index in style objects:

```python
from pyfreeform.config import DotStyle

background_style = DotStyle(radius=8, color="gray", z_index=0)
foreground_style = DotStyle(radius=4, color="red", z_index=10)

cell.add_dot(style=background_style)
cell.add_dot(style=foreground_style)  # Renders on top
```

![Setting Z-Index With Styles](./_images/05-layering/04-setting-z-index-with-styles.svg)

---

## Common Layering Patterns

### Pattern 1: Background → Shapes → Accents

```python
Z_BACKGROUND = 0
Z_SHAPES = 1
Z_ACCENTS = 2

for cell in scene.grid:
    # Background
    cell.add_fill(color="lightgray", z_index=Z_BACKGROUND)

    # Main shapes
    if cell.brightness > 0.5:
        cell.add_ellipse(
            rx=10, ry=8,
            fill="blue",
            z_index=Z_SHAPES
        )

    # Accent dots
    cell.add_dot(
        radius=2,
        color="white",
        z_index=Z_ACCENTS
    )
```

![Pattern Background Shapes Accents](./_images/05-layering/05-pattern-background-shapes-accents.svg)

Result: Gray background, blue ellipses on top, white dots on top of everything.

### Pattern 2: Grid → Lines → Dots

```python
Z_GRID = 0
Z_LINES = 1
Z_DOTS = 2

# Grid borders (bottom layer)
for cell in scene.grid:
    cell.add_border(color="#eeeeee", width=0.5, z_index=Z_GRID)

# Diagonal lines (middle layer)
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_diagonal(start="bottom_left", end="top_right", color="gray", z_index=Z_LINES)

# Dots (top layer)
for cell in scene.grid:
    cell.add_dot(
        radius=3,
        color=cell.color,
        z_index=Z_DOTS
    )
```

![Pattern Grid Lines Dots](./_images/05-layering/06-pattern-grid-lines-dots.svg)

### Pattern 3: Multi-Layer Composition

Complex artwork with many layers:

```python
# Define layers
Z_BG = 0
Z_GRID = 1
Z_CURVES = 2
Z_SHAPES = 3
Z_HIGHLIGHTS = 4
Z_TEXT = 5

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()

# Background (bottom)
scene.background = colors.background

# Grid lines
for cell in scene.grid:
    cell.add_border(color=colors.grid, z_index=Z_GRID)

# Curves in medium brightness
for cell in scene.grid:
    if 0.3 < cell.brightness < 0.7:
        curve = cell.add_curve(
            curvature=0.5,
            color=colors.line,
            z_index=Z_CURVES
        )

# Hexagons in bright areas
from pyfreeform import shapes
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_polygon(
            shapes.hexagon(),
            fill=colors.primary,
            z_index=Z_SHAPES
        )

# Highlight dots
for cell in scene.grid:
    if cell.brightness > 0.8:
        cell.add_dot(
            radius=3,
            color=colors.accent,
            z_index=Z_HIGHLIGHTS
        )

# Title text (top)
from pyfreeform import Text
title = Text(
    x=scene.width // 2,
    y=30,
    content="Layered Artwork",
    font_size=24,
    color="white",
    z_index=Z_TEXT
)
scene.add(title)
```

---

## Practical Examples

### Example 1: Dot on Line

```python
# Line behind (z-index: 0)
line = cell.add_line(
    start="top_left",
    end="bottom_right",
    width=2,
    color="gray",
    z_index=0
)

# Dot on top (z-index: 1)
cell.add_dot(
    along=line,
    t=0.5,
    radius=5,
    color="red",
    z_index=1  # Renders above the line
)
```

![Practical Dot on Line](./_images/05-layering/07-practical-dot-on-line.svg)

### Example 2: Overlapping Cells

When elements extend beyond cell boundaries:

```python
for cell in scene.grid:
    # Large background circle (might overlap neighbors)
    cell.add_ellipse(
        rx=20, ry=20,
        fill="lightblue",
        z_index=0  # Background
    )

    # Small foreground dot (always on top)
    cell.add_dot(
        radius=5,
        color="navy",
        z_index=10  # Foreground
    )
```

![Practical Overlapping Cells](./_images/05-layering/08-practical-overlapping-cells.svg)

The higher z-index ensures foreground dots stay on top even when background circles overlap.

### Example 3: Text Overlay

Add text labels on top of artwork:

```python
# Create artwork
for cell in scene.grid:
    cell.add_dot(color=cell.color, z_index=0)

# Add labels on top
from pyfreeform import Text
for row in range(0, scene.grid.rows, 5):
    cell = scene.grid[row, 0]
    label = Text(
        x=5,
        y=cell.y + cell.height / 2,
        content=f"Row {row}",
        font_size=10,
        color="white",
        z_index=100  # Way on top
    )
    scene.add(label)
```

![Practical Text Overlay](./_images/05-layering/09-practical-text-overlay.svg)

---

## Z-Index Best Practices

### Use Named Constants

Define layer constants for clarity:

```python
# Good - clear intent
Z_BACKGROUND = 0
Z_CONTENT = 5
Z_OVERLAY = 10

cell.add_fill(z_index=Z_BACKGROUND)
cell.add_dot(z_index=Z_CONTENT)

# Avoid - magic numbers
cell.add_fill(z_index=0)
cell.add_dot(z_index=5)
```

![Best Practice Named Constants](./_images/05-layering/10-best-practice-named-constants.svg)

### Space Out Layers

Leave gaps between z-index values for flexibility:

```python
# Good - room for additions
Z_BACKGROUND = 0
Z_LINES = 10      # Can add layers 1-9 if needed
Z_SHAPES = 20     # Can add layers 11-19
Z_ACCENTS = 30    # Can add layers 21-29

# Avoid - no room to insert layers
Z_BACKGROUND = 0
Z_LINES = 1
Z_SHAPES = 2
Z_ACCENTS = 3
```

![Best Practice Space Out Layers](./_images/05-layering/11-best-practice-space-out-layers.svg)

### Default is Zero

If you don't specify z-index, it defaults to 0:

```python
cell.add_dot()  # z_index = 0 (default)
```

### Relative Values Work

You can use any integer, including negatives:

```python
cell.add_fill(z_index=-100)  # Far background
cell.add_dot(z_index=0)      # Middle
cell.add_text("label", z_index=100)   # Far foreground
```

---

## Debugging Layering Issues

### Issue: Element Hidden Behind Others

**Solution**: Increase its z-index

```python
# Was hidden
dot = cell.add_dot(color="red", z_index=0)

# Now visible
dot.z_index = 10
```

![Debugging Hidden Element](./_images/05-layering/15-debugging-hidden-element.svg)

### Issue: Unexpected Render Order

**Solution**: Check z-index values are spaced correctly

```python
# Print all z-indices
for entity in scene.entities:
    print(f"{type(entity).__name__}: z={entity.z_index}")
```

### Issue: Can't See Background

**Solution**: Ensure background has lowest z-index

```python
# Background
cell.add_fill(color="lightgray", z_index=-10)

# Everything else
cell.add_dot(color="red", z_index=0)
```

![Comparison With Without Z-Index](./_images/05-layering/16-comparison-with-without-z-index.svg)

---

## Advanced Layering

### Dynamic Layer Assignment

Assign z-index based on data:

```python
for cell in scene.grid:
    # Brighter cells render on top
    z = int(cell.brightness * 10)  # 0-10 range

    cell.add_dot(
        radius=5,
        color=cell.color,
        z_index=z
    )
```

![Advanced Dynamic Layers](./_images/05-layering/12-advanced-dynamic-layers.svg)

### Layer Groups

Organize entities into layer groups:

```python
LAYER_BACKGROUND = range(-10, 0)
LAYER_CONTENT = range(0, 10)
LAYER_FOREGROUND = range(10, 20)

# Use ranges
cell.add_fill(z_index=LAYER_BACKGROUND.start)
cell.add_dot(z_index=LAYER_CONTENT.start)
cell.add_border(z_index=LAYER_FOREGROUND.start)
```

![Advanced Layer Groups](./_images/05-layering/13-advanced-layer-groups.svg)

### Connection Layers

Place connections between content layers:

```python
Z_SHAPES = 0
Z_CONNECTIONS = 5  # Between shapes and highlights
Z_HIGHLIGHTS = 10

# Shapes
dot1 = cell1.add_dot(z_index=Z_SHAPES)
dot2 = cell2.add_dot(z_index=Z_SHAPES)

# Connection
connection = dot1.connect(
    dot2,
    style={"width": 1, "color": "gray", "z_index": Z_CONNECTIONS}
)

# Highlights
cell1.add_dot(radius=2, color="white", z_index=Z_HIGHLIGHTS)
```

---

## Real-World Example

Here's a complete multi-layer composition from Example 06:

```python
from pyfreeform import Scene, Palette, shapes

scene = Scene.from_image("photo.jpg", grid_size=25)
colors = Palette.midnight()
scene.background = colors.background

# Define layers
Z_GRID = 1
Z_LINES = 2
Z_DOTS_MAIN = 3
Z_DOTS_HIGHLIGHT = 4
Z_CONNECTIONS = 5

# Layer 1: Subtle grid
for cell in scene.grid.border(thickness=1):
    cell.add_border(color=colors.grid, width=0.5, z_index=Z_GRID)

# Layer 2: Diagonal lines in medium brightness
for cell in scene.grid.where(lambda c: 0.3 < c.brightness < 0.7):
    cell.add_diagonal(
        start="bottom_left",
        end="top_right",
        color=colors.line,
        width=1,
        z_index=Z_LINES
    )

# Layer 3: Main dots based on brightness
for cell in scene.grid:
    size = 2 + cell.brightness * 6
    cell.add_dot(
        radius=size,
        color=cell.color,
        z_index=Z_DOTS_MAIN
    )

# Layer 4: Highlight dots for bright areas
bright_dots = []
for cell in scene.grid.where(lambda c: c.brightness > 0.7):
    dot = cell.add_dot(
        radius=4,
        color=colors.accent,
        z_index=Z_DOTS_HIGHLIGHT
    )
    bright_dots.append(dot)

# Layer 5: Connect bright dots
for i, dot in enumerate(bright_dots[:-1]):
    if dot.cell and dot.cell.right:
        next_dot = bright_dots[i + 1]
        connection = dot.connect(
            next_dot,
            style={"width": 1, "color": colors.accent, "z_index": Z_CONNECTIONS}
        )
        scene.add(connection)

scene.save("layered_art.svg")
```

![Complex Multi-Layer Example](./_images/05-layering/14-complex-multi-layer-example.svg)

---

## Summary

Key points about layering:

- **Z-index controls render order** - higher renders on top
- **Default is zero** - specify only when you need layering
- **Use named constants** - makes code clearer
- **Space out values** - leaves room for additions
- **Check for issues** - print z-indices when debugging

Proper layering creates depth and ensures your artwork renders exactly as intended!

---

## Next Steps

You've completed the fundamentals! Now explore specific topics:

- **Individual entities**: [Entities Section](../entities/01-dots.md)
- **Advanced features**: [Advanced Concepts](../advanced-concepts/01-anchor-system.md)
- **See it in action**: [Multi-Layer Example](../examples/advanced/multi-layer.md)

---

## See Also

- 📖 [Entities](03-entities.md) - What you're layering
- 📖 [Styling](04-styling.md) - How to style layers
- 🎯 [Advanced Example](../examples/advanced/multi-layer.md) - Multi-layer composition
- 🎯 [Showcase Example](../examples/advanced/showcase.md) - Complex layering
- 🔍 [Entity API Reference](../api-reference/entities.md)

