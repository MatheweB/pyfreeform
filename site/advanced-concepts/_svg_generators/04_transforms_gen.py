#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/04-transforms.md

Generates visual examples for entity transformations.

Corresponds to sections:
- Rotation
- Scaling
- Translation
- Method Chaining
- Examples
"""

from pyfreeform import Scene, shapes
from pyfreeform.core.point import Point
from pathlib import Path
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-transforms"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Rotation
# =============================================================================

def rotation_basic():
    """Basic rotation around entity center"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    angles = [0, 15, 30, 45]

    for i, angle in enumerate(angles):
        cell = scene.grid[0, i]

        from pyfreeform import Rect

        rect = Rect(cell.center.x - 20.0, cell.center.y - 12.5, 40, 25, fill="#3b82f6")

        rect.cell = cell

        cell._entities.append(rect)
        rect.rotate(angle)

        # Show center point
        cell.add_dot(at=rect.anchor("center"), radius=2, color="#ef4444", z_index=5)

        cell.add_text(f"{angle}°", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "01-rotation-basic.svg")

def rotation_progressive():
    """Progressive rotation angles"""
    scene = Scene.with_grid(cols=6, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    for i in range(6):
        angle = i * 30
        cell = scene.grid[0, i]

        poly = cell.add_polygon(shapes.hexagon( size=25), fill="#10b981")
        poly.rotate(angle)

        cell.add_text(f"{angle}°", at=(0.5, 0.85), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "02-rotation-progressive.svg")

def rotation_custom_origin():
    """Rotation around custom point"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Rotate around center (default)
    cell1 = scene.grid[0, 0]
    from pyfreeform import Rect
    rect1 = Rect(cell1.center.x - 20.0, cell1.center.y - 12.5, 40, 25, fill="#3b82f6")
    rect1.cell = cell1
    cell1._entities.append(rect1)
    rect1.rotate(30)
    cell1.add_dot(at=cell1.center, radius=3, color="#ef4444", z_index=5)
    cell1.add_text("Center origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Rotate around top-left
    cell2 = scene.grid[0, 1]
    from pyfreeform import Rect
    rect2 = Rect(cell2.center.x - 20.0, cell2.center.y - 12.5, 40, 25, fill="#3b82f6")
    rect2.cell = cell2
    cell2._entities.append(rect2)
    origin = rect2.anchor("top_left")
    cell2.add_dot(at=origin, radius=3, color="#ef4444", z_index=5)
    rect2.rotate(30, origin=origin)
    cell2.add_text("Top-left origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Rotate around bottom-right
    cell3 = scene.grid[0, 2]
    from pyfreeform import Rect
    rect3 = Rect(cell3.center.x - 20.0, cell3.center.y - 12.5, 40, 25, fill="#3b82f6")
    rect3.cell = cell3
    cell3._entities.append(rect3)
    origin3 = rect3.anchor("bottom_right")
    cell3.add_dot(at=origin3, radius=3, color="#ef4444", z_index=5)
    rect3.rotate(30, origin=origin3)
    cell3.add_text("Bottom-right origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "03-rotation-custom-origin.svg")

def rotation_full_circle():
    """Full rotation circle"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create rotated rectangles in circle
    for i in range(12):
        angle = i * 30
        from pyfreeform import Rect
        rect = Rect(cell.center.x - 15.0, cell.center.y - 5.0, 30, 10, fill="#3b82f6")
        rect.cell = cell
        cell._entities.append(rect)
        rect.rotate(angle)

    scene.save(OUTPUT_DIR / "04-rotation-full-circle.svg")

# =============================================================================
# SECTION: Scaling
# =============================================================================

def scaling_basic():
    """Basic uniform scaling"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    scales = [0.5, 0.75, 1.0, 1.5]

    for i, scale in enumerate(scales):
        cell = scene.grid[0, i]

        ellipse = cell.add_ellipse(rx=20, ry=15, fill="#10b981")
        ellipse.scale(scale)

        cell.add_text(f"{scale}x", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "05-scaling-basic.svg")

def scaling_progressive():
    """Progressive scaling"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create concentric scaled shapes
    scales = [0.3, 0.5, 0.7, 0.9, 1.1, 1.3]
    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]

    for scale, color in zip(scales, colors):
        poly = cell.add_polygon(shapes.hexagon( size=20), fill=color)
        poly.scale(scale)

    scene.save(OUTPUT_DIR / "06-scaling-progressive.svg")

