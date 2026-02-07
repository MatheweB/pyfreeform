"""Tests for Features 1-5: rect cells, fit-grid-to-image, QoL, sampling, relative positioning."""

import sys
import math
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Grid, Cell, Point, Dot, Rect, Text, Image


# =========================================================================
# Helpers
# =========================================================================

def _make_image(width: int, height: int, r=128, g=128, b=128) -> Image:
    """Create a solid-color test image."""
    red = np.full((height, width), r, dtype=np.float64)
    green = np.full((height, width), g, dtype=np.float64)
    blue = np.full((height, width), b, dtype=np.float64)
    return Image(red, green, blue)


def _make_quadrant_image(size: int = 100) -> Image:
    """Create a 4-quadrant test image: TL=red, TR=green, BL=blue, BR=white."""
    h = size // 2
    red = np.zeros((size, size), dtype=np.float64)
    green = np.zeros((size, size), dtype=np.float64)
    blue = np.zeros((size, size), dtype=np.float64)
    # Top-left: red (255,0,0)
    red[:h, :h] = 255
    # Top-right: green (0,255,0)
    green[:h, h:] = 255
    # Bottom-left: blue (0,0,255)
    blue[h:, :h] = 255
    # Bottom-right: white (255,255,255)
    red[h:, h:] = 255
    green[h:, h:] = 255
    blue[h:, h:] = 255
    return Image(red, green, blue)


# =========================================================================
# Feature 1: Rectangle Cells / cell_ratio
# =========================================================================


class TestRectCells:
    def test_cell_ratio_from_image(self):
        """cell_ratio=2.0 creates cells with width=20, height=10."""
        img = _make_image(400, 200)
        grid = Grid.from_image(img, cols=20, cell_size=10, cell_ratio=2.0)
        assert grid.cell_width == 20.0
        assert grid.cell_height == 10.0

    def test_explicit_cell_width_height(self):
        """Explicit cell_width/cell_height override cell_size."""
        img = _make_image(300, 300)
        grid = Grid.from_image(img, cols=10, cell_size=10, cell_width=15, cell_height=20)
        assert grid.cell_width == 15.0
        assert grid.cell_height == 20.0

    def test_backward_compat_square_cells(self):
        """Default params produce square cells."""
        img = _make_image(300, 300)
        grid = Grid.from_image(img, cols=10, cell_size=10)
        assert grid.cell_width == 10.0
        assert grid.cell_height == 10.0

    def test_with_grid_cell_width_height(self):
        """Scene.with_grid supports cell_width/cell_height."""
        scene = Scene.with_grid(cols=10, rows=5, cell_width=20.0, cell_height=10.0)
        grid = scene.grid
        assert grid.cell_width == 20.0
        assert grid.cell_height == 10.0
        assert scene.width == 200  # 10 * 20
        assert scene.height == 50  # 5 * 10

    def test_scene_dimensions_correct(self):
        """Scene dimensions = cols * cell_width, rows * cell_height."""
        scene = Scene.from_image(
            _make_image(500, 250),
            grid_size=25,
            cell_size=10,
            cell_ratio=2.0,
        )
        grid = scene.grid
        assert grid.cell_width == 20.0
        assert grid.cell_height == 10.0
        assert scene.width == grid.cols * 20
        assert scene.height == grid.rows * 10

    def test_cell_width_only(self):
        """Specifying only cell_width uses cell_size for height."""
        grid = Grid.from_image(_make_image(200, 200), cols=10, cell_size=10, cell_width=15)
        assert grid.cell_width == 15.0
        assert grid.cell_height == 10.0

    def test_cell_height_only(self):
        """Specifying only cell_height uses cell_size for width."""
        grid = Grid.from_image(_make_image(200, 200), cols=10, cell_size=10, cell_height=15)
        assert grid.cell_width == 10.0
        assert grid.cell_height == 15.0


# =========================================================================
# Feature 2: Fit Grid to Image Mode
# =========================================================================


