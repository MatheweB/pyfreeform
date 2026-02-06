#!/usr/bin/env python3
"""
Example 08: Transforms

Demonstrates rotation and scaling transformations on entities.

Transforms let you:
- Rotate lines, polygons, and positions around any point
- Scale entities larger or smaller
- Chain transformations with method chaining

This demonstrates:
- line.rotate(angle) and line.scale(factor)
- polygon.rotate(angle) and polygon.scale(factor)
- Rotation around custom origins
- Creating dynamic patterns with transforms

Output: examples/08_transforms.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, shapes

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 12
CELL_SIZE = 40

colors = Palette.sunset()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

for cell in scene.grid:
    # Calculate rotation based on distance from center
    center_row = GRID_SIZE / 2
    center_col = GRID_SIZE / 2
    
    # Distance from center (0 to ~0.7 for corners)
    dx = (cell.col - center_col) / GRID_SIZE
    dy = (cell.row - center_row) / GRID_SIZE
    distance = (dx**2 + dy**2) ** 0.5
    
    # Rotation increases with distance from center (0° to 45°)
    rotation = distance * 90
    
    # Scale decreases slightly toward edges
    scale = 1.0 - distance * 0.3
    
    # Create a diamond shape
    poly = cell.add_polygon(
        shapes.diamond(size=0.7),
        fill=colors.primary,
        stroke=colors.accent,
        stroke_width=1,
        z_index=1,
    )
    
    # Apply rotation around polygon center
    poly.rotate(rotation)
    
    # Add a line through the center that rotates the same way
    line = cell.add_line(
        start=(0.2, 0.5),
        end=(0.8, 0.5),
        color=colors.secondary,
        width=2,
        z_index=2,
    )
    line.rotate(rotation, origin=cell.center)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "08_transforms.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("Notice how:")
print("  • Center shapes are aligned, edges are rotated")
print("  • Rotation creates a spiral/vortex effect")
print("  • Both the diamond and line rotate together")
