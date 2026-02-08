#!/usr/bin/env python3
"""
SVG Generator for: color-and-style/03-style-objects.md

Generates visual examples demonstrating style objects and their usage.

Corresponds to sections:
- DotStyle
- LineStyle
- FillStyle
- BorderStyle
"""

from pathlib import Path
from pyfreeform import Scene, Dot, Line, Rect, Connection, Polygon
from pyfreeform.config import (
    DotStyle, LineStyle, FillStyle, BorderStyle,
    ShapeStyle, TextStyle, ConnectionStyle,
)


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-style-objects"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: DotStyle
# =============================================================================

def example_01_dotstyle_basic():
    """
    Basic DotStyle usage with radius, color, and z_index
    """
    scene = Scene.with_grid(cols=10, rows=3, cell_size=50)
    scene.background = "#f8f9fa"

    style = DotStyle(radius=5, color="coral", z_index=0)

    # Create a pattern using the same style
    for cell in scene.grid:
        cell.add_dot(style=style)

    scene.save(OUTPUT_DIR / "01-dotstyle-basic.svg")


def example_02_dotstyle_builder_methods():
    """
    Demonstrate builder methods: with_radius() and with_color()
    """
    scene = Scene.with_grid(cols=8, rows=3, cell_size=80)
    scene.background = "#f8f9fa"

    # Base style
    base_style = DotStyle(radius=5, color="coral", z_index=0)

    cells = list(scene.grid)

    # Row 1: Original style
    for i in range(8):
        cells[i].add_dot(style=base_style)

    # Row 2: Modified with larger radius
    large = base_style.with_radius(10)
    for i in range(8, 16):
        cells[i].add_dot(style=large)

    # Row 3: Modified with different color
    blue = base_style.with_color("blue")
    for i in range(16, 24):
        cells[i].add_dot(style=blue)

    scene.save(OUTPUT_DIR / "02-dotstyle-builder-methods.svg")


def example_03_dotstyle_variations():
    """
    Create variations of a style showing different sizes and colors
    """
    scene = Scene.with_grid(cols=8, rows=2, cell_size=85)
    scene.background = "#ffffff"

    base_style = DotStyle(radius=8, color="#3498db", z_index=0)

    cells = list(scene.grid)

    # Size variations (row 1)
    sizes = [4, 6, 8, 10, 12, 14, 16, 18]
    for i, size in enumerate(sizes):
        variant = base_style.with_radius(size)
        cells[i].add_dot(style=variant)

    # Color variations (row 2)
    colors = ["#e74c3c", "#e67e22", "#f39c12", "#2ecc71", "#1abc9c", "#3498db", "#9b59b6", "#34495e"]
    for i, color in enumerate(colors):
        variant = base_style.with_color(color)
        cells[i + 8].add_dot(style=variant)

    scene.save(OUTPUT_DIR / "03-dotstyle-variations.svg")


# =============================================================================
# SECTION: LineStyle
# =============================================================================

def example_04_linestyle_basic():
    """
    Basic LineStyle with width, color, cap, and z_index
    """
    scene = Scene.with_grid(cols=1, rows=6, cell_size=50)
    scene.background = "#f8f9fa"

    # Resize scene to be wider
    scene = Scene(width=700, height=400, background="#f8f9fa")

    style = LineStyle(width=2, color="navy", cap="round", z_index=0)

    # Create a pattern of lines
    for i in range(6):
        y = 80 + i * 50
        scene.add(Line(x1=50, y1=y, x2=650, y2=y, color=style.color, width=style.width))

    scene.save(OUTPUT_DIR / "04-linestyle-basic.svg")


def example_05_linestyle_cap_options():
    """
    Demonstrate different cap options: round, square, butt
    """
    scene = Scene(width=700, height=350, background="#f8f9fa")

    caps = ["round", "square", "butt"]
    colors = ["#e74c3c", "#3498db", "#2ecc71"]

    for i, (cap, color) in enumerate(zip(caps, colors)):
        y = 100 + i * 100

        # Draw thick line to show cap style - note: pyfreeform Line doesn't expose cap directly
        scene.add(Line(x1=100, y1=y, x2=600, y2=y, color=color, width=15, cap=cap))

        # Add guide dots to show endpoints
        scene.add(Dot(x=100, y=y, radius=3, color="#95a5a6"))
        scene.add(Dot(x=600, y=y, radius=3, color="#95a5a6"))

    scene.save(OUTPUT_DIR / "05-linestyle-cap-options.svg")


