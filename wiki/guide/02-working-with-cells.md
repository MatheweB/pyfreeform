# Working with Cells

Every cell in the grid carries **data** — brightness, color, position — and you use that data to drive your art.

## Cell Data Properties

When a scene is created with `from_image()`, each cell samples the pixels beneath it:

| Property | Type | Range | Description |
|---|---|---|---|
| `cell.brightness` | `float` | 0.0 – 1.0 | Perceived luminance (0 = black, 1 = white) |
| `cell.color` | `str` | Hex string | Average color as `"#rrggbb"` |
| `cell.rgb` | `tuple` | (0-255, 0-255, 0-255) | RGB components |
| `cell.alpha` | `float` | 0.0 – 1.0 | Opacity from source image |

!!! tip "No image?"
    Cells from `Scene.with_grid()` default to brightness 0.5, color `"#808080"`. Use `normalized_position`, math, or `distance_to()` instead.

## Brightness-Driven Effects

### Size by Brightness

The most classic effect — bright areas get larger marks:

```python
scene = Scene.from_image("MonaLisa.jpg", grid_size=40, cell_size=10)

for cell in scene.grid:
    r = cell.brightness * scene.grid.cell_width * 0.48
    if r > 0.3:
        cell.add_dot(radius=r, color="#ffffff")
```

<figure markdown>
![Brightness to radius](../_images/guide/cells-brightness-radius.svg){ width="420" }
<figcaption>White dots sized by brightness — the classic dot art look.</figcaption>
</figure>

### Rotation by Brightness

Drive shape rotation from the image:

```python
for cell in scene.grid:
    rotation = cell.brightness * 90
    size = 0.4 + cell.brightness * 0.4
    cell.add_polygon(
        Polygon.square(size=size),
        fill=cell.color,
        opacity=0.7,
        rotation=rotation,
    )
```

<figure markdown>
![Brightness-driven rotation](../_images/guide/cells-brightness-rotation.svg){ width="420" }
<figcaption>Squares rotate and grow with brightness, colored by the source image.</figcaption>
</figure>

### Color Fill

The simplest approach — fill each cell with its sampled color:

```python
for cell in scene.grid:
    cell.add_fill(color=cell.color)
```

<figure markdown>
![Color fill mosaic](../_images/guide/cells-color-fill.svg){ width="380" }
<figcaption>A gradient image reproduced as a pixelated color mosaic.</figcaption>
</figure>

---

## Neighbors and Edge Detection

Every cell knows its 8 neighbors:

```python
cell.above          # Cell | None
cell.below          # Cell | None
cell.left           # Cell | None
cell.right          # Cell | None
cell.above_left     # Cell | None  (diagonal)
cell.above_right    # Cell | None
cell.below_left     # Cell | None
cell.below_right    # Cell | None
```

Comparing a cell's brightness to its neighbors reveals edges:

```python
for cell in scene.grid:
    edge = 0.0
    if cell.right:
        edge += abs(cell.brightness - cell.right.brightness)
    if cell.below:
        edge += abs(cell.brightness - cell.below.brightness)
    edge = min(edge * 3, 1.0)  # Amplify
    if edge > 0.1:
        cell.add_dot(radius=edge * 3.5, color="#00d9ff", opacity=edge)
```

<figure markdown>
![Edge detection](../_images/guide/cells-edge-detection.svg){ width="420" }
<figcaption>Edges glow cyan — only cells where brightness changes sharply get marks.</figcaption>
</figure>

---

## Position-Based Effects

### Distance to a Point

`cell.distance_to()` measures pixel distance to any cell, point, or coordinate:

```python
center = scene.grid[10, 10]
max_d = center.distance_to(scene.grid[0, 0])

for cell in scene.grid:
    d = cell.distance_to(center)
    t = 1 - (d / max_d)  # 1 at center, 0 at corners
    cell.add_dot(radius=t * 7, color=colors.primary, opacity=0.3 + t * 0.7)
```

<figure markdown>
![Radial distance effect](../_images/guide/cells-distance-radial.svg){ width="340" }
<figcaption>Dots fade and shrink with distance from the center cell.</figcaption>
</figure>

### Normalized Position

`cell.normalized_position` returns `(nx, ny)` where both range from 0.0 (top-left) to 1.0 (bottom-right):

```python
for cell in scene.grid:
    nx, ny = cell.normalized_position
    size = 0.3 + ny * 0.5   # Grow downward
    # ... color gradient from left to right
```

<figure markdown>
![Position-based gradient](../_images/guide/cells-normalized-position.svg){ width="360" }
<figcaption>Diamonds grow downward, colors shift from left to right.</figcaption>
</figure>

---

## Sub-Cell Sampling

For higher-detail effects, sample the image at multiple points within each cell:

```python
for cell in scene.grid:
    for (rx, ry), pos in [
        ((0.25, 0.25), "top_left"),
        ((0.75, 0.25), "top_right"),
        ((0.25, 0.75), "bottom_left"),
        ((0.75, 0.75), "bottom_right"),
    ]:
        color = cell.sample_hex(rx, ry)      # (1)!
        brightness = cell.sample_brightness(rx, ry)
        cell.add_dot(at=pos, radius=brightness * 3.5, color=color)
```

1. `sample_hex(rx, ry)` reads the pixel at relative position (rx, ry) within the cell. Only works with `from_image()`.

<figure markdown>
![Sub-cell sampling](../_images/guide/cells-sub-sampling.svg){ width="420" }
<figcaption>4 dots per cell, each sampling a different quadrant — effectively 4x resolution.</figcaption>
</figure>

---

## Filtering with `where()`

Use `grid.where()` to select cells by any condition:

```python
# Dark cells get fills, bright cells get stars
for cell in scene.grid.where(lambda c: c.brightness < 0.4):
    cell.add_fill(color=cell.color, opacity=0.5)

for cell in scene.grid.where(lambda c: c.brightness >= 0.4):
    cell.add_polygon(
        Polygon.star(points=4, size=0.3 + cell.brightness * 0.5),
        fill=cell.color, opacity=0.7,
    )
```

<figure markdown>
![Where threshold](../_images/guide/cells-where-threshold.svg){ width="420" }
<figcaption>Different treatments for dark (fills) and bright (stars) cells.</figcaption>
</figure>

---

## What's Next?

You've mastered reading cell data. Now learn all the entity types you can place in cells:

[Drawing with Entities &rarr;](03-drawing-with-entities.md){ .md-button }
