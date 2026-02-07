#!/usr/bin/env python3
"""
SVG Generator for: examples/beginner/grid-patterns

Demonstrates grid selection methods: checkerboard, border, stripes.
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "grid-patterns"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_checkerboard():
    """Checkerboard pattern using cell fills."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=15, rows=15, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.2)

    scene.save(OUTPUT_DIR / "01_checkerboard.svg")


def example_02_border_highlight():
    """Border cells highlighted with dots."""
    colors = Palette.midnight()
    grid_cols, grid_rows = 15, 15
    scene = Scene.with_grid(
        cols=grid_cols, rows=grid_rows, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        is_edge = (
            cell.row == 0
            or cell.row == grid_rows - 1
            or cell.col == 0
            or cell.col == grid_cols - 1
        )
        if is_edge:
            cell.add_dot(color=colors.secondary, radius=5)

    scene.save(OUTPUT_DIR / "02_border_highlight.svg")


def example_03_stripe_patterns():
    """Diagonal stripe pattern with dots."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=15, rows=15, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        if (cell.row + cell.col) % 4 == 0:
            cell.add_dot(color=colors.accent, radius=3)

    scene.save(OUTPUT_DIR / "03_stripe_patterns.svg")


def example_04_radial_selection():
    """Distance-based radial pattern."""
    colors = Palette.midnight()
    grid_size = 15
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=20, background=colors.background
    )

    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)

    for cell in scene.grid:
        dist = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = 1 - (dist / max_dist)

        if brightness > 0.5:
            cell.add_dot(color=colors.primary, radius=3 + brightness * 4)
        elif brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=2)

    scene.save(OUTPUT_DIR / "04_radial_selection.svg")


GENERATORS = {
    "01_checkerboard": example_01_checkerboard,
    "02_border_highlight": example_02_border_highlight,
    "03_stripe_patterns": example_03_stripe_patterns,
    "04_radial_selection": example_04_radial_selection,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for grid-patterns examples...")

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
