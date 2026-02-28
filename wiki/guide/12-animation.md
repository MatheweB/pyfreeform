# Animation

PyFreeform supports animations on any entity. Call a method like `.fade()` or `.spin()`, save as SVG, and open in a browser to see it play. Under the hood, animations use SVG SMIL — no JavaScript required.

!!! tip "Browser preview"
    Animated SVGs play automatically when opened in a web browser. They won't animate in image viewers or editors.

## Fade

Animate opacity with `.fade()`. Pass the target opacity and a duration:

```python
dot = cell.add_dot(at="center", radius=0.2, color="coral")

dot.fade(to=0.0, duration=3.0, easing="ease-in-out", bounce=True, repeat=True)
```

The dot pulses — fading to invisible and back again. `bounce=True` reverses each cycle, and `repeat=True` loops forever.

<figure markdown>
![Fade animation](../_images/guide/anim-fade.svg){ width="240" }
<figcaption>A coral dot pulsing between visible and invisible.</figcaption>
</figure>

Fade to any value — `to=0.3` makes the entity ghostly, `to=1.0` fades it *in* (if it started transparent).

## Spin

Rotate an entity with `.spin()`:

```python
rect = cell.add_rect(at="center", width=0.38, height=0.38,
                     fill="dodgerblue", stroke="white", stroke_width=2)

rect.spin(360, duration=2.5, repeat=True, easing="linear")
```

<figure markdown>
![Spin animation](../_images/guide/anim-spin.svg){ width="240" }
<figcaption>A rectangle spinning continuously — `repeat=True` makes it loop forever.</figcaption>
</figure>

The first argument is the total rotation angle in degrees. Use `repeat=True` for continuous spinning.

## Zoom

Animate an entity's scale with `.zoom()`:

```python
dot = cell.add_dot(at="center", radius=0.08, color="tomato")

dot.zoom(to=2.0, duration=2.0, easing="ease-in-out", bounce=True, repeat=True)
```

<figure markdown>
![Zoom animation](../_images/guide/anim-zoom.svg){ width="240" }
<figcaption>A dot pulsing between normal size and 2&times; — `bounce=True` reverses each cycle.</figcaption>
</figure>

`.zoom(to=)` animates the scale factor over time. This is the animated counterpart to `.scale()` — just as `.spin()` is to `.rotate()`.

## Draw

Paths and connections can draw themselves with `.draw()` — the stroke reveals progressively like a pen tracing the shape:

```python
from pyfreeform.paths import Wave

w, h = cell.width, cell.height
wave_shape = Wave(start=(w * 0.08, h * 0.4), end=(w * 0.92, h * 0.4),
                  amplitude=h * 0.28, frequency=3)
path = cell.add_path(wave_shape, width=3, color="limegreen")

path.draw(duration=2.5, easing="ease-in-out", bounce=True, repeat=True)
```

The wave draws itself left to right, then undraws back — `bounce=True` reverses the stroke reveal each cycle.

<figure markdown>
![Draw animation](../_images/guide/anim-draw.svg){ width="360" }
<figcaption>A wave drawing and undrawing itself in a loop.</figcaption>
</figure>

Connections support `.draw()` too:

```python
d1 = cell.add_dot(at=(0.1, 0.42), radius=0.04, color="white")
d2 = cell.add_dot(at=(0.9, 0.42), radius=0.04, color="white")

conn = d1.connect(d2, curvature=0.4, color="skyblue", width=2)
conn.draw(duration=2.0, easing="ease-in-out", bounce=True, repeat=True)
```

<figure markdown>
![Connection animation](../_images/guide/anim-connection.svg){ width="360" }
<figcaption>A curved connection drawing and undrawing itself between two dots.</figcaption>
</figure>

!!! tip "Delayed draw"
    When using `.draw()` with a `delay`, the stroke is fully hidden during the wait — then the draw begins on schedule. Pair it with a fade for a smooth entrance:

    ```python
    conn = d1.connect(d2, color="skyblue", width=2, opacity=0.0)
    conn.fade(to=1.0, duration=0.15, delay=2.0, hold=True)
    conn.draw(duration=1.0, delay=2.0)
    ```

---

## Easing

Easing controls the *speed curve* of an animation — whether it starts slow, ends slow, or moves at constant speed.

Pass a string name:

```python
dot.fade(to=0.0, duration=2.0, easing="ease-in-out")
```

