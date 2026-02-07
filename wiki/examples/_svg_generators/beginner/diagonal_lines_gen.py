#!/usr/bin/env python3
"""
SVG Generator for: examples/beginner/diagonal-lines

Demonstrates parametric positioning along diagonal lines.
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "diagonal-lines"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _wave_brightness(col, row):
    """Compute wave-based brightness."""
    return (math.sin(col * 0.2) * math.cos(row * 0.2) + 1) / 2


def example_01_sliding_dots():
    """Diagonal lines with dots positioned along them by brightness."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=30, rows=30, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row)
        line = cell.add_diagonal(
            start="bottom_left", end="top_right",
            color=colors.primary, width=0.5, opacity=0.3,
        )
        cell.add_dot(along=line, t=brightness, radius=3, color=colors.secondary)

    scene.save(OUTPUT_DIR / "01_sliding_dots.svg")


def example_02_brightness_driven():
    """Dot color and size vary with brightness."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=30, rows=30, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row)
        line = cell.add_diagonal(
            start="bottom_left", end="top_right",
            color=colors.line, width=0.5, opacity=0.2,
        )

        if brightness > 0.6:
            color, radius = colors.accent, 4
        elif brightness > 0.3:
            color, radius = colors.secondary, 3
        else:
            color, radius = colors.primary, 2

        cell.add_dot(along=line, t=brightness, radius=radius, color=color)

    scene.save(OUTPUT_DIR / "02_brightness_driven.svg")


def example_03_inverted_position():
    """Dots slide in opposite direction: t = 1 - brightness."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=30, rows=30, cell_size=20, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row)
        line = cell.add_diagonal(
            start="bottom_left", end="top_right",
            color=colors.primary, width=0.5, opacity=0.3,
        )
        cell.add_dot(along=line, t=1 - brightness, radius=3, color=colors.accent)

    scene.save(OUTPUT_DIR / "03_inverted_position.svg")


GENERATORS = {
    "01_sliding_dots": example_01_sliding_dots,
    "02_brightness_driven": example_02_brightness_driven,
    "03_inverted_position": example_03_inverted_position,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for diagonal-lines examples...")

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
