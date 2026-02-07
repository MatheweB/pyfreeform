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

import pathlib
import math

from pyfreeform import Scene, Dot, Line, Text, Point, Path


# Paths
OUTPUT_DIR = pathlib.Path(__file__).parent.parent / "_images" / "05-custom-paths"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Custom Pathable classes
# =============================================================================

class Spiral:
    def __init__(self, center, start_r, end_r, turns):
        self.center = center
        self.start_r = start_r
        self.end_r = end_r
        self.turns = turns

    def point_at(self, t):
        angle = t * self.turns * 2 * math.pi
        radius = self.start_r + (self.end_r - self.start_r) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Point(x, y)


class Wave:
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t):
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        wave = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        return Point(x, base_y + wave)


class Lissajous:
    def __init__(self, center, a, b, delta, size):
        self.center = center
        self.a = a
        self.b = b
        self.delta = delta
        self.size = size

    def point_at(self, t):
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Point(x, y)


class Superellipse:
    def __init__(self, center, size, n):
        self.center = center
        self.size = size
        self.n = n

    def point_at(self, t):
        angle = t * 2 * math.pi

        def sgn_pow(val, exp):
            return abs(val) ** exp if val >= 0 else -(abs(val) ** exp)

        x = self.center.x + self.size * sgn_pow(math.cos(angle), 2 / self.n)
        y = self.center.y + self.size * sgn_pow(math.sin(angle), 2 / self.n)
        return Point(x, y)


class Epitrochoid:
    def __init__(self, center, R, r, d, full_rotations=3):
        self.center = center
        self.R = R
        self.r = r
        self.d = d
        self.full_rotations = full_rotations

    def point_at(self, t):
        angle = t * self.full_rotations * 2 * math.pi
        R, r, d = self.R, self.r, self.d
        x = self.center.x + (R + r) * math.cos(angle) - d * math.cos((R + r) / r * angle)
        y = self.center.y + (R + r) * math.sin(angle) - d * math.sin((R + r) / r * angle)
        return Point(x, y)


class Butterfly:
    def __init__(self, center, scale):
        self.center = center
        self.scale = scale

    def point_at(self, t):
        angle = t * 12 * math.pi
        r = math.exp(math.sin(angle)) - 2 * math.cos(4 * angle) + math.sin(angle / 12) ** 5
        x = self.center.x + self.scale * r * math.cos(angle)
        y = self.center.y + self.scale * r * math.sin(angle)
        return Point(x, y)


# =============================================================================
# SECTION: The Pathable Protocol
# =============================================================================

