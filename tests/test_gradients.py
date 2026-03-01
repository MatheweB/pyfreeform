"""Tests for gradient support: LinearGradient, RadialGradient, entity integration, SVG output."""

import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from pyfreeform import (
    Dot,
    EntityGroup,
    FillStyle,
    LinearGradient,
    PathStyle,
    RadialGradient,
    Rect,
    Scene,
    ShapeStyle,
)
from pyfreeform.gradient import GradientStop, _parse_stops
from pyfreeform.paths import Lissajous, Wave


# =========================================================================
# GradientStop
# =========================================================================


class TestGradientStop:
    def test_to_svg_opaque(self):
        s = GradientStop(color="red", offset=0.5)
        assert s.to_svg() == '<stop offset="0.5" stop-color="red" />'

    def test_to_svg_transparent(self):
        s = GradientStop(color="#ff0000", offset=0.0, opacity=0.3)
        svg = s.to_svg()
        assert 'stop-opacity="0.3"' in svg

    def test_to_svg_fully_opaque_omits_attr(self):
        s = GradientStop(color="blue", offset=1.0, opacity=1.0)
        assert "stop-opacity" not in s.to_svg()


# =========================================================================
# _parse_stops
# =========================================================================


class TestParseStops:
    def test_minimum_two_stops(self):
        with pytest.raises(ValueError, match="at least 2"):
            _parse_stops(("red",))

    def test_bare_strings(self):
        stops = _parse_stops(("red", "blue"))
        assert len(stops) == 2
        assert stops[0].offset == 0.0
        assert stops[1].offset == 1.0

    def test_rgb_tuple(self):
        stops = _parse_stops(((255, 0, 0), (0, 0, 255)))
        assert stops[0].color == "#ff0000"
        assert stops[1].color == "#0000ff"

    def test_color_offset_tuple(self):
        stops = _parse_stops((("red", 0.3), ("blue", 0.8)))
        assert stops[0].offset == 0.3
        assert stops[1].offset == 0.8

    def test_color_offset_opacity_tuple(self):
        stops = _parse_stops((("red", 0.0, 0.5), ("blue", 1.0, 0.8)))
        assert stops[0].opacity == 0.5
        assert stops[1].opacity == 0.8

    def test_mixed_formats(self):
        stops = _parse_stops(("red", ("#00ff00", 0.5), ((0, 0, 255), 0.8, 0.5)))
        assert len(stops) == 3
        assert stops[1].offset == 0.5
        assert stops[2].opacity == 0.5

    def test_auto_distribute_offsets(self):
        stops = _parse_stops(("red", "green", "blue", "white"))
        offsets = [s.offset for s in stops]
        assert offsets == pytest.approx([0.0, 1 / 3, 2 / 3, 1.0])

    def test_bool_not_treated_as_int(self):
        # (True, 128, 0) should NOT be treated as RGB
        with pytest.raises(TypeError):
            _parse_stops(((True, 128, 0), "blue"))

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid stop format"):
            _parse_stops((("red", 0.0, 0.5, "extra"), "blue"))


# =========================================================================
# LinearGradient
# =========================================================================


class TestLinearGradient:
    def test_angle_0_left_to_right(self):
        g = LinearGradient("red", "blue", angle=0)
        assert g._x1 == pytest.approx(0.0)
        assert g._y1 == pytest.approx(0.5)
        assert g._x2 == pytest.approx(1.0)
        assert g._y2 == pytest.approx(0.5)

    def test_angle_90_top_to_bottom(self):
        g = LinearGradient("red", "blue", angle=90)
        assert g._x1 == pytest.approx(0.5)
        assert g._y1 == pytest.approx(0.0)
        assert g._x2 == pytest.approx(0.5)
        assert g._y2 == pytest.approx(1.0)

    def test_explicit_coordinates(self):
        g = LinearGradient("red", "blue", x1=0, y1=0, x2=1, y2=1)
        assert g._x1 == 0.0 and g._x2 == 1.0

    def test_partial_coordinates_rejected(self):
        with pytest.raises(ValueError, match="all of x1"):
            LinearGradient("red", "blue", x1=0.0)

    def test_bad_spread_method(self):
        with pytest.raises(ValueError, match="spread_method"):
            LinearGradient("red", "blue", spread_method="invalid")

    def test_bad_gradient_units(self):
        with pytest.raises(ValueError, match="gradient_units"):
            LinearGradient("red", "blue", gradient_units="invalid")

    def test_deterministic_id(self):
        g1 = LinearGradient("red", "blue")
        g2 = LinearGradient("red", "blue")
        assert g1.gradient_id == g2.gradient_id

    def test_different_params_different_id(self):
        g1 = LinearGradient("red", "blue")
        g2 = LinearGradient("red", "blue", angle=45)
        assert g1.gradient_id != g2.gradient_id

    def test_svg_ref(self):
        g = LinearGradient("red", "blue")
        assert g.to_svg_ref().startswith("url(#grad-")

    def test_svg_def(self):
        g = LinearGradient("red", "blue")
        svg = g.to_svg_def()
        assert svg.startswith("<linearGradient")
        assert "</linearGradient>" in svg
        assert '<stop offset="0.0"' in svg

    def test_spread_method_in_svg(self):
        g = LinearGradient("red", "blue", spread_method="reflect")
        assert 'spreadMethod="reflect"' in g.to_svg_def()

    def test_gradient_units_in_svg(self):
        g = LinearGradient("red", "blue", gradient_units="userSpaceOnUse")
        assert 'gradientUnits="userSpaceOnUse"' in g.to_svg_def()

    def test_repr(self):
        g = LinearGradient("red", "blue")
        assert "LinearGradient" in repr(g)


