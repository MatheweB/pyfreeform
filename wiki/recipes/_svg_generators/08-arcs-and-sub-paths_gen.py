#!/usr/bin/env python3
"""
SVG Generator for: recipes/08-arcs-and-sub-paths.md

Generates visual examples showing:
- Basic arc from an ellipse using start_t/end_t
- Multiple arcs with gaps (dashed circle effect)
- Arc progress indicator / gauge
- Spiral sub-section
- Rainbow arcs
- Combined showcase
"""

import pathlib
import math

from pyfreeform import Scene, Dot, Line, Ellipse, Text, Point, Path, Curve


OUTPUT_DIR = (
    pathlib.Path(__file__).parent.parent / "_images" / "08-arcs-and-sub-paths"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# Custom Pathable classes for examples
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


# =============================================================================
# SECTION 1: Basic arc concept
# =============================================================================

def example_01_basic_arc():
    """Show a full ellipse vs a quarter arc."""
    scene = Scene(width=700, height=300, background="white")

    # Left: full ellipse
    cx1, cy1 = 175, 160
    e1 = Ellipse(cx1, cy1, rx=80, ry=80)
    scene.add(Path(e1, closed=True, color="#cbd5e1", width=2))
    scene.add(Text(cx1, cy1 - 105, "Full path (default)",
                   font_size=13, color="#333", text_anchor="middle",
                   font_weight="bold"))
    scene.add(Text(cx1, cy1 + 110, "Path(ellipse, closed=True)",
                   font_size=10, color="#888", text_anchor="middle",
                   font_family="monospace"))

    # Right: quarter arc
    cx2, cy2 = 525, 160
    e2 = Ellipse(cx2, cy2, rx=80, ry=80)
    # Ghost circle
    scene.add(Path(e2, closed=True, color="#f1f5f9", width=1))
    # Arc
    scene.add(Path(e2, start_t=0.0, end_t=0.25, color="#3b82f6", width=4))
    # Dots at start and end
    start = e2.point_at(0.0)
    end = e2.point_at(0.25)
    scene.add(Dot(start.x, start.y, radius=6, color="#10b981"))
    scene.add(Dot(end.x, end.y, radius=6, color="#ef4444"))
    scene.add(Text(start.x + 12, start.y - 5, "t=0.0",
                   font_size=10, color="#10b981"))
    scene.add(Text(end.x - 5, end.y + 18, "t=0.25",
                   font_size=10, color="#ef4444"))
    scene.add(Text(cx2, cy2 - 105, "Quarter arc (start_t/end_t)",
                   font_size=13, color="#333", text_anchor="middle",
                   font_weight="bold"))
    scene.add(Text(cx2, cy2 + 110,
                   "Path(ellipse, start_t=0.0, end_t=0.25)",
                   font_size=10, color="#888", text_anchor="middle",
                   font_family="monospace"))

    scene.save(OUTPUT_DIR / "01-basic-arc.svg")


# =============================================================================
# SECTION 2: Segmented circle (multiple arcs with gaps)
# =============================================================================

def example_02_segmented_circle():
    """Show a circle split into arcs with gaps."""
    scene = Scene(width=500, height=500, background="white")

    cx, cy = 250, 260
    e = Ellipse(cx, cy, rx=120, ry=120)

    # Ghost circle
    scene.add(Path(e, closed=True, color="#f1f5f9", width=1))

    n_segments = 8
    gap = 0.015  # gap between segments as fraction of t
    colors = [
        "#3b82f6", "#8b5cf6", "#ec4899", "#ef4444",
        "#f59e0b", "#10b981", "#06b6d4", "#6366f1",
    ]

    for i in range(n_segments):
        t_start = i / n_segments + gap
        t_end = (i + 1) / n_segments - gap
        scene.add(Path(e, start_t=t_start, end_t=t_end,
                       color=colors[i], width=8, cap="round"))

    scene.add(Text(cx, cy, "8", font_size=48, color="#333",
                   text_anchor="middle", baseline="central",
                   font_weight="bold"))
    scene.add(Text(cx, cy + 30, "segments", font_size=14, color="#888",
                   text_anchor="middle"))
    scene.add(Text(cx, 50, "Segmented Circle",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))

    scene.save(OUTPUT_DIR / "02-segmented-circle.svg")


# =============================================================================
# SECTION 3: Progress gauge
# =============================================================================

def example_03_progress_gauge():
    """Show a circular progress gauge."""
    scene = Scene(width=700, height=300, background="white")

    values = [0.25, 0.60, 0.85]
    labels = ["25%", "60%", "85%"]
    colors = ["#ef4444", "#f59e0b", "#10b981"]

    for i, (val, lbl, color) in enumerate(zip(values, labels, colors)):
        cx = 125 + i * 225
        cy = 155
        e = Ellipse(cx, cy, rx=70, ry=70)

        # Background track
        scene.add(Path(e, start_t=0.0, end_t=0.75,
                       color="#e5e7eb", width=12, cap="round"))
        # Progress arc
        scene.add(Path(e, start_t=0.0, end_t=val * 0.75,
                       color=color, width=12, cap="round"))

        # Label
        scene.add(Text(cx, cy + 5, lbl, font_size=28, color=color,
                       text_anchor="middle", baseline="central",
                       font_weight="bold"))

    scene.add(Text(350, 28, "Progress Gauges",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))

    scene.save(OUTPUT_DIR / "03-progress-gauge.svg")


# =============================================================================
# SECTION 4: Spiral sub-section
# =============================================================================

def example_04_spiral_sub():
    """Show a spiral with only a portion rendered."""
    scene = Scene(width=600, height=400, background="white")

    cx, cy = 300, 210
    spiral = Spiral(Point(cx, cy), 10, 150, 3)

    # Full spiral ghost
    scene.add(Path(spiral, color="#e5e7eb", width=1, segments=128))

    # Highlighted sub-section
    scene.add(Path(spiral, start_t=0.3, end_t=0.7,
                   color="#8b5cf6", width=4, segments=64))

    # Mark start and end of sub-section
    p_start = spiral.point_at(0.3)
    p_end = spiral.point_at(0.7)
    scene.add(Dot(p_start.x, p_start.y, radius=6, color="#10b981"))
    scene.add(Dot(p_end.x, p_end.y, radius=6, color="#ef4444"))
    scene.add(Text(p_start.x + 12, p_start.y - 8, "start_t=0.3",
                   font_size=10, color="#10b981"))
    scene.add(Text(p_end.x + 12, p_end.y + 5, "end_t=0.7",
                   font_size=10, color="#ef4444"))

    scene.add(Text(cx, 28, "Spiral Sub-Path",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))
    scene.add(Text(cx, 385, "Works with any Pathable - not just ellipses!",
                   font_size=12, color="#888", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "04-spiral-sub.svg")


# =============================================================================
# SECTION 5: Rainbow arcs
# =============================================================================

def example_05_rainbow_arcs():
    """Show concentric rainbow arcs."""
    scene = Scene(width=600, height=350, background="#1a1a2e")

    cx, cy = 300, 280

    rainbow = [
        ("#ef4444", 140),  # Red
        ("#f97316", 125),  # Orange
        ("#facc15", 110),  # Yellow
        ("#22c55e",  95),  # Green
        ("#3b82f6",  80),  # Blue
        ("#8b5cf6",  65),  # Indigo
        ("#a855f7",  50),  # Violet
    ]

    for color, radius in rainbow:
        e = Ellipse(cx, cy, rx=radius, ry=radius)
        scene.add(Path(e, start_t=0.25, end_t=0.75,
                       color=color, width=10, cap="round"))

    scene.add(Text(cx, 30, "Rainbow Arcs",
                   font_size=18, color="white", text_anchor="middle",
                   font_weight="bold"))

    scene.save(OUTPUT_DIR / "05-rainbow-arcs.svg")


# =============================================================================
# SECTION 6: Combined showcase - loading spinner
# =============================================================================

def example_06_loading_spinner():
    """Show animated-style loading spinners."""
    scene = Scene(width=700, height=300, background="white")

    # Spinner 1: single arc
    cx1 = 125
    cy = 155
    e1 = Ellipse(cx1, cy, rx=50, ry=50)
    scene.add(Path(e1, closed=True, color="#e5e7eb", width=6))
    scene.add(Path(e1, start_t=0.0, end_t=0.3,
                   color="#3b82f6", width=6, cap="round"))
    scene.add(Text(cx1, cy + 80, "Single arc",
                   font_size=11, color="#888", text_anchor="middle"))

    # Spinner 2: dual opposing arcs
    cx2 = 350
    e2 = Ellipse(cx2, cy, rx=50, ry=50)
    scene.add(Path(e2, closed=True, color="#e5e7eb", width=6))
    scene.add(Path(e2, start_t=0.0, end_t=0.3,
                   color="#8b5cf6", width=6, cap="round"))
    scene.add(Path(e2, start_t=0.5, end_t=0.8,
                   color="#8b5cf6", width=6, cap="round"))
    scene.add(Text(cx2, cy + 80, "Dual arcs",
                   font_size=11, color="#888", text_anchor="middle"))

    # Spinner 3: gradient-like segments
    cx3 = 575
    e3 = Ellipse(cx3, cy, rx=50, ry=50)
    n = 12
    for i in range(n):
        opacity = 0.2 + 0.8 * (i / (n - 1))
        t_start = i / n + 0.005
        t_end = (i + 1) / n - 0.005
        scene.add(Path(e3, start_t=t_start, end_t=t_end,
                       color="#10b981", width=6, cap="round",
                       opacity=opacity))
    scene.add(Text(cx3, cy + 80, "Fading segments",
                   font_size=11, color="#888", text_anchor="middle"))

    scene.add(Text(350, 28, "Loading Spinners",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))

    scene.save(OUTPUT_DIR / "06-loading-spinners.svg")


# =============================================================================
# SECTION 7: Curve sub-path
# =============================================================================

def example_07_curve_sub():
    """Show sub-paths work on Curve entities too."""
    scene = Scene(width=600, height=300, background="white")

    # Full curve (ghost)
    c = Curve(50, 250, 550, 250, curvature=0.8, color="#e5e7eb", width=2)
    scene.add(c)

    # Three colored sub-sections
    sections = [
        (0.0, 0.33, "#3b82f6", "First third"),
        (0.33, 0.66, "#ec4899", "Middle third"),
        (0.66, 1.0, "#f59e0b", "Last third"),
    ]

    for s, e, color, lbl in sections:
        scene.add(Path(c, start_t=s, end_t=e,
                       color=color, width=4, cap="round"))
        mid_t = (s + e) / 2
        mid = c.point_at(mid_t)
        scene.add(Text(mid.x, mid.y - 20, lbl,
                       font_size=11, color=color, text_anchor="middle"))

    scene.add(Text(300, 28, "Sub-Paths on Curves",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))
    scene.add(Text(300, 280, "Works on any Pathable: Line, Curve, "
                   "Ellipse, custom paths...",
                   font_size=12, color="#888", text_anchor="middle"))

    scene.save(OUTPUT_DIR / "07-curve-sub.svg")


# =============================================================================
# SECTION 8: Elliptical arcs (rx != ry)
# =============================================================================

def example_08_elliptical_arcs():
    """Show arcs on non-circular ellipses."""
    scene = Scene(width=600, height=350, background="white")

    cx, cy = 300, 190

    # Ghost ellipse
    e = Ellipse(cx, cy, rx=150, ry=80)
    scene.add(Path(e, closed=True, color="#f1f5f9", width=1))

    # Four arcs in different colors
    arcs = [
        (0.0, 0.25, "#3b82f6", "Q1"),
        (0.25, 0.5, "#ec4899", "Q2"),
        (0.5, 0.75, "#f59e0b", "Q3"),
        (0.75, 1.0, "#10b981", "Q4"),
    ]

    for s, en, color, lbl in arcs:
        scene.add(Path(e, start_t=s, end_t=en,
                       color=color, width=5, cap="round"))
        mid_t = (s + en) / 2
        mid = e.point_at(mid_t)
        # Offset label outward from center
        dx = mid.x - cx
        dy = mid.y - cy
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            label_x = mid.x + dx / dist * 25
            label_y = mid.y + dy / dist * 25
        else:
            label_x, label_y = mid.x, mid.y - 20
        scene.add(Text(label_x, label_y, lbl,
                       font_size=12, color=color, text_anchor="middle",
                       font_weight="bold"))

    scene.add(Text(cx, 35, "Elliptical Arcs (rx=150, ry=80)",
                   font_size=18, color="#333", text_anchor="middle",
                   font_weight="bold"))

    scene.save(OUTPUT_DIR / "08-elliptical-arcs.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-basic-arc": example_01_basic_arc,
    "02-segmented-circle": example_02_segmented_circle,
    "03-progress-gauge": example_03_progress_gauge,
    "04-spiral-sub": example_04_spiral_sub,
    "05-rainbow-arcs": example_05_rainbow_arcs,
    "06-loading-spinners": example_06_loading_spinner,
    "07-curve-sub": example_07_curve_sub,
    "08-elliptical-arcs": example_08_elliptical_arcs,
}


def generate_all():
    """Generate all SVG images for this document."""
    print(f"Generating {len(GENERATORS)} SVGs for "
          "08-arcs-and-sub-paths.md...")

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
