# Maintaining SVG Examples

This guide explains how to maintain and regenerate the visual examples throughout the PyFreeform wiki documentation.

---

## 📋 Overview

The PyFreeform wiki uses an **automated SVG generation system** to create visual examples for every code snippet in the documentation. This ensures:

- ✅ **Consistency** - All examples use the same styling and test data
- ✅ **Accuracy** - Visuals are generated from actual working code
- ✅ **Maintainability** - Regenerate all images with one command when APIs change
- ✅ **Incrementality** - Step-by-step visuals show learning progression

---

## 🗂️ System Architecture

### Folder Structure

```
wiki/
├── regenerate_all_svgs.py          # Master regeneration script
├── getting-started/
│   ├── 01-your-first-artwork.md    # Markdown documentation
│   ├── _svg_generators/
│   │   └── 01_your_first_artwork_gen.py  # Python generator script
│   └── _images/
│       ├── step1-import.svg         # Generated SVG files
│       ├── step2-load-image.svg
│       └── ...
├── fundamentals/
│   ├── 01-scenes.md
│   ├── _svg_generators/
│   │   └── 01_scenes_gen.py
│   └── _images/
│       └── ...
```

### How It Works

1. **Generator Scripts** (`*_gen.py`) - Python files that create SVG images using PyFreeform
2. **Output Directory** (`_images/`) - Where generated SVG files are saved
3. **Master Script** (`regenerate_all_svgs.py`) - Runs all generators at once
4. **Markdown Files** (`*.md`) - Reference the generated images

---

## 🚀 Quick Start

### Regenerate All Images

```bash
cd wiki/
python regenerate_all_svgs.py
```

This will regenerate **all** SVG images across the entire wiki.

### Regenerate One Section

```bash
python regenerate_all_svgs.py --section getting-started
```

### Regenerate One File

```bash
cd wiki/getting-started/_svg_generators/
python 01_your_first_artwork_gen.py
```

### List All Generators

```bash
python regenerate_all_svgs.py --list
```

---

## 📝 Creating a New Generator

### Step 1: Create the Generator File

```bash
# For a new documentation file: wiki/section/filename.md
# Create: wiki/section/_svg_generators/filename_gen.py
```

### Step 2: Generator Template

```python
#!/usr/bin/env python3
"""
SVG Generator for: section/filename.md

Generates incremental visual examples for each code snippet.
"""

from pyfreeform import Scene, Palette
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images"
OUTPUT_DIR.mkdir(exist_ok=True)

# Create test data (gradient, patterns, etc.)
def create_test_gradient() -> Path:
    """Create a test image for examples"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_test.png"
    # ... create gradient image ...
    return temp_file

TEST_IMAGE = create_test_gradient()

# =============================================================================
# SECTION: Your First Example
# =============================================================================

def example_step1():
    """Step 1: Description of what this shows"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # ... create visualization ...

    scene.save(OUTPUT_DIR / "example-step1.svg")


def example_step2():
    """Step 2: Next incremental step"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    # ... build on previous step ...

    scene.save(OUTPUT_DIR / "example-step2.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "example-step1": example_step1,
    "example-step2": example_step2,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for filename.md...")

    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")

    print(f"Complete! Generated to {OUTPUT_DIR}/")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Generate specific image
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            print(f"Available generators:")
            for key in sorted(GENERATORS.keys()):
                print(f"  - {key}")
    else:
        # Generate all
        generate_all()
```

### Step 3: Reference in Markdown

In your markdown file:

```markdown
### Step 2: Load Your Image

\```python
scene = Scene.from_image("photo.jpg", grid_size=40)
\```

![Grid loaded from image](./_images/step2-load-image.svg)

This creates a scene with a 40×40 grid...
```

---

## 🎨 Best Practices for Generators

### 1. Be Highly Incremental

**Don't just show final results!** Show each step:

```python
# ❌ Bad - Only one image
def example_complete():
    """Complete example"""
    # ... all code ...

# ✅ Good - Show progression
def example_step1():
    """Step 1: Create scene"""
    # ... minimal code ...

def example_step2():
    """Step 2: Add grid"""
    # ... build on step 1 ...

def example_step3():
    """Step 3: Add dots"""
    # ... build on step 2 ...
```

### 2. Use Descriptive Names

```python
# ❌ Bad
"example1.svg"
"example2.svg"

# ✅ Good
"step-01-create-scene.svg"
"step-02-add-grid.svg"
"variation-brightness-sizing.svg"
```

### 3. Create Variations

Show different parameter values:

```python
def experiment_grid_size_20():
    """Grid size = 20 (more abstract)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=20)
    # ...

def experiment_grid_size_60():
    """Grid size = 60 (more detailed)"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=60)
    # ...
```

### 4. Use Consistent Test Data

Create helper functions for test images:

