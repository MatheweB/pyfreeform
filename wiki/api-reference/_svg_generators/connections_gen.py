#!/usr/bin/env python3
"""
SVG Generator for: api-reference/connections.md

Generates visual examples demonstrating Connection class usage.
"""

from pyfreeform import Scene, Palette, Dot, Connection, shapes
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "connections"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Basic Connection
# =============================================================================

def example1_basic():
    """Connection() - Connect two dots"""
    scene = Scene(width=400, height=200, background="#1a1a2e")
    colors = Palette.ocean()

    # Create two dots
    dot1 = Dot(100, 100, radius=15, color=colors.primary)
    dot2 = Dot(300, 100, radius=15, color=colors.accent)

    scene.add(dot1)
    scene.add(dot2)

    # Connect them
    conn = Connection(dot1, dot2, style={"width": 2, "color": colors.line})
    scene.add(conn)

    scene.save(OUTPUT_DIR / "example1-basic.svg")


# =============================================================================
# Multiple Connections
# =============================================================================

def example2_multiple():
    """Multiple connections between dots"""
    scene = Scene(width=400, height=300, background="#1a1a2e")
    colors = Palette.midnight()

    # Create dots in triangle pattern
    dot1 = Dot(200, 80, radius=15, color=colors.primary)
    dot2 = Dot(100, 220, radius=15, color=colors.secondary)
    dot3 = Dot(300, 220, radius=15, color=colors.accent)

    scene.add(dot1)
    scene.add(dot2)
    scene.add(dot3)

    # Connect all pairs
    scene.add(Connection(dot1, dot2, style={"width": 2, "color": colors.line}))
    scene.add(Connection(dot2, dot3, style={"width": 2, "color": colors.line}))
    scene.add(Connection(dot1, dot3, style={"width": 2, "color": colors.line}))

    scene.save(OUTPUT_DIR / "example2-multiple.svg")


# =============================================================================
# Connection with Different Anchors
# =============================================================================

