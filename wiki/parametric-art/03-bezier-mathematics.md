
# Bézier Mathematics

Deep dive into the quadratic Bézier curves used in PyFreeform.

## The Quadratic Bézier Formula

```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂

Components:
  (1-t)²      : Weight on start point
  2(1-t)t     : Weight on control point  
  t²          : Weight on end point

Total weight = (1-t)² + 2(1-t)t + t² = 1 (always!)
```

![Quadratic Bezier curve with labeled control points P0, P1, P2](./_images/03-bezier-mathematics/01-bezier-basic.svg)

![Individual weight components (1-t)², 2(1-t)t, and t² of the Bezier formula](./_images/03-bezier-mathematics/02-weight-components.svg)

## Expanded Form

```
x(t) = (1-t)²·x₀ + 2(1-t)t·x₁ + t²·x₂
y(t) = (1-t)²·y₀ + 2(1-t)t·y₁ + t²·y₂

Where:
  P₀ = (x₀, y₀) : Start point
  P₁ = (x₁, y₁) : Control point
  P₂ = (x₂, y₂) : End point
  t ∈ [0,1]     : Parameter
```

## Weight Distribution

At different t values:

| t | (1-t)² | 2(1-t)t | t² | Point |
|---|--------|---------|-----|-------|
| 0.0 | 1.0 | 0.0 | 0.0 | P₀ (start) |
| 0.25 | 0.5625 | 0.375 | 0.0625 | Near start |
| 0.5 | 0.25 | 0.5 | 0.25 | Midpoint |
| 0.75 | 0.0625 | 0.375 | 0.5625 | Near end |
| 1.0 | 0.0 | 0.0 | 1.0 | P₂ (end) |

The control point has maximum influence at t=0.5!

![How the control point influences the shape of the curve](./_images/03-bezier-mathematics/04-control-point-influence.svg)

![Weight distribution at different t values along the Bezier curve](./_images/03-bezier-mathematics/03-weight-distribution.svg)

## Derivatives

### First Derivative (Velocity/Tangent)

```
B'(t) = 2(1-t)(P₁ - P₀) + 2t(P₂ - P₁)
```

Gives the tangent direction at any point.

### Second Derivative (Acceleration/Curvature)

```
B''(t) = 2(P₂ - 2P₁ + P₀)
```

Constant for quadratic Bézier!

## Control Point from Curvature

PyFreeform calculates P₁ from the curvature parameter:

```
1. midpoint = (P₀ + P₂) / 2

2. direction = P₂ - P₀
   length = ||direction||

3. perpendicular = rotate(direction, 90°)
   unit_perp = perpendicular / length

4. offset = curvature × length / 2

5. P₁ = midpoint + unit_perp × offset
```

![How the control point is calculated from the curvature parameter](./_images/03-bezier-mathematics/09-curvature-calculation.svg)

## De Casteljau's Algorithm

Alternative way to evaluate - numerically stable:

```
# Linear interpolations
Q₀ = (1-t)P₀ + tP₁
Q₁ = (1-t)P₁ + tP₂

# Final point
B(t) = (1-t)Q₀ + tQ₁
```

Same result, different computation!

![De Casteljau step 1: Linear interpolation between adjacent control points](./_images/03-bezier-mathematics/05-de-casteljau-step1.svg)

![De Casteljau step 2: Final interpolation to find the point on the curve](./_images/03-bezier-mathematics/06-de-casteljau-step2.svg)

## Properties

1. **Interpolation**: Passes through P₀ and P₂
2. **Tangent**: Tangent at P₀ points toward P₁
3. **Convex hull**: Curve stays within triangle P₀P₁P₂
4. **Affine invariance**: Transform points = transform curve

![Tangent property showing tangent directions at start and end points](./_images/03-bezier-mathematics/08-tangent-property.svg)

![Convex hull property showing the curve stays within triangle P0 P1 P2](./_images/03-bezier-mathematics/07-convex-hull.svg)

## Arc Length

No closed form! Numerical approximation:

```python
def arc_length(curve, segments=100):
    length = 0
    prev = curve.point_at(0)
    
    for i in range(1, segments + 1):
        curr = curve.point_at(i / segments)
        length += prev.distance_to(curr)
        prev = curr
    
    return length
```

## See Also
- [Curves Entity](../entities/03-curves.md)
- [Custom Paths](05-custom-paths.md)
