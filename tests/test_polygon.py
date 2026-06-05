"""Tests for Polygon vertex handling — valid forms work, bad specs fail loudly."""

import pytest

from pyfreeform import Polygon, Coord, Point


class TestPolygonVertexSpecs:
    def test_tuple_vertices(self):
        p = Polygon([(0, 0), (10, 0), (5, 10)], fill="red")
        assert len(p.vertices) == 3

    def test_coord_vertices(self):
        p = Polygon([Coord(0, 0), Coord(10, 0), Coord(5, 10)])
        assert len(p.vertices) == 3

    def test_point_vertices_reactive(self):
        pts = [Point(0, 0), Point(10, 0), Point(5, 10)]
        p = Polygon(pts)
        assert len(p.vertices) == 3

    def test_point_anchor_pair(self):
        a, b, c = Point(0, 0), Point(10, 0), Point(5, 10)
        p = Polygon([(a, "center"), (b, "center"), (c, "center")])
        assert len(p.vertices) == 3


class TestPolygonValidation:
    def test_list_vertex_raises(self):
        # A list instead of a tuple used to be silently dropped.
        with pytest.raises(TypeError, match="Invalid polygon vertex"):
            Polygon([(0, 0), (10, 0), (5, 10), [3, 3]])

    def test_none_vertex_raises(self):
        with pytest.raises(TypeError, match="Invalid polygon vertex"):
            Polygon([(0, 0), (10, 0), None])

    def test_too_few_vertices_still_raises(self):
        with pytest.raises(ValueError, match="at least 3"):
            Polygon([(0, 0), (10, 0)])

    def test_no_silent_vertex_loss(self):
        # 4 good vertices in -> 4 out (the silent-drop regression guard).
        p = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
        assert len(p.vertices) == 4
