#!/usr/bin/env python3
"""
SVG Generator for: api-reference/entities.md

Generates visual examples demonstrating all Entity types and their properties.
"""

from pyfreeform import Scene, Palette, Dot, Line, Curve, Ellipse, Polygon, Text, Rect
from pyfreeform.core.point import Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "entities"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Dot Entity
# =============================================================================

def example1_dot():
    """Dot - Simple circle entity"""
    scene = Scene(width=400, height=200, background="#1a1a2e")

    # Different sized dots
    scene.add(Dot(50, 100, radius=5, color="#ee4266"))
    scene.add(Dot(150, 100, radius=10, color="#4ecca3"))
    scene.add(Dot(250, 100, radius=15, color="#ffd23f"))
    scene.add(Dot(350, 100, radius=20, color="#64ffda"))

    scene.save(OUTPUT_DIR / "example1-dot.svg")


# =============================================================================
# Line Entity
# =============================================================================

def example2_line():
    """Line - Straight line entity"""
    scene = Scene(width=400, height=300, background="#1a1a2e")
    colors = Palette.ocean()

    # Different line styles
    scene.add(Line(50, 50, 350, 50, color=colors.primary, width=1))
    scene.add(Line(50, 100, 350, 100, color=colors.secondary, width=2))
    scene.add(Line(50, 150, 350, 150, color=colors.accent, width=3))
    scene.add(Line(50, 200, 350, 250, color="#ffd23f", width=4))

    scene.save(OUTPUT_DIR / "example2-line.svg")


# =============================================================================
# Curve Entity
# =============================================================================

def example3_curve():
    """Curve - Quadratic Bezier curve"""
    scene = Scene(width=400, height=300, background="#1a1a2e")
    colors = Palette.midnight()

    # Different curvature values
    scene.add(Curve(50, 250, 350, 250, curvature=0.3, color=colors.primary, width=2))
    scene.add(Curve(50, 200, 350, 200, curvature=0.5, color=colors.secondary, width=2))
    scene.add(Curve(50, 150, 350, 150, curvature=-0.5, color=colors.accent, width=2))
    scene.add(Curve(50, 100, 350, 100, curvature=0.8, color="#ffd23f", width=2))

    scene.save(OUTPUT_DIR / "example3-curve.svg")


# =============================================================================
# Ellipse Entity
# =============================================================================

def example4_ellipse():
    """Ellipse - Circle and oval shapes"""
    scene = Scene(width=500, height=200, background="#1a1a2e")
    colors = Palette.ocean()

    # Different ellipse styles
    scene.add(Ellipse(75, 100, rx=30, ry=30, fill=colors.primary))  # Circle
    scene.add(Ellipse(200, 100, rx=50, ry=30, fill=colors.secondary))  # Horizontal
    scene.add(Ellipse(325, 100, rx=30, ry=50, fill=colors.accent))  # Vertical
    scene.add(Ellipse(450, 100, rx=40, ry=25, rotation=45, fill="#64ffda"))  # Rotated

    scene.save(OUTPUT_DIR / "example4-ellipse.svg")


# =============================================================================
# Polygon Entity
# =============================================================================

def example5_polygon():
    """Polygon - Custom polygon shapes"""
    scene = Scene(width=500, height=200, background="#1a1a2e")
    colors = Palette.midnight()

    # Different polygon shapes
    triangle = [Point(50, 150), Point(100, 50), Point(150, 150)]
    scene.add(Polygon(triangle, fill=colors.primary))

    square = [Point(200, 50), Point(300, 50), Point(300, 150), Point(200, 150)]
    scene.add(Polygon(square, fill=colors.secondary))

    hexagon_verts = [Point(350 + 40 * math.cos(i * math.pi / 3), 100 + 40 * math.sin(i * math.pi / 3)) for i in range(6)]
    scene.add(Polygon(hexagon_verts, fill=colors.accent))

    scene.save(OUTPUT_DIR / "example5-polygon.svg")


# =============================================================================
# Polygon with Shape Helpers
# =============================================================================

