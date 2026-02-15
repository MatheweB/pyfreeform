# Transforms

All entities support non-destructive transforms — rotation and scale are stored as numbers and applied at render time via SVG `transform`, not baked into geometry. Transforms preserve relative bindings: rotating or scaling an entity that tracks a container-relative position does not destroy that binding.

!!! info "See also"
    For hands-on transform examples, see [Transforms and Layout](../guide/08-transforms-and-layout.md).

---

::: pyfreeform.Entity
    options:
      heading_level: 2
      members:
        - rotate
        - scale
        - rotation
        - scale_factor
        - rotation_center
        - fit_within
        - fit_to_cell

!!! note "Model-space vs world-space"
    - **Model-space** properties (`.radius`, `.width`, `.end`, `.vertices`) are **unchanged** by transforms
    - **World-space** methods (`anchor()`, `bounds()`, `point_at()`) apply rotation and scale automatically
    - **SVG output** uses model-space coordinates with a `transform` attribute

### Per-Entity Pivot Points

Each entity type defines its own natural `rotation_center`:

| Entity | Pivot |
|---|---|
| Dot, Ellipse, Text | Center (position) |
| Rect | Center of rectangle |
| Line, Curve | Chord midpoint (start → end) |
| Polygon | Centroid of vertices |
| Path | Bezier midpoint at t=0.5 |
| EntityGroup | Accumulates in `<g>` transform (children unchanged) |

!!! tip "Text fit_to_cell"
    For **Text** entities, `fit_to_cell(fraction)` adjusts font size (up or down) to fill the cell. Compare with `add_text(fit=True)` which only *shrinks*.
