# The Surface Protocol

The **Surface Protocol** is the unifying abstraction behind PyFreeform's builder API. Every rectangular region you can draw in — a Cell, a merged group of cells, or the entire Scene canvas — is a **Surface** with the same convenient methods.

## The Core Idea

All the builder methods you know from cells (`add_dot`, `add_line`, `add_curve`, `add_text`, etc.) work identically on any Surface:

| Surface | Bounds | What it is |
|---|---|---|
| **Cell** | Single grid cell | Per-cell art (the usual workflow) |
| **CellGroup** | Merged cells | Title bars, dominoes, super-pixels |
| **Scene** | Entire canvas | Cross-cell overlays, global elements |

```python
# The same API everywhere:
cell.add_dot(at="center", color="red")         # in a cell
group.add_dot(at="center", color="red")        # in a merged region
scene.add_dot(at="center", color="red")        # on the whole canvas
```

## Scene as "Big Cell"

The Scene canvas has the same builder methods as a cell. Named positions, relative coordinates, and `along=`/`t=` all work at the scene level.

### Named positions on the scene

![Scene named positions](_images/07-surface-protocol/01-scene-as-surface.svg)

```python
scene = Scene(400, 300, background="#0f172a")

# Named positions work on the full canvas
scene.add_dot(at="center", radius=12, color="#f43f5e")
scene.add_dot(at="top_left", radius=8, color="#3b82f6")
scene.add_dot(at="bottom_right", radius=8, color="#22c55e")
scene.add_line(start="top_left", end="bottom_right", color="#334155")
```

### Cross-cell curves with `along=`

This is the killer feature. Before the Surface Protocol, placing entities along a curve that spans multiple cells required manual coordinate math. Now it just works:

![Scene along= and t=](_images/07-surface-protocol/02-scene-along-t.svg)

```python
scene = Scene.with_grid(cols=20, rows=12, cell_size=15)

# Cells do their thing
for cell in scene.grid:
    cell.add_dot(radius=2, color="#1e293b")

# Scene-level curve spanning the whole canvas
curve = scene.add_curve(start="left", end="right", curvature=0.4, color="#334155", width=2)

# Place dots along it — same along=/t= syntax as cells!
for i in range(8):
    t = (i + 0.5) / 8
    scene.add_dot(along=curve, t=t, radius=6, color="#f43f5e", z_index=1)
```

## Cell Merging with `grid.merge()`

Merge any rectangular region of cells into a single **CellGroup** surface. The group has averaged brightness/color from its constituent cells and all the builder methods.

### Basic merge

![Basic merge](_images/07-surface-protocol/03-basic-merge.svg)

```python
scene = Scene.with_grid(cols=10, rows=8, cell_size=40)

# Merge a 3x4 block of cells
group = scene.grid.merge(row_start=2, row_end=5, col_start=3, col_end=7)
group.add_fill(color="#3b82f6", opacity=0.3)
group.add_border(color="#60a5fa", width=2)
group.add_text("Merged!", at="center", font_size=16, color="white")
```

### Title bars and sidebars

`merge_row()` and `merge_col()` are shortcuts for common patterns:

![Layout with merged regions](_images/07-surface-protocol/04-layout-merge.svg)

```python
scene = Scene.with_grid(cols=15, rows=10, cell_size=25)

# Header spanning the full width
header = scene.grid.merge(row_start=0, row_end=2)
header.add_fill(color="#1e293b")
header.add_text("My Artwork", at="center", font_size=16, color="#f8fafc")

# Sidebar on the left
sidebar = scene.grid.merge(row_start=2, row_end=10, col_start=0, col_end=3)
sidebar.add_fill(color="#1e293b", opacity=0.5)
```

### Averaged data properties

When you merge cells loaded from an image, the CellGroup automatically averages their brightness, color, and RGB values:

![Averaged data](_images/07-surface-protocol/05-averaged-data.svg)

```python
scene = Scene.from_image("photo.jpg", grid_size=20)

# Merge 2x2 blocks — "super pixels"
for row in range(0, scene.grid.rows - 1, 2):
    for col in range(0, scene.grid.cols - 1, 2):
        block = scene.grid.merge(row, row + 2, col, col + 2)
        # block.color and block.brightness are averaged!
        block.add_dot(at="center", color=block.color,
                      radius=3 + block.brightness * 6)
```

## Curves on merged groups

CellGroups support `along=` and `t=` just like cells and scenes:

![CellGroup along=](_images/07-surface-protocol/06-group-along.svg)

```python
# Merge the top row into a banner
banner = scene.grid.merge_row(0)

# Draw a curve across the banner
wave = banner.add_curve(start="left", end="right", curvature=0.5, color="#64748b")

# Place dots along the wave
for i in range(6):
    banner.add_dot(along=wave, t=(i + 0.5) / 6, radius=4, color="#f43f5e")
```

## Showcase: Everything Together

A complete example combining cells, merged regions, and scene-level overlays:

![Showcase](_images/07-surface-protocol/07-showcase.svg)

```python
scene = Scene.with_grid(cols=20, rows=14, cell_size=20, background="#0f172a")

# Header
header = scene.grid.merge(row_start=0, row_end=2)
header.add_fill(color="#1e293b")
header.add_text("Surface Protocol", at="center", font_size=14, color="#f8fafc")

# Cell-level art in the body
for cell in scene.grid:
    if cell.row >= 2:
        t = (cell.row - 2) / 12
        cell.add_dot(radius=2 + t * 4, color="#3b82f6", opacity=0.3 + t * 0.7)

# Scene-level decorative arc
arc = scene.add_curve(start=(0.1, 0.85), end=(0.9, 0.85),
                      curvature=-0.3, color="#f43f5e", width=2)
for i in range(10):
    scene.add_dot(along=arc, t=(i + 0.5) / 10, radius=3, color="#f43f5e")
```

## API Summary

### Surface (base class)

All surfaces share these methods:

| Method | Description |
|---|---|
| `add_dot(at=, along=, t=, ...)` | Add a dot |
| `add_line(start=, end=, ...)` | Add a line |
| `add_curve(start=, end=, curvature=, ...)` | Add a curve |
| `add_text(content, at=, ...)` | Add text |
| `add_rect(at=, width=, height=, ...)` | Add a rectangle |
| `add_ellipse(at=, rx=, ry=, ...)` | Add an ellipse |
| `add_polygon(vertices, ...)` | Add a polygon |
| `add_fill(color=)` | Fill the entire surface |
| `add_border(color=, width=)` | Border around the surface |
| `add_diagonal(...)` | Add a diagonal line |

Position properties: `center`, `top_left`, `top_right`, `bottom_left`, `bottom_right`, `bounds`

### Grid merge methods

| Method | Description |
|---|---|
| `grid.merge(row_start, row_end, col_start, col_end)` | Merge a rectangular region |
| `grid.merge_row(index)` | Merge an entire row |
| `grid.merge_col(index)` | Merge an entire column |

### CellGroup properties

| Property | Description |
|---|---|
| `brightness` | Average brightness across cells |
| `color` | Average color as hex string |
| `rgb` | Average RGB as (r, g, b) tuple |
| `alpha` | Average alpha |
| `cells` | The constituent Cell objects |