def example_06_linestyle_widths():
    """
    Show various line widths
    """
    scene = Scene(width=700, height=450, background="#ffffff")

    widths = [1, 2, 3, 5, 8, 10, 15, 20]

    for i, width in enumerate(widths):
        y = 50 + i * 50
        scene.add(Line(x1=50, y1=y, x2=650, y2=y, color="#34495e", width=width))

    scene.save(OUTPUT_DIR / "06-linestyle-widths.svg")


# =============================================================================
# SECTION: FillStyle
# =============================================================================

def example_07_fillstyle_basic():
    """
    Basic FillStyle with color, opacity, and z_index
    """
    scene = Scene.with_grid(cols=4, rows=1, cell_size=150)
    scene.background = "#f8f9fa"

    style = FillStyle(color="blue", z_index=0)

    # Create overlapping effect by using cells
    for cell in scene.grid:
        cell.add_fill(style=style)

    scene.save(OUTPUT_DIR / "07-fillstyle-basic.svg")


def example_08_fillstyle_opacity():
    """
    Demonstrate different opacity values
    """
    scene = Scene.with_grid(cols=5, rows=1, cell_size=140)
    scene.background = "#ffffff"

    opacities = [1.0, 0.8, 0.6, 0.4, 0.2]

    cells = list(scene.grid)
    for i, opacity in enumerate(opacities):
        style = FillStyle(color="#e74c3c", opacity=opacity, z_index=0)
        cells[i].add_fill(style=style)

    scene.save(OUTPUT_DIR / "08-fillstyle-opacity.svg")


def example_09_fillstyle_colors():
    """
    Show various fill colors
    """
    scene = Scene.with_grid(cols=4, rows=2, cell_size=160)
    scene.background = "#2c3e50"

    colors = ["#e74c3c", "#e67e22", "#f39c12", "#2ecc71", "#1abc9c", "#3498db", "#9b59b6", "#ecf0f1"]

    cells = list(scene.grid)
    for i, color in enumerate(colors):
        if i < len(cells):
            style = FillStyle(color=color, z_index=0)
            cells[i].add_fill(style=style)

    scene.save(OUTPUT_DIR / "09-fillstyle-colors.svg")


# =============================================================================
# SECTION: BorderStyle
# =============================================================================

def example_10_borderstyle_basic():
    """
    Basic BorderStyle with width, color, and z_index
    """
    scene = Scene.with_grid(cols=5, rows=3, cell_size=100)
    scene.background = "#f8f9fa"

    style = BorderStyle(width=1, color="#cccccc", z_index=0)

    # Create a grid pattern
    for cell in scene.grid:
        cell.add_border(style=style)

    scene.save(OUTPUT_DIR / "10-borderstyle-basic.svg")


def example_11_borderstyle_widths():
    """
    Demonstrate different border widths
    """
    scene = Scene.with_grid(cols=5, rows=1, cell_size=140)
    scene.background = "#ffffff"

    widths = [0.5, 1, 2, 4, 6]

    cells = list(scene.grid)
    for i, width in enumerate(widths):
        style = BorderStyle(width=width, color="#34495e", z_index=0)
        cells[i].add_border(style=style)

    scene.save(OUTPUT_DIR / "11-borderstyle-widths.svg")


def example_12_borderstyle_colors():
    """
    Show various border colors
    """
    scene = Scene.with_grid(cols=4, rows=2, cell_size=160)
    scene.background = "#ecf0f1"

    colors = ["#e74c3c", "#e67e22", "#f39c12", "#2ecc71", "#1abc9c", "#3498db", "#9b59b6", "#34495e"]

    cells = list(scene.grid)
    for i, color in enumerate(colors):
        if i < len(cells):
            style = BorderStyle(width=3, color=color, z_index=0)
            cells[i].add_border(style=style)

    scene.save(OUTPUT_DIR / "12-borderstyle-colors.svg")


