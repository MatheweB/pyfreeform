#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/06-mathematical-reference.md

Generates visual reference diagrams for all parametric formulas:
- Lines
- Quadratic Bézier curves
- Ellipses
- Rotation matrix
- Custom paths (spiral, wave, Lissajous, superellipse)

This is a quick visual reference sheet showing all formulas at a glance.
"""

from pyfreeform import Scene, Dot, Line, Text, Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "06-mathematical-reference"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: Quick Reference - All Formulas
# =============================================================================

def example_01_line_reference():
    """
    Quick visual reference for line formula
    """
    scene = Scene(width=500, height=250, background="white")

    # Draw line
    start_x, start_y = 100, 180
    end_x, end_y = 400, 120

    scene.add(Line(start_x, start_y, end_x, end_y, color="#3b82f6", width=3))

    # Mark points
    scene.add(Dot(start_x, start_y, radius=7, color="#3b82f6"))
    scene.add(Text(start_x - 35, start_y, "P₀", font_size=13, color="#333"))

    scene.add(Dot(end_x, end_y, radius=7, color="#3b82f6"))
    scene.add(Text(end_x + 30, end_y, "P₁", font_size=13, color="#333"))

    # Mark midpoint (t=0.5)
    mid_x = start_x + (end_x - start_x) * 0.5
    mid_y = start_y + (end_y - start_y) * 0.5
    scene.add(Dot(mid_x, mid_y, radius=5, color="#ef4444"))
    scene.add(Text(mid_x, mid_y - 20, "t=0.5", font_size=11, color="#ef4444", text_anchor="middle"))

    # Formulas
    scene.add(Text(250, 25, "Line", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 210, "P(t) = P₀ + (P₁ - P₀) × t", font_size=13, color="#3b82f6", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 230, "P(t) = (1-t)P₀ + tP₁", font_size=13, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "01-line-reference.svg")


def example_02_bezier_reference():
    """
    Quick visual reference for Bézier curve formula
    """
    scene = Scene(width=500, height=300, background="white")

    # Control points
    p0 = Point(80, 240)
    p1 = Point(250, 60)
    p2 = Point(420, 240)

    # Draw construction
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#e5e7eb", width=1))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#e5e7eb", width=1))

    # Draw curve
    points = []
    for i in range(101):
        t = i / 100
        x = (1-t)**2 * p0.x + 2*(1-t)*t * p1.x + t**2 * p2.x
        y = (1-t)**2 * p0.y + 2*(1-t)*t * p1.y + t**2 * p2.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#8b5cf6", width=3))

    # Mark points
    scene.add(Dot(p0.x, p0.y, radius=7, color="#8b5cf6"))
    scene.add(Text(p0.x - 20, p0.y + 20, "P₀", font_size=12, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=7, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 20, "P₁", font_size=12, color="#ec4899"))

    scene.add(Dot(p2.x, p2.y, radius=7, color="#8b5cf6"))
    scene.add(Text(p2.x + 20, p2.y + 20, "P₂", font_size=12, color="#333"))

    # Formula
    scene.add(Text(250, 20, "Quadratic Bézier", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 280, "B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂", font_size=12, color="#8b5cf6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "02-bezier-reference.svg")


def example_03_ellipse_reference():
    """
    Quick visual reference for ellipse formula
    """
    scene = Scene(width=500, height=350, background="white")

    cx, cy = 250, 180
    rx, ry = 180, 110

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#10b981", width=3))

    # Draw radii
    scene.add(Line(cx, cy, cx + rx, cy, color="#cbd5e1", width=1.5))
    scene.add(Text(cx + rx/2, cy - 12, "rx", font_size=12, color="#666", text_anchor="middle"))

    scene.add(Line(cx, cy, cx, cy - ry, color="#cbd5e1", width=1.5))
    scene.add(Text(cx + 12, cy - ry/2, "ry", font_size=12, color="#666"))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Formulas
    scene.add(Text(250, 25, "Ellipse", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 310, "x(t) = rx × cos(2πt)", font_size=12, color="#10b981", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 330, "y(t) = ry × sin(2πt)", font_size=12, color="#10b981", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "03-ellipse-reference.svg")


def example_04_rotation_reference():
    """
    Quick visual reference for rotation matrix
    """
    scene = Scene(width=500, height=400, background="white")

    cx, cy = 250, 200
    rx, ry = 140, 90
    theta = math.pi / 4

    # Draw unrotated (light)
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y,
                      color="#cbd5e1", width=1.5))

    # Draw rotated
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x_unrot = rx * math.cos(angle)
        y_unrot = ry * math.sin(angle)
        x = cx + x_unrot * math.cos(theta) - y_unrot * math.sin(theta)
        y = cy + x_unrot * math.sin(theta) + y_unrot * math.cos(theta)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#8b5cf6", width=3))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Formulas
    scene.add(Text(250, 25, "Rotation Matrix (2D)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 50, "θ = 45°", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(250, 350, "x' = x·cos(θ) - y·sin(θ)", font_size=12, color="#8b5cf6", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 370, "y' = x·sin(θ) + y·cos(θ)", font_size=12, color="#8b5cf6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-rotation-reference.svg")


def example_05_custom_paths_reference():
    """
    Quick visual reference showing multiple custom paths
    """
    scene = Scene(width=700, height=700, background="white")

    # Spiral
    cx1, cy1 = 175, 175
    start_r, end_r = 10, 120
    turns = 3

    points = []
    for i in range(201):
        t = i / 200
        angle = t * turns * 2 * math.pi
        radius = start_r + (end_r - start_r) * t
        x = cx1 + radius * math.cos(angle)
        y = cy1 + radius * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#3b82f6", width=2))

    scene.add(Text(cx1, 50, "Spiral", font_size=14, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(cx1, 310, "r(t) = r₀+(r₁-r₀)×t", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    # Wave
    cx2, cy2 = 525, 175
    points = []
    for i in range(201):
        t = i / 200
        x = cx2 - 120 + 240 * t
        y = cy2 + 60 * math.sin(t * 3 * 2 * math.pi)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#10b981", width=2))

    scene.add(Text(cx2, 50, "Wave", font_size=14, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(cx2, 310, "y = A·sin(ω·t)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    # Lissajous
    cx3, cy3 = 175, 525
    a, b = 3, 2
    delta = math.pi / 2
    size = 120

    points = []
    for i in range(401):
        t = i / 400
        angle = t * 2 * math.pi
        x = cx3 + size * math.sin(a * angle + delta)
        y = cy3 + size * math.sin(b * angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#ec4899", width=2))

    scene.add(Text(cx3, 380, "Lissajous", font_size=14, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(cx3, 660, "x=A·sin(at+δ)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    # Superellipse
    def sgn_pow(val, exp):
        return abs(val) ** exp if val >= 0 else -(abs(val) ** exp)

    cx4, cy4 = 525, 525
    n = 3
    size = 100

    points = []
    for i in range(201):
        t = i / 200
        angle = t * 2 * math.pi
        x = cx4 + size * sgn_pow(math.cos(angle), 2/n)
        y = cy4 + size * sgn_pow(math.sin(angle), 2/n)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#f59e0b", width=2))

    scene.add(Text(cx4, 380, "Superellipse", font_size=14, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(cx4, 660, "|x/a|ⁿ+|y/b|ⁿ=1", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    # Title
    scene.add(Text(350, 25, "Custom Paths", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "05-custom-paths-reference.svg")


def example_06_all_formulas_sheet():
    """
    Create a comprehensive formula reference sheet
    """
    scene = Scene(width=800, height=1000, background="white")

    # Title
    scene.add(Text(400, 30, "PyFreeform Parametric Reference", font_size=22, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(400, 55, "All parametric formulas (t ∈ [0,1])", font_size=14, color="#666", text_anchor="middle"))

    y_offset = 90

    # Section 1: Lines
    scene.add(Text(50, y_offset, "LINES", font_size=16, color="#3b82f6", font_weight="bold"))
    y_offset += 25
    scene.add(Text(50, y_offset, "P(t) = P₀ + (P₁ - P₀) × t", font_size=12, color="#333", font_family="monospace"))
    y_offset += 20
    scene.add(Text(50, y_offset, "P(t) = (1-t)P₀ + tP₁", font_size=12, color="#333", font_family="monospace"))
    y_offset += 20
    scene.add(Text(50, y_offset, "x(t) = (1-t)x₀ + tx₁", font_size=11, color="#666", font_family="monospace"))
    y_offset += 18
    scene.add(Text(50, y_offset, "y(t) = (1-t)y₀ + ty₁", font_size=11, color="#666", font_family="monospace"))
    y_offset += 40

    # Section 2: Bézier Curves
    scene.add(Text(50, y_offset, "QUADRATIC BÉZIER CURVES", font_size=16, color="#8b5cf6", font_weight="bold"))
    y_offset += 25
    scene.add(Text(50, y_offset, "B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂", font_size=12, color="#333", font_family="monospace"))
    y_offset += 25
    scene.add(Text(50, y_offset, "Components:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "(1-t)²     : Weight on start point", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "2(1-t)t    : Weight on control point", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "t²         : Weight on end point", font_size=10, color="#666", font_family="monospace"))
    y_offset += 25
    scene.add(Text(50, y_offset, "Control point from curvature:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "P₁ = midpoint + perpendicular × curvature × length/2", font_size=10, color="#666", font_family="monospace"))
    y_offset += 40

    # Section 3: Ellipses
    scene.add(Text(50, y_offset, "ELLIPSES", font_size=16, color="#10b981", font_weight="bold"))
    y_offset += 25
    scene.add(Text(50, y_offset, "Unrotated:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "x(t) = rx × cos(2πt)", font_size=11, color="#333", font_family="monospace"))
    y_offset += 18
    scene.add(Text(70, y_offset, "y(t) = ry × sin(2πt)", font_size=11, color="#333", font_family="monospace"))
    y_offset += 25
    scene.add(Text(50, y_offset, "With rotation θ:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "x'(t) = cx + rx·cos(2πt)·cos(θ) - ry·sin(2πt)·sin(θ)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "y'(t) = cy + rx·cos(2πt)·sin(θ) + ry·sin(2πt)·cos(θ)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 25
    scene.add(Text(50, y_offset, "Properties:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "Area = π × rx × ry", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "Eccentricity = √(1 - (min/max)²)", font_size=10, color="#666", font_family="monospace"))
    y_offset += 40

    # Section 4: Rotation
    scene.add(Text(50, y_offset, "ROTATION MATRIX (2D)", font_size=16, color="#ec4899", font_weight="bold"))
    y_offset += 25
    scene.add(Text(50, y_offset, "x' = x·cos(θ) - y·sin(θ)", font_size=11, color="#333", font_family="monospace"))
    y_offset += 18
    scene.add(Text(50, y_offset, "y' = x·sin(θ) + y·cos(θ)", font_size=11, color="#333", font_family="monospace"))
    y_offset += 40

    # Section 5: Custom Paths
    scene.add(Text(50, y_offset, "CUSTOM PATHS", font_size=16, color="#f59e0b", font_weight="bold"))
    y_offset += 25

    scene.add(Text(50, y_offset, "Archimedean Spiral:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "θ(t) = t × turns × 2π", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "r(t) = r₀ + (r₁ - r₀) × t", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "x(t) = cx + r(t)·cos(θ(t))", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "y(t) = cy + r(t)·sin(θ(t))", font_size=10, color="#333", font_family="monospace"))
    y_offset += 25

    scene.add(Text(50, y_offset, "Sinusoidal Wave:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "x(t) = x₀ + (x₁ - x₀) × t", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "y(t) = y₀ + (y₁ - y₀) × t + A·sin(ω·t)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 25

    scene.add(Text(50, y_offset, "Lissajous Curve:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "x(t) = A·sin(a·t + δ)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "y(t) = B·sin(b·t)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "Famous ratios: a:b = 1:1, 1:2, 3:2, 5:4", font_size=9, color="#999", font_family="monospace"))
    y_offset += 25

    scene.add(Text(50, y_offset, "Superellipse:", font_size=11, color="#666"))
    y_offset += 18
    scene.add(Text(70, y_offset, "|x/a|ⁿ + |y/b|ⁿ = 1", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "x(t) = a × sgn(cos θ) × |cos θ|^(2/n)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 16
    scene.add(Text(70, y_offset, "y(t) = b × sgn(sin θ) × |sin θ|^(2/n)", font_size=10, color="#333", font_family="monospace"))
    y_offset += 40

    # Section 6: Useful Conversions
    scene.add(Text(50, y_offset, "USEFUL CONVERSIONS", font_size=16, color="#6366f1", font_weight="bold"))
    y_offset += 25
    scene.add(Text(50, y_offset, "Degrees to Radians: rad = deg × π/180", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(50, y_offset, "Radians to Degrees: deg = rad × 180/π", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(50, y_offset, "Distance: d = √((x₂-x₁)² + (y₂-y₁)²)", font_size=10, color="#666", font_family="monospace"))
    y_offset += 16
    scene.add(Text(50, y_offset, "LERP: lerp(a,b,t) = a + (b-a)×t = (1-t)a + tb", font_size=10, color="#666", font_family="monospace"))

    scene.save(OUTPUT_DIR / "06-all-formulas-sheet.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Individual references
    "01-line-reference": example_01_line_reference,
    "02-bezier-reference": example_02_bezier_reference,
    "03-ellipse-reference": example_03_ellipse_reference,
    "04-rotation-reference": example_04_rotation_reference,
    "05-custom-paths-reference": example_05_custom_paths_reference,

    # Comprehensive sheet
    "06-all-formulas-sheet": example_06_all_formulas_sheet,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 06-mathematical-reference.md...")

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
        # Generate specific image
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
        # Generate all
        generate_all()
