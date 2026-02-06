
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

## See Also
- [Curves](../entities/03-curves.md) - Bézier paths
- [Ellipses](../entities/04-ellipses.md) - Circular paths
- [Pathable Protocol](../advanced-concepts/03-pathable-protocol.md)
