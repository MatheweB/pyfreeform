
# Positioning Along Paths

The `along=` pattern positions entities parametrically along any path.

## The Pattern

```python
path = cell.add_line(start="left", end="right")  # Or curve, ellipse
cell.add_dot(along=path, t=0.5, radius=3)
```

![Basic along= pattern showing a dot positioned at t=0.5 on a line](./_images/02-positioning-along-paths/01-basic-pattern-line.svg)

## Works With All Pathables

```python
# Line - linear interpolation
line = cell.add_line(start="left", end="right")
cell.add_dot(along=line, t=cell.brightness)

# Curve - Bézier parametric
curve = cell.add_curve(curvature=0.5)
cell.add_dot(along=curve, t=cell.brightness)

# Ellipse - around perimeter
ellipse = cell.add_ellipse(rx=15, ry=10)
cell.add_dot(along=ellipse, t=cell.brightness)
```

![Dot positioned along a line path](./_images/02-positioning-along-paths/02-along-line.svg)

![Dot positioned along a Bezier curve path](./_images/02-positioning-along-paths/03-along-curve.svg)

![Dot positioned along an ellipse path](./_images/02-positioning-along-paths/04-along-ellipse.svg)

![Comparison of all three path types with the same along= interface](./_images/02-positioning-along-paths/05-comparison-all-three.svg)

## Data-Driven Positioning

Use cell data to drive t:

```python
for cell in scene.grid:
    line = cell.add_diagonal(start="bottom_left", end="top_right")

    # Dot position based on brightness (0-1)
    cell.add_dot(
        along=line,
        t=cell.brightness,  # Smooth distribution
        radius=4
    )
```

Creates smooth, organic distributions!

![Step 1: Setting up the grid](./_images/02-positioning-along-paths/06-data-driven-step1-grid.svg)

![Step 2: Adding diagonal lines to each cell](./_images/02-positioning-along-paths/06-data-driven-step2-lines.svg)

![Step 3: Positioning dots along lines based on brightness](./_images/02-positioning-along-paths/06-data-driven-step3-positioned.svg)

![Brightness controls dot position along diagonal lines](./_images/02-positioning-along-paths/07-brightness-distribution.svg)

## Multiple Points

```python
curve = cell.add_curve(curvature=0.5)

# Position multiple dots along curve
for i in range(5):
    t = i / 4  # 0, 0.25, 0.5, 0.75, 1.0
    cell.add_dot(along=curve, t=t, radius=2)
```

![Setting up the curve for multiple point placement](./_images/02-positioning-along-paths/08-multiple-points-step1.svg)

![Five evenly-spaced dots positioned along a curve](./_images/02-positioning-along-paths/08-multiple-points-step2.svg)

![Many points distributed along a curve creating a dense pattern](./_images/02-positioning-along-paths/09-many-points.svg)

![Complete code example output showing data-driven parametric positioning](./_images/02-positioning-along-paths/10-code-example.svg)

## Along= for All Entities

The `along=` pattern works with **every entity type**, not just dots:

```python
curve = cell.add_curve(curvature=0.5, color="gray")

# Position ANY entity along a path
cell.add_dot(along=curve, t=0.3, radius=3, color="red")
cell.add_text("Hello", along=curve, t=0.5, font_size=10, color="white")
cell.add_rect(along=curve, t=0.7, width=8, height=6, fill="coral")
cell.add_ellipse(along=curve, t=0.9, rx=6, ry=4, fill="gold")
```

![All entity types positioned along a single curve](./_images/02-positioning-along-paths/11-along-all-entities.svg)

For **polygons**, the centroid is positioned at the path point:

```python
triangle = [(0, -5), (5, 5), (-5, 5)]
cell.add_polygon(triangle, along=curve, t=0.5, fill="purple")
```

For **lines and curves**, the midpoint is repositioned:

```python
# Small line centered at t=0.5 on the path
cell.add_line(start=(0, 0), end=(10, 0), along=curve, t=0.5, color="blue")
```

## Tangent Alignment (align=True)

By default, entities keep their original orientation. Pass `align=True` to rotate them to follow the path's tangent:

```python
curve = cell.add_curve(curvature=0.5, color="gray")

# Without align: rects stay axis-aligned
cell.add_rect(along=curve, t=0.5, width=8, height=4, fill="blue")

# With align: rects rotate to follow the curve
cell.add_rect(along=curve, t=0.5, width=8, height=4, fill="red", align=True)
```

![Aligned vs non-aligned entities along a curve](./_images/02-positioning-along-paths/12-align-vs-no-align.svg)

This creates beautiful effects when distributing many aligned shapes:

```python
for cell in scene.grid:
    curve = cell.add_curve(curvature=0.4, color="#333", width=0.5)
    for i in range(5):
        t = (i + 0.5) / 5
        cell.add_rect(
            along=curve, t=t, align=True,
            width=6, height=3, fill=cell.color
        )
```

![Rectangles aligned along curves across a grid](./_images/02-positioning-along-paths/13-align-rects-on-curve.svg)

## Text Along Paths (TextPath)

Text has a special mode: call `add_text` with `along=` but **without `t=`** to warp text along the full path using SVG `<textPath>`:

```python
curve = cell.add_curve(start="left", end="right", curvature=0.5)

# Warp text along the curve (no t= parameter)
cell.add_text("Hello World", along=curve, font_size=10, color="white")
```

![Text warped along a curve using textPath](./_images/02-positioning-along-paths/14-textpath-curve.svg)

With `t=`, text is **positioned** at that point (and optionally aligned):

```python
# Position text at t=0.5 (not warped)
cell.add_text("Label", along=curve, t=0.5, align=True, font_size=10)
```

TextPath works with any path that has `to_svg_path_d()` — lines, curves, and ellipses:

![Text warped along an ellipse](./_images/02-positioning-along-paths/15-textpath-ellipse.svg)

## Lines and Curves Along Paths

Dual-position entities (lines, curves) are repositioned at their midpoint. With `align=True`, they also rotate to match the path tangent:

```python
path = cell.add_curve(curvature=0.5, color="gray")

# Distribute small lines along the curve
for i in range(8):
    t = (i + 0.5) / 8
    cell.add_line(
        start=(0, 0), end=(6, 0),
        along=path, t=t, align=True,
        color="coral", width=1.5
    )
```

![Small lines distributed along a path with alignment](./_images/02-positioning-along-paths/16-lines-along-path.svg)

This is especially powerful for creating tick marks, hatching, or decorative patterns that follow any path shape.

![Complete parametric art example with multiple entity types](./_images/02-positioning-along-paths/17-complete-example.svg)

## See Also
- [Curves](../entities/03-curves.md) - Bezier paths
- [Ellipses](../entities/04-ellipses.md) - Circular paths
- [Text Along Paths](../entities/06-text.md#text-along-paths) - TextPath details
- [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
