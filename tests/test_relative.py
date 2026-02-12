"""Tests for the relative-first coordinate system.

Covers:
- within= parameter for all add_*() methods
- Multi-pass: reading and writing .at property
- Reactive positioning: entities auto-update when references move
- Circular reference detection
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene
from pyfreeform.core.coord import Coord
from pyfreeform.core.relcoord import RelCoord
from pyfreeform.core.binding import Binding


# =========================================================================
# Helper
# =========================================================================


def _scene_with_cell(cell_size=100):
    """Create a 1x1 scene with a single cell."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=cell_size)
    return scene, scene.grid[0, 0]


# =========================================================================
# within= for add_dot
# =========================================================================


class TestWithinDot:
    def test_dot_centered_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        dot = cell.add_dot(within=rect, at="center", color="red")
        # rect is 50x50 centered at (50,50) → rect bounds: (25,25,75,75)
        assert abs(dot.x - 50.0) < 0.01
        assert abs(dot.y - 50.0) < 0.01

    def test_dot_top_left_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        dot = cell.add_dot(within=rect, at="top_left", color="red")
        # top-left of rect bounds = (25, 25)
        assert abs(dot.x - 25.0) < 0.01
        assert abs(dot.y - 25.0) < 0.01

    def test_dot_bottom_right_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        dot = cell.add_dot(within=rect, at="bottom_right", color="red")
        # bottom-right of rect bounds = (75, 75)
        assert abs(dot.x - 75.0) < 0.01
        assert abs(dot.y - 75.0) < 0.01


# =========================================================================
# within= for add_line
# =========================================================================


class TestWithinLine:
    def test_line_spans_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        line = cell.add_line(within=rect, start="top_left", end="bottom_right", color="red")
        # line should span rect bounds: (25,25) to (75,75)
        assert abs(line.start.x - 25.0) < 0.01
        assert abs(line.start.y - 25.0) < 0.01
        assert abs(line.end.x - 75.0) < 0.01
        assert abs(line.end.y - 75.0) < 0.01

    def test_line_left_to_right_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        line = cell.add_line(within=rect, start="left", end="right", color="red")
        # left/right are (0, 0.5) and (1, 0.5) of rect bounds
        assert abs(line.start.x - 25.0) < 0.01
        assert abs(line.start.y - 50.0) < 0.01
        assert abs(line.end.x - 75.0) < 0.01
        assert abs(line.end.y - 50.0) < 0.01


# =========================================================================
# within= for add_curve
# =========================================================================


class TestWithinCurve:
    def test_curve_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        curve = cell.add_curve(
            within=rect, start="bottom_left", end="top_right", curvature=0.5, color="red"
        )
        # start=(0,1), end=(1,0) of rect bounds: (25,75) to (75,25)
        assert abs(curve.start.x - 25.0) < 0.01
        assert abs(curve.start.y - 75.0) < 0.01
        assert abs(curve.end.x - 75.0) < 0.01
        assert abs(curve.end.y - 25.0) < 0.01


# =========================================================================
# within= for add_ellipse
# =========================================================================


class TestWithinEllipse:
    def test_ellipse_centered_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        ellipse = cell.add_ellipse(within=rect, at="center", rx=0.5, ry=0.5, fill="red")
        # center of rect = (50, 50)
        assert abs(ellipse.x - 50.0) < 0.01
        assert abs(ellipse.y - 50.0) < 0.01
        # rx=0.5 of rect width (50) = 25, ry=0.5 of rect height (50) = 25
        assert abs(ellipse.rx - 25.0) < 0.01
        assert abs(ellipse.ry - 25.0) < 0.01

    def test_ellipse_sizes_relative_to_within(self):
        scene, cell = _scene_with_cell(200)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.25)
        # rect is 100x50
        ellipse = cell.add_ellipse(within=rect, rx=0.4, ry=0.4, fill="red")
        # rx=0.4 of rect width (100) = 40, ry=0.4 of rect height (50) = 20
        assert abs(ellipse.rx - 40.0) < 0.01
        assert abs(ellipse.ry - 20.0) < 0.01