class TestFitGridToImage:
    def test_grid_size_none_square(self):
        """500x500 image, cell_size=10 → 50x50 grid."""
        scene = Scene.from_image(_make_image(500, 500), grid_size=None, cell_size=10)
        assert scene.grid.cols == 50
        assert scene.grid.rows == 50

    def test_grid_size_none_rectangular(self):
        """1200x800 image, cell_size=15."""
        scene = Scene.from_image(_make_image(1200, 800), grid_size=None, cell_size=15)
        assert scene.grid.cols == 80  # round(1200/15)
        assert scene.grid.rows == 53  # round(800/15)

    def test_scene_matches_image_dims(self):
        """Scene dimensions ≈ image dimensions when grid_size=None."""
        scene = Scene.from_image(_make_image(500, 500), grid_size=None, cell_size=10)
        assert scene.width == 500
        assert scene.height == 500

    def test_backward_compat_grid_size_default(self):
        """grid_size=40 (default) still works as before."""
        scene = Scene.from_image(_make_image(400, 200), grid_size=40, cell_size=10)
        assert scene.grid.cols == 40
        # rows from aspect ratio: round(40 * 200/400) = 20
        assert scene.grid.rows == 20

    def test_fit_with_cell_ratio(self):
        """Fit-to-image works with non-square cells."""
        scene = Scene.from_image(
            _make_image(400, 200),
            grid_size=None,
            cell_size=10,
            cell_ratio=2.0,
        )
        # cell_width=20, cell_height=10
        assert scene.grid.cols == 20  # round(400/20)
        assert scene.grid.rows == 20  # round(200/10)

    def test_image_data_loads_in_fit_mode(self):
        """Cell data loads correctly in fit-grid-to-image mode."""
        img = _make_image(100, 100, r=255, g=128, b=64)
        scene = Scene.from_image(img, grid_size=None, cell_size=10)
        cell = scene.grid[0, 0]
        # Should have loaded color data (not the default gray)
        assert cell.color != "#808080"
        assert cell.color.startswith("#")


# =========================================================================
# Feature 3: QoL Methods
# =========================================================================


class TestCellDistanceTo:
    def test_same_cell(self):
        """Distance to self is 0."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        cell = scene.grid[0, 0]
        assert cell.distance_to(cell) == 0.0

    def test_adjacent_cells(self):
        """Adjacent cells have distance = cell_size."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        c1 = scene.grid[0, 0]
        c2 = scene.grid[0, 1]
        assert abs(c1.distance_to(c2) - 10.0) < 0.01

    def test_diagonal_cells(self):
        """Diagonal distance for 3,4 grid offset = 5 * cell_size."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        c1 = scene.grid[0, 0]
        c2 = scene.grid[3, 4]
        expected = math.sqrt(30**2 + 40**2)  # pixels
        assert abs(c1.distance_to(c2) - expected) < 0.01

    def test_distance_to_point(self):
        """Distance to a Point."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        cell = scene.grid[0, 0]  # center at (5, 5)
        point = Point(5, 5)
        assert cell.distance_to(point) == 0.0

    def test_distance_to_tuple(self):
        """Distance to a tuple."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        cell = scene.grid[0, 0]
        center = cell.center
        assert cell.distance_to((center.x, center.y)) == 0.0

    def test_distance_to_anchor_point(self):
        """Distance to an entity anchor (Point)."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        cell = scene.grid[5, 5]
        dot = Dot(x=cell.center.x, y=cell.center.y, radius=5, color="red")
        # entity.anchor("center") returns a Point
        anchor_point = dot.anchor("center")
        assert cell.distance_to(anchor_point) == 0.0

    def test_distance_to_invalid_type(self):
        """TypeError for unsupported types."""
        scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
        cell = scene.grid[0, 0]
        with pytest.raises(TypeError):
            cell.distance_to("invalid")


class TestNormalizedPosition:
    def test_corners(self):
        """Corners are (0,0) and (1,1)."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        assert scene.grid[0, 0].normalized_position == (0.0, 0.0)
        assert scene.grid[9, 9].normalized_position == (1.0, 1.0)

    def test_center(self):
        """Center of 11x11 grid = (0.5, 0.5)."""
        scene = Scene.with_grid(cols=11, rows=11, cell_size=10)
        nx, ny = scene.grid[5, 5].normalized_position
        assert abs(nx - 0.5) < 0.01
        assert abs(ny - 0.5) < 0.01

    def test_single_cell(self):
        """Single cell grid = (0.0, 0.0)."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=10)
        assert scene.grid[0, 0].normalized_position == (0.0, 0.0)

    def test_top_right(self):
        """Top-right corner."""
        scene = Scene.with_grid(cols=10, rows=10, cell_size=10)
        nx, ny = scene.grid[0, 9].normalized_position
        assert abs(nx - 1.0) < 0.01
        assert abs(ny - 0.0) < 0.01


# =========================================================================
# Feature 4: Sub-Cell Image Sampling
# =========================================================================


