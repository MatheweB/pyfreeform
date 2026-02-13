"""Tests for along= parametric positioning, angle_at, textPath warping, and StrokedPathMixin."""

import math
import pytest

from pyfreeform import (
    Scene,
    Line,
    Curve,
    Ellipse,
    Dot,
    get_angle_at,
    Point,
    Connection,
)
from pyfreeform.core.coord import Coord


# =========================================================================
# Helper: create a simple scene with a surface to test builder methods
# =========================================================================


def make_scene():
    return Scene.with_grid(cols=10, rows=10, cell_size=10)


# =========================================================================
# 1. angle_at() — analytical tangent angles
# =========================================================================


class TestAngleAt:
    def test_line_constant_angle(self):
        line = Line(0, 0, 100, 0)
        assert line.angle_at(0) == pytest.approx(0.0)
        assert line.angle_at(0.5) == pytest.approx(0.0)
        assert line.angle_at(1.0) == pytest.approx(0.0)

    def test_line_45_degrees(self):
        line = Line(0, 0, 100, 100)
        assert line.angle_at(0.5) == pytest.approx(45.0)

    def test_line_vertical(self):
        line = Line(0, 0, 0, 100)
        assert line.angle_at(0) == pytest.approx(90.0)

    def test_curve_angle_at_endpoints(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        # At start: tangent from P0 toward P1 (control)
        angle_start = curve.angle_at(0)
        # At end: tangent from P1 toward P2
        angle_end = curve.angle_at(1.0)
        # Both should be within -90..90 for a horizontal curve
        assert -90 <= angle_start <= 90
        assert -90 <= angle_end <= 90

    def test_curve_zero_curvature_is_straight(self):
        curve = Curve(0, 0, 100, 0, curvature=0)
        assert curve.angle_at(0.5) == pytest.approx(0.0, abs=0.1)

    def test_ellipse_angle_at(self):
        ellipse = Ellipse(0, 0, rx=50, ry=50)
        # At t=0 (rightmost), tangent should be ~90° (moving upward)
        angle = ellipse.angle_at(0)
        assert angle == pytest.approx(90.0, abs=1.0)

    def test_connection_angle_at(self):
        dot1 = Dot(0, 0)
        dot2 = Dot(100, 0)
        conn = Connection(dot1, dot2)
        assert conn.angle_at(0.5) == pytest.approx(0.0)


# =========================================================================
# 2. get_angle_at() — fallback for custom Pathables
# =========================================================================


class TestGetAngleAt:
    def test_uses_angle_at_if_available(self):
        line = Line(0, 0, 100, 0)
        assert get_angle_at(line, 0.5) == pytest.approx(0.0)

    def test_numeric_fallback(self):
        class CustomPath:
            def point_at(self, t):
                return Point(t * 100, t * 50)

        path = CustomPath()
        angle = get_angle_at(path, 0.5) # pyright: ignore[reportArgumentType]
        expected = math.degrees(math.atan2(50, 100))
        assert angle == pytest.approx(expected, abs=0.5)


# =========================================================================
# 3. to_svg_path_d() — SVG path strings
# =========================================================================


class TestToSvgPathD:
    def test_line_path_d(self):
        line = Line(10, 20, 30, 40)
        assert line.to_svg_path_d() == "M 10 20 L 30 40"

    def test_curve_path_d(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        d = curve.to_svg_path_d()
        assert d.startswith("M 0 0 Q ")
        assert d.endswith("100 0")

    def test_ellipse_path_d(self):
        ellipse = Ellipse(50, 50, rx=30, ry=20)
        d = ellipse.to_svg_path_d()
        assert "A" in d  # Contains arc commands

    def test_connection_path_d(self):
        dot1 = Dot(10, 20)
        dot2 = Dot(30, 40)
        conn = Connection(dot1, dot2)
        d = conn.to_svg_path_d()
        # Line → direct M L, no bezier overhead
        assert d == "M 10 20 L 30 40"

    def test_connection_curve_path_d(self):
        dot1 = Dot(10, 20)
        dot2 = Dot(30, 40)
        conn = Connection(dot1, dot2, curvature=0.5)
        d = conn.to_svg_path_d()
        # Curve → single cubic bezier (exact degree elevation)
        assert d.startswith("M ")
        assert "C " in d


# =========================================================================
# 4. StrokedPathMixin — Line/Curve/Connection SVG output
# =========================================================================


class TestStrokedPathMixin:
    def test_line_svg_has_arrow_marker(self):
        line = Line(0, 0, 100, 0, end_cap="arrow")
        svg = line.to_svg()
        assert "marker-end=" in svg

    def test_curve_svg_has_arrow_marker(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5, end_cap="arrow")
        svg = curve.to_svg()
        assert "marker-end=" in svg

    def test_connection_svg_has_arrow_marker(self):
        dot1 = Dot(0, 0)
        dot2 = Dot(100, 0)
        conn = Connection(dot1, dot2, end_cap="arrow")
        svg = conn.to_svg()
        assert "marker-end=" in svg

    def test_line_effective_caps(self):
        line = Line(0, 0, 100, 0, cap="butt", end_cap="arrow")
        assert line.effective_start_cap == "butt"
        assert line.effective_end_cap == "arrow"

    def test_line_default_caps(self):
        line = Line(0, 0, 100, 0)
        assert line.effective_start_cap == "round"
        assert line.effective_end_cap == "round"


# =========================================================================
# 5. Surface along= for each entity type
# =========================================================================


class TestSurfaceAlong:
    def test_add_dot_along(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        dot = scene.add_dot(along=line, t=0.5)
        assert dot.position.x == pytest.approx(50.0)
        assert dot.position.y == pytest.approx(0.0)

    def test_add_dot_along_defaults_t_to_half(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        dot = scene.add_dot(along=line)
        assert dot.position.x == pytest.approx(50.0)

    def test_add_rect_along(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        rect = scene.add_rect(width=0.1, height=0.1, along=line, t=0.5)
        # Center should be at line midpoint (50, 0)
        center_x = rect.x + rect.width / 2
        center_y = rect.y + rect.height / 2
        assert center_x == pytest.approx(50.0)
        assert center_y == pytest.approx(0.0)

    def test_add_rect_along_with_align(self):
        scene = make_scene()
        # A 45-degree line
        line = Line(0, 0, 100, 100)
        scene.place(line)
        rect = scene.add_rect(width=0.1, height=0.1, along=line, t=0.5, align=True)
        assert rect.rotation == pytest.approx(45.0)

    def test_add_ellipse_along(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        ellipse = scene.add_ellipse(rx=0.05, ry=0.03, along=line, t=0.5)
        assert ellipse.position.x == pytest.approx(50.0)
        assert ellipse.position.y == pytest.approx(0.0)

    def test_add_ellipse_along_align(self):
        scene = make_scene()
        line = Line(0, 0, 100, 100)
        scene.place(line)
        ellipse = scene.add_ellipse(rx=0.05, ry=0.03, along=line, t=0.5, align=True)
        assert ellipse.rotation == pytest.approx(45.0)

    def test_add_ellipse_along_align_with_user_rotation(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        ellipse = scene.add_ellipse(rx=0.05, ry=0.03, along=line, t=0.5, align=True, rotation=10)
        # tangent=0° + user_rotation=10°
        assert ellipse.rotation == pytest.approx(10.0)

    def test_add_text_along_with_t(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        text = scene.add_text("Hi", along=line, t=0.5, align=True)
        assert text.position.x == pytest.approx(50.0)

    def test_add_polygon_along(self):
        scene = make_scene()
        line = Line(0, 0, 100, 0)
        scene.place(line)
        # Triangle vertices (relative coords)
        polygon = scene.add_polygon(
            [(0.4, 0.4), (0.6, 0.4), (0.5, 0.6)],
            along=line,
            t=0.5,
        )
        # The centroid should be near (50, 0) after repositioning
        assert polygon.position.x == pytest.approx(50.0, abs=1)
        assert polygon.position.y == pytest.approx(0.0, abs=1)

    def test_add_line_along(self):
        scene = make_scene()
        path = Line(0, 0, 200, 0)
        scene.place(path)
        # Place a short line along the path at t=0.5
        line = scene.add_line(start=(0, 0), end=(20, 0), along=path, t=0.5)
        midpoint = line.anchor("center")
        assert midpoint.x == pytest.approx(100.0)

    def test_add_curve_along(self):
        scene = make_scene()
        path = Line(0, 0, 200, 0)
        scene.place(path)
        curve = scene.add_curve(
            start=(0, 0),
            end=(20, 0),
            curvature=0.3,
            along=path,
            t=0.5,
        )
        midpoint = curve.point_at(0.5)
        # Midpoint should be near (100, y) — x repositioned
        assert midpoint.x == pytest.approx(100.0, abs=2)

    def test_add_diagonal_along(self):
        scene = make_scene()
        path = Line(0, 0, 200, 0)
        scene.place(path)
        line = scene.add_diagonal(along=path, t=0.5)
        midpoint = line.anchor("center")
        assert midpoint.x == pytest.approx(100.0, abs=1)


# =========================================================================
# 6. TextPath warping
# =========================================================================


class TestTextPathWarp:
    def test_textpath_svg_output(self):
        scene = Scene(200, 100)
        curve = Curve(0, 50, 200, 50, curvature=0.5)
        scene.place(curve)
        # along without t → textPath warp mode
        cell = scene
        text = cell.add_text("Hello", along=curve)
        assert text.has_textpath

        svg = text.to_svg()
        assert "<textPath" in svg
        assert 'href="#' in svg

    def test_textpath_defs_in_scene(self):
        scene = Scene(200, 100)
        curve = Curve(0, 50, 200, 50, curvature=0.5)
        scene.place(curve)
        scene.add_text("Hello", along=curve)

        full_svg = scene.to_svg()
        assert "<defs>" in full_svg
        assert "textpath-" in full_svg
        assert "<textPath" in full_svg

    def test_textpath_requires_to_svg_path_d(self):
        scene = Scene(200, 100)

        class FakePath:
            def point_at(self, t):
                return Point(t * 100, 50)

        with pytest.raises(TypeError, match="to_svg_path_d"):
            scene.add_text("Hello", along=FakePath())  # pyright: ignore[reportArgumentType]

    def test_text_along_with_t_does_not_warp(self):
        scene = Scene(200, 100)
        curve = Curve(0, 50, 200, 50, curvature=0.5)
        scene.place(curve)
        text = scene.add_text("Hi", along=curve, t=0.5)
        assert not text.has_textpath
        svg = text.to_svg()
        assert "<textPath" not in svg


# =========================================================================
# 7. Edge cases
# =========================================================================


class TestEdgeCases:
    def test_along_t_zero(self):
        scene = make_scene()
        line = Line(10, 20, 30, 40)
        scene.place(line)
        dot = scene.add_dot(along=line, t=0)
        assert dot.position.x == pytest.approx(10.0)
        assert dot.position.y == pytest.approx(20.0)

    def test_along_t_one(self):
        scene = make_scene()
        line = Line(10, 20, 30, 40)
        scene.place(line)
        dot = scene.add_dot(along=line, t=1.0)
        assert dot.position.x == pytest.approx(30.0)
        assert dot.position.y == pytest.approx(40.0)

    def test_degenerate_zero_length_path(self):
        line = Line(50, 50, 50, 50)
        assert line.angle_at(0.5) == 0.0
        assert get_angle_at(line, 0.5) == 0.0

    def test_angle_at_analytical_matches_numeric(self):
        """Verify analytical angle_at matches numeric get_angle_at fallback."""
        curve = Curve(0, 0, 100, 0, curvature=0.7)
        for t in [0.0, 0.25, 0.5, 0.75, 1.0]:
            analytical = curve.angle_at(t)
            # Compute numeric fallback manually
            eps = 1e-5
            t0 = max(0.0, t - eps)
            t1 = min(1.0, t + eps)
            p0 = curve.point_at(t0)
            p1 = curve.point_at(t1)
            dx = p1.x - p0.x
            dy = p1.y - p0.y
            numeric = math.degrees(math.atan2(dy, dx))
            assert analytical == pytest.approx(numeric, abs=0.5)


# =========================================================================
# 8. Curve movement fixes (Phase 4)
# =========================================================================


class TestCurveMovement:
    def test_curve_translate(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        # Move both endpoints
        curve.position = Coord(10, 20)
        curve.end = Coord(110, 20)
        assert curve.start == Coord(10, 20)
        assert curve.end == Coord(110, 20)

    def test_curve_rotate(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        curve.rotate(90)
        # Non-destructive: rotation stored, model-space unchanged
        assert curve.rotation == pytest.approx(90.0)
        # World-space anchor should differ from model-space start
        ws_start = curve.anchor("start")
        assert ws_start.x != 0 or ws_start.y != 0

    def test_curve_scale(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5)
        curve.scale(2.0)
        # Non-destructive: scale_factor stored
        assert curve.scale_factor == pytest.approx(2.0)
        # World-space distance between anchors should roughly double
        ws_start = curve.anchor("start")
        ws_end = curve.anchor("end")
        dx = ws_end.x - ws_start.x
        dy = ws_end.y - ws_start.y
        length = math.sqrt(dx * dx + dy * dy)
        assert length == pytest.approx(200.0, abs=1)
