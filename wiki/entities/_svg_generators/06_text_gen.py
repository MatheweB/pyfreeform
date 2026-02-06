#!/usr/bin/env python3
"""
SVG Generator for: entities/06-text.md

Generates visual examples for text entity documentation.
"""

from pyfreeform import Scene, Text, shapes
from pathlib import Path
from PIL import Image, ImageDraw
import tempfile

# Paths
OUTPUT_DIR = Path(__file__).parent.parent / "_images" / "06-text"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def create_test_image() -> Path:
    """Create a simple test image with gradient"""
    temp_file = Path(tempfile.gettempdir()) / "pyfreeform_wiki_text.png"
    img = Image.new('RGB', (400, 400))
    draw = ImageDraw.Draw(img)
    for y in range(400):
        for x in range(400):
            brightness = int(255 * (1 - ((x + y) / 800)))
            draw.point((x, y), fill=(brightness, brightness, brightness))
    img.save(temp_file)
    return temp_file


TEST_IMAGE = create_test_image()


# =============================================================================
# SECTION: Font Sizes
# =============================================================================

def font_sizes():
    """Text at different font sizes"""
    scene = Scene.with_grid(cols=4, rows=1, cell_size=100)
    scene.background = "white"
    cells = list(scene.grid)

    sizes = [10, 16, 24, 36]
    for i, size in enumerate(sizes):
        cells[i].add_text(f"{size}px", font_size=size, color="#1f2937")

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "01_font_sizes.svg")


# =============================================================================
# SECTION: Font Families
# =============================================================================

def font_families():
    """Text with different font families"""
    scene = Scene.with_grid(cols=3, rows=1, cell_size=120)
    scene.background = "white"
    cells = list(scene.grid)

    fonts = [
        ("sans-serif", "Sans"),
        ("serif", "Serif"),
        ("monospace", "Mono"),
    ]

    for i, (family, label) in enumerate(fonts):
        cells[i].add_text(label, font_size=20, color="#1f2937", font_family=family)

    for cell in scene.grid:
        cell.add_border(color="#e0e0e0", width=0.5)

    scene.save(OUTPUT_DIR / "02_font_families.svg")


# =============================================================================
# SECTION: Grid Labels
# =============================================================================

def grid_labels():
    """Column and row labels on a grid"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=30)
    scene.background = "white"

    for cell in scene.grid:
        if cell.row == 0:
            # Column headers (A-H)
            label = chr(65 + cell.col)
            cell.add_text(label, font_size=12, color="#3b82f6")
        elif cell.col == 0:
            # Row numbers (1-8)
            cell.add_text(str(cell.row), font_size=12, color="#ef4444")
        else:
            cell.add_dot(radius=2, color="#e0e0e0")

        cell.add_border(color="#e0e0e0", width=0.3)

    scene.save(OUTPUT_DIR / "03_grid_labels.svg")


# =============================================================================
# SECTION: Title Overlay
# =============================================================================

def title_overlay():
    """Large text 'HELLO' overlaid on a grid pattern"""
    scene = Scene.with_grid(cols=10, rows=6, cell_size=30)
    scene.background = "#1e1b4b"

    # Grid pattern background
    colors = ["#312e81", "#3730a3", "#4338ca", "#4f46e5"]
    for cell in scene.grid:
        idx = (cell.row + cell.col) % len(colors)
        cell.add_fill(color=colors[idx], z_index=0)

    # Title overlay
    title = Text(
        x=scene.width // 2,
        y=scene.height // 2,
        content="HELLO",
        font_size=48,
        color="white",
        font_family="sans-serif",
        text_anchor="middle",
        baseline="middle",
        z_index=100,
    )
    scene.add(title)

    scene.save(OUTPUT_DIR / "04_title_overlay.svg")


# =============================================================================
# SECTION: Data Labels
# =============================================================================

def data_labels():
    """Brightness values displayed in monospace font"""
    scene = Scene.from_image(TEST_IMAGE, grid_size=40)

    for cell in scene.grid:
        # Background fill from brightness
        gray = int(cell.brightness * 255)
        cell.add_fill(color=f"rgb({gray},{gray},{gray})", z_index=0)

        # Text label showing brightness
        value = f"{cell.brightness:.2f}"
        text_color = "white" if cell.brightness < 0.5 else "black"
        cell.add_text(
            value,
            font_size=8,
            color=text_color,
            font_family="monospace",
            z_index=10,
        )

    scene.save(OUTPUT_DIR / "05_data_labels.svg")


# =============================================================================
# SECTION: Rotating Text
# =============================================================================

def rotating_text():
    """Text rotated by position: angle = (row+col)*15"""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=35)
    scene.background = "white"

    colors = ["#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6", "#ec4899"]

    for cell in scene.grid:
        angle = (cell.row + cell.col) * 15
        color_idx = (cell.row + cell.col) % len(colors)

        cell.add_text(
            "Aa",
            font_size=12,
            rotation=angle,
            color=colors[color_idx],
        )

    scene.save(OUTPUT_DIR / "06_rotating_text.svg")


# =============================================================================
# SECTION: Complete Example
# =============================================================================

def complete_example():
    """Comprehensive text demo with varied styles"""
    scene = Scene.with_grid(cols=4, rows=4, cell_size=100)
    scene.background = "#0f172a"

    families = ["sans-serif", "serif", "monospace", "sans-serif"]

    for cell in scene.grid:
        row, col = cell.row, cell.col

        if row == 0:
            # Font family examples
            cell.add_fill(color="#1e293b", z_index=0)
            cell.add_text(
                families[col],
                font_family=families[col],
                font_size=14,
                color="#7dd3fc",
                z_index=10,
            )
        elif row == 1:
            # Size variations
            cell.add_fill(color="#1e293b", z_index=0)
            size = 10 + col * 6
            cell.add_text(
                f"{size}px",
                font_size=size,
                color="#fbbf24",
                z_index=10,
            )
        elif row == 2:
            # Colored text
            cell.add_fill(color="#1e293b", z_index=0)
            text_colors = ["#ef4444", "#10b981", "#3b82f6", "#f59e0b"]
            cell.add_text(
                "Color",
                font_size=18,
                color=text_colors[col],
                z_index=10,
            )
        else:
            # Rotation
            cell.add_fill(color="#1e293b", z_index=0)
            angle = col * 30
            cell.add_text(
                f"{angle}deg",
                rotation=angle,
                font_size=14,
                color="#c084fc",
                z_index=10,
            )

        cell.add_border(color="#334155", width=0.5, z_index=1)

    # Title at bottom
    title = Text(
        x=scene.width // 2,
        y=scene.height + 25,
        content="Text Features",
        font_size=20,
        color="white",
        text_anchor="middle",
        z_index=100,
    )
    scene.add(title)

    scene.save(OUTPUT_DIR / "07_complete_example.svg")


# =============================================================================
# Generator Registry
# =============================================================================

GENERATORS = {
    "01_font_sizes": font_sizes,
    "02_font_families": font_families,
    "03_grid_labels": grid_labels,
    "04_title_overlay": title_overlay,
    "05_data_labels": data_labels,
    "06_rotating_text": rotating_text,
    "07_complete_example": complete_example,
}


def generate_all():
    """Generate all SVG images for this document"""
    print(f"Generating {len(GENERATORS)} SVGs for 06-text.md...")
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
        name = sys.argv[1]
        if name in GENERATORS:
            GENERATORS[name]()
            print(f"Generated {name}.svg")
        else:
            print(f"Unknown generator: {name}")
            print(f"Available: {', '.join(sorted(GENERATORS.keys()))}")
    else:
        generate_all()
