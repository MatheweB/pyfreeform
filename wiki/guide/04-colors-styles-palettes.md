# Colors, Styles & Palettes

PyFreeform provides a coherent color and styling system. Master three concepts: the **color parameter split**, **style objects**, and **palettes**.

## The Color Parameter Split

This is the most important API distinction to remember:

| Parameter | Used by | Description |
|---|---|---|
| **`color=`** | Dot, Line, Curve, Text, `add_fill`, `add_border` | Stroke-like entities |
| **`fill=`** | Rect, Ellipse, Polygon | Filled shapes |

<figure markdown>
![fill= vs color= comparison](../_images/guide/styles-fill-vs-color.svg){ width="400" }
<figcaption>Top row: entities using <code>color=</code>. Bottom row: entities using <code>fill=</code>.</figcaption>
</figure>

!!! warning "Common mistake"
    Writing `cell.add_polygon(verts, color="red")` will raise an error. Use `fill="red"` for shapes.

## Color Formats

All color parameters accept:

- **Named colors**: `"red"`, `"coral"`, `"navy"`, `"salmon"`
- **Hex strings**: `"#ff6b6b"`, `"#f00"`, `"#FF6B6B"`
- **RGB tuples**: Colors from `cell.rgb` can be formatted to hex with `cell.color`

---

## Opacity

Every entity supports `opacity` (0.0 transparent → 1.0 opaque, default 1.0):

```python
cell.add_dot(radius=10, color="coral", opacity=0.5)
cell.add_fill(color="navy", opacity=0.3)
```

### Shape-Specific: fill_opacity & stroke_opacity

Shapes (Rect, Ellipse, Polygon) support independent opacity for fill and stroke:

```python
cell.add_ellipse(
    rx=0.45, ry=0.45,
    fill=colors.primary,
    stroke=colors.accent,
    stroke_width=3,
    fill_opacity=0.4,     # Semi-transparent fill
    stroke_opacity=1.0,   # Fully opaque stroke
)
```

<figure markdown>
![Fill opacity progression](../_images/guide/styles-fill-stroke-opacity.svg){ width="380" }
<figcaption>Fill opacity from 0.2 to 1.0 with constant stroke opacity.</figcaption>
</figure>

### Layered Opacity

Stack semi-transparent shapes for color mixing effects:

<figure markdown>
![Opacity layering](../_images/guide/styles-opacity-layers.svg){ width="220" }
<figcaption>Three overlapping circles at 50% opacity — colors blend where they overlap.</figcaption>
</figure>

---

## Style Objects

Instead of repeating parameters, define a **style object** once and reuse it:

```python
from pyfreeform import DotStyle, LineStyle, ShapeStyle

dot_small = DotStyle(radius=3, color="coral", opacity=0.6)
dot_large = DotStyle(radius=7, color="gold", opacity=0.9)
line_thin = LineStyle(width=1, color="#666688", opacity=0.4)
shape_hex = ShapeStyle(color="teal", opacity=0.5)

for cell in scene.grid:
    cell.add_dot(style=dot_small)               # Apply directly
    cell.add_line(start="top", end="bottom", style=line_thin)
```

<figure markdown>
![Style reuse](../_images/guide/styles-reuse.svg){ width="320" }
<figcaption>Three zones using different pre-defined styles — consistent look with no parameter repetition.</figcaption>
</figure>

### All Style Classes

| Class | For Methods | Key Fields |
|---|---|---|
| `DotStyle` | `add_dot()` | `radius`, `color`, `opacity` |
| `LineStyle` | `add_line()`, `add_diagonal()`, `add_curve()`, `add_path()` | `width`, `color`, `cap`, `start_cap`, `end_cap` |
| `FillStyle` | `add_fill()` | `color`, `opacity` |
| `BorderStyle` | `add_border()` | `width`, `color`, `opacity` |
| `ShapeStyle` | `add_ellipse()`, `add_polygon()`, `add_rect()` | `color` (→ fill), `stroke`, `stroke_width` |
| `TextStyle` | `add_text()` | `font_size`, `color`, `font_family`, `bold`, `italic` |
| `ConnectionStyle` | `Connection` | `width`, `color`, `cap` |

### Builder Methods

Styles are immutable. Use `.with_*()` to create modified copies:

```python
base = LineStyle(width=2, color="coral")
thick = base.with_width(4)          # New style, width=4
arrow = base.with_end_cap("arrow")  # New style, with arrow cap
```

---

## Palettes

8 pre-built color palettes with 6 named colors each:

<div class="compare-grid" markdown>

<figure markdown>
![Midnight](../_images/guide/styles-palette-midnight.svg)
<figcaption>Midnight</figcaption>
</figure>

<figure markdown>
![Sunset](../_images/guide/styles-palette-sunset.svg)
<figcaption>Sunset</figcaption>
</figure>

<figure markdown>
![Ocean](../_images/guide/styles-palette-ocean.svg)
<figcaption>Ocean</figcaption>
</figure>

<figure markdown>
![Forest](../_images/guide/styles-palette-forest.svg)
<figcaption>Forest</figcaption>
</figure>

<figure markdown>
![Monochrome](../_images/guide/styles-palette-monochrome.svg)
<figcaption>Monochrome</figcaption>
</figure>

<figure markdown>
![Paper](../_images/guide/styles-palette-paper.svg)
<figcaption>Paper</figcaption>
</figure>

<figure markdown>
![Neon](../_images/guide/styles-palette-neon.svg)
<figcaption>Neon</figcaption>
</figure>

<figure markdown>
![Pastel](../_images/guide/styles-palette-pastel.svg)
<figcaption>Pastel</figcaption>
</figure>

</div>

### Using Palettes

```python
from pyfreeform import Palette

colors = Palette.midnight()
scene = Scene.with_grid(cols=10, rows=10, cell_size=20, background=colors.background)

for cell in scene.grid:
    cell.add_dot(color=colors.primary)
    cell.add_border(color=colors.grid, width=0.3)
```

### Named Colors

| Name | Purpose |
|---|---|
| `colors.background` | Scene background |
| `colors.primary` | Main element color |
| `colors.secondary` | Supporting element color |
| `colors.accent` | Highlight/emphasis color |
| `colors.line` | Lines and connections |
| `colors.grid` | Grid borders |

### Custom Palettes

```python
my_palette = Palette(
    background="#1a1a2e",
    primary="#ff6b6b",
    secondary="#4ecdc4",
    accent="#ffe66d",
    line="#666688",
    grid="#3d3d5c",
)
```

Utilities: `colors.with_background("#000")`, `colors.inverted()`, `colors.all_colors()`.

---

## What's Next?

Learn the "killer feature" — positioning entities along any path:

[Paths & Parametric Positioning &rarr;](05-paths-and-parametric.md){ .md-button }
