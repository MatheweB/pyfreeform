"""Generate animated SVGs for Recipe: Animated Art.

Every SVG uses real SMIL animations — open in a browser to see them play.
All examples use relative coordinates via Scene.with_grid and cell add_* methods.
"""

from __future__ import annotations

import math

from pyfreeform import Polygon, Scene, stagger
from pyfreeform.color import hsl
from pyfreeform.paths import Lissajous

from wiki._generator import save


def generate():
    _generate_mandelbrot()
    _generate_lissajous_trace()
    _generate_spiral_galaxy()
    _generate_breathing_mandala()
    _generate_sierpinski_triangle()


# ── 1. Mandelbrot Set — animated fractal reveal ──────────────────────


def _generate_mandelbrot(max_iter=50):
    """Reveal the Mandelbrot set iteration by iteration, then dissolve back.

    Each cell maps to a point on the complex plane. Cells are colored by
    escape iteration and fade in band-by-band — low iterations first,
    high iterations (near the boundary) last. The whole sequence then
    bounces in reverse and loops forever.
    """
    cols, rows = 100, 100
    scene = Scene.with_grid(
        cols=cols, rows=rows, cell_size=4, background="#0a0a1a",
    )

    # Map grid to complex plane: x ∈ [-2, 0.5], y ∈ [-1.25, 1.25]
    x_min, x_max = -2.0, 0.5
    y_min, y_max = -1.25, 1.25

    # (fill_entity, appear_delay) tuples grouped by escape iteration
    by_iter: dict[int, list] = {}

    for row in range(rows):
        for col in range(cols):
            cell = scene.grid[row][col]

            # Cell center → complex coordinate
            cx = x_min + (col + 0.5) / cols * (x_max - x_min)
            cy = y_min + (row + 0.5) / rows * (y_max - y_min)
            c = complex(cx, cy)

            # Iterate z = z² + c
            z = 0 + 0j
            escape = max_iter
            for i in range(max_iter):
                z = z * z + c
                if z.real * z.real + z.imag * z.imag > 4:
                    escape = i
                    break

            if escape == max_iter:
                # Inside the set — subtle dark fill
                cell.add_fill(color="#0c0c2a")
                continue

            # Smooth HSL gradient: warm (low iter) → cool (near boundary)
            t = escape / max_iter
            hue_val = (240 + t * 300) % 360
            lightness = 0.35 + 0.3 * t
            color = hsl(hue_val, 0.85, lightness)
            fill = cell.add_fill(color=color, opacity=0.0)
            by_iter.setdefault(escape, []).append(fill)

    # Compute per-band appear delays
    delay = 0.0
    band_delays: list[tuple[float, list]] = []
    for i in sorted(by_iter):
        band_delays.append((delay, by_iter[i]))
        delay += 0.06

    # Total forward time + brief hold before bounce
    forward_time = delay + 0.5

    # Keyframe animation: build up → hold → bounce back → loop
    for appear, fills in band_delays:
        for fill in fills:
            fill.animate_fade(
                keyframes={0: 0, appear: 0, appear + 0.4: 1.0,
                           forward_time: 1.0},
            )
            fill.loop(bounce=True)

    save(scene, "recipes/anim-mandelbrot.svg")


# ── 2. Lissajous Harmonograph — dot tracing a curve ──────────────────


def _generate_lissajous_trace():
    """A dot follows a Lissajous curve while the path draws itself behind it.

    Uses cell pixel dimensions for the Pathable (required by add_path/follow),
    but all entities are placed via cell add_* methods.
    """
    scene = Scene.with_grid(cols=1, rows=1, cell_size=400, background="#0a0a1a")
    cell = scene.grid[0][0]
    w, h = cell.width, cell.height
    cx_px, cy_px = cell.center

    liss = Lissajous(
        center=(cx_px, cy_px), a=5, b=4,
        delta=math.pi / 2, size=w * 0.38,
    )

    # The drawn path
    path = cell.add_path(liss, width=2, color="mediumpurple", opacity=0.7)
    path.animate_draw(duration=6.0, easing="linear")

    # Place tracer dot at the Lissajous starting position
    start = liss.point_at(0.0)
    start_rx, start_ry = start.x / w, start.y / h

    tracer = cell.add_dot(at=(start_rx, start_ry), radius=0.015, color="coral")
    tracer.animate_follow(liss, duration=6.0, easing="linear")
    tracer.loop()

    # Glow dot that pulses
    glow = cell.add_dot(at=(start_rx, start_ry), radius=0.008, color="white")
    glow.animate_follow(liss, duration=6.0, easing="linear")
    glow.animate_radius(to=8, duration=0.8, easing="ease-in-out")
    glow.loop(bounce=True)

    save(scene, "recipes/anim-lissajous.svg")


# ── 3. Spiral Galaxy — phyllotaxis bloom ──────────────────────────────


def _generate_spiral_galaxy(n_stars=200):
    """Stars appear in golden-angle spiral order with staggered scale.

    All positions use relative coords within a single cell.
    """
    scene = Scene.with_grid(cols=1, rows=1, cell_size=440, background="#050510")
    cell = scene.grid[0][0]

    golden_angle = 137.508
    max_r = 0.44  # relative radius

    stars = []
    for i in range(1, n_stars + 1):
        angle = math.radians(i * golden_angle)
        t = i / n_stars
        r = max_r * math.sqrt(t)
        rx = 0.5 + r * math.cos(angle)
        ry = 0.5 + r * math.sin(angle)

        # Inner stars warm, outer stars cool
        hue = (40 - t * 220) % 360
        color = hsl(hue, 0.85, 0.55)
        star_size = 0.015 + 0.025 * (1 - t)  # inner stars larger
        dot = cell.add_polygon(
            Polygon.star(size=star_size, center=(rx, ry)),
            fill=color, opacity=0.0,
        )
        stars.append(dot)

    # Stagger: each star fades in with offset timing
    stagger(
        *stars,
        offset=0.02,
        each=lambda d: d.animate_fade(to=0.9, duration=0.5,
                                 easing="ease-out", hold=True),
    )

    # A few spinning "arms" via subtle rotation on outer stars
    for i, dot in enumerate(stars):
        if i % 5 == 0:
            dot.animate_spin(360, duration=8.0 + (i % 3) * 2,
                     easing="linear")
            dot.loop()

    save(scene, "recipes/anim-galaxy.svg")


