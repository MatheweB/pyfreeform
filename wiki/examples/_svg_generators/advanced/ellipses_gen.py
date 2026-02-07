#!/usr/bin/env python3
"""
SVG Generator for: examples/advanced/ellipses

Demonstrates rotated ellipses and parametric positioning along them.
"""

import math
from pyfreeform import Scene, Palette
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "ellipses"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_radial_ellipses():
    """Ellipses rotated to point away from center, sized by distance."""
    colors = Palette.midnight()
    grid_size = 30
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=15, background=colors.background
    )

    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)

    for cell in scene.grid:
        dr = cell.row - center
        dc = cell.col - center
        distance = math.sqrt(dr * dr + dc * dc)
        angle = math.degrees(math.atan2(dr, dc))
        brightness = 1 - (distance / max_dist)

        if brightness < 0.2:
            continue

        scale = 0.3 + brightness * 0.7
        color_val = int(brightness * 255)
        color = f"#{color_val:02x}{int(color_val * 0.8):02x}{int(color_val * 0.6):02x}"

        cell.add_ellipse(
            rx=12 * scale, ry=6 * scale,
            rotation=angle, fill=color, opacity=0.7,
        )

    scene.save(OUTPUT_DIR / "01_radial_ellipses.svg")


def example_02_orbital_rings():
    """Concentric elliptical rings with dots along the perimeter."""
    colors = Palette.ocean()
    scene = Scene(width=300, height=300, background=colors.background)

    ring_colors = [colors.primary, colors.secondary, colors.accent]

    for ring_idx, (rx, ry, n_dots) in enumerate([
        (40, 30, 8),
        (80, 60, 16),
        (120, 90, 24),
    ]):
        ellipse = scene.add_ellipse(
            at=(0.5, 0.5), rx=rx, ry=ry,
            fill="none", stroke=ring_colors[ring_idx], stroke_width=1, opacity=0.4,
        )
        color = ring_colors[ring_idx]
        for i in range(n_dots):
            t = i / n_dots
            scene.add_dot(along=ellipse, t=t, radius=3, color=color, z_index=1)

    scene.save(OUTPUT_DIR / "02_orbital_rings.svg")


def example_03_parametric_dots():
    """Dots positioned parametrically along rotated cell ellipses."""
    colors = Palette.midnight()
    grid_size = 20
    scene = Scene.with_grid(
        cols=grid_size, rows=grid_size, cell_size=20, background=colors.background
    )

    center = grid_size / 2
    max_dist = math.sqrt(center**2 + center**2)

    for cell in scene.grid:
        dr = cell.row - center
        dc = cell.col - center
        distance = math.sqrt(dr * dr + dc * dc)
        angle = math.degrees(math.atan2(dr, dc))
        brightness = 1 - (distance / max_dist)

        if brightness < 0.3:
            continue

        scale = 0.4 + brightness * 0.6
        ellipse = cell.add_ellipse(
            rx=10 * scale, ry=5 * scale,
            rotation=angle, fill=colors.primary, opacity=0.3,
        )

        # Dot along ellipse at brightness-driven position
        cell.add_dot(along=ellipse, t=brightness, radius=2, color=colors.secondary)

    scene.save(OUTPUT_DIR / "03_parametric_dots.svg")


GENERATORS = {
    "01_radial_ellipses": example_01_radial_ellipses,
    "02_orbital_rings": example_02_orbital_rings,
    "03_parametric_dots": example_03_parametric_dots,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for ellipses examples...")

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
