"""Tests for Color parsing — focus on numeric RGB acceptance."""

import numpy as np
import pytest

from pyfreeform import Color


class TestColorRGBNumeric:
    def test_int_rgb(self):
        assert Color((255, 0, 0)).to_hex() == "#ff0000"

    def test_float_rgb_rounds(self):
        # Was the bug: floats raised "Unknown format code 'x'".
        assert Color((255.0, 0.0, 0.0)).to_hex() == "#ff0000"
        assert Color((127.5, 10.4, 200.6)).to_hex() == "#800ac9"  # round-half-to-even

    def test_numpy_scalar_rgb(self):
        c = Color((np.float64(255.0), np.uint8(0), np.uint8(0)))
        assert c.to_hex() == "#ff0000"

    def test_computed_rgb(self):
        # The common real-world shape: arithmetic on channel values.
        r, g, b = 200, 100, 50
        assert Color((r * 0.5, g, b)).to_hex() == "#646432"  # (100, 100, 50)

    def test_out_of_range_raises_clearly(self):
        with pytest.raises(ValueError, match="0-255"):
            Color((300, 0, 0))
        with pytest.raises(ValueError, match="0-255"):
            Color((-1.0, 0, 0))

    def test_wrong_length_raises(self):
        with pytest.raises(ValueError, match="3 values"):
            Color((255, 0))


class TestColorBasics:
    def test_named(self):
        assert Color("red").to_hex() == "red"
        assert Color("red").to_rgb() == (255, 0, 0)

    def test_hex_passthrough_and_shorthand(self):
        assert Color("#ff0000").to_hex() == "#ff0000"
        assert Color("#f00").to_hex() == "#ff0000"

    def test_round_trip_rgb(self):
        assert Color((38, 166, 154)).to_rgb() == (38, 166, 154)
