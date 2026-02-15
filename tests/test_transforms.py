"""Tests for non-destructive rotation and scale transforms."""

import math
import sys
from pathlib import Path as SysPath

import pytest

sys.path.insert(0, str(SysPath(__file__).parent.parent / "src"))

from pyfreeform import Scene
from pyfreeform.core.coord import Coord
from pyfreeform.entities.dot import Dot
from pyfreeform.entities.line import Line
from pyfreeform.entities.curve import Curve
from pyfreeform.entities.rect import Rect
from pyfreeform.entities.ellipse import Ellipse
from pyfreeform.entities.polygon import Polygon
from pyfreeform.entities.text import Text
from pyfreeform.entities.path import Path
from pyfreeform.paths import Wave


# =========================================================================
# Rotation accumulation (no origin)
# =========================================================================


class TestRotateAccumulates:
    """rotate(angle) accumulates _rotation without affecting relative state."""

    def test_dot_rotate(self):
        dot = Dot(10, 20, radius=5)
        dot.rotate(45)
        assert dot.rotation == pytest.approx(45.0)
        assert not dot.is_relative

    def test_line_rotate(self):
        line = Line(0, 0, 100, 0)
        line.rotate(30)
        assert line.rotation == pytest.approx(30.0)
        assert not line.is_relative

    def test_curve_rotate(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        curve.rotate(60)
        assert curve.rotation == pytest.approx(60.0)
        assert not curve.is_relative

    def test_rect_rotate(self):
        rect = Rect(0, 0, 50, 30, fill="red")
        rect.rotate(90)
        assert rect.rotation == pytest.approx(90.0)
        assert not rect.is_relative

    def test_ellipse_rotate(self):
        ellipse = Ellipse(50, 50, 40, 20)
        ellipse.rotate(120)
        assert ellipse.rotation == pytest.approx(120.0)
        assert not ellipse.is_relative

    def test_polygon_rotate(self):
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="blue")
        poly.rotate(45)
        assert poly.rotation == pytest.approx(45.0)
        assert not poly.is_relative

    def test_text_rotate(self):
        text = Text(10, 20, "Hello", font_size=16)
        text.rotate(15)
        assert text.rotation == pytest.approx(15.0)
        assert not text.is_relative

    def test_path_rotate(self):
        wave = Wave(start=Coord(0, 50), end=Coord(200, 50), amplitude=20, frequency=3)
        path = Path(wave, width=2, color="blue")
        path.rotate(45)
        assert path.rotation == pytest.approx(45.0)
        assert not path.is_relative

    def test_multiple_rotations_compose(self):
        dot = Dot(10, 20)
        dot.rotate(30)
        dot.rotate(60)
        assert dot.rotation == pytest.approx(90.0)

    def test_rotation_wraps_at_360(self):
        dot = Dot(10, 20)
        dot.rotate(350)
        dot.rotate(20)
        assert dot.rotation == pytest.approx(10.0)


# =========================================================================
# Scale accumulation (no origin)
# =========================================================================


class TestScaleAccumulates:
    """scale(factor) accumulates _scale_factor without affecting relative state."""

    def test_dot_scale(self):
        dot = Dot(10, 20, radius=5)
        dot.scale(2.0)
        assert dot.scale_factor == pytest.approx(2.0)
        assert not dot.is_relative

    def test_line_scale(self):
        line = Line(0, 0, 100, 0)
        line.scale(3.0)
        assert line.scale_factor == pytest.approx(3.0)
        assert not line.is_relative

    def test_rect_scale(self):
        rect = Rect(0, 0, 50, 30, fill="red")
        rect.scale(0.5)
        assert rect.scale_factor == pytest.approx(0.5)
        assert not rect.is_relative

    def test_polygon_scale(self):
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="blue")
        poly.scale(2.0)
        assert poly.scale_factor == pytest.approx(2.0)
        assert not poly.is_relative

    def test_multiple_scales_compose(self):
        dot = Dot(10, 20)
        dot.scale(2.0)
        dot.scale(3.0)
        assert dot.scale_factor == pytest.approx(6.0)


# =========================================================================
# Rotation with origin (orbits position, preserves relative state)
# =========================================================================


