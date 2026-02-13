"""Tests for AnchorSpec — unified anchoring with strings, RelCoord, and tuples."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import (
    AnchorSpec,
    Connection,
    Coord,
    Dot,
    Ellipse,
    Line,
    Polygon,
    Rect,
    RelCoord,
    Scene,
)


# =========================================================================
# Entity anchors with RelCoord / tuple
# =========================================================================


class TestEntityRelCoordAnchors:
    def test_dot_relcoord_anchor(self):
        """Dot has zero-size bounds; RelCoord maps to its position."""
        dot = Dot(50, 50, radius=5)
        # (0.5, 0.5) on a zero-size AABB still returns position
        result = dot.anchor(RelCoord(0.5, 0.5))
        assert result == Coord(50, 50)

    def test_dot_tuple_anchor(self):
        """Tuple is coerced to RelCoord."""
        dot = Dot(50, 50, radius=5)
        result = dot.anchor((0.5, 0.5))
        assert result == Coord(50, 50)

    def test_rect_relcoord_center(self):
        """RelCoord(0.5, 0.5) resolves to center of rect."""
        rect = Rect(10, 20, 100, 60)
        result = rect.anchor(RelCoord(0.5, 0.5))
        assert abs(result.x - 60) < 1e-6
        assert abs(result.y - 50) < 1e-6

    def test_rect_relcoord_top_left(self):
        """RelCoord(0, 0) resolves to top-left of rect."""
        rect = Rect(10, 20, 100, 60)
        result = rect.anchor(RelCoord(0, 0))
        assert abs(result.x - 10) < 1e-6
        assert abs(result.y - 20) < 1e-6

    def test_rect_relcoord_arbitrary(self):
        """Arbitrary fraction resolves proportionally."""
        rect = Rect(0, 0, 200, 100)
        result = rect.anchor((0.7, 0.3))
        assert abs(result.x - 140) < 1e-6
        assert abs(result.y - 30) < 1e-6

    def test_rect_rotated_relcoord(self):
        """RelCoord on a rotated rect goes through local space."""
        rect = Rect(0, 0, 100, 100, rotation=90)
        # (0,0) = top-left in local space, then rotated
        tl = rect.anchor(RelCoord(0, 0))
        # (1,1) = bottom-right in local space, then rotated
        br = rect.anchor(RelCoord(1, 1))
        # They should be symmetric about center
        center = rect.anchor("center")
        assert abs(tl.x + br.x - 2 * center.x) < 1e-3
        assert abs(tl.y + br.y - 2 * center.y) < 1e-3

    def test_polygon_relcoord_anchor(self):
        """Polygon AABB-based RelCoord resolution."""
        poly = Polygon([(0, 0), (100, 0), (50, 100)], fill="red")
        # (0, 0) should give AABB top-left = (0, 0)
        tl = poly.anchor((0, 0))
        assert tl.x == pytest.approx(0, abs=1e-6)
        assert tl.y == pytest.approx(0, abs=1e-6)
        # (1, 1) should give AABB bottom-right = (100, 100)
        br = poly.anchor((1, 1))
        assert br.x == pytest.approx(100, abs=1e-6)
        assert br.y == pytest.approx(100, abs=1e-6)

    def test_line_relcoord_anchor(self):
        """Line AABB-based RelCoord resolution."""
        line = Line(0, 0, 100, 0)
        # (0.5, 0.5) on a horizontal line → midpoint
        mid = line.anchor((0.5, 0.5))
        assert mid.x == pytest.approx(50, abs=1e-6)
        assert mid.y == pytest.approx(0, abs=1e-6)

    def test_ellipse_relcoord_anchor(self):
        """Ellipse AABB-based RelCoord resolution."""
        e = Ellipse(100, 100, rx=50, ry=30)
        # (0, 0) = AABB top-left
        tl = e.anchor((0, 0))
        assert tl.x == pytest.approx(50, abs=1e-6)
        assert tl.y == pytest.approx(70, abs=1e-6)


# =========================================================================
# Surface anchors with RelCoord / tuple
# =========================================================================


class TestSurfaceRelCoordAnchors:
    def test_cell_tuple_anchor(self):
        """Cell accepts (rx, ry) tuple as anchor."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0, 0]
        result = cell.anchor((0.5, 0.5))
        assert result == cell.center

    def test_cell_relcoord_anchor(self):
        """Cell accepts RelCoord as anchor."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0, 0]
        result = cell.anchor(RelCoord(0.0, 0.0))
        assert result == cell.top_left

    def test_cell_arbitrary_anchor(self):
        """Arbitrary fraction on cell resolves proportionally."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
        cell = scene.grid[0, 0]
        x, y, w, h = cell.bounds
        result = cell.anchor((0.25, 0.75))
        assert result.x == pytest.approx(x + 0.25 * w, abs=1e-6)
        assert result.y == pytest.approx(y + 0.75 * h, abs=1e-6)


