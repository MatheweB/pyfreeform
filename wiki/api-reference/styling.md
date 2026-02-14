# Styling & Caps

Colors, opacity, style classes, palettes, and the cap system for line endpoints.

!!! info "See also"
    For creative styling techniques and palette usage, see [Colors, Styles, and Palettes](../guide/04-colors-styles-palettes.md).

---

## The Color Parameter Split

!!! danger "Critical API distinction: `fill=` vs `color=`"
    This is the most common source of errors. Using the wrong parameter will raise a `TypeError`.

    | Parameter | Used by |
    |---|---|
    | **`color=`** | Dot, Line, Curve, Text, add_dot, add_line, add_curve, add_text, add_fill, add_border, all style classes |
    | **`fill=`** | Rect, Ellipse, Polygon, add_rect, add_ellipse, add_polygon, Path (closed) |

    `ShapeStyle.color` maps to `fill=` when applied to shapes.

## Color Formats

Anywhere a color is accepted (ColorLike), you can use:

- **Named colors**: `"red"`, `"coral"`, `"navy"`, etc.
- **Hex**: `"#ff0000"`, `"#f00"`, `"#FF0000"`
- **RGB tuple**: `(255, 0, 0)`

## Opacity System

- **`opacity`** on every entity and style: 0.0 (transparent) to 1.0 (opaque). Default 1.0 emits no SVG attribute.
- **`fill_opacity` / `stroke_opacity`** on shapes (Rect, Ellipse, Polygon, Path, ShapeStyle): optional overrides for independent control.
- Simple entities (Dot, Line, Curve, Text, Connection): SVG `opacity` attribute.
- Shapes: SVG `fill-opacity` + `stroke-opacity` attributes.

---

## Style Classes

All 7 style classes are dataclasses with `.with_*()` builder methods for immutable updates:

```python
base_style = LineStyle(width=2, color="coral")
thick_style = base_style.with_width(4)
arrow_style = base_style.with_end_cap("arrow")
```

::: pyfreeform.DotStyle
    options:
      heading_level: 3

::: pyfreeform.LineStyle
    options:
      heading_level: 3

::: pyfreeform.FillStyle
    options:
      heading_level: 3

::: pyfreeform.BorderStyle
    options:
      heading_level: 3

::: pyfreeform.ShapeStyle
    options:
      heading_level: 3

::: pyfreeform.TextStyle
    options:
      heading_level: 3

::: pyfreeform.ConnectionStyle
    options:
      heading_level: 3

---

::: pyfreeform.Palette
    options:
      heading_level: 2

| Palette | Background | Vibe |
|---|---|---|
| `Palette.midnight()` | `#1a1a2e` | Dark blue with coral accent |
| `Palette.sunset()` | `#2d1b4e` | Warm oranges and purples |
| `Palette.ocean()` | `#0a1628` | Cool blues and teals |
| `Palette.forest()` | `#1a2e1a` | Natural greens and earth |
| `Palette.monochrome()` | `#0a0a0a` | Black, white, grays |
| `Palette.paper()` | `#fafafa` | Light, clean, minimalist |
| `Palette.neon()` | `#0d0d0d` | Vibrant neon electric |
| `Palette.pastel()` | `#fef6e4` | Soft, gentle pastels |

---

## Cap System

Line, Curve, Path, and Connection endpoints support caps. All cap parameters are typed as `CapName`, so your IDE will autocomplete the available options.

```python
from pyfreeform import CapName  # Literal["butt", "round", "square", "arrow", "arrow_in", "diamond"]
```

SVG provides three native caps (`"round"`, `"square"`, `"butt"`). PyFreeform extends this with marker-based caps that use SVG `<marker>` elements.

| Built-in Cap | Type | Description |
|---|---|---|
| `"round"` | SVG native | Semicircle extending past the endpoint |
| `"square"` | SVG native | Rectangle extending past the endpoint |
| `"butt"` | SVG native | Flat end, flush with the endpoint |
| `"arrow"` | Marker | Arrowhead pointing away from the path |
| `"arrow_in"` | Marker | Arrowhead pointing into the path |
| `"diamond"` | Marker | Diamond shape centered on the endpoint |

Per-end caps: `start_cap` and `end_cap` override the base `cap`:

```python
line = cell.add_line(start="left", end="right", cap="round", end_cap="arrow")
line.effective_start_cap  # "round" (inherited from cap)
line.effective_end_cap    # "arrow" (overridden)
```

### Creating Custom Caps

A cap shape is just a list of `(x, y)` vertices in a 10x10 grid. No SVG knowledge needed.

::: pyfreeform.cap_shape

::: pyfreeform.register_cap

**Tip position** controls alignment -- the point on your shape that sits exactly at the stroke endpoint:

- `(10, 5)` -- right edge, center height (right-pointing arrow tip)
- `(0, 5)` -- left edge, center height (left-pointing arrow tip)
- `(5, 5)` -- dead center (symmetric shapes like diamonds)

**Directional caps** need a separate reversed shape for the start end. Symmetric caps only need one shape:

```python
# Symmetric -- same shape in both directions
register_cap("diamond", cap_shape(DIAMOND, tip=(5, 5)))

# Directional -- separate start/end shapes
register_cap(
    "arrow",
    cap_shape([(0, 0), (10, 5), (0, 10)], tip=(10, 5)),                 # end: points outward
    start_generator=cap_shape([(10, 0), (0, 5), (10, 10)], tip=(0, 5)),  # start: points outward
)
```
