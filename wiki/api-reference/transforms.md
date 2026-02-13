# Transforms

All entities support non-destructive transforms -- rotation and scale are stored as numbers and applied at render time via SVG `transform`, not baked into geometry.

!!! info "See also"
    For hands-on transform examples including `fit_to_cell` and `fit_within`, see [Transforms and Layout](../guide/08-transforms-and-layout.md).

---

## Entity Transforms

- **`rotate(angle, origin)`** -- Accumulates `rotation` (degrees). Without `origin`, rotates in place. With `origin`, also orbits the entity around that point (resolves relative properties to absolute values first).
- **`scale(factor, origin)`** -- Accumulates `scale_factor` (multiplier). Without `origin`, scales in place. With `origin`, also moves the entity toward/away from that point (resolves relative properties first).

Properties after transforms:

- **Model-space** properties (`.radius`, `.width`, `.end`, `.vertices`) are **unchanged** by transforms
- **World-space** methods (`anchor()`, `bounds()`, `point_at()`) apply rotation and scale automatically
- **SVG output** uses model-space coordinates with a `transform` attribute for rotation and scale

### Per-Entity Pivot Points (`rotation_center`)

| Entity | Pivot |
|---|---|
| Dot, Ellipse, Text | Center (position) |
| Rect | Center of rectangle |
| Line, Curve | Chord midpoint (start-end) |
| Polygon | Centroid of vertices |
| Path | Bezier midpoint at t=0.5 |
| EntityGroup | Accumulates in `<g>` transform (children unchanged) |

---

## Fitting

### fit_within

```python
entity.fit_within(target, scale=1.0, recenter=True, *,
                  at=None, visual=True, rotate=False, match_aspect=False)
```

Scales and positions any entity to fit within a target region.

| Parameter | Description |
|---|---|
| `target` | An `Entity` (uses its inner bounds) or a raw `(min_x, min_y, max_x, max_y)` tuple |
| `scale` | Fraction of target to fill (0.0--1.0). Default 1.0 = fill entire area |
| `recenter` | Center entity within target after scaling |
| `at` | `(rx, ry)` position within target. Available space is constrained by nearest edges |
| `visual` | Include stroke width when measuring bounds (default True) |
| `rotate` | Find the rotation angle that maximizes fill before scaling |
| `match_aspect` | Rotate to match the target's aspect ratio. Mutually exclusive with `rotate` |

### fit_to_cell

```python
entity.fit_to_cell(scale=1.0, recenter=True, *,
                   at=None, visual=True, rotate=False, match_aspect=False)
```

Convenience wrapper -- calls `fit_within()` using the containing cell's bounds as the target. All parameters are forwarded directly.

For **Text** entities, `fit_to_cell(fraction)` adjusts font size (up or down) to fill the cell at `fraction`. Compare with `add_text(fit=True)` which only *shrinks*.
