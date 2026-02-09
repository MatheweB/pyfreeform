#!/usr/bin/env python3
"""
Example 11: Working with Element Groups

PyFreeform doesn't have a formal "group" system - and that's intentional!
Instead, you use Python's natural data structures to organize elements.

This example shows the pattern for:
- Collecting related elements into lists
- Applying bulk operations (color, transform)
- Creating layered compositions with named groups

The pattern is simple and flexible:
    stars = [cell.add_dot(...) for cell in some_cells]
    for star in stars:
        star.color = "gold"

Output: examples/11_groups.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Polygon, Line

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 16
CELL_SIZE = 25

colors = Palette.ocean()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=GRID_SIZE, rows=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# =============================================================================
# PATTERN: Collect related elements into groups (Python lists)
# =============================================================================

# Group 1: Border frame
border_elements = []
for cell in scene.grid.border(thickness=1):
    elem = cell.add_fill(color=colors.grid, z_index=0)
    border_elements.append(elem)

# Group 2: Diagonal accent line of hexagons
diagonal_hexagons = []
for cell in scene.grid.where(lambda c: c.row == c.col):
    hex_poly = cell.add_polygon(
        Polygon.hexagon(size=0.8),
        fill=colors.primary,
        z_index=2,
    )
    diagonal_hexagons.append(hex_poly)

# Group 3: Stars in corners (2x2 regions)
corner_stars = []
corner_regions = [
    (0, 0),                           # Top-left
    (0, GRID_SIZE - 2),               # Top-right
    (GRID_SIZE - 2, 0),               # Bottom-left
    (GRID_SIZE - 2, GRID_SIZE - 2),   # Bottom-right
]

for start_row, start_col in corner_regions:
    for dr in range(2):
        for dc in range(2):
            cell = scene.grid[start_row + dr, start_col + dc]
            star_poly = cell.add_polygon(
                Polygon.star(points=4, size=0.6, inner_ratio=0.3),
                fill=colors.accent,
                z_index=3,
            )
            corner_stars.append(star_poly)

# Group 4: Center cluster of dots
center_dots = []
center_start = GRID_SIZE // 2 - 2
for cell in scene.grid.region(
    row_start=center_start,
    row_end=center_start + 4,
    col_start=center_start,
    col_end=center_start + 4,
):
    dot = cell.add_dot(radius=0.16, color=colors.secondary, z_index=1)
    center_dots.append(dot)

# =============================================================================
# PATTERN: Bulk operations on groups
# =============================================================================

# Rotate all diagonal hexagons by 30 degrees
for hex_poly in diagonal_hexagons:
    hex_poly.rotate(30)

# Scale up corner stars and change their color
for star in corner_stars:
    star.scale(1.2)  # 20% larger
    star.fill = colors.primary  # Change from accent to primary

# Add glow effect to center dots (by making them slightly transparent)
# Note: We'd need opacity support for true glow - here we just make them bigger
for i, dot in enumerate(center_dots):
    # Vary size based on position in group
    dot.radius = 3 + (i % 4)

# =============================================================================
# PATTERN: Connect elements from different groups
# =============================================================================

# Connect the first star in each corner to the center dots
if corner_stars and center_dots:
    # Connect first corner star to first center dot
    for i in range(min(4, len(corner_stars) // 4)):
        star = corner_stars[i * 4]  # First star of each corner
        
        # Find the nearest center dot
        center_dot = center_dots[i % len(center_dots)]
        
        conn = star.connect(center_dot, shape=Line(), style={
            "width": 1,
            "color": colors.line,
            "z_index": 1,
        })
        scene.add(conn)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "11_groups.svg"
scene.save(output)

print(f"Created: {output.name}")
print()
print("Element groups:")
print(f"  • Border elements: {len(border_elements)}")
print(f"  • Diagonal hexagons: {len(diagonal_hexagons)}")
print(f"  • Corner stars: {len(corner_stars)}")
print(f"  • Center dots: {len(center_dots)}")
print()
print("This pattern works because:")
print("  • Python lists are natural 'groups'")
print("  • List comprehensions collect elements efficiently")
print("  • Bulk operations are just for-loops")
print("  • No special API needed!")
