#!/usr/bin/env python3
"""
SVG Generator for: getting-started/01-your-first-artwork.md

Generates highly incremental visual examples showing each step of the tutorial.
Every code change gets its own visual representation.

Corresponds to sections:
- The Famous 5-Line Example
- Step-by-Step Breakdown (Steps 1-4)
- Experiment section (grid size variations, dot sizing, spacing)
- Common Variations (brightness-based sizing, conditional rendering, palettes)
"""

from pyfreeform import Scene, Palette
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "01-your-first-artwork"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Create a test gradient image for consistent examples
def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_gradient.png"

    # Create 400x400 gradient (blue to orange)
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Radial gradient from center
            center_x, center_y = 200, 200
            distance = ((x - center_x)**2 + (y - center_y)**2) ** 0.5
            max_distance = (200**2 + 200**2) ** 0.5

            # Interpolate between blue (center) and orange (edges)
            t = min(distance / max_distance, 1.0)
            r = int(30 + t * (255 - 30))
            g = int(144 + t * (165 - 144))
            b = int(255 + t * (0 - 255))

            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_gradient()


# =============================================================================
# SECTION: The Famous 5-Line Example
# =============================================================================

def example_01_complete_5_line():
    """
    The complete 5-line example showing the final result.
    This is what users see first in the tutorial.
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color)

    scene.save(OUTPUT_DIR / "01-complete-5-line.svg")


# =============================================================================
# SECTION: Step-by-Step Breakdown
# =============================================================================

def step_00_blank_canvas():
    """
    Step 0: Before anything - just a blank canvas
    Shows what we're starting with
    """
    scene = Scene(width=400, height=400, background="#f8f9fa")
    scene.save(OUTPUT_DIR / "step-00-blank-canvas.svg")


def step_01_after_import():
    """
    Step 1: After 'from pyfreeform import Scene'
    Still blank, but we're ready to go
    """
    scene = Scene(width=400, height=400, background="#ffffff")
    scene.save(OUTPUT_DIR / "step-01-after-import.svg")


def step_02_grid_structure():
    """
    Step 2: After 'scene = Scene.from_image("photo.jpg", grid_size=40)'
    Show the grid structure with borders, no dots yet
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Show grid structure with light borders
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "step-02-grid-structure.svg")


def step_02b_grid_with_centers():
    """
    Step 2b: Show where dots will be placed (cell centers)
    Helps visualize the grid layout
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Show grid with small center markers
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)
        cell.add_dot(at="center", radius=1, color="#888888")

    scene.save(OUTPUT_DIR / "step-02b-grid-with-centers.svg")


def step_03_first_dots():
    """
    Step 3: After adding dots - but just a few to show the concept
    Show only first row to demonstrate the effect
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Add dots only to first 5 rows to show progression
    for cell in scene.grid:
        if cell.row < 5:
            cell.add_dot(color=cell.color, radius=5)
        else:
            cell.add_border(color="#f0f0f0", width=0.2)

    scene.save(OUTPUT_DIR / "step-03-first-dots.svg")


def step_03b_half_complete():
    """
    Step 3b: Halfway through the loop
    Show the progression of adding dots
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Add dots to first half
    for cell in scene.grid:
        if cell.row < scene.grid.rows // 2:
            cell.add_dot(color=cell.color, radius=5)
        else:
            cell.add_border(color="#f0f0f0", width=0.2)

    scene.save(OUTPUT_DIR / "step-03b-half-complete.svg")


def step_04_complete():
    """
    Step 4: Complete artwork - all dots added
    This is the final result after the loop completes
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "step-04-complete.svg")


# =============================================================================
# SECTION: Experiment - Grid Size Variations
# =============================================================================

def experiment_grid_size_10():
    """Very abstract with grid_size=10"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=10)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=18)

    scene.save(OUTPUT_DIR / "experiment-grid-size-10.svg")


def experiment_grid_size_20():
    """More abstract with grid_size=20"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=9)

    scene.save(OUTPUT_DIR / "experiment-grid-size-20.svg")


def experiment_grid_size_40():
    """Balanced with grid_size=40 (default)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "experiment-grid-size-40.svg")


def experiment_grid_size_60():
    """More detailed with grid_size=60"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=60)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=3)

    scene.save(OUTPUT_DIR / "experiment-grid-size-60.svg")


def experiment_grid_size_80():
    """Very detailed with grid_size=80"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=80)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=2.5)

    scene.save(OUTPUT_DIR / "experiment-grid-size-80.svg")


# =============================================================================
# SECTION: Experiment - Dot Size Variations
# =============================================================================

def experiment_dot_radius_2():
    """Small dots (radius=2)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=2)

    scene.save(OUTPUT_DIR / "experiment-dot-radius-2.svg")


def experiment_dot_radius_4():
    """Medium-small dots (radius=4)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "experiment-dot-radius-4.svg")


def experiment_dot_radius_6():
    """Medium-large dots (radius=6)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=6)

    scene.save(OUTPUT_DIR / "experiment-dot-radius-6.svg")


def experiment_dot_radius_8():
    """Large dots (radius=8) - overlapping"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=8)

    scene.save(OUTPUT_DIR / "experiment-dot-radius-8.svg")


# =============================================================================
# SECTION: Experiment - Cell Size (Spacing)
# =============================================================================

def experiment_cell_size_8():
    """Tight packing with cell_size=8"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40, cell_size=8)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=3)

    scene.save(OUTPUT_DIR / "experiment-cell-size-8.svg")


def experiment_cell_size_12():
    """Normal spacing with cell_size=12"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40, cell_size=12)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "experiment-cell-size-12.svg")


def experiment_cell_size_15():
    """More spacing with cell_size=15"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40, cell_size=15)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=6)

    scene.save(OUTPUT_DIR / "experiment-cell-size-15.svg")


