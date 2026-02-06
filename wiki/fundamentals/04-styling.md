
# Styling

Make your artwork beautiful with PyFreeform's flexible styling system. Control colors, sizes, opacity, and visual properties with ease.

---

## The Styling System

PyFreeform provides two ways to style entities:

1. **Inline Parameters** - Pass properties directly when creating entities
2. **Style Objects** - Use typed configuration objects for reusability

Both approaches work identically - choose based on your preference and needs.

---

## Color System

PyFreeform's color system is flexible and intuitive, supporting multiple formats:

### Named Colors

Use any standard CSS color name:

```python
cell.add_dot(color="red")
cell.add_dot(color="coral")
cell.add_dot(color="dodgerblue")
cell.add_dot(color="mediumseagreen")
```

![Named Colors](./_images/04-styling/01-color-named-colors.svg)

Common names: `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan`, `magenta`, `black`, `white`, `gray`.

### Hex Colors

Standard hex notation:

```python
cell.add_dot(color="#ff5733")   # Full hex
cell.add_dot(color="#f57")      # Short hex
```

![Hex Colors](./_images/04-styling/02-color-hex-colors.svg)

### RGB Tuples

Specify exact RGB values (0-255):

```python
cell.add_dot(color=(255, 87, 51))
cell.add_dot(color=(100, 150, 200))
```

![RGB Tuples](./_images/04-styling/03-color-rgb-tuples.svg)

### Automatic Conversion

The Color class handles all conversions internally:

```python
from pyfreeform import Color

c = Color("red")
c = Color("#ff0000")
c = Color((255, 0, 0))

# All produce the same color
hex_value = c.to_hex()  # "#ff0000"
```

See [Color System](../color-and-style/01-color-system.md) for details.

---

## Inline Styling

Pass styling parameters directly when creating entities:

### Dots

```python
cell.add_dot(
    radius=5,          # Size in pixels
    color="coral",     # Fill color
    z_index=0          # Layer (optional)
)
```

![Inline Styling Dots](./_images/04-styling/04-inline-styling-dots.svg)

### Lines

```python
cell.add_line(
    start="top_left",
    end="bottom_right",
    width=2,           # Stroke width
    color="navy",      # Stroke color
    z_index=0
)
```

![Inline Styling Lines](./_images/04-styling/05-inline-styling-lines.svg)

### Curves

```python
cell.add_curve(
    start="left",
    end="right",
    curvature=0.5,
    width=1,           # Stroke width
    color="purple",
    z_index=0
)
```

### Shapes (Ellipse, Polygon, Rect)

```python
# Ellipse
cell.add_ellipse(
    rx=15,             # Horizontal radius
    ry=10,             # Vertical radius
    rotation=45,       # Degrees
    fill="coral",      # Fill color
    stroke="black",    # Border color (optional)
    stroke_width=1,    # Border width
    z_index=0
)

# Polygon
cell.add_polygon(
    vertices,
    fill="purple",
    stroke="white",
    stroke_width=2,
    z_index=0
)

# Rectangle (fill entire cell)
cell.add_fill(
    color="lightgray",
    z_index=0
)

# Or with a border
cell.add_border(
    color="black",
    width=1,
    z_index=0
)
```

### Text

```python
cell.add_text(
    content="Hello",
    font_size=16,
    color="white",
    font_family="sans-serif",  # or "serif", "monospace"
    text_anchor="middle",      # "start", "middle", "end"
    baseline="middle",         # "auto", "middle", "hanging", etc.
    rotation=0,
    z_index=0
)
```

![Inline Styling Shapes](./_images/04-styling/06-inline-styling-shapes.svg)

---

## Style Objects

For reusable configuration, use style objects:

### DotStyle

```python
from pyfreeform.config import DotStyle

# Create style
style = DotStyle(
    radius=5,
    color="coral",
    z_index=0
)

# Use style
cell.add_dot(style=style)

# Or mix with inline
cell.add_dot(style=style, color="blue")  # Override color
```

**Builder methods:**

```python
style = DotStyle(radius=5, color="red")

# Create variations
large = style.with_radius(10)
blue = style.with_color("blue")
top = style.with_z_index(10)
```