# ── 4. Breathing Mandala — concentric rings pulsing ───────────────────


def _generate_breathing_mandala():
    """Concentric rings of dots that pulse in and out with phase offsets.

    All positions use relative coords within a single cell.
    """
    scene = Scene.with_grid(cols=1, rows=1, cell_size=420, background="#0a0a1a")
    cell = scene.grid[0][0]

    n_rings = 6
    dots_per_ring = [8, 12, 16, 20, 24, 28]
    ring_colors = ["coral", "gold", "#ff6b9d", "skyblue", "mediumpurple",
                   "limegreen"]

    for ring_idx in range(n_rings):
        n = dots_per_ring[ring_idx]
        r = 0.07 + ring_idx * 0.07  # relative radius from center
        color = ring_colors[ring_idx]
        phase_delay = ring_idx * 0.3

        ring_dots = []
        for j in range(n):
            angle = 2 * math.pi * j / n + ring_idx * 0.15
            rx = 0.5 + r * math.cos(angle)
            ry = 0.5 + r * math.sin(angle)
            dot = cell.add_dot(at=(rx, ry), radius=0.01, color=color)
            ring_dots.append(dot)

        # Pulse: animate radius in/out with bounce
        for j, dot in enumerate(ring_dots):
            per_dot_delay = phase_delay + j * 0.05
            dot.animate_radius(
                to=10, duration=2.0,
                delay=per_dot_delay,
                easing="ease-in-out",
            )
            # Alternate dots also pulse opacity
            if j % 2 == 0:
                dot.animate_fade(
                    to=0.3, duration=2.0,
                    delay=per_dot_delay,
                    easing="ease-in-out",
                )
            dot.loop(bounce=True)

    # Center jewel
    center = cell.add_dot(at=(0.5, 0.5), radius=0.02, color="white")
    center.animate_radius(to=16, duration=1.5, easing="ease-in-out")
    center.animate_spin(360, duration=6.0, easing="linear")
    center.loop(bounce=True)

    save(scene, "recipes/anim-mandala.svg")


# ── 5. Sierpinski Triangle — recursive fractal bloom ─────────────────


def _generate_sierpinski_triangle(max_depth=5):
    """A Sierpinski triangle that cuts itself out depth by depth, then reverses.

    All geometry uses relative coords (0–1) within a single cell.
    Builds the fractal forward, holds briefly, then unbuilds in reverse
    order — elements that appeared last disappear first. Loops forever.
    """
    bg = "#0a0a1a"
    scene = Scene.with_grid(cols=1, rows=1, cell_size=420, background=bg)
    cell = scene.grid[0][0]

    margin = 0.08
    top = (0.5, margin)
    bl = (margin, 1.0 - margin)
    br = (1.0 - margin, 1.0 - margin)

    def midpoint(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    # Collect all elements with their appear times
    elements: list[tuple] = []  # (entity, appear_time, target_opacity, fade_dur)

    # Step 1: solid outer triangle
    outer = cell.add_polygon(
        [top, bl, br], fill="#ff6b6b", stroke="#ff6b6b",
        stroke_width=0.5, opacity=0.0,
    )
    elements.append((outer, 0.0, 0.85, 0.6))

    # Step 2: collect holes by depth
    corners = [(top, bl, br)]
    holes_by_depth: dict[int, list[tuple]] = {}

    for d in range(1, max_depth + 1):
        holes = []
        next_corners = []
        for v0, v1, v2 in corners:
            m01 = midpoint(v0, v1)
            m12 = midpoint(v1, v2)
            m02 = midpoint(v0, v2)
            holes.append((m01, m12, m02))
            next_corners.extend([
                (v0, m01, m02), (m01, v1, m12), (m02, m12, v2),
            ])
        holes_by_depth[d] = holes
        corners = next_corners

    # Step 3: create hole polygons with staggered appear times
    total_delay = 0.8  # after outer triangle fades in

    for d in range(1, max_depth + 1):
        holes = holes_by_depth[d]
        per_hole = min(0.04, 1.2 / max(len(holes), 1))

        for k, (h0, h1, h2) in enumerate(holes):
            hole = cell.add_polygon(
                [h0, h1, h2], fill=bg, stroke=bg,
                stroke_width=0.3, opacity=0.0,
            )
            elements.append((hole, total_delay + k * per_hole, 1.0, 0.3))

        total_delay += 1.2 + 0.3

    # Step 4: animate with keyframes + bounce so the whole sequence
    # plays forward (build), then reverses (unbuild), looping forever.
    forward_time = total_delay + 0.5  # brief hold of complete fractal

    for entity, appear, target, dur in elements:
        entity.animate_fade(
            keyframes={0: 0, appear: 0, appear + dur: target,
                       forward_time: target},
        )
        entity.loop(bounce=True)

    save(scene, "recipes/anim-sierpinski.svg")


if __name__ == "__main__":
    generate()
