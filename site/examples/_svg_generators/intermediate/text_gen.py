"""
SVG Generator for Text Example
Demonstrates typography features: alignment, rotation, sizing
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate text example SVG."""
    width = 350
    height = 300

    # Midnight palette
    background = "#1a1a2e"
    primary = "#4ecca3"
    secondary = "#ee4266"
    accent = "#ffd23f"
    text_color = "#e0e0e0"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Title
    svg_lines.append(
        f'  <text x="175" y="30" font-size="24" fill="{primary}" '
        f'font-family="sans-serif" text-anchor="middle" font-weight="bold">'
        'Typography Gallery'
        '</text>'
    )

    # Different alignments
    svg_lines.append(
        f'  <text x="50" y="70" font-size="14" fill="{secondary}" '
        f'font-family="sans-serif" text-anchor="start">'
        'Start Aligned'
        '</text>'
    )
    svg_lines.append(
        f'  <text x="175" y="70" font-size="14" fill="{accent}" '
        f'font-family="sans-serif" text-anchor="middle">'
        'Middle Aligned'
        '</text>'
    )
    svg_lines.append(
        f'  <text x="300" y="70" font-size="14" fill="{primary}" '
        f'font-family="sans-serif" text-anchor="end">'
        'End Aligned'
        '</text>'
    )

    # Font families
    svg_lines.append(
        f'  <text x="50" y="110" font-size="16" fill="{primary}" '
        f'font-family="sans-serif">'
        'Sans-serif'
        '</text>'
    )
    svg_lines.append(
        f'  <text x="50" y="135" font-size="16" fill="{secondary}" '
        f'font-family="serif">'
        'Serif'
        '</text>'
    )
    svg_lines.append(
        f'  <text x="50" y="160" font-size="16" fill="{accent}" '
        f'font-family="monospace">'
        'Monospace'
        '</text>'
    )

    # Rotated text examples
    svg_lines.append('  <g transform="translate(250, 150)">')
    for angle in [0, 45, 90, 135]:
        svg_lines.append(
            f'    <text transform="rotate({angle})" x="0" y="0" '
            f'font-size="12" fill="{primary}">{angle}°</text>'
        )
    svg_lines.append('  </g>')

    # Data labels with dots
    data_points = [
        (50, 220, 15, 0.82, primary),
        (120, 220, 20, 0.95, secondary),
        (200, 220, 10, 0.42, accent),
    ]

    for x, y, radius, value, color in data_points:
        svg_lines.append(
            f'  <circle cx="{x}" cy="{y}" r="{radius}" fill="{color}" opacity="0.5"/>'
        )
        text_color_val = "white" if value > 0.5 else "black"
        svg_lines.append(
            f'  <text x="{x}" y="{y+5}" font-size="10" fill="{text_color_val}" '
            f'font-family="monospace" text-anchor="middle">{value:.2f}</text>'
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
            '_images', 'text'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_alignment.svg',
        '02_font_families.svg',
        '03_data_labels.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