# =========================================================================
# within= for add_rect
# =========================================================================


class TestWithinRect:
    def test_rect_within_rect(self):
        scene, cell = _scene_with_cell(100)
        outer = cell.add_rect(fill="blue", width=0.5, height=0.5)
        inner = cell.add_rect(within=outer, at="center", width=0.5, height=0.5, fill="red")
        # outer is 50x50 at center. inner is 0.5 of outer = 25x25 at center
        assert abs(inner.width - 25.0) < 0.01
        assert abs(inner.height - 25.0) < 0.01
        # inner center = outer center = (50, 50)
        # inner top-left = (50 - 12.5, 50 - 12.5) = (37.5, 37.5)
        assert abs(inner.x - 37.5) < 0.01
        assert abs(inner.y - 37.5) < 0.01


# =========================================================================
# within= for add_polygon
# =========================================================================


class TestWithinPolygon:
    def test_polygon_triangle_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        # Triangle spanning the rect
        triangle = cell.add_polygon([(0.5, 0.0), (1.0, 1.0), (0.0, 1.0)], within=rect, fill="red")
        verts = triangle.vertices
        # (0.5, 0.0) → rect x=25 + 0.5*50, y=25 + 0*50 = (50, 25)
        assert abs(verts[0].x - 50.0) < 0.01
        assert abs(verts[0].y - 25.0) < 0.01
        # (1.0, 1.0) → rect x=25 + 1.0*50, y=25 + 1.0*50 = (75, 75)
        assert abs(verts[1].x - 75.0) < 0.01
        assert abs(verts[1].y - 75.0) < 0.01

    def test_polygon_rotation_not_overridden_by_relative_vertices(self):
        """Rotation and relative_vertices coexist non-destructively.

        add_polygon(rotation=...) stores rotation non-destructively.
        relative_vertices are preserved (no baking), and the SVG transform
        handles the visual rotation.
        """
        scene, cell = _scene_with_cell(100)
        tri_verts = [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)]
        unrotated = cell.add_polygon(tri_verts, fill="red", rotation=0)
        rotated = cell.add_polygon(tri_verts, fill="blue", rotation=45)

        # Rotation is stored non-destructively
        assert rotated.rotation == pytest.approx(45.0)
        assert unrotated.rotation == pytest.approx(0.0)

        # World-space bounds should differ due to rotation
        ub = unrotated.bounds()
        rb = rotated.bounds()
        u_size = (ub[2] - ub[0], ub[3] - ub[1])
        r_size = (rb[2] - rb[0], rb[3] - rb[1])
        assert abs(u_size[0] - r_size[0]) > 1.0 or abs(u_size[1] - r_size[1]) > 1.0, (
            "Rotated polygon bounds should differ from unrotated"
        )

    def test_is_resolved_not_set_by_rotation(self):
        """Non-destructive rotation does NOT resolve relative to absolute."""
        scene, cell = _scene_with_cell(100)
        tri_verts = [(0.3, 0.3), (0.7, 0.3), (0.5, 0.7)]

        plain = cell.add_polygon(tri_verts, fill="red")
        assert not plain.is_resolved
        assert plain.relative_vertices is not None

        rotated = cell.add_polygon(tri_verts, fill="blue", rotation=45)
        # Non-destructive: relative_vertices preserved, not resolved
        assert not rotated.is_resolved
        assert rotated.relative_vertices is not None
        assert rotated.rotation == pytest.approx(45.0)


# =========================================================================
# within= for add_text
# =========================================================================


