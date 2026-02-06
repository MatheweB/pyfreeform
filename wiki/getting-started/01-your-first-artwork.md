
# Your First Artwork

Let's create something beautiful! This tutorial will show you how to make stunning dot art from any image in just 5 lines of Python code.

---

## The Famous 5-Line Example

Here's the complete code:

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    cell.add_dot(color=cell.color)

scene.save("art.svg")
```

![Complete 5-line example result](./_images/01-your-first-artwork/01-complete-5-line.svg)

That's it! This creates a dot art version of your image. Let's break down what's happening.

---

## Step-by-Step Breakdown

![Starting point: blank canvas before any code](./_images/01-your-first-artwork/step-00-blank-canvas.svg)

### Step 1: Import

```python
from pyfreeform import Scene
```

![Blank canvas - ready to start](./_images/01-your-first-artwork/step-01-after-import.svg)

Import the `Scene` class - the main container for your artwork. It provides everything you need to get started.

### Step 2: Load Your Image

```python
scene = Scene.from_image("photo.jpg", grid_size=40)
```

![Grid structure created](./_images/01-your-first-artwork/step-02-grid-structure.svg)

![Grid with cell centers highlighted](./_images/01-your-first-artwork/step-02b-grid-with-centers.svg)

!!! info "What grid_size Does"
    This powerful one-liner:

    1. Loads your image
    2. Creates a scene with the same dimensions
    3. Divides it into a 40x40 grid (1,600 cells)
    4. Loads color and brightness data into each cell

    Each cell now "knows" what color and brightness it should be based on the image.

### Step 3: Create the Art

```python
for cell in scene.grid:
    cell.add_dot(color=cell.color)
```

![First dots appearing on the grid](./_images/01-your-first-artwork/step-03-first-dots.svg)

![Dots being added progressively](./_images/01-your-first-artwork/step-03b-half-complete.svg)

Loop through every cell and add a dot colored by the cell's image data. The `cell.color` property gives you the color from the original image at that position.

### Step 4: Save

```python
scene.save("art.svg")
```

![Complete artwork](./_images/01-your-first-artwork/step-04-complete.svg)

Export your artwork as an SVG file. SVGs are scalable vector graphics that look crisp at any size!

---

## What You Get

Running this code produces an SVG file with 1,600 colored dots arranged in a grid, recreating your original image in dot art form.

### Example Output

![Quick Start Example](./_images/01-your-first-artwork/01-complete-5-line.svg)

*This example uses a simple gradient, but try it with any photo!*

---

## Try It Yourself

### Using Your Own Image

Replace `"photo.jpg"` with the path to any image:

```python
scene = Scene.from_image("/path/to/your/image.jpg", grid_size=40)
```

### Experiment

!!! tip "Try Different Parameters"
    Experiment with these parameters to see how they affect your artwork:

**Grid Size** - More cells = more detail:
```python
scene = Scene.from_image("photo.jpg", grid_size=60)  # More detailed
scene = Scene.from_image("photo.jpg", grid_size=20)  # More abstract
```

| grid_size=10 (Minimal) | grid_size=20 (Abstract) | grid_size=40 (Balanced) | grid_size=60 (Detailed) | grid_size=80 (High Detail) |
|---|---|---|---|---|
| ![](./_images/01-your-first-artwork/experiment-grid-size-10.svg) | ![](./_images/01-your-first-artwork/experiment-grid-size-20.svg) | ![](./_images/01-your-first-artwork/experiment-grid-size-40.svg) | ![](./_images/01-your-first-artwork/experiment-grid-size-60.svg) | ![](./_images/01-your-first-artwork/experiment-grid-size-80.svg) |

**Dot Size** - Control how large dots are:
```python
cell.add_dot(color=cell.color, radius=6)   # Larger dots
cell.add_dot(color=cell.color, radius=2)   # Smaller dots
```

| radius=2 (Small) | radius=4 (Medium) | radius=6 (Large) | radius=8 (Extra Large) |
|---|---|---|---|
| ![](./_images/01-your-first-artwork/experiment-dot-radius-2.svg) | ![](./_images/01-your-first-artwork/experiment-dot-radius-4.svg) | ![](./_images/01-your-first-artwork/experiment-dot-radius-6.svg) | ![](./_images/01-your-first-artwork/experiment-dot-radius-8.svg) |

**Dot Spacing** - Use `cell_size` to control spacing:
```python
scene = Scene.from_image("photo.jpg", grid_size=40, cell_size=15)  # More spacing
scene = Scene.from_image("photo.jpg", grid_size=40, cell_size=8)   # Tight packed
```

| cell_size=8 (Tight) | cell_size=12 (Normal) | cell_size=15 (Spacious) | cell_size=20 (Wide) |
|---|---|---|---|
| ![](./_images/01-your-first-artwork/experiment-cell-size-8.svg) | ![](./_images/01-your-first-artwork/experiment-cell-size-12.svg) | ![](./_images/01-your-first-artwork/experiment-cell-size-15.svg) | ![](./_images/01-your-first-artwork/experiment-cell-size-20.svg) |

---

## What's Happening Under the Hood?

When you call `Scene.from_image()`:

1. **Image Loading**: Pillow loads and processes your image
2. **Grid Creation**: The scene creates a Grid with your specified number of cells
3. **Data Extraction**: Each cell samples the image to get its color and brightness
4. **Ready to Draw**: Cells are now accessible via `scene.grid`

When you add dots:
- `cell.add_dot()` creates a Dot entity
- The dot is automatically positioned at the cell's center
- The dot's color comes from `cell.color` (from the image)
- The entity is added to the scene's render list

When you save:
- All entities are rendered to SVG
- Z-index determines layering (more on this later)
- The SVG file is written to disk

---

## Common Variations

### Brightness-Based Sizing

!!! example "Variable Dot Sizes"
    Make brighter areas have larger dots:

```python
for cell in scene.grid:
    size = 2 + cell.brightness * 6  # Range: 2 to 8
    cell.add_dot(color=cell.color, radius=size)
