#!/usr/bin/env python3
"""
Example 03: Diagonal Lines with Brightness-Controlled Dots

Creates a grid where each cell has:
- A visible cell border
- A diagonal line (SW to NE)
- A dot that slides along the line based on image brightness

The dot position is controlled by brightness:
- Bright areas (white): dot at TOP-RIGHT (t=1.0)
- Dark areas (black): dot at BOTTOM-LEFT (t=0.0)

This demonstrates:
- cell.add_border() for grid visibility
- cell.add_diagonal() for line creation
- cell.add_dot(along=line, t=...) for parametric positioning
- z_index for layering control

Output: examples/03_diagonal.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 20
CELL_SIZE = 25

# Layer ordering (higher = on top)
Z_BORDER = 0
Z_LINE = 1
Z_DOT = 2

# Colors
colors = Palette.midnight()

# =============================================================================
# Create Art
# =============================================================================

# Use horizontal gradient: white on left, black on right
from create_sample_image import create_horizontal_gradient
image_path = create_horizontal_gradient(GRID_SIZE, GRID_SIZE)

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

for cell in scene.grid:
    # 1. Cell border (bottom layer)
    cell.add_border(color=colors.grid, width=0.5, z_index=Z_BORDER)
    
    # 2. Diagonal line SWâ†’NE (middle layer)
    line = cell.add_diagonal(
        # Default: start="bottom_left", end="top_right"
        color=colors.line,
        width=1,
        z_index=Z_LINE,
    )
    
    # 3. Dot slides along line based on brightness (top layer)
    # brightness=0 (dark) â†’ t=0 (bottom-left)
    # brightness=1 (bright) â†’ t=1 (top-right)
    cell.add_dot(
        along=line,
        t=cell.brightness,
        color=colors.accent,
        radius=3,
        z_index=Z_DOT,
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "03_diagonal.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("How to read the output:")
print("  â€¢ Left side (bright): dots at top-right of cells")
print("  â€¢ Right side (dark): dots at bottom-left of cells")
