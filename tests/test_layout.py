"""Tests for layout utilities and relative anchor/bounds primitives."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, Dot, RelCoord
from pyfreeform.layout import between, align, distribute, stack


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _scene_with_cell(cell_size=100):
    """Create a 1x1 scene for simple layout tests."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=cell_size)
    return scene, scene.grid[0][0]


def _merged_cell(cols=4, rows=1, cell_size=100):
    """Create a merged cell spanning the full grid."""
    scene = Scene.with_grid(cols=cols, rows=rows, cell_size=cell_size)
    cell = scene.grid.merge()
    return scene, cell


# ---------------------------------------------------------------------------
# TestRelativeAnchor
# ---------------------------------------------------------------------------

class TestRelativeAnchor:
    def test_rect_center(self):
        """Rect at center has relative_anchor('center') ≈ (0.5, 0.5)."""
        _, cell = _scene_with_cell()
        rect = cell.add_rect(at=(0.5, 0.5), width=0.6, height=0.4, fill="blue")
        ra = rect.relative_anchor("center")
        assert abs(ra.rx - 0.5) < 0.01
        assert abs(ra.ry - 0.5) < 0.01

    def test_rect_bottom(self):
        """Rect bottom anchor is at center_x + half height below."""
        _, cell = _scene_with_cell()
        rect = cell.add_rect(at=(0.5, 0.3), width=0.6, height=0.4, fill="blue")
        ra = rect.relative_anchor("bottom")
        assert abs(ra.rx - 0.5) < 0.01
        assert abs(ra.ry - 0.5) < 0.01  # 0.3 + 0.4/2 = 0.5

    def test_dot_center(self):
        """Dot center matches its at position."""
        _, cell = _scene_with_cell()
        dot = cell.add_dot(at=(0.25, 0.75), color="red")
        ra = dot.relative_anchor("center")
        assert abs(ra.rx - 0.25) < 0.01
        assert abs(ra.ry - 0.75) < 0.01

    def test_requires_surface(self):
        """relative_anchor raises when entity has no surface."""
        dot = Dot(50, 50, radius=5, color="red")
        with pytest.raises(ValueError, match="must be in a surface"):
            dot.relative_anchor("center")

    def test_surface_relative_anchor(self):
        """Surface relative_anchor returns named position as RelCoord."""
        _, cell = _scene_with_cell()
        ra = cell.relative_anchor("bottom")
        assert ra == RelCoord(0.5, 1.0)

    def test_surface_relative_anchor_center(self):
        """Surface center is (0.5, 0.5)."""
        _, cell = _scene_with_cell()
        ra = cell.relative_anchor("center")
        assert ra == RelCoord(0.5, 0.5)


# ---------------------------------------------------------------------------
# TestRelativeBounds
# ---------------------------------------------------------------------------

class TestRelativeBounds:
    def test_rect_bounds(self):
        """Rect relative bounds match expected fractions."""
        _, cell = _scene_with_cell()
        rect = cell.add_rect(at=(0.5, 0.5), width=0.6, height=0.4, fill="blue")
        rb = rect.relative_bounds()
        # width=0.6 → min_rx=0.2, max_rx=0.8
        # height=0.4 → min_ry=0.3, max_ry=0.7
        assert abs(rb[0] - 0.2) < 0.01
        assert abs(rb[1] - 0.3) < 0.01
        assert abs(rb[2] - 0.8) < 0.01
        assert abs(rb[3] - 0.7) < 0.01

    def test_requires_surface(self):
        """relative_bounds raises when entity has no surface."""
        dot = Dot(50, 50, radius=5, color="red")
        with pytest.raises(ValueError, match="must be in a surface"):
            dot.relative_bounds()

    def test_dot_bounds(self):
        """Dot relative bounds are symmetric around center."""
        _, cell = _scene_with_cell(cell_size=100)
        dot = cell.add_dot(at=(0.5, 0.5), radius=0.1, color="red")
        rb = dot.relative_bounds()
        # radius=0.1 of min(100,100) = 10px → 0.1 of each axis
        assert abs(rb[0] - 0.4) < 0.01
        assert abs(rb[1] - 0.4) < 0.01
        assert abs(rb[2] - 0.6) < 0.01
        assert abs(rb[3] - 0.6) < 0.01


# ---------------------------------------------------------------------------
# TestBetween
# ---------------------------------------------------------------------------