```

| Before (Uniform) | After (Brightness-based) | Extreme Sizing |
|---|---|---|
| ![](./_images/01-your-first-artwork/variation-brightness-step1-uniform.svg) | ![](./_images/01-your-first-artwork/variation-brightness-step2-dynamic.svg) | ![](./_images/01-your-first-artwork/variation-brightness-step3-extreme.svg) |

### Conditional Rendering

Only draw dots in bright areas:

```python
for cell in scene.grid:
    if cell.brightness > 0.5:  # Only bright areas
        cell.add_dot(color=cell.color)
```

| All Dots | Brightness > 0.5 | Brightness > 0.7 | Dark Only (< 0.3) |
|---|---|---|---|
| ![](./_images/01-your-first-artwork/variation-conditional-step1-all.svg) | ![](./_images/01-your-first-artwork/variation-conditional-step2-bright.svg) | ![](./_images/01-your-first-artwork/variation-conditional-step3-very-bright.svg) | ![](./_images/01-your-first-artwork/variation-conditional-step4-dark.svg) |

### Using Palettes

Replace image colors with a consistent palette:

```python
from pyfreeform import Palette

colors = Palette.midnight()
scene.background = colors.background

for cell in scene.grid:
    if cell.brightness > 0.6:
        cell.add_dot(color=colors.primary, radius=5)
    elif cell.brightness > 0.3:
        cell.add_dot(color=colors.secondary, radius=3)
```

| Original Colors | Midnight Palette | Ocean Palette | Sunset Palette |
|---|---|---|---|
| ![](./_images/01-your-first-artwork/variation-palette-step1-original.svg) | ![](./_images/01-your-first-artwork/variation-palette-step2-midnight.svg) | ![](./_images/01-your-first-artwork/variation-palette-step3-ocean.svg) | ![](./_images/01-your-first-artwork/variation-palette-step4-sunset.svg) |

---

## Next Steps

You've created your first PyFreeform artwork! Now you can:

1. **Understand the concepts**: Learn about [Core Concepts](02-core-concepts.md)
2. **Go deeper with images**: Read the [Image to Art Guide](03-image-to-art.md)
3. **See more examples**: Browse the [Example Gallery](../examples/index.md)
4. **Learn fundamentals**: Explore [Scenes](../fundamentals/01-scenes.md)

---

## See Also

- 🎯 [Custom Dots Example](../examples/beginner/custom-dots.md) - Styling variations
- 📖 [Color and Palettes](../color-and-style/02-palettes.md) - Color schemes
- 🎨 [Dot Art Recipe](../recipes/01-dot-art-from-images.md) - More techniques

