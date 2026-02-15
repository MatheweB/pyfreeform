"""Tests for the cap registry and arrow cap support."""

import sys
from pathlib import Path

from pyfreeform.entities.point import Point

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform.config.caps import (
    get_marker,
    is_marker_cap,
    make_marker_id,
    register_cap,
)
from pyfreeform.config.styles import PathStyle
from pyfreeform.entities.curve import Curve
from pyfreeform.entities.line import Line
from pyfreeform import Scene


# ---- Cap registry tests ----


def test_is_marker_cap_arrow():
    assert is_marker_cap("arrow") is True


def test_is_marker_cap_native():
    assert is_marker_cap("round") is False
    assert is_marker_cap("square") is False
    assert is_marker_cap("butt") is False


def test_make_marker_id_deterministic():
    id1 = make_marker_id("arrow", "#ff0000", 6.0)
    id2 = make_marker_id("arrow", "#ff0000", 6.0)
    assert id1 == id2


def test_make_marker_id_varies_by_color():
    id1 = make_marker_id("arrow", "#ff0000", 6.0)
    id2 = make_marker_id("arrow", "#0000ff", 6.0)
    assert id1 != id2


def test_make_marker_id_varies_by_size():
    id1 = make_marker_id("arrow", "#ff0000", 6.0)
    id2 = make_marker_id("arrow", "#ff0000", 9.0)
    assert id1 != id2


def test_get_marker_arrow():
    result = get_marker("arrow", "#ff0000", 6.0)
    assert result is not None
    marker_id, marker_svg = result
    assert "marker" in marker_svg
    assert "#ff0000" in marker_svg
    assert marker_id in marker_svg


def test_get_marker_native_returns_none():
    assert get_marker("round", "#000000", 3.0) is None


def test_register_custom_cap():
    def _diamond(marker_id, color, size):
        return f'<marker id="{marker_id}"><polygon fill="{color}" /></marker>'

    register_cap("diamond", _diamond)
    assert is_marker_cap("diamond") is True
    result = get_marker("diamond", "red", 5.0)
    assert result is not None
    assert "red" in result[1]


# ---- Line arrow tests ----


def test_line_no_arrow_default():
    line = Line(0, 0, 100, 0)
    svg = line.to_svg()
    assert "marker-" not in svg
    assert 'stroke-linecap="round"' in svg


def test_line_end_cap_arrow():
    line = Line(0, 0, 100, 0, end_cap="arrow")
    svg = line.to_svg()
    assert "marker-end" in svg
    assert "marker-start" not in svg
    # Marker caps force "butt" linecap so round/square doesn't poke past the tip
    assert 'stroke-linecap="butt"' in svg


def test_line_start_cap_arrow():
    line = Line(0, 0, 100, 0, start_cap="arrow")
    svg = line.to_svg()
    assert "marker-start" in svg
    assert "marker-end" not in svg


def test_line_cap_arrow_both():
    line = Line(0, 0, 100, 0, cap="arrow")
    svg = line.to_svg()
    assert "marker-start" in svg
    assert "marker-end" in svg


def test_line_effective_caps():
    line = Line(0, 0, 100, 0, cap="round", end_cap="arrow")
    assert line.effective_start_cap == "round"
    assert line.effective_end_cap == "arrow"


def test_line_required_markers():
    line = Line(0, 0, 100, 0, end_cap="arrow", width=2)
    markers = line.get_required_markers()
    assert len(markers) == 1
    marker_id, marker_svg = markers[0]
    assert "arrow" in marker_id


def test_line_from_points_with_caps():
    line = Line.from_points(Point(0, 0), Point(100, 0), end_cap="arrow")
    assert line.effective_end_cap == "arrow"
    assert "marker-end" in line.to_svg()


# ---- Curve arrow tests ----


def test_curve_end_cap_arrow():
    curve = Curve(0, 0, 100, 0, curvature=0.5, end_cap="arrow")
    svg = curve.to_svg()
    assert "marker-end" in svg
    assert "marker-start" not in svg


def test_curve_cap_arrow_both():
    curve = Curve(0, 0, 100, 0, curvature=0.5, cap="arrow")
    svg = curve.to_svg()
    assert "marker-start" in svg
    assert "marker-end" in svg


def test_curve_no_arrow_default():
    curve = Curve(0, 0, 100, 0, curvature=0.5)
    svg = curve.to_svg()
    assert "marker-" not in svg


