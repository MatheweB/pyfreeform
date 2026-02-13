"""Tests for PathShape is_closed and connection_data behavior."""

import math
import sys
from pathlib import Path as FilePath

import pytest

sys.path.insert(0, str(FilePath(__file__).parent.parent / "src"))

from pyfreeform import Dot, Scene
from pyfreeform.entities.path import Path
from pyfreeform.paths import Lissajous, Spiral, Wave, Zigzag


# =========================================================================
# is_closed property
# =========================================================================


def test_wave_is_open():
    assert Wave().is_closed is False


def test_zigzag_is_open():
    assert Zigzag().is_closed is False


def test_spiral_is_open():
    assert Spiral().is_closed is False


def test_lissajous_is_closed():
    assert Lissajous().is_closed is True


# =========================================================================
# to_svg_path_d respects is_closed
# =========================================================================


def test_lissajous_svg_path_ends_with_Z():
    liss = Lissajous(center=(100, 100), size=50)
    d = liss.to_svg_path_d()
    assert d.rstrip().endswith("Z")


def test_wave_svg_path_no_Z():
    wave = Wave(start=(0, 0), end=(100, 0))
    d = wave.to_svg_path_d()
    assert not d.rstrip().endswith("Z")


# =========================================================================
# connection_data behavior
# =========================================================================


def test_closed_path_connection_data_raises():
    """Closed Path raises ValueError with helpful message."""
    liss = Lissajous(center=(100, 100), size=50)
    path = Path(liss, closed=True)
    with pytest.raises(ValueError, match="start_t/end_t"):
        path.connection_data()


def test_degenerate_chord_raises():
    """Path with coincident start/end (not explicitly closed) raises ValueError."""
    liss = Lissajous(center=(100, 100), size=50)
    # closed=False but Lissajous returns to start at t=1
    path = Path(liss, closed=False)
    with pytest.raises(ValueError, match="start and end coincide"):
        path.connection_data()


def test_arc_of_closed_path_succeeds():
    """Path with start_t/end_t arc from closed pathable works."""
    liss = Lissajous(center=(100, 100), size=50)
    path = Path(liss, start_t=0, end_t=0.5)
    kind, beziers = path.connection_data()
    assert kind == "path"
    assert len(beziers) > 0
    # Start and end should NOT coincide
    p0 = beziers[0][0]
    pN = beziers[-1][3]
    assert math.hypot(pN.x - p0.x, pN.y - p0.y) > 1e-6


def test_open_path_connection_data_succeeds():
    """Open paths work as connection shapes."""
    wave = Wave(start=(0, 0), end=(100, 0), amplitude=20)
    path = Path(wave)
    kind, beziers = path.connection_data()
    assert kind == "path"
    assert len(beziers) > 0


def test_connection_with_lissajous_arc():
    """Full integration: connect two dots via a Lissajous arc."""
    scene = Scene(300, 300)
    d1 = Dot(50, 150, radius=5)
    d2 = Dot(250, 150, radius=5)
    scene.place(d1)
    scene.place(d2)

    liss_arc = Path(Lissajous(size=50), start_t=0, end_t=0.5)
    conn = d1.connect(d2, path=liss_arc)

    # Connection should render without error
    svg = conn.to_svg()
    assert "<path" in svg or "<line" in svg
