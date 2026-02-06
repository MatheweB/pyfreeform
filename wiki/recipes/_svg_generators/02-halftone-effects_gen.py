"""SVG Generator for Recipe: Halftone Effects."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/02-halftone-effects')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def create_synthetic_brightness_grid(scene):
    """Create synthetic brightness values simulating an image."""
    for cell in scene.grid:
        # Create a portrait-like brightness pattern
        dx = cell.col - scene.grid.cols / 2
        dy = cell.row - scene.grid.rows / 2
        distance = math.sqrt(dx*dx + dy*dy)
        max_distance = math.sqrt((scene.grid.cols/2)**2 + (scene.grid.rows/2)**2)

        # Simulate brightness: bright in center, dark at edges
        brightness = 1 - (distance / max_distance)
        brightness = max(0, min(1, brightness))

        # Add texture
        texture = (math.sin(cell.col * 0.3) * math.cos(cell.row * 0.3)) * 0.2
        brightness = max(0, min(1, brightness + texture))

        cell._brightness = brightness

        # Calculate color
        gray = int(brightness * 255)
        cell._color = f"#{gray:02x}{gray:02x}{gray:02x}"


def image_01_basic_halftone():
    """Basic halftone - black dots on white."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    scene.background = "white"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Invert brightness for halftone effect
        size = (1 - cell._brightness) * 8
        if size > 0.5:  # Don't draw tiny dots
            cell.add_dot(radius=size, color="black")

    save_svg("01_basic_halftone.svg", scene)


def image_02_color_halftone():
    """Color halftone with brightness-based sizing."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    scene.background = "#f5f5f5"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        size = cell._brightness * 6
        if size > 0.5:
            cell.add_dot(radius=size, color=cell._color)

    save_svg("02_color_halftone.svg", scene)


def image_03_cmyk_style():
    """CMYK-style halftone with color overlay."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    colors = Palette.sunset()
    scene.background = "white"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Inverted size
        size = (1 - cell._brightness) * 7

        # Color based on position
        if cell.col < scene.grid.cols / 3:
            color = "#00FFFF"  # Cyan
        elif cell.col < 2 * scene.grid.cols / 3:
            color = "#FF00FF"  # Magenta
        else:
            color = "#FFFF00"  # Yellow

        if size > 0.5:
            cell.add_dot(radius=size, color=color)

    save_svg("03_cmyk_style.svg", scene)


def image_04_threshold_halftone():
    """Threshold-based halftone."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    scene.background = "white"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Different dot sizes based on brightness thresholds
        if cell._brightness < 0.3:
            size = 7
        elif cell._brightness < 0.5:
            size = 5
        elif cell._brightness < 0.7:
            size = 3
        else:
            size = 1

        if size > 0:
            cell.add_dot(radius=size, color="black")

    save_svg("04_threshold_halftone.svg", scene)


def image_05_dual_color():
    """Dual-color halftone effect."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    colors = Palette.midnight()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        size = (1 - cell._brightness) * 7

        # Alternate colors
        if (cell.row + cell.col) % 2 == 0:
            color = colors.primary
        else:
            color = colors.secondary

        if size > 0.5:
            cell.add_dot(radius=size, color=color)

    save_svg("05_dual_color.svg", scene)


def image_06_newspaper_style():
    """Classic newspaper halftone style."""
    scene = Scene.with_grid(cols=60, rows=45, cell_size=7)
    scene.background = "#fafafa"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Newspaper uses inverted brightness
        inverted = 1 - cell._brightness
        size = inverted * 6

        # Only render if meaningful size
        if size > 0.3:
            cell.add_dot(radius=size, color="#1a1a1a")

    save_svg("06_newspaper_style.svg", scene)


def image_07_gradient_halftone():
    """Halftone with gradient color mapping."""
    scene = Scene.with_grid(cols=50, rows=50, cell_size=8)
    colors = Palette.ocean()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        size = cell._brightness * 7

        # Map brightness to color gradient
        if cell._brightness > 0.7:
            color = colors.accent
        elif cell._brightness > 0.4:
            color = colors.primary
        else:
            color = colors.secondary

        if size > 0.5:
            cell.add_dot(radius=size, color=color)

    save_svg("07_gradient_halftone.svg", scene)


def image_08_overlapping_halftone():
    """Overlapping halftone dots for organic feel."""
    scene = Scene.with_grid(cols=40, rows=40, cell_size=10)
    scene.background = "white"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Intentionally large dots to create overlap
        size = (1 - cell._brightness) * 12

        if size > 0.5:
            cell.add_dot(radius=size, color="black")

    save_svg("08_overlapping_halftone.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 02: Halftone Effects...")

    image_01_basic_halftone()
    image_02_color_halftone()
    image_03_cmyk_style()
    image_04_threshold_halftone()
    image_05_dual_color()
    image_06_newspaper_style()
    image_07_gradient_halftone()
    image_08_overlapping_halftone()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
