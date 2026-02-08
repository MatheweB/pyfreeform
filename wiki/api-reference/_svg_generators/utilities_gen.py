#!/usr/bin/env python3
"""
SVG Generator for: api-reference/utilities.md

Generates visual examples demonstrating utility functions and helpers.
"""

from pyfreeform import Scene, Palette, Polygon
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "utilities"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Shape Helpers: Basic Shapes
# =============================================================================

def example1_basic_shapes():
    """Polygon.triangle(), Polygon.square(), Polygon.hexagon()"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Basic shapes
    cells[0].add_polygon(Polygon.triangle(size=0.8), fill=colors.primary)
    cells[1].add_polygon(Polygon.square(size=0.8), fill=colors.secondary)
    cells[2].add_polygon(Polygon.diamond(size=0.8), fill=colors.accent)
    cells[3].add_polygon(Polygon.hexagon(size=0.8), fill="#64ffda")

    scene.save(OUTPUT_DIR / "example1-basic-Polygon.svg")


# =============================================================================
# Shape Helpers: Star
# =============================================================================

def example2_stars():
    """Polygon.star() - Different point counts"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different star configurations
    cells[0].add_polygon(Polygon.star(4), fill=colors.primary)
    cells[1].add_polygon(Polygon.star(5), fill=colors.secondary)
    cells[2].add_polygon(Polygon.star(6), fill=colors.accent)
    cells[3].add_polygon(Polygon.star(8), fill="#ffd23f")

    scene.save(OUTPUT_DIR / "example2-stars.svg")


# =============================================================================
# Shape Helpers: Star Inner Radius
# =============================================================================

def example3_star_radius():
    """Polygon.star() - Different inner radius values"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different inner radius values
    cells[0].add_polygon(Polygon.star(5, inner_ratio=0.3), fill=colors.primary)
    cells[1].add_polygon(Polygon.star(5, inner_ratio=0.4), fill=colors.secondary)
    cells[2].add_polygon(Polygon.star(5, inner_ratio=0.5), fill=colors.accent)
    cells[3].add_polygon(Polygon.star(5, inner_ratio=0.6), fill="#64ffda")

    scene.save(OUTPUT_DIR / "example3-star-radius.svg")


# =============================================================================
# Shape Helpers: Regular Polygons
# =============================================================================

def example4_regular_polygons():
    """Polygon.regular_polygon() - Different side counts"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different regular polygons
    for i, n_sides in enumerate([3, 5, 6, 7, 8]):
        cells[i].add_polygon(Polygon.regular_polygon(n_sides), fill=colors.primary)

    scene.save(OUTPUT_DIR / "example4-regular-polygons.svg")


# =============================================================================
# Shape Helpers: Squircle
# =============================================================================

def example5_squircle():
    """Polygon.squircle() - Different n values"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different squircle values
    n_values = [2, 3, 4, 5, 6]
    for i, n in enumerate(n_values):
        cells[i].add_polygon(Polygon.squircle(size=0.8, n=n), fill=colors.accent)

    scene.save(OUTPUT_DIR / "example5-squircle.svg")


# =============================================================================
# Shape Helpers: Rounded Rectangle
# =============================================================================

def example6_rounded_rect():
    """Polygon.rounded_rect() - Different corner radius"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Different corner radius values
    cells[0].add_polygon(Polygon.rounded_rect(size=0.8, corner_radius=0.05), fill=colors.primary)
    cells[1].add_polygon(Polygon.rounded_rect(size=0.8, corner_radius=0.1), fill=colors.secondary)
    cells[2].add_polygon(Polygon.rounded_rect(size=0.8, corner_radius=0.2), fill=colors.accent)
    cells[3].add_polygon(Polygon.rounded_rect(size=0.8, corner_radius=0.3), fill="#ffd23f")

    scene.save(OUTPUT_DIR / "example6-rounded-rect.svg")


# =============================================================================
# Palettes: Different Color Schemes
# =============================================================================

