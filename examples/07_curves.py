#!/usr/bin/env python3
"""
Example 07: Curves

Demonstrates the Curve entity - quadratic Bézier curves that add
organic, flowing shapes to your art.

Key feature: dots can slide along curves just like lines!

    curve = cell.add_curve(curvature=0.5)
    cell.add_dot(along=curve, t=cell.brightness)

This demonstrates:
- cell.add_curve() for creating curved paths
- curvature parameter: 0 = straight, positive/negative = bowing direction
- Positioning dots along curves with along= and t=

Output: examples/07_curves.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 15
CELL_SIZE = 30

# Layer ordering
Z_CURVE = 1
Z_DOT = 2

colors = Palette.ocean()

# =============================================================================
# Create Art
# =============================================================================

# Use radial gradient: bright center, dark edges
from create_sample_image import create_radial_gradient
image_path = create_radial_gradient(GRID_SIZE, GRID_SIZE)

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

for cell in scene.grid:
    # Curvature varies by position: left side curves one way, right side the other
    # This creates a flowing wave pattern across the grid
    curvature = (cell.col / GRID_SIZE - 0.5) * 1.5  # Range: -0.75 to 0.75
    
    # Create curve from bottom-left to top-right
    curve = cell.add_curve(
        start="bottom_left",
        end="top_right",
        curvature=curvature,
        color=colors.line,
        width=1,
        z_index=Z_CURVE,
    )
    
    # Dot slides along curve based on brightness
    # Bright = toward end (top-right), Dark = toward start (bottom-left)
    cell.add_dot(
        along=curve,
        t=cell.brightness,
        color=colors.accent,
        radius=3,
        z_index=Z_DOT,
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "07_curves.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("Notice how:")
print("  • Curves bow left on the left side, right on the right side")
print("  • Dots cluster toward the center (bright area)")
print("  • The organic curves break the rigid grid feel")
