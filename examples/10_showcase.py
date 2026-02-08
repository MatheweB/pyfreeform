#!/usr/bin/env python3
"""
Example 10: Showcase

A beautiful artwork combining all PyFreeform features:
- Image-based data (brightness, color)
- Curves with parametric dot positioning
- Polygons with rotation
- Multiple z-index layers
- Cross-cell connections

This creates a cohesive piece showing how the features work together.

Output: examples/10_showcase.svg
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Polygon

# =============================================================================
# Configuration
# =============================================================================

GRID_SIZE = 20
CELL_SIZE = 20

# Layer ordering
Z_BACKGROUND = 0
Z_CURVES = 1
Z_POLYGONS = 2
Z_DOTS = 3
Z_CONNECTIONS = 4

colors = Palette.midnight()

# Thresholds
BRIGHT_THRESHOLD = 0.65
DIM_THRESHOLD = 0.35

# =============================================================================
# Create Art
# =============================================================================

from create_sample_image import create_gradient_image
image_path = create_gradient_image()

scene = Scene.from_image(image_path, grid_size=GRID_SIZE, cell_size=CELL_SIZE)
scene.background = colors.background

# Track bright dots for connections
bright_dots = []

for cell in scene.grid:
    b = cell.brightness
    
    # --- Layer 1: Subtle checkerboard for dark cells ---
    if (cell.row + cell.col) % 2 == 0 and b < DIM_THRESHOLD:
        cell.add_fill(color="#1f1f3d", z_index=Z_BACKGROUND)
    
    # --- Layer 2: Curves in medium-brightness cells ---
    if DIM_THRESHOLD < b < BRIGHT_THRESHOLD:
        # Curvature based on position - creates flow
        curvature = (cell.col / GRID_SIZE - 0.5) * 0.8
        
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            color=colors.line,
            width=0.5,
            z_index=Z_CURVES,
        )
        
        # Small dot along curve
        cell.add_dot(
            along=curve,
            t=b,
            color=colors.secondary,
            radius=2,
            z_index=Z_DOTS,
        )
    
    # --- Layer 3: Hexagons in bright cells ---
    if b > BRIGHT_THRESHOLD:
        # Size based on brightness
        size = 0.4 + (b - BRIGHT_THRESHOLD) * 1.5
        
        poly = cell.add_polygon(
            Polygon.hexagon(size=min(size, 0.9)),
            fill=colors.primary,
            stroke=colors.accent,
            stroke_width=1,
            z_index=Z_POLYGONS,
        )
        
        # Rotate based on position
        rotation = (cell.row + cell.col) * 15
        poly.rotate(rotation)
        
        # Add accent dot and track for connections
        dot = cell.add_dot(
            at="center",
            color=colors.accent,
            radius=3,
            z_index=Z_DOTS,
        )
        bright_dots.append((cell, dot))
    
    # --- Layer 4: Tiny dots in dark cells ---
    elif b < DIM_THRESHOLD:
        cell.add_dot(
            at="center",
            color=colors.grid,
            radius=1,
            z_index=Z_DOTS,
        )

# --- Layer 5: Connect nearby bright cells ---
for i, (cell1, dot1) in enumerate(bright_dots):
    for cell2, dot2 in bright_dots[i+1:]:
        # Only connect if they're neighbors (within 2 cells)
        row_diff = abs(cell1.row - cell2.row)
        col_diff = abs(cell1.col - cell2.col)
        
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0:
            conn = dot1.connect(dot2, style={
                "width": 1,
                "color": colors.accent,
                "z_index": Z_CONNECTIONS,
            })
            scene.add(conn)

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "10_showcase.svg"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print(f"Total entities: {len(scene.entities)}")
print(f"Connections: {len(scene.connections)}")
print()
print("This artwork combines:")
print("  • Image data driving all visual decisions")
print("  • Curves in mid-brightness areas (flowing lines)")
print("  • Rotating hexagons in bright areas")
print("  • Subtle dots in dark areas")
print("  • Connections between neighboring bright cells")
