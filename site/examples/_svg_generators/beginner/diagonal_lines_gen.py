"""
SVG Generator for Diagonal Lines Example
Demonstrates parametric positioning along diagonal lines
"""

def generate_svg(output_path: str, number: int) -> None:
    """Generate diagonal lines example SVG."""
    import math

    grid_size = 30
    cell_size = 20
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

    # Generate diagonal lines with sliding dots
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size

            # Calculate brightness (wave pattern)
            brightness = (math.sin(col * 0.2) * math.cos(row * 0.2) + 1) / 2

            # Diagonal line coordinates (bottom-left to top-right)
            x1 = x
            y1 = y + cell_size
            x2 = x + cell_size
            y2 = y

            # Draw line
            svg_lines.append(
                f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="{line_color}" stroke-width="0.5" opacity="0.3"/>'
            )

            # Position dot along line based on brightness (t = brightness)
            dot_x = x1 + brightness * (x2 - x1)
            dot_y = y1 + brightness * (y2 - y1)

            svg_lines.append(
                f'  <circle cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="3" fill="{primary}"/>'
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
            '_images', 'diagonal-lines'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_sliding_dots.svg',
        '02_brightness_driven.svg',
        '03_inverted_position.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