def example6_polygon_shapes():
    """Polygon - Using shape helpers"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Built-in shapes
    cells[0].add_polygon(Polygon.triangle(size=0.8), fill=colors.primary)
    cells[1].add_polygon(Polygon.hexagon(size=0.8), fill=colors.secondary)
    cells[2].add_polygon(Polygon.star(5), fill=colors.accent)
    cells[3].add_polygon(Polygon.squircle(n=4), fill="#64ffda")
    cells[4].add_polygon(Polygon.diamond(size=0.8), fill="#ffd23f")

    scene.save(OUTPUT_DIR / "example6-polygon-Polygon.svg")


# =============================================================================
# Text Entity
# =============================================================================

def example7_text():
    """Text - Typography and labels"""
    scene = Scene(width=400, height=300, background="#1a1a2e")
    colors = Palette.midnight()

    # Different text styles
    scene.add(Text(200, 50, "Large Text", font_size=32, color=colors.primary, text_anchor="middle"))
    scene.add(Text(200, 100, "Medium Text", font_size=24, color=colors.secondary, text_anchor="middle"))
    scene.add(Text(200, 150, "Small Text", font_size=16, color=colors.accent, text_anchor="middle"))
    scene.add(Text(200, 200, "Monospace", font_size=20, color="#64ffda", font_family="monospace", text_anchor="middle"))
    scene.add(Text(200, 250, "Rotated", font_size=20, color="#ffd23f", rotation=45, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "example7-text.svg")


# =============================================================================
# Rect Entity
# =============================================================================

def example8_rect():
    """Rect - Rectangle shapes"""
    scene = Scene(width=500, height=200, background="#1a1a2e")
    colors = Palette.ocean()

    # Different rectangle styles
    scene.add(Rect(25, 50, 80, 60, fill=colors.primary))
    scene.add(Rect(135, 50, 80, 60, fill=None, stroke=colors.secondary, stroke_width=3))
    scene.add(Rect(245, 50, 80, 60, fill=colors.accent, stroke=colors.line, stroke_width=2))
    scene.add(Rect(355, 50, 80, 100, fill="#64ffda", stroke="#ffd23f", stroke_width=3))

    scene.save(OUTPUT_DIR / "example8-rect.svg")


# =============================================================================
# Anchor Points - Dot
# =============================================================================

def example9_dot_anchors():
    """Dot anchors - center only"""
    scene = Scene(width=200, height=200, background="#1a1a2e")
    colors = Palette.midnight()

    # Main dot
    dot = Dot(100, 100, radius=30, color=colors.primary)
    scene.add(dot)

    # Show anchor point
    anchor_pos = dot.anchor("center")
    scene.add(Dot(anchor_pos.x, anchor_pos.y, radius=5, color="#ee4266"))

    # Label
    scene.add(Text(100, 150, "center", font_size=12, color="#ee4266", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "example9-dot-anchors.svg")


# =============================================================================
# Anchor Points - Line
# =============================================================================

def example10_line_anchors():
    """Line anchors - start, center, end"""
    scene = Scene(width=400, height=200, background="#1a1a2e")
    colors = Palette.ocean()

    # Line
    line = Line(50, 100, 350, 100, color=colors.primary, width=3)
    scene.add(line)

    # Show anchors
    start = line.anchor("start")
    center = line.anchor("center")
    end = line.anchor("end")

    scene.add(Dot(start.x, start.y, radius=6, color="#ee4266"))
    scene.add(Dot(center.x, center.y, radius=6, color="#ffd23f"))
    scene.add(Dot(end.x, end.y, radius=6, color="#64ffda"))

    # Labels
    scene.add(Text(start.x, 130, "start", font_size=11, color="#ee4266", text_anchor="middle"))
    scene.add(Text(center.x, 130, "center", font_size=11, color="#ffd23f", text_anchor="middle"))
    scene.add(Text(end.x, 130, "end", font_size=11, color="#64ffda", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "example10-line-anchors.svg")


# =============================================================================
# Anchor Points - Rect
# =============================================================================

def example11_rect_anchors():
    """Rect anchors - all 9 positions"""
    scene = Scene(width=300, height=300, background="#1a1a2e")
    colors = Palette.midnight()

    # Rectangle
    rect = Rect(75, 75, 150, 150, fill=None, stroke=colors.primary, stroke_width=2)
    scene.add(rect)

    # Show all anchors
    anchors = ["top_left", "top", "top_right", "left", "center", "right", "bottom_left", "bottom", "bottom_right"]
    colors_list = ["#ee4266", "#ffd23f", "#ee4266", "#ffd23f", "#64ffda", "#ffd23f", "#ee4266", "#ffd23f", "#ee4266"]

    for anchor_name, color in zip(anchors, colors_list):
        pos = rect.anchor(anchor_name)
        scene.add(Dot(pos.x, pos.y, radius=5, color=color))

    scene.save(OUTPUT_DIR / "example11-rect-anchors.svg")


# =============================================================================
# Complete Example: All Entities
# =============================================================================

def example12_all_entities():
    """All entity types in one scene"""
    scene = Scene(width=600, height=400, background="#1a1a2e")
    colors = Palette.ocean()

    # Dots
    scene.add(Dot(50, 50, radius=15, color=colors.primary))
    scene.add(Dot(550, 50, radius=15, color=colors.primary))

    # Lines
    scene.add(Line(50, 50, 550, 50, color=colors.line, width=1))
    scene.add(Line(50, 50, 50, 350, color=colors.line, width=1))

    # Curve
    scene.add(Curve(100, 150, 500, 150, curvature=0.5, color=colors.secondary, width=2))

    # Ellipse
    scene.add(Ellipse(300, 250, rx=80, ry=50, fill=colors.primary, stroke=colors.accent, stroke_width=2))

    # Polygon
    scene.add(Polygon([Point(450, 200), Point(550, 200), Point(500, 300)], fill=colors.accent))

    # Rect
    scene.add(Rect(80, 250, 100, 80, fill=None, stroke=colors.secondary, stroke_width=2))

    # Text
    scene.add(Text(300, 50, "All Entity Types", font_size=20, color=colors.accent, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "example12-all-entities.svg")


# =============================================================================
# Generator Registry
# =============================================================================


GENERATORS = {
    "example1-dot": example1_dot,
    "example2-line": example2_line,
    "example3-curve": example3_curve,
    "example4-ellipse": example4_ellipse,
    "example5-polygon": example5_polygon,
    "example6-polygon-shapes": example6_polygon_shapes,
    "example7-text": example7_text,
    "example8-rect": example8_rect,
    "example9-dot-anchors": example9_dot_anchors,
    "example10-line-anchors": example10_line_anchors,
    "example11-rect-anchors": example11_rect_anchors,
    "example12-all-entities": example12_all_entities,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for entities.md...")

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
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
