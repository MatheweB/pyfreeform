"""Tests for EntityGroup: rotation and opacity support."""

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

    cell.add(group)
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

    cell.add(group)
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


# =========================================================================
# Opacity tests
# =========================================================================


def test_group_opacity_default():
    """Default opacity is 1.0 and not emitted in SVG."""
    group = EntityGroup()
    group.add(Dot(0, 0, radius=5, color="red"))

    assert group.opacity == 1.0
    assert "opacity" not in group.to_svg()


def test_group_opacity_in_svg():
    """Non-default opacity should appear on the <g> element."""
    group = EntityGroup(opacity=0.5)
    group.add(Dot(0, 0, radius=5, color="red"))

    svg = group.to_svg()
    assert 'opacity="0.5"' in svg


def test_group_opacity_settable():
    """opacity should be settable after construction."""
    group = EntityGroup()
    group.add(Dot(0, 0, radius=5, color="red"))

    group.opacity = 0.3
    assert 'opacity="0.3"' in group.to_svg()


# =========================================================================
# Rotational fitting tests
# =========================================================================


def test_fit_to_cell_rotate_default_false():
    """rotate=False (default) should not change rotation."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    group = EntityGroup()
    group.add(Line(-50, 0, 50, 0, width=5, color="red"))
    cell.add(group)
    group.fit_to_cell(0.8)

    assert group._rotation == 0.0


def test_fit_to_cell_rotate_wide_in_tall():
    """A wide group in a tall cell should rotate for better fill."""
    scene = Scene.with_grid(cols=1, rows=1, cell_width=50, cell_height=200)
    cell = scene.grid[0, 0]

    # Wide group: 200px wide, 10px tall
    group = EntityGroup()
    group.add(Line(-100, 0, 100, 0, width=10, color="red"))
    cell.add(group)

    # Measure unrotated scale factor
    unrotated_w = 200  # line length
    unrotated_factor = min(50 / unrotated_w, 200 / 10)

    group.fit_to_cell(1.0, rotate=True)

    # Should have rotated significantly (>45°) to better use the tall cell.
    # The optimal angle is ~78° (balanced angle), NOT 90°, because the
    # closed-form solution finds where both dimensions are equally used.
    assert group._rotation > 45

    # Bounds should fit within cell
    min_x, min_y, max_x, max_y = group.bounds()
    assert min_x >= cell.x - 1.0
    assert min_y >= cell.y - 1.0
    assert max_x <= cell.x + cell.width + 1.0
    assert max_y <= cell.y + cell.height + 1.0

    # Scale factor should be much better than unrotated (0.25)
    assert group._scale > unrotated_factor


def test_fit_to_cell_rotate_square_noop():
    """Square bbox in square cell — rotation shouldn't change much."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    # Square group: equal width and height
    group = EntityGroup()
    group.add(Dot(0, 0, radius=40, color="red"))
    cell.add(group)

    group.fit_to_cell(0.9, rotate=True)

    # Should pick 0° (or equivalent) since bbox is already square
    assert group._rotation % 90 == pytest.approx(0, abs=1.0)


def test_fit_to_cell_rotate_with_at():
    """rotate=True should work with at= position-aware mode."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    group = EntityGroup()
    group.add(Line(-50, -5, 50, 5, width=10, color="red"))
    cell.add(group)

    group.fit_to_cell(0.5, at=(0.5, 0.5), rotate=True)

    # Bounds should stay within cell
    min_x, min_y, max_x, max_y = group.bounds()
    assert min_x >= cell.x - 1.0
    assert min_y >= cell.y - 1.0
    assert max_x <= cell.x + cell.width + 1.0
    assert max_y <= cell.y + cell.height + 1.0


def test_fit_within_rotate():
    """rotate=True should work with fit_within."""
    from pyfreeform.entities.rect import Rect

    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    cell = scene.grid[0, 0]

    # Tall target rect
    rect = Rect(20, 20, 40, 160, fill="blue")
    scene.place(rect)

    # Wide group
    group = EntityGroup()
    group.add(Line(-60, -5, 60, 5, width=10, color="red"))
    scene.place(group)

    group.fit_within(rect, rotate=True)

    # Should have rotated to fit the tall rectangle
    min_x, min_y, max_x, max_y = group.bounds()
    r_min_x, r_min_y, r_max_x, r_max_y = rect.bounds()
    assert min_x >= r_min_x - 1.0
    assert min_y >= r_min_y - 1.0
    assert max_x <= r_max_x + 1.0
    assert max_y <= r_max_y + 1.0


def test_fit_to_cell_rotate_works_on_polygon():
    """rotate=True should work on Polygon (bakes into vertices)."""
    from pyfreeform.entities.polygon import Polygon

    scene = Scene.with_grid(cols=1, rows=1, cell_width=50, cell_height=200)
    cell = scene.grid[0, 0]

    # Wide diamond
    poly = cell.add_polygon(
        Polygon.diamond(size=0.8),
        fill="blue",
    )
    poly.fit_to_cell(0.9, rotate=True)

    # Bounds should fit within cell
    min_x, min_y, max_x, max_y = poly.bounds()
    assert min_x >= cell.x - 1.0
    assert max_x <= cell.x + cell.width + 1.0
    assert min_y >= cell.y - 1.0
    assert max_y <= cell.y + cell.height + 1.0


def test_fit_to_cell_rotate_works_on_rect():
    """rotate=True should work on Rect (sets self.rotation)."""
    from pyfreeform.entities.rect import Rect

    scene = Scene.with_grid(cols=1, rows=1, cell_width=50, cell_height=200)
    cell = scene.grid[0, 0]

    rect = cell.add_rect(width=0.9, height=0.1, fill="blue")
    rect.fit_to_cell(0.9, rotate=True)

    # Wide rect in tall cell should have rotated
    assert rect.rotation != 0.0


def test_fit_to_cell_rotate_dot_noop():
    """rotate=True on Dot should work (no-op, circle is symmetric)."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    dot = cell.add_dot(radius=0.3, color="red")
    # Should not raise — Dot is symmetric, rotation is a no-op
    dot.fit_to_cell(0.8, rotate=True)


