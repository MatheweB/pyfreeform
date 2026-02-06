
# Dot Art from Images

Transform any photo into stunning dot art with PyFreeform. This recipe explores various techniques for converting images into dots, from simple uniform grids to sophisticated variable-sizing algorithms.

## What is Dot Art?

Dot art (also called stippling or pointillism in traditional art) is a technique where an image is composed entirely of dots. The density, size, color, and placement of dots create the illusion of continuous tones and shapes. In PyFreeform, we sample colors and brightness values from images, then use those values to control dot properties.

!!! info "Why Dot Art Works"
    Our visual system naturally interpolates between discrete elements. When dots are placed close enough together, our brain "fills in" the gaps, creating the perception of continuous forms. This technique has been used by artists from Georges Seurat to modern digital artists.

## Basic Pattern

The simplest dot art approach: place uniform dots on a grid, using the original image colors.

```python
scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    cell.add_dot(color=cell.color, radius=4)

scene.save("dot_art.svg")
```

![Basic dot art pattern with uniform dots on grid](./_images/01-dot-art-from-images/01_basic_pattern.svg)

!!! tip "Choosing Grid Size"
    Start with `grid_size=40` for balanced detail and performance. Increase to 60-80 for high-detail artwork, or decrease to 20-30 for more abstract, impressionistic results. Remember: higher grid sizes create exponentially more dots (40x40 = 1,600 cells, 80x80 = 6,400 cells).

## Variable Sizing

The most powerful dot art technique: vary dot size based on brightness to create depth and dimension.

```python
for cell in scene.grid:
    size = 2 + cell.brightness * 8
    cell.add_dot(radius=size, color=cell.color)
```

![Dots with size varying based on brightness](./_images/01-dot-art-from-images/02_variable_sizing.svg)

!!! note "Understanding the Formula"
    The formula `size = 2 + cell.brightness * 8` creates dots ranging from radius 2 (darkest) to radius 10 (brightest). Breaking it down:

    - `cell.brightness` ranges from 0.0 (black) to 1.0 (white)
    - `cell.brightness * 8` scales this to 0-8
    - Adding 2 ensures minimum visibility: `2 + 0 = 2` (dark) to `2 + 8 = 10` (bright)

### When to Use Variable Sizing

- **Photographic images**: Creates natural-looking depth and dimensionality
- **Portraits**: Bright areas (highlights) become larger, creating volume
- **High contrast scenes**: Emphasizes the contrast between light and shadow

### Parameter Tuning

Adjust the formula to control the effect:

```python
# Subtle variation (radius 3-7)
size = 3 + cell.brightness * 4

# Extreme variation (radius 1-15)
size = 1 + cell.brightness * 14

# Compressed range (radius 5-8)
size = 5 + cell.brightness * 3

# Logarithmic scaling (more gradual)
import math
size = 2 + math.log(1 + cell.brightness) * 5
```

!!! tip "Avoiding Dot Overlap"
    If dots overlap too much, reduce the maximum size. For a grid of 40x40, keep radius below 10. For 60x60, keep below 7. Formula: `max_radius ≈ (canvas_width / grid_size) / 2`

## Threshold Effect

Create posterized, graphic effects by quantizing brightness into discrete levels.

```python
colors = Palette.midnight()

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(radius=6, color=colors.primary)
    elif cell.brightness > 0.4:
        cell.add_dot(radius=4, color=colors.secondary)
```

![Threshold-based dot rendering with two brightness levels](./_images/01-dot-art-from-images/03_threshold_effect.svg)

!!! info "Thresholding Explained"
    Thresholding converts continuous brightness values into discrete levels. This creates a posterized, screen-print aesthetic. In this example:

    - Brightness > 0.7 (bright highlights): Large primary dots
    - Brightness 0.4-0.7 (midtones): Medium secondary dots
    - Brightness < 0.4 (shadows): No dots (transparent)

### Choosing Threshold Values

The threshold values determine which parts of the image get dots:

