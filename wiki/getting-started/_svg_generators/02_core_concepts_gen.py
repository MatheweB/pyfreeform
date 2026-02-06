#!/usr/bin/env python3
"""
SVG Generator for: getting-started/02-core-concepts.md

Generates visual examples for the core concepts: Scene, Grid, Cell, and Entity.

Corresponds to sections:
- Creating Scenes (3 methods)
- Grid and Cell Access
- How They Work Together (complete example)
"""

from pyfreeform import Scene, Palette
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "02-core-concepts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Create a test gradient image for consistent examples
def create_test_gradient() -> Path:
    """Create a simple gradient image for testing"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_core_concepts.png"

    # Create 400x400 gradient
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)

    for y in range(400):
        for x in range(400):
            # Diagonal gradient
            t = (x + y) / 800
            r = int(70 + t * 150)
            g = int(130 + t * 100)
            b = int(180 + t * 50)
            draw.point((x, y), fill=(r, g, b))

    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_gradient()


# =============================================================================
# SECTION: Creating Scenes - 3 Methods
# =============================================================================

def example_01_scene_from_image():
    """Method 1: Create scene from an image"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # Add dots to show it's loaded with image data
    for cell in scene.grid:
        cell.add_dot(color=cell.color, radius=4)

    scene.save(OUTPUT_DIR / "01-scene-from-image.svg")


def example_02_scene_with_grid():
    """Method 2: Create scene with an empty grid"""
    scene = Scene.with_grid(cols=30, rows=30, cell_size=12)

    # Add a simple pattern to show the grid
    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_dot(radius=4, color="#6366f1")

    scene.save(OUTPUT_DIR / "02-scene-with-grid.svg")


def example_03_scene_manual():
    """Method 3: Create scene manually — using scene builder methods"""
    scene = Scene(width=800, height=600, background="white")

    # Scene is a Surface — use builder methods directly!
    scene.add_dot(at=(0.5, 0.5), radius=50, color="#f59e0b")
    scene.add_ellipse(at=(0.75, 0.33), rx=80, ry=40, fill="#10b981")
    scene.add_line(start=(0.125, 0.17), end=(0.875, 0.83), color="#ef4444", width=3)

    scene.save(OUTPUT_DIR / "03-scene-manual.svg")


# =============================================================================
# SECTION: Grid and Cell Access
# =============================================================================

def example_04_cell_access():
    """Demonstrate accessing cells by index and iteration"""
    scene = Scene.with_grid(cols=10, rows=10, cell_size=40)

    # Access specific cell by index
    cell = scene.grid[5, 3]
    cell.add_dot(radius=15, color="#dc2626")

    # Show grid structure
    for c in scene.grid:
        c.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "04-cell-access.svg")


def example_05_cell_properties():
    """Show cell properties and helpers"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=50)

    # Demonstrate position helpers
    for cell in scene.grid:
        # Add dots at named positions
        if cell.row == 3 and cell.col == 3:
            cell.add_dot(at="top_left", radius=3, color="#ef4444")
            cell.add_dot(at="top_right", radius=3, color="#f59e0b")
            cell.add_dot(at="bottom_left", radius=3, color="#10b981")
            cell.add_dot(at="bottom_right", radius=3, color="#3b82f6")
            cell.add_dot(at="center", radius=5, color="#8b5cf6")
        else:
            cell.add_border(color="#f0f0f0", width=0.3)

    scene.save(OUTPUT_DIR / "05-cell-properties.svg")


# =============================================================================
# SECTION: How They Work Together
# =============================================================================

def example_06_complete_workflow():
    """
    Complete example from the doc showing Scene, Grid, Cell, Entity working together.
    This is the main teaching example of the file.
    """
    # 1. Create Scene with Grid
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    colors = Palette.ocean()
    scene.background = colors.background

    # 2. Work with Cells and Entities
    for cell in scene.grid:
        # Cell knows its brightness from the image
        if cell.brightness > 0.7:
            # Add a large dot entity in bright areas
            dot = cell.add_dot(radius=8, color=colors.primary)

        elif cell.brightness > 0.4:
            # Add a curve entity in medium areas
            curve = cell.add_curve(
                start="bottom_left",
                end="top_right",
                curvature=0.5,
                color=colors.secondary
            )
            # Add smaller dot along the curve
            cell.add_dot(
                along=curve,
                t=cell.brightness,
                radius=3,
                color=colors.accent
            )

        else:
            # Add border in dark areas
            cell.add_border(color=colors.line, width=0.5)

    # 3. Scene renders all entities
    scene.save(OUTPUT_DIR / "06-complete-workflow.svg")


# =============================================================================
# SECTION: Coordinate Systems
# =============================================================================

def example_07_coordinate_systems():
    """Demonstrate the different coordinate systems"""
    scene = Scene.with_grid(cols=5, rows=5, cell_size=60)

    # Scene-level positioning (named positions work on the whole canvas)
    scene.add_dot(at="center", radius=8, color="#dc2626")

    # Relative positioning within cells
    center_cell = scene.grid[2, 2]
    center_cell.add_dot(at=(0.25, 0.25), radius=5, color="#f59e0b")
    center_cell.add_dot(at=(0.75, 0.75), radius=5, color="#10b981")

    # Parametric positioning along a path
    curve = center_cell.add_curve(
        start="top_left",
        end="bottom_right",
        curvature=0.8,
        color="#6366f1"
    )
    center_cell.add_dot(along=curve, t=0.5, radius=4, color="#8b5cf6")

    # Show grid
    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "07-coordinate-systems.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-scene-from-image": example_01_scene_from_image,
    "02-scene-with-grid": example_02_scene_with_grid,
    "03-scene-manual": example_03_scene_manual,
    "04-cell-access": example_04_cell_access,
    "05-cell-properties": example_05_cell_properties,
    "06-complete-workflow": example_06_complete_workflow,
    "07-coordinate-systems": example_07_coordinate_systems,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 02-core-concepts.md...")

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
