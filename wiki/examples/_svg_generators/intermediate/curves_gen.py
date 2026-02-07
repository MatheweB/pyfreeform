#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/curves

Demonstrates quadratic Bezier curves with parametric positioning.
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "curves"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_flowing_curves():
    """Curves in each cell with dots positioned along them by brightness."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=30, rows=30, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        brightness = (math.sin(cell.col * 0.15) * math.cos(cell.row * 0.15) + 1) / 2

        if 0.3 < brightness < 0.7:
            curve = cell.add_curve(
                start="bottom_left", end="top_right",
                curvature=0.5, color=colors.primary, width=1, opacity=0.5,
            )
            cell.add_dot(along=curve, t=brightness, radius=2, color=colors.secondary)

    scene.save(OUTPUT_DIR / "01_flowing_curves.svg")


def example_02_varying_curvature():
    """Curvature varies based on cell position."""
    colors = Palette.ocean()
    scene = Scene.with_grid(
        cols=20, rows=20, cell_size=25, background=colors.background
    )

    for cell in scene.grid:
        # Curvature ranges from -0.8 to 0.8 across the grid
        curvature = (cell.col / 20 - 0.5) * 1.6

        curve = cell.add_curve(
            start="bottom_left", end="top_right",
            curvature=curvature, color=colors.primary, width=1, opacity=0.5,
        )
        t = cell.row / 20
        cell.add_dot(along=curve, t=t, radius=2, color=colors.accent)

    scene.save(OUTPUT_DIR / "02_varying_curvature.svg")


def example_03_multiple_dots():
    """Multiple dots distributed along each curve."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=15, rows=15, cell_size=30, background=colors.background
    )

    for cell in scene.grid:
        curve = cell.add_curve(
            start="bottom_left", end="top_right",
            curvature=0.5, color=colors.line, width=0.5, opacity=0.3,
        )
        for i in range(5):
            t = (i + 0.5) / 5
            cell.add_dot(along=curve, t=t, radius=2, color=colors.secondary)

    scene.save(OUTPUT_DIR / "03_multiple_dots.svg")


GENERATORS = {
    "01_flowing_curves": example_01_flowing_curves,
    "02_varying_curvature": example_02_varying_curvature,
    "03_multiple_dots": example_03_multiple_dots,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for curves examples...")

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