```python
# High threshold (only brightest areas)
if cell.brightness > 0.8:
    cell.add_dot(radius=5, color="white")

# Low threshold (most areas get dots)
if cell.brightness > 0.2:
    cell.add_dot(radius=4, color=cell.color)

# Multiple levels (4-tone effect)
if cell.brightness > 0.75:
    cell.add_dot(radius=7, color="white")
elif cell.brightness > 0.5:
    cell.add_dot(radius=5, color="lightgray")
elif cell.brightness > 0.25:
    cell.add_dot(radius=3, color="darkgray")
else:
    cell.add_dot(radius=2, color="black")
```

!!! tip "Finding Good Thresholds"
    Most images work well with thresholds at 0.3, 0.5, and 0.7 (thirds). For high-key images (bright overall), shift lower: 0.2, 0.4, 0.6. For low-key images (dark overall), shift higher: 0.4, 0.6, 0.8.

## Color Dots

Preserve the original image colors for vibrant, true-to-source artwork.

```python
for cell in scene.grid:
    cell.add_dot(radius=4, color=cell.color)
```

![Color dots preserving original image colors](./_images/01-dot-art-from-images/04_color_dots.svg)

!!! note "Color vs Brightness"
    PyFreeform provides two key cell properties:

    - `cell.color`: The average color in this cell (as hex string like "#ff5533")
    - `cell.brightness`: The perceived luminance (0.0 to 1.0)

    You can use `cell.color` for vibrant, colorful dots, or use `cell.brightness` to control sizing while choosing your own color palette.

## Sparse Pattern

Create minimalist compositions by only placing dots in certain brightness ranges.

```python
for cell in scene.grid:
    if cell.brightness > 0.5:
        cell.add_dot(radius=3, color=cell.color)
```

![Sparse dot pattern with only bright areas rendered](./_images/01-dot-art-from-images/05_sparse_pattern.svg)

### Use Cases for Sparse Patterns

- **High-key images**: Only render highlights, let darkness be absence
- **Silhouettes**: Filter out backgrounds by brightness
- **Minimalist art**: Less is more, focus on key features

### Advanced Filtering

Combine multiple conditions for sophisticated control:

```python
# Only medium-bright areas (midtones only)
if 0.4 < cell.brightness < 0.7:
    cell.add_dot(radius=4, color=cell.color)

# Checkerboard sparsity
if cell.brightness > 0.5 and (cell.row + cell.col) % 2 == 0:
    cell.add_dot(radius=5, color=cell.color)

# Random sparsity
import random
if cell.brightness > 0.3 and random.random() > 0.5:
    cell.add_dot(radius=4, color=cell.color)

# Edge detection (brightness differs from neighbors)
if cell.right and abs(cell.brightness - cell.right.brightness) > 0.2:
    cell.add_dot(radius=3, color="black")
```

!!! tip "Performance Benefit"
    Sparse patterns render faster because fewer dots are drawn. If generating large SVGs (80x80 grids or more), sparse patterns can reduce file size by 50-90%.

## Inverted Brightness

Flip the relationship: make dark areas large and bright areas small, creating a halftone-like negative effect.

```python
for cell in scene.grid:
    size = (1 - cell.brightness) * 8
    cell.add_dot(radius=size, color=cell.color)
```

![Inverted brightness mapping where dark areas get larger dots](./_images/01-dot-art-from-images/06_inverted_brightness.svg)

!!! info "Why Invert?"
    Inverting brightness is essential for halftone effects on white backgrounds. In traditional halftone printing, dark areas need more ink (larger dots), and light areas need less ink (smaller dots). The formula `(1 - cell.brightness)` converts:

    - Bright pixels (brightness = 1.0) → small dots (1 - 1.0 = 0.0)
    - Dark pixels (brightness = 0.0) → large dots (1 - 0.0 = 1.0)

### Inverted with Color Mapping

```python
# Dark areas = large colored dots
# Bright areas = small white dots
for cell in scene.grid:
    if cell.brightness < 0.5:
        # Dark region: use image color
        size = (1 - cell.brightness) * 8
        cell.add_dot(radius=size, color=cell.color)
    else:
        # Bright region: use white
        size = (1 - cell.brightness) * 6
        cell.add_dot(radius=size, color="white")
```

## Dual Layer

Layer multiple dot passes for richer, more complex compositions.

