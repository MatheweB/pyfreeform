#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/02-positioning-along-paths.md

Generates visual examples showing:
- The along= pattern for lines, curves, ellipses
- Data-driven positioning using brightness
- Multiple points along paths
- Along= for all entity types
- Tangent alignment (align=True)
- TextPath (text warped along paths)
- Lines and curves along paths

Corresponds to sections:
- The Pattern
- Works With All Pathables
- Data-Driven Positioning
- Multiple Points
- Along= for All Entities
- Tangent Alignment
- Text Along Paths
- Lines and Curves Along Paths
"""

from pyfreeform import Scene, Text, Point
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-positioning-along-paths"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_gradient_image() -> Path:
    """Create a simple diagonal gradient for data-driven examples"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_diagonal_gradient.png"

    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Diagonal gradient
            brightness = (x + y) / 800
            val = int(brightness * 255)
            draw.point((x, y), fill=(val, val, val))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_gradient_image()


# =============================================================================
# SECTION: The Pattern - Basic along= usage
# =============================================================================

def example_01_basic_pattern_line():
    """
    Show the basic pattern: path = cell.add_line(...); cell.add_dot(along=path, t=0.5)
    Uses the actual along= API to position the dot.
    """
    scene = Scene(width=400, height=200, background="#f8f9fa")

    # Draw a line across the scene
    line = scene.add_line(
        start=Point(50, 100), end=Point(350, 100),
        color="#64748b", width=3,
    )

    # Add dot at t=0.5 using along=
    scene.add_dot(along=line, t=0.5, radius=8, color="#ef4444")

    # Code annotation
    scene.add(Text(200, 30, "path = cell.add_line(start='left', end='right')",
                   font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(200, 50, "cell.add_dot(along=path, t=0.5, radius=3)",
                   font_size=11, color="#ef4444", text_anchor="middle", font_family="monospace"))

    # Label at dot position
    pt = line.point_at(0.5)
    scene.add(Text(pt.x, pt.y + 30, "t=0.5 (midpoint)",
                   font_size=13, color="#ef4444", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01-basic-pattern-line.svg")


# =============================================================================
# SECTION: Works With All Pathables
# =============================================================================

def example_02_along_line():
    """
    Show dot positioned along a line at different brightness values.
    Uses along= for each dot.
    """
    scene = Scene(width=400, height=200, background="white")

    # Create the line
    line = scene.add_line(
        start=Point(50, 100), end=Point(350, 100),
        color="#94a3b8", width=2.5,
    )

    # Show several positions based on different "brightness" values
    brightness_values = [0.2, 0.5, 0.8]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        scene.add_dot(along=line, t=brightness, radius=7, color=color)

        pt = line.point_at(brightness)
        scene.add(Text(pt.x, pt.y - 25, f"brightness={brightness}",
                       font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Line: Linear Interpolation",
                   font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 180, "along=line, t=cell.brightness",
                   font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "02-along-line.svg")


def example_03_along_curve():
    """
    Show dot positioned along a curve at different brightness values.
    Uses a Curve entity instead of manually computing Bézier segments.
    """
    scene = Scene(width=400, height=250, background="white")

    # Create the curve using the Curve entity (bowing upward)
    curve = scene.add_curve(
        start=Point(50, 200), end=Point(350, 200),
        curvature=-1.0,  # Negative = bows upward in SVG
        color="#94a3b8", width=2.5,
    )

    # Show positions along the curve
    brightness_values = [0.2, 0.5, 0.8]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        scene.add_dot(along=curve, t=brightness, radius=7, color=color)

        pt = curve.point_at(brightness)
        scene.add(Text(pt.x, pt.y - 25, f"brightness={brightness}",
                       font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Curve: Bézier Parametric",
                   font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 235, "along=curve, t=cell.brightness",
                   font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "03-along-curve.svg")


def example_04_along_ellipse():
    """
    Show dot positioned along an ellipse at different brightness values.
    Uses an Ellipse entity instead of manually computing line segments.
    """
    scene = Scene(width=400, height=300, background="white")

    # Create the ellipse (stroke-only, no fill)
    ellipse = scene.add_ellipse(
        at=Point(200, 150), rx=150, ry=100,
        fill=None, stroke="#94a3b8", stroke_width=2.5,
    )

    # Show positions around the ellipse
    brightness_values = [0.25, 0.5, 0.75]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        scene.add_dot(along=ellipse, t=brightness, radius=7, color=color)

        # Label outside the ellipse
        pt = ellipse.point_at(brightness)
        # Push the label outward from center
        dx = pt.x - 200
        dy = pt.y - 150
        import math
        dist = math.sqrt(dx * dx + dy * dy) if (dx or dy) else 1
        label_x = pt.x + dx / dist * 15
        label_y = pt.y + dy / dist * 15
        scene.add(Text(label_x, label_y, f"b={brightness}",
                       font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Ellipse: Around Perimeter",
                   font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 285, "along=ellipse, t=cell.brightness",
                   font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-along-ellipse.svg")


def example_05_comparison_all_three():
    """
    Show all three path types side by side with same t values.
    Uses actual Line, Curve, and Ellipse entities with along= for dots.
    """
    scene = Scene(width=600, height=500, background="white")

    # Title
    scene.add(Text(300, 25, "All Pathables: Same Interface",
                   font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    # --- Line section ---
    y_offset = 80
    scene.add(Text(100, y_offset, "Line",
                   font_size=14, color="#666", font_weight="bold"))

    line = scene.add_line(
        start=Point(150, y_offset + 20), end=Point(450, y_offset + 20),
        color="#cbd5e1", width=2,
    )

    for t in [0.25, 0.5, 0.75]:
        scene.add_dot(along=line, t=t, radius=5, color="#3b82f6")

    # --- Curve section ---
    y_offset = 200
    scene.add(Text(100, y_offset, "Curve",
                   font_size=14, color="#666", font_weight="bold"))

    curve = scene.add_curve(
        start=Point(150, y_offset + 80), end=Point(450, y_offset + 80),
        curvature=-0.75,  # Bows upward
        color="#cbd5e1", width=2,
    )

    for t in [0.25, 0.5, 0.75]:
        scene.add_dot(along=curve, t=t, radius=5, color="#3b82f6")

    # --- Ellipse section ---
    y_offset = 360
    scene.add(Text(100, y_offset, "Ellipse",
                   font_size=14, color="#666", font_weight="bold"))

    ellipse = scene.add_ellipse(
        at=Point(300, y_offset + 50), rx=120, ry=40,
        fill=None, stroke="#cbd5e1", stroke_width=2,
    )

    for t in [0.25, 0.5, 0.75]:
        scene.add_dot(along=ellipse, t=t, radius=5, color="#3b82f6")

    # Bottom note
    scene.add(Text(300, 475,
                   "Same code works for all: cell.add_dot(along=path, t=value)",
                   font_size=12, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "05-comparison-all-three.svg")


# =============================================================================
# SECTION: Data-Driven Positioning
# =============================================================================

def example_06_data_driven_step1():
    """
    Show grid with varying brightness (before adding dots)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=20, cell_size=15)

    # Just show the grid structure
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "06-data-driven-step1-grid.svg")


def example_06_data_driven_step2():
    """
    Add diagonal lines to cells
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=20, cell_size=15)

    for cell in scene.grid:
        # Add diagonal line
        cell.add_diagonal(start="bottom_left", end="top_right",
                          color="#cbd5e1", width=1.5)

    scene.save(OUTPUT_DIR / "06-data-driven-step2-lines.svg")


def example_06_data_driven_step3():
    """
    Add dots along diagonals based on brightness.
    Uses along= and t=cell.brightness for smooth, organic distribution.
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=20, cell_size=15)

    for cell in scene.grid:
        line = cell.add_diagonal(start="bottom_left", end="top_right",
                                 color="#cbd5e1", width=1)

        # Dot position driven by brightness using along=
        cell.add_dot(along=line, t=cell.brightness, radius=3, color="#3b82f6")

    scene.save(OUTPUT_DIR / "06-data-driven-step3-positioned.svg")


def example_07_brightness_distribution():
    """
    Show how brightness affects position more clearly.
    Single row with varying brightness, using along= for each dot.
    """
    scene = Scene(width=600, height=150, background="white")

    # Create 10 "cells" with increasing brightness
    for i in range(10):
        brightness = i / 9  # 0 to 1

        # Cell bounds
        x = 50 + i * 50
        y = 50

        # Draw diagonal line and position dot along it
        line = scene.add_line(
            start=Point(x, y + 50), end=Point(x + 40, y),
            color="#cbd5e1", width=2,
        )

        scene.add_dot(along=line, t=brightness, radius=4, color="#3b82f6")

        # Label brightness
        scene.add(Text(x + 20, y + 70, f"{brightness:.1f}",
                       font_size=10, color="#666", text_anchor="middle"))

    # Title
    scene.add(Text(300, 20, "Brightness Controls Position",
                   font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "07-brightness-distribution.svg")


# =============================================================================
# SECTION: Multiple Points
# =============================================================================

def example_08_multiple_points_step1():
    """
    Show a curve (before adding multiple points).
    Uses a Curve entity instead of manually computing line segments.
    """
    scene = Scene(width=500, height=250, background="white")

    # Create a single Curve entity
    scene.add_curve(
        start=Point(50, 200), end=Point(450, 200),
        curvature=-0.75,  # Bows upward
        color="#94a3b8", width=3,
    )

    # Title
    scene.add(Text(250, 20, "Step 1: Create the curve",
                   font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-multiple-points-step1.svg")


def example_08_multiple_points_step2():
    """
    Add 5 evenly spaced points along the curve using along=.
    """
    scene = Scene(width=500, height=250, background="white")

    # Create the curve
    curve = scene.add_curve(
        start=Point(50, 200), end=Point(450, 200),
        curvature=-0.75,
        color="#94a3b8", width=3,
    )

    # Add 5 dots along the curve using along=
    for i in range(5):
        t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0
        scene.add_dot(along=curve, t=t, radius=6, color="#ef4444")

        pt = curve.point_at(t)
        scene.add(Text(pt.x, pt.y - 20, f"t={t:.2f}",
                       font_size=10, color="#ef4444", text_anchor="middle"))

    # Title
    scene.add(Text(250, 20, "Step 2: Add 5 evenly-spaced dots",
                   font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-multiple-points-step2.svg")


def example_09_many_points():
    """
    Show many points along a curve (creates a dotted effect).
    Uses along= for all 20 dots.
    """
    scene = Scene(width=500, height=250, background="white")

    # Create the curve (lighter)
    curve = scene.add_curve(
        start=Point(50, 200), end=Point(450, 200),
        curvature=-0.75,
        color="#e5e7eb", width=2,
    )

    # Add many dots (20) along the curve
    for i in range(20):
        t = i / 19
        scene.add_dot(along=curve, t=t, radius=4, color="#3b82f6")

    # Title
    scene.add(Text(250, 20, "Multiple Points: for i in range(20)",
                   font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "09-many-points.svg")


def example_10_code_example():
    """
    Visualize the actual code example from the documentation.
    Uses the proper API: add_curve + add_dot(along=...).
    """
    scene = Scene(width=550, height=280, background="#f8f9fa")

    # Create the curve
    curve = scene.add_curve(
        start=Point(50, 230), end=Point(500, 230),
        curvature=-0.67,
        color="#64748b", width=2.5,
    )

    # Add 5 dots along the curve
    for i in range(5):
        t = i / 4
        scene.add_dot(along=curve, t=t, radius=5, color="#ef4444")

    # Code annotations
    scene.add(Text(275, 25, "curve = cell.add_curve(curvature=0.5)",
                   font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 45, "for i in range(5):",
                   font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 65, "    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0",
                   font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 85, "    cell.add_dot(along=curve, t=t, radius=2)",
                   font_size=11, color="#ef4444", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "10-code-example.svg")


# =============================================================================
# SECTION: Along for All Entity Types
# =============================================================================

def example_11_along_all_entities():
    """
    Show all entity types positioned along a single curve on a plain Scene.
    Demonstrates that dots, text, rects, ellipses, polygons, and lines can
    all use the along= parameter.
    """
    scene = Scene(width=600, height=300, background="white")

    # Draw a big curve across the scene
    curve = scene.add_curve(
        start=(0.05, 0.75),
        end=(0.95, 0.75),
        curvature=0.7,
        color="#cbd5e1",
        width=3,
    )

    # Dot at t=0.0
    scene.add_dot(along=curve, t=0.0, radius=8, color="#ef4444")
    scene.add_text("Dot (t=0.0)", along=curve, t=0.0, align=True,
                   font_size=10, color="#ef4444")

    # Text at t=0.2 (positioned, not warped)
    scene.add_text("Text", along=curve, t=0.2, align=True,
                   font_size=14, color="#8b5cf6")
    scene.add_text("(t=0.2)", along=curve, t=0.18, align=True,
                   font_size=9, color="#8b5cf6")

    # Rect at t=0.4
    scene.add_rect(width=30, height=16, along=curve, t=0.4, align=True,
                   fill="#3b82f6", opacity=0.8)
    scene.add_text("Rect (t=0.4)", along=curve, t=0.4, align=True,
                   font_size=9, color="#3b82f6")

    # Ellipse at t=0.6
    scene.add_ellipse(rx=18, ry=10, along=curve, t=0.6, align=True,
                      fill="#06b6d4", opacity=0.8)
    scene.add_text("Ellipse (t=0.6)", along=curve, t=0.6, align=True,
                   font_size=9, color="#06b6d4")

    # Polygon (diamond) at t=0.8
    diamond = [(0.5, 0.2), (0.8, 0.5), (0.5, 0.8), (0.2, 0.5)]
    scene.add_polygon(diamond, along=curve, t=0.8, align=True,
                      fill="#f59e0b", opacity=0.8)
    scene.add_text("Polygon (t=0.8)", along=curve, t=0.8, align=True,
                   font_size=9, color="#f59e0b")

    # Line (tick mark) at t=1.0
    scene.add_line(start=(0.48, 0.45), end=(0.52, 0.55),
                   along=curve, t=1.0, align=True,
                   color="#10b981", width=3)
    scene.add_text("Line (t=1.0)", along=curve, t=1.0, align=True,
                   font_size=9, color="#10b981")

    # Title
    scene.add(Text(300, 20, "All Entity Types Along a Curve",
                   font_size=16, color="#334155", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "11-along-all-entities.svg")


def example_12_align_vs_no_align():
    """
    Two rows comparing align=False (default) vs align=True.
    5 rects at t=0, 0.25, 0.5, 0.75, 1.0 along a curve.
    Without align they stay axis-aligned; with align they follow the tangent.
    """
    scene = Scene(width=550, height=350, background="white")

    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors = ["#ef4444", "#f59e0b", "#3b82f6", "#8b5cf6", "#10b981"]

    # --- Top row: no align ---
    scene.add(Text(275, 25, "align=False (default)", font_size=14,
                   color="#334155", text_anchor="middle"))

    curve_top = scene.add_curve(
        start=(0.05, 0.45),
        end=(0.95, 0.45),
        curvature=0.5,
        color="#cbd5e1",
        width=2,
    )

    for t, col in zip(t_values, colors):
        scene.add_rect(width=24, height=12, along=curve_top, t=t,
                       align=False, fill=col, opacity=0.85)
        scene.add_text(f"t={t}", along=curve_top, t=t,
                       font_size=8, color=col)

    # --- Bottom row: align=True ---
    scene.add(Text(275, 195, "align=True", font_size=14,
                   color="#334155", text_anchor="middle"))

    curve_bot = scene.add_curve(
        start=(0.05, 0.9),
        end=(0.95, 0.9),
        curvature=0.5,
        color="#cbd5e1",
        width=2,
    )

    for t, col in zip(t_values, colors):
        scene.add_rect(width=24, height=12, along=curve_bot, t=t,
                       align=True, fill=col, opacity=0.85)
        scene.add_text(f"t={t}", along=curve_bot, t=t, align=True,
                       font_size=8, color=col)

    scene.save(OUTPUT_DIR / "12-align-vs-no-align.svg")


def example_13_align_rects_on_curve():
    """
    Grid from TEST_IMAGE (grid_size=15, cell_size=20).
    Each cell gets a curve and 3 rects aligned along it, colored by cell.color.
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=15, cell_size=20)

    for cell in scene.grid:
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.4,
            color="#cbd5e1",
            width=0.5,
        )

        for i in range(3):
            t = (i + 1) / 4  # t = 0.25, 0.5, 0.75
            cell.add_rect(
                width=6, height=3,
                along=curve, t=t, align=True,
                fill=cell.color,
            )

    scene.save(OUTPUT_DIR / "13-align-rects-on-curve.svg")


def example_14_textpath_curve():
    """
    Scene-level textPath: warp text along a curve using SVG <textPath>.
    add_text with along= but WITHOUT t= triggers warp mode.
    """
    scene = Scene(width=500, height=250, background="#f8f9fa")

    # Title
    scene.add(Text(250, 25, "Text Warped Along a Curve (textPath)",
                   font_size=14, color="#334155", text_anchor="middle"))

    # Create a wide curve
    curve = scene.add_curve(
        start=(0.05, 0.5),
        end=(0.95, 0.55),
        curvature=0.6,
        color="#e2e8f0",
        width=2,
    )

    # Warp text along the curve (no t= means textPath mode)
    scene.add_text(
        "Hello World along a curve!",
        along=curve,
        color="#6366f1",
        font_size=14,
        text_anchor="left"
    )

    scene.save(OUTPUT_DIR / "14-textpath-curve.svg")


def example_15_textpath_ellipse():
    """
    Scene-level textPath along an ellipse.
    Warp text around an ellipse perimeter using SVG <textPath>.
    """
    scene = Scene(width=400, height=300, background="#f8f9fa")

    # Title
    scene.add(Text(200, 25, "Text Warped Along an Ellipse",
                   font_size=14, color="#334155", text_anchor="middle"))

    # Create an ellipse at center
    ellipse = scene.add_ellipse(
        at="center",
        rx=130, ry=80,
        fill=None,
        stroke="#e2e8f0",
        stroke_width=2,
    )

    # Warp text along the ellipse (no t= means textPath mode)
    scene.add_text(
        "Text flowing around an ellipse path...",
        along=ellipse,
        color="coral",
        font_size=14,
    )

    scene.save(OUTPUT_DIR / "15-textpath-ellipse.svg")


def example_16_lines_along_path():
    """
    Grid from TEST_IMAGE (grid_size=12, cell_size=25).
    Each cell gets a curve with 4 small perpendicular tick-mark lines
    distributed along it with align=True.
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=12, cell_size=25)

    for cell in scene.grid:
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.4,
            color="#94a3b8",
            width=1,
        )

        # 4 tick marks at t = 0.1, 0.35, 0.65, 0.9
        for t in [0.1, 0.35, 0.65, 0.9]:
            cell.add_line(
                start=(0.45, 0.5),
                end=(0.55, 0.5),
                along=curve, t=t, align=True,
                color=cell.color,
                width=2,
            )

    scene.save(OUTPUT_DIR / "16-lines-along-path.svg")


def example_17_complete_example():
    """
    Comprehensive parametric art: grid from TEST_IMAGE (grid_size=20, cell_size=15).
    Each cell: curve with curvature based on brightness, 3 aligned rects colored
    by cell.color, and 2 dots at the endpoints.
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=20, cell_size=15)

    for cell in scene.grid:
        b = cell.brightness

        # Curvature varies with brightness: dark cells = flat, bright = bowed
        curvature = 0.1 + b * 0.7

        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            color="#94a3b8",
            width=0.5,
        )

        # 3 aligned rects along the curve
        for i in range(3):
            t = (i + 1) / 4  # 0.25, 0.5, 0.75
            cell.add_rect(
                width=5, height=3,
                along=curve, t=t, align=True,
                fill=cell.color,
            )

        # Dots at endpoints
        cell.add_dot(along=curve, t=0.0, radius=1.5, color="#6366f1")
        cell.add_dot(along=curve, t=1.0, radius=1.5, color="#ec4899")

    scene.save(OUTPUT_DIR / "17-complete-example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Basic pattern
    "01-basic-pattern-line": example_01_basic_pattern_line,

    # Works with all pathables
    "02-along-line": example_02_along_line,
    "03-along-curve": example_03_along_curve,
    "04-along-ellipse": example_04_along_ellipse,
    "05-comparison-all-three": example_05_comparison_all_three,

    # Data-driven positioning
    "06-data-driven-step1-grid": example_06_data_driven_step1,
    "06-data-driven-step2-lines": example_06_data_driven_step2,
    "06-data-driven-step3-positioned": example_06_data_driven_step3,
    "07-brightness-distribution": example_07_brightness_distribution,

    # Multiple points
    "08-multiple-points-step1": example_08_multiple_points_step1,
    "08-multiple-points-step2": example_08_multiple_points_step2,
    "09-many-points": example_09_many_points,
    "10-code-example": example_10_code_example,

    # Along for all entity types
    "11-along-all-entities": example_11_along_all_entities,
    "12-align-vs-no-align": example_12_align_vs_no_align,
    "13-align-rects-on-curve": example_13_align_rects_on_curve,
    "14-textpath-curve": example_14_textpath_curve,
    "15-textpath-ellipse": example_15_textpath_ellipse,
    "16-lines-along-path": example_16_lines_along_path,
    "17-complete-example": example_17_complete_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-positioning-along-paths.md...")

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
