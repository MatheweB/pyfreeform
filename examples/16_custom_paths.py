#!/usr/bin/env python3
"""
Example 16: Custom Parametric Paths

Shows how to create custom path objects that work with along=

Thanks to the Pathable protocol, any object with point_at(t) works!

This example implements:
- Spiral path (Archimedean spiral)
- Wave path (sinusoidal oscillation)
- Lissajous curve (parametric curve)

All work seamlessly with cell.add_dot(along=..., t=...)

Output: examples/16_custom_paths.svg
"""

from pathlib import Path
import sys
import math

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Palette, Point

# =============================================================================
# Custom Path Classes
# =============================================================================

class Spiral:
    """Archimedean spiral path."""

    def __init__(self, center: Point, start_radius: float, end_radius: float, turns: float):
        self.center = center
        self.start_radius = start_radius
        self.end_radius = end_radius
        self.turns = turns

    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0 to 1) along the spiral."""
        angle = t * self.turns * 2 * math.pi
        radius = self.start_radius + (self.end_radius - self.start_radius) * t
        x = self.center.x + radius * math.cos(angle)
        y = self.center.y + radius * math.sin(angle)
        return Point(x, y)


class Wave:
    """Sinusoidal wave path."""

    def __init__(self, start: Point, end: Point, amplitude: float, frequency: float):
        self.start = start
        self.end = end
        self.amplitude = amplitude
        self.frequency = frequency

    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0 to 1) along the wave."""
        # Base line interpolation
        x = self.start.x + (self.end.x - self.start.x) * t
        base_y = self.start.y + (self.end.y - self.start.y) * t

        # Add wave oscillation perpendicular to direction
        wave_offset = self.amplitude * math.sin(t * self.frequency * 2 * math.pi)
        y = base_y + wave_offset

        return Point(x, y)


class Lissajous:
    """Lissajous curve path."""

    def __init__(self, center: Point, a: float, b: float, delta: float, size: float):
        """
        Args:
            center: Center point
            a: Frequency of x oscillation
            b: Frequency of y oscillation
            delta: Phase difference (in radians)
            size: Size of the curve
        """
        self.center = center
        self.a = a
        self.b = b
        self.delta = delta
        self.size = size

    def point_at(self, t: float) -> Point:
        """Get point at parameter t (0 to 1) along the Lissajous curve."""
        angle = t * 2 * math.pi
        x = self.center.x + self.size * math.sin(self.a * angle + self.delta)
        y = self.center.y + self.size * math.sin(self.b * angle)
        return Point(x, y)


# =============================================================================
# Configuration
# =============================================================================

colors = Palette.neon()

# =============================================================================
# Create Art
# =============================================================================

scene = Scene.with_grid(cols=15, rows=15, cell_size=30)
scene.background = colors.background

for cell in scene.grid:
    # Choose path type based on position
    col_third = cell.col // 5
    row_third = cell.row // 5

    if col_third == 0:
        # Left third: Spirals
        path = Spiral(
            center=cell.center,
            start_radius=0,
            end_radius=12,
            turns=2
        )
        # Multiple dots along spiral
        for i in range(6):
            cell.add_dot(
                along=path,
                t=i / 5,
                radius=1.5,
                color=colors.primary
            )

    elif col_third == 1:
        # Middle third: Waves
        path = Wave(
            start=cell.top_left,
            end=cell.bottom_right,
            amplitude=5,
            frequency=2
        )
        # Multiple dots along wave
        for i in range(8):
            cell.add_dot(
                along=path,
                t=i / 7,
                radius=1,
                color=colors.accent
            )

    else:
        # Right third: Lissajous curves
        # Vary parameters based on row
        a = 1 + (row_third * 0.5)
        b = 1 + ((2 - row_third) * 0.5)
        delta = row_third * math.pi / 4

        path = Lissajous(
            center=cell.center,
            a=a,
            b=b,
            delta=delta,
            size=10
        )
        # Multiple dots along curve
        for i in range(12):
            cell.add_dot(
                along=path,
                t=i / 11,
                radius=1,
                color=colors.secondary
            )

# =============================================================================
# Save
# =============================================================================

output = Path(__file__).parent / "16_custom_paths.py"
scene.save(output)

print(f"Created: {output.name}")
print(f"Grid: {scene.grid.cols}x{scene.grid.rows}")
print()
print("This example demonstrates:")
print("  • Custom Pathable implementations (Spiral, Wave, Lissajous)")
print("  • point_at(t) method makes any object work with along=")
print("  • Spiral: Archimedean spiral expanding from center")
print("  • Wave: Sinusoidal oscillation along a line")
print("  • Lissajous: Parametric curve with frequency ratios")
print("  • All work seamlessly with cell.add_dot(along=..., t=...)")
