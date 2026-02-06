#!/usr/bin/env python3
"""
Example 14: Ellipses

Demonstrates ellipse entity in PyFreeform with parametric positioning.

Ellipses support:
- Horizontal radius (rx) and vertical radius (ry)
- Rotation
- Fill and stroke styling
- Parametric positioning with along= (like lines and curves)

Output: examples/14_ellipses.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

colors = Palette.ocean()

# Grid configuration
GRID_SIZE = 30

# Z-index layers
Z_FILL = 0
Z_ELLIPSE = 1
Z_DOT = 2

# =============================================================================
# Create Art
# =============================================================================

# Use radial gradient for interesting ellipse patterns
from create_sample_image import create_radial_gradient
image_path = create_radial_gradient(width=450, height=450)

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=15)
scene.background = colors.background

for cell in scene.grid:
    # Fill cells based on brightness
    if cell.brightness < 0.3:
        cell.add_fill(color=colors.background, z_index=Z_FILL)

    # Rotation based on position
    rotation = (cell.row + cell.col) * 15

    # Add ellipse - use large values, will be auto-constrained
    ellipse = cell.add_ellipse(
        rx=100,  # Start large
        ry=60,   # Will be auto-scaled to fit
        rotation=rotation,
        fill=cell.color,
        stroke=None,
        z_index=Z_ELLIPSE
    )

    # Auto-constrain to cell with brightness-based scaling
    # Dark cells: 30% of cell, bright cells: 100% of cell
    target_scale = 0.3 + cell.brightness * 0.7
    ellipse.fit_to_cell(target_scale)

    # Position dot along ellipse perimeter
    # t=0 is right side, t=0.25 is top, t=0.5 is left, t=0.75 is bottom
    cell.add_dot(
        along=ellipse,
        t=cell.brightness,  # Dot position varies with brightness
        radius=1.5,
        color=colors.accent,
        z_index=Z_DOT
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "14_ellipses.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("This example demonstrates:")
print("  • Ellipse entity with rx/ry (radii)")
print("  • Ellipse rotation based on grid position")
print("  • Ellipse fill with image colors")
print("  • Auto-constraining with .fit_to_cell() - handles rotation automatically")
print("  • Brightness-based scaling (30% to 100% of cell)")
print("  • Parametric positioning: cell.add_dot(along=ellipse, t=...)")
