"""
SVG Generator for Curves Example
Demonstrates quadratic Bezier curves with parametric positioning
"""

import math

def quadratic_bezier_point(t, p0, p1, p2):
    """Calculate point on quadratic Bezier curve at parameter t."""
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return (x, y)

def generate_svg(output_path: str, number: int) -> None:
    """Generate curves example SVG."""
    grid_size = 30
    cell_size = 20
    width = grid_size * cell_size
    height = grid_size * cell_size

    # Ocean palette
    background = "#1a1a2e"
    line_color = "#4ecca3"
    accent = "#ee4266"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Generate curves with dots positioned along them
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size

            # Calculate brightness (sine wave pattern)
            brightness = (math.sin(col * 0.15) * math.cos(row * 0.15) + 1) / 2

            # Only draw in medium brightness range
            if 0.3 < brightness < 0.7:
                # Curve from bottom-left to top-right
                p0 = (x, y + cell_size)  # start (bottom-left)
                p2 = (x + cell_size, y)  # end (top-right)

                # Control point for curvature=0.5
                curvature = 0.5
                mid_x = (p0[0] + p2[0]) / 2
                mid_y = (p0[1] + p2[1]) / 2
                perp_x = -(p2[1] - p0[1])
                perp_y = (p2[0] - p0[0])
                length = math.sqrt(perp_x**2 + perp_y**2)
                if length > 0:
                    perp_x /= length
                    perp_y /= length
                offset = cell_size * curvature
                p1 = (mid_x + perp_x * offset, mid_y + perp_y * offset)

                # Draw curve
                svg_lines.append(
                    f'  <path d="M {p0[0]},{p0[1]} Q {p1[0]},{p1[1]} {p2[0]},{p2[1]}" '
                    f'stroke="{line_color}" stroke-width="1" fill="none" opacity="0.5"/>'
                )

                # Position dot along curve based on brightness
                dot_pos = quadratic_bezier_point(brightness, p0, p1, p2)
                svg_lines.append(
                    f'  <circle cx="{dot_pos[0]:.1f}" cy="{dot_pos[1]:.1f}" '
                    f'r="2" fill="{accent}"/>'
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
            '_images', 'curves'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_flowing_curves.svg',
        '02_varying_curvature.svg',
        '03_multiple_dots.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