```python
def create_test_gradient() -> Path:
    """Create consistent gradient for all examples"""
    # ... same gradient every time ...
    return temp_file

def create_test_pattern() -> Path:
    """Create consistent pattern for examples"""
    # ... geometric pattern ...
    return temp_file
```

### 5. Handle Errors Gracefully

```python
def generate_all():
    for name, func in GENERATORS.items():
        try:
            func()
            print(f"  ✓ {name}.svg")
        except Exception as e:
            print(f"  ✗ {name}.svg - ERROR: {e}")
            # Don't fail completely - keep generating others
```

---

## 🔧 Workflow for Documentation Updates

### When Adding New Content

1. **Write the markdown** - Add your new section/example
2. **Create generator functions** - One per code snippet/concept
3. **Add to GENERATORS dict** - Register your functions
4. **Test locally** - `python your_generator.py`
5. **Reference in markdown** - `![](./_images/your-image.svg)`
6. **Regenerate all** - `python regenerate_all_svgs.py` (to verify)
7. **Commit everything** - Both markdown and generated SVGs

### When Updating PyFreeform API

1. **Update generator scripts** - Fix deprecated API calls
2. **Regenerate all** - `python regenerate_all_svgs.py`
3. **Review changes** - Check that visuals still look correct
4. **Commit updated SVGs** - Git will show what changed

### When Fixing a Bug in Examples

1. **Fix the generator function** - Update the Python code
2. **Regenerate** - `python your_generator.py`
3. **Visual check** - Open the SVG to verify
4. **Commit** - Both the generator and updated SVG

---

## 🎯 Examples of Incrementality

### Example: Tutorial Progression

For [getting-started/01-your-first-artwork.md](getting-started/01-your-first-artwork.md):

```python
# Show EVERY step, not just the final result!
def step_00_blank_canvas():      # Before anything
def step_01_after_import():      # After importing
def step_02_grid_structure():    # Grid created (no dots)
def step_02b_grid_with_centers(): # Show where dots go
def step_03_first_dots():        # First few dots added
def step_03b_half_complete():    # Halfway through
def step_04_complete():          # Final result
```

### Example: Parameter Variations

```python
# Show the EFFECT of different parameters
def experiment_grid_size_10():   # Very abstract
def experiment_grid_size_20():   # Abstract
def experiment_grid_size_40():   # Balanced (default)
def experiment_grid_size_60():   # Detailed
def experiment_grid_size_80():   # Very detailed
```

### Example: Concept Progression

```python
# Build up a complex concept step-by-step
def brightness_step1_uniform():      # All same size (before)
def brightness_step2_dynamic():      # Apply brightness formula
def brightness_step3_extreme():      # More extreme variation
```

---

## 📊 Statistics

Run with `--verbose` to see detailed output:

```bash
python regenerate_all_svgs.py --verbose
```

Current generators:
- `getting-started/01_your_first_artwork_gen.py` - **32 images**
- `fundamentals/01_scenes_gen.py` - **29 images**
- Total: **61+ incremental visual examples**

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'pyfreeform'"

Install PyFreeform in editable mode:

```bash
cd /path/to/pyfreeform
pip install -e .
```

### "Invalid hex color: #ffffff30"

PyFreeform doesn't support alpha in hex colors. Use solid colors:

```python
# ❌ Bad
color="#ffffff30"  # Alpha channel

# ✅ Good
color="#cccccc"    # Solid color
```

### "Text.__init__() got an unexpected keyword argument 'anchor'"

The parameter is `text_anchor`, not `anchor`:

```python
# ❌ Bad
Text(x=100, y=100, content="Hello", anchor="middle")

# ✅ Good
Text(x=100, y=100, content="Hello", text_anchor="middle")
```

### "Scene' object has no attribute 'add_entity'"

Use `scene.add()` instead:

```python
# ❌ Bad
scene.add(dot)

# ✅ Good
scene.add(dot)
```

### Import Errors

Check the correct entity names:

```python
from pyfreeform import (
    Scene, Palette,
    Dot, Line, Rect,  # Not "Rectangle"!
    Curve, Ellipse, Text, Polygon,
    Grid
)
```

---

## 📚 See Also

- [regenerate_all_svgs.py](regenerate_all_svgs.py) - Master script source code
- [getting-started/_svg_generators/](getting-started/_svg_generators/) - Example generators
- [PyFreeform Documentation](index.md) - Main wiki index

---

## 💡 Philosophy

> **"Every code snippet deserves a visual."**

The goal is to make PyFreeform documentation **the most visual, incremental, and beginner-friendly generative art library documentation** out there. When users see code, they should immediately see what it produces—not just the final result, but every step along the way.

**Remember:** More incremental is better! Show progression, not just completion.

---

**Last Updated:** 2026-02-05
**Maintainer:** PyFreeform Team
