#!/usr/bin/env python3
"""
SVG Generator for: api-reference/transforms.md

Generates visual examples demonstrating polygon transformation methods.
"""

from pyfreeform import Scene, Palette, shapes
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "transforms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# rotate() - Basic Rotation
# =============================================================================

def example1_rotate_basic():
    """polygon.rotate() - Basic rotation"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Same shape, different rotations
    angles = [0, 30, 60, 90]
    for cell, angle in zip(cells, angles):
        poly = cell.add_polygon(shapes.triangle(size=0.8), fill=colors.primary)
        poly.rotate(angle)

    scene.save(OUTPUT_DIR / "example1-rotate-basic.svg")


# =============================================================================
# rotate() - Around Different Origins
# =============================================================================

def example2_rotate_origin():
    """polygon.rotate(origin=...) - Rotate around different points"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Rotate around center (default)
    poly1 = cells[0].add_polygon(shapes.hexagon(size=0.7), fill=colors.primary)
    poly1.rotate(45)

    # Rotate around top_left
    poly2 = cells[1].add_polygon(shapes.hexagon(size=0.7), fill=colors.secondary)
    poly2.rotate(45, origin=cells[1].top_left)

    # Rotate around custom point
    poly3 = cells[2].add_polygon(shapes.hexagon(size=0.7), fill=colors.accent)
    poly3.rotate(45, origin=cells[2].bottom_right)

    scene.save(OUTPUT_DIR / "example2-rotate-origin.svg")


# =============================================================================
# scale() - Basic Scaling
# =============================================================================

def example3_scale_basic():
    """polygon.scale() - Scale polygons"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different scale factors
    scale_factors = [0.5, 0.7, 0.9, 1.1]
    for cell, factor in zip(cells, scale_factors):
        poly = cell.add_polygon(shapes.star(5), fill=colors.accent)
        poly.scale(factor)

    scene.save(OUTPUT_DIR / "example3-scale-basic.svg")


# =============================================================================
# scale() - Around Different Origins
# =============================================================================

def example4_scale_origin():
    """polygon.scale(origin=...) - Scale from different origins"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Scale from center (default)
    poly1 = cells[0].add_polygon(shapes.square(size=0.5), fill=colors.primary)
    poly1.scale(1.5)

    # Scale from top_left
    poly2 = cells[1].add_polygon(shapes.square(size=0.5), fill=colors.secondary)
    poly2.scale(1.5, origin=cells[1].top_left)

    # Scale from bottom_right
    poly3 = cells[2].add_polygon(shapes.square(size=0.5), fill=colors.accent)
    poly3.scale(1.5, origin=cells[2].bottom_right)

    scene.save(OUTPUT_DIR / "example4-scale-origin.svg")


# =============================================================================
# translate() - Basic Translation
# =============================================================================

def example5_translate():
    """polygon.translate() - Move polygons"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Different translations
    cells[0].add_polygon(shapes.hexagon(size=0.6), fill=colors.primary)  # No translation

    poly2 = cells[1].add_polygon(shapes.hexagon(size=0.6), fill=colors.secondary)
    poly2.translate(dx=15, dy=0)  # Right

    poly3 = cells[2].add_polygon(shapes.hexagon(size=0.6), fill=colors.accent)
    poly3.translate(dx=0, dy=15)  # Down

    poly4 = cells[3].add_polygon(shapes.hexagon(size=0.6), fill="#64ffda")
    poly4.translate(dx=10, dy=10)  # Diagonal

    scene.save(OUTPUT_DIR / "example5-translate.svg")


# =============================================================================
# Combining Transforms
# =============================================================================

def example6_combined():
    """Combine multiple transforms"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100, background="#1a1a2e")
    colors = Palette.midnight()

    cells = list(scene.grid)

    # Original
    cells[0].add_polygon(shapes.star(5), fill=colors.primary)

    # Rotate only
    poly2 = cells[1].add_polygon(shapes.star(5), fill=colors.secondary)
    poly2.rotate(45)

    # Scale only
    poly3 = cells[2].add_polygon(shapes.star(5), fill=colors.accent)
    poly3.scale(1.3)

    # Rotate + Scale
    poly4 = cells[3].add_polygon(shapes.star(5), fill="#ffd23f")
    poly4.rotate(45)
    poly4.scale(1.3)

    scene.save(OUTPUT_DIR / "example6-combined.svg")