![Style Objects Dot](./_images/04-styling/07-style-objects-dot.svg)

### LineStyle

```python
from pyfreeform.config import LineStyle

style = LineStyle(
    width=2,
    color="navy",
    z_index=0,
    cap="round"  # "round", "square", or "butt"
)

cell.add_line(start="left", end="right", style=style)
```

![Style Objects Line](./_images/04-styling/08-style-objects-line.svg)

### FillStyle

```python
from pyfreeform.config import FillStyle

style = FillStyle(
    color="blue",
    opacity=0.5,  # 0.0 = transparent, 1.0 = opaque
    z_index=0
)

cell.add_fill(style=style)
```

### BorderStyle

```python
from pyfreeform.config import BorderStyle

style = BorderStyle(
    width=1,
    color="#cccccc",
    z_index=0
)

cell.add_border(style=style)
```

---

## Palettes

Palettes provide cohesive color schemes for your artwork:

### Using Built-in Palettes

```python
from pyfreeform import Palette

# Choose a palette
colors = Palette.midnight()   # Dark blue theme
colors = Palette.sunset()     # Warm oranges
colors = Palette.ocean()      # Cool blues
colors = Palette.forest()     # Natural greens
colors = Palette.monochrome() # Black and white
colors = Palette.paper()      # Beige tones
colors = Palette.neon()       # Vibrant colors
colors = Palette.pastel()     # Soft colors

# Apply to scene
scene.background = colors.background

# Use palette colors
cell.add_dot(color=colors.primary)
cell.add_dot(color=colors.secondary)
cell.add_dot(color=colors.accent)
cell.add_line(start="left", end="right", color=colors.line)
cell.add_border(color=colors.grid)
```

![Palettes Overview](./_images/04-styling/09-palettes-overview.svg)
![Palette Midnight](./_images/04-styling/10-palette-midnight.svg)
![Palette Sunset](./_images/04-styling/11-palette-sunset.svg)
![Palette Ocean](./_images/04-styling/12-palette-ocean.svg)

### Palette Properties

Each palette provides:

```python
colors.background  # Background color
colors.primary     # Main color
colors.secondary   # Secondary color
colors.accent      # Accent/highlight color
colors.line        # Line/stroke color
colors.grid        # Grid/structure color
```

See [Palettes](../color-and-style/02-palettes.md) for all palettes with visual swatches.

---

## Opacity and Transparency

### Fill Opacity

Control transparency of filled shapes:

```python
# Semi-transparent fill (via FillStyle)
from pyfreeform import FillStyle
style = FillStyle(color="blue", opacity=0.5)
cell.add_fill(style=style)

# Or with a different color
style = FillStyle(color="red", opacity=0.3)
cell.add_fill(style=style)
```

![Opacity Demonstration](./_images/04-styling/13-opacity-demonstration.svg)

### Background Transparency

Scene backgrounds default to transparent:

```python
scene.background = None  # Transparent (default)
scene.background = "white"  # Opaque white
```

---

## Common Styling Patterns

### Pattern 1: Consistent Palette

```python
from pyfreeform import Palette

colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(color=colors.primary, radius=6)
    elif cell.brightness > 0.4:
        cell.add_dot(color=colors.secondary, radius=4)
    else:
        cell.add_dot(color=colors.accent, radius=2)
```

![Pattern Consistent Palette](./_images/04-styling/14-pattern-consistent-palette.svg)

### Pattern 2: Style Reuse

```python
from pyfreeform.config import DotStyle

# Define styles once
large_style = DotStyle(radius=8, color="coral")
small_style = DotStyle(radius=3, color="navy")

# Reuse across cells
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(style=large_style)
    else:
        cell.add_dot(style=small_style)
```

![Pattern Style Reuse](./_images/04-styling/15-pattern-style-reuse.svg)

### Pattern 3: Data-Driven Colors

```python
for cell in scene.grid:
    # Use actual image color
    cell.add_dot(color=cell.color, radius=5)

    # Or map brightness to palette
    if cell.brightness > 0.6:
        color = colors.primary
    else:
        color = colors.secondary

    cell.add_dot(color=color)
```

![Pattern Data-Driven Colors](./_images/04-styling/16-pattern-data-driven-colors.svg)

