# Installation

## Install PyFreeform

```bash
pip install pyfreeform
```

**Requirements**: Python 3.10+ and [Pillow](https://pillow.readthedocs.io/) (installed automatically).

## Verify It Works

Create a file called `hello.py`:

```python
from pyfreeform import Scene, Palette

colors = Palette.midnight()
scene = Scene.with_grid(cols=8, rows=8, cell_size=30, background=colors.background)

for cell in scene.grid:
    nx, ny = cell.normalized_position
    radius = (nx + ny) / 2 * 0.4
    cell.add_dot(radius=radius, color=colors.primary)

scene.save("hello.svg")
print("Saved hello.svg")
```

Run it:

```bash
python hello.py
```

Open `hello.svg` in your browser. You should see a grid of dots that grow from top-left to bottom-right.

!!! success "Ready to go"
    If you see dots, everything is working. Head to [Your First Artwork](02-your-first-artwork.md) to create something more exciting.

## Optional: Jupyter Support

PyFreeform works in Jupyter notebooks with inline SVG display:

```python
from pyfreeform import Scene, display

scene = Scene.with_grid(cols=10, rows=10, cell_size=20)
for cell in scene.grid:
    cell.add_dot(color="coral")
display(scene)  # Renders inline in the notebook
```

## Troubleshooting

??? warning "ImportError: No module named 'pyfreeform'"
    Make sure you're using the same Python environment where you installed the package:
    ```bash
    python -m pip install pyfreeform
    ```

??? warning "Pillow not found"
    Pillow should install automatically. If not:
    ```bash
    pip install Pillow
    ```
