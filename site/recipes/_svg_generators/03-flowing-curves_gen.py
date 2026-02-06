"""SVG Generator for Recipe: Flowing Curves."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/03-flowing-curves')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def create_synthetic_brightness_grid(scene):
    """Create synthetic brightness values."""
    for cell in scene.grid:
        # Create wave-like brightness pattern
        wave_x = math.sin(cell.col * 0.3) * 0.5 + 0.5
        wave_y = math.cos(cell.row * 0.3) * 0.5 + 0.5
        brightness = (wave_x + wave_y) / 2
        cell._brightness = brightness


def image_01_horizontal_flow():
    """Horizontal flowing curves with varying curvature."""
    scene = Scene.with_grid(cols=30, rows=25, cell_size=12)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Curvature varies based on column position
        curvature = (cell.col / scene.grid.cols - 0.5) * 2  # Range: -1 to 1

        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=colors.line,
            width=1
        )

    save_svg("01_horizontal_flow.svg", scene)


def image_02_vertical_flow():
    """Vertical flowing curves."""
    scene = Scene.with_grid(cols=25, rows=30, cell_size=12)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        # Curvature varies vertically
        curvature = (cell.row / scene.grid.rows - 0.5) * 2

        cell.add_curve(
            start="top",
            end="bottom",
            curvature=curvature,
            color=colors.line,
            width=1
        )

    save_svg("02_vertical_flow.svg", scene)


def image_03_brightness_driven():
    """Curves with brightness-driven curvature."""
    scene = Scene.with_grid(cols=30, rows=25, cell_size=12)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Only draw in certain brightness range
        if 0.3 < cell._brightness < 0.7:
            # Curvature based on brightness
            curvature = cell._brightness - 0.5  # Range: -0.2 to 0.2

            cell.add_curve(
                start="left",
                end="right",
                curvature=curvature,
                color=colors.line,
                width=1
            )

    save_svg("03_brightness_driven.svg", scene)


def image_04_wave_pattern():
    """Sine wave curvature pattern."""
    scene = Scene.with_grid(cols=30, rows=25, cell_size=12)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Sine wave curvature
        phase = cell.col / scene.grid.cols * math.pi * 2
        curvature = math.sin(phase)

        cell.add_curve(
            start="top",
            end="bottom",
            curvature=curvature,
            color=colors.primary,
            width=1
        )

    save_svg("04_wave_pattern.svg", scene)


def image_05_radial_flow():
    """Radial flowing curves from center."""
    scene = Scene.with_grid(cols=30, rows=30, cell_size=12)
    colors = Palette.midnight()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        # Distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr*dr + dc*dc)

        # Curvature based on distance
        curvature = (distance / 10) * 0.5

        cell.add_curve(
            start="center",
            end="top_right",
            curvature=curvature,
            color=colors.line,
            width=1,
        )

    save_svg("05_radial_flow.svg", scene)


def image_06_dual_direction():
    """Horizontal and vertical curves layered."""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=12)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Horizontal curves
        curv_h = (cell.col / scene.grid.cols - 0.5) * 1.5

        cell.add_curve(
            start="left",
            end="right",
            curvature=curv_h,
            color=colors.primary,
            width=0.8,
            z_index=0
        )

        # Vertical curves
        curv_v = (cell.row / scene.grid.rows - 0.5) * 1.5

        cell.add_curve(
            start="top",
            end="bottom",
            curvature=curv_v,
            color=colors.secondary,
            width=0.8,
            z_index=1,
        )

    save_svg("06_dual_direction.svg", scene)


def image_07_varying_width():
    """Curves with varying line width."""
    scene = Scene.with_grid(cols=30, rows=25, cell_size=12)
    colors = Palette.sunset()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Width based on brightness
        width = 0.5 + cell._brightness * 2  # 0.5 to 2.5

        curvature = (cell.col / scene.grid.cols - 0.5) * 2

        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=colors.primary,
            width=width
        )

    save_svg("07_varying_width.svg", scene)


def image_08_diagonal_curves():
    """Diagonal flowing curves."""
    scene = Scene.with_grid(cols=25, rows=25, cell_size=12)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        # Diagonal pattern
        diagonal = (cell.row + cell.col) / (scene.grid.rows + scene.grid.cols)
        curvature = (diagonal - 0.5) * 2

        cell.add_curve(
            start="bottom_left",
            end="top_right",
            curvature=curvature,
            color=colors.line,
            width=1
        )

    save_svg("08_diagonal_curves.svg", scene)


def image_09_curves_with_dots():
    """Curves with dots flowing along them."""
    scene = Scene.with_grid(cols=25, rows=20, cell_size=14)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        if 0.3 < cell._brightness < 0.7:
            # Horizontal curve
            curvature_h = (cell.col / scene.grid.cols - 0.5) * 2

            curve = cell.add_curve(
                start="left",
                end="right",
                curvature=curvature_h,
                color=colors.line,
                width=1,
                z_index=0
            )

            # Add dot along curve
            cell.add_dot(
                at=(0.5, 0.5),  # Center of cell approximates curve middle
                radius=2,
                color=colors.accent,
                z_index=10
            )

    save_svg("09_curves_with_dots.svg", scene)


def image_10_alternating_curves():
    """Alternating curve directions."""
    scene = Scene.with_grid(cols=30, rows=25, cell_size=12)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Alternate direction based on row
        if cell.row % 2 == 0:
            curvature = 0.5
            color = colors.primary
        else:
            curvature = -0.5
            color = colors.secondary

        cell.add_curve(
            start="left",
            end="right",
            curvature=curvature,
            color=color,
            width=1
        )

    save_svg("10_alternating_curves.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 03: Flowing Curves...")

    image_01_horizontal_flow()
    image_02_vertical_flow()
    image_03_brightness_driven()
    image_04_wave_pattern()
    image_05_radial_flow()
    image_06_dual_direction()
    image_07_varying_width()
    image_08_diagonal_curves()
    image_09_curves_with_dots()
    image_10_alternating_curves()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
