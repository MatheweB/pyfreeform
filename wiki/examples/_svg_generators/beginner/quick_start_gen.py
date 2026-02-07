#!/usr/bin/env python3
"""
SVG Generator for: examples/beginner/quick-start

Simple dot art from synthetic brightness data.
"""

import math
from pyfreeform import Scene
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "quick-start"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_simple_dot_art():
    """Simple radial gradient dot pattern."""
    grid_size = 30
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=12, background="#1a1a2e"
    )

    center = grid_size / 2
    max_distance = math.sqrt(center**2 + center**2)

    for cell in scene.grid:
        distance = math.sqrt((cell.col - center) ** 2 + (cell.row - center) ** 2)
        brightness = 1 - (distance / max_distance)

        color_val = int(brightness * 255)
        color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"

        cell.add_dot(color=color, radius=4)

    scene.save(OUTPUT_DIR / "01_simple_dot_art.svg")


GENERATORS = {
    "01_simple_dot_art": example_01_simple_dot_art,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for quick-start examples...")

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
