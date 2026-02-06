#!/usr/bin/env python3
"""
SVG Generator for: advanced-concepts/03-pathable-protocol.md

Generates visual examples for the Pathable protocol.

Corresponds to sections:
- What is Pathable?
- Built-In Pathables
- Using Pathables
- Creating Custom Paths
"""

from pyfreeform import Scene
from pyfreeform.core.point import Point
from pathlib import Path
import math

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "03-pathable-protocol"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# SECTION: What is Pathable?
# =============================================================================

def what_is_pathable_concept():
    """Pathable protocol concept"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create a line as example pathable
    line = cell.add_line(start="left", end="right", color="#3b82f6", width=2)

    # Show points along the path
    colors = ["#ef4444", "#f59e0b", "#10b981", "#8b5cf6", "#ec4899"]
    for i, t in enumerate([0.0, 0.25, 0.5, 0.75, 1.0]):
        point = line.point_at(t)
        cell.add_dot(at=point, radius=4, color=colors[i])
        cell.add_text(f"t={t:.2f}", at=(t, 0.2), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "01-what-is-pathable-concept.svg")

def what_is_pathable_interface():
    """Pathable interface demonstration"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Line
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#3b82f6", width=2)
    for t in [0.0, 0.5, 1.0]:
        cell1.add_dot(at=line.point_at(t), radius=3, color="#ef4444")
    cell1.add_text("Line", at=(0.5, 0.85), font_size=9, color="#1f2937")

    # Curve
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.4, color="#3b82f6", width=2)
    for t in [0.0, 0.5, 1.0]:
        cell2.add_dot(at=curve.point_at(t), radius=3, color="#ef4444")
    cell2.add_text("Curve", at=(0.5, 0.85), font_size=9, color="#1f2937")

    # Ellipse
    cell3 = scene.grid[0, 2]
    ellipse = cell3.add_ellipse(rx=35, ry=25, fill="#3b82f6")
    for t in [0.0, 0.5, 1.0]:
        cell3.add_dot(at=ellipse.point_at(t), radius=3, color="#ef4444")
    cell3.add_text("Ellipse", at=(0.5, 0.85), font_size=9, color="#1f2937")

    scene.save(OUTPUT_DIR / "02-what-is-pathable-interface.svg")

# =============================================================================
# SECTION: Built-In Pathables
# =============================================================================

def builtin_line():
    """Line as pathable - linear interpolation"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create line
    line = cell.add_line(start="left", end="right", color="#3b82f6", width=2)

    # Show points along line
    for i in range(11):
        t = i / 10
        point = line.point_at(t)
        size = 2 + (1 - abs(t - 0.5) * 2) * 3
        cell.add_dot(at=point, radius=size, color="#ef4444")

    cell.add_text("Line: Linear Interpolation", at=(0.5, 0.85), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "03-builtin-line.svg")

def builtin_curve():
    """Curve as pathable - Bézier parametric position"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create curve
    curve = cell.add_curve(start="left", end="right", curvature=0.5, color="#3b82f6", width=2)

    # Show points along curve
    for i in range(11):
        t = i / 10
        point = curve.point_at(t)
        size = 2 + (1 - abs(t - 0.5) * 2) * 3
        cell.add_dot(at=point, radius=size, color="#10b981")

    cell.add_text("Curve: Bézier Parametric", at=(0.5, 0.85), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "04-builtin-curve.svg")

def builtin_ellipse():
    """Ellipse as pathable - position around perimeter"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create ellipse
    ellipse = cell.add_ellipse(rx=60, ry=40, fill="#3b82f6")

    # Show points around perimeter
    for i in range(16):
        t = i / 16
        point = ellipse.point_at(t)
        cell.add_dot(at=point, radius=3, color="#f59e0b")

    cell.add_text("Ellipse: Perimeter Position", at=(0.5, 0.85), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "05-builtin-ellipse.svg")

# =============================================================================
# SECTION: Using Pathables
# =============================================================================

def using_pathables_unified():
    """Unified interface for all pathables"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Line
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#3b82f6", width=2)
    cell1.add_dot(along=line, t=0.5, radius=6, color="#ef4444")
    cell1.add_text("line, t=0.5", at=(0.5, 0.2), font_size=7, color="#1f2937")

    # Curve
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.5, color="#3b82f6", width=2)
    cell2.add_dot(along=curve, t=0.5, radius=6, color="#ef4444")
    cell2.add_text("curve, t=0.5", at=(0.5, 0.2), font_size=7, color="#1f2937")

    # Ellipse
    cell3 = scene.grid[0, 2]
    ellipse = cell3.add_ellipse(rx=35, ry=25, fill="#3b82f6")
    cell3.add_dot(along=ellipse, t=0.5, radius=6, color="#ef4444")
    cell3.add_text("ellipse, t=0.5", at=(0.5, 0.85), font_size=7, color="#1f2937")

    scene.save(OUTPUT_DIR / "06-using-pathables-unified.svg")

