"""
SVG Generator for Multi-Layer Composition Example
Demonstrates strategic z-index management and layering
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate multi-layer composition SVG."""
    grid_size = 25
    cell_size = 16
    width = grid_size * cell_size
    height = grid_size * cell_size

    # Midnight palette
    background = "#0d1117"
    grid_color = "#1a1a2e"
    primary = "#4ecca3"
    secondary = "#374151"
    accent = "#ee4266"
    line_color = "#64ffda"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Layer 1: Grid structure (z=0)
    svg_lines.append('  <!-- Layer 1: Grid background -->')
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * cell_size
            y = row * cell_size
            svg_lines.append(
                f'  <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" '
                f'fill="none" stroke="{grid_color}" stroke-width="0.5" opacity="0.3"/>'
            )

    # Layer 2: Large background ellipses (z=5)
    svg_lines.append('')
    svg_lines.append('  <!-- Layer 2: Background shapes -->')
    for row in range(0, grid_size, 5):
        for col in range(0, grid_size, 5):
            cx = col * cell_size + 2.5 * cell_size
            cy = row * cell_size + 2.5 * cell_size
            svg_lines.append(
                f'  <ellipse cx="{cx}" cy="{cy}" rx="{cell_size*2}" ry="{cell_size*1.5}" '
                f'fill="{secondary}" opacity="0.2"/>'
            )

    # Layer 3: Network connections (z=10)
    svg_lines.append('')
    svg_lines.append('  <!-- Layer 3: Connection lines -->')

    # Create network nodes
    nodes = []
    for row in range(grid_size):
        for col in range(grid_size):
            # Radial brightness pattern
            center = grid_size / 2
            distance = math.sqrt((col - center)**2 + (row - center)**2)
            max_dist = math.sqrt(center**2 + center**2)
            brightness = 1 - (distance / max_dist)

            if brightness > 0.5:
                x = col * cell_size + cell_size / 2
                y = row * cell_size + cell_size / 2
                radius = 2 + brightness * 4
                nodes.append((x, y, radius, row, col))

    # Draw connections
    for i, (x1, y1, r1, row1, col1) in enumerate(nodes):
        for x2, y2, r2, row2, col2 in nodes[i+1:i+3]:
            dr = row1 - row2
            dc = col1 - col2
            dist = math.sqrt(dr*dr + dc*dc)
            if dist < 4:
                opacity = (1 - dist / 4) * 0.5
                svg_lines.append(
                    f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                    f'stroke="{line_color}" stroke-width="0.5" opacity="{opacity:.2f}"/>'
                )

    # Layer 4: Main nodes (z=20)
    svg_lines.append('')
    svg_lines.append('  <!-- Layer 4: Main nodes -->')
    for x, y, radius, row, col in nodes:
        svg_lines.append(
            f'  <circle cx="{x}" cy="{y}" r="{radius:.1f}" fill="{primary}"/>'
        )

    # Layer 5: Highlights (z=30)
    svg_lines.append('')
    svg_lines.append('  <!-- Layer 5: Highlights -->')
    for x, y, radius, row, col in nodes:
        if radius > 5:  # Only bright nodes
            svg_lines.append(
                f'  <circle cx="{x}" cy="{y}" r="{radius*0.3:.1f}" '
                f'fill="white" opacity="0.8"/>'
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
            '_images', 'multi-layer'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_layered_composition.svg',
        '02_depth_effect.svg',
        '03_complex_layering.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