# =============================================================================
# SECTION: Combined Styles
# =============================================================================

def example_13_combined_styles():
    """
    Demonstrate using multiple style objects together
    """
    scene = Scene.with_grid(cols=2, rows=2, cell_size=200)
    scene.background = "#f8f9fa"

    # Create styled boxes
    fill_style = FillStyle(color="#3498db", z_index=0)
    border_style = BorderStyle(width=2, color="#2c3e50", z_index=1)
    dot_style = DotStyle(radius=8, color="#e74c3c", z_index=2)

    for cell in scene.grid:
        # Fill
        cell.add_fill(style=fill_style)

        # Border
        cell.add_border(style=border_style)

        # Decorative dot
        cell.add_dot(style=dot_style)

        # Decorative line
        cell.add_line(start="left", end="right", width=3, color="#2ecc71")

    scene.save(OUTPUT_DIR / "13-combined-styles.svg")


def example_14_style_reusability():
    """
    Show how styles promote consistency and reusability
    """
    scene = Scene.with_grid(cols=8, rows=5, cell_size=100)
    scene.background = "#ffffff"

    # Define a consistent style palette
    primary_dot = DotStyle(radius=12, color="#3498db", z_index=2)
    secondary_dot = DotStyle(radius=8, color="#e74c3c", z_index=1)
    accent_dot = DotStyle(radius=5, color="#f39c12", z_index=0)

    grid_border = BorderStyle(width=1, color="#bdc3c7", z_index=0)

    # Create a consistent pattern using reusable styles
    cells = list(scene.grid)
    for i, cell in enumerate(cells):
        # Grid borders on all cells
        cell.add_border(style=grid_border)

        # Dots with consistent styles based on pattern
        if i % 3 == 0:
            cell.add_dot(style=primary_dot)
        elif i % 3 == 1:
            cell.add_dot(style=secondary_dot)
        else:
            cell.add_dot(style=accent_dot)

    scene.save(OUTPUT_DIR / "14-style-reusability.svg")


# =============================================================================
# SECTION: ShapeStyle
# =============================================================================

def example_15_shapestyle_basic():
    """
    Basic ShapeStyle usage with ellipses and polygons
    """
    scene = Scene.with_grid(cols=4, rows=2, cell_size=150)
    scene.background = "#f8f9fa"

    style = ShapeStyle(color="coral", stroke="navy", stroke_width=2, z_index=0)

    cells = list(scene.grid)

    # Row 1: Ellipses with same style
    for i in range(4):
        cells[i].add_ellipse(rx=40, ry=25, style=style)

    # Row 2: Polygons with same style
    for i in range(4, 8):
        cells[i].add_polygon(Polygon.hexagon(), style=style)

    scene.save(OUTPUT_DIR / "15-shapestyle-basic.svg")


def example_16_shapestyle_variations():
    """
    ShapeStyle builder methods for variations
    """
    scene = Scene.with_grid(cols=5, rows=2, cell_size=140)
    scene.background = "#ffffff"

    base = ShapeStyle(color="#3498db", stroke="#2c3e50", stroke_width=2, z_index=0)

    cells = list(scene.grid)

    # Row 1: Color variations on ellipses
    colors = ["#e74c3c", "#e67e22", "#f39c12", "#2ecc71", "#3498db"]
    for i, color in enumerate(colors):
        variant = base.with_color(color)
        cells[i].add_ellipse(rx=35, ry=25, style=variant)

    # Row 2: Stroke variations on polygons
    strokes = [None, "#e74c3c", "#2ecc71", "#3498db", "#9b59b6"]
    for i, stroke in enumerate(strokes):
        variant = base.with_stroke(stroke)
        cells[i + 5].add_polygon(Polygon.star(5), style=variant)

    scene.save(OUTPUT_DIR / "16-shapestyle-variations.svg")


