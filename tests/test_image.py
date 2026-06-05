"""Tests for image loading, resizing, sampling, and Layer.

Covers the previously-untested image/ subpackage. The headline case is the
constant-channel resize bug: a fully-opaque image has a constant alpha (255),
and a solid-color image has constant RGB — both used to resize to all-zeros.
"""

import numpy as np
import pytest
from PIL import Image as PILImage

import pyfreeform as pf
from pyfreeform.image.image import Image
from pyfreeform.image.layer import Layer
from pyfreeform.image.resize import resize_array, fit_dimensions, downscale_array


# ---------------------------------------------------------------------------
# resize_array — the constant-channel fix
# ---------------------------------------------------------------------------
class TestResizeArray:
    def test_constant_array_preserves_value(self):
        # Was the bug: a constant array resized to all-zeros.
        out = resize_array(np.full((4, 4), 200.0), 2, 2)
        assert out.shape == (2, 2)
        assert np.allclose(out, 200.0)

    def test_constant_zero_array_stays_zero(self):
        out = resize_array(np.zeros((4, 4)), 3, 3)
        assert np.allclose(out, 0.0)

    def test_varying_array_resizes_and_keeps_range(self):
        arr = np.linspace(10, 250, 16).reshape(4, 4)
        out = resize_array(arr, 2, 2)
        assert out.shape == (2, 2)
        # Resampled values stay within the original range (no blanking).
        assert out.min() >= 10 - 1 and out.max() <= 250 + 1
        assert out.max() > out.min()  # contrast preserved

    def test_non_square_resize(self):
        out = resize_array(np.full((6, 9), 128.0), 3, 2)
        assert out.shape == (2, 3)  # (height, width)
        assert np.allclose(out, 128.0)


# ---------------------------------------------------------------------------
# Image.resize — channel preservation
# ---------------------------------------------------------------------------
class TestImageResize:
    def test_opaque_image_keeps_alpha(self):
        # Any fully-opaque image: alpha is a constant 255 -> must stay 255.
        rgb = np.random.randint(0, 255, (16, 16, 3), dtype=np.uint8)
        img = Image.from_pil(PILImage.fromarray(rgb).convert("RGBA"))
        assert img.has_alpha
        resized = img.resize(4, 4)
        assert np.allclose(resized["alpha"].data, 255.0)

    def test_solid_color_image_keeps_color(self):
        solid = Image.from_pil(PILImage.new("RGB", (16, 16), (51, 102, 204)))
        resized = solid.resize(4, 4)
        assert resized.hex_at(0, 0) == "#3366cc"

    def test_varying_image_resizes(self):
        arr = np.zeros((8, 8, 3), dtype=np.uint8)
        arr[:, :4] = (255, 0, 0)
        arr[:, 4:] = (0, 0, 255)
        img = Image.from_pil(PILImage.fromarray(arr))
        resized = img.resize(4, 4)
        # Left stays reddish, right stays bluish.
        lr, _, lb = resized.rgb_at(0, 0)
        rr, _, rb = resized.rgb_at(3, 0)
        assert lr > lb and rb > rr


# ---------------------------------------------------------------------------
# Scene.from_image integration — the user-facing symptom
# ---------------------------------------------------------------------------
class TestSceneFromImageChannels:
    def test_opaque_image_cell_alpha_is_one(self):
        rgb = np.random.randint(0, 255, (20, 20, 3), dtype=np.uint8)
        img = Image.from_pil(PILImage.fromarray(rgb).convert("RGBA"))
        scene = pf.Scene.from_image(img, grid_size=5)
        assert all(cell.alpha == pytest.approx(1.0) for cell in scene.grid)

    def test_solid_color_image_not_black(self):
        solid = Image.from_pil(PILImage.new("RGB", (20, 20), (38, 166, 154)))
        scene = pf.Scene.from_image(solid, grid_size=5)
        cell = scene.grid[0][0]
        assert cell.color != "#000000"
        assert cell.brightness > 0.0


# ---------------------------------------------------------------------------
# Layer
# ---------------------------------------------------------------------------
class TestLayer:
    def test_dimensions_and_indexing_xy_order(self):
        data = np.arange(6, dtype=np.float64).reshape(2, 3)  # 2 rows, 3 cols
        layer = Layer(data)
        assert layer.width == 3 and layer.height == 2
        assert layer.shape == (2, 3)
        assert layer[0, 0] == 0.0          # (x=0, y=0)
        assert layer[2, 1] == 5.0          # (x=2, y=1) -> data[1, 2]

    def test_setitem(self):
        layer = Layer(np.zeros((2, 2)))
        layer[1, 0] = 9.0
        assert layer[1, 0] == 9.0

    def test_requires_2d(self):
        with pytest.raises(ValueError):
            Layer(np.zeros((2, 2, 2)))


# ---------------------------------------------------------------------------
# misc resize helpers
# ---------------------------------------------------------------------------
class TestResizeHelpers:
    def test_fit_dimensions_preserves_aspect(self):
        assert fit_dimensions(800, 400, 200, 200) == (200, 100)

    def test_fit_dimensions_no_upscale(self):
        assert fit_dimensions(100, 100, 500, 500) == (100, 100)

    def test_downscale_average(self):
        arr = np.array([[0.0, 0, 4, 4], [0, 0, 4, 4]])
        out = downscale_array(arr, 2)
        assert out.shape == (1, 2)
        assert np.allclose(out, [[0.0, 4.0]])