def example3_anchors():
    """Using different anchor points"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=150, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Create rectangles in each cell
    rects = []
    for cell in cells:
        rect = cell.add_rect(width=80, height=60,
                              fill=colors.primary, stroke=colors.accent, stroke_width=2)
        rects.append(rect)

    # Get the rectangles
    rect1 = rects[0]
    rect2 = rects[1]

    # Connect using different anchors
    scene.add(Connection(rect1, rect2, start_anchor="right", end_anchor="left", style={"width": 2, "color": colors.line}))

    scene.save(OUTPUT_DIR / "example3-anchors.svg")


# =============================================================================
# Neighbor Connections in Grid
# =============================================================================

def example4_grid_neighbors():
    """Connect cells to their neighbors"""
    scene = Scene.with_grid(cols=5, rows=4, cell_size=60, background="#1a1a2e")
    colors = Palette.midnight()

    # Store dots for connections
    dots = {}

    for cell in scene.grid:
        dot = cell.add_dot(radius=8, color=colors.primary, z_index=10)
        dots[(cell.row, cell.col)] = dot

        # Connect to right neighbor
        if cell.right:
            dot_right = cell.right.add_dot(radius=8, color=colors.primary, z_index=10)
            dots[(cell.right.row, cell.right.col)] = dot_right

            conn = Connection(dot, dot_right, style={"width": 1, "color": colors.line})
            scene.add(conn)

        # Connect to bottom neighbor
        if cell.below:
            dot_below = dots.get((cell.below.row, cell.below.col))
            if dot_below:
                conn = Connection(dot, dot_below, style={"width": 1, "color": colors.line})
                scene.add(conn)

    scene.save(OUTPUT_DIR / "example4-grid-neighbors.svg")


# =============================================================================
# Connection Properties: Width and Opacity
# =============================================================================

def example5_properties():
    """Different connection widths and opacity"""
    scene = Scene(width=400, height=300, background="#1a1a2e")
    colors = Palette.ocean()

    # Create dots
    dot1 = Dot(100, 80, radius=12, color=colors.primary)
    dot2 = Dot(300, 80, radius=12, color=colors.primary)
    dot3 = Dot(100, 160, radius=12, color=colors.secondary)
    dot4 = Dot(300, 160, radius=12, color=colors.secondary)
    dot5 = Dot(100, 240, radius=12, color=colors.accent)
    dot6 = Dot(300, 240, radius=12, color=colors.accent)

    scene.add(dot1)
    scene.add(dot2)
    scene.add(dot3)
    scene.add(dot4)
    scene.add(dot5)
    scene.add(dot6)

    # Different widths
    scene.add(Connection(dot1, dot2, style={"width": 1, "color": colors.line}))
    scene.add(Connection(dot3, dot4, style={"width": 3, "color": colors.line}))
    scene.add(Connection(dot5, dot6, style={"width": 5, "color": colors.line}))

    scene.save(OUTPUT_DIR / "example5-properties.svg")


# =============================================================================
# Network Graph Pattern
# =============================================================================

def example6_network():
    """Create network with distance-based connections"""
    scene = Scene.with_grid(cols=8, rows=6, cell_size=50, background="#1a1a2e")
    colors = Palette.midnight()

    # Create dots in some cells
    dots = []
    for cell in scene.grid:
        if (cell.row + cell.col * 2) % 3 == 0:
            dot = cell.add_dot(radius=6, color=colors.primary, z_index=10)
            dots.append((dot, cell))

    # Connect nearby dots
    max_distance = 2.5

    for i, (dot1, cell1) in enumerate(dots):
        for dot2, cell2 in dots[i+1:]:
            dr = cell1.row - cell2.row
            dc = cell1.col - cell2.col
            distance = math.sqrt(dr*dr + dc*dc)

            if distance <= max_distance:
                opacity = 1 - (distance / max_distance)
                conn = Connection(dot1, dot2,
                    style={"width": 1, "color": colors.line})
                scene.add(conn)

    scene.save(OUTPUT_DIR / "example6-network.svg")


# =============================================================================
# Hub and Spoke Pattern
# =============================================================================

def example7_hub_spoke():
    """Central hub connected to multiple nodes"""
    scene = Scene.with_grid(cols=9, rows=9, cell_size=50, background="#1a1a2e")
    colors = Palette.ocean()

    # Central hub
    center = scene.grid[4, 4]
    hub = center.add_dot(radius=12, color=colors.accent, z_index=20)

    # Spokes to selected cells
    spoke_positions = [
        (0, 0), (0, 4), (0, 8),
        (4, 0), (4, 8),
        (8, 0), (8, 4), (8, 8)
    ]

    for row, col in spoke_positions:
        cell = scene.grid[row, col]
        spoke = cell.add_dot(radius=8, color=colors.primary, z_index=10)

        conn = Connection(hub, spoke, style={"width": 1, "color": colors.line})
        scene.add(conn)

    scene.save(OUTPUT_DIR / "example7-hub-spoke.svg")


# =============================================================================
# Layering: Connections Behind Entities
# =============================================================================

def example8_layering():
    """z_index - Connections behind entities"""
    scene = Scene.with_grid(cols=4, rows=3, cell_size=70, background="#1a1a2e")
    colors = Palette.midnight()

    # Create polygons in each cell
    dots = []
    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(size=0.8), fill=colors.primary, z_index=10)
        # Get center as connection point
        dot = cell.add_dot(radius=0, color="transparent", z_index=10)  # Invisible anchor
        dots.append(dot)

    # Connect all adjacent cells
    for cell in scene.grid:
        idx = cell.row * 4 + cell.col

        if cell.right:
            idx_right = cell.right.row * 4 + cell.right.col
            scene.add(Connection(dots[idx], dots[idx_right], style={"width": 1, "color": colors.line}))

        if cell.below:
            idx_below = cell.below.row * 4 + cell.below.col
            scene.add(Connection(dots[idx], dots[idx_below], style={"width": 1, "color": colors.line}))

    scene.save(OUTPUT_DIR / "example8-layering.svg")


# =============================================================================
# Connection Colors
# =============================================================================

def example9_colors():
    """Different colored connections"""
    scene = Scene(width=400, height=400, background="#1a1a2e")
    colors = Palette.ocean()

    # Create dots in circle
    n = 8
    center_x, center_y = 200, 200
    radius = 120

    dots = []
    for i in range(n):
        angle = i * 2 * math.pi / n
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        dot = Dot(x, y, radius=10, color=colors.primary)
        scene.add(dot)
        dots.append(dot)

    # Connect with different colors
    connection_colors = ["#ee4266", "#4ecca3", "#ffd23f", "#64ffda"]

    for i in range(n):
        next_i = (i + 1) % n
        color = connection_colors[i % len(connection_colors)]
        scene.add(Connection(dots[i], dots[next_i], style={"width": 2, "color": color}))

    scene.save(OUTPUT_DIR / "example9-colors.svg")


# =============================================================================
# Complete Example
# =============================================================================

def example10_complete():
    """Complex connection pattern"""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    # Create dots based on pattern
    dots = []
    for cell in scene.grid:
        if cell.brightness > 0.3 or (cell.row + cell.col) % 3 == 0:
            dot = cell.add_dot(radius=5, color=colors.primary, z_index=10)
            dots.append((dot, cell))

    # Connect nearby dots
    for i, (dot1, cell1) in enumerate(dots):
        for dot2, cell2 in dots[i+1:]:
            dr = cell1.row - cell2.row
            dc = cell1.col - cell2.col
            distance = math.sqrt(dr*dr + dc*dc)

            if distance < 2:
                scene.add(Connection(dot1, dot2, style={"width": 1, "color": colors.line}))

    scene.save(OUTPUT_DIR / "example10-complete.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-basic": example1_basic,
    "example2-multiple": example2_multiple,
    "example3-anchors": example3_anchors,
    "example4-grid-neighbors": example4_grid_neighbors,
    "example5-properties": example5_properties,
    "example6-network": example6_network,
    "example7-hub-spoke": example7_hub_spoke,
    "example8-layering": example8_layering,
    "example9-colors": example9_colors,
    "example10-complete": example10_complete,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for connections.md...")

    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")

    print(f"Complete! Generated to {OUTPUT_DIR}/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
