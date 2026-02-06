#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/03-bezier-mathematics.md

Generates visual examples showing:
- The quadratic Bézier formula and its components
- Weight distribution at different t values
- Control point influence
- De Casteljau's algorithm
- Derivatives and properties

Corresponds to sections:
- The Quadratic Bézier Formula
- Weight Distribution
- Derivatives
- Control Point from Curvature
- De Casteljau's Algorithm
- Properties
"""

from pyfreeform import Scene, Dot, Line, Text, Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-bezier-mathematics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: The Quadratic Bézier Formula
# =============================================================================

def example_01_bezier_basic():
    """
    Show a basic Bézier curve with control points labeled
    """
    scene = Scene(width=600, height=400, background="white")

    # Control points
    p0 = Point(100, 300)  # start
    p1 = Point(300, 80)   # control
    p2 = Point(500, 300)  # end

    # Draw construction lines
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
            color="#3b82f6", width=3
        ))

    # Mark control points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#3b82f6"))
    scene.add(Text(p0.x - 40, p0.y, "P₀ (start)", font_size=14, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=8, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 25, "P₁ (control)", font_size=14, color="#ec4899", text_anchor="middle"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#3b82f6"))
    scene.add(Text(p2.x + 35, p2.y, "P₂ (end)", font_size=14, color="#333"))

    # Formula
    scene.add(Text(300, 30, "Quadratic Bézier Curve", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 365, "B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂", font_size=15, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "01-bezier-basic.svg")


def example_02_weight_components():
    """
    Show the three weight components separately
    """
    scene = Scene(width=700, height=500, background="white")

    # Plot weight functions
    x_start, y_base = 50, 450
    width = 600
    height = 300

    # Draw axes
    scene.add(Line(x_start, y_base, x_start + width, y_base, color="#333", width=2))  # t-axis
    scene.add(Line(x_start, y_base, x_start, y_base - height, color="#333", width=2))  # weight-axis

    # Labels
    scene.add(Text(x_start + width + 10, y_base, "t", font_size=14, color="#333"))
    scene.add(Text(x_start - 10, y_base - height, "weight", font_size=14, color="#333", text_anchor="end"))
    scene.add(Text(x_start - 5, y_base + 15, "0", font_size=12, color="#666"))
    scene.add(Text(x_start + width - 5, y_base + 15, "1", font_size=12, color="#666"))

    # Plot the three weight functions
    colors = ["#3b82f6", "#ec4899", "#10b981"]
    labels = ["(1-t)² (start)", "2(1-t)t (control)", "t² (end)"]

    for idx, (color, label) in enumerate(zip(colors, labels)):
        points = []
        for i in range(101):
            t = i / 100
            x = x_start + t * width

            # Calculate weight
            if idx == 0:
                weight = (1-t)**2
            elif idx == 1:
                weight = 2*(1-t)*t
            else:
                weight = t**2

            y = y_base - weight * height
            points.append(Point(x, y))

        # Draw curve
        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2.5
            ))

        # Label
        scene.add(Text(100 + idx * 200, 30 + idx * 20, label, font_size=13, color=color))

    # Title
    scene.add(Text(350, 30, "Weight Functions", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "02-weight-components.svg")


# =============================================================================
# SECTION: Weight Distribution Table Visualization
# =============================================================================

def example_03_weight_distribution():
    """
    Visualize the weight distribution table at different t values
    """
    scene = Scene(width=700, height=400, background="white")

    # Control points
    p0 = Point(100, 300)
    p1 = Point(350, 100)
    p2 = Point(600, 300)

    # Draw construction triangle
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#e5e7eb", width=1))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#e5e7eb", width=1))
    scene.add(Line(p0.x, p0.y, p2.x, p2.y, color="#e5e7eb", width=1))

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
            color="#94a3b8", width=2
        ))

    # Mark specific t values with weights
    t_values = [0, 0.25, 0.5, 0.75, 1.0]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#f59e0b", "#10b981"]

    for t, color in zip(t_values, colors):
        # Calculate position
        x = (1-t)**2 * p0.x + 2*(1-t)*t * p1.x + t**2 * p2.x
        y = (1-t)**2 * p0.y + 2*(1-t)*t * p1.y + t**2 * p2.y

        # Calculate weights
        w0 = (1-t)**2
        w1 = 2*(1-t)*t
        w2 = t**2

        # Draw point
        scene.add(Dot(x, y, radius=7, color=color))

        # Label with t value
        scene.add(Text(x, y - 20, f"t={t}", font_size=11, color=color, text_anchor="middle"))

    # Control points
    scene.add(Dot(p0.x, p0.y, radius=6, color="#666"))
    scene.add(Text(p0.x - 20, p0.y + 20, "P₀", font_size=12, color="#666"))

    scene.add(Dot(p1.x, p1.y, radius=6, color="#666"))
    scene.add(Text(p1.x, p1.y - 20, "P₁", font_size=12, color="#666"))

    scene.add(Dot(p2.x, p2.y, radius=6, color="#666"))
    scene.add(Text(p2.x + 20, p2.y + 20, "P₂", font_size=12, color="#666"))

    # Title
    scene.add(Text(350, 25, "Weight Distribution at Different t Values", font_size=16, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(350, 380, "Control point P₁ has maximum influence at t=0.5", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "03-weight-distribution.svg")


def example_04_control_point_influence():
    """
    Show how control point position affects the curve
    Three curves with different control point positions
    """
    scene = Scene(width=700, height=500, background="white")

    # Same start and end
    p0 = Point(100, 400)
    p2 = Point(600, 400)

    # Three different control points
    controls = [
        (Point(350, 150), "#3b82f6", "Low control point"),
        (Point(350, 250), "#8b5cf6", "Mid control point"),
        (Point(350, 350), "#ec4899", "High control point"),
    ]

    for p1, color, label in controls:
        # Draw curve
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
                color=color, width=2.5
            ))

        # Mark control point
        scene.add(Dot(p1.x, p1.y, radius=6, color=color))
        scene.add(Line(p0.x, p0.y, p1.x, p1.y, color=color, width=1))
        scene.add(Line(p1.x, p1.y, p2.x, p2.y, color=color, width=1))

    # Start and end points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#333"))
    scene.add(Text(p0.x - 20, p0.y + 20, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#333"))
    scene.add(Text(p2.x + 20, p2.y + 20, "P₂", font_size=13, color="#333"))

    # Legend
    y_offset = 50
    for p1, color, label in controls:
        scene.add(Dot(500, y_offset, radius=5, color=color))
        scene.add(Text(515, y_offset, label, font_size=12, color=color))
        y_offset += 25

    # Title
    scene.add(Text(350, 25, "Control Point Influence", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "04-control-point-influence.svg")


# =============================================================================
# SECTION: De Casteljau's Algorithm
# =============================================================================

def example_05_de_casteljau_step1():
    """
    Show first step of De Casteljau's algorithm
    """
    scene = Scene(width=600, height=400, background="white")

    # Control points
    p0 = Point(100, 300)
    p1 = Point(300, 80)
    p2 = Point(500, 300)

    # Choose t = 0.6 for visualization
    t = 0.6

    # Draw construction lines
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#cbd5e1", width=2))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#cbd5e1", width=2))

    # First level interpolations
    q0_x = (1-t) * p0.x + t * p1.x
    q0_y = (1-t) * p0.y + t * p1.y

    q1_x = (1-t) * p1.x + t * p2.x
    q1_y = (1-t) * p1.y + t * p2.y

    # Draw Q0 and Q1
    scene.add(Dot(q0_x, q0_y, radius=7, color="#8b5cf6"))
    scene.add(Text(q0_x - 25, q0_y, "Q₀", font_size=13, color="#8b5cf6"))

    scene.add(Dot(q1_x, q1_y, radius=7, color="#8b5cf6"))
    scene.add(Text(q1_x + 25, q1_y, "Q₁", font_size=13, color="#8b5cf6"))

    # Original control points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#3b82f6"))
    scene.add(Text(p0.x - 20, p0.y + 25, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=8, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 25, "P₁", font_size=13, color="#333"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#3b82f6"))
    scene.add(Text(p2.x + 20, p2.y + 25, "P₂", font_size=13, color="#333"))

    # Title
    scene.add(Text(300, 25, "De Casteljau - Step 1: Linear Interpolations", font_size=16, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 50, f"t = {t}", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(300, 365, "Q₀ = (1-t)P₀ + tP₁", font_size=12, color="#8b5cf6", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 385, "Q₁ = (1-t)P₁ + tP₂", font_size=12, color="#8b5cf6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "05-de-casteljau-step1.svg")


def example_06_de_casteljau_step2():
    """
    Show second step of De Casteljau's algorithm - final point
    """
    scene = Scene(width=600, height=400, background="white")

    # Control points
    p0 = Point(100, 300)
    p1 = Point(300, 80)
    p2 = Point(500, 300)

    t = 0.6

    # Draw the complete curve (light)
    points = []
    for i in range(101):
        t_val = i / 100
        x = (1-t_val)**2 * p0.x + 2*(1-t_val)*t_val * p1.x + t_val**2 * p2.x
        y = (1-t_val)**2 * p0.y + 2*(1-t_val)*t_val * p1.y + t_val**2 * p2.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#e5e7eb", width=2
        ))

    # Draw construction lines
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#cbd5e1", width=1.5))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#cbd5e1", width=1.5))

    # First level
    q0_x = (1-t) * p0.x + t * p1.x
    q0_y = (1-t) * p0.y + t * p1.y
    q1_x = (1-t) * p1.x + t * p2.x
    q1_y = (1-t) * p1.y + t * p2.y

    scene.add(Line(q0_x, q0_y, q1_x, q1_y, color="#8b5cf6", width=2))
    scene.add(Dot(q0_x, q0_y, radius=6, color="#8b5cf6"))
    scene.add(Dot(q1_x, q1_y, radius=6, color="#8b5cf6"))

    # Final point
    final_x = (1-t) * q0_x + t * q1_x
    final_y = (1-t) * q0_y + t * q1_y

    scene.add(Dot(final_x, final_y, radius=9, color="#ef4444"))
    scene.add(Text(final_x, final_y - 25, "B(t)", font_size=14, color="#ef4444", text_anchor="middle", font_weight="bold"))

    # Original control points
    scene.add(Dot(p0.x, p0.y, radius=7, color="#666"))
    scene.add(Dot(p1.x, p1.y, radius=7, color="#666"))
    scene.add(Dot(p2.x, p2.y, radius=7, color="#666"))

    # Title
    scene.add(Text(300, 25, "De Casteljau - Step 2: Final Point", font_size=16, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 365, "B(t) = (1-t)Q₀ + tQ₁", font_size=12, color="#ef4444", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "06-de-casteljau-step2.svg")


# =============================================================================
# SECTION: Properties - Convex Hull
# =============================================================================

def example_07_convex_hull():
    """
    Show that curve stays within convex hull (triangle P0P1P2)
    """
    scene = Scene(width=600, height=400, background="white")

    # Control points
    p0 = Point(100, 300)
    p1 = Point(300, 80)
    p2 = Point(500, 300)

    # Draw convex hull (triangle) - filled
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#fca5a5", width=2))
    scene.add(Line(p1.x, p1.y, p2.x, p2.y, color="#fca5a5", width=2))
    scene.add(Line(p0.x, p0.y, p2.x, p2.y, color="#fca5a5", width=2))

    # Shade the triangle (approximate with many lines)
    for i in range(100):
        t = i / 100
        # Top edge (p0 to p1)
        x1 = (1-t) * p0.x + t * p1.x
        y1 = (1-t) * p0.y + t * p1.y
        # From p1 to p2
        x2 = (1-t) * p1.x + t * p2.x
        y2 = (1-t) * p1.y + t * p2.y
        # Bottom edge (p0 to p2)
        x3 = (1-t) * p0.x + t * p2.x
        y3 = p0.y  # Constant because p0 and p2 have same y

        scene.add(Line(x1, y1, x3, y3, color="#fee2e2", width=1))

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
            color="#3b82f6", width=3
        ))

    # Control points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#3b82f6"))
    scene.add(Text(p0.x - 30, p0.y + 20, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=8, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 25, "P₁", font_size=13, color="#333"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#3b82f6"))
    scene.add(Text(p2.x + 30, p2.y + 20, "P₂", font_size=13, color="#333"))

    # Title
    scene.add(Text(300, 25, "Convex Hull Property", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 380, "Curve stays within triangle P₀P₁P₂", font_size=13, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "07-convex-hull.svg")


def example_08_tangent_property():
    """
    Show tangent property - tangent at start points toward control point
    """
    scene = Scene(width=600, height=400, background="white")

    # Control points
    p0 = Point(100, 300)
    p1 = Point(300, 80)
    p2 = Point(500, 300)

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
            color="#3b82f6", width=3
        ))

    # Draw tangent at start (direction from P0 to P1)
    tangent_length = 120
    dx = p1.x - p0.x
    dy = p1.y - p0.y
    length = math.sqrt(dx**2 + dy**2)
    dx /= length
    dy /= length

    scene.add(Line(
        p0.x, p0.y,
        p0.x + dx * tangent_length, p0.y + dy * tangent_length,
        color="#ef4444", width=2.5
    ))
    scene.add(Text(p0.x + dx * 60, p0.y + dy * 60 - 15, "Tangent", font_size=12, color="#ef4444"))

    # Draw line to control point
    scene.add(Line(p0.x, p0.y, p1.x, p1.y, color="#cbd5e1", width=1.5))

    # Control points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#3b82f6"))
    scene.add(Text(p0.x - 30, p0.y + 20, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p1.x, p1.y, radius=8, color="#ec4899"))
    scene.add(Text(p1.x, p1.y - 25, "P₁", font_size=13, color="#333"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#3b82f6"))
    scene.add(Text(p2.x + 30, p2.y + 20, "P₂", font_size=13, color="#333"))

    # Title
    scene.add(Text(300, 25, "Tangent Property", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 380, "Tangent at P₀ points toward P₁", font_size=13, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-tangent-property.svg")


# =============================================================================
# SECTION: Control Point from Curvature
# =============================================================================

def example_09_curvature_calculation():
    """
    Show how control point is calculated from curvature parameter
    """
    scene = Scene(width=600, height=450, background="white")

    # Start and end points
    p0 = Point(100, 350)
    p2 = Point(500, 350)

    # Curvature parameter
    curvature = 0.5

    # Calculate control point (following the algorithm)
    # 1. Midpoint
    mid_x = (p0.x + p2.x) / 2
    mid_y = (p0.y + p2.y) / 2

    # 2. Direction and length
    dx = p2.x - p0.x
    dy = p2.y - p0.y
    length = math.sqrt(dx**2 + dy**2)

    # 3. Perpendicular (rotate 90°)
    perp_x = -dy
    perp_y = dx
    perp_length = math.sqrt(perp_x**2 + perp_y**2)
    unit_perp_x = perp_x / perp_length
    unit_perp_y = perp_y / perp_length

    # 4. Offset
    offset = curvature * length / 2

    # 5. Control point
    p1_x = mid_x + unit_perp_x * offset
    p1_y = mid_y + unit_perp_y * offset

    # Draw base line
    scene.add(Line(p0.x, p0.y, p2.x, p2.y, color="#cbd5e1", width=2))

    # Draw midpoint
    scene.add(Dot(mid_x, mid_y, radius=6, color="#8b5cf6"))
    scene.add(Text(mid_x, mid_y + 20, "midpoint", font_size=11, color="#8b5cf6", text_anchor="middle"))

    # Draw perpendicular offset
    scene.add(Line(mid_x, mid_y, p1_x, p1_y, color="#ec4899", width=2))
    scene.add(Text((mid_x + p1_x)/2 + 15, (mid_y + p1_y)/2, "offset", font_size=11, color="#ec4899"))

    # Draw the curve
    points = []
    for i in range(101):
        t = i / 100
        x = (1-t)**2 * p0.x + 2*(1-t)*t * p1_x + t**2 * p2.x
        y = (1-t)**2 * p0.y + 2*(1-t)*t * p1_y + t**2 * p2.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=3
        ))

    # Control points
    scene.add(Dot(p0.x, p0.y, radius=8, color="#3b82f6"))
    scene.add(Text(p0.x - 30, p0.y, "P₀", font_size=13, color="#333"))

    scene.add(Dot(p1_x, p1_y, radius=8, color="#ec4899"))
    scene.add(Text(p1_x, p1_y - 25, "P₁", font_size=13, color="#ec4899", text_anchor="middle"))

    scene.add(Dot(p2.x, p2.y, radius=8, color="#3b82f6"))
    scene.add(Text(p2.x + 30, p2.y, "P₂", font_size=13, color="#333"))

    # Title and formula
    scene.add(Text(300, 25, "Control Point from Curvature", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 50, f"curvature = {curvature}", font_size=13, color="#666", text_anchor="middle"))
    scene.add(Text(300, 410, "P₁ = midpoint + perpendicular × curvature × length / 2", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "09-curvature-calculation.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Basic Bézier
    "01-bezier-basic": example_01_bezier_basic,
    "02-weight-components": example_02_weight_components,

    # Weight distribution
    "03-weight-distribution": example_03_weight_distribution,
    "04-control-point-influence": example_04_control_point_influence,

    # De Casteljau's algorithm
    "05-de-casteljau-step1": example_05_de_casteljau_step1,
    "06-de-casteljau-step2": example_06_de_casteljau_step2,

    # Properties
    "07-convex-hull": example_07_convex_hull,
    "08-tangent-property": example_08_tangent_property,

    # Curvature
    "09-curvature-calculation": example_09_curvature_calculation,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-bezier-mathematics.md...")

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
