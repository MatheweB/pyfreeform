
# Image to Art

Transform any photo or image into stunning generative artwork. This guide shows you the complete workflow from loading an image to creating custom visual styles.

---

## The Workflow

Creating art from images in PyFreeform follows this pattern:

1. **Load** - Import image data into a scene
2. **Sample** - Access color and brightness from cells
3. **Transform** - Use data to drive visual properties
4. **Render** - Save as SVG

Let's explore each step in detail.

---

## Step 1: Load Your Image

### Basic Loading

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)
```

This creates:
- A scene matching your image dimensions
- A 40×40 grid (1,600 cells)
- Each cell loaded with color and brightness data

### Parameters Explained

```python
Scene.from_image(
    source="path/to/image.jpg",  # Image file path
    grid_size=40,                # Grid dimensions (square)
    cell_size=10,                # Cell size in pixels (optional)
    background=None              # Background color (optional)
)
```

**`grid_size`**: Controls detail vs. performance
- `20` = 400 cells, very abstract
- `40` = 1,600 cells, good balance (default)
- `60` = 3,600 cells, high detail
- `100` = 10,000 cells, very detailed (slower)

**`cell_size`**: Overrides automatic sizing
- If not specified, calculated from image dimensions and grid_size
- Larger values = more spacing between dots/elements

---

## Step 2: Access Image Data

Each cell provides typed properties for image data:

### Brightness

```python
cell.brightness  # Range: 0.0 to 1.0
```

- `0.0` = Pure black (darkest)
- `0.5` = Medium gray
- `1.0` = Pure white (brightest)

Automatically normalized from 0-255 range.

### Color

```python
cell.color  # Hex string: "#ff5733"
cell.rgb    # Tuple: (255, 87, 51)
```

The average color of the image pixels in that cell's region.

### Usage Examples

```python
for cell in scene.grid:
    # Brightness thresholds
    if cell.brightness > 0.8:
        print("Very bright")
    elif cell.brightness > 0.5:
        print("Medium")
    else:
        print("Dark")

    # Direct color usage
    cell.add_dot(color=cell.color)  # Use image color

    # RGB manipulation
    r, g, b = cell.rgb
    adjusted_color = (r, g // 2, b)  # Darken green channel
```

---

## Step 3: Transform Data into Art

Now comes the creative part! Use the data to drive your artistic decisions.

### Size-Based on Brightness

Make elements larger in brighter areas:

```python
for cell in scene.grid:
    # Map brightness (0-1) to radius (2-10)
    radius = 2 + cell.brightness * 8
    cell.add_dot(radius=radius, color=cell.color)
```

![Size Based on Brightness](./_images/03-image-to-art/01-size-based-brightness.svg)

### Conditional Rendering

Only draw in certain areas:

```python
for cell in scene.grid:
    # Only bright areas
    if cell.brightness > 0.6:
        cell.add_dot(radius=8, color=cell.color)

    # Only dark areas
    elif cell.brightness < 0.3:
        cell.add_border(color="black", width=1)
```

![Conditional Rendering - Bright Areas](./_images/03-image-to-art/02-conditional-bright-only.svg)
![Conditional Rendering - Dark Areas](./_images/03-image-to-art/03-conditional-dark-only.svg)
![Conditional Rendering - Combined](./_images/03-image-to-art/04-conditional-combined.svg)

### Different Shapes by Brightness

```python
from pyfreeform import Polygon

for cell in scene.grid:
    if cell.brightness > 0.7:
        # Bright: Hexagons
        cell.add_polygon(Polygon.hexagon(), fill=cell.color)

    elif cell.brightness > 0.4:
        # Medium: Curves
        curve = cell.add_curve(curvature=0.5, color=cell.color)
        cell.add_dot(along=curve, t=cell.brightness, radius=3)

    else:
        # Dark: Small dots
        cell.add_dot(radius=2, color=cell.color)
```

![Different Shapes by Brightness](./_images/03-image-to-art/05-shapes-by-brightness.svg)

### Position Along Paths

Use brightness to control position along curves or lines:

```python
for cell in scene.grid:
    # Create a diagonal line
    line = cell.add_diagonal(start="bottom_left", end="top_right", color="gray", width=0.5)

    # Position dot along line based on brightness
    # 0.0 = bottom-left, 1.0 = top-right
    cell.add_dot(
        along=line,
        t=cell.brightness,
        radius=4,
        color=cell.color
    )
```

![Position Along Diagonal](./_images/03-image-to-art/06-position-along-diagonal.svg)
![Position Along Curves](./_images/03-image-to-art/07-position-along-curves.svg)

---

## Complete Examples

### Example 1: Halftone Effect

Create a classic halftone pattern:

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=50)
scene.background = "white"

for cell in scene.grid:
    # Invert brightness for halftone effect
    size = (1 - cell.brightness) * 8
    cell.add_dot(radius=size, color="black")

scene.save("halftone.svg")
```

![Halftone Effect - Black and White](./_images/03-image-to-art/08-halftone-effect.svg)
![Halftone Effect - Colored](./_images/03-image-to-art/09-halftone-colored.svg)

### Example 2: Color Threshold

Artistic color separation:

```python
from pyfreeform import Scene, Palette

scene = Scene.from_image("photo.jpg", grid_size=40)
colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.7:
        cell.add_dot(radius=6, color=colors.primary)
    elif cell.brightness > 0.4:
        cell.add_dot(radius=4, color=colors.secondary)
    elif cell.brightness > 0.2:
        cell.add_dot(radius=2, color=colors.accent)

scene.save("threshold.svg")
```

![Color Threshold - Midnight Palette](./_images/03-image-to-art/10-color-threshold.svg)
![Color Threshold - Ocean Palette](./_images/03-image-to-art/11-color-threshold-ocean.svg)

### Example 3: Flow Fields

Create flowing curves based on image:

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=30)

