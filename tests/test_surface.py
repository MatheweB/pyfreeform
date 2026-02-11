"""Tests for the Surface protocol — Scene builders, CellGroup, grid.merge()."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import Scene, CellGroup, Surface, Text


# =========================================================================
# Surface inheritance
# =========================================================================


def test_cell_is_surface():
    scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
    assert isinstance(scene.grid[0, 0], Surface)


def test_scene_is_surface():
    scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
    assert isinstance(scene, Surface)


def test_cell_group_is_surface():
    scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    assert isinstance(group, Surface)


# =========================================================================
# Scene builder methods
# =========================================================================


def test_scene_add_dot():
    scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
    dot = scene.add_dot(at="center", color="red")
    assert dot is not None
    assert dot.x == scene.width / 2
    assert dot.y == scene.height / 2


def test_scene_add_line():
    scene = Scene.with_grid(cols=3, rows=3, cell_size=10)
    line = scene.add_line(start="top_left", end="bottom_right", color="blue")
    assert line is not None
    assert line.start.x == 0.0
    assert line.start.y == 0.0
    assert line.end.x == scene.width
    assert line.end.y == scene.height


def test_scene_add_curve():
    scene = Scene(200, 100)
    curve = scene.add_curve(start="left", end="right", curvature=0.5, color="green")
    assert curve is not None
    assert curve.start.x == 0.0
    assert curve.start.y == 50.0  # left = (0, 0.5) * height


def test_scene_add_text():
    scene = Scene(200, 100)
    text = scene.add_text("Hello", at="center", font_size=0.20, color="white")
    assert text is not None
    assert text.content == "Hello"
    assert text.x == 100.0
    assert text.y == 50.0


def test_scene_add_fill():
    scene = Scene(100, 100, background="#000")
    fill = scene.add_fill(color="red")
    assert fill is not None
    # Fill should be a Rect covering the full scene
    assert fill.width == 100
    assert fill.height == 100


def test_scene_add_rect():
    scene = Scene(200, 200)
    rect = scene.add_rect(at="center", width=0.25, height=0.15, fill="blue")
    assert rect is not None
    assert rect.width == pytest.approx(50)
    assert rect.height == pytest.approx(30)


def test_scene_entities_in_svg():
    """Scene builder entities should appear in rendered SVG."""
    scene = Scene(100, 100)
    scene.add_dot(at="center", color="red", radius=0.05)
    svg = scene.to_svg()
    assert "<circle" in svg
    assert 'fill="red"' in svg


def test_scene_along_and_t():
    """along= and t= should work at scene level."""
    scene = Scene(200, 100)
    curve = scene.add_curve(start="left", end="right", curvature=0.3, color="gray")
    dot = scene.add_dot(along=curve, t=0.5, color="red")
    # Dot should be roughly in the middle area
    assert 50 < dot.x < 150


# =========================================================================
# CellGroup basics
# =========================================================================


def test_merge_returns_cell_group():
    scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 2))
    assert isinstance(group, CellGroup)


def test_merge_bounds():
    """Merged group should span the correct pixel region."""
    scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
    group = scene.grid.merge((1, 1), (2, 3))
    # cells at col=1..3, row=1..2 → x from 10 to 40, y from 10 to 30
    assert group.x == 10.0
    assert group.y == 10.0
    assert group.width == 30.0  # 3 cols * 10
    assert group.height == 20.0  # 2 rows * 10


def test_merge_row():
    scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
    row_group = scene.grid.merge_row(2)
    assert row_group.width == 50.0  # Full row width
    assert row_group.height == 10.0  # Single row height
    assert row_group.y == 20.0  # Row 2 starts at y=20


def test_merge_col():
    scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
    col_group = scene.grid.merge_col(3)
    assert col_group.width == 10.0  # Single column width
    assert col_group.height == 50.0  # Full column height
    assert col_group.x == 30.0  # Col 3 starts at x=30


def test_merge_empty_region_raises():
    scene = Scene.with_grid(cols=5, rows=5, cell_size=10)
    with pytest.raises(ValueError):
        # end row < start row → no cells
        scene.grid.merge((3, 0), (2, 4))


def test_cell_group_cells():
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    assert len(group.cells) == 4  # 2x2 grid


def test_cell_group_averaged_brightness():
    """CellGroup.brightness should average constituent cells."""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=10)
    # Set brightness on cells manually
    scene.grid[0, 0].data["brightness"] = 0.2
    scene.grid[0, 1].data["brightness"] = 0.8
    group = scene.grid.merge((0, 0), (0, 1))
    assert abs(group.brightness - 0.5) < 0.01


def test_cell_group_averaged_color():
    """CellGroup.color should average constituent cells' RGB."""
    scene = Scene.with_grid(cols=2, rows=1, cell_size=10)
    scene.grid[0, 0].data["color"] = "#ff0000"  # Red
    scene.grid[0, 1].data["color"] = "#0000ff"  # Blue
    group = scene.grid.merge((0, 0), (0, 1))
    # Average of (255,0,0) and (0,0,255) → (128, 0, 128) → #800080
    r, g, b = group.rgb
    assert r == 128
    assert g == 0
    assert b == 128


# =========================================================================
# CellGroup builder methods
# =========================================================================


