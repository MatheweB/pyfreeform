"""
SVG Generator for Groups Example
Demonstrates organizing entities into groups
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate groups example SVG."""
    cols = 12
    rows = 10
    cell_size = 25
    width = cols * cell_size
    height = rows * cell_size

    # Midnight palette
    background = "#1a1a2e"
    primary = "#4ecca3"
    accent = "#ee4266"
    secondary = "#ffd23f"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Example 1: Flower pattern (grouped and rotated)
    def create_flower(cx, cy, scale, rotation):
        """Create a flower pattern as a grouped set of elements."""
        flower_group = []

        # Center dot
        flower_group.append(
            f'    <circle cx="0" cy="0" r="{10*scale}" fill="{primary}" opacity="0.8"/>'
        )

        # Petals around center
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            distance = 15 * scale
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            flower_group.append(
                f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="{6*scale}" fill="{accent}" opacity="0.9"/>'
            )

        # Wrap in group with transform
        svg_lines.append(f'  <g transform="translate({cx},{cy}) rotate({rotation})">')
        svg_lines.extend(flower_group)
        svg_lines.append('  </g>')

    # Create multiple flowers
    create_flower(75, 75, 1.0, 15)
    create_flower(225, 75, 0.8, -30)
    create_flower(150, 200, 1.2, 45)

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
            '_images', 'groups'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_flower_groups.svg',
        '02_composite_shapes.svg',
        '03_radial_groups.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
