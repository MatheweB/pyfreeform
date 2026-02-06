#!/usr/bin/env python3
"""
SVG Generator for: entities/01-dots.md

Generates visual examples for dot entity documentation.
"""

from pyfreeform import Scene, Dot, shapes
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-dots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_dots.png"
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
# SECTION: Varying Sizes
# =============================================================================

def varying_sizes():
    """Dots of different sizes"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60)
    scene.background = "white"
    cells = list(scene.grid)

    sizes = [3, 6, 10, 15, 20]
    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"]
    for i, (size, color) in enumerate(zip(sizes, colors)):
        cells[i].add_dot(radius=size, color=color)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_varying_sizes.svg")


# =============================================================================
# SECTION: Positioning
# =============================================================================

def positioning():
    """Dot positioning methods"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=100)
    scene.background = "white"
    cells = list(scene.grid)

    # Named position
    cells[0].add_dot(at="top_left", radius=5, color="#3b82f6")
    cells[0].add_dot(at="center", radius=5, color="#ef4444")
    cells[0].add_dot(at="bottom_right", radius=5, color="#10b981")

    # Relative position
    cells[1].add_dot(at=(0.25, 0.25), radius=5, color="#f59e0b")
    cells[1].add_dot(at=(0.75, 0.25), radius=5, color="#8b5cf6")
    cells[1].add_dot(at=(0.5, 0.75), radius=5, color="#ec4899")

    # Along a path
    line = cells[2].add_line(start="left", end="right", width=1, color="#94a3b8")
    cells[2].add_dot(along=line, t=0.0, radius=4, color="#3b82f6")
    cells[2].add_dot(along=line, t=0.5, radius=4, color="#ef4444")
    cells[2].add_dot(along=line, t=1.0, radius=4, color="#10b981")

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "02_positioning.svg")


# =============================================================================
# SECTION: Basic Grid Pattern
# =============================================================================

def grid_pattern():
    """Basic dot grid from image colors"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "02_grid_pattern.svg")


# =============================================================================
# SECTION: Brightness Sizing
# =============================================================================

def brightness_sized():
    """Dots sized by brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        size = 2 + cell.brightness * 8
        cell.add_dot(radius=size, color=cell.color)

    scene.save(OUTPUT_DIR / "03_brightness_sized.svg")


# =============================================================================
# SECTION: Layering
# =============================================================================

def layering():
    """Z-index layering with dots"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=150)
    scene.background = "white"
    cell = list(scene.grid)[0]

    # Three overlapping dots
    cell.add_dot(at=(0.35, 0.5), radius=25, color="#3b82f6", z_index=0)
    cell.add_dot(at=(0.5, 0.5), radius=25, color="#ef4444", z_index=1)
    cell.add_dot(at=(0.65, 0.5), radius=25, color="#10b981", z_index=2)

    cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "03_layering.svg")


def advanced_layering():
    """Advanced layering example"""
    scene = Scene.with_grid(cols=5, rows=5, cell_size=40)
    scene.background = "white"

    for cell in scene.grid:
        # Background circle
        cell.add_dot(radius=15, color="#e0e7ff", z_index=0)
        # Foreground smaller dot
        cell.add_dot(radius=6, color="#3b82f6", z_index=1)

    scene.save(OUTPUT_DIR / "04_layering.svg")


# =============================================================================
# SECTION: Radial Grid Pattern
# =============================================================================

def radial_grid_pattern():
    """Grid with radial size variation"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=20)
    scene.background = "#1a1a2e"

    center_row = 7
    center_col = 7

    for cell in scene.grid:
        dx = cell.col - center_col
        dy = cell.row - center_row
        distance = math.sqrt(dx * dx + dy * dy)
        max_dist = math.sqrt(center_row ** 2 + center_col ** 2)

        radius = 8 * (1 - distance / max_dist)
        if radius > 1:
            cell.add_dot(radius=radius, color="#8b5cf6")

    scene.save(OUTPUT_DIR / "05_grid_pattern.svg")


# =============================================================================
# SECTION: Multi-Color Composition
# =============================================================================

def multicolor_composition():
    """Multi-color dots with brightness thresholds (Example 2)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = {
        "background": "#1a1a2e",
        "primary": "#ff6b6b",
        "secondary": "#4ecdc4",
        "accent": "#ffe66d",
    }
    scene.background = colors["background"]

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(radius=6, color=colors["primary"])
        elif cell.brightness > 0.4:
            cell.add_dot(radius=4, color=colors["secondary"])
        elif cell.brightness > 0.2:
            cell.add_dot(radius=2, color=colors["accent"])

    scene.save(OUTPUT_DIR / "06_multicolor.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_varying_sizes": varying_sizes,
    "02_positioning": positioning,
    "02_grid_pattern": grid_pattern,
    "03_brightness_sized": brightness_sized,
    "03_layering": layering,
    "04_layering": advanced_layering,
    "05_grid_pattern": radial_grid_pattern,
    "06_multicolor": multicolor_composition,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-dots.md...")
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
