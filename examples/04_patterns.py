#!/usr/bin/env python3
"""
Example 04: Grid Patterns and Selection

Demonstrates grid selection methods for creating patterns:
- grid.where() for conditional selection
- grid.checkerboard() for checkerboard patterns
- grid.border() for edge cells
- grid.row() and grid.column() for lines

Output: examples/04_patterns.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 20
CELL_SIZE = 20

colors = Palette.neon()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# --- Pattern 1: Checkerboard base ---
for cell in scene.grid.checkerboard("black"):
    cell.add_fill(color="#1a1a2e", z_index=0)

# --- Pattern 2: Border highlight ---
for cell in scene.grid.border(thickness=2):
    cell.add_dot(radius=3, color=colors.secondary, z_index=2)

# --- Pattern 3: Center cross (middle row and column) ---
mid_row = GRID_SIZE // 2
mid_col = GRID_SIZE // 2

for cell in scene.grid.row(mid_row):
    cell.add_fill(color="#ff00ff", z_index=1)
    
for cell in scene.grid.column(mid_col):
    cell.add_fill(color="#00ffff", z_index=1)

# --- Pattern 4: Corner accents ---
corners = [
    scene.grid[0, 0],
    scene.grid[0, GRID_SIZE - 1],
    scene.grid[GRID_SIZE - 1, 0],
    scene.grid[GRID_SIZE - 1, GRID_SIZE - 1],
]
for cell in corners:
    cell.add_dot(radius=8, color=colors.accent, z_index=3)

# --- Pattern 5: Diagonal stripe using where() ---
for cell in scene.grid.where(lambda c: c.row == c.col):
    cell.add_dot(radius=4, color=colors.primary, z_index=2)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "04_patterns.svg"
scene.save(output)

print(f"Created: {output.name}")
print()
print("Patterns shown:")
print("  â€¢ Checkerboard background")
print("  â€¢ Border highlight (2 cells thick)")
print("  â€¢ Center cross (row + column)")
print("  â€¢ Corner accents")
print("  â€¢ Main diagonal dots")
