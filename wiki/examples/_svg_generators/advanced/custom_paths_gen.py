#!/usr/bin/env python3
"""
SVG Generator for: examples/advanced/custom-paths

Demonstrates custom parametric paths using the Pathable protocol:
spirals, waves, and Lissajous curves.
"""

import math
from pyfreeform import Scene, Palette, Dot, Line, Text
from pyfreeform.core.point import Point
from pathlib import Path


OUTPUT_DIR = Path(__file__).parent.parent.parent / "_images" / "custom-paths"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Custom Pathable classes — any object with point_at(t) works with along=
# =============================================================================


class Spiral:
    """Archimedean spiral: radius grows linearly with t."""

    def __init__(self, cx, cy, max_radius, turns):
        self.cx = cx
        self.cy = cy
        self.max_radius = max_radius
        self.turns = turns

    def point_at(self, t):
        angle = t * self.turns * 2 * math.pi
        radius = t * self.max_radius
        return Point(
            self.cx + radius * math.cos(angle),
            self.cy + radius * math.sin(angle),
        )


class Wave:
    """Sinusoidal wave between two endpoints."""

    def __init__(self, start_x, start_y, end_x, end_y, amplitude, frequency):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t):
        x = self.start_x + t * (self.end_x - self.start_x)
        baseline_y = self.start_y + t * (self.end_y - self.start_y)
        wave_offset = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        return Point(x, baseline_y + wave_offset)


class Lissajous:
    """Lissajous curve (parametric figure)."""

    def __init__(self, cx, cy, size, a, b, delta):
        self.cx = cx
        self.cy = cy
        self.size = size
        self.a = a
        self.b = b
        self.delta = delta

    def point_at(self, t):
        angle = t * 2 * math.pi
        return Point(
            self.cx + self.size * math.sin(self.a * angle + self.delta),
            self.cy + self.size * math.sin(self.b * angle),
        )


def _draw_path_trace(scene, path, n_segments, color, width=0.5, opacity=0.3):
    """Draw a path as a series of line segments (for custom pathables)."""
    for i in range(n_segments):
        p1 = path.point_at(i / n_segments)
        p2 = path.point_at((i + 1) / n_segments)
        scene.add(Line(p1.x, p1.y, p2.x, p2.y, color=color, width=width, opacity=opacity))


def example_01_spirals():
    """Archimedean spiral with dots along the path."""
    colors = Palette.midnight()
    scene = Scene(width=250, height=250, background=colors.background)

    spiral = Spiral(125, 125, 80, 3)
    _draw_path_trace(scene, spiral, 100, colors.primary)

    for i in range(20):
        t = i / 19
        pt = spiral.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=2, color=colors.secondary))

    scene.add(Text(125, 230, "Archimedean Spiral", font_size=11, color=colors.line, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "01_spirals.svg")


def example_02_waves():
    """Sinusoidal wave with evenly distributed dots."""
    colors = Palette.midnight()
    scene = Scene(width=300, height=200, background=colors.background)

    wave = Wave(30, 100, 270, 100, 40, 3)
    _draw_path_trace(scene, wave, 100, colors.accent)

    for i in range(25):
        t = i / 24
        pt = wave.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=2, color="#64ffda"))

    scene.add(Text(150, 180, "Sinusoidal Wave", font_size=11, color=colors.line, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "02_waves.svg")


def example_03_lissajous():
    """Lissajous curve (3:2) with dense dot sampling."""
    colors = Palette.midnight()
    scene = Scene(width=250, height=250, background=colors.background)

    liss = Lissajous(125, 110, 60, 3, 2, math.pi / 2)
    _draw_path_trace(scene, liss, 100, colors.secondary)

    for i in range(50):
        t = i / 49
        pt = liss.point_at(t)
        scene.add(Dot(pt.x, pt.y, radius=1.5, color=colors.accent))

    scene.add(Text(125, 210, "Lissajous (3:2)", font_size=11, color=colors.line, text_anchor="middle"))

    scene.save(OUTPUT_DIR / "03_lissajous.svg")


def example_04_all_paths():
    """All three custom path types side by side with variations below."""
    colors = Palette.midnight()
    scene = Scene(width=450, height=300, background=colors.background)

    # Top row: main examples
    spiral = Spiral(75, 75, 50, 3)
    _draw_path_trace(scene, spiral, 100, colors.primary)
    for i in range(20):
        pt = spiral.point_at(i / 19)
        scene.add(Dot(pt.x, pt.y, radius=1.5, color=colors.secondary))
    scene.add(Text(75, 140, "Spiral", font_size=11, color=colors.line, text_anchor="middle"))

    wave = Wave(140, 75, 290, 75, 30, 3)
    _draw_path_trace(scene, wave, 100, colors.accent)
    for i in range(25):
        pt = wave.point_at(i / 24)
        scene.add(Dot(pt.x, pt.y, radius=1.5, color="#64ffda"))
    scene.add(Text(215, 140, "Wave", font_size=11, color=colors.line, text_anchor="middle"))

    liss = Lissajous(370, 75, 40, 3, 2, math.pi / 2)
    _draw_path_trace(scene, liss, 100, colors.secondary)
    for i in range(50):
        pt = liss.point_at(i / 49)
        scene.add(Dot(pt.x, pt.y, radius=1.5, color=colors.accent))
    scene.add(Text(370, 140, "Lissajous", font_size=11, color=colors.line, text_anchor="middle"))

    # Bottom row: variations
    variations = [
        Spiral(75, 210, 30, 2),
        Wave(125, 210, 175, 210, 20, 2),
        Lissajous(225, 210, 30, 5, 4, 0),
        Spiral(300, 210, 30, 4),
        Wave(350, 210, 400, 210, 25, 4),
    ]
    dot_colors = [colors.secondary, "#64ffda", colors.accent, colors.secondary, "#64ffda"]
    n_dots = [15, 20, 30, 15, 20]

    for path, color, n in zip(variations, dot_colors, n_dots):
        for i in range(n):
            pt = path.point_at(i / (n - 1))
            scene.add(Dot(pt.x, pt.y, radius=1, color=color, opacity=0.7))

    scene.save(OUTPUT_DIR / "04_all_paths.svg")


GENERATORS = {
    "01_spirals": example_01_spirals,
    "02_waves": example_02_waves,
    "03_lissajous": example_03_lissajous,
    "04_all_paths": example_04_all_paths,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for custom-paths examples...")

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