### Pattern 4: Gradient Effect

```python
for cell in scene.grid:
    # Interpolate between colors based on position
    t = cell.col / scene.grid.cols

    # Simple red-to-blue gradient
    r = int(255 * (1 - t))
    b = int(255 * t)
    color = (r, 0, b)

    cell.add_dot(color=color, radius=5)
```

![Pattern Gradient Effect](./_images/04-styling/17-pattern-gradient-effect.svg)

---

## Stroke vs Fill

Shapes can have both fill and stroke (border):

### Fill Only (Default)

```python
cell.add_ellipse(fill="coral")
cell.add_polygon(vertices, fill="purple")
```

![Fill Only](./_images/04-styling/18-stroke-fill-only.svg)

### Stroke Only

```python
cell.add_ellipse(fill=None, stroke="black", stroke_width=2)
cell.add_border(color="navy", width=1)
```

![Stroke Only](./_images/04-styling/19-stroke-stroke-only.svg)

### Both Fill and Stroke

```python
cell.add_ellipse(
    fill="coral",
    stroke="darkred",
    stroke_width=2
)

cell.add_polygon(
    vertices,
    fill="lightblue",
    stroke="navy",
    stroke_width=1
)
```

![Both Fill and Stroke](./_images/04-styling/20-stroke-both-fill-and-stroke.svg)

---

## Line Caps

Control how line endpoints are rendered:

```python
from pyfreeform.config import LineStyle

# Round caps (default) - smooth endpoints
round_style = LineStyle(width=5, cap="round")

# Square caps - extends past endpoint
square_style = LineStyle(width=5, cap="square")

# Butt caps - flush with endpoint
butt_style = LineStyle(width=5, cap="butt")

cell.add_line(start="left", end="right", style=round_style)
```

![Line Caps](./_images/04-styling/21-line-caps.svg)

---

## Font Styling

Text entities have extensive typography control:

```python
cell.add_text(
    content="Title",
    font_size=24,              # Size in pixels
    font_family="sans-serif",  # Font family
    color="white",             # Text color
    text_anchor="middle",      # Horizontal alignment
    baseline="middle",         # Vertical alignment
    rotation=0                 # Rotation in degrees
)
```

**Font families:**
- `"sans-serif"` - Modern, clean (default)
- `"serif"` - Traditional, elegant
- `"monospace"` - Fixed-width, technical
- `"Arial"`, `"Georgia"`, etc. - Specific fonts

![Font Styling](./_images/04-styling/22-font-styling.svg)

See [Text Entity](../entities/06-text.md) for details.

---

## Tips and Best Practices

### Use Palettes for Consistency

Palettes ensure your artwork has a cohesive color scheme:

```python
colors = Palette.sunset()
scene.background = colors.background
# Use colors.primary, colors.secondary throughout
```

### Define Styles Early

Create reusable styles at the top of your script:

```python
bright_dot = DotStyle(radius=6, color="yellow")
dim_dot = DotStyle(radius=2, color="gray")

# Use throughout
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(style=bright_dot)
```

### Leverage Image Colors

When working with images, cell.color is powerful:

```python
# Direct use
cell.add_dot(color=cell.color)

# Or manipulate
r, g, b = cell.rgb
darkened = (r//2, g//2, b//2)
cell.add_dot(color=darkened)
```

### Test with Monochrome First

Develop your composition in black and white, then add color:

```python
# Develop structure
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(color="black", radius=5)

# Then add color
colors = Palette.ocean()
# ... update colors
```

---

## Next Steps

- **Learn layering**: [Layering](05-layering.md)
- **Explore palettes**: [Palettes](../color-and-style/02-palettes.md)
- **See styled examples**: [Custom Dots](../examples/beginner/custom-dots.md)

---

## See Also

- 📖 [Layering](05-layering.md) - Z-index system
- 📖 [Color System](../color-and-style/01-color-system.md) - Color details
- 📖 [Palettes](../color-and-style/02-palettes.md) - All color schemes
- 📖 [Style Objects](../color-and-style/03-style-objects.md) - Style classes
- 🎯 [Custom Dots Example](../examples/beginner/custom-dots.md) - Styling in action
- 🔍 [Styling API Reference](../api-reference/entities.md)

