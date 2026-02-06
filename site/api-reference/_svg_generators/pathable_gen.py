#!/usr/bin/env python3
"""
SVG Generator for: api-reference/pathable.md

Generates visual examples demonstrating the Pathable protocol and point_at() method.
"""

from pyfreeform import Scene, Palette, Dot, Line, Curve, Ellipse
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "pathable"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Line.point_at()
# =============================================================================

def example1_line_point_at():
    """Line.point_at(t) - Get points along a line"""
    scene = Scene(width=400, height=200, background="#1a1a2e")
    colors = Palette.ocean()

    # Create line
    line = Line(50, 100, 350, 100, color=colors.line, width=2)
    scene.add(line)

    # Add dots at different t values
    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    dot_colors = ["#ee4266", "#ffd23f", "#64ffda", "#ffd23f", "#ee4266"]

    for t, color in zip(t_values, dot_colors):
        point = line.point_at(t)
        scene.add(Dot(point.x, point.y, radius=6, color=color))

        # Label
        from pyfreeform import Text
        scene.add(Text(point.x, 130, f"t={t}", font_size=10, color=color, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "example1-line-point-at.svg")


# =============================================================================
# Curve.point_at()
# =============================================================================

def example2_curve_point_at():
    """Curve.point_at(t) - Get points along a curve"""
    scene = Scene(width=400, height=250, background="#1a1a2e")
    colors = Palette.midnight()

    # Create curve
    curve = Curve(50, 200, 350, 200, curvature=0.6, color=colors.line, width=2)
    scene.add(curve)

    # Add dots at different t values
    t_values = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]

    for t in t_values:
        point = curve.point_at(t)
        scene.add(Dot(point.x, point.y, radius=5, color=colors.accent))

    scene.save(OUTPUT_DIR / "example2-curve-point-at.svg")


# =============================================================================
# Ellipse.point_at()
# =============================================================================

def example3_ellipse_point_at():
    """Ellipse.point_at(t) - Get points around ellipse perimeter"""
    scene = Scene(width=400, height=400, background="#1a1a2e")
    colors = Palette.ocean()

    # Create ellipse
    ellipse = Ellipse(200, 200, rx=120, ry=80, fill=None, stroke=colors.line, stroke_width=2)
    scene.add(ellipse)

    # Add dots at different t values (around perimeter)
    n_dots = 8
    for i in range(n_dots):
        t = i / n_dots
        point = ellipse.point_at(t)
        scene.add(Dot(point.x, point.y, radius=6, color=colors.accent))

    scene.save(OUTPUT_DIR / "example3-ellipse-point-at.svg")


# =============================================================================
# Using along= parameter with Line
# =============================================================================

def example4_along_line():
    """cell.add_dot(along=line, t=...) - Position dots along a line"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=400, background="#1a1a2e")
    colors = Palette.midnight()

    cell = scene.grid[0, 0]

    # Create path
    line = cell.add_line(start="left", end="right", color=colors.line, width=2)

    # Position dots along the path
    for i in range(7):
        t = i / 6
        cell.add_dot(along=line, t=t, radius=5, color=colors.primary)

    scene.save(OUTPUT_DIR / "example4-along-line.svg")


# =============================================================================
# Using along= parameter with Curve
# =============================================================================

def example5_along_curve():
    """cell.add_dot(along=curve, t=...) - Position dots along a curve"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=400, background="#1a1a2e")
    colors = Palette.ocean()

    cell = scene.grid[0, 0]

    # Create curved path
    curve = cell.add_curve(
        start="left",
        end="right",
        curvature=0.5,
        color=colors.line,
        width=2
    )

    # Position dots along the curve
    for i in range(9):
        t = i / 8
        cell.add_dot(along=curve, t=t, radius=5, color=colors.accent)

    scene.save(OUTPUT_DIR / "example5-along-curve.svg")


# =============================================================================
# Using along= parameter with Ellipse
# =============================================================================

def example6_along_ellipse():
    """cell.add_dot(along=ellipse, t=...) - Position dots around ellipse"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=400, background="#1a1a2e")
    colors = Palette.midnight()

    cell = scene.grid[0, 0]

    # Create ellipse path
    ellipse = cell.add_ellipse(
        rx=150,
        ry=100,
        fill=None,
        stroke=colors.line,
        stroke_width=2
    )

    # Position dots around the ellipse
    for i in range(12):
        t = i / 12
        cell.add_dot(along=ellipse, t=t, radius=6, color=colors.primary)

    scene.save(OUTPUT_DIR / "example6-along-ellipse.svg")


# =============================================================================
# Multiple dots along curve with varying size
# =============================================================================

def example7_varying_sizes():
    """Varying dot sizes along a curve"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=400, background="#1a1a2e")
    colors = Palette.ocean()

    cell = scene.grid[0, 0]

    # Create curve
    curve = cell.add_curve(
        start="bottom_left",
        end="top_right",
        curvature=0.4,
        color=colors.line,
        width=2
    )

    # Dots with varying sizes
    for i in range(15):
        t = i / 14
        # Size increases then decreases
        size = 3 + 10 * (1 - abs(2*t - 1))
        cell.add_dot(along=curve, t=t, radius=size, color=colors.accent)

    scene.save(OUTPUT_DIR / "example7-varying-sizes.svg")


# =============================================================================
# Comparing all three Pathable types
# =============================================================================

def example8_comparison():
    """Compare Line, Curve, and Ellipse pathable behaviors"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=150, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Line
    line = cells[0].add_line(start="left", end="right", color=colors.line, width=2)
    for i in range(5):
        t = i / 4
        cells[0].add_dot(along=line, t=t, radius=4, color=colors.primary)

    # Curve
    curve = cells[1].add_curve(start="left", end="right", curvature=0.5, color=colors.line, width=2)
    for i in range(5):
        t = i / 4
        cells[1].add_dot(along=curve, t=t, radius=4, color=colors.secondary)

    # Ellipse
    ellipse = cells[2].add_ellipse(rx=50, ry=30, fill=None, stroke=colors.line, stroke_width=2)
    for i in range(8):
        t = i / 8
        cells[2].add_dot(along=ellipse, t=t, radius=4, color=colors.accent)

    scene.save(OUTPUT_DIR / "example8-comparison.svg")


# =============================================================================
# Complex path arrangement
# =============================================================================

def example9_complex():
    """Complex arrangement using multiple paths"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=500, background="#1a1a2e")
    colors = Palette.ocean()

    cell = scene.grid[0, 0]

    # Create multiple curves
    curve1 = cell.add_curve(
        start="left",
        end="right",
        curvature=0.5,
        color=colors.line,
        width=1
    )

    curve2 = cell.add_curve(
        start="top",
        end="bottom",
        curvature=0.5,
        color=colors.line,
        width=1
    )

    # Place dots along both curves
    for i in range(10):
        t = i / 9
        cell.add_dot(along=curve1, t=t, radius=5, color=colors.primary)
        cell.add_dot(along=curve2, t=t, radius=5, color=colors.accent)

    scene.save(OUTPUT_DIR / "example9-complex.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-line-point-at": example1_line_point_at,
    "example2-curve-point-at": example2_curve_point_at,
    "example3-ellipse-point-at": example3_ellipse_point_at,
    "example4-along-line": example4_along_line,
    "example5-along-curve": example5_along_curve,
    "example6-along-ellipse": example6_along_ellipse,
    "example7-varying-sizes": example7_varying_sizes,
    "example8-comparison": example8_comparison,
    "example9-complex": example9_complex,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for pathable.md...")

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