# =========================================================================
# RadialGradient
# =========================================================================


class TestRadialGradient:
    def test_default_center(self):
        g = RadialGradient("white", "black")
        assert g._cx == 0.5 and g._cy == 0.5

    def test_focal_point(self):
        g = RadialGradient("white", "black", fx=0.3, fy=0.3)
        assert 'fx="0.3"' in g.to_svg_def()
        assert 'fy="0.3"' in g.to_svg_def()

    def test_svg_def(self):
        g = RadialGradient("white", "black")
        svg = g.to_svg_def()
        assert svg.startswith("<radialGradient")
        assert "</radialGradient>" in svg


# =========================================================================
# Entity integration
# =========================================================================


class TestEntityIntegration:
    def test_dot_gradient(self):
        scene = Scene(100, 100)
        g = RadialGradient("white", "black")
        scene.add_dot(at=(0.5, 0.5), radius=0.3, color=g)
        svg = scene.to_svg()
        assert "url(#" in svg
        assert "<radialGradient" in svg

    def test_rect_fill_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_rect(fill=g, width=0.8, height=0.8)
        svg = scene.to_svg()
        assert "<linearGradient" in svg

    def test_rect_stroke_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_rect(fill=None, stroke=g, stroke_width=3, width=0.8, height=0.8)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_ellipse_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_ellipse(fill=g, rx=0.4, ry=0.4)
        svg = scene.to_svg()
        assert "<linearGradient" in svg

    def test_polygon_gradient(self):
        from pyfreeform import Polygon

        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_polygon(Polygon.hexagon(size=0.7), fill=g)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_text_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_text("Hi", at=(0.5, 0.5), color=g)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_line_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_line(start=(0.1, 0.1), end=(0.9, 0.9), color=g)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_curve_gradient(self):
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_curve(start=(0.1, 0.5), end=(0.9, 0.5), curvature=0.5, color=g)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_connection_gradient(self):
        scene = Scene(200, 100)
        g = LinearGradient("orange", "purple")
        d1 = scene.add_dot(at=(0.2, 0.5), radius=0.05)
        d2 = scene.add_dot(at=(0.8, 0.5), radius=0.05)
        d1.connect(d2, color=g)
        svg = scene.to_svg()
        assert "<linearGradient" in svg

    def test_closed_path_gradient_fill(self):
        scene = Scene(200, 200)
        g = LinearGradient("red", "blue")
        scene.add_path(
            Lissajous(center=(0.5, 0.5), size=0.35),
            fill=g,
            width=2,
            color="black",
            closed=True,
        )
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_entity_group_gradient_collection(self):
        outer = EntityGroup()
        inner = EntityGroup()
        g = LinearGradient("red", "blue")
        inner.add(Dot(0, 0, radius=5, color=g))
        outer.add(inner)
        grads = outer.get_required_gradients()
        assert len(grads) == 1


# =========================================================================
# SVG output
# =========================================================================


