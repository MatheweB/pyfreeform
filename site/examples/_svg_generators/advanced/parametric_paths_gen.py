"""
SVG Generator for Parametric Paths Example
Demonstrates unified parametric interface across lines, curves, and ellipses
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate parametric paths comparison SVG."""
    width = 500
    height = 350

    # Midnight palette
    background = "#1a1a2e"
    line_color = "#4ecca3"
    line_dots = "#ee4266"
    curve_dots = "#ffd23f"
    ellipse_dots = "#64ffda"
    text_color = "white"
    formula_color = "#6b7280"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Title
    svg_lines.append(
        f'  <text x="250" y="30" font-size="20" fill="{text_color}" '
        f'font-family="sans-serif" text-anchor="middle" font-weight="bold">'
        'Unified Parametric Interface'
        '</text>'
    )

    # Path 1: Line (Linear)
    svg_lines.append('')
    svg_lines.append('  <!-- Line path (Linear interpolation) -->')
    svg_lines.append('  <g transform="translate(0, 50)">')

    start_x, start_y = 50, 50
    end_x, end_y = 200, 50

    svg_lines.append(
        f'    <line x1="{start_x}" y1="{start_y}" x2="{end_x}" y2="{end_y}" '
        f'stroke="{line_color}" stroke-width="2" opacity="0.3"/>'
    )

    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x = start_x + t * (end_x - start_x)
        y = start_y + t * (end_y - start_y)
        svg_lines.append(
            f'    <circle cx="{x}" cy="{y}" r="4" fill="{line_dots}"/>'
        )

    svg_lines.append(
        f'    <text x="125" y="80" font-size="12" fill="{line_color}" '
        f'text-anchor="middle">Line (Linear)</text>'
    )
    svg_lines.append('  </g>')

    # Path 2: Curve (Bézier)
    svg_lines.append('')
    svg_lines.append('  <!-- Curve path (Bézier interpolation) -->')
    svg_lines.append('  <g transform="translate(0, 150)">')

    p0 = (50, 50)
    p1 = (125, 20)
    p2 = (200, 50)

    svg_lines.append(
        f'    <path d="M {p0[0]},{p0[1]} Q {p1[0]},{p1[1]} {p2[0]},{p2[1]}" '
        f'stroke="{line_color}" stroke-width="2" fill="none" opacity="0.3"/>'
    )

    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
        y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        svg_lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{curve_dots}"/>'
        )

    svg_lines.append(
        f'    <text x="125" y="80" font-size="12" fill="{line_color}" '
        f'text-anchor="middle">Curve (Bézier)</text>'
    )
    svg_lines.append('  </g>')

    # Path 3: Ellipse (Parametric)
    svg_lines.append('')
    svg_lines.append('  <!-- Ellipse path (Circular interpolation) -->')
    svg_lines.append('  <g transform="translate(250, 50)">')

    cx, cy = 125, 100
    rx, ry = 75, 50

    svg_lines.append(
        f'    <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'stroke="{line_color}" stroke-width="2" fill="none" opacity="0.3"/>'
    )

    for t in [0.0, 0.25, 0.5, 0.75]:
        angle = t * 2 * math.pi
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        svg_lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{ellipse_dots}"/>'
        )

    svg_lines.append(
        f'    <text x="125" y="180" font-size="12" fill="{line_color}" '
        f'text-anchor="middle">Ellipse (Parametric)</text>'
    )
    svg_lines.append('  </g>')

    # Formula
    svg_lines.append('')
    svg_lines.append(
        f'  <text x="250" y="330" font-size="11" fill="{formula_color}" '
        f'font-family="monospace" text-anchor="middle">'
        'point = path.point_at(t) where t ∈ [0, 1]'
        '</text>'
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
            '_images', 'parametric-paths'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_unified_interface.svg',
        '02_path_comparison.svg',
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