def example_01_pathable_concept():
    """Show the concept of implementing point_at(t)"""
    scene = Scene(width=700, height=300, background="#f8f9fa")

    cx, cy = 350, 150

    # Draw a figure-8 using Path
    class Figure8:
        def point_at(self, t):
            angle = t * 2 * math.pi
            x = cx + 120 * math.sin(angle)
            y = cy + 80 * math.sin(2 * angle)
            return Point(x, y)

    fig8 = Figure8()
    scene.add(Path(fig8, closed=True, color="#3b82f6", width=2.5, segments=128))

    # Mark a few points
    for t in [0, 0.25, 0.5, 0.75]:
        pt = fig8.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=5, color="#ef4444"))

    # Code snippet
    scene.add(Text(350, 25, "class MyPath:", font_size=12, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 45, "    def point_at(self, t: float) -> Point:", font_size=12, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 65, "        # Your math here", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(350, 85, "        return Point(x, y)", font_size=12, color="#ef4444", text_anchor="middle", font_family="monospace"))

    scene.add(Text(350, 275, "Any class with point_at() can be rendered with Path()", font_size=13, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01-pathable-concept.svg")


# =============================================================================
# SECTION: Example 1 - Archimedean Spiral
# =============================================================================

def example_02_spiral_basic():
    """Show basic Archimedean spiral"""
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    spiral = Spiral(Point(cx, cy), 10, 200, 3)

    scene.add(Path(spiral, color="#3b82f6", width=2.5, segments=128))

    # Mark start and end
    start = spiral.point_at(0)
    end = spiral.point_at(1)
    scene.add(Dot(start.x, start.y, radius=7, color="#10b981"))
    scene.add(Text(start.x + 15, start.y, "start", font_size=12, color="#10b981"))
    scene.add(Dot(end.x, end.y, radius=7, color="#ef4444"))
    scene.add(Text(end.x + 15, end.y, "end", font_size=12, color="#ef4444"))

    scene.add(Dot(cx, cy, radius=5, color="#666"))

    scene.add(Text(250, 25, "Archimedean Spiral", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "r(t) = start_r + (end_r - start_r) \u00d7 t", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "\u03b8(t) = t \u00d7 turns \u00d7 2\u03c0", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "02-spiral-basic.svg")


def example_03_spiral_variations():
    """Show spirals with different turn counts"""
    scene = Scene(width=700, height=500, background="white")

    configs = [
        (175, 150, 2, "#3b82f6", "2 turns"),
        (525, 150, 3, "#8b5cf6", "3 turns"),
        (175, 350, 4, "#ec4899", "4 turns"),
        (525, 350, 5, "#f59e0b", "5 turns"),
    ]

    for cx, cy, turns, color, label in configs:
        spiral = Spiral(Point(cx, cy), 5, 120, turns)
        scene.add(Path(spiral, color=color, width=2, segments=128))
        scene.add(Text(cx, cy - 140, label, font_size=13, color=color, text_anchor="middle", font_weight="bold"))

    scene.add(Text(350, 25, "Spiral Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "03-spiral-variations.svg")


def example_04_spiral_with_dots():
    """Show dots positioned along spiral path"""
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    spiral = Spiral(Point(cx, cy), 10, 200, 3)

    # Draw spiral as smooth path (light)
    scene.add(Path(spiral, color="#cbd5e1", width=2, segments=128))

    # Add dots along spiral
    for i in range(20):
        t = i / 19
        pt = spiral.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=4, color="#3b82f6"))

    scene.add(Text(250, 25, "Positioning Dots Along Spiral", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 480, "for i in range(20): cell.add_dot(along=spiral, t=i/19)", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "04-spiral-with-dots.svg")


# =============================================================================
# SECTION: Example 2 - Sinusoidal Wave
# =============================================================================

def example_05_wave_basic():
    """Show basic sinusoidal wave"""
    scene = Scene(width=600, height=300, background="white")

    start = Point(50, 150)
    end = Point(550, 150)
    wave = Wave(start, end, amplitude=60, frequency=3)

    scene.add(Path(wave, color="#3b82f6", width=2.5, segments=128))

    # Draw baseline
    scene.add(Line(start.x, start.y, end.x, end.y, color="#cbd5e1", width=1.5))

    # Mark amplitude
    scene.add(Line(300, 150, 300, 90, color="#ec4899", width=1.5))
    scene.add(Text(310, 120, "amplitude", font_size=11, color="#ec4899"))

    scene.add(Text(300, 25, "Sinusoidal Wave", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(300, 270, "y(t) = base_y + amplitude \u00d7 sin(frequency \u00d7 2\u03c0t)", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "05-wave-basic.svg")


def example_06_wave_variations():
    """Show waves with different frequencies and amplitudes"""
    scene = Scene(width=600, height=550, background="white")

    configs = [
        (1, 30, "#3b82f6", "freq=1, amp=30"),
        (2, 40, "#8b5cf6", "freq=2, amp=40"),
        (3, 50, "#ec4899", "freq=3, amp=50"),
        (4, 30, "#f59e0b", "freq=4, amp=30"),
    ]

    for idx, (frequency, amplitude, color, label) in enumerate(configs):
        y_offset = 100 + idx * 110
        start = Point(50, y_offset)
        end = Point(550, y_offset)

        wave = Wave(start, end, amplitude, frequency)
        scene.add(Path(wave, color=color, width=2.5, segments=128))

        scene.add(Line(start.x, start.y, end.x, end.y, color="#e5e7eb", width=1))
        scene.add(Text(560, y_offset, label, font_size=11, color=color))

    scene.add(Text(300, 25, "Wave Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "06-wave-variations.svg")


# =============================================================================
# SECTION: Example 3 - Lissajous Curve
# =============================================================================

def example_07_lissajous_basic():
    """Show basic Lissajous curve (3:2 ratio)"""
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    liss = Lissajous(Point(cx, cy), 3, 2, math.pi / 2, 180)

    scene.add(Path(liss, closed=True, color="#3b82f6", width=2.5, segments=128))

    scene.add(Dot(cx, cy, radius=5, color="#666"))

    scene.add(Text(250, 25, "Lissajous Curve (3:2)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "x(t) = A \u00d7 sin(3t + \u03c0/2)", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "y(t) = B \u00d7 sin(2t)", font_size=12, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "07-lissajous-basic.svg")


def example_08_lissajous_variations():
    """Show different Lissajous curves with different ratios"""
    scene = Scene(width=700, height=700, background="white")

    configs = [
        (1, 1, 0, 175, 175, "#3b82f6", "1:1 (circle)"),
        (1, 2, 0, 525, 175, "#8b5cf6", "1:2 (figure-8)"),
        (3, 2, math.pi / 2, 175, 525, "#ec4899", "3:2 (clover)"),
        (5, 4, 0, 525, 525, "#f59e0b", "5:4 (complex)"),
    ]

    for a, b, delta, cx, cy, color, label in configs:
        liss = Lissajous(Point(cx, cy), a, b, delta, 120)
        scene.add(Path(liss, closed=True, color=color, width=2, segments=128))
        scene.add(Text(cx, cy - 140, label, font_size=13, color=color, text_anchor="middle", font_weight="bold"))

    scene.add(Text(350, 25, "Lissajous Variations", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(350, 50, "Different frequency ratios create different patterns", font_size=12, color="#666", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "08-lissajous-variations.svg")


# =============================================================================
# SECTION: More Ideas - Other Curves
# =============================================================================

def example_09_superellipse():
    """Show superellipse (squircle) with different n values"""
    scene = Scene(width=700, height=500, background="white")

    configs = [
        (1, 175, 150, "#3b82f6", "n=1 (diamond)"),
        (2, 525, 150, "#8b5cf6", "n=2 (ellipse)"),
        (3, 175, 350, "#ec4899", "n=3 (squircle)"),
        (4, 525, 350, "#f59e0b", "n=4 (rounded)"),
    ]

    for n, cx, cy, color, label in configs:
        se = Superellipse(Point(cx, cy), 100, n)
        scene.add(Path(se, closed=True, color=color, width=2.5, segments=128))
        scene.add(Text(cx, cy - 120, label, font_size=12, color=color, text_anchor="middle", font_weight="bold"))

    scene.add(Text(350, 25, "Superellipse (|x/a|\u207f + |y/b|\u207f = 1)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))

    scene.save(OUTPUT_DIR / "09-superellipse.svg")


def example_10_epitrochoid():
    """Show epitrochoid (spirograph-like curve)"""
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 250
    epi = Epitrochoid(Point(cx, cy), R=100, r=40, d=60, full_rotations=3)

    scene.add(Path(epi, closed=True, color="#8b5cf6", width=2, segments=256))

    scene.add(Dot(cx, cy, radius=5, color="#666"))

    scene.add(Text(250, 25, "Epitrochoid (Spirograph)", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 460, "x = (R+r)cos(t) - d\u00b7cos((R+r)/r\u00b7t)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(250, 480, "y = (R+r)sin(t) - d\u00b7sin((R+r)/r\u00b7t)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "10-epitrochoid.svg")


def example_11_butterfly_curve():
    """Show butterfly curve"""
    scene = Scene(width=500, height=500, background="white")

    butterfly = Butterfly(Point(250, 250), scale=40)

    scene.add(Path(butterfly, closed=True, color="#ec4899", width=1.5, segments=512))

    scene.add(Text(250, 25, "Butterfly Curve", font_size=18, color="#333", text_anchor="middle", font_weight="bold"))
    scene.add(Text(250, 470, "r = exp(sin \u03b8) - 2cos(4\u03b8) + sin\u2075(\u03b8/12)", font_size=10, color="#666", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "11-butterfly-curve.svg")


def example_12_usage_example():
    """Show how to render and position dots along custom paths"""
    scene = Scene(width=600, height=400, background="#f8f9fa")

    cx, cy = 300, 200
    liss = Lissajous(Point(cx, cy), 3, 2, math.pi / 2, 150)

    # Render the path as a smooth curve
    scene.add(Path(liss, closed=True, color="#cbd5e1", width=2, segments=128))

    # Position dots along it
    for i in range(15):
        t = i / 14
        pt = liss.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=5, color="#3b82f6"))

    scene.add(Text(300, 25, "# Render as smooth path", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 45, "cell.add_path(lissajous, closed=True, color='navy')", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 70, "# Position dots along it", font_size=11, color="#666", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 90, "for i in range(15):", font_size=11, color="#333", text_anchor="middle", font_family="monospace"))
    scene.add(Text(300, 110, "    cell.add_dot(along=lissajous, t=i/14, radius=2)", font_size=11, color="#3b82f6", text_anchor="middle", font_family="monospace"))

    scene.save(OUTPUT_DIR / "12-usage-example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-pathable-concept": example_01_pathable_concept,
    "02-spiral-basic": example_02_spiral_basic,
    "03-spiral-variations": example_03_spiral_variations,
    "04-spiral-with-dots": example_04_spiral_with_dots,
    "05-wave-basic": example_05_wave_basic,
    "06-wave-variations": example_06_wave_variations,
    "07-lissajous-basic": example_07_lissajous_basic,
    "08-lissajous-variations": example_08_lissajous_variations,
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
            print(f"  \u2713 {name}.svg")
        except Exception as e:
            print(f"  \u2717 {name}.svg - ERROR: {e}")

    print(f"Complete! Generated to {OUTPUT_DIR}/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        generate_all()
