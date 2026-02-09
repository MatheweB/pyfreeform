---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# PyFreeform

<p class="tagline">Turn images into art with Python.</p>

![Hero artwork](_images/home/hero-mona-lisa.svg){ width="500" }

</div>

---

## Three Lines of Code, Infinite Possibilities

<div class="image-row" markdown>

<figure markdown>
![Hexagonal pattern](_images/home/snippet-hexagons.svg){ width="320" }
<figcaption>Geometric patterns</figcaption>
</figure>

<figure markdown>
![Flowing curves](_images/home/snippet-curves.svg){ width="320" }
<figcaption>Flowing curves</figcaption>
</figure>

<figure markdown>
![Star field](_images/home/snippet-stars.svg){ width="320" }
<figcaption>Parametric shapes</figcaption>
</figure>

</div>

```python
from pyfreeform import Scene

scene = Scene.from_image("photo.jpg", grid_size=40)
for cell in scene.grid:
    cell.add_dot(radius=cell.brightness * 4, color=cell.color)
scene.save("artwork.svg")
```

---

## Choose Your Path

<div class="grid cards" markdown>

-   **Getting Started**

    ---

    Install PyFreeform and create your first artwork in minutes.

    [Get started &rarr;](getting-started/01-installation.md)

-   **Guide**

    ---

    Learn every feature through progressive, visual examples.

    [Start learning &rarr;](guide/01-scenes-and-grids.md)

-   **Recipes**

    ---

    Build complete projects: portraits, patterns, typography, and more.

    [Browse recipes &rarr;](recipes/01-image-to-art.md)

-   **API Surface**

    ---

    Comprehensive reference for every class, method, and parameter.

    [Explore the API &rarr;](api-surface/index.md)

</div>

---

## Install

```bash
pip install pyfreeform
```

Requires Python 3.10+ and [Pillow](https://pillow.readthedocs.io/) (installed automatically).