# ---- Style object tests ----


def test_line_style_with_caps():
    style = PathStyle(width=2, color="red", end_cap="arrow")
    assert style.end_cap == "arrow"
    assert style.start_cap is None


def test_line_style_direct_construction():
    style = PathStyle(width=2, end_cap="arrow")
    assert style.end_cap == "arrow"
    assert style.width == 2


def test_line_style_dataclass_replace():
    from dataclasses import replace

    style = PathStyle(width=3, color="blue", cap="butt", end_cap="arrow")
    new_style = replace(style, color="red")
    assert new_style.end_cap == "arrow"
    assert new_style.cap == "butt"
    assert new_style.width == 3


def test_connection_style_with_caps():
    style = PathStyle(width=2, color="red", end_cap="arrow")
    d = style.to_kwargs()
    assert d["end_cap"] == "arrow"
    assert "start_cap" not in d  # None values omitted


def test_connection_style_direct_construction():
    style = PathStyle(width=2, end_cap="arrow")
    assert style.end_cap == "arrow"


# ---- Scene defs tests ----


def test_scene_no_defs_without_arrows():
    scene = Scene(200, 200)
    scene.place(Line(0, 0, 100, 100))
    svg = scene.to_svg()
    assert "<defs>" not in svg


def test_scene_defs_with_arrows():
    scene = Scene(200, 200)
    scene.place(Line(0, 0, 100, 100, end_cap="arrow"))
    svg = scene.to_svg()
    assert "<defs>" in svg
    assert "<marker" in svg
    assert "</defs>" in svg


def test_scene_marker_deduplication():
    scene = Scene(200, 200)
    # Two lines with same color and width -> same marker
    scene.place(Line(0, 0, 100, 0, width=2, color="red", end_cap="arrow"))
    scene.place(Line(0, 50, 100, 50, width=2, color="red", end_cap="arrow"))
    svg = scene.to_svg()
    # Should only have one marker definition
    assert svg.count("<marker") == 1


def test_scene_multiple_markers_different_colors():
    scene = Scene(200, 200)
    scene.place(Line(0, 0, 100, 0, color="red", end_cap="arrow"))
    scene.place(Line(0, 50, 100, 50, color="blue", end_cap="arrow"))
    svg = scene.to_svg()
    # Should have two different markers
    assert svg.count("<marker") == 2


# ---- Cell builder tests ----


def test_cell_add_line_with_arrow():
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0][0]
    line = cell.add_line(start="left", end="right", end_cap="arrow")
    assert line.effective_end_cap == "arrow"


def test_cell_add_line_with_style_arrow():
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0][0]
    style = PathStyle(width=2, end_cap="arrow")
    line = cell.add_line(start="left", end="right", style=style)
    assert line.effective_end_cap == "arrow"


def test_cell_add_diagonal_with_arrow():
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0][0]
    line = cell.add_diagonal(end_cap="arrow")
    assert line.effective_end_cap == "arrow"


def test_cell_add_curve_with_arrow():
    scene = Scene.with_grid(cols=2, rows=2, cell_size=20)
    cell = scene.grid[0][0]
    curve = cell.add_curve(curvature=0.5, end_cap="arrow")
    assert curve.effective_end_cap == "arrow"


# ---- Backward compatibility ----


def test_backward_compat_line():
    """Existing code without arrows should produce identical output."""
    line = Line(10, 20, 100, 50, width=2, color="red", cap="round")
    svg = line.to_svg()
    assert 'stroke-linecap="round"' in svg
    assert "marker" not in svg


def test_backward_compat_curve():
    curve = Curve(10, 20, 100, 50, curvature=0.5, width=2, color="blue")
    svg = curve.to_svg()
    assert 'stroke-linecap="round"' in svg
    assert "marker" not in svg


# ---- Integration: full render ----


def test_full_render_with_arrows():
    """End-to-end: scene with arrow lines renders valid SVG."""
    scene = Scene.with_grid(cols=3, rows=3, cell_size=20)
    for cell in scene.grid:
        cell.add_line(start="left", end="right", end_cap="arrow", color="navy")
    svg = scene.to_svg()
    assert svg.startswith("<?xml")
    assert "<defs>" in svg
    assert "<marker" in svg
    assert "marker-end" in svg
    assert svg.endswith("</svg>")