class TestRotateWithOrigin:
    """rotate(angle, origin) orbits position and preserves relative state."""

    def test_dot_orbit(self):
        dot = Dot(100, 0)
        dot.rotate(90, origin=(0, 0))
        assert not dot.is_relative
        assert dot.rotation == pytest.approx(90.0)
        # Position should orbit: (100, 0) → (0, 100) around origin
        assert dot.x == pytest.approx(0.0, abs=0.01)
        assert dot.y == pytest.approx(100.0, abs=0.01)

    def test_line_orbit(self):
        line = Line(0, 0, 100, 0)
        line.rotate(90, origin=(50, 0))
        assert not line.is_relative
        assert line.rotation == pytest.approx(90.0)

    def test_rect_orbit(self):
        rect = Rect(0, 0, 100, 50, fill="red")
        rect.rotate(180, origin=(50, 25))
        assert not rect.is_relative
        assert rect.rotation == pytest.approx(180.0)


# =========================================================================
# Scale with origin (orbits position, preserves relative state)
# =========================================================================


class TestScaleWithOrigin:
    """scale(factor, origin) shifts position and preserves relative state."""

    def test_dot_scale_origin(self):
        dot = Dot(100, 0)
        dot.scale(2.0, origin=(0, 0))
        assert not dot.is_relative
        assert dot.scale_factor == pytest.approx(2.0)
        # Position should move: (100, 0) → (200, 0)
        assert dot.x == pytest.approx(200.0, abs=0.01)
        assert dot.y == pytest.approx(0.0, abs=0.01)


# =========================================================================
# World-space anchors
# =========================================================================


class TestWorldSpaceAnchors:
    """anchor() returns world-space coordinates (transforms applied)."""

    def test_line_anchor_rotated(self):
        line = Line(0, 0, 100, 0)
        line.rotate(90)
        start = line.anchor("start")
        end = line.anchor("end")
        # Rotated 90° around midpoint (50, 0): start → (50, -50), end → (50, 50)
        assert start.x == pytest.approx(50.0, abs=0.1)
        assert start.y == pytest.approx(-50.0, abs=0.1)
        assert end.x == pytest.approx(50.0, abs=0.1)
        assert end.y == pytest.approx(50.0, abs=0.1)

    def test_line_anchor_scaled(self):
        line = Line(0, 0, 100, 0)
        line.scale(2.0)
        start = line.anchor("start")
        end = line.anchor("end")
        # Scaled 2x around midpoint (50, 0): start → (-50, 0), end → (150, 0)
        assert start.x == pytest.approx(-50.0, abs=0.1)
        assert end.x == pytest.approx(150.0, abs=0.1)

    def test_rect_anchor_scaled(self):
        rect = Rect(0, 0, 100, 50, fill="red")
        rect.scale(2.0)
        # Rect center = (50, 25), scale around center
        tl = rect.anchor("top_left")
        br = rect.anchor("bottom_right")
        assert tl.x == pytest.approx(-50.0, abs=0.1)
        assert tl.y == pytest.approx(-25.0, abs=0.1)
        assert br.x == pytest.approx(150.0, abs=0.1)
        assert br.y == pytest.approx(75.0, abs=0.1)

    def test_polygon_anchor_rotated(self):
        # Equilateral triangle
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="blue")
        original_v0 = poly.anchor("v0")
        poly.rotate(90)
        rotated_v0 = poly.anchor("v0")
        # World-space v0 should differ from original
        assert abs(original_v0.x - rotated_v0.x) > 1 or abs(original_v0.y - rotated_v0.y) > 1

    def test_curve_anchor_identity(self):
        """With no transforms, anchor() matches model-space points."""
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        assert curve.anchor("start").x == pytest.approx(0.0)
        assert curve.anchor("end").x == pytest.approx(100.0)


# =========================================================================
# World-space bounds
# =========================================================================