def experiment_cell_size_20():
    """Loose spacing with cell_size=20"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40, cell_size=20)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=8)

    scene.save(OUTPUT_DIR / "experiment-cell-size-20.svg")


# =============================================================================
# SECTION: Common Variations
# =============================================================================

def variation_brightness_sizing_step1():
    """
    Brightness-based sizing - Step 1: Show formula
    All dots same size first (before applying brightness)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)  # All same size

    scene.save(OUTPUT_DIR / "variation-brightness-step1-uniform.svg")


def variation_brightness_sizing_step2():
    """
    Brightness-based sizing - Step 2: Apply brightness formula
    size = 2 + cell.brightness * 6
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        size = 2 + cell.brightness * 6  # Range: 2 to 8
        cell.add_dot(color=cell.color, radius=size)

    scene.save(OUTPUT_DIR / "variation-brightness-step2-dynamic.svg")


def variation_brightness_sizing_step3():
    """
    Brightness-based sizing - Step 3: More extreme variation
    size = 1 + cell.brightness * 8
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        size = 1 + cell.brightness * 8  # Range: 1 to 9
        cell.add_dot(color=cell.color, radius=size)

    scene.save(OUTPUT_DIR / "variation-brightness-step3-extreme.svg")


def variation_conditional_step1():
    """
    Conditional rendering - Step 1: All dots (before condition)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "variation-conditional-step1-all.svg")


def variation_conditional_step2():
    """
    Conditional rendering - Step 2: Only brightness > 0.5
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.5:
            cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "variation-conditional-step2-bright.svg")


def variation_conditional_step3():
    """
    Conditional rendering - Step 3: Only brightness > 0.7 (more selective)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.7:
            cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "variation-conditional-step3-very-bright.svg")


def variation_conditional_step4():
    """
    Conditional rendering - Step 4: Only brightness < 0.3 (dark areas)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness < 0.3:
            cell.add_dot(color=cell.color, radius=5)

    scene.save(OUTPUT_DIR / "variation-conditional-step4-dark.svg")


def variation_palette_step1():
    """
    Using palettes - Step 1: Original colors (before palette)
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        if cell.brightness > 0.6:
            cell.add_dot(color=cell.color, radius=5)
        elif cell.brightness > 0.3:
            cell.add_dot(color=cell.color, radius=3)

    scene.save(OUTPUT_DIR / "variation-palette-step1-original.svg")


def variation_palette_step2():
    """
    Using palettes - Step 2: Apply midnight palette
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.6:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=3)

    scene.save(OUTPUT_DIR / "variation-palette-step2-midnight.svg")


def variation_palette_step3():
    """
    Using palettes - Step 3: Try ocean palette
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.6:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=3)

    scene.save(OUTPUT_DIR / "variation-palette-step3-ocean.svg")


def variation_palette_step4():
    """
    Using palettes - Step 4: Try sunset palette
    """
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        if cell.brightness > 0.6:
            cell.add_dot(color=colors.primary, radius=5)
        elif cell.brightness > 0.3:
            cell.add_dot(color=colors.secondary, radius=3)

    scene.save(OUTPUT_DIR / "variation-palette-step4-sunset.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Main 5-line example
    "01-complete-5-line": example_01_complete_5_line,

    # Step-by-step breakdown (highly incremental!)
    "step-00-blank-canvas": step_00_blank_canvas,
    "step-01-after-import": step_01_after_import,
    "step-02-grid-structure": step_02_grid_structure,
    "step-02b-grid-with-centers": step_02b_grid_with_centers,
    "step-03-first-dots": step_03_first_dots,
    "step-03b-half-complete": step_03b_half_complete,
    "step-04-complete": step_04_complete,

    # Grid size experiments
    "experiment-grid-size-10": experiment_grid_size_10,
    "experiment-grid-size-20": experiment_grid_size_20,
    "experiment-grid-size-40": experiment_grid_size_40,
    "experiment-grid-size-60": experiment_grid_size_60,
    "experiment-grid-size-80": experiment_grid_size_80,

    # Dot size experiments
    "experiment-dot-radius-2": experiment_dot_radius_2,
    "experiment-dot-radius-4": experiment_dot_radius_4,
    "experiment-dot-radius-6": experiment_dot_radius_6,
    "experiment-dot-radius-8": experiment_dot_radius_8,

    # Cell size (spacing) experiments
    "experiment-cell-size-8": experiment_cell_size_8,
    "experiment-cell-size-12": experiment_cell_size_12,
    "experiment-cell-size-15": experiment_cell_size_15,
    "experiment-cell-size-20": experiment_cell_size_20,

    # Brightness-based sizing (incremental)
    "variation-brightness-step1-uniform": variation_brightness_sizing_step1,
    "variation-brightness-step2-dynamic": variation_brightness_sizing_step2,
    "variation-brightness-step3-extreme": variation_brightness_sizing_step3,

    # Conditional rendering (incremental)
    "variation-conditional-step1-all": variation_conditional_step1,
    "variation-conditional-step2-bright": variation_conditional_step2,
    "variation-conditional-step3-very-bright": variation_conditional_step3,
    "variation-conditional-step4-dark": variation_conditional_step4,

    # Palette usage (incremental)
    "variation-palette-step1-original": variation_palette_step1,
    "variation-palette-step2-midnight": variation_palette_step2,
    "variation-palette-step3-ocean": variation_palette_step3,
    "variation-palette-step4-sunset": variation_palette_step4,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 01-your-first-artwork.md...")

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