# =============================================================================
# Position-Based Rotation Pattern
# =============================================================================

def example7_position_rotation():
    """Rotation based on grid position"""
    scene = Scene.with_grid(cols=8, rows=6, cell_size=50, background="#1a1a2e")
    colors = Palette.ocean()

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.triangle(size=0.8), fill=colors.primary)

        # Rotate based on position
        angle = (cell.row + cell.col) * 15
        poly.rotate(angle)

    scene.save(OUTPUT_DIR / "example7-position-rotation.svg")


# =============================================================================
# Radial Rotation Pattern
# =============================================================================

def example8_radial_rotation():
    """Shapes pointing toward center"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.triangle(size=0.7), fill=colors.primary)

        # Calculate angle toward center
        dr = cell.row - center_row
        dc = cell.col - center_col
        angle = math.degrees(math.atan2(dr, dc))

        poly.rotate(angle + 90)  # +90 to point upward initially

    scene.save(OUTPUT_DIR / "example8-radial-rotation.svg")


# =============================================================================
# Brightness-Based Scaling
# =============================================================================

def example9_brightness_scaling():
    """Scale based on distance from center"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=40, background="#1a1a2e")
    colors = Palette.ocean()

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        # Calculate distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = (dr*dr + dc*dc) ** 0.5

        # Scale based on distance (larger near center)
        max_distance = 7
        if distance < max_distance:
            scale_factor = 0.5 + (max_distance - distance) * 0.1
            poly = cell.add_polygon(shapes.hexagon(size=0.8), fill=colors.accent)
            poly.scale(scale_factor)

    scene.save(OUTPUT_DIR / "example9-brightness-scaling.svg")


# =============================================================================
# Complex Transform Pattern
# =============================================================================

def example10_complex():
    """Complex pattern with rotation and scaling"""
    scene = Scene.with_grid(cols=12, rows=9, cell_size=40, background="#1a1a2e")
    colors = Palette.midnight()

    for cell in scene.grid:
        # Alternate shapes
        if (cell.row + cell.col) % 2 == 0:
            poly = cell.add_polygon(shapes.star(5, inner_ratio=0.4), fill=colors.primary)
        else:
            poly = cell.add_polygon(shapes.hexagon(size=0.7), fill=colors.secondary)

        # Rotate based on position
        angle = (cell.row * 10 + cell.col * 15) % 360
        poly.rotate(angle)

        # Scale based on row
        scale = 0.6 + (cell.row / scene.grid.rows) * 0.4
        poly.scale(scale)

    scene.save(OUTPUT_DIR / "example10-complex.svg")


# =============================================================================
# Transform Order Matters
# =============================================================================

def example11_order_matters():
    """Demonstrate that transform order affects results"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=150, background="#1a1a2e")
    colors = Palette.ocean()

    cells = list(scene.grid)

    # Scale then rotate
    poly1 = cells[0].add_polygon(shapes.triangle(size=0.6), fill=colors.primary)
    poly1.scale(1.5)
    poly1.rotate(45)

    # Rotate then scale
    poly2 = cells[1].add_polygon(shapes.triangle(size=0.6), fill=colors.secondary)
    poly2.rotate(45)
    poly2.scale(1.5)

    scene.save(OUTPUT_DIR / "example11-order-matters.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example1-rotate-basic": example1_rotate_basic,
    "example2-rotate-origin": example2_rotate_origin,
    "example3-scale-basic": example3_scale_basic,
    "example4-scale-origin": example4_scale_origin,
    "example5-translate": example5_translate,
    "example6-combined": example6_combined,
    "example7-position-rotation": example7_position_rotation,
    "example8-radial-rotation": example8_radial_rotation,
    "example9-brightness-scaling": example9_brightness_scaling,
    "example10-complex": example10_complex,
    "example11-order-matters": example11_order_matters,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for transforms.md...")

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
