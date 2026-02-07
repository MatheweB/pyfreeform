#!/usr/bin/env python3
"""
SVG Generator for: fundamentals/01-scenes.md

Generates incremental visual examples for scene creation and usage.

Corresponds to sections:
- Creating Scenes (3 methods: from_image, with_grid, manual)
- Scene Properties
- Adding Content
- Common Patterns (3 patterns)
"""

from pyfreeform import Scene, Palette, Grid
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-scenes"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_gradient_scenes.png"

    # Create 600x400 gradient (purple to teal)
    img = Image.new('RGB', (600, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(600):
            # Horizontal gradient
            t = x / 600
            r = int(147 + t * (64 - 147))
            g = int(112 + t * (224 - 112))
            b = int(219 + t * (208 - 219))
            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_gradient()


# =============================================================================
# SECTION: Creating Scenes - Method 1: from_image()
# =============================================================================

def method1_step0_original_image():
    """Show what the original image looks like"""
    # Just create a visual representation
    scene = Scene.from_image(TEST_IMAGE, grid_size=1)

    # Show the actual image as filled cells
    for cell in scene.grid:
        cell.add_fill(color=cell.color)

    scene.save(OUTPUT_DIR / "method1-step0-original-image.svg")


def method1_step1_with_grid():
    """from_image() - Show the grid overlay"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Just show grid structure
    for cell in scene.grid:
        cell.add_border(color="#ffffff", width=0.5)

    scene.save(OUTPUT_DIR / "method1-step1-with-grid.svg")


def method1_step2_grid_and_dots():
    """from_image() - Add dots to show image data is loaded"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Show every 4th cell to demonstrate
        if (cell.row + cell.col) % 4 == 0:
            cell.add_dot(color=cell.color, radius=3)

    scene.save(OUTPUT_DIR / "method1-step2-grid-and-dots.svg")


def method1_step3_complete_dots():
    """from_image() - Complete dot artwork from image"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.5:
            cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "method1-step3-complete-dots.svg")


def method1_variation_grid_size():
    """from_image() - Show different grid_size parameter"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=50)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "method1-variation-grid-size-50.svg")


def method1_variation_cell_size():
    """from_image() - Show cell_size parameter effect"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=50, cell_size=12)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "method1-variation-cell-size.svg")


# =============================================================================
# SECTION: Creating Scenes - Method 2: with_grid()
# =============================================================================

def method2_step1_empty_grid():
    """with_grid() - Empty grid structure"""
    scene = Scene.with_grid(cols=30, rows=30, cell_size=12)

    # Show grid with borders only
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "method2-step1-empty-grid.svg")


def method2_step2_checkerboard():
    """with_grid() - Simple algorithmic pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        # Algorithmic pattern based on position
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color=colors.primary, radius=6)

    scene.save(OUTPUT_DIR / "method2-step2-checkerboard.svg")


def method2_step3_full_pattern():
    """with_grid() - Complete generative pattern"""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=15)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color=colors.primary, radius=6)
        else:
            cell.add_dot(color=colors.secondary, radius=3)

    scene.save(OUTPUT_DIR / "method2-step3-full-pattern.svg")


def method2_variation_different_size():
    """with_grid() - Different grid dimensions"""
    scene = Scene.with_grid(cols=40, rows=25, cell_size=10)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color=colors.primary, radius=4)

    scene.save(OUTPUT_DIR / "method2-variation-dimensions.svg")


# =============================================================================
# SECTION: Creating Scenes - Method 3: Manual
# =============================================================================

def method3_step1_blank_canvas():
    """Manual scene - Blank canvas"""
    scene = Scene(width=800, height=600, background="white")
    scene.save(OUTPUT_DIR / "method3-step1-blank-canvas.svg")


def method3_step2_add_dots():
    """Manual scene - Add dots using scene builder methods"""
    scene = Scene(width=800, height=600, background="white")

    # Scene is a Surface — add dots directly!
    scene.add_dot(at=(0.125, 0.17), radius=20, color="red")
    scene.add_dot(at=(0.375, 0.33), radius=20, color="blue")

    scene.save(OUTPUT_DIR / "method3-step2-add-dots.svg")


def method3_step3_add_line():
    """Manual scene - Add line connecting dots"""
    scene = Scene(width=800, height=600, background="white")

    # Builder methods — no manual coordinate math needed
    scene.add_line(start=(0.125, 0.17), end=(0.375, 0.33), color="gray", width=2)
    scene.add_dot(at=(0.125, 0.17), radius=20, color="red", z_index=1)
    scene.add_dot(at=(0.375, 0.33), radius=20, color="blue", z_index=1)

    scene.save(OUTPUT_DIR / "method3-step3-add-line.svg")


