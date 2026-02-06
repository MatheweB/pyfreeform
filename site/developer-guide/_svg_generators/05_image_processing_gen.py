#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/05-image-processing.md

Generates visual examples for image processing internals.

Corresponds to sections:
- Image Class
- Layer Class
- Grid Loading
"""

from pathlib import Path
from PIL import Image as PILImage, ImageDraw
import tempfile
from pyfreeform import Scene

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "05-image-processing"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create a test image
def create_test_image() -> Path:
    """Create a simple gradient test image"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_dev_guide_test.png"
    img = PILImage.new('RGB', (200, 200))
    draw = ImageDraw.Draw(img)

    for y in range(200):
        for x in range(200):
            # Gradient from top-left (bright) to bottom-right (dark)
            brightness = int(255 * (1 - ((x + y) / 400)))
            draw.point((x, y), fill=(brightness, brightness, brightness))

    img.save(temp_file)
    return temp_file

TEST_IMAGE = create_test_image()

# =============================================================================
# SECTION: Image Loading Demonstration
# =============================================================================

def image_loading_basic():
    """Show basic image loading"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    # Just show the loaded grid
    for cell in scene.grid:
        cell.add_border(color="#ffffff", width=0.5)

    scene.save(OUTPUT_DIR / "01-image-loading-basic.svg")

def image_to_grid():
    """Show image converted to grid"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Show grid with brightness-based dots
    for cell in scene.grid:
        radius = 2 + cell.brightness * 6
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "02-image-to-grid.svg")

# =============================================================================
# SECTION: Layer Extraction Visualization
# =============================================================================

def layer_brightness():
    """Brightness layer visualization"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Use brightness to size dots
    for cell in scene.grid:
        if cell.brightness > 0.3:
            radius = 2 + cell.brightness * 8
            cell.add_dot(radius=radius, color="#3b82f6")

    scene.save(OUTPUT_DIR / "03-layer-brightness.svg")

def layer_comparison():
    """Compare different layer uses"""
    # Create grid from image
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Use brightness for sizing, color for... color
    for cell in scene.grid:
        radius = 2 + cell.brightness * 8
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "04-layer-comparison.svg")

# =============================================================================
# SECTION: Grid Loading Process
# =============================================================================

def grid_loading_steps():
    """Show different grid sizes"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    # Simple border view
    for cell in scene.grid:
        cell.add_border(color="#3b82f6", width=1)

    scene.save(OUTPUT_DIR / "05-grid-loading-steps.svg")

def grid_sizes():
    """Compare different grid sizes (concept)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=25)

    # Show every other cell
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=cell.color)

    scene.save(OUTPUT_DIR / "06-grid-sizes.svg")

# =============================================================================
# SECTION: Cell Data Access
# =============================================================================

def cell_data_brightness():
    """Access cell brightness data"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=35)

    # Only show bright cells
    for cell in scene.grid:
        if cell.brightness > 0.6:
            cell.add_ellipse(rx=10, ry=10, fill="#10b981")
        elif cell.brightness > 0.3:
            cell.add_dot(radius=5, color="#3b82f6")

    scene.save(OUTPUT_DIR / "07-cell-data-brightness.svg")

def cell_data_color():
    """Access cell color data"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Use cell color directly
    for cell in scene.grid:
        radius = 3 + cell.brightness * 7
        cell.add_dot(radius=radius, color=cell.color)

    scene.save(OUTPUT_DIR / "08-cell-data-color.svg")

# =============================================================================
# SECTION: Practical Application
# =============================================================================

def practical_halftone():
    """Halftone effect from image"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Create halftone dots
    for cell in scene.grid:
        radius = 1 + cell.brightness * 8
        cell.add_dot(radius=radius, color="#1f2937")

    scene.save(OUTPUT_DIR / "09-practical-halftone.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-image-loading-basic": image_loading_basic,
    "02-image-to-grid": image_to_grid,
    "03-layer-brightness": layer_brightness,
    "04-layer-comparison": layer_comparison,
    "05-grid-loading-steps": grid_loading_steps,
    "06-grid-sizes": grid_sizes,
    "07-cell-data-brightness": cell_data_brightness,
    "08-cell-data-color": cell_data_color,
    "09-practical-halftone": practical_halftone,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 05-image-processing.md...")

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