def using_pathables_distribution():
    """Distributing dots along different pathables"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "#f8f9fa"

    # Line with dots
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#3b82f6", width=2)
    for i in range(7):
        t = i / 6
        cell1.add_dot(along=line, t=t, radius=3, color="#ef4444")
    cell1.add_text("Line", at=(0.5, 0.85), font_size=9, color="#1f2937")

    # Curve with dots
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.4, color="#3b82f6", width=2)
    for i in range(7):
        t = i / 6
        cell2.add_dot(along=curve, t=t, radius=3, color="#10b981")
    cell2.add_text("Curve", at=(0.5, 0.85), font_size=9, color="#1f2937")

    # Ellipse with dots
    cell3 = scene.grid[0, 2]
    ellipse = cell3.add_ellipse(rx=35, ry=25, fill="#3b82f6")
    for i in range(12):
        t = i / 12
        cell3.add_dot(along=ellipse, t=t, radius=3, color="#f59e0b")
    cell3.add_text("Ellipse", at=(0.5, 0.85), font_size=9, color="#1f2937")

    scene.save(OUTPUT_DIR / "07-using-pathables-distribution.svg")

# =============================================================================
# SECTION: Creating Custom Paths
# =============================================================================

class Spiral:
    """Custom spiral path"""
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

def custom_spiral():
    """Custom spiral path"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create spiral
    spiral = Spiral(cell.center, start_r=5, end_r=70, turns=3)

    # Draw points along spiral
    for i in range(50):
        t = i / 49
        point = spiral.point_at(t)
        size = 1 + t * 3
        cell.add_dot(at=point, radius=size, color="#8b5cf6")

    cell.add_text("Custom Spiral", at=(0.5, 0.9), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "08-custom-spiral.svg")

class Wave:
    """Custom wave path"""
    def __init__(self, start, end, amplitude, frequency):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t: float) -> Point:
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t
        wave_y = math.sin(t * self.frequency * 2 * math.pi) * self.amplitude
        y = base_y + wave_y
        return Point(x, y)

def custom_wave():
    """Custom wave path"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create wave from left edge to right edge at center height
    left = Point(cell.x, cell.center.y)
    right = Point(cell.x + cell.width, cell.center.y)
    wave = Wave(left, right, amplitude=30, frequency=3)

    # Draw points along wave
    for i in range(60):
        t = i / 59
        point = wave.point_at(t)
        cell.add_dot(at=point, radius=2, color="#10b981")

    cell.add_text("Custom Wave", at=(0.5, 0.9), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "09-custom-wave.svg")

class Heart:
    """Custom heart path"""
    def __init__(self, center, size):
        self.center = center
        self.size = size

    def point_at(self, t: float) -> Point:
        # Parametric heart curve
        angle = t * 2 * math.pi
        # Cardioid-like equation
        x = 16 * math.sin(angle) ** 3
        y = -(13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle))

        # Scale and position
        x = self.center.x + x * self.size / 20
        y = self.center.y + y * self.size / 20

        return Point(x, y)

def custom_heart():
    """Custom heart path"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create heart
    heart = Heart(cell.center, size=50)

    # Draw points along heart
    for i in range(60):
        t = i / 60
        point = heart.point_at(t)
        cell.add_dot(at=point, radius=2.5, color="#ef4444")

    cell.add_text("Custom Heart", at=(0.5, 0.9), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "10-custom-heart.svg")

class Lissajous:
    """Custom Lissajous curve path"""
    def __init__(self, center, size, a, b, delta):
        self.center = center
        self.size = size
        self.a = a
        self.b = b
        self.delta = delta

    def point_at(self, t: float) -> Point:
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Point(x, y)

def custom_lissajous():
    """Custom Lissajous curve"""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    scene.background = "#f8f9fa"

    cell = scene.grid[0, 0]

    # Create Lissajous curve
    lissajous = Lissajous(cell.center, size=60, a=3, b=4, delta=math.pi / 2)

    # Draw points along curve
    for i in range(100):
        t = i / 100
        point = lissajous.point_at(t)
        cell.add_dot(at=point, radius=1.5, color="#3b82f6")

    cell.add_text("Lissajous Curve", at=(0.5, 0.9), font_size=10, color="#1f2937")

    scene.save(OUTPUT_DIR / "11-custom-lissajous.svg")

