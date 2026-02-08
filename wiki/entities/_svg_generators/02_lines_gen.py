#!/usr/bin/env python3
"""
SVG Generator for: entities/02-lines.md

Generates visual examples for line entity documentation.
"""

from pyfreeform import Scene, Line
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-lines"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_lines.png"
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
# SECTION: Line Directions
# =============================================================================

def line_directions():
    """Different line directions and orientations"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=80)
    scene.background = "white"
    cells = list(scene.grid)

    # Horizontal
    cells[0].add_line(start="left", end="right", width=2, color="#3b82f6")
    # Vertical
    cells[1].add_line(start="top", end="bottom", width=2, color="#ef4444")
    # Diagonal (top-left to bottom-right)
    cells[2].add_diagonal(start="top_left", end="bottom_right", width=2, color="#10b981")
    # Diagonal (bottom-left to top-right)
    cells[3].add_diagonal(start="bottom_left", end="top_right", width=2, color="#f59e0b")

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_line_directions.svg")


# =============================================================================
# SECTION: Parametric Positioning
# =============================================================================

def parametric_positioning():
    """Dots positioned along a line parametrically"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "white"
    cell = list(scene.grid)[0]

    line = cell.add_line(start="left", end="right", width=2, color="#94a3b8")

    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"]
    for i, t_val in enumerate([0.0, 0.25, 0.5, 0.75, 1.0]):
        cell.add_dot(along=line, t=t_val, radius=8, color=colors[i])

    cell.add_border(color="#e0e0e0", width=0.5)
    scene.save(OUTPUT_DIR / "02_parametric_positioning.svg")


# =============================================================================
# SECTION: Grid Lines
# =============================================================================

def grid_lines():
    """Grid with border lines"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "03_grid_lines.svg")


# =============================================================================
# SECTION: Diagonal with Sliding Dots
# =============================================================================

def diagonal_dots():
    """Diagonal lines with dots positioned by brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        line = cell.add_diagonal(
            start="bottom_left", end="top_right", width=1, color="#94a3b8"
        )

        # Dot position driven by brightness
        cell.add_dot(
            along=line,
            t=cell.brightness,
            radius=4,
            color="#ef4444",
        )

    scene.save(OUTPUT_DIR / "04_diagonal_dots.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_line_directions": line_directions,
    "02_parametric_positioning": parametric_positioning,
    "03_grid_lines": grid_lines,
    "04_diagonal_dots": diagonal_dots,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-lines.md...")
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
