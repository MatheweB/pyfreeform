
# Rectangles

Rectangles provide boxes, backgrounds, and borders. Essential for structure, fills, and framing.

---

## What is a Rectangle?

A **Rect** entity is a box with:
- **Position** - Top-left corner (x, y)
- **Dimensions** - Width and height
- **Fill** - Interior color (optional)
- **Stroke** - Border color (optional)
- **Stroke width** - Border thickness

Rectangles are perfect for backgrounds, borders, and structural elements.

![Rectangle Styles](./_images/07-rectangles/01_fill_vs_stroke.svg)

---

## Creating Rectangles

### Via Cell Methods

```python
# Fill entire cell
cell.add_fill(color="lightgray")

# Border around cell
cell.add_border(color="black", width=1)

# Custom rectangle (direct construction)
from pyfreeform import Rect
rect = Rect(
    x=cell.center.x - 15,
    y=cell.center.y - 10,
    width=30,
    height=20,
    fill="blue",
    stroke="navy",
    stroke_width=2
)
scene.add(rect)
```

### Direct Construction

```python
from pyfreeform import Rect

rect = Rect(
    x=50,
    y=100,
    width=100,
    height=60,
    fill="coral",
    stroke="darkred",
    stroke_width=2
)

scene.add(rect)
```

---

## Properties

```python
rect.position      # Top-left corner (Point)
rect.x, rect.y     # Coordinates
rect.width         # Width
rect.height        # Height
rect.fill          # Fill color
rect.stroke        # Stroke color
rect.stroke_width  # Border thickness
rect.z_index       # Layer order
```

---

## Anchors

Rectangles have rich anchor system:

```python
rect.anchor_names  # ["center", "top_left", "top_right",
                   #  "bottom_left", "bottom_right",
                   #  "top", "bottom", "left", "right"]

rect.anchor("center")        # Center point
rect.anchor("top_left")      # Top-left corner
rect.anchor("bottom_right")  # Bottom-right corner
rect.anchor("top")           # Top center
rect.anchor("left")          # Left center
# etc.
```

---

## Common Patterns

### Pattern 1: Cell Backgrounds

```python
for cell in scene.grid:
    # Background color from image
    cell.add_fill(color=cell.color, z_index=0)

    # Content on top
    cell.add_dot(radius=5, color="white", z_index=1)
```

![Cell Backgrounds](./_images/07-rectangles/04_cell_backgrounds.svg)

### Pattern 2: Grid Borders

```python
for cell in scene.grid:
    cell.add_border(color="#eeeeee", width=0.5)
```

![Grid Borders](./_images/07-rectangles/03_grid_borders.svg)

### Pattern 3: Checkerboard

```python
for cell in scene.grid:
    if (cell.row + cell.col) % 2 == 0:
        cell.add_fill(color="black")
    else:
        cell.add_fill(color="white")
```

![Checkerboard Pattern](./_images/07-rectangles/02_checkerboard.svg)

### Pattern 4: Highlight Border

```python
for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_border(color="gold", width=2, z_index=10)
```

![Highlight Border](./_images/07-rectangles/05_highlight_border.svg)

---

## Fill vs Stroke

### Fill Only

```python
cell.add_fill(color="blue")
```

### Stroke Only

```python
cell.add_border(color="black", width=2)
```

### Both

```python
# Fill + border (two separate operations)
cell.add_fill(color="lightblue", z_index=0)
cell.add_border(color="navy", width=1, z_index=1)
```

---

## Styling with Style Objects

```python
from pyfreeform.config import FillStyle, BorderStyle

# Reusable styles
bg_style = FillStyle(color="lightgray", opacity=0.5)
border_style = BorderStyle(width=1, color="#333")

cell.add_fill(style=bg_style)
cell.add_border(style=border_style)
```

---

## Layering

Rectangles are often used as backgrounds:

```python
# Background (lowest layer)
cell.add_fill(color="white", z_index=-10)

# Content (middle)
cell.add_dot(radius=5, z_index=0)

# Border (top)
cell.add_border(color="black", width=1, z_index=10)
```

---

## Complete Example

```python
from pyfreeform import Scene, Palette

scene = Scene.with_grid(cols=10, rows=10, cell_size=30)
colors = Palette.paper()
scene.background = colors.background

for cell in scene.grid:
    # Alternating pattern
    if (cell.row + cell.col) % 2 == 0:
        cell.add_fill(color=colors.grid, z_index=0)

    # Border on all cells
    cell.add_border(color=colors.line, width=0.5, z_index=1)

    # Highlight corners
    if cell.row == 0 or cell.row == 9 or cell.col == 0 or cell.col == 9:
        cell.add_border(color=colors.accent, width=2, z_index=2)

scene.save("bordered_grid.svg")
```

![Complete Rectangle Example](./_images/07-rectangles/06_complete_example.svg)

---

## Tips

### Use fill for Backgrounds

```python
cell.add_fill(color="lightgray", z_index=-1)  # Behind everything
```

### Borders for Structure

```python
# Subtle grid
for cell in scene.grid:
    cell.add_border(color="#f0f0f0", width=0.5)
```

### Opacity for Overlays

```python
from pyfreeform.config import FillStyle

overlay = FillStyle(color="black", opacity=0.3)
cell.add_fill(style=overlay)
```

---

## See Also

- 📖 [Dots](01-dots.md) - Content to place on backgrounds
- 📖 [Styling](../fundamentals/04-styling.md) - Fill and stroke options
- 📖 [Layering](../fundamentals/05-layering.md) - Z-index for backgrounds
- 🎯 [Grid Patterns](../examples/beginner/grid-patterns.md)

