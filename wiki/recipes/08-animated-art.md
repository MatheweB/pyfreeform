# Animated Art

Five animations that showcase what's possible when you combine PyFreeform's animation system with parametric curves, fractals, and algorithmic geometry. Every SVG below is pure SMIL — open in a browser to watch it play.

!!! tip "Browser preview"
    Animated SVGs play in web browsers. They won't animate in image viewers or editors like Inkscape.

## Animated Fractal — Koch Snowflake

Build a Koch snowflake iteration by iteration. Each depth level appears in sequence, revealing the fractal's self-similar structure as it grows:

```python
import math
from pyfreeform import Scene, Line

scene = Scene(420, 420, background="#0a0a1a")
cx, cy = 210, 210
r = 420 * 0.38

# Equilateral triangle vertices
v = []
for i in range(3):
    angle = math.radians(-90 + i * 120)
    v.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

def koch_points(p1, p2, depth):
    """Recursively subdivide a segment into Koch curve points."""
    if depth == 0:
        return [p1]
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = (x2 - x1) / 3, (y2 - y1) / 3
    a = (x1 + dx, y1 + dy)
    b = (x1 + 2 * dx, y1 + 2 * dy)
    peak = (
        (a[0] + b[0]) / 2 + math.sqrt(3) / 2 * (a[1] - b[1]),
        (a[1] + b[1]) / 2 + math.sqrt(3) / 2 * (b[0] - a[0]),
    )
    return (
        koch_points(p1, a, depth - 1)
        + koch_points(a, peak, depth - 1)
        + koch_points(peak, b, depth - 1)
        + koch_points(b, p2, depth - 1)
    )

# Build each depth layer with sequential animation
colors = ["#ff6b6b", "#ffd93d", "#6bcb77", "#4d96ff"]
total_delay = 0.0

for d in range(1, 5):
    points = []
    for i in range(3):
        points.extend(koch_points(v[i], v[(i + 1) % 3], d))
    points.append(points[0])

    color = colors[(d - 1) % len(colors)]
    segments = []
    step = max(1, len(points) // 80)
    for j in range(0, len(points) - 1, step):
        end_idx = min(j + step, len(points) - 1)
        line = Line(*points[j], *points[end_idx], width=1.5, color=color, opacity=0.0)
        scene.place(line)
        segments.append(line)

    # Each segment fades in with staggered timing
    dur = 1.5
    per_seg = dur / max(len(segments), 1)
    for k, seg in enumerate(segments):
        seg.animate_fade(to=0.85, duration=0.3,
                         delay=total_delay + k * per_seg, easing="ease-out")
    total_delay += dur + 0.3
```

<figure markdown>
![Koch snowflake animation](../_images/recipes/anim-koch.svg){ width="420" }
<figcaption>A Koch snowflake assembling itself — each fractal depth appears in sequence, colored by iteration.</figcaption>
</figure>

!!! tip "Fractal math"
    Each Koch iteration replaces every line segment with 4 segments at 1/3 the length. After *n* iterations, the snowflake has 3 &times; 4<sup>n</sup> segments. The perimeter grows without bound, but the area converges — a classic fractal paradox.

---

## Lissajous Harmonograph

A dot traces a Lissajous curve in real time while the path draws itself behind it. The frequency ratio `a=5, b=4` creates an intricate closed knot:

```python
import math
from pyfreeform import Scene, Dot, Path
from pyfreeform.paths import Lissajous

scene = Scene(400, 400, background="#0a0a1a")
cx, cy = 200, 200

liss = Lissajous(center=(cx, cy), a=5, b=4, delta=math.pi / 2, size=150)

# The curve draws itself
path = Path(liss, width=2, color="mediumpurple", opacity=0.7)
scene.place(path)
path.animate_draw(duration=6.0, easing="linear")

# A dot follows the same curve
start = liss.point_at(0.0)
tracer = Dot(start.x, start.y, radius=6, color="coral")
scene.place(tracer)
tracer.animate_follow(liss, duration=6.0, easing="linear", repeat=True)

# Glowing center on the tracer — pulse radius, not scale
glow = Dot(start.x, start.y, radius=3, color="white")
scene.place(glow)
glow.animate_follow(liss, duration=6.0, easing="linear", repeat=True)
glow.animate_radius(to=8, duration=0.8, easing="ease-in-out", bounce=True, repeat=True)
```

<figure markdown>
![Lissajous harmonograph](../_images/recipes/anim-lissajous.svg){ width="400" }
<figcaption>A 5:4 Lissajous curve drawing itself while a dot traces the path — like a mathematical Spirograph.</figcaption>
</figure>

!!! tip "Lissajous curves"
    A Lissajous figure is defined by `x = sin(a·t + δ)`, `y = sin(b·t)`. When the frequency ratio `a/b` is rational, the curve closes. Different ratios produce wildly different patterns — try `a=3, b=2` for a figure-eight, or `a=7, b=5` for a complex star-knot.

---

## Spiral Galaxy

Stars bloom outward in golden-angle phyllotaxis order. Each star fades in with staggered timing, recreating the way a spiral galaxy's arms emerge:

