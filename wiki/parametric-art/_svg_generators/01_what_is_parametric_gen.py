#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/01-what-is-parametric.md

Generates visual examples showing:
- Parametric vs Cartesian comparison
- The t parameter visualization
- Examples of parametric paths (line, curve, ellipse)

Corresponds to sections:
- Parametric vs Cartesian
- The t Parameter
- Examples in PyFreeform
"""

from pyfreeform import Scene, Palette, Dot, Line, Curve, Ellipse, Text, Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-what-is-parametric"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: Parametric vs Cartesian
# =============================================================================

def example_01_cartesian_limitation():
    """
    Show limitation of Cartesian (y = f(x)) - can't draw a circle
    Draw a parabola and show it can only have one y for each x
    """
    scene = Scene(width=400, height=400, background="white")

    # Draw axes
    scene.add(Line(50, 350, 350, 350, color="#999", width=2))  # x-axis
    scene.add(Line(50, 350, 50, 50, color="#999", width=2))    # y-axis

    # Labels
    scene.add(Text(360, 360, "x", font_size=20, color="#666"))
    scene.add(Text(30, 40, "y", font_size=20, color="#666"))

    # Draw parabola y = x²
    points = []
    for i in range(61):
        t = i / 60
        x = 50 + t * 300
        # Scale parabola to fit
        cart_x = (t - 0.5) * 2  # -1 to 1
        y = 350 - (cart_x ** 2) * 250
        points.append(Point(x, y))

    # Draw the curve
    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Show one x maps to one y
    x_test = 200
    scene.add(Line(x_test, 350, x_test, 50, color="#fca5a5", width=1))
    scene.add(Dot(x_test, 225, radius=5, color="#dc2626"))
    scene.add(Text(x_test + 15, 225, "one y", font_size=14, color="#dc2626"))

    # Title
    scene.add(Text(200, 25, "Cartesian: y = x²", font_size=18, color="#333", text_anchor="middle"))
    scene.add(Text(200, 385, "Limited: one y per x", font_size=14, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01-cartesian-limitation.svg")


def example_02_parametric_circle():
    """
    Show how parametric can draw a circle (impossible in Cartesian)
    x(t) = r × cos(2πt), y(t) = r × sin(2πt)
    """
    scene = Scene(width=400, height=400, background="white")

    # Draw axes
    scene.add(Line(50, 200, 350, 200, color="#999", width=2))  # x-axis
    scene.add(Line(200, 50, 200, 350, color="#999", width=2))  # y-axis

    # Draw circle parametrically
    radius = 120
    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = 200 + radius * math.cos(angle)
        y = 200 + radius * math.sin(angle)
        points.append(Point(x, y))

    # Draw the circle
    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#10b981", width=2.5
        ))

    # Show multiple y values for same x
    x_test = 200
    scene.add(Line(x_test, 50, x_test, 350, color="#fca5a5", width=1))
    scene.add(Dot(x_test, 200 - radius, radius=5, color="#dc2626"))
    scene.add(Dot(x_test, 200 + radius, radius=5, color="#dc2626"))
    scene.add(Text(x_test + 15, 200, "two y!", font_size=14, color="#dc2626"))

    # Title
    scene.add(Text(200, 25, "Parametric: Circle", font_size=18, color="#333", text_anchor="middle"))
    scene.add(Text(200, 385, "Powerful: any curve!", font_size=14, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "02-parametric-circle.svg")


# =============================================================================
# SECTION: The t Parameter
# =============================================================================

def example_03_t_parameter_line():
    """
    Show how t parameter works on a line (0 to 1)
    Mark specific t values along the line
    """
    scene = Scene(width=600, height=200, background="white")

    # Draw line
    start_x, start_y = 50, 100
    end_x, end_y = 550, 100

    scene.add(Line(start_x, start_y, end_x, end_y, color="#94a3b8", width=3))

    # Mark t values
    t_values = [0, 0.25, 0.5, 0.75, 1.0]
    labels = ["t=0\nStart", "t=0.25", "t=0.5\nMidpoint", "t=0.75", "t=1\nEnd"]

    for t, label in zip(t_values, labels):
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t

        # Dot
        scene.add(Dot(x, y, radius=6, color="#3b82f6"))

        # Label
        lines = label.split('\n')
        for i, line in enumerate(lines):
            scene.add(Text(
                x, y + 25 + i * 16,
                line,
                font_size=13,
                color="#333",
                text_anchor="middle"
            ))

    # Title
    scene.add(Text(300, 20, "The t Parameter (0 to 1)", font_size=16, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "03-t-parameter-line.svg")


def example_04_t_parameter_curve():
    """
    Show t parameter on a curved path
    """
    scene = Scene(width=600, height=300, background="white")

    # Create a curve
    start = Point(50, 250)
    end = Point(550, 250)
    control = Point(300, 50)

    # Draw the curve
    points = []
    for i in range(101):
        t = i / 100
        # Quadratic Bézier formula
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#94a3b8", width=3
        ))

    # Mark t values
    t_values = [0, 0.25, 0.5, 0.75, 1.0]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]

    for t, color in zip(t_values, colors):
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

        scene.add(Dot(x, y, radius=7, color=color))
        scene.add(Text(x, y - 20, f"t={t}", font_size=12, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(300, 20, "t Parameter on Curve", font_size=16, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "04-t-parameter-curve.svg")


def example_05_t_parameter_ellipse():
    """
    Show t parameter on ellipse (goes around the perimeter)
    """
    scene = Scene(width=400, height=400, background="white")

    # Draw ellipse
    cx, cy = 200, 200
    rx, ry = 150, 100

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
            color="#94a3b8", width=3
        ))

    # Mark t values (quarters)
    t_values = [0, 0.25, 0.5, 0.75]
    labels = ["t=0", "t=0.25", "t=0.5", "t=0.75"]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b"]

    for t, label, color in zip(t_values, labels, colors):
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)

        scene.add(Dot(x, y, radius=8, color=color))

        # Position label outside
        label_x = cx + (rx + 30) * math.cos(angle)
        label_y = cy + (ry + 30) * math.sin(angle)
        scene.add(Text(label_x, label_y, label, font_size=13, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 25, "t Parameter on Ellipse", font_size=16, color="#333", text_anchor="middle"))
    scene.add(Text(200, 385, "t goes around perimeter", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "05-t-parameter-ellipse.svg")


# =============================================================================
# SECTION: Code Example Visualization
# =============================================================================

def example_06_code_visualization():
    """
    Visualize the code example: cell.add_dot(along=curve, t=0.75)
    Show a curve with a dot positioned at t=0.75
    """
    scene = Scene(width=500, height=300, background="#f8f9fa")

    # Create curve (similar to cell curve)
    start = Point(50, 250)
    end = Point(450, 250)
    control = Point(250, 100)

    # Draw the curve
    points = []
    for i in range(101):
        t = i / 100
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#64748b", width=2.5
        ))

    # Calculate position at t=0.75
    t = 0.75
    dot_x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
    dot_y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

    # Add the dot
    scene.add(Dot(dot_x, dot_y, radius=10, color="#ef4444"))

    # Add annotation
    scene.add(Text(dot_x, dot_y - 30, "t=0.75", font_size=15, color="#ef4444", text_anchor="middle"))
    scene.add(Text(dot_x, dot_y - 50, "75% along curve", font_size=12, color="#666", text_anchor="middle"))

    # Code snippet
    scene.add(Text(250, 20, "curve = cell.add_curve(curvature=0.5)", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 40, "cell.add_dot(along=curve, t=0.75)", font_size=11, color="#ef4444", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "06-code-visualization.svg")


# =============================================================================
# SECTION: Examples - Line, Curve, Ellipse formulas
# =============================================================================

def example_07_line_formula():
    """
    Show line formula: P(t) = start + (end - start) × t
    """
    scene = Scene(width=500, height=350, background="white")

    # Draw line
    start_x, start_y = 100, 250
    end_x, end_y = 400, 150

    scene.add(Line(start_x, start_y, end_x, end_y, color="#3b82f6", width=3))

    # Mark start and end
    scene.add(Dot(start_x, start_y, radius=8, color="#3b82f6"))
    scene.add(Text(start_x - 40, start_y, "start", font_size=13, color="#333"))

    scene.add(Dot(end_x, end_y, radius=8, color="#3b82f6"))
    scene.add(Text(end_x + 30, end_y, "end", font_size=13, color="#333"))

    # Show formula
    scene.add(Text(250, 30, "Line Formula", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 55, "P(t) = start + (end - start) × t", font_size=14, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    # Show example point at t=0.6
    t = 0.6
    x = start_x + (end_x - start_x) * t
    y = start_y + (end_y - start_y) * t
    scene.add(Dot(x, y, radius=6, color="#f59e0b"))
    scene.add(Text(x + 30, y, "t=0.6", font_size=12, color="#f59e0b"))

    scene.save(OUTPUT_DIR / "07-line-formula.svg")


def example_08_curve_formula():
    """
    Show Bézier curve formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
    """
    scene = Scene(width=500, height=400, background="white")

    # Control points
    p0 = Point(50, 300)   # start
    p1 = Point(250, 50)   # control
    p2 = Point(450, 300)  # end

    # Draw construction lines (light)
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#cbd5e1", width=1.5))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#cbd5e1", width=1.5))

    # Draw the curve
    points = []
    for i in range(101):
        t = i / 100
        x = (1-t)**2 * p0.x + 2*(1-t)*t * p1.x + t**2 * p2.x
        y = (1-t)**2 * p0.y + 2*(1-t)*t * p1.y + t**2 * p2.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#8b5cf6", width=3
        ))

    # Mark control points
    scene.add(Dot(p0.x, p0.y, radius=7, color="#8b5cf6"))
    scene.add(Text(p0.x - 25, p0.y + 20, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=7, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 20, "P₁ (control)", font_size=13, color="#ec4899"))

    scene.add(Dot(p2.x, p2.y, radius=7, color="#8b5cf6"))
    scene.add(Text(p2.x + 25, p2.y + 20, "P₂", font_size=13, color="#333"))

    # Formula
    scene.add(Text(250, 360, "Quadratic Bézier", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 385, "B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂", font_size=13, color="#8b5cf6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "08-curve-formula.svg")


def example_09_ellipse_formula():
    """
    Show ellipse formula: x(t) = rx×cos(2πt), y(t) = ry×sin(2πt)
    """
    scene = Scene(width=500, height=400, background="white")

    # Draw ellipse
    cx, cy = 250, 200
    rx, ry = 180, 120

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
            color="#10b981", width=3
        ))

    # Draw radii
    scene.add(Line(cx, cy, cx + rx, cy, color="#cbd5e1", width=1.5))
    scene.add(Text(cx + rx/2, cy - 15, "rx", font_size=13, color="#666"))

    scene.add(Line(cx, cy, cx, cy - ry, color="#cbd5e1", width=1.5))
    scene.add(Text(cx + 15, cy - ry/2, "ry", font_size=13, color="#666"))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Formula
    scene.add(Text(250, 30, "Ellipse Formula", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 55, "x(t) = rx × cos(2πt)", font_size=13, color="#10b981", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 75, "y(t) = ry × sin(2πt)", font_size=13, color="#10b981", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "09-ellipse-formula.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Parametric vs Cartesian
    "01-cartesian-limitation": example_01_cartesian_limitation,
    "02-parametric-circle": example_02_parametric_circle,

    # The t Parameter
    "03-t-parameter-line": example_03_t_parameter_line,
    "04-t-parameter-curve": example_04_t_parameter_curve,
    "05-t-parameter-ellipse": example_05_t_parameter_ellipse,
    "06-code-visualization": example_06_code_visualization,

    # Formulas
    "07-line-formula": example_07_line_formula,
    "08-curve-formula": example_08_curve_formula,
    "09-ellipse-formula": example_09_ellipse_formula,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-what-is-parametric.md...")

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