<figure markdown>
![Easing comparison](../_images/guide/anim-easing.svg){ width="440" }
<figcaption>Four dots racing across the same distance — watch how their speeds differ.</figcaption>
</figure>

Available named easings:

| Name | Behavior |
|---|---|
| `"linear"` | Constant speed (default for most animations) |
| `"ease-in"` | Starts slow, accelerates |
| `"ease-out"` | Starts fast, decelerates |
| `"ease-in-out"` | Slow start and end (default for `draw` and `move`) |

You can also pass a custom cubic-bezier as a tuple:

```python
dot.fade(to=0.0, easing=(0.68, -0.55, 0.27, 1.55))  # overshoot
```

Or use the `Easing` class directly:

```python
from pyfreeform import Easing

dot.fade(to=0.0, easing=Easing(0.68, -0.55, 0.27, 1.55))
dot.fade(to=0.0, easing=Easing.EASE_IN_OUT)
```

---

## Common Parameters

Every animation method accepts these parameters:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `duration` | `float` | `1.0` | Duration in seconds |
| `delay` | `float` | `0.0` | Wait this many seconds before starting |
| `easing` | `str \| tuple \| Easing` | `"linear"` | Speed curve (see above) |
| `repeat` | `bool \| int` | `False` | `True` = loop forever, `int` = loop N times |
| `bounce` | `bool` | `False` | Alternate direction each cycle |
| `hold` | `bool` | `True` | Hold final value after animation ends |

---

## Method Chaining

All animation methods return `self`, so you can chain them:

```python
rect = cell.add_rect(at="center", width=0.35, height=0.35,
                     fill="mediumpurple", stroke="white", stroke_width=1)

rect.fade(to=0.3, duration=2.0, easing="ease-in-out",
          bounce=True, repeat=True).spin(360, duration=3.0, repeat=True)
```

This applies both a fade and a spin to the same entity — they play simultaneously. The rect pulses between 30% and full opacity while spinning continuously.

<figure markdown>
![Chaining](../_images/guide/anim-chaining.svg){ width="240" }
<figcaption>A rect pulsing opacity while spinning — both animations play at once.</figcaption>
</figure>

## Sequential Chaining

Use `.then()` to start an animation *after* the previous ones finish — no manual delay math:

```python
rect.fade(to=0.3, duration=1.5, easing="ease-in-out") \
    .then() \
    .spin(360, duration=2.0, easing="ease-in-out")
```

The rect fades to 30% opacity over 1.5 seconds, then spins a full turn. The spin starts at exactly 1.5 seconds — when the fade ends.

<figure markdown>
![Then chaining](../_images/guide/anim-then.svg){ width="300" }
<figcaption>Fade to ghostly, then spin — two steps playing one after the other.</figcaption>
</figure>

Add a gap between animations:

```python
dot.fade(to=0.0, duration=1.0).then(0.5).spin(360, duration=1.0)
# spin starts at 1.5s (1.0 fade + 0.5 gap)
```

Chain as many times as you like:

```python
dot.fade(to=0.5, duration=1.0).then().spin(360, duration=2.0).then().fade(to=1.0, duration=0.5)
```

`.then()` also works on connections:

```python
conn.draw(duration=1.5).then().fade(to=0.0, duration=0.5)
```

## Stagger

Animate a group of entities with offset timing using `stagger()`:

```python
from pyfreeform import stagger

dots = []
for i in range(6):
    dots.append(cell.add_dot(at=(0.1 + i * 0.15, 0.4), radius=0.08, color="coral"))

stagger(*dots, offset=0.3, each=lambda d: d.fade(to=0.0, duration=1.5))
```

<figure markdown>
![Stagger animation](../_images/guide/anim-stagger.svg){ width="360" }
<figcaption>Six dots fading out one by one — each starts 0.3 seconds after the last.</figcaption>
</figure>

The `each` callback applies animation(s) to each entity, and `stagger` offsets the timing by `offset` seconds per entity. You can apply multiple animations at once:

```python
stagger(*dots, offset=0.15, each=lambda d: d.fade(to=0.0).spin(360))
```

## Move

Animate position with `.move()`. Use `to=` for an absolute target, or `by=` for a relative offset:

```python
dot.move(to=(0.8, 0.5), duration=1.0)     # move to position
dot.move(by=(0.1, 0), duration=1.0)        # shift right by 10%
```

