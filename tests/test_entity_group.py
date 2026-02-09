"""Tests for EntityGroup, particularly rotation support."""

import math
import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene
from pyfreeform.entities.entity_group import EntityGroup
from pyfreeform.entities.dot import Dot
from pyfreeform.entities.line import Line


def test_group_rotate_accumulates():
    """rotate() should accumulate internal rotation angle."""
    group = EntityGroup()
    group.add(Dot(0, 0, radius=5, color="red"))

    group.rotate(30)
    assert group._rotation == 30

    group.rotate(15)
    assert group._rotation == 45


def test_group_rotate_no_origin_no_position_change():
    """rotate() without origin should not change position."""
    group = EntityGroup(x=100, y=200)
    group.add(Dot(0, 0, radius=5, color="red"))

    group.rotate(90)

    assert group.x == 100
    assert group.y == 200
    assert group._rotation == 90


def test_group_rotate_with_origin_orbits_position():
    """rotate() with origin should orbit position around that point."""
    group = EntityGroup(x=100, y=0)
    group.add(Dot(0, 0, radius=5, color="red"))

    # Rotate 90 degrees around the origin (0, 0)
    group.rotate(90, origin=(0, 0))

    assert group._rotation == 90
    # (100, 0) rotated 90° CCW around (0,0) → (0, 100)
    assert abs(group.x - 0) < 0.01
    assert abs(group.y - 100) < 0.01


def test_group_rotate_svg_transform():
    """to_svg() should include rotate() in the transform."""
    group = EntityGroup(x=50, y=60)
    group.add(Dot(0, 0, radius=5, color="red"))

    group.rotate(45)
    svg = group.to_svg()

    assert "rotate(45" in svg
    assert "translate(50, 60)" in svg


def test_group_rotate_zero_no_transform():
    """rotation=0 should not emit rotate() in SVG."""
    group = EntityGroup(x=10, y=20)
    group.add(Dot(0, 0, radius=5, color="red"))

    svg = group.to_svg()

    assert "rotate" not in svg


def test_group_rotate_and_scale_svg_order():
    """SVG transform order should be translate, rotate, scale."""
    group = EntityGroup(x=10, y=20)
    group.add(Dot(0, 0, radius=5, color="red"))

    group.rotate(30)
    group.scale(2.0)

    svg = group.to_svg()
    # Verify order: translate before rotate before scale
    translate_pos = svg.index("translate(")
    rotate_pos = svg.index("rotate(")
    scale_pos = svg.index("scale(")
    assert translate_pos < rotate_pos < scale_pos


def test_group_rotate_bounds_90():
    """Bounds of a rotated group should reflect the rotation."""
    group = EntityGroup()
    # A horizontal line from (-50, -5) to (50, 5) — 100x10 bounding box
    group.add(Line(-50, 0, 50, 0, width=10, color="black"))

    unrotated = group.bounds()
    unrotated_w = unrotated[2] - unrotated[0]
    unrotated_h = unrotated[3] - unrotated[1]

    group.rotate(90)
    rotated = group.bounds()
    rotated_w = rotated[2] - rotated[0]
    rotated_h = rotated[3] - rotated[1]

    # After 90° rotation, width and height should approximately swap
    assert abs(rotated_w - unrotated_h) < 1.0
    assert abs(rotated_h - unrotated_w) < 1.0


def test_group_rotate_bounds_45():
    """45° rotation should make bounds larger (diagonal)."""
    group = EntityGroup()
    group.add(Line(-50, -5, 50, 5, width=1, color="black"))

    unrotated = group.bounds()
    unrotated_w = unrotated[2] - unrotated[0]
    unrotated_h = unrotated[3] - unrotated[1]

    group.rotate(45)
    rotated = group.bounds()
    rotated_w = rotated[2] - rotated[0]
    rotated_h = rotated[3] - rotated[1]

    # 45° rotation of a wide rectangle should make it more square-ish
    # and the AABB should be larger than the original width
    assert rotated_w > unrotated_h  # wider than original height
    assert rotated_h > unrotated_h  # taller than original height


def test_group_fit_to_cell_after_rotate():
    """fit_to_cell should work correctly on a rotated group."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    group = EntityGroup()
    group.add(Dot(0, 0, radius=50, color="red"))
    group.add(Line(-40, 0, 40, 0, width=3, color="blue"))

    cell.place(group)
    group.rotate(45)
    group.fit_to_cell(0.8)

    # Bounds should fit within cell
    min_x, min_y, max_x, max_y = group.bounds()
    assert min_x >= cell.x - 1.0
    assert min_y >= cell.y - 1.0
    assert max_x <= cell.x + cell.width + 1.0
    assert max_y <= cell.y + cell.height + 1.0


def test_group_rotate_then_fit_then_rotate():
    """Multiple rotations interleaved with fit should accumulate correctly."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    group = EntityGroup()
    group.add(Dot(0, 0, radius=30, color="red"))

    cell.place(group)
    group.rotate(30)
    group.fit_to_cell(0.8)
    group.rotate(15)

    assert group._rotation == 45


def test_group_rotate_method_chaining():
    """rotate() should return self for method chaining."""
    group = EntityGroup()
    group.add(Dot(0, 0, radius=5, color="red"))

    result = group.rotate(45)
    assert result is group
