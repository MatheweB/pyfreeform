#!/usr/bin/env python3
"""
Example 06: Advanced - Combining Techniques

A complete artwork combining multiple PyFreeform features:
- Image-based brightness data
- Multiple layers with z-index
- Conditional styling based on cell data
- Grid patterns and selections
- Cross-cell connections

Output: examples/06_advanced.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 25
CELL_SIZE = 16

# Layer ordering
Z_BACKGROUND = 0
Z_GRID = 1
Z_LINES = 2
Z_DOTS = 3
Z_HIGHLIGHTS = 4

colors = Palette.midnight()

# Thresholds for brightness-based styling
BRIGHT_THRESHOLD = 0.7
DIM_THRESHOLD = 0.3

# =============================================================================
# Create Art
# =============================================================================

from create_sample_image import create_gradient_image
image_path = create_gradient_image()

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# --- Layer 1: Subtle grid for all cells ---
for cell in scene.grid:
    cell.add_border(color=colors.grid, width=0.3, z_index=Z_GRID)

# --- Layer 2: Diagonal lines only in medium-brightness cells ---
for cell in scene.grid.where(lambda c: DIM_THRESHOLD < c.brightness < BRIGHT_THRESHOLD):
    cell.add_diagonal(
        # Default: start="bottom_left", end="top_right"
        color=colors.line,
        width=0.5,
        z_index=Z_LINES,
    )

# --- Layer 3: Dots sized by brightness ---
for cell in scene.grid:
    # Size: small for dark, large for bright
    radius = 1 + cell.brightness * 5
    
    # Color: use image color, but brighten for visibility
    cell.add_dot(
        color=cell.color,
        radius=radius,
        z_index=Z_DOTS,
    )

# --- Layer 4: Highlight dots for very bright cells ---
for cell in scene.grid.where(lambda c: c.brightness > BRIGHT_THRESHOLD):
    # Extra glow dot
    cell.add_dot(
        radius=8,
        color=colors.accent,
        z_index=Z_HIGHLIGHTS,
    )

# --- Layer 5: Connect bright cells to their neighbors ---
for cell in scene.grid.where(lambda c: c.brightness > BRIGHT_THRESHOLD):
    # Connect to right neighbor if it's also bright
    if cell.right and cell.right.brightness > BRIGHT_THRESHOLD:
        # Get the highlight dots we created
        if cell.entities and cell.right.entities:
            my_dot = cell.entities[-1]  # Last added was highlight
            neighbor_dot = cell.right.entities[-1]
            conn = my_dot.connect(neighbor_dot, style={
                "width": 1,
                "color": colors.accent,
                "z_index": Z_HIGHLIGHTS,
            })
            scene.add(conn)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "06_advanced.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print(f"Total entities: {len(scene.entities)}")
print()
print("Layers:")
print(f"  â€¢ Grid borders")
print(f"  â€¢ Diagonal lines (medium brightness only)")
print(f"  â€¢ Dots sized by brightness")
print(f"  â€¢ Highlight glows (bright areas)")
print(f"  â€¢ Connections between bright neighbors")