for cell in scene.grid:
    # Curvature driven by brightness
    curvature = (cell.brightness - 0.5) * 2  # Range: -1 to 1

    curve = cell.add_curve(
        start="left",
        end="right",
        curvature=curvature,
        color=cell.color,
        width=2
    )

    # Add dots along curves
    for t in [0.25, 0.5, 0.75]:
        cell.add_dot(
            along=curve,
            t=t,
            radius=2,
            color=cell.color
        )

scene.save("flow.svg")
```

![Flow Fields - Basic](./_images/03-image-to-art/12-flow-fields.svg)
![Flow Fields - Varied](./_images/03-image-to-art/13-flow-fields-varied.svg)

---

## Tips and Techniques

### Choose the Right Grid Size

**For portraits**: 30-50 works well
**For landscapes**: 40-60 for detail
**For abstract**: 20-30 for bold shapes
**For complex scenes**: 60-100 for fine detail

### Background Matters

```python
scene.background = "white"  # Clean, minimalist
scene.background = "black"  # Dramatic, bold
scene.background = colors.background  # Palette integration
scene.background = None     # Transparent (default)
```

![Background - White](./_images/03-image-to-art/14-background-white.svg)
![Background - Black](./_images/03-image-to-art/15-background-black.svg)
![Background - Palette](./_images/03-image-to-art/16-background-palette.svg)

### Use Palettes for Consistency

Instead of using image colors directly:

```python
from pyfreeform import Palette

colors = Palette.ocean()
scene.background = colors.background

for cell in scene.grid:
    # Map brightness to palette colors
    if cell.brightness > 0.7:
        color = colors.primary
    elif cell.brightness > 0.4:
        color = colors.secondary
    else:
        color = colors.accent

    cell.add_dot(color=color, radius=5)
```

![Palette Mapping - Ocean](./_images/03-image-to-art/17-palette-mapping.svg)
![Palette Mapping - Forest](./_images/03-image-to-art/18-palette-forest.svg)

### Layer for Depth

Use multiple layers (z-index) for complex compositions:

```python
Z_BACKGROUND = 0
Z_SHAPES = 1
Z_ACCENTS = 2

for cell in scene.grid:
    # Background layer
    cell.add_fill(color=cell.color, z_index=Z_BACKGROUND)

    # Shape layer
    if cell.brightness > 0.5:
        cell.add_ellipse(
            rx=8, ry=6,
            fill="white",
            z_index=Z_SHAPES
        )

    # Accent layer
    cell.add_dot(
        radius=2,
        color="black",
        z_index=Z_ACCENTS
    )
```

![Layering - Basic](./_images/03-image-to-art/19-layering-basic.svg)
![Layering - Complex](./_images/03-image-to-art/20-layering-complex.svg)

---

## Image Formats

PyFreeform supports all formats that Pillow can load:

- **JPEG/JPG** - Most common, good for photos
- **PNG** - Supports transparency
- **GIF** - Animated frames (first frame used)
- **BMP** - Uncompressed
- **TIFF** - High quality

The library automatically handles color space conversions and normalization.

---

## Common Patterns

### Inverting Brightness

For light-on-dark effects:

```python
inverted = 1 - cell.brightness
```

![Inverted Brightness](./_images/03-image-to-art/21-inverting-brightness.svg)

### Mapping Ranges

Convert brightness to custom ranges:

```python
from pyfreeform import map_range

# Map brightness (0-1) to rotation (0-360)
rotation = map_range(cell.brightness, 0, 1, 0, 360)

# Map brightness (0-1) to size (5-20)
size = map_range(cell.brightness, 0, 1, 5, 20)
```

![Mapping Ranges](./_images/03-image-to-art/22-mapping-ranges.svg)

### Neighbor Comparisons

Create edge detection:

```python
for cell in scene.grid:
    if cell.right:  # Check neighbor exists
        # Large difference = edge
        diff = abs(cell.brightness - cell.right.brightness)
        if diff > 0.3:
            cell.add_line(start="center", end="right", width=2)
```

![Neighbor Comparison - Edge Detection](./_images/03-image-to-art/23-neighbor-comparison.svg)

### Mixed Techniques

Combine multiple techniques for rich, layered artwork:

![Mixed Techniques - combining brightness, color, shapes, and layering](./_images/03-image-to-art/24-mixed-techniques.svg)

---

## Performance Tips

For large images or high grid counts:

1. **Use appropriate grid_size**: Start with 40, increase as needed
2. **Limit entities per cell**: More entities = larger SVG = slower render
3. **Test with small grids first**: Prototype with grid_size=20, then increase
4. **Consider cell_size**: Smaller cells = more packed = potentially slower

---

## Next Steps

You now know how to transform images into art! Continue your journey:

- **Learn more entities**: [Entities Section](../entities/01-dots.md)
- **Try advanced techniques**: [Advanced Concepts](../advanced-concepts/01-anchor-system.md)
- **See complete examples**: [Example Gallery](../examples/index.md)
- **Try recipes**: [Dot Art Recipe](../recipes/01-dot-art-from-images.md)

---

## See Also

- 🎯 [Quick Start Example](../examples/beginner/quick-start.md) - Simple dot art
- 🎯 [Custom Dots Example](../examples/beginner/custom-dots.md) - Styling variations
- 🚀 [Advanced Example](../examples/advanced/multi-layer.md) - Multi-layer composition
- 📖 [Color and Palettes](../color-and-style/02-palettes.md) - Color schemes
- 📖 [Halftone Recipe](../recipes/02-halftone-effects.md) - Classic halftone patterns

