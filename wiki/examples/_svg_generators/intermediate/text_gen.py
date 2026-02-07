#!/usr/bin/env python3
"""
SVG Generator for: examples/intermediate/text

Demonstrates typography features: alignment, rotation, sizing.
"""

from pyfreeform import Scene, Palette, Dot, Text
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "text"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_alignment():
    """Text alignment: start, middle, end."""
    colors = Palette.midnight()
    scene = Scene(width=350, height=150, background=colors.background)

    # Title
    scene.add(Text(
        175, 30, "Typography Gallery",
        font_size=24, color=colors.primary, text_anchor="middle", bold=True,
    ))

    # Alignments
    scene.add(Text(
        50, 80, "Start Aligned",
        font_size=14, color=colors.secondary, text_anchor="start",
    ))
    scene.add(Text(
        175, 80, "Middle Aligned",
        font_size=14, color=colors.accent, text_anchor="middle",
    ))
    scene.add(Text(
        300, 80, "End Aligned",
        font_size=14, color=colors.primary, text_anchor="end",
    ))

    scene.save(OUTPUT_DIR / "01_alignment.svg")


def example_02_font_families():
    """Different font families and styles."""
    colors = Palette.midnight()
    scene = Scene(width=350, height=200, background=colors.background)

    scene.add(Text(50, 40, "Sans-serif", font_size=16, color=colors.primary))
    scene.add(Text(50, 70, "Serif", font_size=16, color=colors.secondary, font_family="serif"))
    scene.add(Text(50, 100, "Monospace", font_size=16, color=colors.accent, font_family="monospace"))

    # Rotated text
    for angle in [0, 45, 90, 135]:
        scene.add(Text(
            250, 100, f"{angle}\u00b0",
            font_size=12, color=colors.primary, rotation=angle,
        ))

    scene.save(OUTPUT_DIR / "02_font_families.svg")


def example_03_data_labels():
    """Data points with value labels."""
    colors = Palette.midnight()
    scene = Scene(width=350, height=150, background=colors.background)

    data_points = [
        (75, 75, 15, 0.82, colors.primary),
        (175, 75, 20, 0.95, colors.secondary),
        (275, 75, 10, 0.42, colors.accent),
    ]

    for x, y, radius, value, color in data_points:
        scene.add(Dot(x, y, radius=radius, color=color, opacity=0.5))
        scene.add(Text(
            x, y + 5, f"{value:.2f}",
            font_size=10, color="white", font_family="monospace", text_anchor="middle",
        ))

    scene.save(OUTPUT_DIR / "03_data_labels.svg")


GENERATORS = {
    "01_alignment": example_01_alignment,
    "02_font_families": example_02_font_families,
    "03_data_labels": example_03_data_labels,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for text examples...")

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
