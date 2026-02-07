#!/usr/bin/env python3
"""
SVG Generator for: examples/beginner/custom-dots

Demonstrates palettes and brightness-based sizing.
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "custom-dots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _wave_brightness(col, row, freq_x=0.3, freq_y=0.3):
    """Compute wave-based brightness for a cell position."""
    return (math.sin(col * freq_x) + math.cos(row * freq_y) + 2) / 4


def example_01_brightness_tiers():
    """Wave pattern with three brightness tiers using midnight palette."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=40, rows=40, cell_size=10, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row)

        if brightness > 0.6:
            cell.add_dot(color=colors.primary, radius=5 + brightness * 5)
        elif brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=3 + brightness * 4)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "01_brightness_tiers.svg")


def example_02_palette_variation():
    """Same wave pattern with ocean palette for comparison."""
    colors = Palette.ocean()
    scene = Scene.with_grid(
        cols=40, rows=40, cell_size=10, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row)

        if brightness > 0.6:
            cell.add_dot(color=colors.primary, radius=5 + brightness * 5)
        elif brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=3 + brightness * 4)
        else:
            cell.add_dot(color=colors.accent, radius=2)

    scene.save(OUTPUT_DIR / "02_palette_variation.svg")


def example_03_size_scaling():
    """Brightness directly controls dot size, single color."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=40, rows=40, cell_size=10, background=colors.background
    )

    for cell in scene.grid:
        brightness = _wave_brightness(cell.col, cell.row, 0.2, 0.2)
        radius = 1 + brightness * 8
        cell.add_dot(color=colors.primary, radius=radius)

    scene.save(OUTPUT_DIR / "03_size_scaling.svg")


GENERATORS = {
    "01_brightness_tiers": example_01_brightness_tiers,
    "02_palette_variation": example_02_palette_variation,
    "03_size_scaling": example_03_size_scaling,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for custom-dots examples...")

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
