
# Halftone Effects

Master the classic printing technique that has defined visual media for over a century. Halftone converts continuous-tone images into patterns of dots, creating the illusion of shades and tones through optical mixing.

## What is Halftone?

Halftone is a reprographic technique that simulates continuous-tone imagery through the use of dots, varying in size, shape, or spacing. Invented in the 1850s for printing photographs in newspapers and magazines, halftone remains a powerful aesthetic technique in modern digital art.

!!! info "How Halftone Works"
    Traditional printing can't reproduce continuous tones like a photograph - it can only print ink or no ink. Halftone solves this by creating the illusion of gray tones:

    - **Dark areas**: Large dots that merge together, covering most of the paper
    - **Light areas**: Small dots with more white space showing through
    - **Optical mixing**: Our eyes blend the dots and white space into perceived tones

    The closer you look, the more you see individual dots. From a distance, you see a continuous image.

### The Inverted Brightness Formula

The key to halftone is inverting brightness: `size = (1 - cell.brightness) * scale_factor`

- **Why invert?** In printing, dark areas need MORE ink (larger dots)
- **Bright pixel (brightness = 1.0)**: `(1 - 1.0) * 8 = 0` (tiny or no dot)
- **Dark pixel (brightness = 0.0)**: `(1 - 0.0) * 8 = 8` (large dot)

This creates the authentic halftone appearance where dots fill in the shadows.

## Basic Halftone

The classic newspaper halftone: black dots on white background with inverted brightness.

```python
scene = Scene.from_image("photo.jpg", grid_size=50)
scene.background = "white"

for cell in scene.grid:
    # Invert brightness
    size = (1 - cell.brightness) * 8
    cell.add_dot(radius=size, color="black")

scene.save("halftone.svg")
```

![Basic halftone effect with black dots on white](./_images/02-halftone-effects/01_basic_halftone.svg)

!!! tip "Background is Essential"
    Always set `scene.background = "white"` for traditional halftone. The white background is part of the illusion - it represents the unprinted paper showing through the dots.

## Color Halftone

Add vibrant color while maintaining the halftone aesthetic. This version uses original brightness (not inverted) for a different effect.

```python
for cell in scene.grid:
    size = cell.brightness * 6
    cell.add_dot(radius=size, color=cell.color)
```

![Color halftone with brightness-based sizing](./_images/02-halftone-effects/02_color_halftone.svg)

!!! note "Inverted vs Non-Inverted"
    This example uses `cell.brightness * 6` (NOT inverted) which creates:

    - Bright areas: Large colored dots
    - Dark areas: Small or no dots (background shows through)

    This is opposite to traditional halftone, but works well with colored backgrounds or when you want brightness to feel "additive" rather than subtractive.

### True Color Halftone (Inverted)

For authentic color halftone that behaves like printed color:

```python
scene.background = "white"

for cell in scene.grid:
    # Invert: dark areas get larger colored dots
    size = (1 - cell.brightness) * 7
    cell.add_dot(radius=size, color=cell.color)
```

## CMYK Style

Simulate four-color printing by layering offset dots in cyan, magenta, yellow, and black. This recreates the rosette patterns seen in printed magazines.

```python
offsets = [(0, 0), (2, 1), (1, 2), (2, 2)]
cmyk = ["cyan", "magenta", "yellow", "black"]

for i, (color, offset) in enumerate(zip(cmyk, offsets)):
    for cell in scene.grid:
        size = (1 - cell.brightness) * 5
        cell.add_dot(radius=size, color=color, dx=offset[0], dy=offset[1])
```

![CMYK-style halftone with offset color channels](./_images/02-halftone-effects/03_cmyk_style.svg)

!!! info "CMYK Printing Explained"
    Professional color printing uses four ink colors:

    - **C**yan: Blue-green ink
    - **M**agenta: Pink-red ink
    - **Y**ellow: Yellow ink
    - **K**ey (Black): Black ink for depth and contrast

    Each color is printed as a separate halftone pattern at slightly different angles. Where dots overlap, they create new colors (cyan + magenta = blue, cyan + yellow = green, etc.). The offset positions in this recipe simulate the angular rotation used in real printing.