Positions are relative coordinates — `(0.0, 0.0)` is the top-left and `(1.0, 1.0)` is the bottom-right of the containing surface.

---

## Reactive Animation

When a **Polygon** references entities as vertices, or a **Connection** references entities as endpoints, those shapes automatically animate when the referenced entities move.

```python
# Four dots in a cell — polygon tracks their positions
p1 = cell.add_dot(at=(0.1, 0.12), radius=0.02, color="white")
p2 = cell.add_dot(at=(0.1, 0.72), radius=0.02, color="white")
p3 = cell.add_dot(at=(0.42, 0.72), radius=0.02, color="white")
p4 = cell.add_dot(at=(0.42, 0.12), radius=0.02, color="white")

poly = Polygon([p1, p2, p3, p4], fill="mediumpurple", stroke="white",
               stroke_width=1, opacity=0.7)
scene.place(poly)

# Move dots inward — polygon follows automatically
p1.move(to=(0.2, 0.28), duration=2.0, bounce=True, repeat=True, easing="ease-in-out")
p2.move(to=(0.16, 0.58), duration=2.0, bounce=True, repeat=True, easing="ease-in-out")
p3.move(to=(0.48, 0.58), duration=2.0, bounce=True, repeat=True, easing="ease-in-out")
p4.move(to=(0.52, 0.28), duration=2.0, bounce=True, repeat=True, easing="ease-in-out")
```

The polygon's shape animates to follow its vertices — no extra code needed.

Connections work the same way:

```python
d1 = cell.add_dot(at=(0.62, 0.2), radius=0.03, color="coral")
d2 = cell.add_dot(at=(0.92, 0.7), radius=0.03, color="gold")
conn = d1.connect(d2, color="skyblue", width=2)

d1.move(to=(0.75, 0.7), duration=2.5, bounce=True, repeat=True, easing="ease-in-out")
# conn follows d1 automatically — both straight lines and curves
```

<figure markdown>
![Reactive animation](../_images/guide/anim-reactive.svg){ width="360" }
<figcaption>Left: polygon vertices react to moving dots. Right: connection follows its endpoints.</figcaption>
</figure>

!!! tip "Mixed timing"
    Vertices and endpoints can have different durations, easings, delays, and even different repeat/bounce settings — each vertex follows its own timing schedule. When timings differ, pyfreeform resamples all animations onto a unified timeline so the shape morphs smoothly.

---

## Generic `animate()`

For properties without a named method, use `.animate()`. This lets you animate any SVG-mappable attribute:

```python
dot = cell.add_dot(at="center", radius=0.06, color="coral")

dot.animate("r", to=35, duration=1.2, easing="ease-in-out", repeat=True, bounce=True)
```

<figure markdown>
![Generic animate](../_images/guide/anim-animate.svg){ width="240" }
<figcaption>A dot pulsing in size — `bounce=True` reverses each cycle.</figcaption>
</figure>

More examples:

```python
rect.animate("fill", to="coral", duration=2.0)         # color transition
rect.animate("width", keyframes={0: 100, 1: 200, 2: 100}, repeat=True)  # multi-step
```

The `keyframes` dict maps times (seconds) to property values at those times.

---

## Renderers

By default, `scene.save()` and `scene.to_svg()` auto-detect animations. If any entity has animations, the output includes SMIL `<animate>` elements. If none do, the SVG is identical to static output.

You can force a specific renderer:

```python
from pyfreeform.renderers import SVGRenderer, SMILRenderer

# Force static SVG (ignore all animations)
scene.render(SVGRenderer())

# Force animated SVG (default behavior)
scene.render(SMILRenderer())
```

---

## Showcase

Here's what happens when you combine multiple animation types in one scene — spinning, fading, pulsing, and drawing all playing together:

<figure markdown>
![Showcase](../_images/guide/anim-showcase.svg){ width="460" }
<figcaption>A combined scene: self-drawing connection, spinning rect with fade, pulsing dot, fading dot, self-drawing paths, and a row of spinning squares.</figcaption>
</figure>

!!! info "See also"
    For the full animation and renderer API, see [Animation & Rendering](../api-reference/animation.md).

---

## What's Next?

You've completed the Guide! Put your skills to work with self-contained projects:

[Browse Recipes &rarr;](../recipes/index.md){ .md-button }

Or explore the complete API reference:

[API Reference &rarr;](../api-reference/index.md){ .md-button }

[&larr; Gradients](11-gradients.md){ .md-button }
