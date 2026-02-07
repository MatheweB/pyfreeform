"""Test script for the Path entity — renders Wave, Spiral, and Lissajous as smooth SVG paths."""

import math
import sys
sys.path.insert(0, "src")

from pyfreeform import Scene, Path, Point


# ── Custom Pathables (same as examples/16_custom_paths.py) ──

class Wave:
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t):
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        wave_offset = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        return Point(x, base_y + wave_offset)


class Spiral:
    def __init__(self, center, start_radius, end_radius, turns):
        self.center = center
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.turns = turns

    def point_at(self, t):
        angle = t * self.turns * 2 * math.pi
        radius = self.start_radius + (self.end_radius - self.start_radius) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Point(x, y)


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


# ── Test 1: Open wave path ──
scene = Scene(600, 400, background="white")

wave = Wave(Point(50, 100), Point(550, 100), amplitude=40, frequency=4)
wave_path = Path(wave, width=2, color="steelblue", segments=128)
scene.add(wave_path)

# Place dots along the wave path to verify point_at works
from pyfreeform import Dot
for i in range(21):
    t = i / 20
    pt = wave_path.point_at(t)
    scene.add(Dot(pt.x, pt.y, radius=3, color="coral"))


# ── Test 2: Open spiral ──
spiral = Spiral(Point(150, 300), start_radius=10, end_radius=80, turns=3)
spiral_path = Path(spiral, width=1.5, color="darkgreen", segments=128)
scene.add(spiral_path)


# ── Test 3: Closed Lissajous with fill ──
liss = Lissajous(Point(450, 300), a=3, b=2, delta=math.pi / 2, size=70)
liss_path = Path(liss, closed=True, width=2, color="navy", fill="lightskyblue",
                 segments=128, fill_opacity=0.5)
scene.add(liss_path)


# ── Test 4: Wave with arrow caps ──
wave2 = Wave(Point(50, 200), Point(550, 200), amplitude=25, frequency=2)
wave_path2 = Path(wave2, width=3, color="firebrick", segments=64,
                  start_cap="round", end_cap="arrow")
scene.add(wave_path2)


# ── Write output ──
scene.save("test_path_entity.svg")
print("Saved test_path_entity.svg")
print(f"Wave path: {wave_path}")
print(f"Spiral path: {spiral_path}")
print(f"Lissajous path: {liss_path}")
print(f"Wave path arc length: {wave_path.arc_length():.1f}")
print(f"Lissajous point_at(0.25): {liss_path.point_at(0.25)}")
print(f"Wave angle_at(0.5): {wave_path.angle_at(0.5):.1f} degrees")
