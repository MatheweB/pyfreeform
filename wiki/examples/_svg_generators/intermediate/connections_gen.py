"""
SVG Generator for Connections Example
Demonstrates network visualization with distance-based connections
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate connections example SVG."""
    grid_size = 30
    cell_size = 15
    width = grid_size * cell_size
    height = grid_size * cell_size

    # Midnight palette
    background = "#1a1a2e"
    line_color = "#4ecca3"
    primary = "#ee4266"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Generate dots (nodes) with synthetic brightness
    max_distance = 3
    dots = []

    for row in range(grid_size):
        for col in range(grid_size):
            # Calculate brightness
            center_x = grid_size / 2
            center_y = grid_size / 2
            distance = math.sqrt((col - center_x)**2 + (row - center_y)**2)
            max_dist = math.sqrt(center_x**2 + center_y**2)
            brightness = (math.sin(distance * 0.5) + 1) / 2

            # Only create dots for bright cells
            if brightness > 0.4:
                x = col * cell_size + cell_size / 2
                y = row * cell_size + cell_size / 2
                radius = 2 + brightness * 3
                dots.append((x, y, radius, row, col, brightness))

    # Draw connections first (behind dots)
    for i, (x1, y1, r1, row1, col1, b1) in enumerate(dots):
        for x2, y2, r2, row2, col2, b2 in dots[i+1:i+4]:  # Connect to next 3
            # Calculate distance in grid cells
            dr = row1 - row2
            dc = col1 - col2
            distance = math.sqrt(dr*dr + dc*dc)

            if distance <= max_distance:
                # Fade opacity with distance
                opacity = (1 - distance / max_distance) * 0.5

                svg_lines.append(
                    f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{line_color}" stroke-width="0.5" opacity="{opacity:.2f}"/>'
                )

    # Draw dots on top
    for x, y, radius, row, col, brightness in dots:
        svg_lines.append(
            f'  <circle cx="{x}" cy="{y}" r="{radius:.1f}" fill="{primary}"/>'
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
            '_images', 'connections'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_network.svg',
        '02_distance_fade.svg',
        '03_hub_spoke.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
