#!/usr/bin/env python3
"""
SVG Generator for: developer-guide/04-pathable-protocol.md

Generates visual examples for implementing custom pathable paths.

Corresponds to sections:
- The Protocol
- Example: Wave Path
- Usage
"""

from pathlib import Path
import math
from pyfreeform import Scene
from pyfreeform.core.point import Point

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "04-pathable-protocol"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: Wave Path Implementation
# =============================================================================

class Wave:
    """Custom wave path for visualization"""
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t: float) -> Point:
        # Linear base
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t

        # Add wave
        wave = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        y = base_y + wave

        return Point(x, y)

def wave_path_visual():
    """Visual representation of wave path"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Create wave
    wave = Wave(
        start=Point(cell.x, cell.center.y),
        end=Point(cell.x + cell.width, cell.center.y),
        amplitude=30,
        frequency=3
    )

    # Draw wave with dots
    for i in range(60):
        t = i / 59
        point = wave.point_at(t)
        cell.add_dot(at=point, radius=2, color="#3b82f6")

    # Show start and end
    cell.add_dot(at=wave.start, radius=5, color="#10b981", z_index=1)
    cell.add_dot(at=wave.end, radius=5, color="#ef4444", z_index=1)

    scene.save(OUTPUT_DIR / "01-wave-path-visual.svg")

def wave_parameters():
    """Show how wave parameters affect the path"""
    scene = Scene.with_grid(cols=3, rows=2, cell_size=140)
    scene.background = "#f8f9fa"

    # Amplitude variations
    for i, amp in enumerate([10, 20, 30]):
        cell = scene.grid[0, i]
        cell.add_border(color="#e5e7eb", width=1)

        wave = Wave(
            start=Point(cell.x, cell.center.y),
            end=Point(cell.x + cell.width, cell.center.y),
            amplitude=amp,
            frequency=2
        )

        for j in range(40):
            t = j / 39
            cell.add_dot(at=wave.point_at(t), radius=1.5, color="#3b82f6")

    # Frequency variations
    for i, freq in enumerate([1, 2, 3]):
        cell = scene.grid[1, i]
        cell.add_border(color="#e5e7eb", width=1)

        wave = Wave(
            start=Point(cell.x, cell.center.y),
            end=Point(cell.x + cell.width, cell.center.y),
            amplitude=20,
            frequency=freq
        )

        for j in range(40):
            t = j / 39
            cell.add_dot(at=wave.point_at(t), radius=1.5, color="#10b981")

    scene.save(OUTPUT_DIR / "02-wave-parameters.svg")

def using_wave_with_along():
    """Show wave being used to position elements"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Create wave
    wave = Wave(
        start=Point(cell.x, cell.center.y),
        end=Point(cell.x + cell.width, cell.center.y),
        amplitude=25,
        frequency=3
    )

    # Draw wave path (faint)
    for i in range(60):
        t = i / 59
        cell.add_dot(at=wave.point_at(t), radius=1, color="#cbd5e1")

    # Add dots along wave
    for i in range(11):
        t = i / 10
        point = wave.point_at(t)
        cell.add_dot(at=point, radius=5, color="#3b82f6", z_index=1)

    scene.save(OUTPUT_DIR / "03-using-wave-with-along.svg")

# =============================================================================
# SECTION: Built-in Pathables
# =============================================================================

def builtin_pathables():
    """Show built-in pathables"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Line - pathable
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#3b82f6", width=2)
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        cell1.add_dot(along=line, t=t, radius=3, color="#ef4444")
    cell1.add_border(color="#e5e7eb", width=1)

    # Curve - pathable
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.5, color="#3b82f6", width=2)
    for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
        cell2.add_dot(along=curve, t=t, radius=3, color="#ef4444")
    cell2.add_border(color="#e5e7eb", width=1)

    # Ellipse - pathable
    cell3 = scene.grid[0, 2]
    ellipse = cell3.add_ellipse(rx=35, ry=25, fill="#3b82f6")
    for t in [0.0, 0.25, 0.5, 0.75]:
        cell3.add_dot(along=ellipse, t=t, radius=3, color="#ef4444")
    cell3.add_border(color="#e5e7eb", width=1)

    scene.save(OUTPUT_DIR / "04-builtin-pathables.svg")

# =============================================================================
# SECTION: point_at Method Detail
# =============================================================================

def point_at_method_detail():
    """Detailed explanation of point_at method"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Create wave
    wave = Wave(
        start=Point(cell.x, cell.center.y),
        end=Point(cell.x + cell.width, cell.center.y),
        amplitude=30,
        frequency=2
    )

    # Draw wave
    for i in range(60):
        t = i / 59
        cell.add_dot(at=wave.point_at(t), radius=1.5, color="#cbd5e1")

    # Show specific t values
    t_values = [0.0, 0.25, 0.5, 0.75, 1.0]
    colors = ["#10b981", "#3b82f6", "#f59e0b", "#8b5cf6", "#ef4444"]

    for t, color in zip(t_values, colors):
        point = wave.point_at(t)
        cell.add_dot(at=point, radius=5, color=color, z_index=1)

    scene.save(OUTPUT_DIR / "05-point-at-method-detail.svg")

