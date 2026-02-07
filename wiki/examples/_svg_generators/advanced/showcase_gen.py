#!/usr/bin/env python3
"""
SVG Generator for: examples/advanced/showcase

Integrates multiple PyFreeform features: curves, transforms, connections,
text, parametric positioning, and layering.
"""

import math
from pyfreeform import Scene, Palette, Dot, Text, Connection, shapes
from pyfreeform.core.point import Point
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "showcase"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_comprehensive():
    """Comprehensive showcase: grid, curves, parametric dots, polygons, text."""
    colors = Palette.midnight()
    scene = Scene(width=500, height=400, background="#0d1117")

    # Title (z=30)
    scene.add(Text(
        250, 30, "Feature Showcase",
        font_size=28, color=colors.primary, text_anchor="middle", bold=True,
        z_index=30,
    ))

    # Flowing curves with parametric dots (z=10)
    for start_y in [100, 200, 300]:
        curve = scene.add_curve(
            start=Point(50, start_y), end=Point(450, start_y),
            curvature=-0.15, color=colors.primary, width=2, opacity=0.6,
            z_index=10,
        )
        for i, t in enumerate([0.0, 0.25, 0.5, 0.75, 1.0]):
            radius = 4 + t * 4
            color = colors.secondary if i % 2 == 0 else colors.accent
            scene.add_dot(along=curve, t=t, radius=radius, color=color, z_index=15)

    # Rotating hexagons at bottom (z=20)
    hex_positions = [
        (100, 360, 45, colors.primary),
        (250, 360, -30, colors.secondary),
        (400, 360, 15, colors.accent),
    ]
    for x, y, angle, color in hex_positions:
        # Compute hexagon vertices at absolute position
        verts = []
        angle_rad = math.radians(angle)
        for i in range(6):
            a = i * math.pi / 3 + angle_rad
            verts.append(Point(x + 15 * math.cos(a), y + 15 * math.sin(a)))
        from pyfreeform import Polygon
        scene.add(Polygon(verts, fill=color, opacity=0.8, z_index=20))

    # Legend (z=30)
    scene.add(Text(
        20, 390, "Parametric Paths | Transforms | Layering | Typography",
        font_size=10, color="#6b7280", font_family="monospace", z_index=30,
    ))

    scene.save(OUTPUT_DIR / "01_comprehensive.svg")


def example_02_all_features():
    """Grid-based showcase combining cell builders and scene builders."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=20, rows=15, cell_size=20, background="#0d1117",
    )
    color_cycle = [colors.primary, colors.secondary, colors.accent, "#64ffda"]

    # Cell-level: rotating shapes + parametric dots
    for cell in scene.grid:
        # Checkerboard fill (z=0)
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.primary, opacity=0.03)

        # Curves with dots in every 3rd cell (z=5)
        if cell.row % 3 == 1 and cell.col % 3 == 1:
            curve = cell.add_curve(
                start="bottom_left", end="top_right",
                curvature=0.4, color=colors.line, width=0.5, opacity=0.3,
                z_index=5,
            )
            t = ((cell.row + cell.col) % 10) / 10
            cell.add_dot(
                along=curve, t=t, radius=2,
                color=color_cycle[(cell.row + cell.col) % 4],
                z_index=10,
            )

        # Stars in corners (z=15)
        if cell.row < 3 and cell.col < 3:
            angle = (cell.row + cell.col) * 30
            cell.add_polygon(
                shapes.star(5, size=0.6), fill=colors.accent,
                rotation=angle, opacity=0.6, z_index=15,
            )

    # Scene-level overlay text
    scene.add_text(
        "PyFreeform Feature Showcase", at=(0.5, 0.06),
        font_size=16, color=colors.accent, z_index=30,
    )
    scene.add_text(
        "Grid + Curves + Shapes + Parametric Positioning", at=(0.5, 0.95),
        font_size=9, color="#6b7280", font_family="monospace", z_index=30,
    )

    scene.save(OUTPUT_DIR / "02_all_features.svg")


GENERATORS = {
    "01_comprehensive": example_01_comprehensive,
    "02_all_features": example_02_all_features,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for showcase examples...")

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
