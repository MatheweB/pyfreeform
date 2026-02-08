#!/usr/bin/env python3
"""
Example 09: Polygons

Demonstrates the Polygon entity and shape helper functions.

PyFreeform provides shape helpers for common polygons:
- triangle(), square(), diamond()
- hexagon(), star()
- regular_polygon(sides)

All helpers return vertex lists that work with cell.add_polygon().

This demonstrates:
- cell.add_polygon() with custom vertices
- Shape helpers: hexagon(), star(), diamond()
- Combining polygons with other elements
- Creating patterns with different shapes

Output: examples/09_polygons.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Polygon

# =============================================================================
# Configuration
# =============================================================================

COLS = 8
ROWS = 6
CELL_SIZE = 50

colors = Palette.neon()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=COLS, rows=ROWS, cell_size=CELL_SIZE)
scene.background = colors.background

# Different shape for each column
shape_funcs = [
    lambda: Polygon.triangle(size=0.7),
    lambda: Polygon.square(size=0.6),
    lambda: Polygon.diamond(size=0.7),
    lambda: Polygon.hexagon(size=0.7),
    lambda: Polygon.star(points=5, size=0.75),
    lambda: Polygon.star(points=6, size=0.75, inner_ratio=0.5),
    lambda: Polygon.regular_polygon(sides=8, size=0.7),
    lambda: Polygon.regular_polygon(sides=3, size=0.7),  # Another triangle
]

# Color for each row
row_colors = [
    colors.primary,
    colors.secondary,
    colors.accent,
    colors.primary,
    colors.secondary,
    colors.accent,
]

for cell in scene.grid:
    # Get shape for this column
    shape_vertices = shape_funcs[cell.col % len(shape_funcs)]()
    
    # Get color for this row
    fill_color = row_colors[cell.row % len(row_colors)]
    
    # Add the polygon
    poly = cell.add_polygon(
        shape_vertices,
        fill=fill_color,
        stroke=colors.line,
        stroke_width=1,
        z_index=1,
    )
    
    # Rotate every other row slightly
    if cell.row % 2 == 1:
        poly.rotate(15)
    
    # Add a small center dot
    cell.add_dot(
        at="center",
        radius=2,
        color=colors.background,
        z_index=2,
    )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "09_polygons.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("Shapes shown (left to right):")
print("  • Triangle, Square, Diamond, Hexagon")
print("  • 5-point star, 6-point star, Octagon, Triangle")
