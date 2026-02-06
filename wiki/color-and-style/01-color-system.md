
# Color System

PyFreeform's flexible color system supports multiple formats, making it easy to specify colors in whatever way is most convenient for your project. Whether you prefer named colors for readability, hex codes for precision, or RGB tuples for programmatic generation, PyFreeform has you covered.

## Color Formats

Colors in PyFreeform can be specified in three interchangeable formats:

1. **Named colors** — readable strings like `"red"` or `"coral"`
2. **Hex strings** — CSS-style codes like `"#ff0000"` or `"#f00"`
3. **RGB tuples** — integer triplets like `(255, 0, 0)`

All three formats are equivalent and can be used anywhere a color is expected.

### Named Colors

Named colors are the most readable option, perfect for quick prototyping and when exact color values aren't critical.

```python
cell.add_dot(color="red")
cell.add_dot(color="coral")
cell.add_dot(color="dodgerblue")
```

![Named Colors](_images/01-color-system/01-named-colors.svg)

![Named Colors Variety](_images/01-color-system/02-named-colors-variety.svg)

!!! tip "Common Named Colors"
    PyFreeform supports all standard CSS/SVG named colors. Here are some commonly used ones:

    **Reds**: `red`, `crimson`, `darkred`, `indianred`, `coral`, `salmon`
    **Blues**: `blue`, `navy`, `dodgerblue`, `steelblue`, `skyblue`, `cornflowerblue`
    **Greens**: `green`, `lime`, `forestgreen`, `seagreen`, `olivedrab`, `chartreuse`
    **Yellows/Oranges**: `yellow`, `gold`, `orange`, `darkorange`, `goldenrod`
    **Purples**: `purple`, `indigo`, `violet`, `orchid`, `magenta`, `plum`
    **Grays**: `black`, `dimgray`, `gray`, `darkgray`, `silver`, `lightgray`, `white`
    **Earth tones**: `brown`, `sienna`, `saddlebrown`, `peru`, `tan`, `burlywood`

### Hex Colors

Hex colors provide precise control and are familiar to anyone who has worked with web design or graphic software.

```python
cell.add_dot(color="#ff5733")
cell.add_dot(color="#f57")  # Short form
```

![Hex Colors](_images/01-color-system/03-hex-colors.svg)

![Hex Color Spectrum](_images/01-color-system/04-hex-color-spectrum.svg)

!!! info "Hex Color Format"
    Hex colors use the format `#RRGGBB` where:

    - `RR` = red component (00-FF)
    - `GG` = green component (00-FF)
    - `BB` = blue component (00-FF)

    Short form `#RGB` expands to `#RRGGBB` (e.g., `#f00` → `#ff0000`)

**Examples:**

```python
# Full form
cell.add_dot(color="#ff0000")  # Pure red
cell.add_dot(color="#00ff00")  # Pure green
cell.add_dot(color="#0000ff")  # Pure blue

# Short form
cell.add_dot(color="#f00")     # Pure red
cell.add_dot(color="#0f0")     # Pure green
cell.add_dot(color="#00f")     # Pure blue

# Mixed colors
cell.add_dot(color="#ff6b35")  # Coral orange
cell.add_dot(color="#4ecdc4")  # Turquoise
```

### RGB Tuples

RGB tuples are ideal for programmatic color generation, allowing you to compute colors mathematically.

```python
cell.add_dot(color=(255, 87, 51))
```

![RGB Tuples](_images/01-color-system/05-rgb-tuples.svg)

![RGB Gradient](_images/01-color-system/06-rgb-gradient.svg)

!!! info "RGB Tuple Format"
    RGB tuples are three-element tuples `(red, green, blue)` where each component is an integer from 0 to 255:

    - `(255, 0, 0)` = pure red
    - `(0, 255, 0)` = pure green
    - `(0, 0, 255)` = pure blue
    - `(255, 255, 255)` = white
    - `(0, 0, 0)` = black

**Examples:**

