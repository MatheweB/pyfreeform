# Animation & Rendering

Animations add motion to entities. Renderers convert scenes (with or without animations) into output formats.

!!! info "See also"
    For a tutorial introduction, see [Animation](../guide/12-animation.md).

---

## Entity Animation Methods

All entities inherit these methods from the base `Entity` class. Each returns `self` for chaining.

::: pyfreeform.core.entity.Entity.fade
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.move
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.spin
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.zoom
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.follow
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animate
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.then
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.clear_animations
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.entity.Entity.animations
    options:
      heading_level: 3
      show_root_full_path: false

---

## Path Draw

Paths have an additional method for stroke-reveal animations:

::: pyfreeform.entities.path.Path.draw
    options:
      heading_level: 3
      show_root_full_path: false

---

## Connection Animation Methods

Connections support a subset of animation methods:

::: pyfreeform.core.connection.Connection.fade
    options:
      heading_level: 3
      show_root_full_path: false

::: pyfreeform.core.connection.Connection.draw
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

::: pyfreeform.renderers.svg_smil.SMILRenderer
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
