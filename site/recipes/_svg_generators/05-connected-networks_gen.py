"""SVG Generator for Recipe: Connected Networks."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette, Connection
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/05-connected-networks')
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


def image_01_basic_network():
    """Basic network connecting neighboring dots."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = {}
    for cell in scene.grid:
        if cell._brightness > 0.4:
            dot = cell.add_dot(
                radius=2 + cell._brightness * 3,
                color=colors.primary,
                z_index=10
            )
            dots[(cell.row, cell.col)] = dot

    # Create connections to right and bottom neighbors
    for cell in scene.grid:
        if (cell.row, cell.col) not in dots:
            continue

        dot1 = dots[(cell.row, cell.col)]

        # Connect to right neighbor
        if cell.right and (cell.right.row, cell.right.col) in dots:
            dot2 = dots[(cell.right.row, cell.right.col)]
            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5, "z_index": 0}
            )
            scene.add(connection)

        # Connect to bottom neighbor
        if cell.below and (cell.below.row, cell.below.col) in dots:
            dot2 = dots[(cell.below.row, cell.below.col)]
            connection = Connection(
                start=dot1,
                end=dot2,
                style={"color": colors.line, "width": 0.5, "z_index": 0}
            )
            scene.add(connection)

    save_svg("01_basic_network.svg", scene)


def image_02_distance_based():
    """Connect dots within distance threshold."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = []
    for cell in scene.grid:
        if cell._brightness > 0.5:
            dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
            dots.append((dot, cell))

    # Connect nearby dots
    max_distance = 3  # cells

    for i, (dot1, cell1) in enumerate(dots):
        for dot2, cell2 in dots[i+1:]:
            dr = cell1.row - cell2.row
            dc = cell1.col - cell2.col
            distance = math.sqrt(dr*dr + dc*dc)

            if distance <= max_distance:
                connection = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.line, "width": 1, "z_index": 0}
                )
                scene.add(connection)

    save_svg("02_distance_based.svg", scene)


def image_03_radial_hub():
    """All dots connect to central hub."""
    scene = Scene.with_grid(cols=20, rows=20, cell_size=20)
    colors = Palette.sunset()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Central hub
    center = scene.grid[scene.grid.rows // 2, scene.grid.cols // 2]
    hub_dot = center.add_dot(radius=5, color=colors.accent, z_index=10)

    # Outer dots
    for cell in scene.grid:
        if cell == center:
            continue

        if cell._brightness > 0.6:
            outer_dot = cell.add_dot(radius=2, color=colors.primary, z_index=10)

            connection = Connection(
                start=hub_dot,
                end=outer_dot,
                style={"color": colors.line, "width": 0.5, "z_index": 0}
            )
            scene.add(connection)

    save_svg("03_radial_hub.svg", scene)


def image_04_weighted_connections():
    """Line width based on brightness."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = {}
    for cell in scene.grid:
        if cell._brightness > 0.4:
            dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
            dots[(cell.row, cell.col)] = (dot, cell)

    # Create weighted connections
    for (row, col), (dot1, cell1) in dots.items():
        # Connect to right
        if cell1.right and (cell1.right.row, cell1.right.col) in dots:
            dot2, cell2 = dots[(cell1.right.row, cell1.right.col)]

            # Width based on average brightness
            avg_brightness = (cell1._brightness + cell2._brightness) / 2
            width = 0.5 + avg_brightness * 2

            connection = Connection(
                start=dot1,
                end=dot2,
                style={"width": width, "color": colors.line, "z_index": 0}
            )
            scene.add(connection)

    save_svg("04_weighted_connections.svg", scene)


def image_05_diagonal_connections():
    """Include diagonal connections."""
    scene = Scene.with_grid(cols=12, rows=10, cell_size=30)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = {}
    for cell in scene.grid:
        if cell._brightness > 0.5:
            dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
            dots[(cell.row, cell.col)] = (dot, cell)

    # Connect to all 8 neighbors
    for (row, col), (dot1, cell1) in dots.items():
        neighbors = [
            cell1.right, cell1.below,
            cell1.below_right, cell1.below_left
        ]

        for neighbor in neighbors:
            if neighbor and (neighbor.row, neighbor.col) in dots:
                dot2, cell2 = dots[(neighbor.row, neighbor.col)]

                connection = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.line, "width": 0.5, "z_index": 0}
                )
                scene.add(connection)

    save_svg("05_diagonal_connections.svg", scene)


def image_06_similarity_based():
    """Connect dots with similar brightness."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.sunset()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = {}
    for cell in scene.grid:
        if cell._brightness > 0.3:
            dot = cell.add_dot(
                radius=2 + cell._brightness * 3,
                color=colors.primary,
                z_index=10
            )
            dots[(cell.row, cell.col)] = (dot, cell)

    # Connect similar brightness neighbors
    for (row, col), (dot1, cell1) in dots.items():
        # Check right neighbor
        if cell1.right and (cell1.right.row, cell1.right.col) in dots:
            dot2, cell2 = dots[(cell1.right.row, cell1.right.col)]

            # Only connect if similar brightness
            if abs(cell1._brightness - cell2._brightness) < 0.2:
                connection = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.line, "width": 1, "z_index": 0}
                )
                scene.add(connection)

    save_svg("06_similarity_based.svg", scene)


def image_07_multi_layer():
    """Multiple connection layers."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=25)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots
    dots = {}
    for cell in scene.grid:
        if cell._brightness > 0.3:
            dot = cell.add_dot(radius=3, color=colors.primary, z_index=10)
            dots[(cell.row, cell.col)] = (dot, cell)

    # Two types of connections
    for (row, col), (dot1, cell1) in dots.items():
        if cell1.right and (cell1.right.row, cell1.right.col) in dots:
            dot2, cell2 = dots[(cell1.right.row, cell1.right.col)]

            # Strong connection (high brightness)
            if cell1._brightness > 0.7 and cell2._brightness > 0.7:
                conn = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.accent, "width": 2, "z_index": 5}
                )
                scene.add(conn)
            # Weak connection
            elif cell1._brightness > 0.4:
                conn = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.line, "width": 0.5, "z_index": 0}
                )
                scene.add(conn)

    save_svg("07_multi_layer.svg", scene)


def image_08_sparse_network():
    """Sparse network - fewer connections."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Create dots (sparse)
    dots = []
    for cell in scene.grid:
        if cell._brightness > 0.7:  # Only very bright
            dot = cell.add_dot(radius=4, color=colors.primary, z_index=10)
            dots.append((dot, cell))

    # Connect only very close dots
    max_distance = 2

    for i, (dot1, cell1) in enumerate(dots):
        for dot2, cell2 in dots[i+1:]:
            dr = cell1.row - cell2.row
            dc = cell1.col - cell2.col
            distance = math.sqrt(dr*dr + dc*dc)

            if distance <= max_distance:
                connection = Connection(
                    start=dot1,
                    end=dot2,
                    style={"color": colors.line, "width": 1, "z_index": 0}
                )
                scene.add(connection)

    save_svg("08_sparse_network.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 05: Connected Networks...")

    image_01_basic_network()
    image_02_distance_based()
    image_03_radial_hub()
    image_04_weighted_connections()
    image_05_diagonal_connections()
    image_06_similarity_based()
    image_07_multi_layer()
    image_08_sparse_network()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