class TestWorldSpaceBounds:
    """bounds() returns world-space AABB (transforms applied)."""

    def test_dot_bounds_scaled(self):
        dot = Dot(50, 50, radius=10)
        dot.scale(2.0)
        min_x, min_y, max_x, max_y = dot.bounds()
        # World radius = 10 * 2 = 20
        assert min_x == pytest.approx(30.0, abs=0.1)
        assert max_x == pytest.approx(70.0, abs=0.1)

    def test_line_bounds_rotated_90(self):
        line = Line(0, 0, 100, 0, width=1)
        line.rotate(90)
        min_x, min_y, max_x, max_y = line.bounds()
        # Line (0,0)→(100,0) rotated 90° around midpoint (50,0)
        # → vertical line at x=50, y=-50 to y=50
        assert abs(min_x - max_x) < 2  # Nearly vertical (plus stroke)
        assert (max_y - min_y) == pytest.approx(100.0, abs=2)

    def test_rect_bounds_identity(self):
        """No transforms → bounds unchanged."""
        rect = Rect(10, 20, 100, 50, fill="red")
        min_x, min_y, max_x, max_y = rect.bounds()
        assert min_x == pytest.approx(10.0)
        assert min_y == pytest.approx(20.0)
        assert max_x == pytest.approx(110.0)
        assert max_y == pytest.approx(70.0)

    def test_polygon_bounds_scaled(self):
        poly = Polygon([(0, 0), (100, 0), (50, 100)], fill="blue")
        b1 = poly.bounds()
        poly.scale(2.0)
        b2 = poly.bounds()
        # Width and height should roughly double
        w1 = b1[2] - b1[0]
        w2 = b2[2] - b2[0]
        assert w2 == pytest.approx(w1 * 2, abs=1)


# =========================================================================
# World-space point_at
# =========================================================================


class TestWorldSpacePointAt:
    """point_at() returns world-space coordinates."""

    def test_line_point_at_scaled(self):
        line = Line(0, 0, 100, 0)
        line.scale(2.0)
        mid = line.point_at(0.5)
        # Midpoint should be at rotation_center (unchanged by uniform scale)
        assert mid.x == pytest.approx(50.0, abs=0.1)

    def test_curve_point_at_rotated(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        mid_before = curve.point_at(0.5)
        curve.rotate(90)
        mid_after = curve.point_at(0.5)
        # Rotation center is chord midpoint (50, 0).
        # point_at(0.5) is displaced by curvature, so it DOES move.
        # But its distance from the rotation center should be preserved.
        rc = curve.rotation_center
        dist_before = math.sqrt((mid_before.x - 50) ** 2 + (mid_before.y - 0) ** 2)
        dist_after = math.sqrt((mid_after.x - rc.x) ** 2 + (mid_after.y - rc.y) ** 2)
        assert dist_before == pytest.approx(dist_after, abs=0.5)


# =========================================================================
# SVG transform output
# =========================================================================


class TestSVGTransform:
    """to_svg() emits transform attribute when needed."""

    def test_no_transform_identity(self):
        dot = Dot(10, 20, radius=5)
        svg = dot.to_svg()
        assert "transform" not in svg

    def test_rotation_only(self):
        rect = Rect(0, 0, 100, 50, fill="red")
        rect.rotate(45)
        svg = rect.to_svg()
        assert 'transform="rotate(45' in svg

    def test_scale_only(self):
        dot = Dot(10, 20, radius=5)
        dot.scale(2.0)
        svg = dot.to_svg()
        assert 'transform="translate(' in svg
        assert "scale(2)" in svg

    def test_rotation_and_scale(self):
        line = Line(0, 0, 100, 0)
        line.rotate(30)
        line.scale(1.5)
        svg = line.to_svg()
        assert "rotate(30.0)" in svg
        assert "scale(1.5)" in svg

    def test_polygon_transform(self):
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="blue")
        poly.rotate(45)
        svg = poly.to_svg()
        assert "transform" in svg
        # Model-space vertices should appear in SVG
        assert "0.0,0.0" in svg or "0,0" in svg

    def test_path_transform(self):
        wave = Wave(start=Coord(0, 50), end=Coord(200, 50), amplitude=20, frequency=3)
        path = Path(wave, width=2, color="blue")
        path.scale(1.5)
        svg = path.to_svg()
        assert "transform" in svg
        assert "scale(1.5)" in svg


# =========================================================================
# fit_to_cell compatibility
# =========================================================================


