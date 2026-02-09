# Advanced Compositions

Combine multiple techniques — layers, groups, merged regions, and connections — into complex artwork.

## Multi-Layer Artwork

Use `z_index` to orchestrate four distinct visual layers:

```python
# Layer 0: subtle grid
cell.add_border(color=colors.grid, width=0.3, opacity=0.15, z_index=0)

# Layer 1: faded hexagons
cell.add_polygon(Polygon.hexagon(size=0.6), fill=colors.secondary, opacity=0.15, z_index=1)

# Layer 2: diagonal lines
cell.add_diagonal(width=0.5 + nx * 1.5, color=colors.primary, opacity=0.25, z_index=2)

# Layer 3: accent dots on every 3rd cell
cell.add_dot(radius=4, color=colors.accent, opacity=0.7, z_index=3)
```

<figure markdown>
![Multi-layer](../_images/recipes/adv-multi-layer.svg){ width="380" }
<figcaption>Grid → hexagons → diagonals → dots: four layers building up visual density.</figcaption>
</figure>

## Reusable EntityGroup Motifs

Define a factory function for a reusable crosshair motif:

```python
def make_crosshair(color1, color2):
    g = EntityGroup()
    g.add(Dot(0, 0, radius=8, color=color1, opacity=0.6))
    g.add(Line(-12, 0, 12, 0, width=1, color=color2, opacity=0.5))
    g.add(Line(0, -12, 0, 12, width=1, color=color2, opacity=0.5))
    g.add(Ellipse(0, 0, rx=10, ry=10, fill="none", stroke=color2, stroke_width=0.5))
    return g

for cell in scene.grid:
    group = make_crosshair(colors.primary, colors.secondary)
    cell.place(group)
    group.fit_to_cell(0.8)
    group.rotate(nx * 45)
```

<figure markdown>
![EntityGroup motifs](../_images/recipes/adv-entity-groups.svg){ width="360" }
<figcaption>Crosshair motifs with rotation varying by position.</figcaption>
</figure>

## Merged CellGroup Regions

Use `grid.merge()` to create distinct regions with different treatments:

```python
# Feature area
feature = scene.grid.merge(2, 8, 3, 9)
feature.add_fill(color=colors.primary, opacity=0.15)
feature.add_border(color=colors.accent, width=1.5)
feature.add_text("FEATURED", at="center", font_size=16, color=colors.accent, bold=True)

# Title bar
title = scene.grid.merge_row(0)
title.add_fill(color=colors.primary, opacity=0.2)
title.add_text("COMPOSITION", at="center", font_size=12, color=colors.accent)
```

<figure markdown>
![CellGroup regions](../_images/recipes/adv-cell-groups.svg){ width="320" }
<figcaption>A title bar and featured region created with merged CellGroups.</figcaption>
</figure>

## The Full Stack: Image + Geometry + Connections

Combine every technique into a single composition:

1. **Layer 0**: Faded image fills as a background
2. **Layer 1**: Hexagons sized by brightness
3. **Layer 2**: White dots on bright cells, connected to neighbors
4. **Layer 3**: Title overlay on merged cells

<figure markdown>
![Full combination](../_images/recipes/adv-combined.svg){ width="420" }
<figcaption>Image fills, polygons, connections, and text — every technique working together.</figcaption>
</figure>

!!! tip "Layering strategy"
    Work from background to foreground. Low z_index for ambient elements, high z_index for focal points. Opacity is your best friend for letting layers breathe.
