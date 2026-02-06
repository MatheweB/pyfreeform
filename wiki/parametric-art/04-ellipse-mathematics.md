
# Ellipse Mathematics

Deep dive into parametric ellipses with rotation.

## Parametric Ellipse Equations

**Unrotated ellipse centered at origin:**

```
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)

Where:
  t ∈ [0,1]  : Parameter
  rx         : Horizontal radius (semi-major or semi-minor)
  ry         : Vertical radius
  2πt        : Angle in radians (0 to 2π)
```

![Parametric ellipse with labeled rx, ry radii and t=0 starting point](./_images/04-ellipse-mathematics/01-basic-ellipse.svg)

![Parameter progression around the ellipse from t=0 to t=1](./_images/04-ellipse-mathematics/02-parameter-progression.svg)

## With Rotation

Apply 2D rotation matrix with angle θ:

```
[x']   [cos(θ)  -sin(θ)] [x]
[y'] = [sin(θ)   cos(θ)] [y]

Expanded:
x'(t) = x(t)·cos(θ) - y(t)·sin(θ) + cx
y'(t) = x(t)·sin(θ) + y(t)·cos(θ) + cy

Where:
  (cx, cy) : Center coordinates
  θ        : Rotation angle (radians)
```

![Rotation matrix applied to ellipse coordinates](./_images/04-ellipse-mathematics/04-rotation-matrix.svg)

## Full Formula

```
x'(t) = cx + rx·cos(2πt)·cos(θ) - ry·sin(2πt)·sin(θ)
y'(t) = cy + rx·cos(2πt)·sin(θ) + ry·sin(2πt)·cos(θ)
```

![Comparison of unrotated and 45-degree rotated ellipse](./_images/04-ellipse-mathematics/03-rotation-comparison.svg)

## Circle as Special Case

When rx = ry = r:

```
x(t) = cx + r·cos(2πt)
y(t) = cy + r·sin(2πt)
```

Rotation has no visual effect!

![Circle as a special case of the ellipse when rx equals ry](./_images/04-ellipse-mathematics/05-circle-special-case.svg)

## Eccentricity

Measure of "ovalness":

```
e = sqrt(1 - (b/a)²)

Where:
  a = max(rx, ry) : Semi-major axis
  b = min(rx, ry) : Semi-minor axis

e = 0     : Perfect circle
0 < e < 1 : Ellipse
e = 1     : Parabola (limit)
```

![Ellipses with different eccentricities from circle to elongated](./_images/04-ellipse-mathematics/06-eccentricity-comparison.svg)

## Perimeter Approximation

No exact formula! Ramanujan's approximation:

```
P ≈ π[3(a+b) - sqrt((3a+b)(a+3b))]
```

Better approximation:

```
h = ((a-b)/(a+b))²
P ≈ π(a+b)(1 + 3h/(10 + sqrt(4-3h)))
```

## Area

Exact formula:

```
A = π × rx × ry
```

For circle: A = πr²

![Area formula visualization for ellipses](./_images/04-ellipse-mathematics/09-area-formula.svg)

## Angle vs Parameter

**Not the same!** For non-circles:
- Parameter t → uniform speed around ellipse
- Angle → non-uniform (faster on short axis)

```python
# Parameter t (uniform)
point = ellipse.point_at(0.25)  # 25% around ellipse

# Direct angle (non-uniform)
point = ellipse.point_at_angle(90)  # At 90°
```

![Angle vs parameter difference on an ellipse](./_images/04-ellipse-mathematics/07-angle-vs-parameter.svg)

## Focal Points

For ellipse with a > b:

```
Focal distance from center: c = sqrt(a² - b²)
Foci at: (cx ± c, cy)  # Before rotation

Distance sum property:
  distance(P, F₁) + distance(P, F₂) = 2a
```

![Focal points of an ellipse showing the distance sum property](./_images/04-ellipse-mathematics/08-focal-points.svg)

## See Also
- [Ellipses Entity](../entities/04-ellipses.md)
- [Parametric Paths Example](../examples/advanced/parametric-paths.md)