class TestFitToCell:
    """fit_to_cell works correctly with non-destructive scale."""

    def test_fit_to_cell_dot(self):
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(radius=5.0, color="red")
        dot.fit_to_cell(0.8)
        # World-space bounds should fit within 80% of cell
        min_x, min_y, max_x, max_y = dot.bounds()
        assert max_x - min_x <= 80.1
        assert max_y - min_y <= 80.1

    def test_fit_to_cell_idempotent(self):
        """Calling fit_to_cell twice should give same result."""
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(radius=5.0, color="red")
        dot.fit_to_cell(0.8)
        b1 = dot.bounds()
        dot.fit_to_cell(0.8)
        b2 = dot.bounds()
        assert b1[0] == pytest.approx(b2[0], abs=0.1)
        assert b1[2] == pytest.approx(b2[2], abs=0.1)

    def test_fit_to_cell_rect(self):
        scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
        cell = scene.grid[0][0]
        rect = cell.add_rect(width=0.9, height=0.5, fill="red")
        rect.fit_to_cell(0.8)
        min_x, min_y, max_x, max_y = rect.bounds()
        assert max_x - min_x <= 80.1
        assert max_y - min_y <= 80.1


# =========================================================================
# Model-space properties unchanged
# =========================================================================


class TestModelSpacePreserved:
    """Properties return model-space values, unchanged by transforms."""

    def test_dot_radius_unchanged(self):
        dot = Dot(0, 0, radius=10)
        dot.scale(3.0)
        assert dot.radius == pytest.approx(10.0)

    def test_line_model_end(self):
        line = Line(0, 0, 100, 0)
        line.rotate(45)
        line.scale(2.0)
        # Model-space start/end unchanged
        assert line.start.x == pytest.approx(0.0)
        assert line.end.x == pytest.approx(100.0)

    def test_rect_model_dimensions(self):
        rect = Rect(0, 0, 100, 50, fill="red")
        rect.rotate(90)
        rect.scale(2.0)
        assert rect.width == pytest.approx(100.0)
        assert rect.height == pytest.approx(50.0)

    def test_curve_model_curvature(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        curve.scale(3.0)
        assert curve.curvature == pytest.approx(0.5)


# =========================================================================
# rotation_center property
# =========================================================================


class TestRotationCenter:
    """rotation_center returns the natural pivot for each entity type."""

    def test_dot_default_position(self):
        dot = Dot(10, 20)
        rc = dot.rotation_center
        assert rc.x == pytest.approx(10.0)
        assert rc.y == pytest.approx(20.0)

    def test_rect_center(self):
        rect = Rect(0, 0, 100, 50, fill="red")
        rc = rect.rotation_center
        assert rc.x == pytest.approx(50.0)
        assert rc.y == pytest.approx(25.0)

    def test_line_midpoint(self):
        line = Line(0, 0, 100, 0)
        rc = line.rotation_center
        assert rc.x == pytest.approx(50.0)
        assert rc.y == pytest.approx(0.0)

    def test_curve_chord_midpoint(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        rc = curve.rotation_center
        assert rc.x == pytest.approx(50.0)
        assert rc.y == pytest.approx(0.0)

    def test_polygon_centroid(self):
        poly = Polygon([(0, 0), (100, 0), (50, 90)], fill="blue")
        rc = poly.rotation_center
        assert rc.x == pytest.approx(50.0)
        assert rc.y == pytest.approx(30.0)

    def test_ellipse_default_position(self):
        ellipse = Ellipse(50, 50, 40, 20)
        rc = ellipse.rotation_center
        assert rc.x == pytest.approx(50.0)
        assert rc.y == pytest.approx(50.0)


# =========================================================================
# angle_at with rotation
# =========================================================================


class TestAngleAtWithRotation:
    """angle_at() adds entity rotation to the model-space angle."""

    def test_line_angle_at_rotated(self):
        line = Line(0, 0, 100, 0)
        assert line.angle_at(0.5) == pytest.approx(0.0)
        line.rotate(45)
        assert line.angle_at(0.5) == pytest.approx(45.0)

    def test_curve_angle_at_rotated(self):
        # Straight-ish curve
        curve = Curve(0, 0, 100, 0, curvature=0.0)
        base_angle = curve.angle_at(0.5)
        curve.rotate(90)
        assert curve.angle_at(0.5) == pytest.approx(base_angle + 90.0)