### Advanced CMYK with Transparency

```python
scene.background = "white"

# More pronounced offsets for stronger effect
offsets = [(0, 0), (3, 0), (0, 3), (3, 3)]
cmyk = ["cyan", "magenta", "yellow", "black"]

for color, offset in zip(cmyk, offsets):
    for cell in scene.grid:
        size = (1 - cell.brightness) * 6
        cell.add_dot(
            radius=size,
            color=color,
            opacity=0.7,  # Transparency for color mixing
            dx=offset[0],
            dy=offset[1]
        )
```

### Screen Angles Simulation

In real CMYK printing, each color is rotated at different angles (15°, 45°, 0°, 75°) to prevent moiré patterns:

```python
import math

angles = [15, 45, 0, 75]  # Standard CMYK screen angles
cmyk = ["cyan", "magenta", "yellow", "black"]

for color, angle in zip(cmyk, angles):
    for cell in scene.grid:
        # Calculate rotated offset
        rad = math.radians(angle)
        dx = math.cos(rad) * 2
        dy = math.sin(rad) * 2

        size = (1 - cell.brightness) * 5
        cell.add_dot(radius=size, color=color, dx=dx, dy=dy, opacity=0.6)
```

## Threshold Halftone

Binary halftone: dots are either present or absent, creating high-contrast graphic effects.

```python
for cell in scene.grid:
    if cell.brightness < 0.5:
        cell.add_dot(radius=4, color="black")
```

![Threshold halftone with binary dot placement](./_images/02-halftone-effects/04_threshold_halftone.svg)

!!! note "Binary vs Variable Halftone"
    Traditional variable halftone varies dot size. Threshold halftone varies dot density (presence/absence) instead:

    - **Variable**: Same number of dots everywhere, but different sizes
    - **Threshold**: Different number of dots, but uniform sizes

    Threshold halftone creates a sharper, more graphic look - excellent for logos, text, and high-contrast imagery.

### Multi-Level Threshold

Create posterized effects with multiple dot sizes:

```python
for cell in scene.grid:
    if cell.brightness < 0.25:
        cell.add_dot(radius=6, color="black")      # Darkest areas
    elif cell.brightness < 0.5:
        cell.add_dot(radius=4, color="black")      # Dark midtones
    elif cell.brightness < 0.75:
        cell.add_dot(radius=2, color="darkgray")   # Light midtones
    # Brightest areas (>0.75) get no dots
```

## Dual Color

Combine two colors with brightness-based color selection for dramatic contrast.

```python
for cell in scene.grid:
    size = cell.brightness * 6
    color = "white" if cell.brightness > 0.5 else "black"
    cell.add_dot(radius=size, color=color)
```

![Dual color halftone with black and white dots](./_images/02-halftone-effects/05_dual_color.svg)

### Artistic Duotone

Create stylized duotone effects with custom color pairs:

```python
scene.background = "#1a1a1a"  # Dark background

for cell in scene.grid:
    # Inverted sizing
    size = (1 - cell.brightness) * 7

    # Split at midpoint
    if cell.brightness > 0.5:
        color = "#ff6b35"  # Warm orange for highlights
    else:
        color = "#004e89"  # Cool blue for shadows

    cell.add_dot(radius=size, color=color)
```

