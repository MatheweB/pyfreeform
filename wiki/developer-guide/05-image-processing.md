
# Image Processing

How images are loaded and processed.

## Image Class

```python
from pyfreeform.image import Image

# Load image
img = Image.from_file("photo.jpg")

# Properties
img.width, img.height
img.data  # NumPy array (H, W, C)

# Resize
img_resized = img.resize(width=800, height=600)

# Get pixel
color = img.get_pixel(x, y)  # (r, g, b, a)
```

![Basic image loading into a grid](./_images/05-image-processing/01-image-loading-basic.svg)

![Image converted to grid with brightness-based dots](./_images/05-image-processing/02-image-to-grid.svg)

## Layer Class

Single-channel data:

```python
# Extract channels
brightness = img.brightness_layer()
red = img.red_layer()
green = img.green_layer()
blue = img.blue_layer()

# Sample from layer
value = layer.sample(x, y)  # 0.0 to 1.0
```

![Brightness layer visualization with sized dots](./_images/05-image-processing/03-layer-brightness.svg)

![Layer comparison showing brightness and color data](./_images/05-image-processing/04-layer-comparison.svg)

## Grid Loading

```python
# Automatic loading
scene = Scene.from_image("photo.jpg", grid_size=40)

# Manual loading
from pyfreeform import Grid, Image

img = Image.from_file("photo.jpg")
grid = Grid.from_image(img, cols=40)

# Access cell data
for cell in grid:
    print(cell.brightness)  # From loaded layer
```

![Grid loading with cell borders showing structure](./_images/05-image-processing/05-grid-loading-steps.svg)

![Different grid sizes: how grid_size affects cell count and detail level](./_images/05-image-processing/06-grid-sizes.svg)

### Cell Data

Each cell provides brightness and color data sampled from the image:

![Cell data: brightness values mapped from image pixels](./_images/05-image-processing/07-cell-data-brightness.svg)

![Cell data: color values sampled from image regions](./_images/05-image-processing/08-cell-data-color.svg)

![Halftone effect created from image brightness data](./_images/05-image-processing/09-practical-halftone.svg)

## See Also
- [Image to Art](../getting-started/03-image-to-art.md)
