"""
SVG Generator for Quick Start Example
Simple dot art from synthetic brightness data
"""

def generate_svg(output_path: str, number: int) -> None:
    """Generate quick-start example SVG."""
    # Create synthetic "image" data
    grid_size = 30
    cell_size = 12
    width = grid_size * cell_size
    height = grid_size * cell_size

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="#1a1a2e"/>',
        ''
    ]

    # Generate dot pattern with synthetic brightness
    import math
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size + cell_size / 2
            y = row * cell_size + cell_size / 2

            # Create radial gradient pattern
            center_x = grid_size / 2
            center_y = grid_size / 2
            distance = math.sqrt((col - center_x)**2 + (row - center_y)**2)
            max_distance = math.sqrt(center_x**2 + center_y**2)
            brightness = 1 - (distance / max_distance)

            # Color based on brightness
            color_val = int(brightness * 255)
            color = f"#{color_val:02x}{color_val:02x}{color_val:02x}"

            # Dot size: fixed at 4
            radius = 4

            svg_lines.append(f'  <circle cx="{x}" cy="{y}" r="{radius}" fill="{color}"/>')

    svg_lines.append('</svg>')

    with open(output_path, 'w') as f:
        f.write('\n'.join(svg_lines))


if __name__ == '__main__':
    import sys
    import os

    # Get output directory from command line or use default
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            '_images', 'quick-start'
        )

    os.makedirs(output_dir, exist_ok=True)

    # Generate single example
    output_path = os.path.join(output_dir, '01_simple_dot_art.svg')
    generate_svg(output_path, 1)
    print(f"Generated: {output_path}")
