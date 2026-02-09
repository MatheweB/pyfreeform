#!/usr/bin/env python3
"""
Example 02: Customized Dot Art

Dot art with custom styling using Palette and style objects.

This demonstrates:
- Palette for consistent color schemes
- DotStyle for typed configuration
- cell.brightness for data-driven sizing

Output: examples/02_custom_dots.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, DotStyle

# =============================================================================
# Configuration - all settings in one place
# =============================================================================

GRID_SIZE = 35
CELL_SIZE = 10

# Try different palettes: midnight, sunset, ocean, forest, neon, pastel
colors = Palette.ocean()

# Base dot style (we'll vary the radius based on brightness)
dot_style = DotStyle(radius=0.3, color=colors.primary, z_index=1)

# =============================================================================
# Create Art
# =============================================================================

# Create sample image (or use: Scene.from_image("your_photo.jpg", ...))
from create_sample_image import create_gradient_image
image_path = create_gradient_image()

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

for cell in scene.grid:
    # Size varies with brightness: brighter = larger
    radius = 0.1 + cell.brightness * 0.4  # Range: 0.1 to 0.5
    
    cell.add_dot(
        color=cell.color,  # Use image color
        radius=radius,
        z_index=1,
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "02_custom_dots.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Palette: ocean")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
