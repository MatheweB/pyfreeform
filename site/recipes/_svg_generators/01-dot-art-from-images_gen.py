"""SVG Generator for Recipe: Dot Art from Images."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette, Dot
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/01-dot-art-from-images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def create_synthetic_brightness_grid(scene):
    """Create synthetic brightness values simulating an image."""
    for cell in scene.grid:
        # Create a gradient pattern
        dx = cell.col - scene.grid.cols / 2
        dy = cell.row - scene.grid.rows / 2
        distance = math.sqrt(dx*dx + dy*dy)
        max_distance = math.sqrt((scene.grid.cols/2)**2 + (scene.grid.rows/2)**2)

        # Simulate brightness: bright in center, dark at edges
        brightness = 1 - (distance / max_distance)
        brightness = max(0, min(1, brightness))

        # Also add some wave pattern
        wave = (math.sin(cell.col * 0.5) + math.sin(cell.row * 0.5)) / 4 + 0.5
        brightness = (brightness * 0.7 + wave * 0.3)

        # Store as custom attribute
        cell._brightness = brightness

        # Calculate a color based on brightness
        gray = int(brightness * 255)
        cell._color = f"#{gray:02x}{gray:02x}{gray:02x}"


def image_01_basic_pattern():
    """Basic dot art pattern - uniform dots on grid."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    scene.background = "#0a0a0a"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        cell.add_dot(color=cell._color, radius=4)

    save_svg("01_basic_pattern.svg", scene)


def image_02_variable_sizing():
    """Dots with size based on brightness."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    scene.background = "#0a0a0a"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        size = 2 + cell._brightness * 8
        cell.add_dot(radius=size, color=cell._color)

    save_svg("02_variable_sizing.svg", scene)


def image_03_threshold_effect():
    """Threshold-based dot rendering."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    colors = Palette.midnight()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        if cell._brightness > 0.7:
            cell.add_dot(radius=6, color=colors.primary)
        elif cell._brightness > 0.4:
            cell.add_dot(radius=4, color=colors.secondary)
        # Below 0.4: no dot (dark areas)

    save_svg("03_threshold_effect.svg", scene)


def image_04_color_dots():
    """Color dots with brightness-based sizing."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    colors = Palette.ocean()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        size = 1 + cell._brightness * 7

        # Color based on position and brightness
        if cell._brightness > 0.6:
            color = colors.primary
        elif cell._brightness > 0.3:
            color = colors.secondary
        else:
            color = colors.accent

        cell.add_dot(radius=size, color=color)

    save_svg("04_color_dots.svg", scene)


def image_05_sparse_pattern():
    """Sparse dot pattern - only bright areas."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    colors = Palette.sunset()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Only draw dots in bright areas
        if cell._brightness > 0.5:
            size = 3 + cell._brightness * 6
            cell.add_dot(radius=size, color=colors.primary)

    save_svg("05_sparse_pattern.svg", scene)


def image_06_inverted_brightness():
    """Inverted brightness - larger dots in dark areas."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    scene.background = "#f5f5f5"

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Invert brightness for sizing
        inverted = 1 - cell._brightness
        size = 2 + inverted * 7

        # Dark dots
        cell.add_dot(radius=size, color="#1a1a1a")

    save_svg("06_inverted_brightness.svg", scene)


def image_07_dual_layer():
    """Dual layer dots - background and foreground."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    colors = Palette.midnight()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Background layer - all cells
        bg_size = 3 + cell._brightness * 4
        cell.add_dot(radius=bg_size, color=colors.line, z_index=0)

        # Foreground layer - only bright areas
        if cell._brightness > 0.6:
            fg_size = 2 + cell._brightness * 3
            cell.add_dot(radius=fg_size, color=colors.accent, z_index=10)

    save_svg("07_dual_layer.svg", scene)


def image_08_checkerboard_threshold():
    """Checkerboard pattern with threshold."""
    scene = Scene.with_grid(cols=40, rows=30, cell_size=10)
    colors = Palette.ocean()
    scene.background = colors.background

    # Simulate image brightness
    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Checkerboard logic
        if (cell.row + cell.col) % 2 == 0:
            if cell._brightness > 0.5:
                cell.add_dot(radius=6, color=colors.primary)
        else:
            if cell._brightness > 0.3:
                cell.add_dot(radius=4, color=colors.secondary)

    save_svg("08_checkerboard_threshold.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 01: Dot Art from Images...")

    image_01_basic_pattern()
    image_02_variable_sizing()
    image_03_threshold_effect()
    image_04_color_dots()
    image_05_sparse_pattern()
    image_06_inverted_brightness()
    image_07_dual_layer()
    image_08_checkerboard_threshold()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
