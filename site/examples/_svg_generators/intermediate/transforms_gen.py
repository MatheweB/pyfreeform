"""
SVG Generator for Transforms Example
Demonstrates rotation and scaling of polygons
"""

import math

def hexagon_points(cx, cy, radius):
    """Generate hexagon points."""
    points = []
    for i in range(6):
        angle = i * math.pi / 3
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

def generate_svg(output_path: str, number: int) -> None:
    """Generate transforms example SVG."""
    cols = 20
    rows = 20
    cell_size = 25
    width = cols * cell_size
    height = rows * cell_size

    # Sunset palette
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

    # Generate rotating hexagons
    for row in range(rows):
        for col in range(cols):
            cx = col * cell_size + cell_size / 2
            cy = row * cell_size + cell_size / 2

            # Rotation based on grid position
            angle = (row + col) * 15  # degrees

            # Color based on position
            colors_list = [primary, secondary, accent, line_color]
            color = colors_list[(row + col) % len(colors_list)]

            # Generate hexagon points
            hex_points = hexagon_points(0, 0, 10)
            points_str = ' '.join([f"{x:.1f},{y:.1f}" for x, y in hex_points])

            # Use SVG transform for rotation
            svg_lines.append(
                f'  <g transform="translate({cx},{cy}) rotate({angle})">'
            )
            svg_lines.append(
                f'    <polygon points="{points_str}" fill="{color}" opacity="0.7"/>'
            )
            svg_lines.append('  </g>')

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
            '_images', 'transforms'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_rotating_hexagons.svg',
        '02_radial_rotation.svg',
        '03_spiral_pattern.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
