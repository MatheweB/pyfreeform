"""Generate animated SVGs for Recipe: Animated Art.

Every SVG uses real SMIL animations — open in a browser to see them play.
"""

from __future__ import annotations

import math

from pyfreeform import Dot, Polygon, Scene, Path as PPath, stagger
from pyfreeform.entities.line import Line
from pyfreeform.color import hsl
from pyfreeform.paths import Lissajous

from wiki._generator import save


def generate():
    _generate_koch_snowflake()
    _generate_lissajous_trace()
    _generate_spiral_galaxy()
    _generate_breathing_mandala()
    _generate_sierpinski_triangle()


# ── 1. Koch Snowflake — animated fractal construction ─────────────────


def _generate_koch_snowflake(size=420, depth=4):
    """Build a Koch snowflake iteration by iteration, each depth drawn in sequence."""
    scene = Scene(size, size, background="#0a0a1a")
    cx, cy = size / 2, size / 2
    r = size * 0.38

    # Equilateral triangle vertices (pointing up)
    v = []
    for i in range(3):
        angle = math.radians(-90 + i * 120)
        v.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

    def koch_points(p1, p2, d):
        """Recursively subdivide a segment into Koch curve points."""
        if d == 0:
            return [p1]
        x1, y1 = p1
        x2, y2 = p2
        dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
        a = (x1 + dx, y1 + dy)
        b = (x1 + 2 * dx, y1 + 2 * dy)
        # Peak of equilateral triangle
        peak = (
            (a[0] + b[0]) / 2 + math.sqrt(3) / 2 * (a[1] - b[1]),
            (a[1] + b[1]) / 2 + math.sqrt(3) / 2 * (b[0] - a[0]),
        )
        return (
            koch_points(p1, a, d - 1)
            + koch_points(a, peak, d - 1)
            + koch_points(peak, b, d - 1)
            + koch_points(b, p2, d - 1)
        )

    # Generate the full snowflake as line segments per depth layer
    total_delay = 0.0
    colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff", "#9b59b6"]

    for d in range(1, depth + 1):
        points = []
        for i in range(3):
            points.extend(koch_points(v[i], v[(i + 1) % 3], d))
        points.append(points[0])  # close the loop

        # Build segments as individual lines for staggered draw
        color = colors[d % len(colors)]
        opacity = 0.3 + 0.7 * (d / depth)  # later iterations more visible
        segments = []
        step = max(1, len(points) // 80)  # limit segment count for performance
        for j in range(0, len(points) - 1, step):
            end_idx = min(j + step, len(points) - 1)
            x1, y1 = points[j]
            x2, y2 = points[end_idx]
            line = Line(x1, y1, x2, y2, width=1.5, color=color, opacity=opacity)
            scene.place(line)
            segments.append(line)

        # Each depth layer fades in sequentially
        dur = 1.5
        per_seg = dur / max(len(segments), 1)
        for k, seg in enumerate(segments):
            seg.fade(to=0.0, duration=0.01)  # start invisible
            seg.animate("opacity", to=opacity, duration=0.3,
                        delay=total_delay + k * per_seg,
                        easing="ease-out", hold=True)
        total_delay += dur + 0.3

    save(scene, "recipes/anim-koch.svg")


# ── 2. Lissajous Harmonograph — dot tracing a curve ──────────────────


def _generate_lissajous_trace(size=400):
    """A dot follows a Lissajous curve while the path draws itself behind it."""
    scene = Scene(size, size, background="#0a0a1a")
    cx, cy = size / 2, size / 2

    liss = Lissajous(center=(cx, cy), a=5, b=4, delta=math.pi / 2, size=size * 0.38)

    # The drawn path
    path = PPath(liss, width=2, color="mediumpurple", opacity=0.7)
    scene.place(path)
    path.draw(duration=6.0, easing="linear")

    # The tracing dot follows the same curve
    start = liss.point_at(0.0)
    tracer = Dot(start.x, start.y, radius=6, color="coral")
    scene.place(tracer)
    tracer.follow(liss, duration=6.0, easing="linear", repeat=True)

    # A faint glow dot that pulses via radius animation (not zoom/scale,
    # which conflicts with animateMotion's coordinate system)
    glow = Dot(start.x, start.y, radius=3, color="white")
    scene.place(glow)
    glow.follow(liss, duration=6.0, easing="linear", repeat=True)
    glow.animate("r", to=8, duration=0.8, easing="ease-in-out", bounce=True, repeat=True)

    save(scene, "recipes/anim-lissajous.svg")


# ── 3. Spiral Galaxy — phyllotaxis bloom ──────────────────────────────


def _generate_spiral_galaxy(size=440, n_stars=200):
    """Stars appear in golden-angle spiral order with staggered zoom."""
    scene = Scene(size, size, background="#050510")
    cx, cy = size / 2, size / 2
    golden_angle = 137.508
    max_r = size * 0.44

    stars = []
    for i in range(1, n_stars + 1):
        angle = math.radians(i * golden_angle)
        t = i / n_stars
        r = max_r * math.sqrt(t)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)

        # Color: inner stars warm, outer stars cool
        hue = (40 - t * 220) % 360
        radius = 2.0 + 4.0 * (1 - t)
        color = hsl(hue, 0.85, 0.55)
        dot = Dot(x, y, radius=radius, color=color, opacity=0.0)
        scene.place(dot)
        stars.append(dot)

    # Stagger: each star zooms in from nothing with offset timing
    stagger(
        *stars,
        offset=0.02,
        each=lambda d: (
            d.animate("opacity", to=0.9, duration=0.5, easing="ease-out", hold=True),
        ),
    )

    # Add a few spinning arms via subtle rotation on outer stars
    for i, dot in enumerate(stars):
        if i % 5 == 0:
            dot.spin(360, duration=8.0 + (i % 3) * 2, repeat=True, easing="linear")

    save(scene, "recipes/anim-galaxy.svg")