# =========================================================================
# Connection with AnchorSpec
# =========================================================================


class TestConnectionAnchorSpec:
    def test_connection_tuple_anchors(self):
        """Connections accept tuple anchors."""
        scene = Scene(200, 200)
        d1 = Dot(50, 50, radius=5)
        d2 = Dot(150, 150, radius=5)
        scene.place(d1)
        scene.place(d2)
        conn = d1.connect(d2, start_anchor=(0.5, 0.5), end_anchor=(0.5, 0.5))
        assert conn.start_point == Coord(50, 50)
        assert conn.end_point == Coord(150, 150)

    def test_connection_relcoord_anchors(self):
        """Connections accept RelCoord anchors."""
        scene = Scene(200, 200)
        d1 = Dot(50, 50, radius=5)
        d2 = Dot(150, 150, radius=5)
        scene.place(d1)
        scene.place(d2)
        conn = d1.connect(d2, start_anchor=RelCoord(0.5, 0.5), end_anchor=RelCoord(0.5, 0.5))
        assert conn.start_point == Coord(50, 50)
        assert conn.end_point == Coord(150, 150)

    def test_connection_string_anchors_unchanged(self):
        """Existing string anchors still work."""
        scene = Scene(200, 200)
        d1 = Dot(50, 50, radius=5)
        d2 = Dot(150, 150, radius=5)
        scene.place(d1)
        scene.place(d2)
        conn = d1.connect(d2, start_anchor="center", end_anchor="center")
        assert conn.start_point == Coord(50, 50)
        assert conn.end_point == Coord(150, 150)

    def test_surface_connect_tuple_anchors(self):
        """Surface.connect() accepts tuple anchors."""
        scene = Scene.with_grid(cols=2, rows=1, cell_size=100)
        cell_a = scene.grid[0, 0]
        cell_b = scene.grid[0, 1]
        conn = cell_a.connect(cell_b, start_anchor=(1.0, 0.5), end_anchor=(0.0, 0.5))
        # start_anchor=(1.0, 0.5) = right edge center of cell_a
        # end_anchor=(0.0, 0.5) = left edge center of cell_b
        assert conn.start_point == cell_a.anchor("right")
        assert conn.end_point == cell_b.anchor("left")


# =========================================================================
# Backward compatibility
# =========================================================================


class TestBackwardCompat:
    def test_all_string_anchors_still_work(self):
        """All 9 named positions work on entities and surfaces."""
        rect = Rect(0, 0, 100, 100)
        names = [
            "center", "top_left", "top_right",
            "bottom_left", "bottom_right",
            "top", "bottom", "left", "right",
        ]
        for name in names:
            result = rect.anchor(name)
            assert isinstance(result, Coord), f"anchor('{name}') failed"

    def test_entity_specific_anchors(self):
        """Entity-specific string anchors still work."""
        line = Line(0, 0, 100, 0)
        assert isinstance(line.anchor("start"), Coord)
        assert isinstance(line.anchor("end"), Coord)

        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="red")
        assert isinstance(poly.anchor("v0"), Coord)
        assert isinstance(poly.anchor("v1"), Coord)
        assert isinstance(poly.anchor("v2"), Coord)

    def test_default_anchor_is_center(self):
        """Calling anchor() with no args defaults to 'center'."""
        dot = Dot(50, 50)
        assert dot.anchor() == dot.anchor("center")


# =========================================================================
# Error cases
# =========================================================================


class TestErrorCases:
    def test_invalid_string_anchor(self):
        """Invalid string raises ValueError."""
        dot = Dot(50, 50)
        with pytest.raises(ValueError, match="no anchor"):
            dot.anchor("nonexistent")

    def test_invalid_surface_anchor(self):
        """Invalid string on surface raises ValueError."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0, 0]
        with pytest.raises(ValueError, match="Unknown anchor"):
            cell.anchor("nonexistent")

    def test_invalid_type_raises(self):
        """Non-coercible type raises TypeError."""
        dot = Dot(50, 50)
        with pytest.raises(TypeError):
            dot.anchor(42)