def test_cell_group_add_dot():
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    dot = group.add_dot(at="center", color="red")
    # Center of a 20x20 region starting at (0,0) → (10, 10)
    assert dot.x == 10.0
    assert dot.y == 10.0


def test_cell_group_add_line():
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((1, 1), (2, 2))
    line = group.add_line(start="top_left", end="bottom_right", color="blue")
    assert line.start.x == 10.0  # group starts at (10, 10)
    assert line.start.y == 10.0
    assert line.end.x == 30.0
    assert line.end.y == 30.0


def test_cell_group_add_text():
    scene = Scene.with_grid(cols=6, rows=2, cell_size=10)
    group = scene.grid.merge_row(0)
    text = group.add_text("Title", at="center", font_size=0.50, color="white")
    assert text.x == 30.0  # center of 60-wide row
    assert text.y == 5.0  # center of 10-high row


def test_cell_group_add_fill():
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    fill = group.add_fill(color="navy")
    assert fill.width == 20.0
    assert fill.height == 20.0


# =========================================================================
# CellGroup entities render in scene SVG
# =========================================================================


def test_cell_group_entities_in_svg():
    """Entities added to a CellGroup should appear in the scene's SVG."""
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    group.add_dot(at="center", color="coral", radius=0.15)
    svg = scene.to_svg()
    assert "<circle" in svg
    assert 'fill="coral"' in svg


def test_cell_group_along_and_t():
    """along= and t= should work on CellGroup."""
    scene = Scene.with_grid(cols=10, rows=2, cell_size=10)
    group = scene.grid.merge_row(0)
    curve = group.add_curve(start="left", end="right", curvature=0.3, color="gray")
    dot = group.add_dot(along=curve, t=0.5, color="red")
    # Should be roughly in the middle of the 100-wide group
    assert 25 < dot.x < 75


# =========================================================================
# Grid.clear includes CellGroups
# =========================================================================


def test_grid_clear_clears_groups():
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    group.add_dot(color="red")
    assert len(scene.entities) > 0
    scene.grid.clear()
    assert len(scene.grid.all_entities()) == 0


# =========================================================================
# fit_to_cell works with CellGroup and Scene
# =========================================================================


def test_fit_to_cell_on_cell_group():
    """fit_to_cell should work for entities on a CellGroup."""
    scene = Scene.with_grid(cols=4, rows=4, cell_size=10)
    group = scene.grid.merge((0, 0), (1, 1))
    # 20x20 group, add a huge dot
    dot = group.add_dot(radius=5.0, color="red")
    dot.fit_to_cell(1.0)
    # Should be scaled to fit 20x20 → radius 10
    assert dot.radius <= 10.0 + 0.1
    assert dot.radius >= 9.9


def test_fit_to_cell_on_scene():
    """fit_to_cell should work for entities added directly to Scene."""
    scene = Scene(100, 100)
    dot = scene.add_dot(radius=2.0, color="red")
    dot.fit_to_cell(1.0)
    # Should be scaled to fit 100x100 → radius 50
    assert dot.radius <= 50.0 + 0.1
    assert dot.radius >= 49.9


# =========================================================================
# Text fit=True and fit_to_cell
# =========================================================================


def test_add_text_fit_shrinks_long_string():
    """fit=True should shrink font when text would overflow cell width."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=50)
    cell = scene.grid[0, 0]
    # Without fit: font_size=0.5 → 25px tall, but "ABCDEFGHIJ" is wide
    text_no_fit = cell.add_text("ABCDEFGHIJ", font_size=0.5, fit=False)
    text_fit = cell.add_text("ABCDEFGHIJ", font_size=0.5, fit=True)
    assert text_fit.font_size < text_no_fit.font_size


def test_add_text_fit_keeps_short_string():
    """fit=True should not upsize a short string that already fits."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=100)
    cell = scene.grid[0, 0]
    # "A" at font_size=0.2 → 20px, easily fits in 100px cell
    text_no_fit = cell.add_text("A", font_size=0.2, fit=False)
    text_fit = cell.add_text("A", font_size=0.2, fit=True)
    assert text_fit.font_size == text_no_fit.font_size


def test_text_fit_to_cell_scales_up():
    """fit_to_cell should scale text up to fill the cell."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=200)
    cell = scene.grid[0, 0]
    text = cell.add_text("A", font_size=0.1)  # 20px, small for 200px cell
    text.fit_to_cell(1.0)
    # Should be much larger now
    assert text.font_size > 20.0


def test_text_fit_to_cell_scales_down():
    """fit_to_cell should scale text down for long content."""
    scene = Scene.with_grid(cols=1, rows=1, cell_size=50)
    cell = scene.grid[0, 0]
    text = cell.add_text("ABCDEFGHIJKLMNOP", font_size=0.8)  # 40px, too wide
    text.fit_to_cell(1.0)
    # Should be smaller to fit
    assert text.font_size < 40.0


def test_text_fit_to_cell_no_cell_raises():
    """fit_to_cell should raise if text has no cell."""

    text = Text(0, 0, "Hello", font_size=16)
    try:
        text.fit_to_cell(1.0)
        raise AssertionError("Should have raised ValueError")
    except ValueError:
        pass
