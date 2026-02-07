#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/groups

Demonstrates organizing entities into patterns.
"""

import math
from pyfreeform import Scene, Palette, Dot
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "groups"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _add_flower(scene, cx, cy, scale, rotation, center_color, petal_color):
    """Create a flower pattern from dots at the given position."""
    scene.add(Dot(cx, cy, radius=10 * scale, color=center_color, opacity=0.8))

    rot_rad = math.radians(rotation)
    for i in range(8):
        angle = i * (2 * math.pi / 8) + rot_rad
        distance = 15 * scale
        x = cx + distance * math.cos(angle)
        y = cy + distance * math.sin(angle)
        scene.add(Dot(x, y, radius=6 * scale, color=petal_color, opacity=0.9))


def example_01_flower_groups():
    """Flower patterns composed from dots."""
    colors = Palette.midnight()
    scene = Scene(width=300, height=250, background=colors.background)

    _add_flower(scene, 75, 75, 1.0, 15, colors.primary, colors.secondary)
    _add_flower(scene, 225, 75, 0.8, -30, colors.secondary, colors.accent)
    _add_flower(scene, 150, 200, 1.2, 45, colors.accent, colors.primary)

    scene.save(OUTPUT_DIR / "01_flower_groups.svg")


def example_02_composite_shapes():
    """Concentric ring patterns using dots."""
    colors = Palette.ocean()
    scene = Scene(width=300, height=300, background=colors.background)

    cx, cy = 150, 150
    ring_colors = [colors.primary, colors.secondary, colors.accent]

    for ring_idx, (radius, n_dots, color) in enumerate([
        (30, 6, ring_colors[0]),
        (60, 12, ring_colors[1]),
        (90, 18, ring_colors[2]),
    ]):
        for i in range(n_dots):
            angle = i * (2 * math.pi / n_dots)
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            scene.add(Dot(x, y, radius=4, color=color))

    # Center dot
    scene.add(Dot(cx, cy, radius=8, color=colors.accent))

    scene.save(OUTPUT_DIR / "02_composite_shapes.svg")


def example_03_radial_groups():
    """Flower groups arranged radially around a center."""
    colors = Palette.midnight()
    scene = Scene(width=350, height=350, background=colors.background)

    cx, cy = 175, 175
    petal_colors = [colors.primary, colors.secondary, colors.accent, "#64ffda"]

    for i in range(6):
        angle = i * (2 * math.pi / 6)
        flower_x = cx + 80 * math.cos(angle)
        flower_y = cy + 80 * math.sin(angle)
        petal_color = petal_colors[i % len(petal_colors)]

        _add_flower(
            scene, flower_x, flower_y,
            scale=0.6, rotation=math.degrees(angle),
            center_color=colors.primary, petal_color=petal_color,
        )

    # Central flower
    _add_flower(scene, cx, cy, 0.8, 0, colors.accent, colors.primary)

    scene.save(OUTPUT_DIR / "03_radial_groups.svg")


GENERATORS = {
    "01_flower_groups": example_01_flower_groups,
    "02_composite_shapes": example_02_composite_shapes,
    "03_radial_groups": example_03_radial_groups,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for groups examples...")

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