class TestSvgOutput:
    def test_gradient_deduplication(self):
        scene = Scene(200, 100)
        g = LinearGradient("red", "blue")
        scene.add_rect(fill=g, width=0.4, height=0.8, at=(0.25, 0.5))
        scene.add_rect(fill=g, width=0.4, height=0.8, at=(0.75, 0.5))
        svg = scene.to_svg()
        assert svg.count("<linearGradient") == 1

    def test_multiple_gradient_types(self):
        scene = Scene(200, 100)
        g1 = LinearGradient("red", "blue")
        g2 = RadialGradient("white", "black")
        scene.add_rect(fill=g1, width=0.4, height=0.8, at=(0.25, 0.5))
        scene.add_ellipse(fill=g2, rx=0.15, ry=0.3, at=(0.75, 0.5))
        svg = scene.to_svg()
        assert "<linearGradient" in svg
        assert "<radialGradient" in svg

    def test_empty_scene_no_defs(self):
        scene = Scene(100, 100)
        svg = scene.to_svg()
        assert "<defs>" not in svg

    def test_stop_opacity_in_svg(self):
        scene = Scene(200, 50)
        g = LinearGradient(("coral", 0.0, 1.0), ("coral", 1.0, 0.0))
        scene.add_rect(fill=g, width=1.0, height=1.0)
        svg = scene.to_svg()
        assert "stop-opacity" in svg

    def test_trim_preserves_gradients(self):
        scene = Scene(200, 200, background="white")
        scene.add_rect(fill=LinearGradient("red", "blue"), width=0.5, height=0.5)
        trimmed = scene.trim()
        svg = trimmed.to_svg()
        assert "<linearGradient" in svg

    def test_many_unique_gradients(self):
        scene = Scene(500, 100)
        for i in range(50):
            g = LinearGradient(
                f"hsl({i * 7}, 80%, 50%)", f"hsl({i * 7 + 180}, 80%, 50%)"
            )
            scene.add_rect(fill=g, width=0.018, height=0.8, at=(0.01 + i * 0.02, 0.5))
        svg = scene.to_svg()
        assert svg.count("<linearGradient") == 50


# =========================================================================
# Property mutation
# =========================================================================


class TestPropertyMutation:
    def test_rect_fill_gradient_then_color(self):
        r = Rect(10, 10, 50, 50, fill="red")
        g = LinearGradient("cyan", "magenta")
        r.fill = g
        assert r.fill == g.to_svg_ref()
        r.fill = "green"
        assert r.fill is not None
        assert "url(" not in r.fill

    def test_dot_color_gradient_then_color(self):
        d = Dot(10, 10, radius=5, color="red")
        g = RadialGradient("white", "black")
        d.color = g
        assert d.color == g.to_svg_ref()
        d.color = "blue"
        assert "url(" not in d.color


# =========================================================================
# Style classes
# =========================================================================


class TestStyleClasses:
    def test_fill_style_accepts_gradient(self):
        g = LinearGradient("red", "blue")
        fs = FillStyle(color=g, z_index=1)
        assert fs.color is g

    def test_path_style_accepts_gradient(self):
        g = LinearGradient("red", "blue")
        ps = PathStyle(color=g, width=2)
        assert ps.color is g

    def test_shape_style_accepts_gradient(self):
        g1 = LinearGradient("red", "blue")
        g2 = RadialGradient("white", "black")
        ss = ShapeStyle(color=g1, stroke=g2)
        assert ss.color is g1
        assert ss.stroke is g2


# =========================================================================
# Brightness guard
# =========================================================================


class TestBrightnessGuard:
    def test_gradient_ignores_color_brightness(self):
        """Gradient + color_brightness should not crash."""
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_dot(color=g, radius=0.3, color_brightness=0.5)
        svg = scene.to_svg()
        assert "url(#" in svg

    def test_gradient_ignores_fill_brightness(self):
        """Gradient + fill_brightness should not crash."""
        scene = Scene(100, 100)
        g = LinearGradient("red", "blue")
        scene.add_rect(fill=g, width=0.8, height=0.8, fill_brightness=0.5)
        svg = scene.to_svg()
        assert "url(#" in svg


# =========================================================================
# textPath cross-browser fix
# =========================================================================


class TestTextPath:
    def test_textlength_on_both_elements(self):
        scene = Scene(300, 300)
        w = Wave(start=(0.1, 0.5), end=(0.9, 0.5), amplitude=0.15)
        scene.add_text("Hello World", along=w, color="white")
        svg = scene.to_svg()
        text_tag = re.search(r"<text [^>]+>", svg)
        textpath_tag = re.search(r"<textPath [^>]+>", svg)
        assert text_tag is not None
        assert textpath_tag is not None
        assert "textLength" in text_tag.group()
        assert "textLength" in textpath_tag.group()
        assert "lengthAdjust" in text_tag.group()
        assert "lengthAdjust" in textpath_tag.group()
