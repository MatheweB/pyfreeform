#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/02-positioning-along-paths.md

Generates visual examples showing:
- The along= pattern for lines, curves, ellipses
- Data-driven positioning using brightness
- Multiple points along paths

Corresponds to sections:
- The Pattern
- Works With All Pathables
- Data-Driven Positioning
- Multiple Points
"""

from pyfreeform import Scene, Palette, Dot, Line, Text, Point
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math


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
    Step by step visualization
    """
    scene = Scene(width=400, height=200, background="#f8f9fa")

    # Draw a line (like it would be in a cell)
    start_x, start_y = 50, 100
    end_x, end_y = 350, 100

    scene.add(Line(start_x, start_y, end_x, end_y, color="#64748b", width=3))

    # Add dot at t=0.5
    t = 0.5
    dot_x = start_x + (end_x - start_x) * t
    dot_y = start_y + (end_y - start_y) * t

    scene.add(Dot(dot_x, dot_y, radius=8, color="#ef4444"))

    # Code annotation
    scene.add(Text(200, 30, "path = cell.add_line(start='left', end='right')", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(200, 50, "cell.add_dot(along=path, t=0.5, radius=3)", font_size=11, color="#ef4444", text_anchor="middle", font_family="monospace"))

    # Label
    scene.add(Text(dot_x, dot_y + 30, "t=0.5 (midpoint)", font_size=13, color="#ef4444", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01-basic-pattern-line.svg")


# =============================================================================
# SECTION: Works With All Pathables
# =============================================================================

def example_02_along_line():
    """
    Show dot positioned along a line using brightness
    """
    scene = Scene(width=400, height=200, background="white")

    # Simulate a cell with a line
    start_x, start_y = 50, 100
    end_x, end_y = 350, 100

    scene.add(Line(start_x, start_y, end_x, end_y, color="#94a3b8", width=2.5))

    # Show several positions based on different "brightness" values
    brightness_values = [0.2, 0.5, 0.8]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        x = start_x + (end_x - start_x) * brightness
        y = start_y + (end_y - start_y) * brightness

        scene.add(Dot(x, y, radius=7, color=color))
        scene.add(Text(x, y - 25, f"brightness={brightness}", font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Line: Linear Interpolation", font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 180, "along=line, t=cell.brightness", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "02-along-line.svg")


def example_03_along_curve():
    """
    Show dot positioned along a curve using brightness
    """
    scene = Scene(width=400, height=250, background="white")

    # Create curve
    start = Point(50, 200)
    end = Point(350, 200)
    control = Point(200, 50)

    # Draw curve
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
            color="#94a3b8", width=2.5
        ))

    # Show positions
    brightness_values = [0.2, 0.5, 0.8]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        t = brightness
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

        scene.add(Dot(x, y, radius=7, color=color))
        scene.add(Text(x, y - 25, f"brightness={brightness}", font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Curve: Bézier Parametric", font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 235, "along=curve, t=cell.brightness", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "03-along-curve.svg")


def example_04_along_ellipse():
    """
    Show dot positioned along an ellipse using brightness
    """
    scene = Scene(width=400, height=300, background="white")

    # Draw ellipse
    cx, cy = 200, 150
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
            color="#94a3b8", width=2.5
        ))

    # Show positions
    brightness_values = [0.25, 0.5, 0.75]
    colors = ["#3b82f6", "#8b5cf6", "#ec4899"]

    for brightness, color in zip(brightness_values, colors):
        t = brightness
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)

        scene.add(Dot(x, y, radius=7, color=color))

        # Label outside
        label_x = cx + (rx + 35) * math.cos(angle)
        label_y = cy + (ry + 35) * math.sin(angle)
        scene.add(Text(label_x, label_y, f"b={brightness}", font_size=11, color=color, text_anchor="middle"))

    # Title
    scene.add(Text(200, 20, "Ellipse: Around Perimeter", font_size=15, color="#333", text_anchor="middle"))
    scene.add(Text(200, 285, "along=ellipse, t=cell.brightness", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-along-ellipse.svg")


def example_05_comparison_all_three():
    """
    Show all three path types side by side with same t values
    """
    scene = Scene(width=600, height=500, background="white")

    # Title
    scene.add(Text(300, 25, "All Pathables: Same Interface", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    # Line section
    y_offset = 80
    scene.add(Text(100, y_offset, "Line", font_size=14, color="#666", font_weight="bold"))
    start_x, start_y = 150, y_offset + 20
    end_x, end_y = 450, y_offset + 20
    scene.add(Line(start_x, start_y, end_x, end_y, color="#cbd5e1", width=2))

    for t in [0.25, 0.5, 0.75]:
        x = start_x + (end_x - start_x) * t
        y = start_y
        scene.add(Dot(x, y, radius=5, color="#3b82f6"))

    # Curve section
    y_offset = 200
    scene.add(Text(100, y_offset, "Curve", font_size=14, color="#666", font_weight="bold"))
    start = Point(150, y_offset + 80)
    end = Point(450, y_offset + 80)
    control = Point(300, y_offset + 20)

    points = []
    for i in range(101):
        t = i / 100
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#cbd5e1", width=2))

    for t_val in [0.25, 0.5, 0.75]:
        x = (1-t_val)**2 * start.x + 2*(1-t_val)*t_val * control.x + t_val**2 * end.x
        y = (1-t_val)**2 * start.y + 2*(1-t_val)*t_val * control.y + t_val**2 * end.y
        scene.add(Dot(x, y, radius=5, color="#3b82f6"))

    # Ellipse section
    y_offset = 360
    scene.add(Text(100, y_offset, "Ellipse", font_size=14, color="#666", font_weight="bold"))
    cx, cy = 300, y_offset + 50
    rx, ry = 120, 40

    points = []
    for i in range(101):
        t = i / 100
        angle = 2 * math.pi * t
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(points[i].x, points[i].y, points[i+1].x, points[i+1].y, color="#cbd5e1", width=2))

    for t_val in [0.25, 0.5, 0.75]:
        angle = 2 * math.pi * t_val
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        scene.add(Dot(x, y, radius=5, color="#3b82f6"))

    # Bottom note
    scene.add(Text(300, 475, "Same code works for all: cell.add_dot(along=path, t=value)", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))

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
        cell.add_diagonal(start="bottom_left", end="top_right", color="#cbd5e1", width=1.5)

    scene.save(OUTPUT_DIR / "06-data-driven-step2-lines.svg")


def example_06_data_driven_step3():
    """
    Add dots along diagonals based on brightness
    Creates smooth, organic distribution
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=20, cell_size=15)

    for cell in scene.grid:
        line = cell.add_diagonal(start="bottom_left", end="top_right", color="#cbd5e1", width=1)

        # Dot position based on brightness
        t = cell.brightness
        # Calculate position along diagonal
        x = cell.x + cell.width * t
        y = (cell.y + cell.height) - cell.height * t

        cell.add_dot(at=Point(x, y), radius=3, color="#3b82f6")

    scene.save(OUTPUT_DIR / "06-data-driven-step3-positioned.svg")


def example_07_brightness_distribution():
    """
    Show how brightness affects position more clearly
    Single row with varying brightness
    """
    scene = Scene(width=600, height=150, background="white")

    # Create 10 cells with increasing brightness
    for i in range(10):
        brightness = i / 9  # 0 to 1

        # Cell bounds
        x = 50 + i * 50
        y = 50

        # Draw diagonal line
        scene.add(Line(x, y + 50, x + 40, y, color="#cbd5e1", width=2))

        # Position dot based on brightness
        dot_x = x + 40 * brightness
        dot_y = y + 50 - 50 * brightness

        scene.add(Dot(dot_x, dot_y, radius=4, color="#3b82f6"))

        # Label brightness
        scene.add(Text(x + 20, y + 70, f"{brightness:.1f}", font_size=10, color="#666", text_anchor="middle"))

    # Title
    scene.add(Text(300, 20, "Brightness Controls Position", font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "07-brightness-distribution.svg")


# =============================================================================
# SECTION: Multiple Points
# =============================================================================

def example_08_multiple_points_step1():
    """
    Show a curve (before adding multiple points)
    """
    scene = Scene(width=500, height=250, background="white")

    # Create curve
    start = Point(50, 200)
    end = Point(450, 200)
    control = Point(250, 50)

    # Draw curve
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
            color="#94a3b8", width=3
        ))

    # Title
    scene.add(Text(250, 20, "Step 1: Create the curve", font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-multiple-points-step1.svg")


def example_08_multiple_points_step2():
    """
    Add 5 evenly spaced points along the curve
    """
    scene = Scene(width=500, height=250, background="white")

    # Create curve
    start = Point(50, 200)
    end = Point(450, 200)
    control = Point(250, 50)

    # Draw curve
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
            color="#94a3b8", width=3
        ))

    # Add 5 dots
    for i in range(5):
        t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

        scene.add(Dot(x, y, radius=6, color="#ef4444"))
        scene.add(Text(x, y - 20, f"t={t:.2f}", font_size=10, color="#ef4444", text_anchor="middle"))

    # Title
    scene.add(Text(250, 20, "Step 2: Add 5 evenly-spaced dots", font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-multiple-points-step2.svg")


def example_09_many_points():
    """
    Show many points along a curve (creates a dotted effect)
    """
    scene = Scene(width=500, height=250, background="white")

    # Create curve
    start = Point(50, 200)
    end = Point(450, 200)
    control = Point(250, 50)

    # Draw curve (lighter)
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
            color="#e5e7eb", width=2
        ))

    # Add many dots (20)
    for i in range(20):
        t = i / 19
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

        scene.add(Dot(x, y, radius=4, color="#3b82f6"))

    # Title
    scene.add(Text(250, 20, "Multiple Points: for i in range(20)", font_size=15, color="#333", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "09-many-points.svg")


def example_10_code_example():
    """
    Visualize the actual code example from the documentation
    """
    scene = Scene(width=550, height=280, background="#f8f9fa")

    # Create curve
    start = Point(50, 230)
    end = Point(500, 230)
    control = Point(275, 80)

    # Draw curve
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

    # Add 5 dots
    for i in range(5):
        t = i / 4
        x = (1-t)**2 * start.x + 2*(1-t)*t * control.x + t**2 * end.x
        y = (1-t)**2 * start.y + 2*(1-t)*t * control.y + t**2 * end.y

        scene.add(Dot(x, y, radius=5, color="#ef4444"))

    # Code
    scene.add(Text(275, 25, "curve = cell.add_curve(curvature=0.5)", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 45, "for i in range(5):", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 65, "    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(275, 85, "    cell.add_dot(along=curve, t=t, radius=2)", font_size=11, color="#ef4444", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "10-code-example.svg")


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