def custom_paths_comparison():
    """Comparison of custom paths"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "#f8f9fa"

    # Spiral
    cell1 = scene.grid[0, 0]
    spiral = Spiral(cell1.center, start_r=2, end_r=35, turns=2)
    for i in range(30):
        t = i / 29
        cell1.add_dot(at=spiral.point_at(t), radius=1.5, color="#8b5cf6")
    cell1.add_text("Spiral", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Wave
    cell2 = scene.grid[0, 1]
    left = Point(cell2.x, cell2.center.y)
    right = Point(cell2.x + cell2.width, cell2.center.y)
    wave = Wave(left, right, amplitude=15, frequency=2)
    for i in range(40):
        t = i / 39
        cell2.add_dot(at=wave.point_at(t), radius=1.5, color="#10b981")
    cell2.add_text("Wave", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Heart
    cell3 = scene.grid[0, 2]
    heart = Heart(cell3.center, size=30)
    for i in range(40):
        t = i / 40
        cell3.add_dot(at=heart.point_at(t), radius=1.5, color="#ef4444")
    cell3.add_text("Heart", at=(0.5, 0.9), font_size=8, color="#1f2937")

    # Lissajous
    cell4 = scene.grid[0, 3]
    lissajous = Lissajous(cell4.center, size=35, a=3, b=2, delta=math.pi / 4)
    for i in range(60):
        t = i / 60
        cell4.add_dot(at=lissajous.point_at(t), radius=1.5, color="#3b82f6")
    cell4.add_text("Lissajous", at=(0.5, 0.9), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "12-custom-paths-comparison.svg")

def practical_example_distribution():
    """Practical example: distributing elements along paths"""
    scene = Scene.with_grid(cols=2, rows=2, cell_size=100)
    scene.background = "#f8f9fa"

    # Line distribution
    cell1 = scene.grid[0, 0]
    line = cell1.add_line(start="left", end="right", color="#d1d5db", width=1)
    for i in range(5):
        t = i / 4
        size = 2 + (1 - abs(t - 0.5) * 2) * 4
        cell1.add_dot(along=line, t=t, radius=size, color="#3b82f6")
    cell1.add_text("Line", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Curve distribution
    cell2 = scene.grid[0, 1]
    curve = cell2.add_curve(start="left", end="right", curvature=0.4, color="#d1d5db", width=1)
    for i in range(5):
        t = i / 4
        size = 2 + (1 - abs(t - 0.5) * 2) * 4
        cell2.add_dot(along=curve, t=t, radius=size, color="#10b981")
    cell2.add_text("Curve", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Ellipse distribution
    cell3 = scene.grid[1, 0]
    ellipse = cell3.add_ellipse(rx=30, ry=20, fill="#3b82f6")
    for i in range(8):
        t = i / 8
        cell3.add_dot(along=ellipse, t=t, radius=3, color="#f59e0b")
    cell3.add_text("Ellipse", at=(0.5, 0.85), font_size=8, color="#1f2937")

    # Spiral distribution
    cell4 = scene.grid[1, 1]
    spiral = Spiral(cell4.center, start_r=5, end_r=30, turns=2)
    for i in range(12):
        t = i / 11
        size = 1.5 + t * 2
        cell4.add_dot(at=spiral.point_at(t), radius=size, color="#8b5cf6")
    cell4.add_text("Spiral", at=(0.5, 0.85), font_size=8, color="#1f2937")

    scene.save(OUTPUT_DIR / "13-practical-example-distribution.svg")

# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    # What is Pathable?
    "01-what-is-pathable-concept": what_is_pathable_concept,
    "02-what-is-pathable-interface": what_is_pathable_interface,

    # Built-in pathables
    "03-builtin-line": builtin_line,
    "04-builtin-curve": builtin_curve,
    "05-builtin-ellipse": builtin_ellipse,

    # Using pathables
    "06-using-pathables-unified": using_pathables_unified,
    "07-using-pathables-distribution": using_pathables_distribution,

    # Custom paths
    "08-custom-spiral": custom_spiral,
    "09-custom-wave": custom_wave,
    "10-custom-heart": custom_heart,
    "11-custom-lissajous": custom_lissajous,
    "12-custom-paths-comparison": custom_paths_comparison,
    "13-practical-example-distribution": practical_example_distribution,
}

def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 03-pathable-protocol.md...")

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
