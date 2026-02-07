#!/usr/bin/env python3
"""
SVG Generator for: examples/advanced/parametric-paths

Demonstrates the unified parametric interface across lines, curves, and ellipses.
"""

from pyfreeform import Scene, Palette, Text
from pyfreeform.core.point import Point
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "parametric-paths"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def example_01_unified_interface():
    """Line, curve, and ellipse with dots at the same t values."""
    colors = Palette.midnight()
    scene = Scene(width=500, height=350, background=colors.background)

    # Title
    scene.add(Text(
        250, 30, "Unified Parametric Interface",
        font_size=20, color="white", text_anchor="middle", bold=True,
    ))

    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]

    # Line (Linear)
    line = scene.add_line(
        start=Point(50, 100), end=Point(200, 100),
        color=colors.primary, width=2, opacity=0.3,
    )
    for t in t_values:
        scene.add_dot(along=line, t=t, radius=4, color=colors.secondary, z_index=1)
    scene.add(Text(125, 130, "Line (Linear)", font_size=12, color=colors.primary, text_anchor="middle"))

    # Curve (Bezier)
    curve = scene.add_curve(
        start=Point(50, 200), end=Point(200, 200),
        curvature=-0.6, color=colors.primary, width=2, opacity=0.3,
    )
    for t in t_values:
        scene.add_dot(along=curve, t=t, radius=4, color=colors.accent, z_index=1)
    scene.add(Text(125, 240, "Curve (Bezier)", font_size=12, color=colors.primary, text_anchor="middle"))

    # Ellipse (Parametric)
    ellipse = scene.add_ellipse(
        at=Point(375, 150), rx=75, ry=50,
        fill="none", stroke=colors.primary, stroke_width=2, opacity=0.3,
    )
    for t in [0.0, 0.25, 0.5, 0.75]:
        scene.add_dot(along=ellipse, t=t, radius=4, color="#64ffda", z_index=1)
    scene.add(Text(375, 230, "Ellipse (Parametric)", font_size=12, color=colors.primary, text_anchor="middle"))

    # Formula
    scene.add(Text(
        250, 330, "point = path.point_at(t)  where t \u2208 [0, 1]",
        font_size=11, color="#6b7280", font_family="monospace", text_anchor="middle",
    ))

    scene.save(OUTPUT_DIR / "01_unified_interface.svg")


def example_02_path_comparison():
    """Dense sampling shows path shape differences clearly."""
    colors = Palette.midnight()
    scene = Scene(width=500, height=250, background=colors.background)

    scene.add(Text(
        250, 25, "Path Shape Comparison (20 dots each)",
        font_size=16, color="white", text_anchor="middle", bold=True,
    ))

    n_dots = 20

    # Line
    line = scene.add_line(
        start=Point(50, 80), end=Point(200, 80),
        color=colors.primary, width=1, opacity=0.2,
    )
    for i in range(n_dots):
        t = i / (n_dots - 1)
        scene.add_dot(along=line, t=t, radius=3, color=colors.secondary)
    scene.add(Text(125, 110, "Line", font_size=11, color=colors.primary, text_anchor="middle"))

    # Curve
    curve = scene.add_curve(
        start=Point(50, 160), end=Point(200, 160),
        curvature=-0.7, color=colors.primary, width=1, opacity=0.2,
    )
    for i in range(n_dots):
        t = i / (n_dots - 1)
        scene.add_dot(along=curve, t=t, radius=3, color=colors.accent)
    scene.add(Text(125, 200, "Curve", font_size=11, color=colors.primary, text_anchor="middle"))

    # Ellipse
    ellipse = scene.add_ellipse(
        at=Point(375, 120), rx=75, ry=50,
        fill="none", stroke=colors.primary, stroke_width=1, opacity=0.2,
    )
    for i in range(n_dots):
        t = i / n_dots
        scene.add_dot(along=ellipse, t=t, radius=3, color="#64ffda")
    scene.add(Text(375, 200, "Ellipse", font_size=11, color=colors.primary, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "02_path_comparison.svg")


GENERATORS = {
    "01_unified_interface": example_01_unified_interface,
    "02_path_comparison": example_02_path_comparison,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for parametric-paths examples...")

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
