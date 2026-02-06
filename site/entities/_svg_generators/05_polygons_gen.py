#!/usr/bin/env python3
"""
SVG Generator for: entities/05-polygons.md

Generates visual examples for polygon entity documentation.
"""

from pyfreeform import Scene, shapes
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "05-polygons"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_polygons.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)
    for y in range(400):
        for x in range(400):
            brightness = int(255 * (1 - ((x + y) / 800)))
            draw.point((x, y), fill=(brightness, brightness, brightness))
    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_image()


# =============================================================================
# SECTION: Shape Gallery
# =============================================================================

def shape_gallery():
    """Gallery of all built-in polygon shapes"""
    scene = Scene.with_grid(cols=8, rows=1, cell_size=70)
    scene.background = "white"
    cells = list(scene.grid)

    shape_data = [
        (shapes.triangle(), "#ef4444"),
        (shapes.square(), "#f59e0b"),
        (shapes.diamond(), "#10b981"),
        (shapes.regular_polygon(sides=5), "#3b82f6"),
        (shapes.hexagon(), "#8b5cf6"),
        (shapes.star(points=5), "#ec4899"),
        (shapes.squircle(), "#14b8a6"),
        (shapes.rounded_rect(), "#f97316"),
    ]

    for i, (verts, color) in enumerate(shape_data):
        cells[i].add_polygon(verts, fill=color)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_shape_gallery.svg")


# =============================================================================
# SECTION: Rotating Shapes
# =============================================================================

def rotating_shapes():
    """Hexagons rotated based on position"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        rotation = (cell.row + cell.col) * 15
        poly = cell.add_polygon(shapes.hexagon(size=0.7), fill="#8b5cf6")
        poly.rotate(rotation)

    scene.save(OUTPUT_DIR / "02_rotating_shapes.svg")


# =============================================================================
# SECTION: Squircle Variations
# =============================================================================

def squircle_variations():
    """Squircles with different n values"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "white"
    cells = list(scene.grid)

    n_values = [2, 3, 4, 6, 10]
    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"]

    for i, (n, color) in enumerate(zip(n_values, colors)):
        cells[i].add_polygon(shapes.squircle(n=n), fill=color)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "03_squircle_variations.svg")


# =============================================================================
# SECTION: Conditional Shapes
# =============================================================================

def conditional_shapes():
    """Brightness-based shape selection: triangle vs square vs pentagon"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_polygon(shapes.regular_polygon(sides=5, size=0.7), fill="#fbbf24")
        elif cell.brightness > 0.4:
            cell.add_polygon(shapes.square(size=0.6), fill="#94a3b8")
        else:
            cell.add_polygon(shapes.triangle(size=0.6), fill="#78716c")

    scene.save(OUTPUT_DIR / "04_conditional_shapes.svg")


# =============================================================================
# SECTION: Custom Star Burst
# =============================================================================

def custom_star_burst():
    """Star shapes with varying parameters across the grid"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=40)
    scene.background = "white"

    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]

    for cell in scene.grid:
        points = 4 + (cell.col % 5)  # 4 to 8 points
        inner = 0.2 + (cell.row / 10.0)  # 0.2 to 0.9
        color_idx = (cell.row + cell.col) % len(colors)

        cell.add_polygon(
            shapes.star(points=points, inner_ratio=min(inner, 0.6)),
            fill=colors[color_idx],
        )

    scene.save(OUTPUT_DIR / "05_custom_star_burst.svg")


# =============================================================================
# SECTION: Complete Example - Radial Pattern
# =============================================================================

def complete_example():
    """Radial pattern with distance-based shapes"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
    scene.background = "#1e1b4b"

    center_col = 7.0
    center_row = 7.0

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = (dx * dx + dy * dy) ** 0.5

        # Choose shape by distance from center
        if distance < 3:
            shape_verts = shapes.squircle(n=4, size=0.8)
            color = "#a78bfa"
        elif distance < 5.5:
            shape_verts = shapes.hexagon(size=0.7)
            color = "#818cf8"
        else:
            shape_verts = shapes.triangle(size=0.6)
            color = "#6366f1"

        poly = cell.add_polygon(shape_verts, fill=color)

        # Rotate based on angle from center
        if distance > 0:
            angle = math.degrees(math.atan2(dy, dx))
            poly.rotate(angle)

    scene.save(OUTPUT_DIR / "06_complete_example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_shape_gallery": shape_gallery,
    "02_rotating_shapes": rotating_shapes,
    "03_squircle_variations": squircle_variations,
    "04_conditional_shapes": conditional_shapes,
    "05_custom_star_burst": custom_star_burst,
    "06_complete_example": complete_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 05-polygons.md...")
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
