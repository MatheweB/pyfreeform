---
hide:
  - navigation
  - toc
---

# PyFreeform

**A minimalist, art-focused Python library for creating beautiful generative artwork.**

Whether you're an artist exploring code, a developer seeking creative expression, or a mathematician fascinated by parametric curves — PyFreeform helps you create stunning visual art with Python.

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)

for cell in scene.grid:
    cell.add_dot(color=cell.color)

scene.save("art.svg")
```

---

## Choose Your Path

<div class="grid cards" markdown>

-   **Create art from photos**

    ---

    Transform any photo into generative art using image data to drive visual properties like color, size, and position.

    [Image to Art Guide →](getting-started/03-image-to-art.md)

-   **Learn the fundamentals**

    ---

    Follow our progressive learning path from "hello world" through core concepts to advanced techniques.

    [Your First Artwork →](getting-started/01-your-first-artwork.md)

-   **Browse examples**

    ---

    16 fully-documented examples from beginner to advanced, each with step-by-step breakdowns and SVG outputs.

    [Example Gallery →](examples/index.md)

-   **Mathematical details**

    ---

    Dive into the mathematics behind Bezier curves, ellipse equations, Lissajous curves, and custom parametric paths.

    [Parametric Art →](parametric-art/01-what-is-parametric.md)

-   **Colors & styling**

    ---

    Full control over colors (hex, RGB, named), palettes for consistent aesthetics, and style objects for reuse.

    [Color & Style →](color-and-style/01-color-system.md)

-   **Extend the library**

    ---

    Learn the internal structure and create custom entities, parametric paths, and image processors.

    [Developer Guide →](developer-guide/01-architecture.md)

</div>

---

## Key Features

<div class="grid" markdown>

**Image-Driven Art**
:   Load any image and use its color and brightness data to create generative artwork. Perfect for transforming photos into unique visual styles.

**Grid System**
:   Organize your canvas into cells for structured compositions. Cells provide convenient builder methods and access to image data.

**Dynamic Connections**
:   Link entities through anchor points that automatically update when elements move. Create flowing networks and relationships.

**Parametric Paths**
:   Position elements along lines, curves, and ellipses using a unified interface. Any object with `point_at(t)` works seamlessly.

**Rich Styling**
:   Full control over colors (hex, RGB, named), palettes for consistent aesthetics, and z-index layering for composition depth.

**Pattern Selection**
:   Powerful grid selection methods: `checkerboard()`, `border()`, `where()`, `row()`, `column()` and more for creating patterns.

</div>

---

**Philosophy**: Maximum creative freedom with minimum boilerplate. You focus on the art, PyFreeform handles the SVG rendering.

[GitHub](https://github.com/pyfreeform/pyfreeform){ .md-button }
[API Reference](api-reference/scene.md){ .md-button .md-button--primary }
