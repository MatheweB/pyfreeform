"""SVG Generator for Recipe: Text Art."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from pyfreeform import Scene, Palette, Text
import math

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../_images/07-text-art')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_svg(filename, scene):
    """Save SVG to the output directory."""
    path = os.path.join(OUTPUT_DIR, filename)
    scene.save(path)
    print(f"Generated: {filename}")


def create_synthetic_brightness_grid(scene):
    """Create synthetic brightness values."""
    for cell in scene.grid:
        # Create pattern
        dx = cell.col - scene.grid.cols / 2
        dy = cell.row - scene.grid.rows / 2
        distance = math.sqrt(dx*dx + dy*dy)
        max_distance = math.sqrt((scene.grid.cols/2)**2 + (scene.grid.rows/2)**2)

        brightness = 1 - (distance / max_distance)
        brightness = max(0, min(1, brightness))

        cell._brightness = brightness


def image_01_data_labels():
    """Display brightness values as text."""
    scene = Scene.with_grid(cols=12, rows=8, cell_size=35)
    colors = Palette.paper()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Background color
        gray = int(cell._brightness * 255)
        bg_color = f"#{gray:02x}{gray:02x}{gray:02x}"

        cell.add_fill(color=bg_color, z_index=0)

        # Display brightness value
        value = f"{cell._brightness:.2f}"

        # Choose text color for contrast
        text_color = "white" if cell._brightness < 0.5 else "black"

        cell.add_text(
            content=value,
            font_size=8,
            color=text_color,
            font_family="monospace",
            text_anchor="middle",
            baseline="middle",
            z_index=10
        )

    save_svg("01_data_labels.svg", scene)


def image_02_chess_labels():
    """Chess-style grid labels."""
    scene = Scene.with_grid(cols=8, rows=8, cell_size=40)
    colors = Palette.midnight()
    scene.background = colors.background

    letters = "ABCDEFGH"

    for cell in scene.grid:
        # Checkerboard background
        if (cell.row + cell.col) % 2 == 0:
            cell.add_fill(color=colors.grid, z_index=0)

        # Column letter on top row
        if cell.row == 0:
            cell.add_text(
                content=letters[cell.col],
                font_size=16,
                color=colors.primary,
                font_family="serif",
                text_anchor="middle",
                baseline="middle",
                z_index=10
            )

        # Row number on left column
        if cell.col == 0:
            cell.add_text(
                content=str(8 - cell.row),
                font_size=16,
                color=colors.primary,
                font_family="serif",
                text_anchor="middle",
                baseline="middle",
                z_index=10
            )

    save_svg("02_chess_labels.svg", scene)


def image_03_rotating_text():
    """Text with rotation based on position."""
    scene = Scene.with_grid(cols=15, rows=10, cell_size=30)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Rotation based on position
        angle = (cell.row + cell.col) * 15

        cell.add_text(
            content="ART",
            font_size=12,
            rotation=angle,
            color=colors.primary,
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("03_rotating_text.svg", scene)


def image_04_size_variations():
    """Text size based on brightness."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=25)
    colors = Palette.sunset()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Font size based on brightness
        size = 8 + cell._brightness * 16  # 8 to 24

        cell.add_text(
            content="•",
            font_size=size,
            color=colors.primary,
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("04_size_variations.svg", scene)


def image_05_ascii_art():
    """ASCII character shading."""
    scene = Scene.with_grid(cols=30, rows=20, cell_size=15)
    scene.background = "#000000"

    create_synthetic_brightness_grid(scene)

    # ASCII characters from dark to light
    ascii_chars = " .:-=+*#%@"

    for cell in scene.grid:
        # Choose character based on brightness
        char_idx = int(cell._brightness * (len(ascii_chars) - 1))
        char = ascii_chars[char_idx]

        cell.add_text(
            content=char,
            font_size=14,
            color="white",
            font_family="monospace",
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("05_ascii_art.svg", scene)


def image_06_color_coded():
    """Color-coded text labels."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=30)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        if cell._brightness > 0.7:
            label = "HIGH"
            color = colors.accent
        elif cell._brightness > 0.4:
            label = "MED"
            color = colors.primary
        else:
            label = "LOW"
            color = colors.secondary

        cell.add_text(
            content=label,
            font_size=8,
            color=color,
            font_family="sans-serif",
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("06_color_coded.svg", scene)


def image_07_coordinates():
    """Display grid coordinates."""
    scene = Scene.with_grid(cols=10, rows=8, cell_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Display (row, col) coordinates
        coords = f"({cell.row},{cell.col})"

        cell.add_text(
            content=coords,
            font_size=8,
            color=colors.primary,
            font_family="monospace",
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("07_coordinates.svg", scene)


def image_08_title_overlay():
    """Large title over artwork."""
    scene = Scene.with_grid(cols=25, rows=20, cell_size=15)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Background artwork
    for cell in scene.grid:
        size = 2 + cell._brightness * 6
        cell.add_dot(radius=size, color=colors.primary, z_index=0)

    # Title overlay
    title = Text(
        x=scene.width // 2,
        y=30,
        content="GENERATIVE ART",
        font_size=24,
        color="white",
        font_family="serif",
        text_anchor="middle",
        z_index=1000
    )
    scene.add(title)

    save_svg("08_title_overlay.svg", scene)


def image_09_unicode_symbols():
    """Unicode symbols for patterns."""
    scene = Scene.with_grid(cols=20, rows=15, cell_size=22)
    colors = Palette.sunset()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    # Unicode circle symbols
    symbols = ["○", "◔", "◑", "◕", "●"]

    for cell in scene.grid:
        # Choose symbol based on brightness
        symbol_idx = int(cell._brightness * (len(symbols) - 1))
        symbol = symbols[symbol_idx]

        cell.add_text(
            content=symbol,
            font_size=16,
            color=colors.primary,
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("09_unicode_symbols.svg", scene)


def image_10_mixed_fonts():
    """Different font families."""
    scene = Scene.with_grid(cols=12, rows=4, cell_size=40)
    colors = Palette.ocean()
    scene.background = colors.background

    fonts = ["sans-serif", "serif", "monospace"]
    content = ["SANS", "SERIF", "MONO"]

    for cell in scene.grid:
        font_idx = cell.row % len(fonts)

        cell.add_text(
            content=content[font_idx],
            font_size=10,
            font_family=fonts[font_idx],
            color=colors.primary,
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("10_mixed_fonts.svg", scene)


def image_11_text_with_shapes():
    """Text combined with geometric shapes, auto-sized via fit_within."""
    scene = Scene.with_grid(cols=15, rows=12, cell_size=30)
    colors = Palette.midnight()
    scene.background = colors.background

    create_synthetic_brightness_grid(scene)

    for cell in scene.grid:
        # Background shape
        dot = cell.add_dot(
            radius=8,
            color=colors.primary,
            z_index=0
        )

        # Foreground text — fit_within auto-sizes to inscribed square
        label = cell.add_text(
            content=str(int(cell._brightness * 9)),
            font_size=50,
            color=colors.background,
            font_family="sans-serif",
            z_index=10
        )
        label.fit_within(dot)

    save_svg("11_text_with_shapes.svg", scene)


def image_12_wave_text():
    """Text following wave pattern."""
    scene = Scene.with_grid(cols=25, rows=15, cell_size=20)
    colors = Palette.ocean()
    scene.background = colors.background

    for cell in scene.grid:
        # Wave-based vertical position offset
        phase = cell.col / scene.grid.cols * math.pi * 2
        wave = math.sin(phase) * 0.3 + 0.5  # 0.2 to 0.8

        # Vary size with wave
        size = 8 + wave * 8

        cell.add_text(
            content="~",
            font_size=size,
            color=colors.primary,
            text_anchor="middle",
            baseline="middle"
        )

    save_svg("12_wave_text.svg", scene)


def generate_all():
    """Generate all recipe images."""
    print("Generating Recipe 07: Text Art...")

    image_01_data_labels()
    image_02_chess_labels()
    image_03_rotating_text()
    image_04_size_variations()
    image_05_ascii_art()
    image_06_color_coded()
    image_07_coordinates()
    image_08_title_overlay()
    image_09_unicode_symbols()
    image_10_mixed_fonts()
    image_11_text_with_shapes()
    image_12_wave_text()

    print(f"\nAll images saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_all()