# ── 4. Breathing Mandala — concentric rings pulsing ───────────────────


def _generate_breathing_mandala(size=420):
    """Concentric rings of dots that pulse in and out with phase offsets."""
    scene = Scene(size, size, background="#0a0a1a")
    cx, cy = size / 2, size / 2

    n_rings = 6
    dots_per_ring = [8, 12, 16, 20, 24, 28]
    ring_colors = ["coral", "gold", "#ff6b9d", "skyblue", "mediumpurple", "limegreen"]

    for ring_idx in range(n_rings):
        n = dots_per_ring[ring_idx]
        r = 30 + ring_idx * 30
        color = ring_colors[ring_idx]
        phase_delay = ring_idx * 0.3  # each ring starts later

        ring_dots = []
        for j in range(n):
            angle = 2 * math.pi * j / n + ring_idx * 0.15  # slight offset per ring
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            dot = Dot(x, y, radius=4, color=color)
            scene.place(dot)
            ring_dots.append(dot)

        # Pulse: animate radius in/out with bounce
        for j, dot in enumerate(ring_dots):
            per_dot_delay = phase_delay + j * 0.05
            dot.animate(
                "r", to=10, duration=2.0,
                delay=per_dot_delay,
                easing="ease-in-out", bounce=True, repeat=True,
            )
            # Alternate dots also fade
            if j % 2 == 0:
                dot.fade(
                    to=0.3, duration=2.0,
                    delay=per_dot_delay,
                    easing="ease-in-out",
                )

    # Center jewel
    center = Dot(cx, cy, radius=8, color="white")
    scene.place(center)
    center.animate("r", to=16, duration=1.5, easing="ease-in-out", bounce=True, repeat=True)
    center.spin(360, duration=6.0, repeat=True, easing="linear")

    save(scene, "recipes/anim-mandala.svg")


# ── 5. Sierpinski Triangle — recursive fractal bloom ─────────────────


def _generate_sierpinski_triangle(size=420, max_depth=5):
    """A Sierpinski triangle that cuts itself out depth by depth.

    Starts with a solid triangle, then progressively removes the center
    sub-triangle at each depth — revealing the fractal structure as holes
    are punched out.
    """
    bg = "#0a0a1a"
    scene = Scene(size, size, background=bg)

    margin = size * 0.08
    top = (size / 2, margin)
    bl = (margin, size - margin)
    br = (size - margin, size - margin)

    def midpoint(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    # Step 1: solid outer triangle (fades in first)
    outer = Polygon([top, bl, br], fill="#ff6b6b", stroke="#ff6b6b",
                    stroke_width=0.5, opacity=0.0)
    scene.place(outer)
    outer.animate("opacity", to=0.85, duration=0.6, easing="ease-out", hold=True)

    # Step 2: collect holes by depth — at each depth, the center triangle
    # of every remaining sub-triangle gets "cut out" (drawn in bg color).
    #   depth 1: 1 hole   (center of the whole triangle)
    #   depth 2: 3 holes  (centers of the 3 corner sub-triangles)
    #   depth d: 3^(d-1) holes
    corners = [(top, bl, br)]
    holes_by_depth: dict[int, list[tuple]] = {}

    for d in range(1, max_depth + 1):
        holes = []
        next_corners = []
        for v0, v1, v2 in corners:
            m01, m12, m02 = midpoint(v0, v1), midpoint(v1, v2), midpoint(v0, v2)
            holes.append((m01, m12, m02))  # center = the hole
            next_corners.extend([(v0, m01, m02), (m01, v1, m12), (m02, m12, v2)])
        holes_by_depth[d] = holes
        corners = next_corners

    # Step 3: animate each depth layer's holes appearing
    total_delay = 0.8  # after outer triangle fades in

    for d in range(1, max_depth + 1):
        holes = holes_by_depth[d]
        per_hole = min(0.04, 1.2 / max(len(holes), 1))

        for k, (h0, h1, h2) in enumerate(holes):
            hole = Polygon([h0, h1, h2], fill=bg, stroke=bg,
                           stroke_width=0.3, opacity=0.0)
            scene.place(hole)
            hole.animate(
                "opacity", to=1.0, duration=0.3,
                delay=total_delay + k * per_hole,
                easing="ease-out", hold=True,
            )

        total_delay += 1.2 + 0.3

    save(scene, "recipes/anim-sierpinski.svg")


if __name__ == "__main__":
    generate()
