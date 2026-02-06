
# Lines

Lines create straight paths between two points. Simple, versatile, and essential for structure, grids, and connections.

---

## What is a Line?

A **Line** is a straight path entity with:
- **Start point** - Beginning (x1, y1)
- **End point** - Ending (x2, y2)
- **Width** - Stroke width
- **Color** - Stroke color
- **Cap** - Endpoint style

Lines support parametric positioning, making them useful as paths for other entities.

![Line directions](./_images/02-lines/01_line_directions.svg)

---

## Creating Lines

### Via Cell Method

```python
# Named positions
cell.add_line(start="top_left", end="bottom_right")

# Relative coordinates (0-1)
cell.add_line(start=(0.2, 0.2), end=(0.8, 0.8))

# Diagonal shortcuts
cell.add_diagonal(start="top_left", end="bottom_right")  # NW to SE
cell.add_diagonal(start="bottom_left", end="top_right")  # SW to NE
```

### Direct Construction

```python
from pyfreeform import Line

# From coordinates
line = Line(x1=0, y1=0, x2=100, y2=100, width=2, color="black")

# From points
from pyfreeform.core.point import Point
line = Line.from_points(
    start=Point(0, 0),
    end=Point(100, 100),
    width=2
)

scene.add(line)
```

---

## Properties

```python
line.start        # Start point
line.end          # End point
line.width        # Stroke width
line.color        # Stroke color
line.z_index      # Layer order
```

---

## Parametric Positioning

Position elements along the line:

```python
line = cell.add_line(start="left", end="right")

# Linear interpolation from start (t=0) to end (t=1)
point_at_start = line.point_at(0)
point_at_middle = line.point_at(0.5)
point_at_end = line.point_at(1.0)

# Position dots along line
cell.add_dot(along=line, t=0.25, radius=3)
cell.add_dot(along=line, t=0.5, radius=3)
cell.add_dot(along=line, t=0.75, radius=3)
```

**Formula:**
```
P(t) = start + (end - start) × t
     = start × (1-t) + end × t
```

![Parametric positioning](./_images/02-lines/02_parametric_positioning.svg)

---

## Anchors

```python
line.anchor_names  # ["start", "center", "end"]

line.anchor("start")   # Start point
line.anchor("center")  # Midpoint (t=0.5)
line.anchor("end")     # End point
```

---

## Common Patterns

### Pattern 1: Grid Lines

```python
for cell in scene.grid:
    cell.add_border(color="#eeeeee", width=0.5)
```

![Grid lines](./_images/02-lines/03_grid_lines.svg)

### Pattern 2: Diagonal with Sliding Dots

```python
for cell in scene.grid:
    line = cell.add_diagonal(start="bottom_left", end="top_right", color="gray")

    # Dot position driven by brightness
    cell.add_dot(
        along=line,
        t=cell.brightness,
        radius=4,
        color="red"
    )
```

![Diagonal with Sliding Dots](./_images/02-lines/04_diagonal_dots.svg)

### Pattern 3: Connecting Neighbors

```python
for cell in scene.grid:
    if cell.right:
        line = Line.from_points(
            start=cell.center,
            end=cell.right.center,
            width=1,
            color="blue"
        )
        scene.add(line)
```

---

## Line Caps

The `cap` parameter controls endpoint style. Native SVG caps apply to both ends:

```python
# Round caps (default) - smooth endpoints
cell.add_line(start="left", end="right", cap="round", width=5)

# Square caps - extends past endpoint
cell.add_line(start="left", end="right", cap="square", width=5)

# Butt caps - flush with endpoint
cell.add_line(start="left", end="right", cap="butt", width=5)
```

### Arrow Caps

Use `"arrow"` to add arrowheads. Arrows can be applied per-end with `start_cap` and `end_cap`:

```python
# Arrow at the end (most common)
cell.add_line(start="left", end="right", end_cap="arrow")

# Arrow at the start
cell.add_line(start="left", end="right", start_cap="arrow")

# Arrows at both ends
cell.add_line(start="left", end="right", cap="arrow")

# Works with curves too
cell.add_curve(curvature=0.3, end_cap="arrow")

# Via style objects
from pyfreeform import LineStyle
style = LineStyle(width=2, color="navy", end_cap="arrow")
cell.add_line(start="left", end="right", style=style)
```

Arrow size scales automatically with stroke width (3x by default).

### Per-End Caps

`start_cap` and `end_cap` override `cap` for individual endpoints:

```python
# Round start, arrow end
cell.add_line(start="left", end="right", cap="round", end_cap="arrow")
```

---

## See Also

- 📖 [Dots](01-dots.md) - Position dots along lines
- 📖 [Curves](03-curves.md) - Smooth paths
- 📖 [Connections](../advanced-concepts/02-connections.md) - Dynamic links
- 🎯 [Diagonal Example](../examples/beginner/diagonal-lines.md)

