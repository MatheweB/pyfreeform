#!/usr/bin/env python3
"""
SVG Generator for: entities/04-ellipses.md

Generates visual examples for ellipse entity documentation.
"""

from pyfreeform import Scene
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-ellipses"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_ellipses.png"
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
# SECTION: Circles vs Ellipses
# =============================================================================

def circles_vs_ellipses():
    """Comparison of circles and ellipses"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "white"
    cells = list(scene.grid)

    # Circle (rx == ry)
    cells[0].add_ellipse(rx=30, ry=30, fill="#3b82f6")
    # Wide ellipse
    cells[1].add_ellipse(rx=35, ry=18, fill="#ef4444")
    # Tall ellipse
    cells[2].add_ellipse(rx=18, ry=35, fill="#10b981")
    # Small circle with stroke
    cells[3].add_ellipse(rx=25, ry=25, fill="none", stroke="#8b5cf6", stroke_width=2)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_circles_vs_ellipses.svg")


# =============================================================================
# SECTION: Rotation Angles
# =============================================================================

def rotation_angles():
    """Ellipses at different rotation angles"""
    scene = Scene.with_grid(cols=6, rows=1, cell_size=80)
    scene.background = "white"
    cells = list(scene.grid)

    angles = [0, 30, 45, 60, 90, 135]
    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]

    for i, (angle, color) in enumerate(zip(angles, colors)):
        cells[i].add_ellipse(rx=25, ry=12, rotation=angle, fill=color)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "02_rotation_angles.svg")


# =============================================================================
# SECTION: Parametric Positioning
# =============================================================================

def parametric_positioning():
    """Dots positioned around an ellipse perimeter"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=250)
    scene.background = "white"
    cell = list(scene.grid)[0]

    # Create ellipse
    ellipse = cell.add_ellipse(rx=80, ry=50, fill="none", stroke="#94a3b8", stroke_width=2)

    # Position dots around the perimeter
    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899",
              "#14b8a6", "#f97316"]
    for i in range(8):
        t = i / 8
        cell.add_dot(along=ellipse, t=t, radius=8, color=colors[i])

    cell.add_border(color="#e0e0e0", width=0.5)
    scene.save(OUTPUT_DIR / "03_parametric_positioning.svg")


# =============================================================================
# SECTION: Brightness-Sized Ellipses
# =============================================================================

def brightness_sized_ellipses():
    """Ellipses sized by brightness, filling cells"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    for cell in scene.grid:
        scale = 0.3 + cell.brightness * 0.7  # 30% to 100%

        ellipse = cell.add_ellipse(
            rx=40,
            ry=40,
            fill=cell.color
        )
        ellipse.fit_to_cell(scale)

    scene.save(OUTPUT_DIR / "04_brightness_sized_ellipses.svg")


# =============================================================================
# SECTION: Rotating Ellipses
# =============================================================================

def rotating_ellipses():
    """Ellipses with rotation varying by position"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    for cell in scene.grid:
        rotation = (cell.row + cell.col) * 15  # degrees

        ellipse = cell.add_ellipse(
            rx=40,
            ry=20,
            rotation=rotation,
            fill=cell.color
        )
        ellipse.fit_to_cell(0.85)

    scene.save(OUTPUT_DIR / "05_rotating_ellipses.svg")


# =============================================================================
# SECTION: Orbiting Dots
# =============================================================================

def orbiting_dots():
    """Invisible ellipse paths with dots positioned along them"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)

    for cell in scene.grid:
        if cell.brightness > 0.3:
            # Create ellipse path
            ellipse = cell.add_ellipse(
                rx=40,
                ry=30,
                rotation=45,
                fill="none",
                stroke="#cccccc",
                stroke_width=0.5
            )
            ellipse.fit_to_cell(0.85)

            # Position dot along ellipse based on brightness
            cell.add_dot(
                along=ellipse,
                t=cell.brightness,
                radius=3,
                color=cell.color
            )

    scene.save(OUTPUT_DIR / "06_orbiting_dots.svg")


# =============================================================================
# SECTION: Radial Composition
# =============================================================================

def radial_composition():
    """Ellipses rotated to point toward/away from center based on angle"""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=30)
    scene.background = "#1a1a2e"

    center_row = 7
    center_col = 7

    for cell in scene.grid:
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr * dr + dc * dc)
        max_dist = math.sqrt(center_row ** 2 + center_col ** 2)

        if distance < 0.5:
            continue

        angle = math.degrees(math.atan2(dr, dc))

        # Size decreases with distance (clamp to valid range)
        scale = min(1.0, 0.9 * (1 - distance / max_dist) + 0.2)

        # Color varies by angle
        hue_shift = int((angle + 180) / 360 * 255)
        r = max(50, min(255, 100 + hue_shift))
        g = max(50, min(255, 200 - hue_shift))
        b = max(50, min(255, 150 + int(distance * 20)))
        color = f"#{r:02x}{g:02x}{b:02x}"

        ellipse = cell.add_ellipse(
            rx=20,
            ry=10,
            rotation=angle,
            fill=color
        )
        ellipse.fit_to_cell(scale)

    scene.save(OUTPUT_DIR / "07_radial_composition.svg")


# =============================================================================
# SECTION: Complete Example - Radial Ellipses with Dots
# =============================================================================

def complete_radial_example():
    """Comprehensive radial ellipses with dots on perimeters"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=25)
    scene.background = "#0f172a"

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr * dr + dc * dc)
        angle = math.degrees(math.atan2(dr, dc))

        # Size based on brightness
        scale = 0.3 + cell.brightness * 0.7

        # Create rotated ellipse pointing toward/away from center
        ellipse = cell.add_ellipse(
            rx=40,
            ry=20,
            rotation=angle,
            fill=cell.color,
            z_index=1
        )
        ellipse.fit_to_cell(scale)

        # Add dot on ellipse perimeter
        cell.add_dot(
            along=ellipse,
            t=cell.brightness,
            radius=2,
            color="#f59e0b",
            z_index=2
        )

    scene.save(OUTPUT_DIR / "08_complete_radial_example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_circles_vs_ellipses": circles_vs_ellipses,
    "02_rotation_angles": rotation_angles,
    "03_parametric_positioning": parametric_positioning,
    "04_brightness_sized_ellipses": brightness_sized_ellipses,
    "05_rotating_ellipses": rotating_ellipses,
    "06_orbiting_dots": orbiting_dots,
    "07_radial_composition": radial_composition,
    "08_complete_radial_example": complete_radial_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-ellipses.md...")
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