def example7_palettes():
    """Palette system - Different color schemes"""
    palettes = [
        ("Midnight", Palette.midnight()),
        ("Ocean", Palette.ocean()),
        ("Sunset", Palette.sunset()),
        ("Forest", Palette.forest()),
    ]

    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")

    cells = list(scene.grid)

    for i, (name, palette) in enumerate(palettes):
        # Show primary, secondary, accent colors
        cells[i].add_fill(color=palette.background, z_index=0)
        cells[i].add_polygon(Polygon.hexagon(size=0.8), fill=palette.primary, z_index=5)
        cells[i].add_dot(radius=15, color=palette.accent, z_index=10)

    scene.save(OUTPUT_DIR / "example7-palettes.svg")


# =============================================================================
# Palette Properties
# =============================================================================

def example8_palette_properties():
    """Palette properties - primary, secondary, accent"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Show different palette colors
    cells[0].add_fill(color=colors.background)
    cells[1].add_fill(color=colors.primary)
    cells[2].add_fill(color=colors.secondary)
    cells[3].add_fill(color=colors.accent)
    cells[4].add_fill(color=colors.line)

    scene.save(OUTPUT_DIR / "example8-palette-properties.svg")


# =============================================================================
# Named Colors
# =============================================================================

def example9_named_colors():
    """CSS/SVG named colors"""
    scene = Scene.with_grid(cols=6, rows=1, cell_size=60, background="#1a1a2e")

    cells = list(scene.grid)
    named_colors = ["red", "blue", "green", "coral", "gold", "crimson"]

    for cell, color in zip(cells, named_colors):
        cell.add_dot(radius=20, color=color)

    scene.save(OUTPUT_DIR / "example9-named-colors.svg")


# =============================================================================
# Shape Size Parameter
# =============================================================================

def example10_shape_sizes():
    """Shape size parameter - controlling scale"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)
    sizes = [0.4, 0.5, 0.6, 0.7, 0.8]

    for cell, size in zip(cells, sizes):
        cell.add_polygon(Polygon.hexagon(size=size), fill=colors.primary)

    scene.save(OUTPUT_DIR / "example10-shape-sizes.svg")


# =============================================================================
# All Shapes Gallery
# =============================================================================

def example11_all_shapes():
    """Gallery of all available shapes"""
    scene = Scene.with_grid(cols=6, rows=2, cell_size=70, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Define shapes
    all_shapes = [
        Polygon.triangle(size=0.8),
        Polygon.square(size=0.8),
        Polygon.diamond(size=0.8),
        Polygon.hexagon(size=0.8),
        Polygon.star(5, size=0.8),
        Polygon.star(8, size=0.8),
        Polygon.regular_polygon(5, size=0.8),
        Polygon.regular_polygon(7, size=0.8),
        Polygon.squircle(size=0.8, n=4),
        Polygon.rounded_rect(size=0.8, corner_radius=0.2),
        Polygon.star(6, size=0.8, inner_ratio=0.5),
        Polygon.regular_polygon(9, size=0.8),
    ]

    # Add each shape
    for cell, shape in zip(cells, all_shapes):
        cell.add_polygon(shape, fill=colors.primary)

    scene.save(OUTPUT_DIR / "example11-all-Polygon.svg")


# =============================================================================
# Style Objects Example
# =============================================================================

def example12_style_objects():
    """Using style objects for consistent styling"""
    from pyfreeform.config import DotStyle, LineStyle

    scene = Scene.with_grid(cols=4, rows=2, cell_size=80, background="#1a1a2e")
    colors = Palette.midnight()

    # Define styles
    dot_style = DotStyle(radius=12, color=colors.primary)
    line_style = LineStyle(width=2, color=colors.secondary, cap="round")

    cells = list(scene.grid)

    # Apply same style to multiple elements
    for i in range(4):
        cells[i].add_dot(style=dot_style)

    for i in range(4, 8):
        cells[i].add_line(start="left", end="right", style=line_style)

    scene.save(OUTPUT_DIR / "example12-style-objects.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-basic-shapes": example1_basic_shapes,
    "example2-stars": example2_stars,
    "example3-star-radius": example3_star_radius,
    "example4-regular-polygons": example4_regular_polygons,
    "example5-squircle": example5_squircle,
    "example6-rounded-rect": example6_rounded_rect,
    "example7-palettes": example7_palettes,
    "example8-palette-properties": example8_palette_properties,
    "example9-named-colors": example9_named_colors,
    "example10-shape-sizes": example10_shape_sizes,
    "example11-all-shapes": example11_all_shapes,
    "example12-style-objects": example12_style_objects,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for utilities.md...")

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
