
# Example 01: Quick Start

The simplest PyFreeform artwork - dot art from an image in 5 lines.

## What You'll Learn
- Scene.from_image() one-liner
- cell.color for typed access
- cell.add_dot() for easy creation

## Final Result

![Simple Dot Art](../_images/quick-start/01_simple_dot_art.svg)

## Complete Code

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=30, cell_size=12)

for cell in scene.grid:
    cell.add_dot(color=cell.color, radius=4)

scene.save("art.svg")
```

## How It Works

1. **Load image** - `Scene.from_image()` loads image data into grid cells
2. **Iterate cells** - Loop through all cells in the grid
3. **Add dots** - Use cell's color from the image
4. **Save** - Export to SVG

## Try It Yourself

- Change `grid_size=30` to `50` for more detail
- Adjust `radius=4` to change dot size
- Try `cell.brightness` instead of `cell.color`

## Related
- [Image to Art Guide](../../getting-started/03-image-to-art.md)
- [Dots Entity](../../entities/01-dots.md)
