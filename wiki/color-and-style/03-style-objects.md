
# Style Objects

Reusable style configuration using dataclasses.

## DotStyle

```python
from pyfreeform.config import DotStyle

style = DotStyle(radius=5, color="coral", z_index=0)

cell.add_dot(style=style)

# Builder methods
large = style.with_radius(10)
blue = style.with_color("blue")
```

![DotStyle Basic](_images/03-style-objects/01-dotstyle-basic.svg)

![DotStyle Builder Methods](_images/03-style-objects/02-dotstyle-builder-methods.svg)

![DotStyle Variations](_images/03-style-objects/03-dotstyle-variations.svg)

## LineStyle

```python
from pyfreeform.config import LineStyle

style = LineStyle(
    width=2,
    color="navy",
    cap="round",  # "round", "square", "butt"
    z_index=0
)

cell.add_line(start="left", end="right", style=style)
```

![LineStyle Basic](_images/03-style-objects/04-linestyle-basic.svg)

![LineStyle Cap Options](_images/03-style-objects/05-linestyle-cap-options.svg)

![LineStyle Widths](_images/03-style-objects/06-linestyle-widths.svg)

## FillStyle

```python
from pyfreeform.config import FillStyle

style = FillStyle(
    color="blue",
    opacity=0.5,
    z_index=0
)

cell.add_fill(style=style)
```

![FillStyle Basic](_images/03-style-objects/07-fillstyle-basic.svg)

![FillStyle Opacity](_images/03-style-objects/08-fillstyle-opacity.svg)

![FillStyle Colors](_images/03-style-objects/09-fillstyle-colors.svg)

## BorderStyle

```python
from pyfreeform.config import BorderStyle

style = BorderStyle(
    width=1,
    color="#cccccc",
    z_index=0
)

cell.add_border(style=style)
```

![BorderStyle Basic](_images/03-style-objects/10-borderstyle-basic.svg)

![BorderStyle Widths](_images/03-style-objects/11-borderstyle-widths.svg)

![BorderStyle Colors](_images/03-style-objects/12-borderstyle-colors.svg)

## ShapeStyle

For filled shapes: Ellipse, Polygon, and Rect via `add_ellipse()` / `add_polygon()`.

```python
from pyfreeform.config import ShapeStyle

style = ShapeStyle(
    color="coral",          # fill color
    stroke="navy",          # stroke color (None = no stroke)
    stroke_width=2,         # stroke width in pixels
    z_index=0
)

cell.add_ellipse(style=style)
cell.add_polygon(shapes.hexagon(), style=style)

# Builder methods
outlined = style.with_stroke("black").with_stroke_width(3)
gold = style.with_color("gold")
```

> **Note:** `color` in ShapeStyle maps to `fill` at the entity level. The style layer uses `color` uniformly across all style classes, while the underlying SVG uses `fill` for shapes.

![ShapeStyle Basic](_images/03-style-objects/15-shapestyle-basic.svg)

![ShapeStyle Variations](_images/03-style-objects/16-shapestyle-variations.svg)

## TextStyle

For text via `add_text()`.

```python
from pyfreeform.config import TextStyle

style = TextStyle(
    font_size=12,
    color="navy",
    font_family="monospace",
    bold=True,
    italic=False,
    z_index=0
)

cell.add_text("Hello", style=style)

# Builder methods
large = style.with_font_size(24)
red = style.with_color("red")
italic_style = style.with_italic()
```

![TextStyle Basic](_images/03-style-objects/17-textstyle-basic.svg)

![TextStyle Variations](_images/03-style-objects/18-textstyle-variations.svg)

## ConnectionStyle

For connections between entities. Replaces raw `dict` usage with a typed class.

```python
from pyfreeform.config import ConnectionStyle

style = ConnectionStyle(
    width=2,
    color="red",
    z_index=0
)

# Use with entity.connect()
dot1.connect(dot2, style=style)

# Or with Connection directly
connection = Connection(dot1, dot2, style=style)

# Builder methods
thick = style.with_width(4)
blue = style.with_color("blue")
```

> **Backward compatible:** `Connection` still accepts plain dicts like `{"width": 2, "color": "red"}`.

![ConnectionStyle Basic](_images/03-style-objects/19-connectionstyle-basic.svg)

## Combined Styles

![Combined Styles](_images/03-style-objects/13-combined-styles.svg)

![Style Reusability](_images/03-style-objects/14-style-reusability.svg)

## See Also
- [Styling](../fundamentals/04-styling.md)
- [Palettes](02-palettes.md)
