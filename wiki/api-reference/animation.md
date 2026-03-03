# Animation & Rendering

Animations add motion to entities. Renderers convert scenes (with or without animations) into output formats.

!!! info "See also"
    For a tutorial introduction, see [Animation](../guide/12-animation.md).

---

## Entity Animation Methods

All entities inherit these methods from the base `Entity` class. Each returns `self` for chaining.

### Universal Methods

::: pyfreeform.core.entity.Entity.animate_fade
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate_move
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate_spin
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate_scale
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate_follow
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.then
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.loop
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.clear_animations
    options:
      heading_level: 4
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animations
    options:
      heading_level: 4
      show_root_full_path: false

### Typed Property Methods

Each entity subclass exposes only the `animate_*` methods that match its constructor parameters. These are factory-generated with typed signatures — IDE autocomplete shows exactly what's available.

**Color properties** — `to` accepts `ColorLike` (`str | tuple[int, int, int]`), `keyframes` accepts `dict[float, ColorLike]` or `list[ColorLike]`:

| Method | Dot | Rect | Polygon | Ellipse | Line/Curve | Path | Text |
|--------|-----|------|---------|---------|------------|------|------|
| `animate_color` | Yes | — | — | — | Yes | Yes | Yes |
| `animate_fill` | — | Yes | Yes | Yes | — | Yes | — |
| `animate_stroke` | — | Yes | Yes | Yes | — | — | — |

**Numeric properties** — `to` accepts `float`, `keyframes` accepts `dict[float, float]` or `list[float]`:

| Method | Dot | Rect | Polygon | Ellipse | Line/Curve | Path | Text |
|--------|-----|------|---------|---------|------------|------|------|
| `animate_radius` | Yes | — | — | — | — | — | — |
| `animate_width` | — | Yes | — | — | Yes | Yes | — |
| `animate_height` | — | Yes | — | — | — | — | — |
| `animate_stroke_width` | — | Yes | Yes | Yes | — | — | — |
| `animate_rx` | — | — | — | Yes | — | — | — |
| `animate_ry` | — | — | — | Yes | — | — | — |
| `animate_font_size` | — | — | — | — | — | — | Yes |
| `animate_fill_opacity` | — | Yes | Yes | Yes | — | — | — |
| `animate_stroke_opacity` | — | Yes | Yes | Yes | — | — | — |

---

## Stroke Draw

Lines, curves, and paths have a stroke-reveal animation method:

::: pyfreeform.entities.line.Line.animate_draw
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.entities.curve.Curve.animate_draw
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.entities.path.Path.animate_draw
    options:
      heading_level: 3
      show_root_full_path: false

---

## Connection Animation Methods

Connections support a subset of animation methods:

::: pyfreeform.core.connection.Connection.animate_fade
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.animate_draw
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.animate
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.then
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.loop
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.clear_animations
    options:
      heading_level: 3
      show_root_full_path: false

---

## Utility Functions

::: pyfreeform.animation.builders.stagger
    options:
      heading_level: 3
      show_root_full_path: false

---

## Animation Data Model

These classes live in `pyfreeform.animation` and represent animation data. You rarely need to create them directly — the entity methods do it for you. They're useful for inspection and custom renderers.

!!! note "bounce / repeat fields"
    The `bounce` and `repeat` fields on animation model classes are **storage** — they are stamped by `.loop()`, not passed directly to `animate_*` methods.

::: pyfreeform.animation.models.Easing
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - x1
        - y1
        - x2
        - y2
        - evaluate
        - LINEAR
        - EASE_IN
        - EASE_OUT
        - EASE_IN_OUT

::: pyfreeform.animation.models.Keyframe
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.animation.models.PropertyAnimation
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - prop
        - keyframes
        - easing
        - hold
        - repeat
        - bounce
        - delay
        - duration
        - evaluate

::: pyfreeform.animation.models.MotionAnimation
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - path
        - duration
        - easing
        - hold
        - repeat
        - bounce
        - delay
        - rotate
        - evaluate

::: pyfreeform.animation.models.DrawAnimation
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - duration
        - easing
        - hold
        - repeat
        - bounce
        - delay
        - reverse
        - evaluate

---

## Renderers

Renderers convert a scene into an output format. The base class defines the interface; concrete renderers implement it.

::: pyfreeform.renderers.base.Renderer
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - render_scene
        - render_entity
        - render_connection

::: pyfreeform.renderers.svg.SVGRenderer
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - render_scene
        - render_entity
        - render_connection

::: pyfreeform.renderers.svg.SMILRenderer
    options:
      heading_level: 3
      show_root_full_path: false
      members:
        - render_scene
        - render_entity
        - render_connection

### Renderer Selection

| Scenario | Renderer | Notes |
|---|---|---|
| `scene.save("out.svg")` | `SMILRenderer` (auto) | Default — includes animations if present |
| `scene.render()` | `SMILRenderer` (auto) | Same as save |
| `scene.render(SVGRenderer())` | `SVGRenderer` | Forces static SVG, ignores animations |
| `scene.render(SMILRenderer())` | `SMILRenderer` | Explicit animated SVG |

Non-animated entities produce identical output from both renderers.
