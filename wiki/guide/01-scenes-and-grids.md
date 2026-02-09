# Scenes & Grids

The **Scene** is your canvas, and the **Grid** gives it structure. Together they form the foundation of every PyFreeform artwork.

## Creating Scenes

### From an Image

`Scene.from_image()` loads a photo and divides it into a grid of cells, each sampling the image's colors and brightness.

```python
from pyfreeform import Scene

scene = Scene.from_image("MonaLisa.jpg", grid_size=40, cell_size=10)
```

**`grid_size`** controls resolution — how many columns of cells across. More cells = more detail:

<div class="compare-grid" markdown>

<figure markdown>
![20 cells across](../_images/guide/scenes-grid-size-20.svg)
<figcaption><code>grid_size=20</code></figcaption>
</figure>

<figure markdown>
![40 cells across](../_images/guide/scenes-grid-size-40.svg)
<figcaption><code>grid_size=40</code></figcaption>
</figure>

<figure markdown>
![60 cells across](../_images/guide/scenes-grid-size-60.svg)
<figcaption><code>grid_size=60</code></figcaption>
</figure>

</div>

### Cell Ratio

**`cell_ratio`** changes cell proportions. A ratio of 2.0 makes cells twice as wide as tall:

<div class="compare-grid" markdown>

<figure markdown>
![Square cells](../_images/guide/scenes-ratio-square.svg)
<figcaption><code>cell_ratio=1.0</code> (square)</figcaption>
</figure>

<figure markdown>
![Wide cells](../_images/guide/scenes-ratio-wide.svg)
<figcaption><code>cell_ratio=2.0</code> (wide)</figcaption>
</figure>

<figure markdown>
![Tall cells](../_images/guide/scenes-ratio-tall.svg)
<figcaption><code>cell_ratio=0.5</code> (tall)</figcaption>
</figure>

</div>

### From Scratch

`Scene.with_grid()` creates a grid with no image data — use position and math to drive visuals:

```python
from pyfreeform import Scene, Palette

colors = Palette.midnight()
scene = Scene.with_grid(cols=15, rows=15, cell_size=22, background=colors.background)

for cell in scene.grid:
    nx, ny = cell.normalized_position
    radius = 2 + (nx * ny) * 8
    cell.add_dot(radius=radius, color=colors.primary, opacity=0.5 + nx * 0.5)
```

<figure markdown>
![with_grid basic pattern](../_images/guide/scenes-with-grid-basic.svg){ width="360" }
<figcaption>Dot size grows with position — no image needed.</figcaption>
</figure>

---

## Grid Selections

The grid offers powerful selection methods for targeting specific cells.

### Row & Column

```python
for cell in scene.grid.row(3):        # All cells in row 3
    cell.add_fill(color=colors.primary, opacity=0.4)

for cell in scene.grid.column(6):     # All cells in column 6
    cell.add_fill(color=colors.accent, opacity=0.4)
```

<figure markdown>
![Row and column highlighting](../_images/guide/scenes-row-column.svg){ width="300" }
<figcaption>Row 3 in coral, column 6 in amber, intersection highlighted.</figcaption>
</figure>

### Border

```python
for cell in scene.grid.border(thickness=2):  # (1)!
    cell.add_fill(color=colors.accent, opacity=0.7)
```

1. `thickness` controls how many rows/columns deep the border extends.

<figure markdown>
![Border selection](../_images/guide/scenes-border-selection.svg){ width="320" }
<figcaption>The outer 2 rows/columns highlighted as a border.</figcaption>
</figure>

### Region

```python
for cell in scene.grid.region(2, 6, 3, 9):  # (1)!
    cell.add_polygon(Polygon.hexagon(size=0.6), fill=colors.primary)
```

1. `region(row_start, row_end, col_start, col_end)` — end is exclusive.

<figure markdown>
![Region selection with hexagons](../_images/guide/scenes-region.svg){ width="320" }
<figcaption>Hexagons placed only in the selected rectangular region.</figcaption>
</figure>

### Checkerboard & Diagonal

```python
for cell in scene.grid.checkerboard("black"):
    cell.add_polygon(Polygon.diamond(size=0.7), fill=colors.primary)

for cell in scene.grid.checkerboard("white"):
    cell.add_dot(radius=4, color=colors.accent)
```

<div class="image-row" markdown>

<figure markdown>
![Checkerboard](../_images/guide/scenes-checkerboard.svg){ width="300" }
<figcaption>Checkerboard: diamonds and dots alternate.</figcaption>
</figure>

<figure markdown>
![Diagonal](../_images/guide/scenes-diagonal.svg){ width="300" }
<figcaption>Every 3rd diagonal highlighted with fills.</figcaption>
</figure>

</div>

---

## Merging Cells

Merge a row, column, or rectangular region into a single **CellGroup** — a virtual surface that spans multiple cells:

```python
title_bar = scene.grid.merge_row(0)
title_bar.add_fill(color=colors.primary, opacity=0.2)
title_bar.add_text("TITLE BAR", at="center", font_size=14, color=colors.accent, bold=True)
```

<figure markdown>
![Merged title bar](../_images/guide/scenes-merged-title.svg){ width="320" }
<figcaption>Row 0 merged into a CellGroup with text overlay.</figcaption>
</figure>

A CellGroup has all the same `add_*` methods as a Cell — it's a full Surface.

!!! info "Other merge methods"
    - `grid.merge_col(i)` — merge a full column
    - `grid.merge(row_start, row_end, col_start, col_end)` — merge any rectangular region

---

## What's Next?

Now that you can create and navigate grids, learn how to read and use each cell's data:

[Working with Cells &rarr;](02-working-with-cells.md){ .md-button }
