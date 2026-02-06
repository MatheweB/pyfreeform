"""
SVG Generator for Custom Dots Example
Demonstrates palettes and brightness-based sizing
"""

def generate_svg(output_path: str, number: int) -> None:
    """Generate custom dots example SVG."""
    import math

    grid_size = 40
    cell_size = 10
    width = grid_size * cell_size
    height = grid_size * cell_size

    # Midnight palette colors
    background = "#1a1a2e"
    primary = "#4ecca3"
    secondary = "#ee4266"
    accent = "#ffd23f"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Generate dots with brightness-based sizing and color tiers
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size + cell_size / 2
            y = row * cell_size + cell_size / 2

            # Create wave pattern brightness
            brightness = (math.sin(col * 0.3) + math.cos(row * 0.3) + 2) / 4

            # Three brightness tiers
            if brightness > 0.6:
                # Large primary color dots
                size = 5 + brightness * 5  # 5-10px
                color = primary
            elif brightness > 0.3:
                # Medium secondary color dots
                size = 3 + brightness * 4  # 3-7px
                color = secondary
            else:
                # Small accent dots
                size = 2
                color = accent

            svg_lines.append(f'  <circle cx="{x}" cy="{y}" r="{size:.1f}" fill="{color}"/>')

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
            '_images', 'custom-dots'
        )

    os.makedirs(output_dir, exist_ok=True)

    # Generate examples
    examples = [
        '01_brightness_tiers.svg',
        '02_palette_variation.svg',
        '03_size_scaling.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