# =============================================================================
# SECTION: TextStyle
# =============================================================================

def example_17_textstyle_basic():
    """
    Basic TextStyle usage
    """
    scene = Scene.with_grid(cols=3, rows=2, cell_size=200)
    scene.background = "#f8f9fa"

    style = TextStyle(font_size=14, color="navy", bold=True, z_index=0)

    cells = list(scene.grid)
    labels = ["Bold", "Style", "Text", "Easy", "Clean", "API"]
    for i, label in enumerate(labels):
        if i < len(cells):
            cells[i].add_fill(color="#e8f4f8")
            cells[i].add_border(color="#bdc3c7", width=1)
            cells[i].add_text(label, style=style)

    scene.save(OUTPUT_DIR / "17-textstyle-basic.svg")


def example_18_textstyle_variations():
    """
    TextStyle builder methods for variations
    """
    scene = Scene.with_grid(cols=4, rows=2, cell_size=180)
    scene.background = "#ffffff"

    base = TextStyle(font_size=14, color="#2c3e50", z_index=0)

    cells = list(scene.grid)

    # Row 1: Size variations
    sizes = [10, 14, 18, 22]
    for i, size in enumerate(sizes):
        variant = base.with_font_size(size)
        cells[i].add_text(f"{size}px", style=variant)
        cells[i].add_border(color="#ecf0f1", width=0.5)

    # Row 2: Style variations
    variants = [
        ("Normal", base),
        ("Bold", base.with_bold()),
        ("Italic", base.with_italic()),
        ("Red", base.with_color("#e74c3c")),
    ]
    for i, (label, variant) in enumerate(variants):
        cells[i + 4].add_text(label, style=variant)
        cells[i + 4].add_border(color="#ecf0f1", width=0.5)

    scene.save(OUTPUT_DIR / "18-textstyle-variations.svg")


# =============================================================================
# SECTION: ConnectionStyle
# =============================================================================

def example_19_connectionstyle_basic():
    """
    Basic ConnectionStyle usage
    """
    scene = Scene.with_grid(cols=4, rows=1, cell_size=150)
    scene.background = "#f8f9fa"

    cells = list(scene.grid)

    style = ConnectionStyle(width=2, color="#e74c3c", z_index=0)

    # Create dots and connect them
    dots = []
    for cell in cells:
        dot = cell.add_dot(radius=6, color="#3498db", z_index=2)
        dots.append(dot)

    for i in range(len(dots) - 1):
        conn = Connection(dots[i], dots[i + 1], style=style)
        scene.add(conn)

    scene.save(OUTPUT_DIR / "19-connectionstyle-basic.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # DotStyle
    "01-dotstyle-basic": example_01_dotstyle_basic,
    "02-dotstyle-builder-methods": example_02_dotstyle_builder_methods,
    "03-dotstyle-variations": example_03_dotstyle_variations,

    # LineStyle
    "04-linestyle-basic": example_04_linestyle_basic,
    "05-linestyle-cap-options": example_05_linestyle_cap_options,
    "06-linestyle-widths": example_06_linestyle_widths,

    # FillStyle
    "07-fillstyle-basic": example_07_fillstyle_basic,
    "08-fillstyle-opacity": example_08_fillstyle_opacity,
    "09-fillstyle-colors": example_09_fillstyle_colors,

    # BorderStyle
    "10-borderstyle-basic": example_10_borderstyle_basic,
    "11-borderstyle-widths": example_11_borderstyle_widths,
    "12-borderstyle-colors": example_12_borderstyle_colors,

    # Combined
    "13-combined-styles": example_13_combined_styles,
    "14-style-reusability": example_14_style_reusability,

    # ShapeStyle
    "15-shapestyle-basic": example_15_shapestyle_basic,
    "16-shapestyle-variations": example_16_shapestyle_variations,

    # TextStyle
    "17-textstyle-basic": example_17_textstyle_basic,
    "18-textstyle-variations": example_18_textstyle_variations,

    # ConnectionStyle
    "19-connectionstyle-basic": example_19_connectionstyle_basic,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-style-objects.md...")

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
            print("Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