def method3_step4_complete():
    """Manual scene - Complete freeform composition"""
    scene = Scene(width=800, height=600, background="white")

    # Scene builder methods — same API as cells!
    scene.add_line(start=(0.125, 0.17), end=(0.375, 0.33), color="gray", width=2)
    scene.add_line(start=(0.375, 0.33), end=(0.625, 0.25), color="gray", width=2)
    scene.add_dot(at=(0.125, 0.17), radius=20, color="red", z_index=1)
    scene.add_dot(at=(0.375, 0.33), radius=20, color="blue", z_index=1)
    scene.add_dot(at=(0.625, 0.25), radius=20, color="green", z_index=1)

    scene.save(OUTPUT_DIR / "method3-step4-complete.svg")


# =============================================================================
# SECTION: Scene Properties - Background
# =============================================================================

def properties_background_step1_none():
    """Background property - No background (transparent)"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=15)
    # No background set

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color="#3b82f6", radius=6)

    scene.save(OUTPUT_DIR / "properties-background-none.svg")


def properties_background_step2_white():
    """Background property - White background"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=15)
    scene.background = "white"

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color="#3b82f6", radius=6)

    scene.save(OUTPUT_DIR / "properties-background-white.svg")


def properties_background_step3_color():
    """Background property - Colored background"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=15)
    scene.background = "#f0f9ff"

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(color="#3b82f6", radius=6)

    scene.save(OUTPUT_DIR / "properties-background-colored.svg")


# =============================================================================
# SECTION: Common Pattern 1 - Image-Based Art
# =============================================================================

def pattern1_step1_load_image():
    """Pattern 1 - Load image with grid"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Show grid only
    for cell in scene.grid:
        cell.add_border(color="#cccccc", width=0.3)

    scene.save(OUTPUT_DIR / "pattern1-step1-load-image.svg")


def pattern1_step2_add_dots():
    """Pattern 1 - Add dots based on brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Use image data
        if cell.brightness > 0.5:
            cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "pattern1-step2-add-dots.svg")


def pattern1_step3_final():
    """Pattern 1 - Final image-based artwork"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.5:
            cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "pattern1-step3-final.svg")


# =============================================================================
# SECTION: Common Pattern 2 - Generative Patterns
# =============================================================================

def pattern2_step1_empty_grid():
    """Pattern 2 - Start with empty grid"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=16)
    colors = Palette.ocean()
    scene.background = colors.background

    # Show grid structure
    for cell in scene.grid:
        cell.add_border(color="#dddddd", width=0.3)

    scene.save(OUTPUT_DIR / "pattern2-step1-empty-grid.svg")


def pattern2_step2_center_marker():
    """Pattern 2 - Mark the center point"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=16)
    colors = Palette.ocean()
    scene.background = colors.background

    # Mark center
    center_cell = scene.grid[12, 12]
    center_cell.add_dot(color="red", radius=8)

    scene.save(OUTPUT_DIR / "pattern2-step2-center-marker.svg")


def pattern2_step3_distance_calc():
    """Pattern 2 - Show distance-based sizing (partial)"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=16)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Algorithmic logic
        distance = ((cell.row - 12)**2 + (cell.col - 12)**2) ** 0.5
        if distance < 10:
            # Show first few
            size = 3 + (10 - distance) * 0.4
            cell.add_dot(color=colors.primary, radius=size)

    scene.save(OUTPUT_DIR / "pattern2-step3-distance-calc.svg")


def pattern2_step4_complete():
    """Pattern 2 - Complete circle pattern"""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=16)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        distance = ((cell.row - 12)**2 + (cell.col - 12)**2) ** 0.5
        if distance < 10:
            size = 3 + (10 - distance) * 0.4
            cell.add_dot(color=colors.primary, radius=size)

    scene.save(OUTPUT_DIR / "pattern2-step4-complete.svg")


# =============================================================================
# SECTION: Common Pattern 3 - Mixed Approach
# =============================================================================

def pattern3_step1_image_base():
    """Pattern 3 - Start with image"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Add grid-based elements
    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "pattern3-step1-image-base.svg")


def pattern3_step2_add_title():
    """Pattern 3 - Add title using scene builder methods"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Add grid-based elements
    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    # Scene is a Surface — add text directly with named positions!
    scene.add_text("My Artwork", at=(0.5, 0.1), font_size=24, color="white")

    scene.save(OUTPUT_DIR / "pattern3-step2-add-title.svg")


def pattern3_step3_add_border():
    """Pattern 3 - Add decorative border using scene builder"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    # Add grid-based elements
    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    # Scene builder methods — no manual coordinate math
    scene.add_text("My Artwork", at=(0.5, 0.1), font_size=24, color="white")
    scene.add_border(color="white", width=3)

    scene.save(OUTPUT_DIR / "pattern3-step3-add-border.svg")


