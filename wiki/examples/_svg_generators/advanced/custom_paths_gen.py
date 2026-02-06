"""
SVG Generator for Custom Paths Example
Demonstrates custom parametric paths: spirals, waves, Lissajous curves
"""

import math

def spiral_point(t, cx, cy, max_radius, turns):
    """Calculate point on Archimedean spiral."""
    angle = t * turns * 2 * math.pi
    radius = t * max_radius
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return (x, y)

def wave_point(t, start_x, start_y, end_x, end_y, amplitude, frequency):
    """Calculate point on sinusoidal wave."""
    x = start_x + t * (end_x - start_x)
    baseline_y = start_y + t * (end_y - start_y)
    wave_offset = amplitude * math.sin(t * frequency * 2 * math.pi)
    y = baseline_y + wave_offset
    return (x, y)

def lissajous_point(t, cx, cy, size, a, b, delta):
    """Calculate point on Lissajous curve."""
    angle = t * 2 * math.pi
    x = cx + size * math.sin(a * angle + delta)
    y = cy + size * math.sin(b * angle)
    return (x, y)

def generate_svg(output_path: str, number: int) -> None:
    """Generate custom paths SVG."""
    width = 450
    height = 300

    # Midnight palette
    background = "#1a1a2e"
    spiral_color = "#4ecca3"
    spiral_dots = "#ee4266"
    wave_color = "#ffd23f"
    wave_dots = "#64ffda"
    liss_color = "#ee4266"
    liss_dots = "#ffd23f"
    text_color = "#a0a0a0"

    svg_lines = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'  <rect width="{width}" height="{height}" fill="{background}"/>',
        ''
    ]

    # Section 1: Archimedean Spiral
    svg_lines.append('  <!-- Archimedean Spiral -->')
    svg_lines.append('  <g>')

    cx, cy = 75, 75
    max_radius = 50
    turns = 3

    # Draw spiral path
    path_points = []
    for i in range(100):
        t = i / 99
        x, y = spiral_point(t, cx, cy, max_radius, turns)
        if i == 0:
            path_points.append(f"M {x:.1f},{y:.1f}")
        else:
            path_points.append(f"L {x:.1f},{y:.1f}")

    svg_lines.append(
        f'    <path d="{" ".join(path_points)}" '
        f'stroke="{spiral_color}" stroke-width="0.5" fill="none" opacity="0.3"/>'
    )

    # Draw dots along spiral
    for i in range(0, 20):
        t = i / 19
        x, y = spiral_point(t, cx, cy, max_radius, turns)
        svg_lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{spiral_dots}"/>'
        )

    svg_lines.append(
        f'    <text x="{cx}" y="140" font-size="11" fill="{text_color}" '
        f'text-anchor="middle">Archimedean Spiral</text>'
    )
    svg_lines.append('  </g>')

    # Section 2: Sinusoidal Wave
    svg_lines.append('')
    svg_lines.append('  <!-- Sinusoidal Wave -->')
    svg_lines.append('  <g>')

    start_x, start_y = 140, 75
    end_x, end_y = 290, 75
    amplitude = 30
    frequency = 3

    # Draw wave path
    path_points = []
    for i in range(100):
        t = i / 99
        x, y = wave_point(t, start_x, start_y, end_x, end_y, amplitude, frequency)
        if i == 0:
            path_points.append(f"M {x:.1f},{y:.1f}")
        else:
            path_points.append(f"L {x:.1f},{y:.1f}")

    svg_lines.append(
        f'    <path d="{" ".join(path_points)}" '
        f'stroke="{wave_color}" stroke-width="0.5" fill="none" opacity="0.3"/>'
    )

    # Draw dots along wave
    for i in range(0, 25):
        t = i / 24
        x, y = wave_point(t, start_x, start_y, end_x, end_y, amplitude, frequency)
        svg_lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{wave_dots}"/>'
        )

    center_x = (start_x + end_x) / 2
    svg_lines.append(
        f'    <text x="{center_x}" y="140" font-size="11" fill="{text_color}" '
        f'text-anchor="middle">Sinusoidal Wave</text>'
    )
    svg_lines.append('  </g>')

    # Section 3: Lissajous Curve
    svg_lines.append('')
    svg_lines.append('  <!-- Lissajous Curve -->')
    svg_lines.append('  <g>')

    cx, cy = 370, 75
    size = 40
    a, b = 3, 2
    delta = math.pi / 2

    # Draw Lissajous path
    path_points = []
    for i in range(100):
        t = i / 99
        x, y = lissajous_point(t, cx, cy, size, a, b, delta)
        if i == 0:
            path_points.append(f"M {x:.1f},{y:.1f}")
        else:
            path_points.append(f"L {x:.1f},{y:.1f}")

    svg_lines.append(
        f'    <path d="{" ".join(path_points)}" '
        f'stroke="{liss_color}" stroke-width="0.5" fill="none" opacity="0.3"/>'
    )

    # Draw dots along Lissajous
    for i in range(0, 50):
        t = i / 49
        x, y = lissajous_point(t, cx, cy, size, a, b, delta)
        svg_lines.append(
            f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1.5" fill="{liss_dots}"/>'
        )

    svg_lines.append(
        f'    <text x="{cx}" y="140" font-size="11" fill="{text_color}" '
        f'text-anchor="middle">Lissajous (3:2)</text>'
    )
    svg_lines.append('  </g>')

    # Bottom section: More examples in grid
    svg_lines.append('')
    svg_lines.append('  <!-- Grid of variations -->')

    y_base = 180
    examples_data = [
        # (cx, cy, type, params)
        (75, y_base, 'spiral', {'turns': 2, 'max_radius': 30}),
        (150, y_base, 'wave', {'amplitude': 20, 'frequency': 2}),
        (225, y_base, 'lissajous', {'a': 5, 'b': 4, 'delta': 0, 'size': 30}),
        (300, y_base, 'spiral', {'turns': 4, 'max_radius': 30}),
        (375, y_base, 'wave', {'amplitude': 25, 'frequency': 4}),
    ]

    for cx, cy, path_type, params in examples_data:
        if path_type == 'spiral':
            for i in range(15):
                t = i / 14
                x, y = spiral_point(t, cx, cy, params['max_radius'], params['turns'])
                svg_lines.append(
                    f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1" fill="{spiral_dots}" opacity="0.7"/>'
                )
        elif path_type == 'wave':
            for i in range(20):
                t = i / 19
                x, y = wave_point(t, cx - 25, cy, cx + 25, cy, params['amplitude'], params['frequency'])
                svg_lines.append(
                    f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1" fill="{wave_dots}" opacity="0.7"/>'
                )
        elif path_type == 'lissajous':
            for i in range(30):
                t = i / 29
                x, y = lissajous_point(t, cx, cy, params['size'], params['a'], params['b'], params['delta'])
                svg_lines.append(
                    f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="1" fill="{liss_dots}" opacity="0.7"/>'
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
            '_images', 'custom-paths'
        )

    os.makedirs(output_dir, exist_ok=True)

    examples = [
        '01_spirals.svg',
        '02_waves.svg',
        '03_lissajous.svg',
        '04_all_paths.svg'
    ]

    for idx, filename in enumerate(examples, 1):
        output_path = os.path.join(output_dir, filename)
        generate_svg(output_path, idx)
        print(f"Generated: {output_path}")
