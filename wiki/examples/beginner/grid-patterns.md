
# Example: Grid Patterns

**Difficulty**: ⭐ Beginner

Use grid selection methods to create patterns: checkerboards, borders, stripes, and more.

---

## What You'll Learn

- Grid selection methods (`checkerboard()`, `border()`, etc.)
- Pattern-based iteration
- `where()` for custom conditions
- Row and column selection

---

## Final Result

![Checkerboard](../_images/grid-patterns/01_checkerboard.svg)

### More Examples

| Checkerboard | Border Highlight | Stripe Patterns | Radial Selection |
|--------------|------------------|-----------------|------------------|
| ![Example 1](../_images/grid-patterns/01_checkerboard.svg) | ![Example 2](../_images/grid-patterns/02_border_highlight.svg) | ![Example 3](../_images/grid-patterns/03_stripe_patterns.svg) | ![Example 4](../_images/grid-patterns/04_radial_selection.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette

scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
colors = Palette.midnight()
scene.background = colors.background

# Pattern 1: Checkerboard
for cell in scene.grid.checkerboard():
    cell.add_fill(color=colors.grid, z_index=0)

# Pattern 2: Border highlight
for cell in scene.grid.border():
    cell.add_dot(radius=5, color=colors.accent, z_index=10)

# Pattern 3: Diagonal stripe
for cell in scene.grid.where(lambda c: (c.row + c.col) % 4 == 0):
    cell.add_dot(radius=3, color=colors.primary)

scene.save("grid_patterns.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Checkerboard Pattern

```python
for cell in scene.grid.checkerboard():
    cell.add_fill(color=colors.grid)
```

**What's happening:**
- `checkerboard()` returns alternating cells (like a chessboard)
- Pattern starts with top-left cell included
- Creates natural alternating pattern

**Visual Pattern:**
```
✓ ✗ ✓ ✗ ✓    ✓ = selected
✗ ✓ ✗ ✓ ✗    ✗ = not selected
✓ ✗ ✓ ✗ ✓
✗ ✓ ✗ ✓ ✗
✓ ✗ ✓ ✗ ✓
```

### Step 2: Border Selection

```python
for cell in scene.grid.border():
    cell.add_dot(radius=5, color=colors.accent)
```

**What's happening:**
- `border()` returns cells on the outer edge
- Includes corners and all edges
- Perfect for frames and highlights

**Visual Pattern:**
```
✓ ✓ ✓ ✓ ✓    ✓ = border cells
✓ ✗ ✗ ✗ ✓
✓ ✗ ✗ ✗ ✓
✓ ✗ ✗ ✗ ✓
✓ ✓ ✓ ✓ ✓
```

### Step 3: Custom Conditions with where()

```python
for cell in scene.grid.where(lambda c: (c.row + c.col) % 4 == 0):
    cell.add_dot(radius=3, color=colors.primary)
```

**What's happening:**
- `where()` takes a function that returns True/False
- `(row + col) % 4 == 0` creates diagonal stripes
- Lambda function evaluated for each cell

**Visual Pattern:**
```
✓ ✗ ✗ ✗ ✓    row+col divisible by 4
✗ ✗ ✗ ✓ ✗
✗ ✗ ✓ ✗ ✗
✗ ✓ ✗ ✗ ✗
✓ ✗ ✗ ✗ ✓
```

---

## All Selection Methods

### checkerboard()

Alternating cells in a checkerboard pattern.

```python
for cell in scene.grid.checkerboard():
    cell.add_fill(color="lightgray")
```

### border(thickness=1)

Cells on the outer edge.

```python
# Single border
for cell in scene.grid.border():
    cell.add_dot(color="red")

# Thick border (2 cells deep)
for cell in scene.grid.border(thickness=2):
    cell.add_fill(color="navy")
```

### corners()

Just the four corner cells.

```python
for cell in scene.grid.corners():
    cell.add_dot(radius=8, color="gold")
```

### row(index) / col(index)

Single row or column.

```python
# Middle row
for cell in scene.grid.row(scene.grid.rows // 2):
    cell.add_fill(color="blue")

# First column
for cell in scene.grid.col(0):
    cell.add_border(color="red", width=2)
```

### where(condition)

Custom condition function.

```python
# Brightness threshold
for cell in scene.grid.where(lambda c: c.brightness > 0.5):
    cell.add_dot(radius=5, color="yellow")

# Position-based
for cell in scene.grid.where(lambda c: c.row == c.col):
    cell.add_fill(color="purple")  # Diagonal
```

---

## Try It Yourself

### Experiment 1: Stripe Patterns

```python
# Horizontal stripes
for cell in scene.grid.where(lambda c: c.row % 2 == 0):
    cell.add_fill(color=colors.grid)

# Vertical stripes
for cell in scene.grid.where(lambda c: c.col % 3 == 0):
    cell.add_fill(color=colors.secondary)

# Diagonal stripes
for cell in scene.grid.where(lambda c: (c.row - c.col) % 3 == 0):
    cell.add_fill(color=colors.accent)
```

### Experiment 2: Concentric Borders

```python
# Multiple border layers
for thickness in [1, 2, 3]:
    color_opacity = 1.0 - (thickness - 1) * 0.3
    for cell in scene.grid.border(thickness=thickness):
        cell.add_fill(style=FillStyle(color=colors.primary, opacity=color_opacity))
```

### Experiment 3: Radial Pattern

```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    # Distance from center
    dr = cell.row - center_row
    dc = cell.col - center_col
    distance = (dr*dr + dc*dc) ** 0.5

    # Select cells within radius
    if distance < 5:
        cell.add_dot(radius=8 - distance, color=colors.primary)
```

### Experiment 4: Complex Conditions

```python
# Combine multiple conditions
for cell in scene.grid.where(
    lambda c: c.brightness > 0.5 and (c.row + c.col) % 2 == 0
):
    cell.add_dot(radius=5, color=colors.accent)

# Even/odd rows with different styles
for cell in scene.grid.where(lambda c: c.row % 2 == 0):
    cell.add_fill(color=colors.grid)

for cell in scene.grid.where(lambda c: c.row % 2 == 1):
    cell.add_border(color=colors.line, width=1)
```

---

## Pattern Recipes

### Cross Pattern

```python
middle_row = scene.grid.rows // 2
middle_col = scene.grid.cols // 2

for cell in scene.grid.row(middle_row):
    cell.add_fill(color=colors.primary)

for cell in scene.grid.col(middle_col):
    cell.add_fill(color=colors.primary)
```

### Diamond Pattern

```python
center_row = scene.grid.rows // 2
center_col = scene.grid.cols // 2

for cell in scene.grid:
    manhattan = abs(cell.row - center_row) + abs(cell.col - center_col)
    if manhattan == 5:  # Distance of 5 in Manhattan metric
        cell.add_dot(radius=4, color=colors.accent)
```

### Gradient with Selection

```python
for i in range(0, scene.grid.rows, 2):
    opacity = i / scene.grid.rows  # 0.0 to 1.0
    for cell in scene.grid.row(i):
        cell.add_fill(style=FillStyle(color=colors.primary, opacity=opacity))
```

---

## Related

- 📖 [Grid Selections](../../advanced-concepts/06-grid-selections.md) - Full documentation
- 📖 [Grids and Cells](../../fundamentals/02-grids-and-cells.md) - Grid basics
- 🎯 [Diagonal Lines](diagonal-lines.md) - Previous example
- 🎯 [Polygon Gallery](polygon-gallery.md) - Next example

