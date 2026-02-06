"""
SVG Generator for Showcase Example
Integrates multiple PyFreeform features: curves, transforms, connections, text
"""

import math

def generate_svg(output_path: str, number: int) -> None:
    """Generate comprehensive showcase SVG."""
    width = 500
    height = 400

    # Midnight palette
    background = "#0d1117"
    grid_color = "#1f2937"
    primary = "#4ecca3"
    secondary = "#ee4266"
    accent = "#ffd23f"
    line_color = "#64ffda"
    text_color = "#6b7280"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Feature 1: Grid pattern background
    svg_lines.append('  <!-- Grid pattern background -->')
    svg_lines.append('  <g opacity="0.2">')
    for i in range(0, width, 50):
        svg_lines.append(
            f'    <line x1="{i}" y1="0" x2="{i}" y2="{height}" '
            f'stroke="{grid_color}" stroke-width="0.5"/>'
        )
    for i in range(0, height, 50):
        svg_lines.append(
            f'    <line x1="0" y1="{i}" x2="{width}" y2="{i}" '
            f'stroke="{grid_color}" stroke-width="0.5"/>'
        )
    svg_lines.append('  </g>')

    # Feature 2: Curved paths
    svg_lines.append('')
    svg_lines.append('  <!-- Curved paths -->')

    # Draw flowing curves
    for start_y in [100, 200, 300]:
        # Control point for curve
        svg_lines.append(
            f'  <path d="M 50,{start_y} Q 150,{start_y-40} 250,{start_y} '
            f'Q 350,{start_y+40} 450,{start_y}" '
            f'stroke="{primary}" stroke-width="2" fill="none" opacity="0.6"/>'
        )

        # Dots along curves
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            # Quadratic Bezier calculation
            p0 = (50, start_y)
            p1 = (150, start_y - 40)
            p2 = (250, start_y)

            if t <= 0.5:
                t_local = t * 2
                x = (1-t_local)**2 * p0[0] + 2*(1-t_local)*t_local * p1[0] + t_local**2 * p2[0]
                y = (1-t_local)**2 * p0[1] + 2*(1-t_local)*t_local * p1[1] + t_local**2 * p2[1]
            else:
                t_local = (t - 0.5) * 2
                p0_2 = (250, start_y)
                p1_2 = (350, start_y + 40)
                p2_2 = (450, start_y)
                x = (1-t_local)**2 * p0_2[0] + 2*(1-t_local)*t_local * p1_2[0] + t_local**2 * p2_2[0]
                y = (1-t_local)**2 * p0_2[1] + 2*(1-t_local)*t_local * p1_2[1] + t_local**2 * p2_2[1]

            radius = 4 + t * 4
            color = secondary if int(t * 10) % 2 == 0 else accent
            svg_lines.append(
                f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{color}"/>'
            )

    # Feature 3: Rotating polygons
    svg_lines.append('')
    svg_lines.append('  <!-- Rotating polygons -->')

    polygon_positions = [
        (100, 350, 45, primary),
        (250, 350, -30, secondary),
        (400, 350, 15, accent),
    ]

    for cx, cy, angle, color in polygon_positions:
        # Hexagon
        points = []
        for i in range(6):
            a = i * math.pi / 3
            x = 15 * math.cos(a)
            y = 15 * math.sin(a)
            points.append(f"{x:.1f},{y:.1f}")

        svg_lines.append(
            f'  <g transform="translate({cx},{cy}) rotate({angle})">'
        )
        svg_lines.append(
            f'    <polygon points="{" ".join(points)}" fill="{color}" opacity="0.8"/>'
        )
        svg_lines.append('  </g>')

    # Feature 4: Title
    svg_lines.append('')
    svg_lines.append('  <!-- Title -->')
    svg_lines.append(
        f'  <text x="250" y="30" font-size="28" fill="{primary}" '
        f'font-family="sans-serif" text-anchor="middle" font-weight="bold">'
        'Feature Showcase'
        '</text>'
    )

    # Feature 5: Legend
    svg_lines.append(
        f'  <text x="20" y="380" font-size="10" fill="{text_color}" '
        f'font-family="monospace">'
        'Parametric Paths | Transforms | Layering | Typography'
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
            '_images', 'showcase'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_comprehensive.svg',
        '02_all_features.svg',
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
