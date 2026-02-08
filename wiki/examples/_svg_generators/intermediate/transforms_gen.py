#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/transforms

Demonstrates rotation and scaling of polygons using the shapes module.
"""

from pyfreeform import Scene, Palette, Polygon
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "transforms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_rotating_hexagons():
    """Hexagons rotating based on grid position."""
    colors = Palette.midnight()
    color_cycle = [colors.primary, colors.secondary, colors.accent, "#64ffda"]
    scene = Scene.with_grid(
        cols=20, rows=20, cell_size=25, background=colors.background
    )

    for cell in scene.grid:
        angle = (cell.row + cell.col) * 15
        color = color_cycle[(cell.row + cell.col) % len(color_cycle)]
        cell.add_polygon(
            Polygon.hexagon(size=0.8), fill=color, rotation=angle, opacity=0.7,
        )

    scene.save(OUTPUT_DIR / "01_rotating_hexagons.svg")


def example_02_radial_rotation():
    """Hexagons rotate to point toward grid center."""
    import math

    colors = Palette.ocean()
    grid_size = 20
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=25, background=colors.background
    )

    center = grid_size / 2

    for cell in scene.grid:
        dr = cell.row - center
        dc = cell.col - center
        angle = math.degrees(math.atan2(dr, dc))

        dist = math.sqrt(dr * dr + dc * dc)
        max_dist = math.sqrt(center * center + center * center)
        brightness = 1 - (dist / max_dist)

        if brightness > 0.2:
            cell.add_polygon(
                Polygon.hexagon(size=0.7),
                fill=colors.primary, rotation=angle, opacity=brightness,
            )

    scene.save(OUTPUT_DIR / "02_radial_rotation.svg")


def example_03_spiral_pattern():
    """Stars with rotation increasing in a spiral."""
    import math

    colors = Palette.midnight()
    grid_size = 15
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=30, background=colors.background
    )

    center = grid_size / 2
    color_cycle = [colors.primary, colors.secondary, colors.accent]

    for cell in scene.grid:
        dr = cell.row - center
        dc = cell.col - center
        dist = math.sqrt(dr * dr + dc * dc)
        angle_from_center = math.degrees(math.atan2(dr, dc))

        rotation = angle_from_center + dist * 20
        color = color_cycle[int(dist) % len(color_cycle)]
        size = max(0.3, 0.8 - dist * 0.05)

        cell.add_polygon(
            Polygon.star(5, size=size), fill=color, rotation=rotation, opacity=0.7,
        )

    scene.save(OUTPUT_DIR / "03_spiral_pattern.svg")


GENERATORS = {
    "01_rotating_hexagons": example_01_rotating_hexagons,
    "02_radial_rotation": example_02_radial_rotation,
    "03_spiral_pattern": example_03_spiral_pattern,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for transforms examples...")

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
