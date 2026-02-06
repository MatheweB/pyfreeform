"""
SVG Generator for Ellipses Example
Demonstrates rotated ellipses and parametric positioning
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate ellipses example SVG."""
    grid_size = 30
    cell_size = 15
    width = grid_size * cell_size
    height = grid_size * cell_size

    # Ocean palette
    background = "#1a1a2e"
    primary = "#4ecca3"
    accent = "#ee4266"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Calculate center
    center_row = grid_size / 2
    center_col = grid_size / 2

    # Generate radially rotating ellipses
    for row in range(grid_size):
        for col in range(grid_size):
            cx = col * cell_size + cell_size / 2
            cy = row * cell_size + cell_size / 2

            # Calculate angle from center
            dr = row - center_row
            dc = col - center_col
            distance = math.sqrt(dr*dr + dc*dc)
            angle_rad = math.atan2(dr, dc)
            angle_deg = math.degrees(angle_rad)

            # Brightness based on distance
            max_dist = math.sqrt(center_row**2 + center_col**2)
            brightness = 1 - (distance / max_dist)

            # Skip very dark cells
            if brightness < 0.2:
                continue

            # Size based on brightness
            scale = 0.3 + brightness * 0.7
            rx = 12 * scale
            ry = 6 * scale

            # Color based on brightness
            color_val = int(brightness * 255)
            color = f"#{color_val:02x}{int(color_val*0.8):02x}{int(color_val*0.6):02x}"

            # Draw rotated ellipse
            svg_lines.append(
                f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" '
                f'fill="{color}" transform="rotate({angle_deg:.1f} {cx} {cy})" opacity="0.7"/>'
            )

            # Add dot on ellipse perimeter (parametric position)
            t = brightness  # Use brightness as parameter
            angle_param = t * 2 * math.pi

            # Calculate point on rotated ellipse
            x_local = rx * math.cos(angle_param)
            y_local = ry * math.sin(angle_param)

            # Rotate the point
            angle_rad_rot = math.radians(angle_deg)
            x_rotated = x_local * math.cos(angle_rad_rot) - y_local * math.sin(angle_rad_rot)
            y_rotated = x_local * math.sin(angle_rad_rot) + y_local * math.cos(angle_rad_rot)

            dot_x = cx + x_rotated
            dot_y = cy + y_rotated

            svg_lines.append(
                f'  <circle cx="{dot_x:.1f}" cy="{dot_y:.1f}" r="2" fill="{accent}"/>'
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
            '_images', 'ellipses'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_radial_ellipses.svg',
        '02_orbital_rings.svg',
        '03_parametric_dots.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
