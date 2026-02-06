"""SVG Generator for Recipe: Geometric Patterns."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette, shapes
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/04-geometric-patterns')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def image_01_hexagon_grid():
    """Grid of hexagons."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        cell.add_polygon(shapes.hexagon(), fill=colors.primary)

    save_svg("01_hexagon_grid.svg", scene)


def image_02_alternating_shapes():
    """Checkerboard of hexagons and stars."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        if (cell.row + cell.col) % 2 == 0:
            cell.add_polygon(shapes.hexagon(), fill=colors.primary)
        else:
            cell.add_polygon(shapes.star(5), fill=colors.secondary)

    save_svg("02_alternating_shapes.svg", scene)


def image_03_concentric_rings():
    """Concentric rings with different shapes."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = int(math.sqrt(dr*dr + dc*dc))

        # Different shape per ring
        if distance % 3 == 0:
            cell.add_polygon(shapes.hexagon(), fill=colors.primary)
        elif distance % 3 == 1:
            cell.add_polygon(shapes.triangle(), fill=colors.secondary)
        else:
            cell.add_polygon(shapes.diamond(), fill=colors.accent)

    save_svg("03_concentric_rings.svg", scene)


def image_04_diagonal_stripes():
    """Diagonal stripes with shape variations."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        diagonal = (cell.row + cell.col) % 4

        if diagonal == 0:
            cell.add_polygon(shapes.square(), fill=colors.primary)
        elif diagonal == 1:
            cell.add_polygon(shapes.hexagon(), fill=colors.secondary)
        elif diagonal == 2:
            cell.add_polygon(shapes.star(6), fill=colors.accent)
        # diagonal == 3: leave empty

    save_svg("04_diagonal_stripes.svg", scene)


def image_05_rotating_shapes():
    """Shapes with position-based rotation."""
    scene = Scene.with_grid(cols=15, rows=15, cell_size=25)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.hexagon(), fill=colors.primary)

        # Rotate based on position
        angle = (cell.row * cell.col) * 15
        poly.rotate(angle)

    save_svg("05_rotating_shapes.svg", scene)


def image_06_star_variations():
    """Different star point counts."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    for cell in scene.grid:
        # Vary star points
        points = 5 + (cell.row % 4)  # 5, 6, 7, or 8 points

        cell.add_polygon(
            shapes.star(points=points, inner_ratio=0.4),
            fill=colors.primary
        )

    save_svg("06_star_variations.svg", scene)


def image_07_squircle_pattern():
    """iOS icon-style squircles."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Distance-based color
        dr = cell.row - 6
        dc = cell.col - 7.5
        distance = math.sqrt(dr*dr + dc*dc)

        if distance < 4:
            color = colors.primary
        elif distance < 8:
            color = colors.secondary
        else:
            color = colors.accent

        poly = cell.add_polygon(shapes.squircle(n=4), fill=color)

        # Rotate based on distance
        angle = distance * 10
        poly.rotate(angle)

    save_svg("07_squircle_pattern.svg", scene)


def image_08_nested_shapes():
    """Nested shapes in each cell."""
    scene = Scene.with_grid(cols=12, rows=10, cell_size=30)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Large background hexagon
        cell.add_polygon(
            shapes.hexagon(size=1.0),
            fill=colors.primary,
            z_index=0
        )

        # Smaller foreground star
        cell.add_polygon(
            shapes.star(5),
            fill=colors.accent,
            z_index=10
        )

    save_svg("08_nested_shapes.svg", scene)


def image_09_size_variations():
    """Shapes with varying sizes."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    center_row = scene.grid.rows // 2
    center_col = scene.grid.cols // 2

    for cell in scene.grid:
        # Distance from center
        dr = cell.row - center_row
        dc = cell.col - center_col
        distance = math.sqrt(dr*dr + dc*dc)
        max_distance = math.sqrt(center_row**2 + center_col**2)

        # Size decreases with distance
        size = 1.0 - (distance / max_distance) * 0.6

        poly = cell.add_polygon(
            shapes.hexagon(size=size),
            fill=colors.primary
        )

    save_svg("09_size_variations.svg", scene)


def image_10_triangle_tessellation():
    """Triangle tessellation pattern."""
    scene = Scene.with_grid(cols=25, rows=20, cell_size=15)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        poly = cell.add_polygon(shapes.triangle(), fill=colors.primary)

        # Rotate triangles to create tessellation
        if (cell.row + cell.col) % 2 == 0:
            poly.rotate(0)
        else:
            poly.rotate(180)

    save_svg("10_triangle_tessellation.svg", scene)


def image_11_diamond_pattern():
    """Diamond/rhombus pattern."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    for cell in scene.grid:
        # Checkerboard of diamonds
        if (cell.row + cell.col) % 2 == 0:
            cell.add_polygon(shapes.diamond(), fill=colors.primary)

    save_svg("11_diamond_pattern.svg", scene)


def image_12_mixed_geometry():
    """Mix of all geometric shapes."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.midnight()
    scene.background = colors.background

    shape_types = [
        shapes.triangle(),
        shapes.square(),
        shapes.hexagon(),
        shapes.diamond(),
        shapes.star(5),
    ]

    for cell in scene.grid:
        # Choose shape based on position pattern
        shape_idx = (cell.row + cell.col) % len(shape_types)
        shape = shape_types[shape_idx]

        # Color based on column
        if cell.col < 7:
            color = colors.primary
        elif cell.col < 14:
            color = colors.secondary
        else:
            color = colors.accent

        cell.add_polygon(shape, fill=color)

    save_svg("12_mixed_geometry.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 04: Geometric Patterns...")

    image_01_hexagon_grid()
    image_02_alternating_shapes()
    image_03_concentric_rings()
    image_04_diagonal_stripes()
    image_05_rotating_shapes()
    image_06_star_variations()
    image_07_squircle_pattern()
    image_08_nested_shapes()
    image_09_size_variations()
    image_10_triangle_tessellation()
    image_11_diamond_pattern()
    image_12_mixed_geometry()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