```python
# Primary colors
cell.add_dot(color=(255, 0, 0))    # Red
cell.add_dot(color=(0, 255, 0))    # Green
cell.add_dot(color=(0, 0, 255))    # Blue

# Programmatic generation
for i in range(10):
    intensity = int(255 * i / 9)
    cell.add_dot(color=(intensity, 0, 255 - intensity))

# Using variables
r, g, b = 100, 150, 200
cell.add_dot(color=(r, g, b))
```

## Color Class

The `Color` class provides a unified interface for working with colors and converting between formats.

```python
from pyfreeform import Color

c = Color("red")
c = Color("#ff0000")
c = Color((255, 0, 0))

# Convert to hex
hex_value = c.to_hex()  # "#ff0000"
```

![Color Class](_images/01-color-system/07-color-class.svg)

![Color Formats Comparison](_images/01-color-system/08-color-formats-comparison.svg)

**API:**

- `Color(value: str | tuple[int, int, int])` — create a Color from any format
- `color.to_hex() -> str` — convert to hex string (e.g., `"#ff0000"`)

**Usage examples:**

```python
# Parse different formats
c1 = Color("crimson")
c2 = Color("#dc143c")
c3 = Color((220, 20, 60))

# All convert to the same hex
print(c1.to_hex())  # "#dc143c"
print(c2.to_hex())  # "#dc143c"
print(c3.to_hex())  # "#dc143c"

# Use in your code
def create_gradient(start_color, end_color, steps):
    start = Color(start_color)
    # ... gradient logic
```

## Image-Based Colors

When working with image data, each cell provides color information derived from the underlying image.

### Cell Color Properties

Every cell has three color-related properties:

```python
# Hex string of the cell's dominant color
hex_color = cell.color  # e.g., "#ff6b35"

# RGB tuple of the cell's dominant color
rgb_color = cell.rgb    # e.g., (255, 107, 53)

# Brightness value from 0.0 (black) to 1.0 (white)
brightness = cell.brightness  # e.g., 0.73
```

**Example:**

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=20)

for cell in scene.cells:
    # Use the cell's own color
    cell.add_dot(at="center", radius=5, color=cell.color)

    # Darken bright cells
    if cell.brightness > 0.7:
        cell.add_fill(color="black", z_index=-1)

    # Access RGB components
    r, g, b = cell.rgb
    if r > 200:  # Very red cells
        cell.add_border(color="red", width=2)
```

!!! tip "Using Brightness for Effects"
    The `brightness` property is particularly useful for creating opacity-like effects or conditional rendering based on image luminosity:

    ```python
    for cell in scene.cells:
        # Skip dark cells
        if cell.brightness < 0.3:
            continue

        # Larger dots for brighter cells
        radius = cell.brightness * 10
        cell.add_dot(at="center", radius=radius, color="white")
    ```

## fill= vs color= Parameter Reference

!!! warning "Critical API Distinction"
    PyFreeform uses two different parameter names for colors depending on the entity type. Using the wrong parameter will cause errors.

Different drawing methods use different parameter names for specifying colors:

| Use `color=` | Use `fill=` |
|--------------|-------------|
| `cell.add_dot()` | `cell.add_polygon()` |
| `cell.add_line()` | `cell.add_ellipse()` |
| `cell.add_curve()` | `Rect()` |
| `cell.add_diagonal()` | `Polygon()` |
| `cell.add_text()` | `Ellipse()` |
| `cell.add_fill()` | |
| `cell.add_border()` | |
| `Dot()` | |
| `Line()` | |
| `Curve()` | |
| `Text()` | |
| `Connection` style dict | |
| `DotStyle` | |
| `LineStyle` | |
| `BorderStyle` | |
| `FillStyle` | |

**Quick rule:** If it's a **filled shape** (polygon, ellipse, rectangle), use `fill=`. For everything else, use `color=`.

**Examples:**

```python
# ✓ Correct
cell.add_dot(color="red")           # Use color=
cell.add_polygon(vertices, fill="blue")  # Use fill=
cell.add_line(start, end, color="green")  # Use color=
cell.add_ellipse(at=center, rx=10, ry=5, fill="yellow")  # Use fill=