def scaling_custom_origin():
    """Scaling from custom origin"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Scale from center (default)
    cell1 = scene.grid[0, 0]
    from pyfreeform import Rect
    rect1 = Rect(cell1.center.x - 15.0, cell1.center.y - 10.0, 30, 20, fill="#3b82f6")
    rect1.cell = cell1
    cell1._entities.append(rect1)
    from pyfreeform import Rect
    rect2 = Rect(cell1.center.x - 15.0, cell1.center.y - 10.0, 30, 20, fill="#3b82f6")
    rect2.cell = cell1
    cell1._entities.append(rect2)
    rect2.scale(1.5)
    cell1.add_dot(at=cell1.center, radius=2, color="#ef4444", z_index=5)
    cell1.add_text("Center origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Scale from top-left
    cell2 = scene.grid[0, 1]
    from pyfreeform import Rect
    rect3 = Rect(cell2.center.x - 15.0, cell2.center.y - 10.0, 30, 20, fill="#10b981")
    rect3.cell = cell2
    cell2._entities.append(rect3)
    origin = rect3.anchor("top_left")
    from pyfreeform import Rect
    rect4 = Rect(cell2.center.x - 15.0, cell2.center.y - 10.0, 30, 20, fill="#10b981")
    rect4.cell = cell2
    cell2._entities.append(rect4)
    rect4.scale(1.5, origin=origin)
    cell2.add_dot(at=origin, radius=2, color="#ef4444", z_index=5)
    cell2.add_text("Top-left origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Scale from bottom-right
    cell3 = scene.grid[0, 2]
    from pyfreeform import Rect
    rect5 = Rect(cell3.center.x - 15.0, cell3.center.y - 10.0, 30, 20, fill="#f59e0b")
    rect5.cell = cell3
    cell3._entities.append(rect5)
    origin3 = rect5.anchor("bottom_right")
    from pyfreeform import Rect
    rect6 = Rect(cell3.center.x - 15.0, cell3.center.y - 10.0, 30, 20, fill="#f59e0b")
    rect6.cell = cell3
    cell3._entities.append(rect6)
    rect6.scale(1.5, origin=origin3)
    cell3.add_dot(at=origin3, radius=2, color="#ef4444", z_index=5)
    cell3.add_text("Bottom-right origin", at=(0.5, 0.85), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "07-scaling-custom-origin.svg")

# =============================================================================
# SECTION: Translation
# =============================================================================

def translation_relative():
    """Relative movement with move_by"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    for i in range(5):
        cell = scene.grid[0, i]

        # Original position (faint)
        cell.add_dot(at=(0.3, 0.5), radius=5, color="#d1d5db")

        # Moved position
        dot = cell.add_dot(at=(0.3, 0.5), radius=5, color="#3b82f6")
        dx = i * 5
        dot.move_by(dx=dx, dy=0)

        cell.add_text(f"dx={dx}", at=(0.5, 0.8), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "08-translation-relative.svg")

