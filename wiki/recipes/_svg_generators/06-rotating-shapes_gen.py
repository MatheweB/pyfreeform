"""SVG Generator for Recipe: Rotating Shapes."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette, shapes
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/06-rotating-shapes')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def create_synthetic_brightness_grid(scene):
    """Create synthetic brightness values."""
    for cell in scene.grid:
        # Create pattern
        dx = cell.col - scene.grid.cols / 2
        dy = cell.row - scene.grid.rows / 2
        distance = math.sqrt(dx*dx + dy*dy)
        max_distance = math.sqrt((scene.grid.cols/2)**2 + (scene.grid.rows/2)**2)

        brightness = 1 - (distance / max_distance)
        brightness = max(0, min(1, brightness))

        cell._brightness = brightness


def image_01_linear_progression():
    """Rotation increases steadily across grid."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Rotation increases left to right, top to bottom
        angle = (cell.row * scene.grid.cols + cell.col) * 5
        poly.rotate(angle)

    save_svg("01_linear_progression.svg", scene)


def image_02_radial_pattern():
    """Shapes point toward/away from center."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.triangle(), fill=colors.primary)

        # Calculate angle from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        angle = math.degrees(math.atan2(dr, dc))

        poly.rotate(angle)

    save_svg("02_radial_pattern.svg", scene)


def image_03_spiral_pattern():
    """Vortex/spiral rotation effect."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr*dr + dc*dc)

        # Angle from center
        angle = math.degrees(math.atan2(dr, dc))

        # Rotation combines angle + distance
        rotation = angle + distance * 30
        poly.rotate(rotation)

    save_svg("03_spiral_pattern.svg", scene)


def image_04_brightness_driven():
    """Rotation based on brightness."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        if cell._brightness > 0.3:
            # Choose shape based on brightness
            if cell._brightness > 0.7:
                shape = shapes.star(5)
                color = colors.accent
            elif cell._brightness > 0.5:
                shape = shapes.hexagon()
                color = colors.primary
            else:
                shape = shapes.diamond()
                color = colors.secondary

            poly = cell.add_polygon(shape, fill=color)

            # Bright cells rotate more
            angle = cell._brightness * 360
            poly.rotate(angle)

    save_svg("04_brightness_driven.svg", scene)


def image_05_diagonal_rotation():
    """Rotation based on diagonal position."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Diagonal-based rotation
        angle = (cell.row + cell.col) * 15
        poly.rotate(angle)

    save_svg("05_diagonal_rotation.svg", scene)


def image_06_wave_rotation():
    """Sine wave rotation pattern."""
    scene = Scene.with_grid(cols=25, rows=15, cell_size=18)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.star(5), fill=colors.primary)

        # Sine wave rotation
        phase = cell.col / scene.grid.cols * math.pi * 2
        angle = math.sin(phase) * 180

        poly.rotate(angle)

    save_svg("06_wave_rotation.svg", scene)


def image_07_rotating_ellipses():
    """Ellipses show rotation dramatically."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Create elongated ellipse
        ellipse = cell.add_ellipse(
            rx=12,
            ry=6,
            fill=colors.primary
        )

        # Rotation based on position
        angle = (cell.row + cell.col) * 20
        ellipse.rotation = angle

    save_svg("07_rotating_ellipses.svg", scene)


def image_08_multi_shape_rotation():
    """Different shapes with different rotation speeds."""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=25)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        # Background shape - slow rotation
        bg = cell.add_polygon(
            shapes.hexagon(size=1.0),
            fill=colors.primary,
            z_index=0
        )
        bg.rotate((cell.row + cell.col) * 10)

        # Foreground shape - fast rotation
        fg = cell.add_polygon(
            shapes.star(5),
            fill=colors.accent,
            z_index=10
        )
        fg.rotate((cell.row + cell.col) * 45)

    save_svg("08_multi_shape_rotation.svg", scene)


def image_09_alternating_rotation():
    """Alternating rotation directions."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Alternate rotation direction
        if (cell.row + cell.col) % 2 == 0:
            angle = (cell.row * 20 + cell.col * 15) % 360
        else:
            angle = -(cell.row * 20 + cell.col * 15) % 360

        poly.rotate(angle)

    save_svg("09_alternating_rotation.svg", scene)


def image_10_stepped_rotation():
    """Stepped rotation increments."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.star(6), fill=colors.primary)

        # Only 4 rotation states: 0, 90, 180, 270
        step = ((cell.row + cell.col) % 4) * 90
        poly.rotate(step)

    save_svg("10_stepped_rotation.svg", scene)


def image_11_concentric_rotation():
    """Rotation based on distance rings."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = int(math.sqrt(dr*dr + dc*dc))

        # Rotation per ring
        angle = distance * 30
        poly.rotate(angle)

    save_svg("11_concentric_rotation.svg", scene)


def image_12_complex_pattern():
    """Complex rotation combining multiple factors."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        if cell._brightness > 0.3:
            poly = cell.add_polygon(shapes.star(5), fill=colors.primary)

            # Combine multiple rotation factors
            dr = cell.row - center_row
            dc = cell.col - center_col
            distance = math.sqrt(dr*dr + dc*dc)

            # Base rotation from position
            base = (cell.row + cell.col) * 15

            # Add distance factor
            distance_factor = distance * 10

            # Add brightness factor
            brightness_factor = cell._brightness * 45

            angle = (base + distance_factor + brightness_factor) % 360
            poly.rotate(angle)

    save_svg("12_complex_pattern.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 06: Rotating Shapes...")

    image_01_linear_progression()
    image_02_radial_pattern()
    image_03_spiral_pattern()
    image_04_brightness_driven()
    image_05_diagonal_rotation()
    image_06_wave_rotation()
    image_07_rotating_ellipses()
    image_08_multi_shape_rotation()
    image_09_alternating_rotation()
    image_10_stepped_rotation()
    image_11_concentric_rotation()
    image_12_complex_pattern()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