!!! tip "Choosing Duotone Colors"
    Effective duotone color pairs have strong contrast:

    - **Warm/Cool**: Orange + Blue, Red + Cyan
    - **Light/Dark**: Yellow + Purple, White + Black
    - **Complementary**: Red + Green, Blue + Orange

    Test your colors at [Adobe Color](https://color.adobe.com) or similar tools.

## Newspaper Style

Authentic newsprint aesthetic with high grid density and inverted brightness.

```python
scene.background = "white"
for cell in scene.grid:
    size = (1 - cell.brightness) * 7
    cell.add_dot(radius=size, color="black")
```

![Newspaper-style halftone with black dots on white background](./_images/02-halftone-effects/06_newspaper_style.svg)

!!! info "Newsprint Characteristics"
    Traditional newspaper halftone has distinct features:

    - **High frequency**: Dense grid (85-100 lines per inch historically, we use grid_size 50-80)
    - **Black and white only**: No color, pure monochrome
    - **Inverted brightness**: Dark areas have large merged dots
    - **White background**: Represents the paper

### Enhanced Newspaper Effect

Add ink spread and aging effects:

```python
scene = Scene.from_image("photo.jpg", grid_size=60)
scene.background = "#f5f5dc"  # Aged paper color

for cell in scene.grid:
    # Slightly larger dots to simulate ink spread
    size = (1 - cell.brightness) * 8

    # Add slight randomness to simulate printing imperfection
    import random
    size += random.uniform(-0.3, 0.3)
    size = max(0, size)  # Don't go negative

    cell.add_dot(radius=size, color="#1a1a1a")  # Not pure black, slightly gray
```

## Gradient Halftone

Vary the halftone effect spatially across the image, creating gradient transitions.

```python
for cell in scene.grid:
    t = cell.col / scene.grid.cols
    size = (1 - cell.brightness) * (2 + t * 6)
    cell.add_dot(radius=size, color="black")
```

![Gradient halftone with dot size varying across columns](./_images/02-halftone-effects/07_gradient_halftone.svg)

!!! note "Understanding the Gradient Formula"
    The formula `size = (1 - cell.brightness) * (2 + t * 6)` breaks down as:

    - `t = cell.col / scene.grid.cols` creates a 0→1 gradient left to right
    - `2 + t * 6` creates a multiplier ranging from 2 (left) to 8 (right)
    - Left side: smaller maximum dot size (subtle halftone)
    - Right side: larger maximum dot size (pronounced halftone)

### Gradient Variations

```python
# Vertical gradient (top to bottom)
t = cell.row / scene.grid.rows
size = (1 - cell.brightness) * (3 + t * 7)

# Radial gradient (center outward)
center_row = scene.grid.rows / 2
center_col = scene.grid.cols / 2
dr = cell.row - center_row
dc = cell.col - center_col
distance = (dr*dr + dc*dc) ** 0.5
max_distance = ((center_row**2) + (center_col**2)) ** 0.5
t = distance / max_distance
size = (1 - cell.brightness) * (2 + t * 8)

# Diagonal gradient
t = (cell.row + cell.col) / (scene.grid.rows + scene.grid.cols)
size = (1 - cell.brightness) * (1 + t * 9)
```

## Overlapping Halftone

Layer multiple halftone passes with offsets and transparency for chromatic aberration effects.

```python
for cell in scene.grid:
    size = (1 - cell.brightness) * 8
    cell.add_dot(radius=size, color="black", opacity=0.5)
    cell.add_dot(radius=size * 0.6, color="red", opacity=0.5, dx=2, dy=2)
```

![Overlapping halftone with multiple offset dot layers](./_images/02-halftone-effects/08_overlapping_halftone.svg)

### Chromatic Aberration Halftone

Simulate lens chromatic aberration with RGB channel separation:

```python
scene.background = "white"

channels = [
    ("red", -2, 0),      # Red shifted left
    ("green", 0, 0),      # Green centered
    ("blue", 2, 0)        # Blue shifted right
]

for color, dx, dy in channels:
    for cell in scene.grid:
        size = (1 - cell.brightness) * 6
        cell.add_dot(
            radius=size,
            color=color,
            opacity=0.4,
            dx=dx,
            dy=dy
        )
```

---

## Parameter Tuning Guide

### Size Range Selection

The multiplier in `(1 - cell.brightness) * X` controls the maximum dot size:

| Multiplier | Max Radius | Effect |
|------------|------------|---------|
| 3-4        | 3-4 px     | Subtle, fine halftone (high grid needed) |
| 5-7        | 5-7 px     | Standard newspaper halftone |
| 8-10       | 8-10 px    | Bold, graphic halftone |
| 12-15      | 12-15 px   | Overlapping dots, heavy ink effect |

!!! warning "Dot Overlap"
    When `max_radius > cell_width / 2`, dots will overlap significantly. This can create interesting effects but may make the image harder to read. For grid_size=50 and canvas_width=1000, cell_width=20, so keep radius below 10 for minimal overlap.

### Grid Size for Halftone

Different from dot art, halftone works best with denser grids:

- **Grid 30-40**: Large, chunky halftone (retro/pop art style)
- **Grid 50-60**: Classic newspaper halftone (recommended)
- **Grid 70-90**: Fine halftone (magazine quality)
- **Grid 100+**: Ultra-fine halftone (rarely needed, slow)

### Color vs Monochrome

```python
# Pure monochrome (most authentic)
scene.background = "white"
cell.add_dot(radius=size, color="black")

# Tinted monochrome (vintage feel)
scene.background = "#f5e6d3"  # Sepia paper
cell.add_dot(radius=size, color="#3d2817")  # Sepia ink

# Color halftone (modern/artistic)
cell.add_dot(radius=size, color=cell.color)

# Duotone halftone (graphic/poster style)
color = "#ff0080" if cell.brightness > 0.5 else "#00ffff"
cell.add_dot(radius=size, color=color)
```

---

## Tips and Best Practices

### Choosing the Right Halftone Approach

**Use traditional inverted halftone when:**
- Creating authentic retro/vintage aesthetics
- Simulating newspaper or magazine printing
- Working with black and white images
- You want dark areas to feel "filled in"

**Use non-inverted (brightness-based) halftone when:**
- Creating modern, bright, colorful art
- Working with colored backgrounds
- You want an additive light feel (bright = large)
- Simulating pointillist painting rather than printing

### Image Preparation

Best images for halftone:

1. **High contrast**: Strong blacks and whites
2. **Clear subjects**: Defined shapes, not too busy
3. **Medium complexity**: Some detail but not overwhelming
4. **Good composition**: Clear focal point

Pre-process your images:

```python
# Recommended preprocessing in external software:
# 1. Increase contrast by 20-30%
# 2. Sharpen slightly (unsharp mask)
# 3. Convert to black and white for classic halftone
# 4. Crop to square aspect ratio
```

### Avoiding Moiré Patterns

Moiré (unwanted interference patterns) can occur in halftone. Prevent it by:

1. **Vary grid size**: Don't use grid sizes that are exact multiples of image dimensions
2. **Add slight randomness**: Jitter dot positions slightly
3. **Use proper screen angles**: For CMYK, use 15°/45°/0°/75° angles

```python
# Anti-moiré with position jitter
import random

for cell in scene.grid:
    size = (1 - cell.brightness) * 6
    jitter_x = random.uniform(-0.5, 0.5)
    jitter_y = random.uniform(-0.5, 0.5)
    cell.add_dot(radius=size, color="black", dx=jitter_x, dy=jitter_y)
```

### Performance Optimization

```python
# Skip very small dots (invisible anyway)
for cell in scene.grid:
    size = (1 - cell.brightness) * 7
    if size > 0.5:  # Only draw dots with radius > 0.5
        cell.add_dot(radius=size, color="black")

# Use constant style for faster rendering
from pyfreeform import DotStyle
style = DotStyle(color="black", radius=5)
for cell in scene.grid:
    if (1 - cell.brightness) > 0.3:  # Threshold for presence
        cell.add_dot(style=style)
```

---

## Complete Example: Magazine Cover Effect

```python
from pyfreeform import Scene, Palette

# High-density grid for magazine quality
scene = Scene.from_image("portrait.jpg", grid_size=70)
scene.background = "white"

for cell in scene.grid:
    # Inverted brightness for authentic halftone
    size = (1 - cell.brightness) * 6

    # Color mapping for vibrant magazine aesthetic
    if cell.brightness > 0.8:
        # Highlights: keep white (no dot)
        if size > 0.5:
            cell.add_dot(radius=size * 0.3, color="#ffcccc")
    elif cell.brightness > 0.5:
        # Midtones: use original color
        cell.add_dot(radius=size, color=cell.color)
    else:
        # Shadows: enrich with darker version
        from pyfreeform import Color
        dark_color = Color.darken(cell.color, 0.3)
        cell.add_dot(radius=size, color=dark_color)

scene.save("magazine_halftone.svg")
```

---

## See Also
- [Dot Art Recipe](01-dot-art-from-images.md)
- [Image to Art Guide](../getting-started/03-image-to-art.md)
- [Color Basics](../color-and-style/01-color-system.md)
