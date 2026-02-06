"""
SVG Generator for Polygon Gallery Example
Showcases all built-in polygon shapes
"""

import math

def triangle(size=1.0, center=(0.5, 0.5)):
    """Equilateral triangle pointing up."""
    cx, cy = center
    h = size * 0.866  # height factor
    return [
        (cx, cy - h * 0.5),
        (cx + size * 0.5, cy + h * 0.5),
        (cx - size * 0.5, cy + h * 0.5)
    ]

def square(size=1.0, center=(0.5, 0.5)):
    """Square rotated 45 degrees."""
    cx, cy = center
    d = size * 0.5 * 1.414
    return [
        (cx, cy - d),
        (cx + d, cy),
        (cx, cy + d),
        (cx - d, cy)
    ]

def diamond(size=1.0, center=(0.5, 0.5)):
    """Diamond aligned to axes."""
    cx, cy = center
    return [
        (cx, cy - size * 0.5),
        (cx + size * 0.5, cy),
        (cx, cy + size * 0.5),
        (cx - size * 0.5, cy)
    ]

def hexagon(size=1.0, center=(0.5, 0.5)):
    """Regular hexagon."""
    cx, cy = center
    points = []
    for i in range(6):
        angle = i * math.pi / 3
        x = cx + size * 0.5 * math.cos(angle)
        y = cy + size * 0.5 * math.sin(angle)
        points.append((x, y))
    return points

def star(points=5, size=1.0, inner_ratio=0.4, center=(0.5, 0.5)):
    """Multi-pointed star."""
    cx, cy = center
    vertices = []
    for i in range(points * 2):
        angle = i * math.pi / points - math.pi / 2
        r = size * 0.5 if i % 2 == 0 else size * 0.5 * inner_ratio
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        vertices.append((x, y))
    return vertices

def regular_polygon(n_sides, size=1.0, center=(0.5, 0.5)):
    """Regular n-sided polygon."""
    cx, cy = center
    points = []
    for i in range(n_sides):
        angle = i * 2 * math.pi / n_sides - math.pi / 2
        x = cx + size * 0.5 * math.cos(angle)
        y = cy + size * 0.5 * math.sin(angle)
        points.append((x, y))
    return points

def generate_svg(output_path: str, number: int) -> None:
    """Generate polygon gallery SVG."""
    cols = 8
    rows = 6
    cell_size = 40
    width = cols * cell_size
    height = rows * cell_size

    # Pastel palette
    background = "#1a1a2e"
    primary = "#4ecca3"
    secondary = "#ee4266"
    accent = "#ffd23f"
    line_color = "#64ffda"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Define shapes gallery
    shapes_gallery = [
        (triangle(), "Triangle", primary),
        (square(), "Square", secondary),
        (diamond(), "Diamond", accent),
        (hexagon(), "Hexagon", line_color),
        (star(points=5), "Star 5", primary),
        (star(points=6), "Star 6", secondary),
        (star(points=8), "Star 8", accent),
        (regular_polygon(5), "Pentagon", line_color),
        (regular_polygon(7), "Heptagon", primary),
        (regular_polygon(8), "Octagon", secondary),
    ]

    # Place shapes in grid
    for i, (shape_data, name, color) in enumerate(shapes_gallery):
        row = i // cols
        col = i % cols

        if row >= rows:
            break

        # Cell position
        cell_x = col * cell_size
        cell_y = row * cell_size

        # Scale and translate shape points
        points_str = []
        for x, y in shape_data:
            px = cell_x + x * cell_size
            py = cell_y + y * cell_size
            points_str.append(f"{px:.1f},{py:.1f}")

        svg_lines.append(
            f'  <polygon points="{" ".join(points_str)}" '
            f'fill="{color}" stroke="{line_color}" stroke-width="0.5" opacity="0.8"/>'
        )

    svg_lines.append('</svg>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))


if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            '_images', 'polygon-gallery'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_basic_shapes.svg',
        '02_stars.svg',
        '03_regular_polygons.svg',
        '04_all_shapes.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