```python
for cell in scene.grid:
    # Background layer
    cell.add_dot(radius=6, color=cell.color, z_index=0)
    # Foreground accent
    if cell.brightness > 0.6:
        cell.add_dot(radius=2, color="white", z_index=10)
```

![Dual layer dot art with background and foreground dots](./_images/01-dot-art-from-images/07_dual_layer.svg)

!!! tip "Z-Index Layering"
    The `z_index` parameter controls drawing order. Lower values (0, 1, 2) draw first (background), higher values (10, 20) draw last (foreground). Always use clear separation (0 and 10, not 0 and 1) to make layering intentions obvious.

### Advanced Layering Techniques

```python
# Triple layer: shadow, base, highlight
for cell in scene.grid:
    # Shadow layer (darkest areas)
    if cell.brightness < 0.3:
        cell.add_dot(radius=8, color="black", z_index=0)

    # Base layer (all areas)
    cell.add_dot(radius=5, color=cell.color, z_index=5)

    # Highlight layer (brightest areas)
    if cell.brightness > 0.7:
        cell.add_dot(radius=3, color="white", z_index=10)

# Overlapping semi-transparent layers
for cell in scene.grid:
    cell.add_dot(radius=6, color="cyan", opacity=0.5, z_index=0)
    cell.add_dot(radius=6, color="magenta", opacity=0.5, z_index=1, dx=2, dy=2)
    cell.add_dot(radius=6, color="yellow", opacity=0.5, z_index=2, dx=4, dy=4)
```

!!! note "Performance Consideration"
    Each additional layer multiplies rendering time. Two-layer effects are fast, three-layer are acceptable, but four or more layers may slow SVG rendering in browsers.

## Checkerboard Threshold

Combine spatial patterns with brightness filtering for unique textures.

```python
for cell in scene.grid:
    if (cell.row + cell.col) % 2 == 0 and cell.brightness > 0.4:
        cell.add_dot(radius=5, color=cell.color)
```

![Checkerboard threshold pattern combining grid position and brightness](./_images/01-dot-art-from-images/08_checkerboard_threshold.svg)

### Pattern-Based Filtering

```python
# Vertical stripes
if cell.col % 2 == 0:
    cell.add_dot(radius=4, color=cell.color)

# Horizontal stripes
if cell.row % 2 == 0:
    cell.add_dot(radius=4, color=cell.color)

# Every third cell
if cell.col % 3 == 0:
    cell.add_dot(radius=5, color=cell.color)

# Diagonal pattern
if (cell.row - cell.col) % 3 == 0:
    cell.add_dot(radius=4, color=cell.color)
```

---

## Choosing Good Source Images

Not all images work equally well for dot art. Here's what to look for:

### Best Image Characteristics

1. **High contrast**: Strong difference between light and dark areas
2. **Clear subjects**: Recognizable shapes and forms
3. **Medium complexity**: Not too busy, not too simple
4. **Good resolution**: At least 800x800 pixels for best sampling
5. **Focused composition**: Clear focal point, not too much background clutter

### Image Types That Work Well

- Portraits (especially high-contrast lighting)
- Architecture with strong geometric forms
- Nature photos with clear subjects
- Abstract patterns with defined shapes
- High-contrast black and white photos

### Image Types to Avoid

- Very low contrast (washed out)
- Extremely busy scenes (too much detail)
- Low resolution or pixelated images
- Pure gradients (no structure)

!!! tip "Pre-Processing Images"
    Before using an image with PyFreeform, consider:

    - Increasing contrast in photo editing software
    - Converting to black and white for clarity
    - Cropping to focus on the main subject
    - Resizing to square aspect ratio (1:1)

---

## Performance Considerations

### Grid Size Impact

| Grid Size | Cells  | Render Time | Use Case |
|-----------|--------|-------------|----------|
| 20x20     | 400    | < 1 sec     | Quick tests, abstract art |
| 40x40     | 1,600  | 1-2 sec     | Balanced detail and speed |
| 60x60     | 3,600  | 3-5 sec     | High detail artwork |
| 80x80     | 6,400  | 8-12 sec    | Maximum detail (slow) |
| 100x100   | 10,000 | 20-30 sec   | Professional quality (very slow) |

