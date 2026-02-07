#!/usr/bin/env python3
"""
SVG Generator for: examples/advanced/multi-layer

Demonstrates strategic z-index management and layering.
"""

import math
from pyfreeform import Scene, Palette, Dot, Line, Ellipse, Connection
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "multi-layer"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_layered_composition():
    """Five-layer composition with grid, ellipses, connections, nodes, highlights."""
    colors = Palette.midnight()
    grid_size = 25
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=16,
        background="#0d1117",
    )

    # Layer 1 (z=0): Grid borders
    for cell in scene.grid:
        cell.add_border(color="#1a1a2e", width=0.5, opacity=0.3)

    # Layer 2 (z=5): Background ellipses every 5 cells
    for cell in scene.grid:
        if cell.row % 5 == 2 and cell.col % 5 == 2:
            cell.add_ellipse(rx=32, ry=24, fill="#374151", opacity=0.2, z_index=5)

    # Layers 3-5: Network nodes + connections + highlights
    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)
    bright_cells = []

    for cell in scene.grid:
        dist = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = 1 - (dist / max_dist)

        if brightness > 0.5:
            radius = 2 + brightness * 4
            dot = cell.add_dot(
                color=colors.primary, radius=radius, z_index=20,
            )
            bright_cells.append((dot, cell.row, cell.col, radius))

            # Layer 5 (z=30): Highlights on brightest nodes
            if radius > 5:
                cell.add_dot(
                    color="white", radius=radius * 0.3, opacity=0.8, z_index=30,
                )

    # Layer 3 (z=10): Connections between nearby bright nodes
    for i, (dot1, r1, c1, _) in enumerate(bright_cells):
        for dot2, r2, c2, _ in bright_cells[i + 1 : i + 3]:
            dr, dc = r1 - r2, c1 - c2
            dist = math.sqrt(dr * dr + dc * dc)
            if dist < 4:
                opacity = (1 - dist / 4) * 0.5
                conn = Connection(
                    dot1, dot2,
                    start_anchor="center", end_anchor="center",
                    style={"width": 0.5, "color": "#64ffda", "opacity": opacity},
                )
                scene.add(conn)

    scene.save(OUTPUT_DIR / "01_layered_composition.svg")


def example_02_depth_effect():
    """Overlapping layers create depth: large faint shapes behind small bright ones."""
    colors = Palette.ocean()
    grid_size = 20
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=20,
        background=colors.background,
    )

    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)

    for cell in scene.grid:
        dist = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = 1 - (dist / max_dist)

        # Background layer: large faint ellipses
        if brightness > 0.3:
            cell.add_ellipse(
                rx=12, ry=12, fill=colors.primary, opacity=0.1, z_index=0,
            )

        # Middle layer: medium dots
        if brightness > 0.5:
            cell.add_dot(
                color=colors.secondary, radius=3 + brightness * 3, z_index=10,
            )

        # Top layer: small bright highlights
        if brightness > 0.7:
            cell.add_dot(
                color=colors.accent, radius=2, z_index=20,
            )

    scene.save(OUTPUT_DIR / "02_depth_effect.svg")


def example_03_complex_layering():
    """Multiple entity types layered with precise z-index control."""
    colors = Palette.midnight()
    grid_size = 20
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=20,
        background="#0d1117",
    )

    for cell in scene.grid:
        # z=0: Faint grid borders
        cell.add_border(color="#1a1a2e", width=0.3, opacity=0.2)

        # z=5: Checkerboard fills
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.05, z_index=5)

        # z=10: Diagonal lines on every 3rd cell
        if (cell.row + cell.col) % 3 == 0:
            cell.add_diagonal(
                start="bottom_left", end="top_right",
                color=colors.line, width=0.5, opacity=0.3, z_index=10,
            )

        # z=20: Dots on every 4th cell
        if (cell.row + cell.col) % 4 == 0:
            cell.add_dot(color=colors.secondary, radius=3, z_index=20)

    scene.save(OUTPUT_DIR / "03_complex_layering.svg")


GENERATORS = {
    "01_layered_composition": example_01_layered_composition,
    "02_depth_effect": example_02_depth_effect,
    "03_complex_layering": example_03_complex_layering,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for multi-layer examples...")

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
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