def translation_absolute():
    """Absolute positioning with move_to"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    positions = [
        (0.2, 0.2),
        (0.8, 0.2),
        (0.2, 0.8),
        (0.8, 0.8),
    ]

    for i, (x, y) in enumerate(positions):
        cell = scene.grid[0, i]

        # Show original position
        cell.add_dot(color="#d1d5db", radius=4)

        # Move to new position (absolute positioning within cell)
        dot = cell.add_dot(color="#10b981", radius=5)
        dot.move_to(Point(cell.x + cell.width * x,
                          cell.y + cell.height * y))

        cell.add_text(f"({x}, {y})", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "09-translation-absolute.svg")

def translation_patterns():
    """Translation patterns"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a pattern of translated dots
    base_x, base_y = cell.center
    for row in range(5):
        for col in range(5):
            dot = cell.add_dot(radius=3, color="#3b82f6")
            dx = (col - 2) * 20
            dy = (row - 2) * 20
            dot.move_to(Point(base_x + dx, base_y + dy))

    scene.save(OUTPUT_DIR / "10-translation-patterns.svg")

# =============================================================================
# SECTION: Method Chaining
# =============================================================================

def chaining_basic():
    """Basic method chaining"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Just rotate
    cell1 = scene.grid[0, 0]
    from pyfreeform import Rect
    rect1 = Rect(cell1.center.x - 17.5, cell1.center.y - 10.0, 35, 20, fill="#3b82f6")
    rect1.cell = cell1
    cell1._entities.append(rect1)
    rect1.rotate(30)
    cell1.add_text("rotate(30)", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Rotate + scale
    cell2 = scene.grid[0, 1]
    from pyfreeform import Rect
    rect2 = Rect(cell2.center.x - 17.5, cell2.center.y - 10.0, 35, 20, fill="#10b981")
    rect2.cell = cell2
    cell2._entities.append(rect2)
    rect2.rotate(30).scale(1.3)
    cell2.add_text("rotate + scale", at=(0.5, 0.85), font_size=7, color="#1f2937")

    # Rotate + scale + translate
    cell3 = scene.grid[0, 2]
    from pyfreeform import Rect
    rect3 = Rect(cell3.center.x - 17.5, cell3.center.y - 10.0, 35, 20, fill="#f59e0b")
    rect3.cell = cell3
    cell3._entities.append(rect3)
    rect3.rotate(30).scale(1.3).move_by(0, 5)
    cell3.add_text("rotate + scale + move", at=(0.5, 0.85), font_size=6, color="#1f2937")

    # Complex chain
    cell4 = scene.grid[0, 3]
    from pyfreeform import Rect
    rect4 = Rect(cell4.center.x - 17.5, cell4.center.y - 10.0, 35, 20, fill="#ef4444")
    rect4.cell = cell4
    cell4._entities.append(rect4)
    rect4.scale(0.8).rotate(45).move_by(10, -5)
    cell4.add_text("scale + rotate + move", at=(0.5, 0.85), font_size=6, color="#1f2937")

    scene.save(OUTPUT_DIR / "11-chaining-basic.svg")

def chaining_complex():
    """Complex chaining example"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a pattern with chained transformations
    for i in range(8):
        angle = i * 45
        poly = cell.add_polygon(shapes.triangle( size=15), fill="#3b82f6")
        scale = 0.5 + i * 0.1
        poly.rotate(angle).scale(scale).move_by(0, -i * 3)

    scene.save(OUTPUT_DIR / "12-chaining-complex.svg")

# =============================================================================
# SECTION: Examples
# =============================================================================

def example_distance_based_rotation():
    """Distance-based rotation pattern"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5

        rotation = distance * 10

        poly = cell.add_polygon(shapes.hexagon( size=6), fill="#3b82f6")
        poly.rotate(rotation)

    scene.save(OUTPUT_DIR / "13-example-distance-based-rotation.svg")

def example_wave_rotation():
    """Wave-based rotation"""
    scene = Scene.with_grid(cols=20, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    for cell in scene.grid:
        angle = math.sin(cell.col / scene.grid.cols * math.pi * 4) * 45

        from pyfreeform import Rect

        rect = Rect(cell.center.x - 6.0, cell.center.y - 4.0, 12, 8, fill="#10b981")

        rect.cell = cell

        cell._entities.append(rect)
        rect.rotate(angle)

    scene.save(OUTPUT_DIR / "14-example-wave-rotation.svg")

def example_spiral_scale():
    """Spiral scaling pattern"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5
        max_dist = ((center_row ** 2) + (center_col ** 2)) ** 0.5

        scale = 0.3 + (1 - distance / max_dist) * 0.7

        ellipse = cell.add_ellipse(rx=6, ry=4, fill="#f59e0b")
        ellipse.scale(scale)

    scene.save(OUTPUT_DIR / "15-example-spiral-scale.svg")

