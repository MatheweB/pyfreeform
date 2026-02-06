#!/usr/bin/env python3
"""
SVG Generator for: parametric-art/05-custom-paths.md

Generates visual examples showing:
- The Pathable protocol
- Archimedean spiral example
- Sinusoidal wave example
- Lissajous curve example
- Other creative paths (superellipse, epitrochoid, butterfly)

Corresponds to sections:
- The Pathable Protocol
- Example 1: Archimedean Spiral
- Example 2: Sinusoidal Wave
- Example 3: Lissajous Curve
- More Ideas
"""

from pyfreeform import Scene, Dot, Line, Text, Point
from pathlib import Path
import math


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "05-custom-paths"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: The Pathable Protocol
# =============================================================================

def example_01_pathable_concept():
    """
    Show the concept of implementing point_at(t)
    """
    scene = Scene(width=700, height=300, background="#f8f9fa")

    # Show a simple custom path
    cx, cy = 350, 150

    # Draw a simple custom path (figure-8)
    points = []
    for i in range(201):
        t = i / 200
        angle = t * 2 * math.pi
        x = cx + 120 * math.sin(angle)
        y = cy + 80 * math.sin(2 * angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Mark a few points to show they were placed with point_at()
    for t in [0, 0.25, 0.5, 0.75]:
        angle = t * 2 * math.pi
        x = cx + 120 * math.sin(angle)
        y = cy + 80 * math.sin(2 * angle)
        scene.add(Dot(x, y, radius=5, color="#ef4444"))

    # Code snippet
    scene.add(Text(350, 25, "class MyPath:", font_size=12, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 45, "    def point_at(self, t: float) -> Point:", font_size=12, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 65, "        # Your math here", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 85, "        return Point(x, y)", font_size=12, color="#ef4444", text_anchor="middle", font_family="monospace"))

    # Bottom note
    scene.add(Text(350, 275, "Any class with point_at() can be used with along=", font_size=13, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01-pathable-concept.svg")


# =============================================================================
# SECTION: Example 1 - Archimedean Spiral
# =============================================================================

def example_02_spiral_basic():
    """
    Show basic Archimedean spiral
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    start_r = 10
    end_r = 200
    turns = 3

    # Draw spiral
    points = []
    for i in range(201):
        t = i / 200
        angle = t * turns * 2 * math.pi
        radius = start_r + (end_r - start_r) * t
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Mark start and end
    scene.add(Dot(points[0].x, points[0].y, radius=7, color="#10b981"))
    scene.add(Text(points[0].x + 15, points[0].y, "start", font_size=12, color="#10b981"))

    scene.add(Dot(points[-1].x, points[-1].y, radius=7, color="#ef4444"))
    scene.add(Text(points[-1].x + 15, points[-1].y, "end", font_size=12, color="#ef4444"))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Title and formula
    scene.add(Text(250, 25, "Archimedean Spiral", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "r(t) = start_r + (end_r - start_r) × t", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "θ(t) = t × turns × 2π", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "02-spiral-basic.svg")


def example_03_spiral_variations():
    """
    Show spirals with different turn counts
    """
    scene = Scene(width=700, height=500, background="white")

    configs = [
        (175, 150, 2, "#3b82f6", "2 turns"),
        (525, 150, 3, "#8b5cf6", "3 turns"),
        (175, 350, 4, "#ec4899", "4 turns"),
        (525, 350, 5, "#f59e0b", "5 turns"),
    ]

    start_r = 5
    end_r = 120

    for cx, cy, turns, color, label in configs:
        # Draw spiral
        points = []
        for i in range(201):
            t = i / 200
            angle = t * turns * 2 * math.pi
            radius = start_r + (end_r - start_r) * t
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append(Point(x, y))

        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2
            ))

        # Label
        scene.add(Text(cx, cy - 140, label, font_size=13, color=color, text_anchor="middle", font_weight="bold"))

    # Title
    scene.add(Text(350, 25, "Spiral Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "03-spiral-variations.svg")


def example_04_spiral_with_dots():
    """
    Show dots positioned along spiral path
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    start_r = 10
    end_r = 200
    turns = 3

    # Draw spiral (light)
    points = []
    for i in range(201):
        t = i / 200
        angle = t * turns * 2 * math.pi
        radius = start_r + (end_r - start_r) * t
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#cbd5e1", width=2
        ))

    # Add dots along spiral
    for i in range(20):
        t = i / 19
        angle = t * turns * 2 * math.pi
        radius = start_r + (end_r - start_r) * t
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)

        scene.add(Dot(x, y, radius=4, color="#3b82f6"))

    # Title
    scene.add(Text(250, 25, "Positioning Dots Along Spiral", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 480, "for i in range(20): cell.add_dot(along=spiral, t=i/19)", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-spiral-with-dots.svg")


# =============================================================================
# SECTION: Example 2 - Sinusoidal Wave
# =============================================================================

def example_05_wave_basic():
    """
    Show basic sinusoidal wave
    """
    scene = Scene(width=600, height=300, background="white")

    start_x, start_y = 50, 150
    end_x, end_y = 550, 150
    amplitude = 60
    frequency = 3

    # Draw wave
    points = []
    for i in range(201):
        t = i / 200
        x = start_x + (end_x - start_x) * t
        base_y = start_y + (end_y - start_y) * t
        wave = amplitude * math.sin(t * frequency * 2 * math.pi)
        y = base_y + wave
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Draw baseline (dashed)
    scene.add(Line(start_x, start_y, end_x, end_y, color="#cbd5e1", width=1.5))

    # Mark amplitude
    scene.add(Line(300, 150, 300, 150 - amplitude, color="#ec4899", width=1.5))
    scene.add(Text(310, 150 - amplitude/2, "amplitude", font_size=11, color="#ec4899"))

    # Title and formula
    scene.add(Text(300, 25, "Sinusoidal Wave", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 270, "y(t) = base_y + amplitude × sin(frequency × 2πt)", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "05-wave-basic.svg")


def example_06_wave_variations():
    """
    Show waves with different frequencies and amplitudes
    """
    scene = Scene(width=600, height=550, background="white")

    configs = [
        (1, 30, "#3b82f6", "freq=1, amp=30"),
        (2, 40, "#8b5cf6", "freq=2, amp=40"),
        (3, 50, "#ec4899", "freq=3, amp=50"),
        (4, 30, "#f59e0b", "freq=4, amp=30"),
    ]

    for idx, (frequency, amplitude, color, label) in enumerate(configs):
        y_offset = 100 + idx * 110
        start_x, start_y = 50, y_offset
        end_x, end_y = 550, y_offset

        # Draw wave
        points = []
        for i in range(201):
            t = i / 200
            x = start_x + (end_x - start_x) * t
            wave = amplitude * math.sin(t * frequency * 2 * math.pi)
            y = start_y + wave
            points.append(Point(x, y))

        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2.5
            ))

        # Baseline
        scene.add(Line(start_x, start_y, end_x, end_y, color="#e5e7eb", width=1))

        # Label
        scene.add(Text(560, y_offset, label, font_size=11, color=color))

    # Title
    scene.add(Text(300, 25, "Wave Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "06-wave-variations.svg")


# =============================================================================
# SECTION: Example 3 - Lissajous Curve
# =============================================================================

def example_07_lissajous_basic():
    """
    Show basic Lissajous curve (3:2 ratio)
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    a = 3  # X frequency
    b = 2  # Y frequency
    delta = math.pi / 2  # Phase difference
    size = 180

    # Draw curve
    points = []
    for i in range(401):
        t = i / 400
        angle = t * 2 * math.pi
        x = cx + size * math.sin(a * angle + delta)
        y = cy + size * math.sin(b * angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#3b82f6", width=2.5
        ))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Title and formula
    scene.add(Text(250, 25, "Lissajous Curve (3:2)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "x(t) = A × sin(3t + π/2)", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "y(t) = B × sin(2t)", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "07-lissajous-basic.svg")


def example_08_lissajous_variations():
    """
    Show different Lissajous curves with different ratios
    """
    scene = Scene(width=700, height=700, background="white")

    configs = [
        (1, 1, 0, 175, 175, "#3b82f6", "1:1 (circle)"),
        (1, 2, 0, 525, 175, "#8b5cf6", "1:2 (figure-8)"),
        (3, 2, math.pi/2, 175, 525, "#ec4899", "3:2 (clover)"),
        (5, 4, 0, 525, 525, "#f59e0b", "5:4 (complex)"),
    ]

    size = 120

    for a, b, delta, cx, cy, color, label in configs:
        # Draw curve
        points = []
        for i in range(401):
            t = i / 400
            angle = t * 2 * math.pi
            x = cx + size * math.sin(a * angle + delta)
            y = cy + size * math.sin(b * angle)
            points.append(Point(x, y))

        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2
            ))

        # Label
        scene.add(Text(cx, cy - 140, label, font_size=13, color=color, text_anchor="middle", font_weight="bold"))

    # Title
    scene.add(Text(350, 25, "Lissajous Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(350, 50, "Different frequency ratios create different patterns", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-lissajous-variations.svg")


# =============================================================================
# SECTION: More Ideas - Other Curves
# =============================================================================

def example_09_superellipse():
    """
    Show superellipse (squircle) with different n values
    """
    scene = Scene(width=700, height=500, background="white")

    def sgn_pow(val, exp):
        """Signed power function"""
        return abs(val) ** exp if val >= 0 else -(abs(val) ** exp)

    configs = [
        (1, 175, 150, "#3b82f6", "n=1 (diamond)"),
        (2, 525, 150, "#8b5cf6", "n=2 (ellipse)"),
        (3, 175, 350, "#ec4899", "n=3 (squircle)"),
        (4, 525, 350, "#f59e0b", "n=4 (rounded)"),
    ]

    size = 100

    for n, cx, cy, color, label in configs:
        # Draw superellipse
        points = []
        for i in range(201):
            t = i / 200
            angle = t * 2 * math.pi
            x = cx + size * sgn_pow(math.cos(angle), 2/n)
            y = cy + size * sgn_pow(math.sin(angle), 2/n)
            points.append(Point(x, y))

        for i in range(len(points) - 1):
            scene.add(Line(
                points[i].x, points[i].y,
                points[i+1].x, points[i+1].y,
                color=color, width=2.5
            ))

        # Label
        scene.add(Text(cx, cy - 120, label, font_size=12, color=color, text_anchor="middle", font_weight="bold"))

    # Title
    scene.add(Text(350, 25, "Superellipse (|x/a|ⁿ + |y/b|ⁿ = 1)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "09-superellipse.svg")


def example_10_epitrochoid():
    """
    Show epitrochoid (spirograph-like curve)
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    R = 100  # Fixed circle radius
    r = 40   # Rolling circle radius
    d = 60   # Distance from rolling circle center

    # Draw epitrochoid
    points = []
    for i in range(601):
        t = i / 600
        angle = t * 6 * math.pi  # 3 full rotations
        x = cx + (R + r) * math.cos(angle) - d * math.cos((R + r) / r * angle)
        y = cy + (R + r) * math.sin(angle) - d * math.sin((R + r) / r * angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#8b5cf6", width=2
        ))

    # Center
    scene.add(Dot(cx, cy, radius=5, color="#666"))

    # Title
    scene.add(Text(250, 25, "Epitrochoid (Spirograph)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "x = (R+r)cos(t) - d·cos((R+r)/r·t)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "y = (R+r)sin(t) - d·sin((R+r)/r·t)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "10-epitrochoid.svg")


def example_11_butterfly_curve():
    """
    Show butterfly curve
    """
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    scale = 40

    # Draw butterfly curve
    points = []
    for i in range(2401):
        t = i / 2400
        angle = t * 12 * math.pi
        r = math.exp(math.sin(angle)) - 2 * math.cos(4 * angle) + math.sin(angle / 12) ** 5
        x = cx + scale * r * math.cos(angle)
        y = cy + scale * r * math.sin(angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#ec4899", width=1.5
        ))

    # Title
    scene.add(Text(250, 25, "Butterfly Curve", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 470, "r = exp(sin θ) - 2cos(4θ) + sin⁵(θ/12)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "11-butterfly-curve.svg")


def example_12_usage_example():
    """
    Show how these custom paths work with along=
    """
    scene = Scene(width=600, height=400, background="#f8f9fa")

    # Draw a Lissajous curve
    cx, cy = 300, 200
    a, b = 3, 2
    delta = math.pi / 2
    size = 150

    points = []
    for i in range(401):
        t = i / 400
        angle = t * 2 * math.pi
        x = cx + size * math.sin(a * angle + delta)
        y = cy + size * math.sin(b * angle)
        points.append(Point(x, y))

    for i in range(len(points) - 1):
        scene.add(Line(
            points[i].x, points[i].y,
            points[i+1].x, points[i+1].y,
            color="#cbd5e1", width=2
        ))

    # Position dots along it
    for i in range(15):
        t = i / 14
        angle = t * 2 * math.pi
        x = cx + size * math.sin(a * angle + delta)
        y = cy + size * math.sin(b * angle)

        scene.add(Dot(x, y, radius=5, color="#3b82f6"))

    # Code
    scene.add(Text(300, 25, "# Create custom path", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 45, "lissajous = Lissajous(cell.center, 3, 2, π/2, 10)", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 70, "# Position dots along it", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 90, "for i in range(15):", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 110, "    cell.add_dot(along=lissajous, t=i/14, radius=2)", font_size=11, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "12-usage-example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # Pathable concept
    "01-pathable-concept": example_01_pathable_concept,

    # Spiral
    "02-spiral-basic": example_02_spiral_basic,
    "03-spiral-variations": example_03_spiral_variations,
    "04-spiral-with-dots": example_04_spiral_with_dots,

    # Wave
    "05-wave-basic": example_05_wave_basic,
    "06-wave-variations": example_06_wave_variations,

    # Lissajous
    "07-lissajous-basic": example_07_lissajous_basic,
    "08-lissajous-variations": example_08_lissajous_variations,

    # Other curves
    "09-superellipse": example_09_superellipse,
    "10-epitrochoid": example_10_epitrochoid,
    "11-butterfly-curve": example_11_butterfly_curve,
    "12-usage-example": example_12_usage_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 05-custom-paths.md...")

    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")

    print(f"Complete! Generated to {OUTPUT_DIR}/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Generate specific image
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
