#!/usr/bin/env python3
"""
SVG Generator for: entities/03-curves.md

Generates visual examples for curve entity documentation.
"""

from pyfreeform import Scene, Curve, Palette, shapes
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-curves"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_curves.png"
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
# SECTION: Curvature Comparison
# =============================================================================

def curvature_comparison():
    """Curves with different curvature values"""
    scene = Scene.with_grid(cols=5, rows=1, cell_size=80)
    scene.background = "white"
    cells = list(scene.grid)

    curvatures = [-0.8, -0.3, 0.0, 0.3, 0.8]
    colors = ["#ef4444", "#f59e0b", "#94a3b8", "#3b82f6", "#8b5cf6"]

    for i, (curv, color) in enumerate(zip(curvatures, colors)):
        cells[i].add_curve(start="left", end="right", curvature=curv, width=2, color=color)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_curvature_comparison.svg")


# =============================================================================
# SECTION: Control Point Visualization
# =============================================================================

def control_point_visualization():
    """Visualize how the control point affects curve shape"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "white"
    cell = list(scene.grid)[0]

    # Draw multiple curves with varying curvature
    curvatures = [-0.6, -0.3, 0.0, 0.3, 0.6]
    colors = ["#fca5a5", "#fcd34d", "#94a3b8", "#93c5fd", "#c4b5fd"]

    for curv, color in zip(curvatures, colors):
        cell.add_curve(start="left", end="right", curvature=curv, width=2, color=color)

    # Highlight start and end points
    cell.add_dot(at="left", radius=6, color="#1f2937")
    cell.add_dot(at="right", radius=6, color="#1f2937")

    cell.add_border(color="#e0e0e0", width=0.5)
    scene.save(OUTPUT_DIR / "02_control_point_visualization.svg")


# =============================================================================
# SECTION: Brightness-Driven Curves
# =============================================================================

def brightness_driven():
    """Dots positioned along curves based on brightness"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)

    for cell in scene.grid:
        curve = cell.add_curve(
            start="bottom_left", end="top_right",
            curvature=0.4, width=1, color="#94a3b8"
        )
        cell.add_dot(along=curve, t=cell.brightness, radius=3, color=cell.color)

    scene.save(OUTPUT_DIR / "03_brightness_driven.svg")


# =============================================================================
# SECTION: Variable Curvature
# =============================================================================

def variable_curvature():
    """Curves with curvature varying across the grid (wave pattern)"""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=50)
    scene.background = "white"

    for cell in scene.grid:
        # Curvature varies from -1 to 1 based on column position
        curvature = (cell.col / (scene.grid.cols - 1) - 0.5) * 2

        # Color gradient from warm to cool based on curvature
        if curvature < 0:
            color = "#ef4444"  # Red for negative curvature
        elif curvature == 0:
            color = "#94a3b8"  # Gray for zero
        else:
            color = "#3b82f6"  # Blue for positive curvature

        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            width=1.5,
            color=color,
        )
        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "04_variable_curvature.svg")


# =============================================================================
# SECTION: Multiple Dots Along Curve
# =============================================================================

def multiple_dots_along_curve():
    """Curves with multiple dots placed at t=0, 0.25, 0.5, 0.75, 1.0"""
    scene = Scene.with_grid(cols=6, rows=4, cell_size=70)
    scene.background = "white"

    dot_colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6"]

    for cell in scene.grid:
        curve = cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=0.5,
            width=1,
            color="#94a3b8",
        )

        # Place dots at t = 0, 0.25, 0.5, 0.75, 1.0
        for i in range(5):
            t = i / 4
            cell.add_dot(
                along=curve,
                t=t,
                radius=3,
                color=dot_colors[i],
            )

        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "05_multiple_dots_along_curve.svg")


# =============================================================================
# SECTION: Complete Example (brightness-driven curvature with dots)
# =============================================================================

def complete_example():
    """Comprehensive example: brightness-driven curvature with dots along curves"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=30)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Only draw in medium brightness areas
        if 0.3 < cell.brightness < 0.7:
            # Curvature driven by brightness
            curvature = (cell.brightness - 0.5) * 2  # -0.4 to 0.4

            # Create curve
            curve = cell.add_curve(
                start="bottom_left",
                end="top_right",
                curvature=curvature,
                color=colors.line,
                width=1,
                z_index=1,
            )

            # Add dots along curve
            for i in range(3):
                t = i / 2  # 0, 0.5, 1.0
                cell.add_dot(
                    along=curve,
                    t=t,
                    radius=2,
                    color=colors.accent,
                    z_index=2,
                )

    scene.save(OUTPUT_DIR / "06_complete_example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_curvature_comparison": curvature_comparison,
    "02_control_point_visualization": control_point_visualization,
    "03_brightness_driven": brightness_driven,
    "04_variable_curvature": variable_curvature,
    "05_multiple_dots_along_curve": multiple_dots_along_curve,
    "06_complete_example": complete_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-curves.md...")
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
