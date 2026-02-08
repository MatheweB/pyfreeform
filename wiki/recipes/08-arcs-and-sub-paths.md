
# Recipe: Arcs & Sub-Paths

Render any portion of a path using `start_t` and `end_t` — turning ellipses into arcs, curves into segments, and spirals into slices.

---

## Visual Result

![Rainbow arcs](./_images/08-arcs-and-sub-paths/05-rainbow-arcs.svg)

Concentric arcs created by rendering sub-sections of ellipses.

---

## Why This Works

Every pathable entity in pyfreeform uses a parameter `t` from 0.0 to 1.0 to define positions along its path. By default, `Path()` renders the full range. With `start_t` and `end_t`, you render only a slice — and this works on **any** pathable: ellipses, curves, spirals, or your own custom paths.

No new entity type needed. No special arc math. Just two parameters.

!!! tip "When to Use This Technique"
    Choose sub-paths when you want:

    - Circular or elliptical arcs (progress bars, gauges, pie slices)
    - Segmented circles with gaps between sections
    - Highlighted portions of a larger path
    - Loading spinner patterns
    - Rainbow or gradient arc effects

---

## The Pattern

**Key Idea**: Pass `start_t` and `end_t` to `Path()` or `cell.add_path()` to render only part of a pathable.

```python
from pyfreeform import Ellipse, Path

# Create an ellipse (or any pathable)
ellipse = Ellipse(100, 100, rx=50, ry=50)

# Render just a quarter of it
arc = Path(ellipse, start_t=0.0, end_t=0.25, color="blue", width=3)
scene.add(arc)
```

The `t` values map to positions along the path:

- **Ellipse**: `t=0.0` is the right (3 o'clock), `t=0.25` is the bottom, `t=0.5` is the left, `t=0.75` is the top
- **Line/Curve**: `t=0.0` is the start point, `t=1.0` is the end point
- **Custom paths**: whatever your `point_at()` defines

---

## Basic Arc

![Basic arc comparison](./_images/08-arcs-and-sub-paths/01-basic-arc.svg)

```python
from pyfreeform import Ellipse, Path

ellipse = Ellipse(200, 200, rx=80, ry=80)

# Full ellipse
scene.add(Path(ellipse, closed=True, color="gray"))

# Quarter arc
scene.add(Path(ellipse, start_t=0.0, end_t=0.25, color="blue", width=4))
```

---

## Segmented Circle

Split a circle into colored segments with small gaps between them.

![Segmented circle](./_images/08-arcs-and-sub-paths/02-segmented-circle.svg)

```python
ellipse = Ellipse(cx, cy, rx=120, ry=120)

n_segments = 8
gap = 0.015  # small gap between segments

colors = ["#3b82f6", "#8b5cf6", "#ec4899", "#ef4444",
          "#f59e0b", "#10b981", "#06b6d4", "#6366f1"]

for i in range(n_segments):
    t_start = i / n_segments + gap
    t_end = (i + 1) / n_segments - gap
    scene.add(Path(ellipse, start_t=t_start, end_t=t_end,
                   color=colors[i], width=8, cap="round"))
```

---

## Progress Gauge

Create circular progress indicators by layering a background track with a foreground arc.

![Progress gauges](./_images/08-arcs-and-sub-paths/03-progress-gauge.svg)

```python
ellipse = Ellipse(cx, cy, rx=70, ry=70)
progress = 0.6  # 60%

# Background track (3/4 circle)
scene.add(Path(ellipse, start_t=0.0, end_t=0.75,
               color="#e5e7eb", width=12, cap="round"))

# Progress arc
scene.add(Path(ellipse, start_t=0.0, end_t=progress * 0.75,
               color="#10b981", width=12, cap="round"))
```

---

## Spiral Sub-Section

Sub-paths work on any pathable — not just ellipses.

![Spiral sub-path](./_images/08-arcs-and-sub-paths/04-spiral-sub.svg)

```python
class Spiral:
    def __init__(self, center, start_r, end_r, turns):
        self.center = center
        self.start_r = start_r
        self.end_r = end_r
        self.turns = turns

    def point_at(self, t):
        angle = t * self.turns * 2 * math.pi
        radius = self.start_r + (self.end_r - self.start_r) * t
        return Point(
            self.center.x + radius * math.cos(angle),
            self.center.y + radius * math.sin(angle),
        )

spiral = Spiral(Point(300, 200), 10, 150, 3)

# Full spiral (ghost)
scene.add(Path(spiral, color="#e5e7eb", width=1, segments=128))

# Highlighted sub-section
scene.add(Path(spiral, start_t=0.3, end_t=0.7,
               color="#8b5cf6", width=4, segments=64))
```

---

## Curve Sub-Paths

Split a curve into colored thirds.

![Curve sub-paths](./_images/08-arcs-and-sub-paths/07-curve-sub.svg)

```python
curve = Curve(50, 250, 550, 250, curvature=0.8)

scene.add(Path(curve, start_t=0.0, end_t=0.33, color="#3b82f6", width=4))
scene.add(Path(curve, start_t=0.33, end_t=0.66, color="#ec4899", width=4))
scene.add(Path(curve, start_t=0.66, end_t=1.0, color="#f59e0b", width=4))
```

---

## Elliptical Arcs

Arcs on non-circular ellipses (rx != ry) work naturally.

![Elliptical arcs](./_images/08-arcs-and-sub-paths/08-elliptical-arcs.svg)

```python
ellipse = Ellipse(cx, cy, rx=150, ry=80)

# Four quadrant arcs
scene.add(Path(ellipse, start_t=0.0, end_t=0.25, color="#3b82f6", width=5))
scene.add(Path(ellipse, start_t=0.25, end_t=0.5, color="#ec4899", width=5))
scene.add(Path(ellipse, start_t=0.5, end_t=0.75, color="#f59e0b", width=5))
scene.add(Path(ellipse, start_t=0.75, end_t=1.0, color="#10b981", width=5))
```

---

## Loading Spinners

Create spinner patterns using arcs with varying opacity.

![Loading spinners](./_images/08-arcs-and-sub-paths/06-loading-spinners.svg)

```python
ellipse = Ellipse(cx, cy, rx=50, ry=50)

# Fading segments spinner
n = 12
for i in range(n):
    opacity = 0.2 + 0.8 * (i / (n - 1))
    t_start = i / n + 0.005
    t_end = (i + 1) / n - 0.005
    scene.add(Path(ellipse, start_t=t_start, end_t=t_end,
                   color="#10b981", width=6, cap="round",
                   opacity=opacity))
```

---

## In Cells

Sub-paths work with `cell.add_path()` too:

```python
for cell in scene.grid:
    ellipse = cell.add_ellipse(rx=15, ry=15, fill=None)

    # Arc length based on brightness
    cell.add_path(ellipse, start_t=0.0, end_t=cell.brightness,
                  color=cell.color, width=2, cap="round")
```

---

## API Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `start_t` | `float` | `0.0` | Start position on the pathable (0.0-1.0) |
| `end_t` | `float` | `1.0` | End position on the pathable (0.0-1.0) |

These parameters work on both `Path()` (direct) and `cell.add_path()` (in cells).

The sub-path itself is also pathable — `arc.point_at(0.0)` returns the start of the arc, and `arc.point_at(1.0)` returns the end.
