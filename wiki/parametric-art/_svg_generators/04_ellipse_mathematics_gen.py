#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/04-ellipse-mathematics.md

Generates visual examples showing:
- Parametric ellipse equations
- Rotation matrix and rotated ellipses
- Circle as special case
- Eccentricity
- Angle vs parameter difference
- Focal points

Corresponds to sections:
- Parametric Ellipse Equations
- With Rotation
- Circle as Special Case
- Eccentricity
- Angle vs Parameter
- Focal Points
"""

from pyfreeform import Scene, Dot, Line, Text, Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-ellipse-mathematics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: Parametric Ellipse Equations
# =============================================================================

def example_01_basic_ellipse():
    """
    Show basic unrotated ellipse with formula
    """
    scene = Scene(width=500, height=500, background="white")

    # Center and radii
    cx, cy = 250, 250
    rx, ry = 180, 120

    # Draw axes (light)
    scene.add(Line(50, cy, 450, cy, color="#e5e7eb", width=1))
    scene.add(Line(cx, 50, cx, 450, color="#e5e7eb", width=1))

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=3
        ))

    # Draw radii
    scene.add(Line(cx, cy, cx + rx, cy, color="#ec4899", width=2))
    scene.add(Text(cx + rx/2, cy - 15, "rx", font_size=14, color="#ec4899", text_anchor="middle"))

    scene.add(Line(cx, cy, cx, cy - ry, color="#10b981", width=2))
    scene.add(Text(cx + 15, cy - ry/2, "ry", font_size=14, color="#10b981"))

    # Center point
    scene.add(Dot(cx, cy, radius=5, color="#666"))
    scene.add(Text(cx - 15, cy + 20, "(cx, cy)", font_size=12, color="#666", text_anchor="end"))

    # Mark t=0 point
    scene.add(Dot(cx + rx, cy, radius=7, color="#ef4444"))
    scene.add(Text(cx + rx + 25, cy, "t=0", font_size=12, color="#ef4444"))

    # Formulas
    scene.add(Text(250, 30, "Parametric Ellipse", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "x(t) = rx × cos(2πt)", font_size=13, color="#3b82f6", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "y(t) = ry × sin(2πt)", font_size=13, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "01-basic-ellipse.svg")


def example_02_parameter_progression():
    """
    Show how t parameter progresses around ellipse
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    rx, ry = 180, 120

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#cbd5e1", width=2.5
        ))

    # Mark quarter points
    t_values = [0, 0.25, 0.5, 0.75]
    labels = ["t=0", "t=0.25", "t=0.5", "t=0.75"]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b"]

    for t, label, color in zip(t_values, labels, colors):
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)

        scene.add(Dot(x, y, radius=8, color=color))

        # Position label outside
        label_x = cx + (rx + 40) * math.cos(angle)
        label_y = cy + (ry + 40) * math.sin(angle)
        scene.add(Text(label_x, label_y, label, font_size=13, color=color, text_anchor="middle"))

        # Draw line from center to show angle
        scene.add(Line(cx, cy, x, y, color=color, width=1))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Title
    scene.add(Text(250, 25, "Parameter t Around Ellipse", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 480, "t goes from 0 to 1 (one complete revolution)", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "02-parameter-progression.svg")


# =============================================================================
# SECTION: With Rotation
# =============================================================================

def example_03_rotation_comparison():
    """
    Show unrotated vs rotated ellipse
    """
    scene = Scene(width=700, height=400, background="white")

    # Left: unrotated
    cx1, cy1 = 175, 200
    rx, ry = 120, 80

    # Draw unrotated ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx1 + rx * math.cos(angle)
        y = cy1 + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Draw axes
    scene.add(Line(cx1 - 150, cy1, cx1 + 150, cy1, color="#e5e7eb", width=1))
    scene.add(Line(cx1, cy1 - 120, cx1, cy1 + 120, color="#e5e7eb", width=1))

    # Label
    scene.add(Text(cx1, 370, "Unrotated (θ = 0°)", font_size=14, color="#666", text_anchor="middle"))

    # Right: rotated
    cx2, cy2 = 525, 200
    theta = math.pi / 4  # 45 degrees

    # Draw rotated ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        # Unrotated position
        x_unrot = rx * math.cos(angle)
        y_unrot = ry * math.sin(angle)
        # Apply rotation
        x = cx2 + x_unrot * math.cos(theta) - y_unrot * math.sin(theta)
        y = cy2 + x_unrot * math.sin(theta) + y_unrot * math.cos(theta)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#8b5cf6", width=2.5
        ))

    # Draw rotated axes
    axis_len = 150
    scene.add(Line(
        cx2 - axis_len * math.cos(theta), cy2 - axis_len * math.sin(theta),
        cx2 + axis_len * math.cos(theta), cy2 + axis_len * math.sin(theta),
        color="#e5e7eb", width=1
    ))
    scene.add(Line(
        cx2 + axis_len * math.sin(theta), cy2 - axis_len * math.cos(theta),
        cx2 - axis_len * math.sin(theta), cy2 + axis_len * math.cos(theta),
        color="#e5e7eb", width=1
    ))

    # Label
    scene.add(Text(cx2, 370, "Rotated (θ = 45°)", font_size=14, color="#666", text_anchor="middle"))

    # Title
    scene.add(Text(350, 25, "Rotation Transformation", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "03-rotation-comparison.svg")


def example_04_rotation_matrix():
    """
    Visualize rotation matrix application
    """
    scene = Scene(width=600, height=500, background="white")

    cx, cy = 300, 300
    rx, ry = 150, 100
    theta = math.pi / 6  # 30 degrees

    # Draw original ellipse (light)
    points_orig = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points_orig.append(Point(x, y))

    for i in range(len(points_orig) - 1):
        scene.add(Line(
            points_orig[i].x, points_orig[i].y,
            points_orig[i+1].x, points_orig[i+1].y,
            color="#cbd5e1", width=1.5
        ))

    # Draw rotated ellipse
    points_rot = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x_unrot = rx * math.cos(angle)
        y_unrot = ry * math.sin(angle)
        x = cx + x_unrot * math.cos(theta) - y_unrot * math.sin(theta)
        y = cy + x_unrot * math.sin(theta) + y_unrot * math.cos(theta)
        points_rot.append(Point(x, y))

    for i in range(len(points_rot) - 1):
        scene.add(Line(
            points_rot[i].x, points_rot[i].y,
            points_rot[i+1].x, points_rot[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Show one point transformation
    t = 0.2
    angle = 2 * math.pi * t
    x_orig = cx + rx * math.cos(angle)
    y_orig = cy + ry * math.sin(angle)

    x_unrot = rx * math.cos(angle)
    y_unrot = ry * math.sin(angle)
    x_rot = cx + x_unrot * math.cos(theta) - y_unrot * math.sin(theta)
    y_rot = cy + x_unrot * math.sin(theta) + y_unrot * math.cos(theta)

    scene.add(Dot(x_orig, y_orig, radius=6, color="#cbd5e1"))
    scene.add(Dot(x_rot, y_rot, radius=7, color="#ef4444"))
    scene.add(Line(x_orig, y_orig, x_rot, y_rot, color="#ef4444", width=1.5))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Formulas
    scene.add(Text(300, 30, "Rotation Matrix Application", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 55, f"θ = {math.degrees(theta):.0f}°", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(300, 450, "x' = x·cos(θ) - y·sin(θ)", font_size=12, color="#3b82f6", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 470, "y' = x·sin(θ) + y·cos(θ)", font_size=12, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-rotation-matrix.svg")


# =============================================================================
# SECTION: Circle as Special Case
# =============================================================================

def example_05_circle_special_case():
    """
    Show that when rx = ry, we get a circle
    """
    scene = Scene(width=600, height=400, background="white")

    # Left: ellipse
    cx1, cy1 = 175, 200
    rx1, ry1 = 120, 80

    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx1 + rx1 * math.cos(angle)
        y = cy1 + ry1 * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    scene.add(Text(cx1, 330, f"rx = {rx1}, ry = {ry1}", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(cx1, 350, "Ellipse", font_size=14, color="#666", text_anchor="middle", font_weight="bold"))

    # Right: circle
    cx2, cy2 = 425, 200
    r = 100

    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx2 + r * math.cos(angle)
        y = cy2 + r * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#10b981", width=2.5
        ))

    scene.add(Text(cx2, 330, f"rx = ry = {r}", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(cx2, 350, "Circle", font_size=14, color="#666", text_anchor="middle", font_weight="bold"))

    # Title
    scene.add(Text(300, 25, "Circle as Special Case", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 380, "When rx = ry, ellipse becomes a circle", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "05-circle-special-case.svg")


# =============================================================================
# SECTION: Eccentricity
# =============================================================================

def example_06_eccentricity_comparison():
    """
    Show ellipses with different eccentricities
    """
    scene = Scene(width=700, height=600, background="white")

    # Different eccentricities
    configs = [
        (150, 150, 0.0, "e = 0 (circle)"),
        (150, 120, 0.46, "e ≈ 0.46"),
        (150, 90, 0.66, "e ≈ 0.66"),
        (150, 60, 0.8, "e ≈ 0.8"),
    ]

    for idx, (rx, ry, e, label) in enumerate(configs):
        y_offset = 120 + idx * 120
        cx = 350

        # Draw ellipse
        points = []
        for i in range(101):
            t = i / 100
            angle = 2 * math.pi * t
            x = cx + rx * math.cos(angle)
            y = y_offset + ry * math.sin(angle)
            points.append(Point(x, y))

        color = ["#10b981", "#3b82f6", "#8b5cf6", "#ec4899"][idx]

        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2
            ))

        # Label
        scene.add(Text(80, y_offset, label, font_size=13, color=color, font_weight="bold"))

    # Title and formula
    scene.add(Text(350, 25, "Eccentricity (Ovalness)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(350, 50, "e = √(1 - (b/a)²)", font_size=13, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 570, "Higher eccentricity = more elongated", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "06-eccentricity-comparison.svg")


# =============================================================================
# SECTION: Angle vs Parameter
# =============================================================================

def example_07_angle_vs_parameter():
    """
    Show difference between angle and parameter t
    """
    scene = Scene(width=600, height=500, background="white")

    cx, cy = 300, 250
    rx, ry = 200, 120

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#cbd5e1", width=2
        ))

    # Show t=0.25 (parameter)
    t = 0.25
    angle_t = 2 * math.pi * t
    x_t = cx + rx * math.cos(angle_t)
    y_t = cy + ry * math.sin(angle_t)

    scene.add(Dot(x_t, y_t, radius=8, color="#3b82f6"))
    scene.add(Line(cx, cy, x_t, y_t, color="#3b82f6", width=2))
    scene.add(Text(x_t + 25, y_t - 15, "t=0.25", font_size=13, color="#3b82f6", font_weight="bold"))

    # Show angle=90° (geometric angle)
    angle_90 = math.pi / 2
    x_90 = cx + rx * math.cos(angle_90)
    y_90 = cy + ry * math.sin(angle_90)

    scene.add(Dot(x_90, y_90, radius=8, color="#ec4899"))
    scene.add(Line(cx, cy, x_90, y_90, color="#ec4899", width=2))
    scene.add(Text(x_90 + 10, y_90 - 20, "90°", font_size=13, color="#ec4899", font_weight="bold"))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Draw reference angle arcs (small)
    # For t=0.25
    arc_r = 40
    for i in range(int(math.degrees(angle_t)) + 1):
        a = math.radians(i)
        x1 = cx + arc_r * math.cos(a)
        y1 = cy + arc_r * math.sin(a)
        if i > 0:
            scene.add(Line(x0, y0, x1, y1, color="#3b82f6", width=1))
        x0, y0 = x1, y1

    # Title
    scene.add(Text(300, 25, "Angle vs Parameter", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 460, "For ellipses, parameter t ≠ geometric angle", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(300, 480, "t gives uniform speed, angle gives non-uniform speed", font_size=11, color="#999", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "07-angle-vs-parameter.svg")


# =============================================================================
# SECTION: Focal Points
# =============================================================================

def example_08_focal_points():
    """
    Show focal points and distance sum property
    """
    scene = Scene(width=600, height=400, background="white")

    cx, cy = 300, 200
    rx, ry = 200, 120

    # Calculate focal distance
    c = math.sqrt(rx**2 - ry**2)

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Mark focal points
    f1_x, f1_y = cx - c, cy
    f2_x, f2_y = cx + c, cy

    scene.add(Dot(f1_x, f1_y, radius=8, color="#ec4899"))
    scene.add(Text(f1_x, f1_y + 25, "F₁", font_size=14, color="#ec4899", text_anchor="middle"))

    scene.add(Dot(f2_x, f2_y, radius=8, color="#ec4899"))
    scene.add(Text(f2_x, f2_y + 25, "F₂", font_size=14, color="#ec4899", text_anchor="middle"))

    # Pick a point on ellipse and show distance to both foci
    t = 0.15
    angle = 2 * math.pi * t
    p_x = cx + rx * math.cos(angle)
    p_y = cy + ry * math.sin(angle)

    scene.add(Dot(p_x, p_y, radius=7, color="#10b981"))
    scene.add(Text(p_x + 20, p_y - 15, "P", font_size=13, color="#10b981"))

    # Draw lines to foci
    scene.add(Line(f1_x, f1_y, p_x, p_y, color="#f59e0b", width=1.5))
    scene.add(Line(f2_x, f2_y, p_x, p_y, color="#f59e0b", width=1.5))

    # Calculate distances
    d1 = math.sqrt((p_x - f1_x)**2 + (p_y - f1_y)**2)
    d2 = math.sqrt((p_x - f2_x)**2 + (p_y - f2_y)**2)
    total = d1 + d2

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Title and properties
    scene.add(Text(300, 25, "Focal Points", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 350, f"c = √(a² - b²) = √({rx}² - {ry}²) ≈ {c:.1f}", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 370, f"d(P,F₁) + d(P,F₂) = {total:.1f} = 2a = {2*rx}", font_size=11, color="#f59e0b", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "08-focal-points.svg")


def example_09_area_formula():
    """
    Show area formula visualization
    """
    scene = Scene(width=500, height=400, background="white")

    cx, cy = 250, 200
    rx, ry = 150, 100

    # Draw ellipse
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=3
        ))

    # Draw radii
    scene.add(Line(cx, cy, cx + rx, cy, color="#ec4899", width=2.5))
    scene.add(Text(cx + rx/2, cy - 15, "rx", font_size=14, color="#ec4899", text_anchor="middle", font_weight="bold"))

    scene.add(Line(cx, cy, cx, cy - ry, color="#10b981", width=2.5))
    scene.add(Text(cx + 15, cy - ry/2, "ry", font_size=14, color="#10b981", font_weight="bold"))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Calculate area
    area = math.pi * rx * ry

    # Title and formula
    scene.add(Text(250, 25, "Ellipse Area", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 350, "A = π × rx × ry", font_size=16, color="#666", text_anchor="middle", font_family="monospace", font_weight="bold"))
    scene.add(Text(250, 375, f"A = π × {rx} × {ry} ≈ {area:.0f}", font_size=13, color="#999", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "09-area-formula.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Basic ellipse
    "01-basic-ellipse": example_01_basic_ellipse,
    "02-parameter-progression": example_02_parameter_progression,

    # Rotation
    "03-rotation-comparison": example_03_rotation_comparison,
    "04-rotation-matrix": example_04_rotation_matrix,

    # Circle
    "05-circle-special-case": example_05_circle_special_case,

    # Eccentricity
    "06-eccentricity-comparison": example_06_eccentricity_comparison,

    # Angle vs parameter
    "07-angle-vs-parameter": example_07_angle_vs_parameter,

    # Focal points and area
    "08-focal-points": example_08_focal_points,
    "09-area-formula": example_09_area_formula,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-ellipse-mathematics.md...")

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
