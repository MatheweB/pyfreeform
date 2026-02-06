#!/usr/bin/env python3
"""
SVG Generator for: getting-started/00-installation.md

Generates a simple visual for the installation test example.

Corresponds to sections:
- Test Your Installation
"""

from pyfreeform import Scene
from pathlib import Path


# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "00-installation"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SECTION: Test Your Installation
# =============================================================================

def example_01_installation_test():
    """
    The installation test example - a simple 3x3 grid with a coral dot in the center.
    This is the first thing users create to verify their installation works.
    """
    # Create a simple scene
    scene = Scene.with_grid(cols=3, rows=3, cell_size=100)

    # Add a dot to the center cell
    center = scene.grid[1, 1]
    center.add_dot(radius=20, color="coral")

    scene.save(OUTPUT_DIR / "01-installation-test.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01-installation-test": example_01_installation_test,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVG for 00-installation.md...")

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