# =============================================================================
# SECTION: Multiple Grids (Advanced)
# =============================================================================

def advanced_multiple_grids_step1():
    """Multiple grids - First grid only"""
    scene = Scene(width=800, height=600, background="#1a1a2e")

    # Create first grid
    grid1 = Grid(cols=20, rows=20, cell_size=10, origin=(0, 0))

    for cell in grid1:
        cell.add_dot(color="#e94560", radius=2)

    scene.save(OUTPUT_DIR / "advanced-multiple-grids-step1.svg")


def advanced_multiple_grids_step2():
    """Multiple grids - Add second grid"""
    scene = Scene(width=800, height=600, background="#1a1a2e")

    # Create two grids
    grid1 = Grid(cols=20, rows=20, cell_size=10, origin=(0, 0))
    grid2 = Grid(cols=10, rows=10, cell_size=20, origin=(400, 300))

    for cell in grid1:
        cell.add_dot(color="#e94560", radius=2)

    for cell in grid2:
        cell.add_dot(color="#0f3460", radius=5)

    scene.save(OUTPUT_DIR / "advanced-multiple-grids-step2.svg")


# =============================================================================
# SECTION: Rectangular Cells & Fit-to-Image
# =============================================================================

def scene_rect_cells():
    """Scene with rectangular cells"""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=20, cell_width=30, cell_height=20)
    scene.background = "#1e293b"

    for cell in scene.grid:
        cell.add_dot(radius=4, color="#38bdf8")
        cell.add_border(color="#334155", width=0.5)

    scene.save(OUTPUT_DIR / "scene-rect-cells.svg")

def scene_fit_to_image():
    """Scene.from_image with grid_size=None (fit to image)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=None, cell_size=8)

    for cell in scene.grid:
        cell.add_fill(color=cell.color)

    scene.save(OUTPUT_DIR / "scene-fit-to-image.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Method 1: from_image
    "method1-step0-original-image": method1_step0_original_image,
    "method1-step1-with-grid": method1_step1_with_grid,
    "method1-step2-grid-and-dots": method1_step2_grid_and_dots,
    "method1-step3-complete-dots": method1_step3_complete_dots,
    "method1-variation-grid-size-50": method1_variation_grid_size,
    "method1-variation-cell-size": method1_variation_cell_size,

    # Method 2: with_grid
    "method2-step1-empty-grid": method2_step1_empty_grid,
    "method2-step2-checkerboard": method2_step2_checkerboard,
    "method2-step3-full-pattern": method2_step3_full_pattern,
    "method2-variation-dimensions": method2_variation_different_size,

    # Method 3: Manual
    "method3-step1-blank-canvas": method3_step1_blank_canvas,
    "method3-step2-add-dots": method3_step2_add_dots,
    "method3-step3-add-line": method3_step3_add_line,
    "method3-step4-complete": method3_step4_complete,

    # Properties - Background
    "properties-background-none": properties_background_step1_none,
    "properties-background-white": properties_background_step2_white,
    "properties-background-colored": properties_background_step3_color,

    # Pattern 1: Image-Based Art
    "pattern1-step1-load-image": pattern1_step1_load_image,
    "pattern1-step2-add-dots": pattern1_step2_add_dots,
    "pattern1-step3-final": pattern1_step3_final,

    # Pattern 2: Generative Patterns
    "pattern2-step1-empty-grid": pattern2_step1_empty_grid,
    "pattern2-step2-center-marker": pattern2_step2_center_marker,
    "pattern2-step3-distance-calc": pattern2_step3_distance_calc,
    "pattern2-step4-complete": pattern2_step4_complete,

    # Pattern 3: Mixed Approach
    "pattern3-step1-image-base": pattern3_step1_image_base,
    "pattern3-step2-add-title": pattern3_step2_add_title,
    "pattern3-step3-add-border": pattern3_step3_add_border,

    # Advanced: Multiple Grids
    "advanced-multiple-grids-step1": advanced_multiple_grids_step1,
    "advanced-multiple-grids-step2": advanced_multiple_grids_step2,

    # Rectangular cells & fit-to-image
    "scene-rect-cells": scene_rect_cells,
    "scene-fit-to-image": scene_fit_to_image,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-scenes.md...")

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
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
