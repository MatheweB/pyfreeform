
# Example: Diagonal Lines

**Difficulty**: ⭐ Beginner

Use parametric positioning to slide dots along diagonal lines based on image brightness.

---

## What You'll Learn

- Creating diagonal lines with `add_diagonal()`
- Parametric positioning with `along=` parameter
- Using `t` parameter for position (0 to 1)
- Brightness-driven positioning

---

## Final Result

![Sliding Dots](../_images/diagonal-lines/01_sliding_dots.svg)

### More Examples

| Sliding Dots | Brightness Driven | Inverted Position |
|--------------|-------------------|-------------------|
| ![Example 1](../_images/diagonal-lines/01_sliding_dots.svg) | ![Example 2](../_images/diagonal-lines/02_brightness_driven.svg) | ![Example 3](../_images/diagonal-lines/03_inverted_position.svg) |

---

## Complete Code

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=30)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    # Create diagonal line (bottom-left to top-right)
    line = cell.add_diagonal(
        start="bottom_left",
        end="top_right",
        color=colors.line,
        width=1,
        z_index=0
    )

    # Position dot along line based on brightness
    cell.add_dot(
        along=line,
        t=cell.brightness,  # 0.0 (start) to 1.0 (end)
        radius=4,
        color=colors.primary,
        z_index=1
    )

scene.save("diagonal_art.svg")
```

---

## Step-by-Step Breakdown

### Step 1: Create Diagonal Lines

```python
line = cell.add_diagonal(
    start="bottom_left",
    end="top_right",
    color=colors.line,
    width=1
)
```

**What's happening:**
- `start="bottom_left", end="top_right"` creates a line from bottom-left to top-right (↗)
- `start="top_left", end="bottom_right"` creates a line from top-left to bottom-right (↘)
- Lines are created in every cell of the grid

**Diagonal Directions:**
```
start="top_left",           start="bottom_left",
end="bottom_right":         end="top_right":
  ╲                            ╱
   ╲                          ╱
    ╲                        ╱
     ╲                      ╱
```

### Step 2: Position Dots Parametrically

```python
cell.add_dot(
    along=line,
    t=cell.brightness,  # 0.0 to 1.0
    radius=4,
    color=colors.primary
)
```

**What's happening:**
- `along=line` tells the dot to position itself on the line
- `t=cell.brightness` determines position along the line
- `t=0.0`: bottom-left (start of line)
- `t=0.5`: middle of line
- `t=1.0`: top-right (end of line)

**Position Formula:**
```
point(t) = start + (end - start) × t

Examples (for "up" diagonal):
t=0.0  → bottom-left corner
t=0.25 → 25% up the diagonal
t=0.5  → center of cell
t=0.75 → 75% up the diagonal
t=1.0  → top-right corner
```

### Step 3: Brightness Mapping

```python
t=cell.brightness  # Automatically 0.0 to 1.0
```

**What's happening:**
- Bright cells (brightness near 1.0) place dots at top-right
- Dark cells (brightness near 0.0) place dots at bottom-left
- Creates a flowing, dynamic composition

---

## Try It Yourself

### Experiment 1: Change Direction

```python
# Diagonal going down instead
line = cell.add_diagonal(start="top_left", end="bottom_right")
```

### Experiment 2: Multiple Dots Per Line

```python
line = cell.add_diagonal(start="bottom_left", end="top_right", color=colors.line)

# Place 3 dots along the line
for i in range(3):
    t = i / 2  # 0, 0.5, 1.0
    cell.add_dot(
        along=line,
        t=t,
        radius=2,
        color=colors.primary
    )
```

### Experiment 3: Inverted Brightness

```python
# Bright areas at start, dark at end
cell.add_dot(
    along=line,
    t=1 - cell.brightness,  # Invert
    radius=4,
    color=colors.primary
)
```

### Experiment 4: Both Directions

```python
# Diagonal up
up_line = cell.add_diagonal(start="bottom_left", end="top_right", color=colors.line)
cell.add_dot(along=up_line, t=cell.brightness, radius=3, color=colors.primary)

# Diagonal down
down_line = cell.add_diagonal(start="top_left", end="bottom_right", color=colors.line)
cell.add_dot(along=down_line, t=1 - cell.brightness, radius=3, color=colors.secondary)
```

---

## Understanding Parametric Positioning

The `along=` parameter works with any entity that has a `point_at(t)` method:

- **Lines**: Linear interpolation from start to end
- **Curves**: Smooth Bézier path
- **Ellipses**: Around the perimeter

**Example with different path types:**

```python
# Works with all pathable entities
line = cell.add_line(start="left", end="right")
curve = cell.add_curve(start="left", end="right", curvature=0.5)
ellipse = cell.add_ellipse(rx=10, ry=8)

# Same parametric positioning
cell.add_dot(along=line, t=0.5)    # Middle of line
cell.add_dot(along=curve, t=0.5)   # Middle of curve
cell.add_dot(along=ellipse, t=0.5) # Left side of ellipse (180°)
```

---

## Related

- 📖 [Lines Entity](../../entities/02-lines.md) - Full documentation
- 📖 [Parametric Positioning](../../parametric-art/02-positioning-along-paths.md) - Deep dive
- 📖 [Pathable Protocol](../../advanced-concepts/03-pathable-protocol.md) - How it works
- 🎯 [Custom Dots](custom-dots.md) - Previous example
- 🎯 [Curves Example](../intermediate/curves.md) - More parametric positioning