```python
import math
from pyfreeform import Scene, Dot, stagger
from pyfreeform.color import hsl

scene = Scene(440, 440, background="#050510")
cx, cy = 220, 220
golden_angle = 137.508
max_r = 440 * 0.44

stars = []
for i in range(1, 201):
    angle = math.radians(i * golden_angle)
    t = i / 200
    r = max_r * math.sqrt(t)
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)

    hue = (40 - t * 220) % 360
    radius = 2.0 + 4.0 * (1 - t)
    dot = Dot(x, y, radius=radius, color=hsl(hue, 0.85, 0.55), opacity=0.0)
    scene.place(dot)
    stars.append(dot)

# Stagger: each star fades in with offset timing
stagger(*stars, offset=0.02,
        each=lambda d: d.animate_fade(to=0.9, duration=0.5, easing="ease-out"))

# Some stars spin for a twinkling effect
for i, dot in enumerate(stars):
    if i % 5 == 0:
        dot.animate_spin(360, duration=8.0 + (i % 3) * 2, repeat=True, easing="linear")
```

<figure markdown>
![Spiral galaxy animation](../_images/recipes/anim-galaxy.svg){ width="440" }
<figcaption>200 stars blooming in golden-angle order — the same pattern that arranges sunflower seeds and galaxy arms.</figcaption>
</figure>

!!! tip "The golden angle"
    The golden angle (137.508&deg;) is 360&deg; / &phi;&sup2; where &phi; is the golden ratio. Placing points at successive golden angles produces the most uniform distribution possible — no two arms ever align, creating the natural spiral patterns found throughout nature.

---

## Breathing Mandala

Concentric rings of dots pulse in and out with phase offsets, creating a hypnotic breathing pattern. Each ring starts its cycle slightly after the previous one:

```python
import math
from pyfreeform import Scene, Dot

scene = Scene(420, 420, background="#0a0a1a")
cx, cy = 210, 210

n_rings = 6
dots_per_ring = [8, 12, 16, 20, 24, 28]
ring_colors = ["coral", "gold", "#ff6b9d", "skyblue", "mediumpurple", "limegreen"]

for ring_idx in range(n_rings):
    n = dots_per_ring[ring_idx]
    r = 30 + ring_idx * 30
    color = ring_colors[ring_idx]
    phase_delay = ring_idx * 0.3

    for j in range(n):
        angle = 2 * math.pi * j / n + ring_idx * 0.15
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        dot = Dot(x, y, radius=4, color=color)
        scene.place(dot)

        dot.animate_radius(to=10, duration=2.0, delay=phase_delay + j * 0.05,
                           easing="ease-in-out", bounce=True, repeat=True)

# Center jewel
center = Dot(cx, cy, radius=8, color="white")
scene.place(center)
center.animate_radius(to=16, duration=1.5, easing="ease-in-out", bounce=True, repeat=True)
center.animate_spin(360, duration=6.0, repeat=True, easing="linear")
```

<figure markdown>
![Breathing mandala](../_images/recipes/anim-mandala.svg){ width="420" }
<figcaption>Six concentric rings of dots pulsing with phase-offset timing — a digital mandala that breathes.</figcaption>
</figure>

---

## Sierpinski Triangle

A Sierpinski triangle that cuts itself out depth by depth. A solid triangle appears first, then progressively smaller center holes are punched out to reveal the fractal:

```python
from pyfreeform import Scene, Polygon

scene = Scene(420, 420, background="#0a0a1a")
bg = "#0a0a1a"

margin = 420 * 0.08
top = (210, margin)
bl = (margin, 420 - margin)
br = (420 - margin, 420 - margin)

def midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

# Solid outer triangle
outer = Polygon([top, bl, br], fill="#ff6b6b", stroke="#ff6b6b",
                stroke_width=0.5, opacity=0.0)
scene.place(outer)
outer.animate_fade(to=0.85, duration=0.6, easing="ease-out", hold=True)

# Collect holes by depth: each depth removes center sub-triangles
corners = [(top, bl, br)]
total_delay = 0.8
max_depth = 5

for d in range(1, max_depth + 1):
    holes, next_corners = [], []
    for v0, v1, v2 in corners:
        m01, m12, m02 = midpoint(v0, v1), midpoint(v1, v2), midpoint(v0, v2)
        holes.append((m01, m12, m02))
        next_corners.extend([(v0, m01, m02), (m01, v1, m12), (m02, m12, v2)])
    corners = next_corners

    per_hole = min(0.04, 1.2 / max(len(holes), 1))
    for k, (h0, h1, h2) in enumerate(holes):
        hole = Polygon([h0, h1, h2], fill=bg, stroke=bg,
                       stroke_width=0.3, opacity=0.0)
        scene.place(hole)
        hole.animate_fade(to=1.0, duration=0.3,
                          delay=total_delay + k * per_hole,
                          easing="ease-out", hold=True)

    total_delay += 1.2 + 0.3
```

<figure markdown>
![Sierpinski triangle](../_images/recipes/anim-sierpinski.svg){ width="420" }
<figcaption>A solid triangle with progressively smaller holes punched out — the Sierpinski pattern emerging depth by depth.</figcaption>
</figure>

!!! tip "Sierpinski's triangle"
    The Sierpinski triangle is one of the simplest fractals: start with a triangle, remove the center, and repeat on each remaining sub-triangle. After *n* iterations you have 3<sup>n</sup> triangles, each at 1/2 the scale. The total area shrinks to zero while the structure retains infinite detail — a hallmark of fractal geometry.

---

## What's Next?

These recipes barely scratch the surface. Try combining techniques:

- **Lissajous + color keyframes**: Animate fill color as a dot traces the curve
- **Galaxy + connections**: Connect nearby stars with self-drawing connections
- **Mandala + .then()**: Sequentially build each ring, then start the breathing animation
- **Fractal + follow**: Trace a dot along a Koch snowflake edge using `.animate_follow()`

[&larr; Hidden Gems](07-hidden-gems.md){ .md-button }
