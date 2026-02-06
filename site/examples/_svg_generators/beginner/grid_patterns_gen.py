"""
SVG Generator for Grid Patterns Example
Demonstrates grid selection methods: checkerboard, border, stripes
"""

def generate_svg(output_path: str, number: int) -> None:
    """Generate grid patterns example SVG."""
    cols = 15
    rows = 15
    cell_size = 20
    width = cols * cell_size
    height = rows * cell_size

    # Midnight palette
    background = "#1a1a2e"
    grid_color = "#4ecca3"
    accent = "#ee4266"
    primary = "#ffd23f"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Pattern 1: Checkerboard fills
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 2 == 0:
                x = col * cell_size
                y = row * cell_size
                svg_lines.append(
                    f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                    f'fill="{grid_color}" opacity="0.2"/>'
                )

    # Pattern 2: Border highlight
    for row in range(rows):
        for col in range(cols):
            if row == 0 or row == rows - 1 or col == 0 or col == cols - 1:
                x = col * cell_size + cell_size / 2
                y = row * cell_size + cell_size / 2
                svg_lines.append(
                    f'  <circle cx="{x}" cy="{y}" r="5" fill="{accent}"/>'
                )

    # Pattern 3: Diagonal stripe
    for row in range(rows):
        for col in range(cols):
            if (row + col) % 4 == 0:
                x = col * cell_size + cell_size / 2
                y = row * cell_size + cell_size / 2
                svg_lines.append(
                    f'  <circle cx="{x}" cy="{y}" r="3" fill="{primary}"/>'
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
            '_images', 'grid-patterns'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_checkerboard.svg',
        '02_border_highlight.svg',
        '03_stripe_patterns.svg',
        '04_radial_selection.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