!!! warning "Large Grids"
    Grids above 80x80 create very large SVG files (5-10 MB) that may be slow to open in browsers or editing software. For web use, stick to 60x60 or lower.

### Optimization Strategies

```python
# Strategy 1: Sparse rendering (only some cells)
for cell in scene.grid:
    if cell.brightness > 0.3:  # Skip 30% of cells
        cell.add_dot(radius=4, color=cell.color)

# Strategy 2: Simpler dots (no gradients or effects)
for cell in scene.grid:
    cell.add_dot(radius=4, color=cell.color)  # Simple, flat color

# Strategy 3: Lower grid size for testing
scene = Scene.from_image("photo.jpg", grid_size=30)  # Test at 30
# ... develop your effect ...
# scene = Scene.from_image("photo.jpg", grid_size=60)  # Final render at 60

# Strategy 4: Use DotStyle for consistent rendering
from pyfreeform import DotStyle
style = DotStyle(color="black", radius=4)
for cell in scene.grid:
    cell.add_dot(style=style)  # Faster than individual parameters
```

---

## Complete Example: Portrait Dot Art

```python
from pyfreeform import Scene, Palette

# Load portrait photo
scene = Scene.from_image("portrait.jpg", grid_size=50)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    # Variable sizing based on brightness
    size = 1 + cell.brightness * 6

    # Color mapping: preserve skin tones in midtones
    if 0.3 < cell.brightness < 0.7:
        color = cell.color  # Use original color
    elif cell.brightness >= 0.7:
        color = colors.light  # Highlights
    else:
        color = colors.dark  # Shadows

    cell.add_dot(radius=size, color=color)

    # Add highlight accent in very bright areas
    if cell.brightness > 0.85:
        cell.add_dot(radius=2, color="white", z_index=10)

scene.save("portrait_dot_art.svg")
```

---

## Tips and Best Practices

### Radius Selection

- **Small uniform dots (2-4)**: Clean, precise, technical aesthetic
- **Variable dots (1-10)**: Natural, photographic look with depth
- **Large dots (8-15)**: Bold, abstract, poster-like style
- **Tiny dots (0.5-2)**: Stippling effect, requires high grid size (80+)

### Color Strategies

```python
# Strategy 1: Monochrome with brightness
color = f"rgb({int(b*255)}, {int(b*255)}, {int(b*255)})"
cell.add_dot(radius=4, color=color)

# Strategy 2: Duotone (two color interpolation)
from pyfreeform import Color
c = Color.interpolate("#ff0000", "#0000ff", cell.brightness)
cell.add_dot(radius=4, color=c)

# Strategy 3: Palette mapping
colors = Palette.ocean()
if cell.brightness > 0.6:
    color = colors.light
elif cell.brightness > 0.3:
    color = colors.primary
else:
    color = colors.dark
cell.add_dot(radius=4, color=color)
```

### Combining Techniques

```python
# Variable sizing + threshold + layering
for cell in scene.grid:
    # Base layer: variable sized dots for all cells
    size = 2 + cell.brightness * 6
    cell.add_dot(radius=size, color=cell.color, z_index=0)

    # Accent layer: small dots only in highlights
    if cell.brightness > 0.75:
        cell.add_dot(radius=2, color="white", z_index=10)

    # Pattern layer: checkerboard in shadows
    if cell.brightness < 0.3 and (cell.row + cell.col) % 2 == 0:
        cell.add_dot(radius=4, color="black", z_index=5)
```

!!! tip "Iterative Development"
    Start simple, then add complexity:

    1. Begin with basic uniform dots to verify the image works
    2. Add variable sizing to create depth
    3. Introduce color mapping or thresholds
    4. Add layering for accents
    5. Fine-tune parameters (sizes, thresholds, colors)

---

## See Also
- [Quick Start Example](../examples/beginner/quick-start.md)
- [Image to Art](../getting-started/03-image-to-art.md)
- [Halftone Effects Recipe](02-halftone-effects.md)
- [Color and Style Guide](../color-and-style/01-color-system.md)