class TestSubCellSampling:
    def test_source_image_stored(self):
        """Grid.source_image is set when created from image."""
        img = _make_image(100, 100)
        grid = Grid.from_image(img, cols=10, cell_size=10)
        assert grid.source_image is not None

    def test_source_image_none_for_empty_grid(self):
        """Grid.source_image is None for grids not from image."""
        scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
        assert scene.grid.source_image is None

    def test_sample_image_quadrants(self):
        """4-quadrant image: cells sample correct colors."""
        img = _make_quadrant_image(100)
        grid = Grid.from_image(img, cols=2, rows=2, cell_size=10)
        # Top-left cell → red quadrant
        r, g, b = grid[0, 0].sample_image(0.5, 0.5)
        assert r > 200 and g < 50 and b < 50
        # Top-right cell → green quadrant
        r, g, b = grid[0, 1].sample_image(0.5, 0.5)
        assert g > 200 and r < 50 and b < 50
        # Bottom-left cell → blue quadrant
        r, g, b = grid[1, 0].sample_image(0.5, 0.5)
        assert b > 200 and r < 50 and g < 50
        # Bottom-right cell → white quadrant
        r, g, b = grid[1, 1].sample_image(0.5, 0.5)
        assert r > 200 and g > 200 and b > 200

    def test_sample_brightness_range(self):
        """sample_brightness returns 0.0-1.0."""
        img = _make_image(100, 100, r=255, g=255, b=255)
        grid = Grid.from_image(img, cols=5, cell_size=10)
        br = grid[0, 0].sample_brightness()
        assert 0.0 <= br <= 1.0
        assert br > 0.9  # White should be close to 1.0

    def test_sample_hex_format(self):
        """sample_hex returns valid hex string."""
        img = _make_image(100, 100, r=255, g=0, b=128)
        grid = Grid.from_image(img, cols=5, cell_size=10)
        hex_color = grid[0, 0].sample_hex()
        assert hex_color.startswith("#")
        assert len(hex_color) == 7

    def test_sample_raises_without_image(self):
        """ValueError for grids not created from image."""
        scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
        with pytest.raises(ValueError, match="not created from an image"):
            scene.grid[0, 0].sample_image()


# =========================================================================
# Feature 5: Entity Relative Positioning
# =========================================================================


class TestOffsetFrom:
    def test_no_offset(self):
        """offset_from with no offset = anchor point."""
        dot = Dot(100, 200, radius=10, color="red")
        result = dot.offset_from("center")
        assert result.x == 100
        assert result.y == 200

    def test_with_offset(self):
        """offset_from("center", 10, -5) returns correct point."""
        dot = Dot(100, 200, radius=10, color="red")
        result = dot.offset_from("center", 10, -5)
        assert result.x == 110
        assert result.y == 195

    def test_on_rect_anchor(self):
        """offset_from on Rect named anchors."""
        rect = Rect(100, 100, width=40, height=20, fill="blue")
        # top_left anchor should be at (100, 100)
        result = rect.offset_from("top_left", 5, 5)
        assert abs(result.x - 105) < 0.01
        assert abs(result.y - 105) < 0.01


class TestPlaceBeside:
    def test_place_right(self):
        """Place dot to the right of another."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        d2.place_beside(d1, "right", gap=5)
        # d1 right edge = 110, gap = 5, d2 center should be at 125 (110+5+10)
        assert abs(d2.x - 125) < 0.01
        assert abs(d2.y - 100) < 0.01  # same y

    def test_place_left(self):
        """Place dot to the left of another."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        d2.place_beside(d1, "left", gap=5)
        # d1 left edge = 90, gap = 5, d2 center should be at 75 (90-5-10)
        assert abs(d2.x - 75) < 0.01

    def test_place_above(self):
        """Place dot above another."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        d2.place_beside(d1, "above", gap=5)
        # d1 top edge = 90, gap = 5, d2 center should be at 75 (90-5-10)
        assert abs(d2.y - 75) < 0.01
        assert abs(d2.x - 100) < 0.01  # same x

    def test_place_below(self):
        """Place dot below another."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        d2.place_beside(d1, "below", gap=5)
        # d1 bottom edge = 110, gap = 5, d2 center should be at 125 (110+5+10)
        assert abs(d2.y - 125) < 0.01

    def test_returns_self(self):
        """place_beside returns self for chaining."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        result = d2.place_beside(d1, "right")
        assert result is d2

    def test_invalid_side(self):
        """Invalid side raises ValueError."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        with pytest.raises(ValueError, match="Invalid side"):
            d2.place_beside(d1, "diagonal")

    def test_zero_gap(self):
        """Edges touch with gap=0."""
        d1 = Dot(100, 100, radius=10, color="red")
        d2 = Dot(0, 0, radius=10, color="blue")
        d2.place_beside(d1, "right", gap=0)
        # d1 right edge = 110, d2 left edge should be at 110
        # d2 center = 110 + 10 = 120
        assert abs(d2.x - 120) < 0.01

    def test_with_text(self):
        """place_beside works with Text entity."""
        rect = Rect(100, 100, width=40, height=20, fill="blue")
        text = Text(0, 0, "Hello", font_size=12, color="white")
        result = text.place_beside(rect, "below", gap=3)
        assert result is text
        # Text should be below the rect
        assert text.y > 120  # rect bottom is at 120
