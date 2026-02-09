#!/usr/bin/env python3
"""
Example 12: Text

Demonstrates text labels in PyFreeform.

Text can be added to cells for:
- Labels and annotations
- Data visualization
- Typographic art
- Grid coordinates or values

This demonstrates:
- cell.add_text() for adding text to cells
- Font families: serif, sans-serif, monospace
- Text positioning and alignment
- Combining text with other elements

Output: examples/12_text.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Polygon

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 8
CELL_SIZE = 50

colors = Palette.midnight()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

for cell in scene.grid:
    # Checkerboard background
    if (cell.row + cell.col) % 2 == 0:
        cell.add_fill(color="#252545", z_index=0)
    
    # Different content based on position
    if cell.row == 0:
        # Header row: column letters
        letter = chr(ord('A') + cell.col)
        cell.add_text(
            letter,
            font_size=24,
            font_family="serif",
            color=colors.accent,
            z_index=2,
        )
    elif cell.col == 0:
        # First column: row numbers
        cell.add_text(
            str(cell.row),
            font_size=20,
            font_family="monospace",
            color=colors.secondary,
            z_index=2,
        )
    elif cell.row == cell.col:
        # Diagonal: special symbols
        cell.add_polygon(
            Polygon.star(points=4, size=0.5, inner_ratio=0.4),
            fill=colors.primary,
            z_index=1,
        )
        cell.add_text(
            "★",
            font_size=16,
            color=colors.background,
            z_index=2,
        )
    else:
        # Regular cells: show coordinates
        coord = f"{cell.col},{cell.row}"
        cell.add_text(
            coord,
            font_size=12,
            font_family="monospace",
            color=colors.grid,
            z_index=1,
        )

# Add a title at the top (using scene.add for absolute positioning)
from pyfreeform import Text
title = Text(
    scene.width / 2, 20,
    "Grid Coordinates",
    font_size=14,
    font_family="sans-serif",
    color=colors.line,
    text_anchor="middle",
    baseline="hanging",
    z_index=10,
)
scene.place(title)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "12_text.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("This example shows:")
print("  • Header row with serif letters (A-H)")
print("  • First column with monospace numbers")
print("  • Diagonal cells with stars and symbols")
print("  • Regular cells with coordinate labels")
print("  • A title using absolute positioning")