class TestBetween:
    def test_midpoint_of_two_entities(self):
        """between two dots returns midpoint of their at positions."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.2, 0.3), color="red")
        d2 = cell.add_dot(at=(0.8, 0.7), color="blue")
        mid = between(d1, d2)
        assert abs(mid.rx - 0.5) < 0.01
        assert abs(mid.ry - 0.5) < 0.01

    def test_entity_and_surface(self):
        """between entity and surface anchor."""
        _, cell = _scene_with_cell()
        shape = cell.add_rect(at=(0.5, 0.3), width=0.6, height=0.4, fill="blue")
        mid = between(shape, cell, anchor="bottom")
        # shape bottom ≈ 0.5, cell bottom = 1.0, midpoint ≈ 0.75
        assert abs(mid.rx - 0.5) < 0.01
        assert abs(mid.ry - 0.75) < 0.01

    def test_relcoord_pairs(self):
        """between two RelCoords."""
        mid = between(RelCoord(0.0, 0.0), RelCoord(1.0, 1.0))
        assert abs(mid.rx - 0.5) < 0.01
        assert abs(mid.ry - 0.5) < 0.01

    def test_tuple_pairs(self):
        """between two tuples."""
        mid = between((0.2, 0.4), (0.6, 0.8))
        assert abs(mid.rx - 0.4) < 0.01
        assert abs(mid.ry - 0.6) < 0.01

    def test_custom_t(self):
        """Custom t value for asymmetric interpolation."""
        pt = between((0.0, 0.0), (1.0, 1.0), t=0.25)
        assert abs(pt.rx - 0.25) < 0.01
        assert abs(pt.ry - 0.25) < 0.01

    def test_returns_relcoord(self):
        """Result is a RelCoord, usable with at=."""
        mid = between((0.2, 0.3), (0.8, 0.7))
        assert isinstance(mid, RelCoord)


# ---------------------------------------------------------------------------
# TestAlign
# ---------------------------------------------------------------------------

class TestAlign:
    def test_center_y(self):
        """Align by center_y gives all dots the same at.ry."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.2, 0.3), color="red")
        d2 = cell.add_dot(at=(0.5, 0.7), color="blue")
        d3 = cell.add_dot(at=(0.8, 0.1), color="green")
        align(d1, d2, d3, anchor="center_y")
        assert abs(d1.at.ry - 0.3) < 0.01  # reference stays
        assert abs(d2.at.ry - 0.3) < 0.01
        assert abs(d3.at.ry - 0.3) < 0.01
        # x positions preserved
        assert abs(d2.at.rx - 0.5) < 0.01
        assert abs(d3.at.rx - 0.8) < 0.01

    def test_center_x(self):
        """Align by center_x gives all dots the same at.rx."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.3, 0.2), color="red")
        d2 = cell.add_dot(at=(0.7, 0.5), color="blue")
        align(d1, d2, anchor="center_x")
        assert abs(d2.at.rx - 0.3) < 0.01
        assert abs(d2.at.ry - 0.5) < 0.01  # y preserved

    def test_edge_top(self):
        """Align by top edge using relative_bounds."""
        _, cell = _scene_with_cell()
        r1 = cell.add_rect(at=(0.3, 0.3), width=0.2, height=0.2, fill="red")
        r2 = cell.add_rect(at=(0.7, 0.6), width=0.2, height=0.2, fill="blue")
        align(r1, r2, anchor="top")
        # After alignment, both should have same top edge
        rb1 = r1.relative_bounds()
        rb2 = r2.relative_bounds()
        assert abs(rb1[1] - rb2[1]) < 0.01

    def test_edge_left(self):
        """Align by left edge."""
        _, cell = _scene_with_cell()
        r1 = cell.add_rect(at=(0.3, 0.3), width=0.2, height=0.2, fill="red")
        r2 = cell.add_rect(at=(0.7, 0.7), width=0.4, height=0.2, fill="blue")
        align(r1, r2, anchor="left")
        rb1 = r1.relative_bounds()
        rb2 = r2.relative_bounds()
        assert abs(rb1[0] - rb2[0]) < 0.01

    def test_list_form(self):
        """Accept a single list of entities."""
        _, cell = _scene_with_cell()
        dots = [cell.add_dot(at=(i * 0.3, i * 0.2), color="red") for i in range(3)]
        result = align(dots, anchor="center_y")
        assert len(result) == 3

    def test_fewer_than_two_raises(self):
        """Fewer than 2 entities raises ValueError."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        with pytest.raises(ValueError, match="at least 2"):
            align(d1)

    def test_non_entity_raises(self):
        """Non-Entity argument raises TypeError."""
        with pytest.raises(TypeError, match="Expected Entity"):
            align("not an entity", "also not")

    def test_invalid_anchor_raises(self):
        """Invalid anchor raises ValueError."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.2, 0.3), color="red")
        d2 = cell.add_dot(at=(0.5, 0.7), color="blue")
        with pytest.raises(ValueError, match="Invalid anchor"):
            align(d1, d2, anchor="diagonal")


# ---------------------------------------------------------------------------
# TestDistribute
# ---------------------------------------------------------------------------

class TestDistribute:
    def test_even_spacing_x(self):
        """Distribute 3 dots evenly along x."""
        _, cell = _merged_cell(cols=4)
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        d2 = cell.add_dot(at=(0.5, 0.5), color="blue")
        d3 = cell.add_dot(at=(0.5, 0.5), color="green")
        distribute(d1, d2, d3, axis="x")
        assert abs(d1.at.rx - 0.0) < 0.01
        assert abs(d2.at.rx - 0.5) < 0.01
        assert abs(d3.at.rx - 1.0) < 0.01

    def test_custom_range(self):
        """Distribute with custom start/end."""
        _, cell = _merged_cell(cols=4)
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        d2 = cell.add_dot(at=(0.5, 0.5), color="blue")
        d3 = cell.add_dot(at=(0.5, 0.5), color="green")
        distribute(d1, d2, d3, axis="x", start=0.1, end=0.9)
        assert abs(d1.at.rx - 0.1) < 0.01
        assert abs(d2.at.rx - 0.5) < 0.01
        assert abs(d3.at.rx - 0.9) < 0.01

    def test_preserves_cross_axis(self):
        """Cross-axis at value is preserved."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.5, 0.2), color="red")
        d2 = cell.add_dot(at=(0.5, 0.8), color="blue")
        distribute(d1, d2, axis="x", start=0.1, end=0.9)
        assert abs(d1.at.ry - 0.2) < 0.01
        assert abs(d2.at.ry - 0.8) < 0.01

    def test_y_axis(self):
        """Distribute along y axis."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.3, 0.5), color="red")
        d2 = cell.add_dot(at=(0.7, 0.5), color="blue")
        distribute(d1, d2, axis="y", start=0.2, end=0.8)
        assert abs(d1.at.ry - 0.2) < 0.01
        assert abs(d2.at.ry - 0.8) < 0.01
        # x values preserved
        assert abs(d1.at.rx - 0.3) < 0.01
        assert abs(d2.at.rx - 0.7) < 0.01

    def test_invalid_axis_raises(self):
        """Invalid axis raises ValueError."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        d2 = cell.add_dot(at=(0.5, 0.5), color="blue")
        with pytest.raises(ValueError, match="axis must be"):
            distribute(d1, d2, axis="z")

    def test_preserves_order(self):
        """Distribute preserves argument order."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.9, 0.5), color="red")
        d2 = cell.add_dot(at=(0.1, 0.5), color="blue")
        result = distribute(d1, d2, axis="x")
        # d1 comes first → gets start position
        assert abs(d1.at.rx - 0.0) < 0.01
        assert abs(d2.at.rx - 1.0) < 0.01
        assert result[0] is d1


# ---------------------------------------------------------------------------
# TestStack
# ---------------------------------------------------------------------------

class TestStack:
    def test_stack_below(self):
        """Stack rects vertically with gap."""
        _, cell = _scene_with_cell(cell_size=200)
        r1 = cell.add_rect(at=(0.5, 0.2), width=0.3, height=0.2, fill="red")
        r2 = cell.add_rect(at=(0.5, 0.5), width=0.3, height=0.2, fill="blue")
        stack(r1, r2, direction="below", gap=0.05)
        # r1 stays at center (0.5, 0.2), bottom edge at 0.3
        # r2 center: 0.3 + 0.05 + 0.1 = 0.45
        r1c = r1.relative_anchor("center")
        r2c = r2.relative_anchor("center")
        assert abs(r1c.ry - 0.2) < 0.01  # r1 doesn't move
        assert abs(r2c.ry - 0.45) < 0.02

    def test_stack_right(self):
        """Stack rects horizontally."""
        _, cell = _scene_with_cell(cell_size=200)
        r1 = cell.add_rect(at=(0.2, 0.5), width=0.2, height=0.3, fill="red")
        r2 = cell.add_rect(at=(0.5, 0.5), width=0.2, height=0.3, fill="blue")
        stack(r1, r2, direction="right", gap=0.05)
        # r1 stays at center (0.2, 0.5), right edge at 0.3
        # r2 center: 0.3 + 0.05 + 0.1 = 0.45
        r1c = r1.relative_anchor("center")
        r2c = r2.relative_anchor("center")
        assert abs(r1c.rx - 0.2) < 0.01
        assert abs(r2c.rx - 0.45) < 0.02

    def test_stack_preserves_order(self):
        """Stack preserves argument order."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        d2 = cell.add_dot(at=(0.5, 0.5), color="blue")
        result = stack(d1, d2, direction="right")
        assert result[0] is d1
        assert result[1] is d2

    def test_invalid_direction_raises(self):
        """Invalid direction raises ValueError."""
        _, cell = _scene_with_cell()
        d1 = cell.add_dot(at=(0.5, 0.5), color="red")
        d2 = cell.add_dot(at=(0.5, 0.5), color="blue")
        with pytest.raises(ValueError, match="Invalid direction"):
            stack(d1, d2, direction="diagonal")

    def test_three_entities(self):
        """Stack 3 entities sequentially."""
        _, cell = _scene_with_cell(cell_size=200)
        r1 = cell.add_rect(at=(0.5, 0.15), width=0.3, height=0.1, fill="red")
        r2 = cell.add_rect(at=(0.5, 0.5), width=0.3, height=0.1, fill="blue")
        r3 = cell.add_rect(at=(0.5, 0.5), width=0.3, height=0.1, fill="green")
        stack(r1, r2, r3, direction="below", gap=0.05)
        # Each rect is 0.1 high, gap is 0.05
        # r1: center=0.15, bottom=0.2
        # r2: top=0.2+0.05=0.25, center=0.3
        # r3: top=0.35+0.05=0.4, center=0.45
        assert r1.at.ry < r2.at.ry < r3.at.ry