def example_combined_transforms():
    """Combined rotation and scaling"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5
        max_dist = ((center_row ** 2) + (center_col ** 2)) ** 0.5

        rotation = distance * 15
        scale = 0.3 + (1 - distance / max_dist) * 0.7

        poly = cell.add_polygon(shapes.square( size=7), fill="#8b5cf6")
        poly.rotate(rotation).scale(scale)

    scene.save(OUTPUT_DIR / "16-example-combined-transforms.svg")

def example_transform_comparison():
    """Side-by-side transform comparison"""
    scene = Scene.with_grid(cols=3, rows=2, cell_size=80)
    scene.background = "#f8f9fa"

    # Original
    cell1 = scene.grid[0, 0]
    cell1.add_polygon(shapes.hexagon( size=25), fill="#3b82f6")
    cell1.add_text("Original", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Rotated
    cell2 = scene.grid[0, 1]
    poly2 = cell2.add_polygon(shapes.hexagon( size=25), fill="#10b981")
    poly2.rotate(45)
    cell2.add_text("Rotated", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Scaled
    cell3 = scene.grid[0, 2]
    poly3 = cell3.add_polygon(shapes.hexagon( size=25), fill="#f59e0b")
    poly3.scale(1.3)
    cell3.add_text("Scaled", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Rotated + Scaled
    cell4 = scene.grid[1, 0]
    poly4 = cell4.add_polygon(shapes.hexagon( size=25), fill="#ef4444")
    poly4.rotate(45).scale(1.3)
    cell4.add_text("Rotate + Scale", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Translated
    cell5 = scene.grid[1, 1]
    poly5 = cell5.add_polygon(shapes.hexagon( size=25), fill="#8b5cf6")
    poly5.move_by(dx=10, dy=-8)
    cell5.add_text("Translated", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # All combined
    cell6 = scene.grid[1, 2]
    poly6 = cell6.add_polygon(shapes.hexagon( size=25), fill="#ec4899")
    poly6.rotate(30).scale(1.2).move_by(dx=8, dy=-6)
    cell6.add_text("Combined", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "17-example-transform-comparison.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Rotation
    "01-rotation-basic": rotation_basic,
    "02-rotation-progressive": rotation_progressive,
    "03-rotation-custom-origin": rotation_custom_origin,
    "04-rotation-full-circle": rotation_full_circle,

    # Scaling
    "05-scaling-basic": scaling_basic,
    "06-scaling-progressive": scaling_progressive,
    "07-scaling-custom-origin": scaling_custom_origin,

    # Translation
    "08-translation-relative": translation_relative,
    "09-translation-absolute": translation_absolute,
    "10-translation-patterns": translation_patterns,

    # Method chaining
    "11-chaining-basic": chaining_basic,
    "12-chaining-complex": chaining_complex,

    # Examples
    "13-example-distance-based-rotation": example_distance_based_rotation,
    "14-example-wave-rotation": example_wave_rotation,
    "15-example-spiral-scale": example_spiral_scale,
    "16-example-combined-transforms": example_combined_transforms,
    "17-example-transform-comparison": example_transform_comparison,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-transforms.md...")

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
            print(f"Available: {', '.join(sorted(GENERATORS.keys()))}")
    else:
        generate_all()
