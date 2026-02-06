
# Mathematical Reference

Quick reference for all parametric equations in PyFreeform.

## Lines

**Formula:**
```
P(t) = P₀ + (P₁ - P₀) × t
     = (1-t)P₀ + tP₁
```

**Components:**
```
x(t) = (1-t)x₀ + tx₁
y(t) = (1-t)y₀ + ty₁
```

![Line formula visual reference](./_images/06-mathematical-reference/01-line-reference.svg)

---

## Quadratic Bézier Curves

**Formula:**
```
B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
```

**Expanded:**
```
x(t) = (1-t)²x₀ + 2(1-t)tx₁ + t²x₂
y(t) = (1-t)²y₀ + 2(1-t)ty₁ + t²y₂
```

**Control point from curvature:**
```
P₁ = midpoint + perpendicular × curvature × length / 2
```

![Quadratic Bezier curve visual reference with control points](./_images/06-mathematical-reference/02-bezier-reference.svg)

---

## Ellipses

**Unrotated:**
```
x(t) = rx × cos(2πt)
y(t) = ry × sin(2πt)
```

**With rotation θ:**
```
x'(t) = cx + rx·cos(2πt)·cos(θ) - ry·sin(2πt)·sin(θ)
y'(t) = cy + rx·cos(2πt)·sin(θ) + ry·sin(2πt)·cos(θ)
```

**Properties:**
```
Area = π × rx × ry
Eccentricity = sqrt(1 - (min/max)²)
```

![Ellipse visual reference with rx, ry radii](./_images/06-mathematical-reference/03-ellipse-reference.svg)

---

## Rotation Matrix (2D)

```
[x']   [cos(θ)  -sin(θ)] [x]
[y'] = [sin(θ)   cos(θ)] [y]

Expanded:
x' = x·cos(θ) - y·sin(θ)
y' = x·sin(θ) + y·cos(θ)
```

![Rotation matrix visual reference showing unrotated and rotated ellipse](./_images/06-mathematical-reference/04-rotation-reference.svg)

---

## Custom Paths

**Archimedean Spiral:**
```
θ(t) = t × turns × 2π
r(t) = r₀ + (r₁ - r₀) × t
x(t) = cx + r(t) × cos(θ(t))
y(t) = cy + r(t) × sin(θ(t))
```

**Sinusoidal Wave:**
```
x(t) = x₀ + (x₁ - x₀) × t
y(t) = y₀ + (y₁ - y₀) × t + A·sin(ω·t)
```

**Lissajous Curve:**
```
x(t) = A·sin(a·t + δ)
y(t) = B·sin(b·t)
```

**Superellipse (Squircle):**
```
|x/a|ⁿ + |y/b|ⁿ = 1

Parametric:
x(t) = a × sgn(cos(θ)) × |cos(θ)|^(2/n)
y(t) = b × sgn(sin(θ)) × |sin(θ)|^(2/n)
```

![Custom paths visual reference showing spiral, wave, Lissajous, and superellipse](./_images/06-mathematical-reference/05-custom-paths-reference.svg)

---

## Useful Conversions

**Degrees to Radians:**
```
radians = degrees × π / 180
```

**Radians to Degrees:**
```
degrees = radians × 180 / π
```

**Distance between points:**
```
d = sqrt((x₂-x₁)² + (y₂-y₁)²)
```

**Linear interpolation (LERP):**
```
lerp(a, b, t) = a + (b - a) × t
              = (1-t)a + tb
```

---

![Complete formula reference sheet with all parametric equations](./_images/06-mathematical-reference/06-all-formulas-sheet.svg)

## See Also
- [Bézier Mathematics](03-bezier-mathematics.md)
- [Ellipse Mathematics](04-ellipse-mathematics.md)
- [Custom Paths](05-custom-paths.md)
