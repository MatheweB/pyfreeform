#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/05-fit-to-cell.md

Generates visual examples for the fit_to_cell functionality.

Corresponds to sections:
- What is fit_to_cell()?
- Usage
- Parameters
- Examples (Dynamic Sizing, Rotation-Aware)
- Works For All Entities
"""

from pyfreeform import Scene, shapes
from pathlib import Path

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "05-fit-to-cell"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: What is fit_to_cell()?
# =============================================================================

def what_is_fit_concept():
    """Concept of fit_to_cell"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Before: Large ellipse
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    ellipse1 = cell1.add_ellipse(rx=100, ry=60, fill="#ef4444")
    cell1.add_text("Before", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # After: Fitted ellipse
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    ellipse2 = cell2.add_ellipse(rx=100, ry=60, fill="#10b981")
    ellipse2.fit_to_cell(0.85)
    cell2.add_text("After fit_to_cell(0.85)", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "01-what-is-fit-concept.svg")

def what_is_fit_steps():
    """Steps of fit_to_cell process"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    # Step 1: Original entity
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    ellipse1 = cell1.add_ellipse(rx=60, ry=40, rotation=30, fill="#3b82f6")
    cell1.add_text("1. Original", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Step 2: Calculate bbox
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    ellipse2 = cell2.add_ellipse(rx=60, ry=40, rotation=30, fill="#3b82f6")
    # Draw bounding box concept (simplified)
    from pyfreeform import Rect
    bbox_rect = Rect(cell2.center.x - 37.5, cell2.center.y - 32.5, 75, 65, fill="#f59e0b")
    bbox_rect.cell = cell2
    cell2._entities.append(bbox_rect)
    cell2.add_text("2. Calc bbox", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Step 3: Scale to fit
    cell3 = scene.grid[0, 2]
    cell3.add_border(color="#d1d5db", width=1)
    ellipse3 = cell3.add_ellipse(rx=60, ry=40, rotation=30, fill="#3b82f6")
    ellipse3.fit_to_cell(0.85, recenter=False)
    cell3.add_text("3. Scale", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Step 4: Recenter
    cell4 = scene.grid[0, 3]
    cell4.add_border(color="#d1d5db", width=1)
    ellipse4 = cell4.add_ellipse(rx=60, ry=40, rotation=30, fill="#10b981")
    ellipse4.fit_to_cell(0.85)
    cell4.add_text("4. Center", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "02-what-is-fit-steps.svg")

# =============================================================================
# SECTION: Usage
# =============================================================================

def usage_basic():
    """Basic usage of fit_to_cell"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Without fit
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    ellipse1 = cell1.add_ellipse(rx=100, ry=60, rotation=45, fill="#ef4444")
    cell1.add_text("No fit (overflows)", at=(0.5, 0.9), font_size=6, color="#1f2937")

    # With fit (default scale)
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    ellipse2 = cell2.add_ellipse(rx=100, ry=60, rotation=45, fill="#10b981")
    ellipse2.fit_to_cell()
    cell2.add_text("fit_to_cell()", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # With fit (custom scale)
    cell3 = scene.grid[0, 2]
    cell3.add_border(color="#d1d5db", width=1)
    ellipse3 = cell3.add_ellipse(rx=100, ry=60, rotation=45, fill="#3b82f6")
    ellipse3.fit_to_cell(0.85)
    cell3.add_text("fit_to_cell(0.85)", at=(0.5, 0.9), font_size=6, color="#1f2937")

    scene.save(OUTPUT_DIR / "03-usage-basic.svg")

def usage_different_shapes():
    """fit_to_cell with different shapes"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    # Ellipse
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    ellipse = cell1.add_ellipse(rx=80, ry=50, rotation=30, fill="#3b82f6")
    ellipse.fit_to_cell(0.85)
    cell1.add_text("Ellipse", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Rectangle
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    from pyfreeform import Rect
    rect = Rect(cell2.center.x - 50, cell2.center.y - 30, 100, 60, fill="#10b981")
    rect.cell = cell2
    cell2._entities.append(rect)
    scene.add(rect)
    rect.fit_to_cell(0.85)
    cell2.add_text("Rectangle", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Polygon
    cell3 = scene.grid[0, 2]
    cell3.add_border(color="#d1d5db", width=1)
    poly = cell3.add_polygon(shapes.hexagon( size=60), rotation=15, fill="#f59e0b")
    poly.fit_to_cell(0.85)
    cell3.add_text("Polygon", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Star
    cell4 = scene.grid[0, 3]
    cell4.add_border(color="#d1d5db", width=1)
    star = cell4.add_polygon(shapes.star(5, size=60), rotation=18, fill="#ef4444")
    star.fit_to_cell(0.85)
    cell4.add_text("Star", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "04-usage-different-shapes.svg")

# =============================================================================
# SECTION: Parameters
# =============================================================================

def parameters_scale():
    """Scale parameter variations"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    scales = [0.5, 0.65, 0.8, 0.9, 1.0]

    for i, scale in enumerate(scales):
        cell = scene.grid[0, i]
        cell.add_border(color="#d1d5db", width=1)

        ellipse = cell.add_ellipse(rx=80, ry=50, rotation=45, fill="#3b82f6")
        ellipse.fit_to_cell(scale)

        cell.add_text(f"{scale}", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "05-parameters-scale.svg")

def parameters_recenter():
    """Recenter parameter comparison"""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Without recenter
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    # Create off-center ellipse
    ellipse1 = cell1.add_ellipse(rx=80, ry=50, rotation=30, fill="#ef4444")
    ellipse1.move_by(dx=-10, dy=-10)
    ellipse1.fit_to_cell(0.8, recenter=False)
    cell1.add_text("recenter=False", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # With recenter
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    ellipse2 = cell2.add_ellipse(rx=80, ry=50, rotation=30, fill="#10b981")
    ellipse2.move_by(dx=-10, dy=-10)
    ellipse2.fit_to_cell(0.8, recenter=True)
    cell2.add_text("recenter=True", at=(0.5, 0.9), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "06-parameters-recenter.svg")

# =============================================================================
# SECTION: Examples - Dynamic Sizing
# =============================================================================

def example_brightness_based():
    """Size based on brightness"""
    from PIL import Image, ImageDraw
    import tempfile
    from pathlib import Path

    # Create test image with brightness variation
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_fit_brightness.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            t = ((x - 200)**2 + (y - 200)**2) ** 0.5 / 282.8
            val = int(50 + t * 205)
            draw.point((x, y), fill=(val, val, val))

    img.save(temp_file)

    scene = Scene.from_image(temp_file, grid_size=40)

    for cell in scene.grid:
        # Size based on brightness
        target_scale = 0.3 + cell.brightness * 0.7

        ellipse = cell.add_ellipse(rx=100, ry=60, rotation=45, fill="#3b82f6")
        ellipse.fit_to_cell(target_scale)

    scene.save(OUTPUT_DIR / "07-example-brightness-based.svg")

def example_position_based():
    """Size based on position"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5
        max_dist = ((center_row ** 2) + (center_col ** 2)) ** 0.5

        # Size inversely proportional to distance
        target_scale = 0.3 + (1 - distance / max_dist) * 0.7

        poly = cell.add_polygon(shapes.hexagon( size=40), fill="#10b981")
        poly.fit_to_cell(target_scale)

    scene.save(OUTPUT_DIR / "08-example-position-based.svg")

def example_pattern_based():
    """Size based on pattern"""
    scene = Scene.with_grid(cols=20, rows=10, cell_size=20)
    scene.background = "#f8f9fa"

    import math

    for cell in scene.grid:
        # Wave pattern
        wave = math.sin(cell.col / scene.grid.cols * math.pi * 4)
        target_scale = 0.3 + (wave + 1) / 2 * 0.7

        ellipse = cell.add_ellipse(rx=50, ry=30, fill="#f59e0b")
        ellipse.fit_to_cell(target_scale)

    scene.save(OUTPUT_DIR / "09-example-pattern-based.svg")

# =============================================================================
# SECTION: Examples - Rotation-Aware
# =============================================================================

def example_rotation_awareness():
    """Rotated ellipses still fit perfectly"""
    scene = Scene.with_grid(cols=6, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    for i in range(6):
        rotation = i * 30
        cell = scene.grid[0, i]
        cell.add_border(color="#d1d5db", width=1)

        ellipse = cell.add_ellipse(rx=60, ry=30, rotation=rotation, fill="#8b5cf6")
        ellipse.fit_to_cell(0.8)

        cell.add_text(f"{rotation}°", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "10-example-rotation-awareness.svg")

def example_combined_rotation_sizing():
    """Combined rotation and dynamic sizing"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=16)
    scene.background = "#f8f9fa"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5
        max_dist = ((center_row ** 2) + (center_col ** 2)) ** 0.5

        # Rotation based on distance
        rotation = distance * 15

        # Size inversely proportional to distance
        target_scale = 0.3 + (1 - distance / max_dist) * 0.7

        ellipse = cell.add_ellipse(rx=40, ry=20, rotation=rotation, fill="#ec4899")
        ellipse.fit_to_cell(target_scale)

    scene.save(OUTPUT_DIR / "11-example-combined-rotation-sizing.svg")

def example_rotation_grid():
    """Grid of rotated fitted shapes"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=24)
    scene.background = "#f8f9fa"

    for cell in scene.grid:
        rotation = (cell.row + cell.col) * 15

        ellipse = cell.add_ellipse(rx=50, ry=30, rotation=rotation, fill="#3b82f6")
        ellipse.fit_to_cell(0.8)

    scene.save(OUTPUT_DIR / "12-example-rotation-grid.svg")

# =============================================================================
# SECTION: Works For All Entities
# =============================================================================

def works_for_all_comparison():
    """fit_to_cell works for all entity types"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "#f8f9fa"

    # Dot
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#d1d5db", width=1)
    dot = cell1.add_dot(radius=60, color="#ef4444")
    dot.fit_to_cell(0.8)
    cell1.add_text("Dot", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Ellipse
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#d1d5db", width=1)
    ellipse = cell2.add_ellipse(rx=80, ry=50, rotation=30, fill="#3b82f6")
    ellipse.fit_to_cell(0.8)
    cell2.add_text("Ellipse", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Rectangle
    cell3 = scene.grid[0, 2]
    cell3.add_border(color="#d1d5db", width=1)
    from pyfreeform import Rect
    rect = Rect(cell3.center.x - 50, cell3.center.y - 35, 100, 70, fill="#10b981")
    rect.cell = cell3
    cell3._entities.append(rect)
    scene.add(rect)
    rect.fit_to_cell(0.8)
    cell3.add_text("Rectangle", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Polygon
    cell4 = scene.grid[0, 3]
    cell4.add_border(color="#d1d5db", width=1)
    poly = cell4.add_polygon(shapes.star(5, size=80), rotation=18, fill="#f59e0b")
    poly.fit_to_cell(0.8)
    cell4.add_text("Polygon", at=(0.5, 0.9), font_size=7, color="#1f2937")

    # Text
    cell5 = scene.grid[0, 4]
    cell5.add_border(color="#d1d5db", width=1)
    text = cell5.add_text("ABC", font_size=60, color="#8b5cf6")
    text.fit_to_cell(0.8)
    cell5.add_text("Text", at=(0.5, 0.9), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "13-works-for-all-comparison.svg")

def works_for_all_complex():
    """Complex shapes with fit_to_cell"""
    scene = Scene.with_grid(cols=4, rows=2, cell_size=80)
    scene.background = "#f8f9fa"

    shape_data = [
        (shapes.triangle(), "Triangle"),
        (shapes.square(), "Square"),
        (shapes.regular_polygon(sides=5), "Pentagon"),
        (shapes.hexagon(), "Hexagon"),
        (shapes.star(5), "Star 5"),
        (shapes.star(6), "Star 6"),
        (shapes.star(8), "Star 8"),
        (shapes.diamond(), "Diamond"),
    ]

    for i, (shape, name) in enumerate(shape_data):
        row = i // 4
        col = i % 4
        cell = scene.grid[row, col]
        cell.add_border(color="#d1d5db", width=1)

        rotation = (row * 4 + col) * 20
        poly = cell.add_polygon(shape, rotation=rotation, fill="#3b82f6")
        poly.fit_to_cell(0.8)

        cell.add_text(name, at=(0.5, 0.9), font_size=6, color="#1f2937")

    scene.save(OUTPUT_DIR / "14-works-for-all-complex.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # What is fit_to_cell?
    "01-what-is-fit-concept": what_is_fit_concept,
    "02-what-is-fit-steps": what_is_fit_steps,

    # Usage
    "03-usage-basic": usage_basic,
    "04-usage-different-shapes": usage_different_shapes,

    # Parameters
    "05-parameters-scale": parameters_scale,
    "06-parameters-recenter": parameters_recenter,

    # Dynamic sizing examples
    "07-example-brightness-based": example_brightness_based,
    "08-example-position-based": example_position_based,
    "09-example-pattern-based": example_pattern_based,

    # Rotation-aware examples
    "10-example-rotation-awareness": example_rotation_awareness,
    "11-example-combined-rotation-sizing": example_combined_rotation_sizing,
    "12-example-rotation-grid": example_rotation_grid,

    # Works for all entities
    "13-works-for-all-comparison": works_for_all_comparison,
    "14-works-for-all-complex": works_for_all_complex,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 05-fit-to-cell.md...")

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
