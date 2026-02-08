#!/usr/bin/env python3
"""
SVG Generator for: examples/beginner/polygon-gallery

Showcases all built-in polygon shapes using the shapes module.
"""

from pyfreeform import Scene, Palette, Polygon
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "polygon-gallery"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_basic_shapes():
    """Triangle, square, diamond, hexagon."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=4, rows=1, cell_size=80, background=colors.background
    )
    cells = list(scene.grid)

    cells[0].add_polygon(Polygon.triangle(size=0.8), fill=colors.primary, opacity=0.8)
    cells[1].add_polygon(Polygon.square(size=0.7), fill=colors.secondary, opacity=0.8)
    cells[2].add_polygon(Polygon.diamond(size=0.8), fill=colors.accent, opacity=0.8)
    cells[3].add_polygon(Polygon.hexagon(size=0.8), fill="#64ffda", opacity=0.8)

    scene.save(OUTPUT_DIR / "01_basic_Polygon.svg")


def example_02_stars():
    """Star variations: 5, 6, and 8 pointed."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=3, rows=1, cell_size=80, background=colors.background
    )
    cells = list(scene.grid)

    cells[0].add_polygon(Polygon.star(5), fill=colors.primary, opacity=0.8)
    cells[1].add_polygon(Polygon.star(6), fill=colors.secondary, opacity=0.8)
    cells[2].add_polygon(Polygon.star(8), fill=colors.accent, opacity=0.8)

    scene.save(OUTPUT_DIR / "02_stars.svg")


def example_03_regular_polygons():
    """Pentagon through octagon using regular_polygon."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=4, rows=1, cell_size=80, background=colors.background
    )
    cells = list(scene.grid)
    color_cycle = [colors.primary, colors.secondary, colors.accent, "#64ffda"]

    for i, n_sides in enumerate([5, 6, 7, 8]):
        cells[i].add_polygon(
            Polygon.regular_polygon(n_sides, size=0.8),
            fill=color_cycle[i],
            opacity=0.8,
        )

    scene.save(OUTPUT_DIR / "03_regular_polygons.svg")


def example_04_all_shapes():
    """Comprehensive gallery of all shapes in a grid."""
    colors = Palette.midnight()
    scene = Scene.with_grid(
        cols=5, rows=2, cell_size=60, background=colors.background
    )
    cells = list(scene.grid)
    color_cycle = [
        colors.primary, colors.secondary, colors.accent, "#64ffda",
        colors.primary, colors.secondary, colors.accent, "#64ffda",
        colors.primary, colors.secondary,
    ]

    shape_list = [
        Polygon.triangle(size=0.8),
        Polygon.square(size=0.7),
        Polygon.diamond(size=0.8),
        Polygon.hexagon(size=0.8),
        Polygon.star(5),
        Polygon.star(6),
        Polygon.regular_polygon(5, size=0.8),
        Polygon.regular_polygon(8, size=0.8),
        Polygon.squircle(n=4),
        Polygon.star(8),
    ]

    for i, (shape_verts, color) in enumerate(zip(shape_list, color_cycle)):
        if i < len(cells):
            cells[i].add_polygon(
                shape_verts, fill=color,
                stroke="#64ffda", stroke_width=0.5, opacity=0.8,
            )

    scene.save(OUTPUT_DIR / "04_all_Polygon.svg")


GENERATORS = {
    "01_basic_shapes": example_01_basic_shapes,
    "02_stars": example_02_stars,
    "03_regular_polygons": example_03_regular_polygons,
    "04_all_shapes": example_04_all_shapes,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for polygon-gallery examples...")

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
