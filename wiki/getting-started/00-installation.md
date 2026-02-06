
# Installation

Getting PyFreeform up and running is straightforward. This guide will have you ready to create art in just a few minutes.

---

## Requirements

!!! info "Python Version Requirements"
    PyFreeform requires:

    - **Python 3.9 or higher**
    - **pip** (Python's package installer)

### Check Your Python Version

```bash
python --version
# or
python3 --version
```

If you see Python 3.9 or higher, you're ready to go!

---

## Install PyFreeform

### From PyPI (Recommended)

Install the latest stable version:

```bash
pip install pyfreeform
```

Or if you need to specify Python 3:

```bash
pip3 install pyfreeform
```

### Verify Installation

Test that PyFreeform is installed correctly:

```python
python -c "import pyfreeform; print(pyfreeform.__version__)"
```

You should see the version number printed.

---

## Dependencies

PyFreeform automatically installs these dependencies:

- **Pillow** - For image loading and processing
- **NumPy** - For efficient numerical operations

You don't need to install these separately.

---

## Development Installation

If you want to contribute to PyFreeform or run the latest code from the repository:

```bash
# Clone the repository
git clone https://github.com/anthropics/pyfreeform.git
cd pyfreeform

# Install in development mode
pip install -e .
```

This creates an editable installation that reflects your code changes immediately.

---

## Troubleshooting

### Permission Errors

If you get permission errors, try:

```bash
pip install --user pyfreeform
```

Or use a virtual environment:

!!! tip "Use a Virtual Environment (Recommended)"
    Virtual environments keep your project dependencies isolated and prevent conflicts:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install pyfreeform
    ```

### Module Not Found

If Python can't find pyfreeform after installation:

1. Make sure you're using the same Python that you installed it with
2. Check that the package is installed: `pip list | grep pyfreeform`
3. Try restarting your terminal or IDE

### Pillow Installation Issues

!!! note "Platform-Specific Dependencies"
    On some systems, Pillow may need additional system libraries. See the [Pillow installation docs](https://pillow.readthedocs.io/en/stable/installation.html) for platform-specific instructions.

---

## Test Your Installation

Create a test file to confirm everything works:

```python
# test_pyfreeform.py
from pyfreeform import Scene

# Create a simple scene
scene = Scene.with_grid(cols=3, rows=3, cell_size=100)

# Add a dot to the center cell
center = scene.grid[1, 1]
center.add_dot(radius=20, color="coral")

# Save
scene.save("test.svg")
print("Success! Check test.svg")
```

![Installation test result](./_images/00-installation/01-installation-test.svg)

Run it:

```bash
python test_pyfreeform.py
```

If you see "Success!" and a `test.svg` file appears, you're all set!

---

## Next Steps

Now that PyFreeform is installed, you're ready to create your first artwork:

**Next**: [Your First Artwork](01-your-first-artwork.md) - Create stunning dot art in 5 lines

---

## See Also

- 📖 [Core Concepts](02-core-concepts.md) - Understanding PyFreeform's structure
- 🎨 [Image to Art](03-image-to-art.md) - Transform photos into generative art
- 🔍 [Example Gallery](../examples/index.md) - Browse working examples

[← Back to Home](../index.md) | [Next: Your First Artwork →](01-your-first-artwork.md)