class TestWithinText:
    def test_text_centered_within_rect(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        text = cell.add_text("A", within=rect, at="center", font_size=0.10, color="white")
        # center of rect = (50, 50)
        assert abs(text.x - 50.0) < 0.01
        assert abs(text.y - 50.0) < 0.01


# =========================================================================
# Multi-pass: .at property read/write
# =========================================================================


class TestMultiPass:
    def test_read_at_after_add_dot(self):
        scene, cell = _scene_with_cell(100)
        dot = cell.add_dot(at=(0.25, 0.75), color="red")
        assert dot.at == RelCoord(0.25, 0.75)

    def test_write_at_updates_position(self):
        scene, cell = _scene_with_cell(100)
        dot = cell.add_dot(at="center", color="red")
        assert abs(dot.x - 50.0) < 0.01
        # Modify relative position
        dot.at = (0.0, 0.0)
        assert abs(dot.x - 0.0) < 0.01
        assert abs(dot.y - 0.0) < 0.01

    def test_write_at_shift_all_entities(self):
        scene, cell = _scene_with_cell(100)
        dots = [cell.add_dot(at=(i * 0.1, 0.5), color="red") for i in range(10)]
        # Shift all dots right by 5%
        for dot in dots:
            assert dot.at is not None
            rx, ry = dot.at
            dot.at = (rx + 0.05, ry)
        # First dot: was at (0.0, 0.5), now at (0.05, 0.5) → x = 5.0
        assert abs(dots[0].x - 5.0) < 0.01
        # Last dot: was at (0.9, 0.5), now at (0.95, 0.5) → x = 95.0
        assert abs(dots[9].x - 95.0) < 0.01

    def test_at_is_none_for_absolute_mode(self):
        scene, cell = _scene_with_cell(100)
        from pyfreeform import Dot

        dot = Dot(10, 20, color="red")
        assert dot.at is None


# =========================================================================
# Reactive: entities follow reference movement
# =========================================================================


class TestReactive:
    def test_along_follows_path_movement(self):
        scene, cell = _scene_with_cell(100)
        line = cell.add_line(start="left", end="right", color="gray")
        dot = cell.add_dot(along=line, t=0.5, color="red")
        # Midpoint of line: left=(0,50), right=(100,50) → mid=(50,50)
        assert abs(dot.x - 50.0) < 0.01
        # Move line down by setting both endpoints
        new_start = Coord(line.start.x, line.start.y + 20)
        new_end = Coord(line.end.x, line.end.y + 20)
        line.set_endpoints(new_start, new_end)
        # Dot should follow (it re-resolves along path)
        assert abs(dot.y - 70.0) < 0.01

    def test_within_follows_reference_movement(self):
        scene, cell = _scene_with_cell(100)
        rect = cell.add_rect(fill="blue", width=0.5, height=0.5)
        dot = cell.add_dot(within=rect, at="center", color="red")
        assert abs(dot.x - 50.0) < 0.01
        # Move rect
        rect.position = Coord(rect.x + 20, rect.y)
        # Dot should follow (resolves against rect's new bounds)
        assert abs(dot.x - 70.0) < 0.01


# =========================================================================
# Circular reference detection
# =========================================================================


class TestCircularReference:
    def test_circular_reference_raises(self):
        scene, cell = _scene_with_cell(100)
        dot_a = cell.add_dot(at="center", color="red")
        dot_b = cell.add_dot(at="center", color="blue")
        # Create circular reference
        dot_a.binding = Binding(at=RelCoord(0.5, 0.5), reference=dot_b)
        dot_b.binding = Binding(at=RelCoord(0.5, 0.5), reference=dot_a)
        with pytest.raises(ValueError, match="Circular"):
            _ = dot_a.x


# =========================================================================
# Mode switching
# =========================================================================


class TestModeSwitching:
    def test_position_setter_clears_relative(self):
        scene, cell = _scene_with_cell(100)
        dot = cell.add_dot(at=(0.25, 0.75), color="red")
        assert dot.at is not None
        # Set pixel position
        dot.position = (10, 10)
        assert dot.at is None
        assert abs(dot.x - 10.0) < 0.01

    def test_position_coord_clears_relative(self):
        scene, cell = _scene_with_cell(100)
        dot = cell.add_dot(at=(0.25, 0.75), color="red")
        assert dot.at is not None
        dot.position = Coord(10, 10)
        assert dot.at is None