# =============================================================================
# SECTION: Custom Path Variations
# =============================================================================

class Spiral:
    """Spiral path for comparison"""
    def __init__(self, center, start_r, end_r, turns):
        self.center = center
        self.start_r = start_r
        self.end_r = end_r
        self.turns = turns

    def point_at(self, t: float) -> Point:
        angle = t * self.turns * 2 * math.pi
        radius = self.start_r + (self.end_r - self.start_r) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Point(x, y)

class Zigzag:
    """Zigzag path for comparison"""
    def __init__(self, start, end, amplitude, segments):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.segments = segments

    def point_at(self, t: float) -> Point:
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t

        # Zigzag pattern
        segment_t = (t * self.segments) % 1.0
        zigzag = self.amplitude * (1 - 2 * abs(segment_t - 0.5))
        y = base_y + zigzag

        return Point(x, y)

def custom_path_variations():
    """Show different custom pathable implementations"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=140)
    scene.background = "#f8f9fa"

    # Wave
    cell1 = scene.grid[0, 0]
    cell1.add_border(color="#e5e7eb", width=1)
    wave = Wave(
        start=Point(cell1.x, cell1.center.y),
        end=Point(cell1.x + cell1.width, cell1.center.y),
        amplitude=20,
        frequency=2
    )
    for i in range(40):
        t = i / 39
        cell1.add_dot(at=wave.point_at(t), radius=1.5, color="#3b82f6")

    # Spiral
    cell2 = scene.grid[0, 1]
    cell2.add_border(color="#e5e7eb", width=1)
    spiral = Spiral(cell2.center, start_r=5, end_r=50, turns=2)
    for i in range(40):
        t = i / 39
        cell2.add_dot(at=spiral.point_at(t), radius=1.5, color="#10b981")

    # Zigzag
    cell3 = scene.grid[0, 2]
    cell3.add_border(color="#e5e7eb", width=1)
    zigzag = Zigzag(
        start=Point(cell3.x, cell3.center.y),
        end=Point(cell3.x + cell3.width, cell3.center.y),
        amplitude=25,
        segments=4
    )
    for i in range(40):
        t = i / 39
        cell3.add_dot(at=zigzag.point_at(t), radius=1.5, color="#f59e0b")

    scene.save(OUTPUT_DIR / "06-custom-path-variations.svg")

# =============================================================================
# SECTION: Practical Usage Example
# =============================================================================

def practical_usage_example():
    """Practical example of using custom pathable"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=300)
    scene.background = "#ffffff"

    cell = list(scene.grid)[0]

    # Create wave
    wave = Wave(
        start=Point(cell.x, cell.center.y),
        end=Point(cell.x + cell.width, cell.center.y),
        amplitude=30,
        frequency=3
    )

    # Place different sized dots along the wave
    for i in range(20):
        t = i / 19
        size = 2 + abs(math.sin(t * math.pi)) * 6
        cell.add_dot(at=wave.point_at(t), radius=size, color="#3b82f6")

    scene.save(OUTPUT_DIR / "07-practical-usage-example.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-wave-path-visual": wave_path_visual,
    "02-wave-parameters": wave_parameters,
    "03-using-wave-with-along": using_wave_with_along,
    "04-builtin-pathables": builtin_pathables,
    "05-point-at-method-detail": point_at_method_detail,
    "06-custom-path-variations": custom_path_variations,
    "07-practical-usage-example": practical_usage_example,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 04-pathable-protocol.md...")

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
            print(f"Available: {', '.join(sorted(GENERATORS.keys()))}")
    else:
        generate_all()
