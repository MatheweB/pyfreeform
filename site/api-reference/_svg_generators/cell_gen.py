#!/usr/bin/env python3
"""
SVG Generator for: api-reference/cell.md

Generates visual examples demonstrating Cell API methods and properties.
"""

from pyfreeform import Scene, Palette, shapes
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "cell"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Named Positions
# =============================================================================

def example1_named_positions():
    """cell.top_left, cell.center, etc - Named position properties"""
    scene = Scene.with_grid(cols=3, rows=3, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    # Get center cell
    cell = scene.grid[1, 1]

    # Show cell boundary
    cell.add_border(color=colors.grid, width=2)

    # Add dots at named positions
    cell.add_dot(at="top_left", radius=5, color="#ee4266")
    cell.add_dot(at="top", radius=5, color="#ffd23f")
    cell.add_dot(at="top_right", radius=5, color="#ee4266")
    cell.add_dot(at="left", radius=5, color="#ffd23f")
    cell.add_dot(at="center", radius=5, color="#64ffda")
    cell.add_dot(at="right", radius=5, color="#ffd23f")
    cell.add_dot(at="bottom_left", radius=5, color="#ee4266")
    cell.add_dot(at="bottom", radius=5, color="#ffd23f")
    cell.add_dot(at="bottom_right", radius=5, color="#ee4266")

    scene.save(OUTPUT_DIR / "example1-named-positions.svg")


# =============================================================================
# Neighbor Access
# =============================================================================

def example2_neighbor_access():
    """cell.right, cell.below - Neighbor cell access"""
    scene = Scene.with_grid(cols=5, rows=5, cell_size=50, background="#1a1a2e")
    colors = Palette.ocean()

    # Connect cells to their neighbors
    from pyfreeform import Connection
    for cell in scene.grid:
        # Add dot at center of each cell
        dot1 = cell.add_dot(radius=6, color=colors.primary, z_index=10)

        # Connect to right neighbor
        if cell.right:
            dot2 = cell.right.add_dot(radius=6, color=colors.primary, z_index=10)
            conn = Connection(start=dot1, end=dot2, style={"color": colors.line, "width": 1, "z_index": 0})
            scene.add(conn)

        # Connect to bottom neighbor
        if cell.below:
            dot2 = cell.below.add_dot(radius=6, color=colors.primary, z_index=10)
            conn = Connection(start=dot1, end=dot2, style={"color": colors.line, "width": 1, "z_index": 0})
            scene.add(conn)

    scene.save(OUTPUT_DIR / "example2-neighbor-access.svg")


# =============================================================================
# add_dot()
# =============================================================================

def example3_add_dot():
    """cell.add_dot() - Add dots to cells"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different dot sizes
    cells[0].add_dot(radius=5, color=colors.primary)
    cells[1].add_dot(radius=10, color=colors.secondary)
    cells[2].add_dot(radius=15, color=colors.accent)
    cells[3].add_dot(at="top_left", radius=8, color="#ee4266")

    scene.save(OUTPUT_DIR / "example3-add-dot.svg")


# =============================================================================
# add_line()
# =============================================================================

def example4_add_line():
    """cell.add_line() - Add lines within cells"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different line styles
    cells[0].add_line(start="left", end="right", color=colors.primary, width=2)
    cells[1].add_line(start="top", end="bottom", color=colors.secondary, width=2)
    cells[2].add_line(start="bottom_left", end="top_right", color=colors.accent, width=2)
    cells[3].add_line(start=(0.2, 0.3), end=(0.8, 0.7), color="#ffd23f", width=3)

    scene.save(OUTPUT_DIR / "example4-add-line.svg")


# =============================================================================
# add_curve()
# =============================================================================

def example5_add_curve():
    """cell.add_curve() - Add curves within cells"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different curvature values
    cells[0].add_curve(curvature=0.3, color=colors.primary, width=2)
    cells[1].add_curve(curvature=0.5, color=colors.secondary, width=2)
    cells[2].add_curve(curvature=-0.5, color=colors.accent, width=2)
    cells[3].add_curve(start="top", end="bottom", curvature=0.4, color="#64ffda", width=2)

    scene.save(OUTPUT_DIR / "example5-add-curve.svg")


# =============================================================================
# add_ellipse()
# =============================================================================

def example6_add_ellipse():
    """cell.add_ellipse() - Add ellipses and circles"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different ellipse styles
    cells[0].add_ellipse(rx=15, ry=15, fill=colors.primary)  # Circle
    cells[1].add_ellipse(rx=25, ry=15, fill=colors.secondary)  # Horizontal oval
    cells[2].add_ellipse(rx=15, ry=25, fill=colors.accent)  # Vertical oval
    cells[3].add_ellipse(rx=20, ry=12, rotation=45, fill="#ffd23f")  # Rotated

    scene.save(OUTPUT_DIR / "example6-add-ellipse.svg")


# =============================================================================
# add_polygon()
# =============================================================================

def example7_add_polygon():
    """cell.add_polygon() - Add polygons with shape helpers"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different shapes
    cells[0].add_polygon(shapes.triangle(size=0.8), fill=colors.primary)
    cells[1].add_polygon(shapes.hexagon(size=0.8), fill=colors.secondary)
    cells[2].add_polygon(shapes.star(5), fill=colors.accent)
    cells[3].add_polygon(shapes.squircle(n=4), fill="#64ffda")

    scene.save(OUTPUT_DIR / "example7-add-polygon.svg")


# =============================================================================
# add_text()
# =============================================================================

def example8_add_text():
    """cell.add_text() - Add text labels"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different text styles
    cells[0].add_text("A", font_size=24, color=colors.primary)
    cells[1].add_text("B", font_size=32, color=colors.secondary)
    cells[2].add_text("C", font_size=20, color=colors.accent, rotation=45)
    cells[3].add_text("D", font_size=28, color="#ffd23f", font_family="monospace")

    scene.save(OUTPUT_DIR / "example8-add-text.svg")


# =============================================================================
# add_fill() and add_border()
# =============================================================================

def example9_fill_border():
    """cell.add_fill() and cell.add_border() - Fill and border cells"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different combinations
    cells[0].add_fill(color=colors.primary)
    cells[1].add_border(color=colors.secondary, width=2)
    cells[2].add_fill(color=colors.accent, z_index=0)
    cells[2].add_border(color=colors.line, width=2, z_index=10)
    cells[3].add_fill(color="#1a1a2e")
    cells[3].add_dot(radius=15, color="#64ffda")

    scene.save(OUTPUT_DIR / "example9-fill-border.svg")


# =============================================================================
# Convenience Methods: add_cross() and add_x()
# =============================================================================

def example10_cross_and_x():
    """Creating cross and X patterns with lines"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Cross pattern (horizontal + vertical)
    cells[0].add_line(start="top", end="bottom", color=colors.primary, width=2)
    cells[0].add_line(start="left", end="right", color=colors.primary, width=2)

    # X pattern (two diagonals)
    cells[1].add_diagonal(start="top_left", end="bottom_right", color=colors.secondary, width=2)
    cells[1].add_diagonal(start="bottom_left", end="top_right", color=colors.secondary, width=2)

    # Single diagonal up-right
    cells[2].add_diagonal(start="bottom_left", end="top_right", color=colors.accent, width=3)

    # Single diagonal down-right
    cells[3].add_diagonal(start="top_left", end="bottom_right", color="#ffd23f", width=3)

    scene.save(OUTPUT_DIR / "example10-cross-and-x.svg")


# =============================================================================
# Layering with z_index
# =============================================================================

def example11_layering():
    """z_index - Layer elements within cells"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Cell 0: Background -> Dot -> Border
    cells[0].add_fill(color=colors.background, z_index=0)
    cells[0].add_dot(radius=20, color=colors.primary, z_index=5)
    cells[0].add_border(color=colors.accent, width=2, z_index=10)

    # Cell 1: Overlapping dots
    cells[1].add_dot(at=(0.4, 0.5), radius=18, color=colors.primary, z_index=0)
    cells[1].add_dot(at=(0.6, 0.5), radius=18, color=colors.secondary, z_index=5)

    # Cell 2: Complex layering
    cells[2].add_fill(color="#0a3d62", z_index=0)
    cells[2].add_polygon(shapes.hexagon(size=0.9), fill=colors.primary, z_index=3)
    cells[2].add_dot(radius=12, color=colors.accent, z_index=10)

    scene.save(OUTPUT_DIR / "example11-layering.svg")


# =============================================================================
# Complete Example
# =============================================================================

def example12_complete():
    """Complete cell example - Combining multiple methods"""
    scene = Scene.with_grid(cols=6, rows=4, cell_size=60, background="#1a1a2e")
    colors = Palette.midnight()

    for cell in scene.grid:
        # Background
        cell.add_fill(color=colors.background, z_index=0)

        # Different patterns based on position
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(radius=8, color=colors.primary, z_index=5)
        else:
            cell.add_polygon(shapes.diamond(size=0.6), fill=colors.secondary, z_index=5)

        # Border on edge cells
        if cell.row == 0 or cell.col == 0 or cell.row == 3 or cell.col == 5:
            cell.add_border(color=colors.accent, width=2, z_index=10)

    scene.save(OUTPUT_DIR / "example12-complete.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-named-positions": example1_named_positions,
    "example2-neighbor-access": example2_neighbor_access,
    "example3-add-dot": example3_add_dot,
    "example4-add-line": example4_add_line,
    "example5-add-curve": example5_add_curve,
    "example6-add-ellipse": example6_add_ellipse,
    "example7-add-polygon": example7_add_polygon,
    "example8-add-text": example8_add_text,
    "example9-fill-border": example9_fill_border,
    "example10-cross-and-x": example10_cross_and_x,
    "example11-layering": example11_layering,
    "example12-complete": example12_complete,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for cell.md...")

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
