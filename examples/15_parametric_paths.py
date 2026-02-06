#!/usr/bin/env python3
"""
Example 15: Parametric Paths - Unified Interface

Demonstrates the unified Pathable interface in PyFreeform.

Thanks to the Pathable protocol, Line, Curve, and Ellipse all work
with cell.add_dot(along=..., t=...) for parametric positioning.

This example shows how the same interface works for different path types,
creating a cohesive visual composition.

Output: examples/15_parametric_paths.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

colors = Palette.midnight()

# Z-index layers
Z_BORDER = 0
Z_PATH = 1
Z_DOT = 2

# =============================================================================
# Create Art
# =============================================================================

# Use colorful gradient to show variety in path types
from create_sample_image import create_gradient_image
image_path = create_gradient_image(width=500, height=500)

scene = Scene.from_image(image_path, grid_size=20, cell_size=25)
scene.background = colors.background

for cell in scene.grid:
    cell.add_border(color=colors.grid, width=0.3, z_index=Z_BORDER)

    # Different paths based on brightness
    if cell.brightness < 0.35:
        # Dark areas: straight lines
        path = cell.add_line(
            start="left",
            end="right",
            color=colors.line,
            width=1,
            z_index=Z_PATH
        )
    elif cell.brightness < 0.65:
        # Medium areas: curves
        path = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.5,
            color=colors.line,
            width=1,
            z_index=Z_PATH
        )
    else:
        # Bright areas: ellipses
        path = cell.add_ellipse(
            rx=8,
            ry=6,
            rotation=45,
            fill=None,
            stroke=colors.line,
            stroke_width=1,
            z_index=Z_PATH
        )

    # ALL paths support the same interface!
    # Position a dot along the path using brightness
    cell.add_dot(
        along=path,
        t=cell.brightness,
        radius=2,
        color=colors.accent,
        z_index=Z_DOT
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "15_parametric_paths.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("This example demonstrates:")
print("  • Unified Pathable interface for all path types")
print("  • Line, Curve, and Ellipse all support along= parameter")
print("  • Same code works with different path types")
print("  • Visual variety from single parametric positioning pattern")
print("  • Brightness-based path selection and dot positioning")
