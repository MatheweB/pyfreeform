#!/usr/bin/env python3
"""
Example 05: Cross-Cell Connections

Demonstrates that entities don't have to stay within their cells:
- Connecting dots across cells
- Wave patterns that cross cell boundaries
- Freeform lines independent of grid

Output: examples/05_connections.svg
"""

from pathlib import Path
import math
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Dot, Line

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 15
CELL_SIZE = 30

colors = Palette.sunset()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# --- Part 1: Horizontal connections between neighbors ---
# Connect dots in every other row
for row_idx in range(0, GRID_SIZE, 2):
    prev_dot = None
    for cell in scene.grid.row(row_idx):
        dot = cell.add_dot(radius=4, color=colors.primary, z_index=2)
        
        # Connect to previous dot (crosses cell boundary!)
        if prev_dot:
            conn = prev_dot.connect(dot, style={
                "width": 1,
                "color": colors.line,
                "z_index": 1,
            })
            scene.add(conn)
        
        prev_dot = dot

# --- Part 2: Wave pattern (dots offset from cell centers) ---
for col_idx in range(GRID_SIZE):
    for row_idx in range(GRID_SIZE):
        if row_idx % 2 == 1:  # Only odd rows
            cell = scene.grid[row_idx, col_idx]
            
            # Calculate wave offset
            wave = math.sin(col_idx * 0.5) * (CELL_SIZE * 0.3)
            
            # Place dot with offset (not confined to cell!)
            cell.add_dot(
                at="center",
                radius=2,
                color=colors.secondary,
                z_index=2,
            )

# --- Part 3: Freeform diagonal line (not grid-aligned) ---
# This line goes from top-left to bottom-right, ignoring grid
scene.add(Line(
    20, 20,
    scene.width - 20, scene.height - 20,
    width=3,
    color=colors.accent,
    z_index=3,
))

# --- Part 4: Large dots at grid corners (spanning cells) ---
# These dots are larger than cells, creating overlap
corner_cells = [
    scene.grid[2, 2],
    scene.grid[2, GRID_SIZE - 3],
    scene.grid[GRID_SIZE - 3, 2],
    scene.grid[GRID_SIZE - 3, GRID_SIZE - 3],
]
for cell in corner_cells:
    # Dot larger than cell size creates deliberate overlap
    cell.add_dot(radius=CELL_SIZE * 0.8, color=colors.primary, z_index=0)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "05_connections.svg"
scene.save(output)

print(f"Created: {output.name}")
print()
print("This example shows:")
print("  â€¢ Dots connected across cell boundaries")
print("  â€¢ Elements don't have to stay in their cells")
print("  â€¢ Freeform lines independent of the grid")
print("  â€¢ Large dots that overlap multiple cells")