# ✗ Wrong
cell.add_dot(fill="red")            # ERROR: use color=
cell.add_polygon(vertices, color="blue")  # ERROR: use fill=
```

## Color Manipulation Techniques

### Creating Gradients

Use RGB tuples to programmatically generate color gradients:

```python
def lerp_color(color1, color2, t):
    """Linear interpolation between two RGB colors."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return (r, g, b)

# Create a gradient from red to blue
start = (255, 0, 0)    # Red
end = (0, 0, 255)      # Blue

for i, cell in enumerate(scene.cells[:100]):
    t = i / 99
    color = lerp_color(start, end, t)
    cell.add_fill(color=color)
```

### Brightness-Based Shading

Use the `brightness` property to create adaptive color schemes:

```python
for cell in scene.cells:
    if cell.brightness > 0.8:
        # Very bright cells: dark accent
        cell.add_dot(at="center", radius=8, color="black")
    elif cell.brightness > 0.5:
        # Medium cells: colored accent
        cell.add_dot(at="center", radius=6, color=cell.color)
    else:
        # Dark cells: bright accent
        cell.add_dot(at="center", radius=4, color="white")
```

### Color Mixing Simulation

While PyFreeform doesn't have built-in alpha blending, you can simulate color mixing:

```python
def mix_colors(color1, color2, ratio=0.5):
    """Mix two RGB colors with a given ratio."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 * ratio + r2 * (1 - ratio))
    g = int(g1 * ratio + g2 * (1 - ratio))
    b = int(b1 * ratio + b2 * (1 - ratio))
    return (r, g, b)

base = (255, 100, 50)
overlay = (50, 100, 255)
mixed = mix_colors(base, overlay, 0.7)  # 70% base, 30% overlay
cell.add_fill(color=mixed)
```

### Converting Between Formats

Convert between formats as needed:

```python
def hex_to_rgb(hex_color):
    """Convert hex string to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

# Usage
rgb = hex_to_rgb("#ff6b35")     # (255, 107, 53)
hex_val = rgb_to_hex((255, 107, 53))  # "#ff6b35"
```

## Best Practices

!!! tip "Choosing Color Formats"
    - **Named colors:** Quick prototyping, maximum readability
    - **Hex colors:** Precise control, copying from design tools
    - **RGB tuples:** Programmatic generation, gradients, calculations

!!! tip "Generative Art Color Tips"
    1. **Limit your palette:** 3-5 colors often work better than dozens
    2. **Use color theory:** Complementary, analogous, or triadic color schemes
    3. **Consider contrast:** Ensure enough contrast for visibility
    4. **Test brightness:** Use `cell.brightness` to adapt to image data
    5. **Iterate:** Small color adjustments can dramatically change the feel

!!! warning "Common Mistakes"
    - Using `color=` instead of `fill=` for polygons/ellipses
    - Using `fill=` instead of `color=` for dots/lines
    - Forgetting the `#` prefix for hex colors
    - RGB values outside 0-255 range (will be clamped)

## Example: Cohesive Color Palette

```python
from pyfreeform import Scene

# Define a consistent palette
PALETTE = {
    "primary": "#2d3436",      # Dark gray
    "secondary": "#0984e3",    # Blue
    "accent": "#fdcb6e",       # Yellow
    "highlight": "#e17055",    # Coral
    "background": "#dfe6e9",   # Light gray
}

scene = Scene.from_image("image.jpg", grid_size=30)

# Apply background
for cell in scene.cells:
    if cell.brightness < 0.3:
        cell.add_fill(color=PALETTE["primary"])
    elif cell.brightness < 0.7:
        cell.add_fill(color=PALETTE["background"])

# Add accents
for cell in scene.cells[::3]:  # Every third cell
    r, g, b = cell.rgb
    if r > g and r > b:  # Reddish cells
        cell.add_dot(at="center", radius=5, color=PALETTE["highlight"])
    else:
        cell.add_dot(at="center", radius=5, color=PALETTE["secondary"])

scene.save("output.svg")
```

## See Also
- [Palettes](02-palettes.md)
- [Styling](../fundamentals/04-styling.md)
