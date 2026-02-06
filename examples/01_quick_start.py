#!/usr/bin/env python3
"""
Example 01: Quick Start

The simplest possible PyFreeform artwork - dot art from an image in 5 lines.

This demonstrates:
- Scene.from_image() for one-liner setup
- cell.color for typed access to image data
- cell.add_dot() for easy dot creation

Output: examples/01_quick_start.svg
"""

from pathlib import Path
import sys

# For development: add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene

# =============================================================================
# That's it! Just 5 lines of actual code:
# =============================================================================

# 1. Create a sample image (or use your own: Scene.from_image("photo.jpg", ...))
from create_sample_image import create_gradient_image
image_path = create_gradient_image()

# 2. Create scene from image
scene = Scene.from_image(image_path, grid_size=30, cell_size=12)

# 3. Add a dot to each cell, colored by the image
for cell in scene.grid:
    cell.add_dot(color=cell.color, radius=4)

# 4. Save
scene.save(Path(__file__).parent / "01_quick_start.svg")

print(f"Created: 01_quick_start.svg ({scene.width}x{scene.height})")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows} = {len(scene.grid)} cells")