def test_fit_within_rotate_works_on_non_group():
    """rotate=True should work on non-EntityGroup in fit_within."""
    from pyfreeform.entities.rect import Rect

    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    dot = cell.add_dot(radius=0.3, color="red")
    target = Rect(0, 0, 50, 50, fill="blue")
    scene.place(target)

    # Should not raise
    dot.fit_within(target, rotate=True)


# =========================================================================
# match_aspect tests
# =========================================================================


def test_fit_to_cell_match_aspect_square_cell():
    """match_aspect=True in square cell with wide entity."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    cell = scene.grid[0, 0]

    # Wide group (200 x 10)
    group = EntityGroup()
    group.add(Line(-100, 0, 100, 0, width=10, color="red"))
    cell.add(group)

    group.fit_to_cell(0.9, match_aspect=True)

    # After matching aspect to square cell, bounds should be roughly square
    min_x, min_y, max_x, max_y = group.bounds()
    w = max_x - min_x
    h = max_y - min_y
    if w > 1e-3 and h > 1e-3:
        ratio = w / h
        assert 0.5 < ratio < 2.0  # roughly square-ish


def test_fit_to_cell_match_aspect_tall_cell():
    """match_aspect=True in tall cell with wide entity."""
    scene = Scene.with_grid(cols=1, rows=1, cell_width=100, cell_height=300)
    cell = scene.grid[0, 0]

    # Wide group
    group = EntityGroup()
    group.add(Line(-80, 0, 80, 0, width=8, color="red"))
    cell.add(group)

    group.fit_to_cell(0.9, match_aspect=True)

    # Bounds should fit within cell
    min_x, min_y, max_x, max_y = group.bounds()
    assert min_x >= cell.x - 1.0
    assert max_x <= cell.x + cell.width + 1.0


def test_fit_to_cell_rotate_and_match_aspect_exclusive():
    """rotate=True and match_aspect=True together should raise ValueError."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]

    group = EntityGroup()
    group.add(Dot(0, 0, radius=10, color="red"))
    cell.add(group)

    with pytest.raises(ValueError, match="mutually exclusive"):
        group.fit_to_cell(0.9, rotate=True, match_aspect=True)


def test_fit_within_match_aspect():
    """match_aspect=True should work with fit_within."""
    from pyfreeform.entities.rect import Rect

    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    cell = scene.grid[0, 0]

    # Square target
    target = Rect(20, 20, 100, 100, fill="blue")
    scene.place(target)

    # Wide group
    group = EntityGroup()
    group.add(Line(-60, -5, 60, 5, width=10, color="red"))
    scene.place(group)

    group.fit_within(target, match_aspect=True)

    # Should fit within target bounds
    min_x, min_y, max_x, max_y = group.bounds()
    t_min_x, t_min_y, t_max_x, t_max_y = target.bounds()
    assert min_x >= t_min_x - 2.0
    assert max_x <= t_max_x + 2.0


def test_entity_group_rotation_property():
    """EntityGroup.rotation should expose _rotation."""
    group = EntityGroup()
    assert group.rotation == 0.0
    group.rotate(45)
    assert group.rotation == pytest.approx(45.0)
