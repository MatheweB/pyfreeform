# Animation

PyFreeform supports animations on any entity. Call a method like `.fade()` or `.spin()`, save as SVG, and open in a browser to see it play. Under the hood, animations use SVG SMIL — no JavaScript required.

!!! tip "Browser preview"
    Animated SVGs play automatically when opened in a web browser. They won't animate in image viewers or editors.

## Fade

Animate opacity with `.fade()`. Pass the target opacity and a duration:

```python
dot = Dot(100, 100, radius=30, color="coral")
scene.place(dot)

dot.fade(to=0.0, duration=3.0, easing="ease-in-out")
```

The dot starts fully visible and smoothly fades to invisible over 3 seconds.

<figure markdown>
![Fade animation](../_images/guide/anim-fade.svg){ width="240" }
<figcaption>A coral dot fading to invisible.</figcaption>
</figure>

Fade to any value — `to=0.3` makes the entity ghostly, `to=1.0` fades it *in* (if it started transparent).

## Spin

Rotate an entity with `.spin()`:

```python
rect = Rect.at_center((100, 100), 65, 65, fill="dodgerblue", stroke="white", stroke_width=2)
scene.place(rect)

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
dot = Dot(100, 60, radius=15, color="tomato")
scene.place(dot)

dot.zoom(to=2.5, duration=2.0, easing="ease-in-out", bounce=True, repeat=True)
```

<figure markdown>
![Zoom animation](../_images/guide/anim-zoom.svg){ width="240" }
<figcaption>A dot pulsing between normal size and 2.5&times; — `bounce=True` reverses each cycle.</figcaption>
</figure>

`.zoom(to=)` animates the scale factor over time. This is the animated counterpart to `.scale()` — just as `.spin()` is to `.rotate()`.

## Draw

Paths and connections can draw themselves with `.draw()` — the stroke reveals progressively like a pen tracing the shape:

```python
from pyfreeform.paths import Wave

wave = Path(Wave(start=(30, 55), end=(330, 55), amplitude=30, frequency=3), width=3, color="limegreen")
scene.place(wave)

wave.draw(duration=2.5, easing="ease-in-out")
```

<figure markdown>
![Draw animation](../_images/guide/anim-draw.svg){ width="360" }
<figcaption>A wave path drawing itself from left to right.</figcaption>
</figure>

Connections support `.draw()` too:

```python
d1 = Dot(40, 50, radius=7, color="white")
d2 = Dot(320, 50, radius=7, color="white")
scene.place(d1)
scene.place(d2)

conn = Connection(d1, d2, curvature=0.4, color="skyblue", width=2)
conn.draw(duration=2.0, easing="ease-in-out")
```

<figure markdown>
![Connection animation](../_images/guide/anim-connection.svg){ width="360" }
<figcaption>A curved connection drawing itself between two dots.</figcaption>
</figure>

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
rect.fade(to=0.3, duration=2.0, easing="ease-in-out").spin(360, duration=3.0, repeat=True)
```

This applies both a fade and a spin to the same entity — they play simultaneously.

<figure markdown>
![Chaining](../_images/guide/anim-chaining.svg){ width="240" }
<figcaption>A rect that fades to 30% opacity while spinning forever.</figcaption>
</figure>

## Sequential Chaining

Use `.then()` to start an animation *after* the previous ones finish — no manual delay math:

```python
dot.fade(to=0.0, duration=1.0).then().spin(360, duration=1.0)
```

The spin starts at exactly 1.0 seconds, when the fade ends.

<figure markdown>
![Then chaining](../_images/guide/anim-then.svg){ width="300" }
<figcaption>A dot that fades out, then spins — playing one after the other.</figcaption>
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

dots = [Dot(40 + i * 50, 50, radius=12, color="coral") for i in range(5)]
for d in dots:
    scene.place(d)

stagger(*dots, offset=0.2, each=lambda d: d.fade(to=0.0, duration=1.0))
```

<figure markdown>
![Stagger animation](../_images/guide/anim-stagger.svg){ width="360" }
<figcaption>Five dots fading out one by one — each starts 0.2 seconds after the last.</figcaption>
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

## Generic `animate()`

For properties without a named method, use `.animate()`. This lets you animate any SVG-mappable attribute:

```python
dot.animate("r", to=35, duration=1.2, easing="ease-in-out", repeat=True, bounce=True)
```

<figure markdown>
![Generic animate](../_images/guide/anim-animate.svg){ width="240" }
<figcaption>A dot pulsing between radius 10 and 35 — `bounce=True` reverses each cycle.</figcaption>
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
<figcaption>A combined scene: self-drawing connection, spinning rect with fade, pulsing dot, fading dot, self-drawing zigzag and wave, row of spinning squares.</figcaption>
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
