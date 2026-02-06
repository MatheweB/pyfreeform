#!/usr/bin/env python3
"""
SVG Generator for: entities/07-rectangles.md

Generates visual examples for rectangle entity documentation.
"""

from pyfreeform import Scene, Rect, shapes
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "07-rectangles"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_rects.png"
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
# SECTION: Fill vs Stroke
# =============================================================================

def fill_vs_stroke():
    """Rectangles with fill, stroke, and both"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "white"
    cells = list(scene.grid)

    # Fill only
    rect1 = Rect(cells[0].center.x, cells[0].center.y, 60, 40, fill="#3b82f6")
    rect1.cell = cells[0]
    cells[0]._entities.append(rect1)
    scene.add(rect1)

    # Stroke only
    rect2 = Rect(cells[1].center.x, cells[1].center.y, 60, 40, fill="none", stroke="#ef4444", stroke_width=2)
    rect2.cell = cells[1]
    cells[1]._entities.append(rect2)
    scene.add(rect2)

    # Both
    rect3 = Rect(cells[2].center.x, cells[2].center.y, 60, 40, fill="#d1fae5", stroke="#10b981", stroke_width=2)
    rect3.cell = cells[2]
    cells[2]._entities.append(rect3)
    scene.add(rect3)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_fill_vs_stroke.svg")


# =============================================================================
# SECTION: Checkerboard
# =============================================================================

def checkerboard():
    """Checkerboard pattern with filled cells"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color="#1f2937")
        else:
            cell.add_fill(color="#f3f4f6")

    scene.save(OUTPUT_DIR / "02_checkerboard.svg")


# =============================================================================
# SECTION: Grid Borders
# =============================================================================

def grid_borders():
    """Grid with visible borders"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        cell.add_border(color="#94a3b8", width=0.5)
        cell.add_dot(radius=3, color="#3b82f6")

    scene.save(OUTPUT_DIR / "03_grid_borders.svg")


# =============================================================================
# SECTION: Cell Backgrounds
# =============================================================================

def cell_backgrounds():
    """Fill cells with brightness-based colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        gray = int(cell.brightness * 255)
        cell.add_fill(color=f"rgb({gray},{gray},{gray})", z_index=0)
        cell.add_dot(radius=3, color="white", z_index=1)

    scene.save(OUTPUT_DIR / "04_cell_backgrounds.svg")


# =============================================================================
# SECTION: Highlight Border
# =============================================================================

def highlight_border():
    """Conditional borders on bright cells"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        gray = int(cell.brightness * 255)
        cell.add_fill(color=f"rgb({gray},{gray},{gray})", z_index=0)

        if cell.brightness > 0.7:
            cell.add_border(color="#fbbf24", width=2, z_index=10)
        else:
            cell.add_border(color="#334155", width=0.3, z_index=1)

    scene.save(OUTPUT_DIR / "05_highlight_border.svg")


# =============================================================================
# SECTION: Complete Example - Bordered Grid with Alternating Fills
# =============================================================================

def complete_example():
    """Bordered grid with alternating fills"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=30)
    scene.background = "#f8fafc"

    for cell in scene.grid:
        # Alternating fill pattern
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color="#e0e7ff", z_index=0)

        # Border on all cells
        cell.add_border(color="#94a3b8", width=0.5, z_index=1)

        # Highlight edge cells with accent border
        if (cell.row == 0 or cell.row == 9
                or cell.col == 0 or cell.col == 9):
            cell.add_border(color="#6366f1", width=2, z_index=2)

    scene.save(OUTPUT_DIR / "06_complete_example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_fill_vs_stroke": fill_vs_stroke,
    "02_checkerboard": checkerboard,
    "03_grid_borders": grid_borders,
    "04_cell_backgrounds": cell_backgrounds,
    "05_highlight_border": highlight_border,
    "06_complete_example": complete_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 07-rectangles.md...")
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
