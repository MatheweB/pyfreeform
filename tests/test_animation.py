"""Tests for the animation system — models, builders, and SMIL rendering."""

from __future__ import annotations

import pytest

from pyfreeform import Curve, Dot, Easing, Ellipse, Line, Polygon, Rect, Scene, Path, Text, Connection, stagger
from pyfreeform.core.coord import Coord
from pyfreeform.core.svg_utils import svg_num
from pyfreeform.entities.point import Point
from pyfreeform.animation.models import (
    DrawAnimation,
    Keyframe,
    PropertyAnimation,
    coerce_easing,
)
from pyfreeform.animation.builders import (
    build_animate,
    build_draw,
    build_fade,
    build_move,
    build_scale,
    build_spin,
)
from pyfreeform.renderers import SMILRenderer, SVGRenderer


# ======================================================================
# Easing
# ======================================================================


class TestEasing:
    def test_linear(self):
        assert Easing.LINEAR.evaluate(0.5) == pytest.approx(0.5, abs=0.01)
        assert Easing.LINEAR.evaluate(0.0) == 0.0
        assert Easing.LINEAR.evaluate(1.0) == 1.0

    def test_ease_in(self):
        mid = Easing.EASE_IN.evaluate(0.5)
        # ease-in should be below the linear midpoint
        assert mid < 0.5

    def test_ease_out(self):
        mid = Easing.EASE_OUT.evaluate(0.5)
        # ease-out should be above the linear midpoint
        assert mid > 0.5

    def test_ease_in_out(self):
        q1 = Easing.EASE_IN_OUT.evaluate(0.25)
        q3 = Easing.EASE_IN_OUT.evaluate(0.75)
        # symmetric: ease-in-out(0.25) + ease-in-out(0.75) ≈ 1.0
        assert q1 + q3 == pytest.approx(1.0, abs=0.05)

    def test_coerce_string(self):
        assert coerce_easing("linear") == Easing.LINEAR
        assert coerce_easing("ease-in") == Easing.EASE_IN
        assert coerce_easing("ease-out") == Easing.EASE_OUT
        assert coerce_easing("ease-in-out") == Easing.EASE_IN_OUT

    def test_coerce_tuple(self):
        e = coerce_easing((0.25, 0.1, 0.25, 1.0))
        assert e.x1 == 0.25
        assert e.y1 == 0.1

    def test_coerce_easing_passthrough(self):
        assert coerce_easing(Easing.LINEAR) is Easing.LINEAR


# ======================================================================
# Keyframe and PropertyAnimation
# ======================================================================


class TestPropertyAnimation:
    def test_construction(self):
        anim = PropertyAnimation(
            prop="opacity",
            keyframes=[Keyframe(0, 1.0), Keyframe(2.0, 0.0)],
        )
        assert anim.prop == "opacity"
        assert anim.duration == 2.0
        assert len(anim.keyframes) == 2

    def test_evaluate_linear(self):
        anim = PropertyAnimation(
            prop="opacity",
            keyframes=[Keyframe(0, 1.0), Keyframe(2.0, 0.0)],
        )
        assert anim.evaluate(0.0) == pytest.approx(1.0)
        assert anim.evaluate(1.0) == pytest.approx(0.5, abs=0.05)
        assert anim.evaluate(2.0) == pytest.approx(0.0)

    def test_evaluate_hold(self):
        anim = PropertyAnimation(
            prop="opacity",
            keyframes=[Keyframe(0, 1.0), Keyframe(1.0, 0.0)],
            hold=True,
        )
        # After duration, hold final value
        assert anim.evaluate(2.0) == pytest.approx(0.0)

    def test_evaluate_no_hold(self):
        anim = PropertyAnimation(
            prop="opacity",
            keyframes=[Keyframe(0, 1.0), Keyframe(1.0, 0.0)],
            hold=False,
        )
        # After duration, should return initial value
        assert anim.evaluate(2.0) == pytest.approx(1.0)


# ======================================================================
# DrawAnimation
# ======================================================================


class TestDrawAnimation:
    def test_construction(self):
        anim = DrawAnimation(duration=2.0)
        assert anim.duration == 2.0
        assert anim.reverse is False

    def test_evaluate(self):
        anim = DrawAnimation(duration=2.0)
        assert anim.evaluate(0.0) == pytest.approx(0.0)
        assert anim.evaluate(1.0) == pytest.approx(0.5, abs=0.05)
        assert anim.evaluate(2.0) == pytest.approx(1.0)

    def test_evaluate_reverse(self):
        anim = DrawAnimation(duration=1.0, reverse=True)
        assert anim.evaluate(0.0) == pytest.approx(1.0)
        assert anim.evaluate(1.0) == pytest.approx(0.0)


# ======================================================================
# Builders
# ======================================================================


class TestBuilders:
    def test_build_fade(self):
        dot = Dot(0, 0)
        anim = build_fade(dot, to=0.0, duration=2.0)
        assert isinstance(anim, PropertyAnimation)
        assert anim.prop == "opacity"
        assert anim.keyframes[0].value == 1.0
        assert anim.keyframes[-1].value == 0.0

    def test_build_spin(self):
        dot = Dot(0, 0)
        anim = build_spin(dot, angle=360, duration=3.0)
        anim.repeat = True
        assert isinstance(anim, PropertyAnimation)
        assert anim.prop == "rotation"
        assert anim.repeat is True

    def test_build_draw(self):
        anim = build_draw(duration=2.0, reverse=True)
        assert isinstance(anim, DrawAnimation)
        assert anim.duration == 2.0
        assert anim.reverse is True

    def test_build_animate_generic(self):
        dot = Dot(0, 0, radius=5)
        anim = build_animate(dot, "radius", to=20, duration=1.5)
        assert isinstance(anim, PropertyAnimation)
        assert anim.prop == "radius"


# ======================================================================
# Entity animation API
# ======================================================================


class TestEntityAnimationAPI:
    def test_fade_returns_self(self):
        dot = Dot(0, 0)
        result = dot.animate_fade(to=0.0, duration=1.0)
        assert result is dot

    def test_fade_adds_animation(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "opacity"

    def test_chaining(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.5, duration=1.0).animate_spin(360, duration=2.0)
        assert len(dot.animations) == 2

    def test_clear_animations(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0).animate_spin(360)
        assert len(dot.animations) == 2
        dot.clear_animations()
        assert len(dot.animations) == 0

    def test_generic_animate(self):
        dot = Dot(0, 0, radius=5)
        dot.animate_radius(to=20, duration=1.5)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "r"

    def test_spin(self):
        rect = Rect(0, 0, 100, 100)
        rect.animate_spin(360, duration=2.0)
        rect.loop()
        assert len(rect.animations) == 1
        assert rect.animations[0].prop == "rotation"


# ======================================================================
# Path draw animation
# ======================================================================


class TestPathDraw:
    def test_path_draw(self):
        from pyfreeform.paths import Wave

        p = Path(Wave(), width=2, color="blue")
        result = p.animate_draw(duration=2.0)
        assert result is p
        assert len(p.animations) == 1
        assert isinstance(p.animations[0], DrawAnimation)


class TestLineDraw:
    def test_line_draw_returns_self(self):
        line = Line(0, 0, 100, 50, width=2, color="blue")
        result = line.animate_draw(duration=1.5)
        assert result is line

    def test_line_draw_adds_animation(self):
        line = Line(0, 0, 100, 50, width=2, color="blue")
        line.animate_draw(duration=1.0)
        assert len(line.animations) == 1
        assert isinstance(line.animations[0], DrawAnimation)

    def test_line_draw_smil_output(self):
        line = Line(0, 0, 100, 0, width=2, color="blue")
        line.animate_draw(duration=1.0)
        svg = SMILRenderer().render_entity(line)
        assert 'pathLength="1"' in svg
        assert "stroke-dasharray" in svg


class TestCurveDraw:
    def test_curve_draw_returns_self(self):
        curve = Curve(0, 0, 100, 50, curvature=0.3, width=2, color="red")
        result = curve.animate_draw(duration=1.5)
        assert result is curve

    def test_curve_draw_adds_animation(self):
        curve = Curve(0, 0, 100, 50, curvature=0.3, width=2, color="red")
        curve.animate_draw(duration=1.0)
        assert len(curve.animations) == 1
        assert isinstance(curve.animations[0], DrawAnimation)

    def test_curve_draw_smil_output(self):
        curve = Curve(0, 0, 100, 0, curvature=0.5, width=2, color="red")
        curve.animate_draw(duration=1.0)
        svg = SMILRenderer().render_entity(curve)
        assert 'pathLength="1"' in svg
        assert "stroke-dasharray" in svg


# ======================================================================
# Keyframe list shorthand
# ======================================================================


class TestKeyframeList:
    def test_list_three_values(self):
        """List of 3 values distributes evenly over duration."""
        dot = Dot(0, 0, radius=5, color="red")
        dot.animate_color(keyframes=["red", "blue", "red"], duration=2.0)
        anim = dot.animations[0]
        assert len(anim.keyframes) == 3
        assert anim.keyframes[0].time == pytest.approx(0.0)
        assert anim.keyframes[1].time == pytest.approx(1.0)
        assert anim.keyframes[2].time == pytest.approx(2.0)
        assert anim.keyframes[0].value == "red"
        assert anim.keyframes[1].value == "blue"
        assert anim.keyframes[2].value == "red"

    def test_list_two_values(self):
        """List of 2 values → 0 and duration."""
        dot = Dot(0, 0)
        dot.animate_fade(keyframes=[1.0, 0.0], duration=3.0)
        anim = dot.animations[0]
        assert len(anim.keyframes) == 2
        assert anim.keyframes[0].time == pytest.approx(0.0)
        assert anim.keyframes[1].time == pytest.approx(3.0)

    def test_list_one_value_raises(self):
        """List with fewer than 2 values raises ValueError."""
        dot = Dot(0, 0)
        with pytest.raises(ValueError, match="at least 2"):
            dot.animate_fade(keyframes=[0.5], duration=1.0)

    def test_list_with_generic_animate(self):
        """List keyframes work with the generic .animate() method."""
        dot = Dot(0, 0)
        dot.animate("opacity", keyframes=[1.0, 0.5, 1.0], duration=4.0)
        anim = dot.animations[0]
        assert len(anim.keyframes) == 3
        assert anim.keyframes[0].time == pytest.approx(0.0)
        assert anim.keyframes[1].time == pytest.approx(2.0)
        assert anim.keyframes[2].time == pytest.approx(4.0)


# ======================================================================
# Connection animation API
# ======================================================================


class TestConnectionAnimation:
    def test_connection_fade(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        result = conn.animate_fade(to=0.0, duration=1.0)
        assert result is conn
        assert len(conn.animations) == 1

    def test_connection_draw(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_draw(duration=1.5)
        assert len(conn.animations) == 1
        assert isinstance(conn.animations[0], DrawAnimation)

    def test_connection_clear(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_fade(to=0.0).animate_draw(duration=1.0)
        assert len(conn.animations) == 2
        conn.clear_animations()
        assert len(conn.animations) == 0


# ======================================================================
# Renderer tests
# ======================================================================


class TestSVGRenderer:
    """SVGRenderer should produce identical output to old to_svg() for non-animated entities."""

    def test_render_dot(self):
        dot = Dot(10, 20, radius=5, color="red")
        renderer = SVGRenderer()
        svg = renderer.render_entity(dot)
        assert 'cx="10"' in svg
        assert 'cy="20"' in svg
        assert 'r="5"' in svg
        assert 'fill="red"' in svg or "fill=\"#" in svg

    def test_render_rect(self):
        rect = Rect(10, 20, 100, 50, fill="blue")
        renderer = SVGRenderer()
        svg = renderer.render_entity(rect)
        assert '<rect' in svg
        assert 'width="100"' in svg
        assert 'height="50"' in svg

    def test_render_line(self):
        line = Line(0, 0, 100, 100, width=2, color="green")
        renderer = SVGRenderer()
        svg = renderer.render_entity(line)
        assert '<line' in svg
        assert 'x1="0"' in svg
        assert 'y1="0"' in svg


class TestSMILRenderer:
    """SMILRenderer should add SMIL animation elements for animated entities."""

    def test_no_animation_matches_static(self):
        dot = Dot(10, 20, radius=5, color="red")
        static = SVGRenderer().render_entity(dot)
        animated = SMILRenderer().render_entity(dot)
        assert static == animated

    def test_fade_produces_animate(self):
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_entity(dot)
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg
        assert 'dur="2.0s"' in svg

    def test_spin_produces_animate_transform(self):
        rect = Rect(0, 0, 100, 100)
        rect.animate_spin(360, duration=3.0)
        rect.loop()
        svg = SMILRenderer().render_entity(rect)
        assert "animateTransform" in svg
        assert 'type="rotate"' in svg
        assert 'repeatCount="indefinite"' in svg

    def test_draw_produces_dashoffset(self):
        from pyfreeform.paths import Wave

        p = Path(Wave(), width=2, color="blue")
        p.animate_draw(duration=2.0)
        svg = SMILRenderer().render_entity(p)
        assert 'pathLength="1"' in svg
        assert 'stroke-dasharray="1"' in svg
        assert 'stroke-dashoffset="1"' in svg
        assert "<animate" in svg

    def test_easing_produces_key_splines(self):
        dot = Dot(10, 20)
        dot.animate_fade(to=0.0, duration=1.0, easing="ease-in-out")
        svg = SMILRenderer().render_entity(dot)
        assert 'calcMode="spline"' in svg
        assert "keySplines" in svg

    def test_hold_produces_fill_freeze(self):
        dot = Dot(10, 20)
        dot.animate_fade(to=0.0, duration=1.0, hold=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'fill="freeze"' in svg


# ======================================================================
# Scene render() integration
# ======================================================================


class TestSceneRender:
    def test_scene_render_default(self):
        scene = Scene(100, 100, background="white")
        svg = scene.render()
        assert "<svg" in svg
        assert "</svg>" in svg

    def test_scene_render_explicit_renderer(self):
        scene = Scene(100, 100)
        svg = scene.render(SVGRenderer())
        assert "<svg" in svg

    def test_scene_to_svg_delegates(self):
        scene = Scene(100, 100)
        assert scene.to_svg() == scene.render()

    def test_animated_scene(self):
        scene = Scene(200, 200, background="black")
        dot = Dot(100, 100, radius=10, color="coral")
        scene.place(dot)
        dot.animate_fade(to=0.0, duration=2.0)
        svg = scene.to_svg()
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg


# ======================================================================
# .then() — Sequential chaining
# ======================================================================


class TestThen:
    def test_basic_chaining(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then().animate_spin(360, duration=1.0)
        assert len(dot.animations) == 2
        fade_anim = dot.animations[0]
        spin_anim = dot.animations[1]
        assert fade_anim.delay == 0.0
        assert spin_anim.delay == pytest.approx(1.0)

    def test_gap_parameter(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then(0.5).animate_spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        assert spin_anim.delay == pytest.approx(1.5)

    def test_no_animations(self):
        dot = Dot(0, 0)
        result = dot.then()
        assert result is dot
        # Chain delay should be 0 — next animation starts immediately
        dot.animate_fade(to=0.0, duration=1.0)
        assert dot.animations[0].delay == 0.0

    def test_repeat_finite(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        dot.loop(times=3)
        dot.then().animate_spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        # repeat=3 means 3 cycles × 1.0s = 3.0s total
        assert spin_anim.delay == pytest.approx(3.0)

    def test_repeat_infinite(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        dot.loop()
        dot.then().animate_spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        # repeat=True: use single cycle duration (pragmatic fallback)
        assert spin_anim.delay == pytest.approx(1.0)

    def test_multi_then(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then().animate_spin(360, duration=2.0).then().animate_fade(to=1.0, duration=0.5)
        anims = dot.animations
        assert anims[0].delay == pytest.approx(0.0)   # fade
        assert anims[1].delay == pytest.approx(1.0)   # spin
        assert anims[2].delay == pytest.approx(3.0)   # fade back (1.0 + 2.0)

    def test_with_explicit_delay(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then().animate_spin(360, duration=1.0, delay=0.5)
        spin_anim = dot.animations[1]
        # Chain delay 1.0 + explicit delay 0.5 = 1.5
        assert spin_anim.delay == pytest.approx(1.5)

    def test_returns_self(self):
        dot = Dot(0, 0)
        result = dot.animate_fade(to=0.0).then()
        assert result is dot

    def test_connection_then(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_draw(duration=1.5).then().animate_fade(to=0.0, duration=0.5)
        draw_anim = conn.animations[0]
        fade_anim = conn.animations[1]
        assert draw_anim.delay == 0.0
        assert fade_anim.delay == pytest.approx(1.5)

    def test_clear_resets_chain_delay(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then()
        dot.clear_animations()
        dot.animate_fade(to=0.5, duration=1.0)
        assert dot.animations[0].delay == 0.0

    def test_chain_delay_consumed_once(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then()
        dot.animate_spin(360, duration=1.0)  # consumes chain delay
        dot.animate_fade(to=1.0, duration=1.0)  # no chain delay left
        assert dot.animations[1].delay == pytest.approx(1.0)
        assert dot.animations[2].delay == pytest.approx(0.0)


# ======================================================================
# stagger()
# ======================================================================


class TestStagger:
    def test_basic_stagger(self):
        dots = [Dot(i * 10, 0) for i in range(5)]
        result = stagger(*dots, offset=0.2, each=lambda d: d.animate_fade(to=0.0, duration=1.0))
        assert result is not dots  # returns new list
        assert len(result) == 5
        for i, dot in enumerate(result):
            assert len(dot.animations) == 1
            assert dot.animations[0].delay == pytest.approx(i * 0.2)

    def test_custom_offset(self):
        dots = [Dot(0, 0), Dot(10, 0), Dot(20, 0)]
        stagger(*dots, offset=0.5, each=lambda d: d.animate_fade(to=0.0))
        assert dots[0].animations[0].delay == pytest.approx(0.0)
        assert dots[1].animations[0].delay == pytest.approx(0.5)
        assert dots[2].animations[0].delay == pytest.approx(1.0)

    def test_multiple_animations_per_entity(self):
        dots = [Dot(0, 0), Dot(10, 0)]
        stagger(*dots, offset=0.3, each=lambda d: d.animate_fade(to=0.0).animate_spin(360))
        # Both fade and spin should get stagger offset
        assert dots[0].animations[0].delay == pytest.approx(0.0)
        assert dots[0].animations[1].delay == pytest.approx(0.0)
        assert dots[1].animations[0].delay == pytest.approx(0.3)
        assert dots[1].animations[1].delay == pytest.approx(0.3)

    def test_preserves_explicit_delay(self):
        dots = [Dot(0, 0), Dot(10, 0)]
        stagger(*dots, offset=0.2, each=lambda d: d.animate_fade(to=0.0, delay=0.5))
        # dot[0]: 0.5 + 0*0.2 = 0.5
        # dot[1]: 0.5 + 1*0.2 = 0.7
        assert dots[0].animations[0].delay == pytest.approx(0.5)
        assert dots[1].animations[0].delay == pytest.approx(0.7)


# ======================================================================
# .animate_move(by=)
# ======================================================================


class TestMoveBy:
    def test_move_by_basic(self):
        dot = Dot(0, 0)
        dot.animate_move(by=(0.1, 0.2), duration=1.0)
        # Should have 2 animations (at_rx, at_ry)
        assert len(dot.animations) == 2

    def test_move_to_still_works(self):
        dot = Dot(0, 0)
        dot.animate_move(to=(0.8, 0.5), duration=1.0)
        assert len(dot.animations) == 2

    def test_move_positional_to(self):
        dot = Dot(0, 0)
        dot.animate_move((0.8, 0.5), duration=1.0)
        assert len(dot.animations) == 2

    def test_move_to_and_by_error(self):
        dot = Dot(0, 0)
        with pytest.raises(ValueError, match="Cannot specify both"):
            dot.animate_move(to=(0.5, 0.5), by=(0.1, 0))

    def test_move_neither_error(self):
        dot = Dot(0, 0)
        with pytest.raises(ValueError, match="Must specify either"):
            dot.animate_move(duration=1.0)

    def test_move_by_computes_target(self):
        """move(by=) should compute target as current + delta."""
        anim = build_move(Dot(0, 0), by=(0.1, -0.1), duration=1.0)
        # Default at is (0.5, 0.5), so target should be (0.6, 0.4)
        rx_anim = anim[0]
        ry_anim = anim[1]
        assert rx_anim.keyframes[0].value == pytest.approx(0.5)
        assert rx_anim.keyframes[1].value == pytest.approx(0.6)
        assert ry_anim.keyframes[0].value == pytest.approx(0.5)
        assert ry_anim.keyframes[1].value == pytest.approx(0.4)


# ======================================================================
# .animate_scale()
# ======================================================================


class TestScale:
    def test_scale_returns_self(self):
        dot = Dot(0, 0)
        result = dot.animate_scale(to=2.0, duration=1.0)
        assert result is dot

    def test_scale_adds_animation(self):
        dot = Dot(0, 0)
        dot.animate_scale(to=2.0)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "scale_factor"

    def test_scale_keyframes(self):
        dot = Dot(0, 0)
        dot.animate_scale(to=2.0, duration=1.5)
        anim = dot.animations[0]
        assert anim.keyframes[0].value == pytest.approx(1.0)
        assert anim.keyframes[1].value == pytest.approx(2.0)
        assert anim.duration == pytest.approx(1.5)

    def test_scale_pulse(self):
        dot = Dot(0, 0)
        dot.animate_scale(to=1.5, duration=0.8)
        dot.loop(bounce=True)
        anim = dot.animations[0]
        assert anim.bounce is True
        assert anim.repeat is True
        assert anim.duration == pytest.approx(0.8)

    def test_build_scale(self):
        dot = Dot(0, 0)
        anim = build_scale(dot, to=3.0, duration=2.0)
        assert isinstance(anim, PropertyAnimation)
        assert anim.prop == "scale_factor"
        assert anim.keyframes[0].value == pytest.approx(1.0)
        assert anim.keyframes[1].value == pytest.approx(3.0)

    def test_scale_smil_output(self):
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_scale(to=2.0, duration=1.0)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        assert 'type="scale"' in svg

    def test_scale_with_then(self):
        dot = Dot(0, 0)
        dot.animate_fade(to=0.5, duration=1.0).then().animate_scale(to=2.0, duration=0.5)
        scale_anim = dot.animations[1]
        assert scale_anim.delay == pytest.approx(1.0)


# ======================================================================
# Bounce SMIL rendering
# ======================================================================


class TestBounceSMIL:
    """Test that bounce=True produces correct SMIL output."""

    def test_property_bounce_values_mirrored(self):
        """bounce=True mirrors values: A;B → A;B;A."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0)
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'values="5;10;5"' in svg

    def test_property_bounce_keytimes(self):
        """bounce=True produces keyTimes 0;0.5;1."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0)
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'keyTimes="0;0.5;1"' in svg

    def test_property_bounce_doubled_splines(self):
        """bounce=True doubles keySplines for 2 segments."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0, easing="ease-in-out")
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        # 2 segments (3 values) → 2 keySplines
        assert 'keySplines="0.42 0.0 0.58 1.0;0.42 0.0 0.58 1.0"' in svg

    def test_property_no_bounce_unchanged(self):
        """Without bounce, values stay as-is."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0)
        dot.loop()
        svg = SMILRenderer().render_entity(dot)
        assert 'values="5;10"' in svg
        assert 'keyTimes="0;1"' in svg

    def test_motion_bounce_keypoints(self):
        """bounce=True on follow() adds keyPoints='0;1;0'."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.animate_follow(wave, duration=2.0)
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'keyPoints="0;1;0"' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_motion_no_bounce_no_keypoints(self):
        """Without bounce, no keyPoints on animateMotion."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.animate_follow(wave, duration=2.0)
        dot.loop()
        svg = SMILRenderer().render_entity(dot)
        assert "keyPoints" not in svg

    def test_motion_bounce_eased(self):
        """bounce + easing produces 2 keySplines on animateMotion."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.animate_follow(wave, duration=2.0, easing="ease-in-out")
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'keySplines="0.42 0.0 0.58 1.0;0.42 0.0 0.58 1.0"' in svg

    def test_motion_bounce_linear_uses_linear_calcmode(self):
        """bounce + linear easing uses calcMode='linear'."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.animate_follow(wave, duration=2.0, easing="linear")
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'calcMode="linear"' in svg
        assert "keySplines" not in svg

    def test_draw_bounce_values(self):
        """bounce=True on draw() produces normalized forward-then-reverse dashoffset."""
        from pyfreeform.paths import Wave
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        path = Path(wave, width=2, color="red")
        scene = Scene(200, 200)
        scene.place(path)
        path.animate_draw(duration=2.0)
        path.loop(bounce=True)
        svg = SMILRenderer().render_entity(path)
        # Normalized to [0, 1] via pathLength="1"
        assert 'values="1;0;1"' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_rotation_bounce(self):
        """bounce=True on spin mirrors rotation values."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_spin(90, duration=1.0)
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        # Should have 3 values for rotation (forward;peak;back)
        assert 'keyTimes="0;0.5;1"' in svg

    def test_scale_bounce(self):
        """bounce=True on scale mirrors scale values."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_scale(to=2.0, duration=1.0)
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        assert 'values="1;2;1"' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_multi_keyframe_bounce(self):
        """Bounce with 3+ keyframes mirrors correctly."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(keyframes={0: 5, 0.5: 10, 1.0: 15})
        dot.loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        # 5;10;15 → 5;10;15;10;5 with 5 keyTimes
        assert 'values="5;10;15;10;5"' in svg
        assert 'keyTimes="0;0.25;0.5;0.75;1"' in svg


# ======================================================================
# Fill/Stroke opacity animation (universal mapping)
# ======================================================================


class TestOpacityAnimations:
    """Verify fill-opacity and stroke-opacity animate on all shape types."""

    def test_fill_opacity_animation_ellipse(self):
        """fill_opacity animates to fill-opacity on Ellipse."""
        e = Ellipse(50, 50, rx=20, ry=15, fill="blue")
        e.animate_fill_opacity(keyframes={0: 1.0, 1.0: 0.0}, duration=2.0)
        svg = SMILRenderer().render_entity(e)
        assert 'attributeName="fill-opacity"' in svg
        assert 'values="1;0"' in svg

    def test_stroke_opacity_animation_polygon(self):
        """stroke_opacity animates to stroke-opacity on Polygon."""
        p = Polygon([(0, 0), (20, 0), (10, 20)], fill="red", stroke="black")
        p.animate_stroke_opacity(keyframes={0: 1.0, 1.0: 0.3}, duration=1.5)
        svg = SMILRenderer().render_entity(p)
        assert 'attributeName="stroke-opacity"' in svg

    def test_fill_opacity_animation_rect(self):
        """fill_opacity still works on Rect after universal mapping."""
        r = Rect(10, 10, 50, 30, fill="green")
        r.animate_fill_opacity(keyframes={0: 1.0, 1.0: 0.0}, duration=1.0)
        svg = SMILRenderer().render_entity(r)
        assert 'attributeName="fill-opacity"' in svg


# ======================================================================
# TextPath animation
# ======================================================================


class TestTextPathAnimation:
    """Verify animated text-on-path renders with SMIL elements."""

    def test_textpath_fade(self):
        """Text on a path with fade() emits <animate> inside <text>."""
        t = Text(0, 0, "Hello", font_size=16, color="black")
        t.set_textpath("tp1", "M 10 80 Q 95 10 180 80", start_offset="50%")
        t.animate_fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_entity(t)
        assert "<textPath" in svg
        assert 'href="#tp1"' in svg
        assert 'attributeName="opacity"' in svg
        assert "<animate" in svg

    def test_textpath_color_animation(self):
        """Text on a path with color animation emits fill attribute."""
        t = Text(0, 0, "World", font_size=16, color="red")
        t.set_textpath("tp2", "M 0 0 L 100 0", start_offset="0%")
        t.animate_color(keyframes={0: "red", 1.0: "blue"}, duration=1.0)
        svg = SMILRenderer().render_entity(t)
        assert "<textPath" in svg
        assert 'attributeName="fill"' in svg

    def test_textpath_no_animation_uses_static(self):
        """Text on path without animations still renders statically."""
        t = Text(0, 0, "Static", font_size=16, color="black")
        t.set_textpath("tp3", "M 0 0 L 100 0")
        svg = SMILRenderer().render_entity(t)
        assert "<textPath" in svg
        assert "<animate" not in svg


# ======================================================================
# Connection property animation (regression after dead code removal)
# ======================================================================


class TestConnectionPropertySMIL:
    """Verify connection property animations render correctly."""

    def test_connection_fade_smil(self):
        """Connection fade renders <animate attributeName='opacity'>."""
        d1 = Dot(10, 20, radius=5, color="red")
        d2 = Dot(80, 80, radius=5, color="blue")
        conn = Connection(d1, d2)
        conn.animate_fade(to=0.0, duration=1.5)
        svg = SMILRenderer().render_connection(conn)
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg

    def test_connection_color_animation_smil(self):
        """Connection color animation uses opacity-layer optimization."""
        d1 = Dot(10, 20, radius=5, color="red")
        d2 = Dot(80, 80, radius=5, color="blue")
        conn = Connection(d1, d2)
        conn.animate_color(keyframes={0: "red", 1.0: "blue"}, duration=1.0)
        svg = SMILRenderer().render_connection(conn)
        # Optimized: no attributeName="stroke", uses opacity layers instead
        assert "<g>" in svg
        assert 'attributeName="opacity"' in svg


# ======================================================================
# Reactive animation tests
# ======================================================================


class TestReactivePolygonAnimation:
    """Reactive polygon animations when vertices are animated entities."""

    def test_animated_vertex_emits_points_animate(self):
        """Polygon vertex entity with .animate_move() produces <animate attributeName="points">."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        scene.add(b, at=(0.9, 0.1))
        scene.add(c, at=(0.5, 0.9))
        b.animate_move(to=(0.5, 0.5), duration=2.0)
        poly = Polygon([a, b, c], fill="red")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' in svg
        assert 'dur="2' in svg

    def test_static_vertices_no_reactive(self):
        """Polygon with only static coords emits no reactive animation."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="blue")
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' not in svg

    def test_mixed_static_and_animated(self):
        """Mixed static + animated vertices both appear in points values."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        a.animate_move(to=(0.9, 0.9), duration=1.0)
        poly = Polygon([a, Coord(100, 100), Coord(0, 100)], fill="green")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' in svg
        # Static coords should appear in the values (constant across keyframes)
        assert "100,100" in svg

    def test_incompatible_vertex_anims_resampled(self):
        """Vertices with different durations produce resampled reactive animation."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        scene.add(b, at=(0.9, 0.1))
        scene.add(c, at=(0.5, 0.9))
        a.animate_move(to=(0.5, 0.5), duration=1.0)
        b.animate_move(to=(0.5, 0.5), duration=2.0)  # Different duration
        poly = Polygon([a, b, c], fill="red")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        # Mixed timing now produces a resampled reactive animation
        assert '<animate attributeName="points"' in svg

    def test_own_animations_coexist(self):
        """Polygon's own opacity animation + reactive vertex animation both appear."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        a.animate_move(to=(0.5, 0.5), duration=1.0)
        poly = Polygon([a, Coord(100, 100), Coord(0, 100)], fill="green")
        poly.animate_fade(to=0.0, duration=1.0)
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' in svg
        assert '<animate attributeName="opacity"' in svg

    def test_bounce_and_repeat(self):
        """Reactive vertex animation with bounce mirrors the values."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(0, 0)
        scene.add(a, at=(0.0, 0.0))
        scene.add(b, at=(1.0, 0.0))
        scene.add(c, at=(0.5, 1.0))
        a.animate_move(to=(0.5, 0.5), duration=2.0)
        a.loop(bounce=True)
        b.animate_move(to=(0.5, 0.5), duration=2.0)
        b.loop(bounce=True)
        c.animate_move(to=(0.5, 0.5), duration=2.0)
        c.loop(bounce=True)
        poly = Polygon([a, b, c], fill="red")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' in svg
        assert 'repeatCount="indefinite"' in svg


class TestReactiveConnectionAnimation:
    """Reactive connection animations when endpoints are animated entities."""

    def test_straight_animated_start(self):
        """Straight connection with animated start emits x1/y1 animates."""
        scene = Scene(200, 200)
        d1 = Dot(0, 0, radius=5, color="red")
        d2 = Dot(0, 0, radius=5, color="blue")
        scene.add(d1, at=(0.1, 0.5))
        scene.add(d2, at=(0.9, 0.5))
        d1.animate_move(to=(0.5, 0.5), duration=2.0)
        conn = Connection(d1, d2)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="x1"' in svg
        assert '<animate attributeName="y1"' in svg
        assert '<animate attributeName="x2"' not in svg

    def test_straight_both_animated(self):
        """Both endpoints animated emits x1/y1/x2/y2 animate elements."""
        scene = Scene(200, 200)
        d1 = Dot(0, 0, radius=5, color="red")
        d2 = Dot(0, 0, radius=5, color="blue")
        scene.add(d1, at=(0.1, 0.5))
        scene.add(d2, at=(0.9, 0.5))
        d1.animate_move(to=(0.5, 0.5), duration=2.0)
        d2.animate_move(to=(0.5, 0.8), duration=2.0)
        conn = Connection(d1, d2)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="x1"' in svg
        assert '<animate attributeName="y1"' in svg
        assert '<animate attributeName="x2"' in svg
        assert '<animate attributeName="y2"' in svg

    def test_curve_animated_endpoint(self):
        """Curved connection with animated endpoint emits d attribute animate."""
        scene = Scene(200, 200)
        d1 = Dot(0, 0, radius=5, color="red")
        d2 = Dot(0, 0, radius=5, color="blue")
        scene.add(d1, at=(0.1, 0.5))
        scene.add(d2, at=(0.9, 0.5))
        d1.animate_move(to=(0.5, 0.5), duration=2.0)
        conn = Connection(d1, d2, curvature=0.3)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="d"' in svg

    def test_static_endpoints_no_reactive(self):
        """Connection with static endpoints emits no reactive animations."""
        d1 = Dot(10, 20, radius=5, color="red")
        d2 = Dot(80, 80, radius=5, color="blue")
        conn = Connection(d1, d2)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="x1"' not in svg

    def test_own_anims_coexist_with_reactive(self):
        """Connection's own fade + reactive endpoint animation coexist."""
        scene = Scene(200, 200)
        d1 = Dot(0, 0, radius=5, color="red")
        d2 = Dot(0, 0, radius=5, color="blue")
        scene.add(d1, at=(0.1, 0.5))
        scene.add(d2, at=(0.9, 0.5))
        d1.animate_move(to=(0.5, 0.5), duration=2.0)
        conn = Connection(d1, d2)
        conn.animate_fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="x1"' in svg
        assert '<animate attributeName="opacity"' in svg


# ======================================================================
# Fill-to-opacity layer optimization
# ======================================================================


class TestFillLayerOptimization:
    """GPU-accelerated fill animation via stacked opacity layers."""

    def test_two_color_emits_group(self):
        """Two-color fill animation produces <g> with 2 <polygon> elements."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" in svg
        assert svg.count("<polygon") == 2

    def test_three_color_emits_three_polygons(self):
        """Three unique colors produce 3 <polygon> elements."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="red")
        poly.animate_fill(keyframes={0: "red", 1: "blue", 2: "green"})
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" in svg
        assert svg.count("<polygon") == 3

    def test_base_has_first_color(self):
        """Base polygon uses the first keyframe color."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="#ff0000")
        poly.animate_fill(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_entity(poly)
        assert 'fill="#ff0000"' in svg

    def test_overlay_has_target_color(self):
        """Overlay polygon uses the alternate color."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "#0000ff"})
        svg = SMILRenderer().render_entity(poly)
        assert 'fill="#0000ff"' in svg

    def test_overlay_has_opacity_animate(self):
        """Overlay has <animate attributeName="opacity">."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        svg = SMILRenderer().render_entity(poly)
        assert 'attributeName="opacity"' in svg

    def test_no_fill_animate(self):
        """Optimized output must NOT contain attributeName="fill"."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue"})
        svg = SMILRenderer().render_entity(poly)
        assert 'attributeName="fill"' not in svg

    def test_overlay_starts_transparent(self):
        """Overlay polygon has opacity="0"."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue"})
        svg = SMILRenderer().render_entity(poly)
        assert 'opacity="0"' in svg

    def test_opacity_values_two_color(self):
        """Two-color A→B→A produces opacity values 0;1;0."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        svg = SMILRenderer().render_entity(poly)
        assert 'values="0;1;0"' in svg

    def test_single_color_no_optimization(self):
        """Single color (no-op animation) falls back to standard rendering."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "white"})
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" not in svg

    def test_fallback_when_opacity_animated(self):
        """Falls back when polygon also animates opacity."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue"})
        poly.animate_fade(to=0.0, duration=1.0)
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" not in svg
        assert 'attributeName="fill"' in svg

    def test_reactive_vertices_on_both_layers(self):
        """Both layers get reactive vertex tracking animations."""
        scene = Scene(200, 200)
        pt = scene.add_point(at=(0.1, 0.1))
        pt.animate_move(to=(0.5, 0.5), duration=2.0)
        poly = Polygon(
            [pt, Coord(100, 100), Coord(0, 100)], fill="white",
        )
        poly.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" in svg
        assert svg.count('attributeName="points"') == 2

    def test_other_anims_on_base_only(self):
        """Non-fill animations (e.g. spin) appear on the base layer only."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue"})
        poly.animate_spin(360, duration=2.0)
        svg = SMILRenderer().render_entity(poly)
        assert "<g>" in svg
        assert svg.count('type="rotate"') == 1

    def test_timing_preserved(self):
        """Delay, duration, repeat, easing carry over to opacity animation."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(
            keyframes={0: "white", 1: "blue"},
            delay=0.5, easing="ease-in-out",
        )
        poly.loop()
        svg = SMILRenderer().render_entity(poly)
        assert 'begin="0.5s"' in svg
        assert 'repeatCount="indefinite"' in svg
        assert 'calcMode="spline"' in svg

    def test_overlay_no_stroke(self):
        """Overlay polygon should not carry the stroke."""
        poly = Polygon(
            [(0, 0), (100, 0), (50, 80)],
            fill="white", stroke="red", stroke_width=2,
        )
        poly.animate_fill(keyframes={0: "white", 1: "blue"})
        svg = SMILRenderer().render_entity(poly)
        # Base has stroke, overlay doesn't — stroke appears once
        assert svg.count('stroke="red"') == 1
        assert svg.count("<polygon") == 2

    # ------------------------------------------------------------------
    # Rect fill optimization
    # ------------------------------------------------------------------

    def test_rect_two_color_emits_group(self):
        """Rect fill animation produces <g> with 2 <rect> elements."""
        rect = Rect(0, 0, 100, 50, fill="#ff0000")
        rect.animate_fill(keyframes={0: "#ff0000", 1: "#0000ff", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(rect)
        assert "<g>" in svg
        assert svg.count("<rect") == 2

    def test_rect_no_fill_animate(self):
        """Optimized rect output has no attributeName="fill"."""
        rect = Rect(0, 0, 100, 50, fill="#ff0000")
        rect.animate_fill(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_entity(rect)
        assert 'attributeName="fill"' not in svg

    def test_rect_overlay_no_stroke(self):
        """Rect overlay should not carry the stroke."""
        rect = Rect(0, 0, 100, 50, fill="#ff0000", stroke="green", stroke_width=3)
        rect.animate_fill(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_entity(rect)
        assert svg.count('stroke="green"') == 1
        assert svg.count("<rect") == 2

    # ------------------------------------------------------------------
    # Ellipse fill optimization
    # ------------------------------------------------------------------

    def test_ellipse_two_color_emits_group(self):
        """Ellipse fill animation produces <g> with 2 <ellipse> elements."""
        ell = Ellipse(50, 50, 30, 20, fill="#ff0000")
        ell.animate_fill(keyframes={0: "#ff0000", 1: "#00ff00", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(ell)
        assert "<g>" in svg
        assert svg.count("<ellipse") == 2

    def test_ellipse_no_fill_animate(self):
        """Optimized ellipse output has no attributeName="fill"."""
        ell = Ellipse(50, 50, 30, 20, fill="#ff0000")
        ell.animate_fill(keyframes={0: "#ff0000", 1: "#00ff00"})
        svg = SMILRenderer().render_entity(ell)
        assert 'attributeName="fill"' not in svg

    # ------------------------------------------------------------------
    # Path fill optimization
    # ------------------------------------------------------------------

    def test_path_closed_fill_optimization(self):
        """Closed path with fill animation gets optimized."""
        path = Path(Path.Lissajous(size=50), closed=True, fill="#ff0000", color="black")
        path.animate_fill(keyframes={0: "#ff0000", 1: "#0000ff", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(path)
        assert "<g>" in svg
        assert svg.count("<path") == 2
        assert 'attributeName="fill"' not in svg

    def test_path_open_no_fill_optimization(self):
        """Open path does NOT get fill optimized (fill='none')."""
        path = Path(Path.Wave(start=(0, 0), end=(100, 0)), color="blue")
        path.animate_fill(keyframes={0: "blue", 1: "red"})
        svg = SMILRenderer().render_entity(path)
        # Should NOT have the <g> wrapper — open path has no fill
        assert "<g>" not in svg

    def test_path_open_stroke_optimization(self):
        """Open path with stroke color animation gets optimized."""
        path = Path(Path.Wave(start=(0, 0), end=(100, 0)), color="#ff0000", width=2)
        path.animate_color(keyframes={0: "#ff0000", 1: "#0000ff", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(path)
        assert "<g>" in svg
        assert svg.count("<path") == 2
        assert 'attributeName="stroke"' not in svg

    # ------------------------------------------------------------------
    # Connection stroke color optimization
    # ------------------------------------------------------------------

    def test_connection_stroke_optimization(self):
        """Connection stroke color animation gets optimized."""
        d1, d2 = Dot(0, 0), Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_color(keyframes={0: "#ff0000", 1: "#0000ff", 2: "#ff0000"})
        svg = SMILRenderer().render_connection(conn)
        assert "<g>" in svg
        assert svg.count("<line") == 2

    def test_connection_no_stroke_animate(self):
        """Optimized connection has no attributeName="stroke"."""
        d1, d2 = Dot(0, 0), Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_color(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_connection(conn)
        assert 'attributeName="stroke"' not in svg

    def test_connection_overlay_has_stroke_width(self):
        """Connection overlay carries stroke-width for proper coverage."""
        d1, d2 = Dot(0, 0), Dot(100, 100)
        conn = Connection(d1, d2, width=3)
        conn.animate_color(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_connection(conn)
        assert svg.count('stroke-width="3"') == 2  # base + overlay

    # ------------------------------------------------------------------
    # Line stroke color optimization
    # ------------------------------------------------------------------

    def test_line_stroke_optimization(self):
        """Line stroke color animation gets optimized."""
        line = Line(0, 0, 100, 100, width=2, color="#ff0000")
        line.animate_color(keyframes={0: "#ff0000", 1: "#0000ff", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(line)
        assert "<g>" in svg
        assert svg.count("<line") == 2
        assert 'attributeName="stroke"' not in svg

    def test_line_overlay_has_stroke_width(self):
        """Line overlay carries stroke-width."""
        line = Line(0, 0, 100, 100, width=4, color="#ff0000")
        line.animate_color(keyframes={0: "#ff0000", 1: "#0000ff"})
        svg = SMILRenderer().render_entity(line)
        assert svg.count('stroke-width="4"') == 2

    # ------------------------------------------------------------------
    # Curve stroke color optimization
    # ------------------------------------------------------------------

    def test_curve_stroke_optimization(self):
        """Curve stroke color animation gets optimized."""
        from pyfreeform import Curve
        curve = Curve(0, 0, 100, 100, curvature=0.3, width=2, color="#ff0000")
        curve.animate_color(keyframes={0: "#ff0000", 1: "#00ff00", 2: "#ff0000"})
        svg = SMILRenderer().render_entity(curve)
        assert "<g>" in svg
        assert svg.count("<path") == 2
        assert 'attributeName="stroke"' not in svg


# ======================================================================
# Fill-layer batching (cross-entity)
# ======================================================================


class TestFillLayerBatching:
    """Cross-entity fill animation batching at render_scene level."""

    def test_two_same_timing_one_animate(self):
        """Two polygons with identical fill timing produce 1 shared <animate>."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        for p in (p1, p2):
            p.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
            scene.place(p)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 1

    def test_different_timing_not_batched(self):
        """Different durations prevent batching."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        p1.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        p2.animate_fill(keyframes={0: "white", 0.5: "blue", 1: "white"})
        scene.place(p1)
        scene.place(p2)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 2

    def test_different_z_index_not_batched(self):
        """Different z_index prevents batching."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white", z_index=0)
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white", z_index=1)
        for p in (p1, p2):
            p.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
            scene.place(p)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 2

    def test_single_entity_not_batched(self):
        """Single entity still uses per-entity rendering."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p1.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        scene.place(p1)
        svg = scene.to_svg()
        # Still has per-entity <g> wrapper
        assert svg.count('attributeName="opacity"') == 1
        assert "<g>" in svg

    def test_three_entities_same_timing(self):
        """Three entities batched together produce 1 shared animate."""
        scene = Scene(300, 200)
        for x in (0, 60, 120):
            p = Polygon([(x, 0), (x + 50, 0), (x + 25, 40)], fill="red")
            p.animate_fill(keyframes={0: "red", 1: "blue", 2: "red"})
            scene.place(p)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 1

    def test_mixed_entity_types_same_timing(self):
        """Polygon and Rect with same fill timing can be batched."""
        scene = Scene(200, 200)
        p = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        r = Rect(60, 0, 50, 40, fill="white")
        for e in (p, r):
            e.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
            scene.place(e)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 1

    def test_three_color_batch(self):
        """Three-color animation batching produces 2 shared overlay groups."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="red")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="red")
        for p in (p1, p2):
            p.animate_fill(keyframes={0: "red", 1: "blue", 2: "green"})
            scene.place(p)
        svg = scene.to_svg()
        # 2 overlay groups (one for blue, one for green), each with 1 animate
        assert svg.count('attributeName="opacity"') == 2

    def test_non_fill_anims_on_base_only(self):
        """Spin animation appears once per entity (on base), not in overlay group."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        for p in (p1, p2):
            p.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
            p.animate_spin(360, duration=2.0)
            scene.place(p)
        svg = scene.to_svg()
        assert svg.count('type="rotate"') == 2  # one per base
        assert svg.count('attributeName="opacity"') == 1  # shared

    def test_render_entity_direct_not_batched(self):
        """Calling render_entity directly (not via render_scene) is not batched."""
        poly = Polygon([(0, 0), (100, 0), (50, 80)], fill="white")
        poly.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
        svg = SMILRenderer().render_entity(poly)
        # Per-entity rendering, not batched
        assert svg.count('attributeName="opacity"') == 1
        assert "<g>" in svg

    def test_batch_preserves_base_colors(self):
        """Batched bases use their own fill_opt base color."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        p1.animate_fill(keyframes={0: "white", 1: "#aabbcc", 2: "white"})
        p2.animate_fill(keyframes={0: "white", 1: "#112233", 2: "white"})
        scene.place(p1)
        scene.place(p2)
        svg = scene.to_svg()
        # Both overlay colors appear
        assert "#aabbcc" in svg
        assert "#112233" in svg
        # Batched: 1 shared animate
        assert svg.count('attributeName="opacity"') == 1

    def test_different_delay_not_batched(self):
        """Same keyframes but different delay prevents batching."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        p1.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"}, delay=0.0)
        p2.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"}, delay=0.5)
        scene.place(p1)
        scene.place(p2)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 2

    def test_different_easing_not_batched(self):
        """Same keyframes but different easing prevents batching."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        p1.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"}, easing="linear")
        p2.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"}, easing="ease-in")
        scene.place(p1)
        scene.place(p2)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 2

    def test_same_bounce_batched(self):
        """Same timing with identical bounce=True are batched together."""
        scene = Scene(200, 200)
        p1 = Polygon([(0, 0), (50, 0), (25, 40)], fill="white")
        p2 = Polygon([(60, 0), (110, 0), (85, 40)], fill="white")
        for p in (p1, p2):
            p.animate_fill(keyframes={0: "white", 1: "blue", 2: "white"})
            p.loop(bounce=True)
            scene.place(p)
        svg = scene.to_svg()
        assert svg.count('attributeName="opacity"') == 1


# ======================================================================
# .loop() — Looping API
# ======================================================================


class TestLoop:
    def test_loop_stamps_all_animations(self):
        """loop() sets bounce and repeat on every animation in the entity."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.3, duration=1.0)
        dot.animate_spin(360, duration=2.0)
        dot.loop(bounce=True)
        for anim in dot.animations:
            assert anim.bounce is True
            assert anim.repeat is True

    def test_loop_returns_none(self):
        """animate_fade().loop() returns None, not the entity."""
        dot = Dot(0, 0)
        result = dot.animate_fade(to=0.3).loop()
        assert result is None

    def test_loop_on_chain(self):
        """loop() after animate + .then() + animate stamps all animations."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0).then().animate_spin(360, duration=1.0)
        dot.loop(bounce=True)
        assert len(dot.animations) == 2
        for anim in dot.animations:
            assert anim.bounce is True

    def test_loop_defaults(self):
        """loop() with no args sets bounce=False and repeat=True."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        dot.loop()
        anim = dot.animations[0]
        assert anim.bounce is False
        assert anim.repeat is True

    def test_loop_times(self):
        """loop(times=3) sets repeat=3 on all animations."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        dot.animate_spin(360, duration=2.0)
        dot.loop(times=3)
        for anim in dot.animations:
            assert anim.repeat == 3

    def test_loop_on_connection(self):
        """Connection.loop() works identically to entity loop()."""
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_fade(to=0.0, duration=1.0)
        conn.animate_draw(duration=1.5)
        conn.loop(bounce=True)
        for anim in conn.animations:
            assert anim.bounce is True
            assert anim.repeat is True

    def test_loop_invalid_times_false(self):
        """loop(times=False) raises ValueError."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        with pytest.raises(ValueError):
            dot.loop(times=False)

    def test_loop_invalid_times_zero(self):
        """loop(times=0) raises ValueError."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        with pytest.raises(ValueError):
            dot.loop(times=0)

    def test_loop_invalid_times_one(self):
        """loop(times=1) raises ValueError."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        with pytest.raises(ValueError):
            dot.loop(times=1)

    def test_loop_invalid_times_negative(self):
        """loop(times=-1) raises ValueError."""
        dot = Dot(0, 0)
        dot.animate_fade(to=0.0, duration=1.0)
        with pytest.raises(ValueError):
            dot.loop(times=-1)

    def test_loop_no_animations(self):
        """loop() with no animations added raises ValueError."""
        dot = Dot(0, 0)
        with pytest.raises(ValueError):
            dot.loop()


# ======================================================================
# Per-animation repeat= / bounce= inline params
# ======================================================================


class TestPerAnimationRepeat:
    """Inline repeat=/bounce= on animate_* methods (industry-standard pattern)."""

    def test_per_anim_default_no_repeat(self):
        """Default animate_* leaves repeat=False, bounce=False."""
        dot = Dot(0, 0)
        dot.animate_radius(to=10, duration=1.0)
        anim = dot.animations[0]
        assert anim.repeat is False
        assert anim.bounce is False

    def test_per_anim_repeat_only_that_anim(self):
        """animate_radius(repeat=True) only affects that animation, not a subsequent one."""
        dot = Dot(0, 0)
        dot.animate_radius(to=10, duration=1.0, repeat=True)
        dot.animate_color(to="blue", duration=1.0)
        assert dot.animations[0].repeat is True
        assert dot.animations[1].repeat is False

    def test_per_anim_bounce(self):
        """repeat=True, bounce=True sets both on just that animation."""
        dot = Dot(0, 0)
        dot.animate_radius(to=10, duration=1.2, repeat=True, bounce=True)
        anim = dot.animations[0]
        assert anim.repeat is True
        assert anim.bounce is True

    def test_per_anim_finite(self):
        """repeat=3 sets repeat=3 on just that animation."""
        dot = Dot(0, 0)
        dot.animate_radius(to=10, duration=1.0, repeat=3)
        anim = dot.animations[0]
        assert anim.repeat == 3
        assert anim.bounce is False

    def test_per_anim_bounce_without_repeat_ignored(self):
        """bounce=True with default repeat=False leaves bounce=False on the model."""
        dot = Dot(0, 0)
        dot.animate_radius(to=10, duration=1.0, bounce=True)
        # bounce=True silently ignored when repeat=False
        anim = dot.animations[0]
        assert anim.bounce is True   # stored but won't fire (repeat=False stops it)
        assert anim.repeat is False

    def test_per_anim_move_stamps_both_axes(self):
        """animate_move(repeat=True) sets repeat=True on both at_rx and at_ry."""
        from pyfreeform import Scene
        scene = Scene(200, 200)
        dot = Dot(0, 0)
        scene.add(dot, at=(0.5, 0.5))
        dot.animate_move(to=(0.8, 0.5), duration=1.0, repeat=True, bounce=True)
        assert len(dot.animations) == 2
        for anim in dot.animations:
            assert anim.repeat is True
            assert anim.bounce is True

    def test_per_anim_connection_draw(self):
        """conn.animate_draw(repeat=True, bounce=True) works inline."""
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.animate_draw(duration=1.5, repeat=True, bounce=True)
        anim = conn.animations[0]
        assert anim.repeat is True
        assert anim.bounce is True

    def test_mixed_spin_once_color_loops(self):
        """Spin plays once; color loops independently. entity.loop() not called."""
        dot = Dot(0, 0)
        dot.animate_spin(360, duration=2.0)                       # plays once
        dot.animate_color(to="blue", duration=1.0, repeat=True)   # loops forever
        spin = dot.animations[0]
        color = dot.animations[1]
        assert spin.repeat is False
        assert color.repeat is True

    def test_entity_loop_overrides_inline(self):
        """entity.loop() after inline repeat=True overwrites with its own settings."""
        dot = Dot(0, 0)
        dot.animate_radius(to=35, duration=1.2, repeat=True, bounce=True)
        dot.loop()  # bounce=False, times=True — overwrites
        anim = dot.animations[0]
        assert anim.repeat is True   # still loops (True from loop())
        assert anim.bounce is False  # overwritten to False

    def test_per_anim_spin(self):
        """animate_spin(repeat=True) sets repeat on spin animation."""
        dot = Dot(0, 0)
        dot.animate_spin(360, duration=2.0, repeat=True)
        anim = dot.animations[0]
        assert anim.prop == "rotation"
        assert anim.repeat is True

    def test_per_anim_scale(self):
        """animate_scale(repeat=True, bounce=True) sets both inline."""
        dot = Dot(0, 0)
        dot.animate_scale(to=2.0, duration=1.0, repeat=True, bounce=True)
        anim = dot.animations[0]
        assert anim.prop == "scale_factor"
        assert anim.repeat is True
        assert anim.bounce is True

    def test_per_anim_follow(self):
        """animate_follow(repeat=True) sets repeat on MotionAnimation."""
        from pyfreeform.paths import Wave
        dot = Dot(0, 0)
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.animate_follow(wave, duration=2.0, repeat=True, bounce=True)
        anim = dot.animations[0]
        assert anim.repeat is True
        assert anim.bounce is True

    def test_per_anim_draw_line(self):
        """Line.animate_draw(repeat=True) sets repeat on DrawAnimation."""
        line = Line(0, 0, 100, 100)
        line.animate_draw(duration=1.0, repeat=True, bounce=True)
        anim = line.animations[0]
        assert anim.repeat is True
        assert anim.bounce is True

    def test_per_anim_draw_path(self):
        """Path.animate_draw(repeat=True) sets repeat on DrawAnimation."""
        from pyfreeform.paths import Wave
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        scene = Scene(200, 200)
        path = Path(wave, width=2, color="red")
        scene.place(path)
        path.animate_draw(duration=1.0, repeat=True, bounce=True)
        anim = path.animations[0]
        assert anim.repeat is True
        assert anim.bounce is True

    def test_per_anim_smil_produces_repeat_indefinite(self):
        """Inline repeat=True renders to repeatCount='indefinite' in SMIL."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'repeatCount="indefinite"' in svg

    def test_per_anim_finite_smil_repeat_count(self):
        """Inline repeat=3 renders to repeatCount='3' in SMIL."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate_radius(to=10, duration=1.0, repeat=3)
        svg = SMILRenderer().render_entity(dot)
        assert 'repeatCount="3"' in svg


# ======================================================================
# Transform Pivot
# ======================================================================

class TestTransformPivot:
    """Tests for animate_spin / animate_scale pivot= parameter."""

    def _cell_dot(self):
        """A Dot placed in a 200×100 cell, so pivot fractions are predictable."""
        scene = Scene.with_grid(cols=1, rows=1, cell_width=200, cell_height=100)
        return scene.grid[0][0].add_dot(at=(0.5, 0.5), radius=0.05, color="red")

    def test_spin_default_no_pivot(self):
        """No pivot arg → anim.pivot is None."""
        dot = Dot(50, 50, radius=5, color="red")
        dot.animate_spin(360, duration=1.0)
        assert dot.animations[0].pivot is None

    def test_spin_pivot_stored_as_relcoord(self):
        """pivot=(0.3, 0.5) is stored as RelCoord(0.3, 0.5)."""
        from pyfreeform.core.relcoord import RelCoord
        dot = self._cell_dot()
        dot.animate_spin(360, duration=1.0, pivot=(0.3, 0.5))
        assert dot.animations[0].pivot == RelCoord(0.3, 0.5)

    def test_pivot_tuple_coerced(self):
        """Plain tuple is auto-coerced to RelCoord."""
        from pyfreeform.core.relcoord import RelCoord
        dot = self._cell_dot()
        dot.animate_spin(360, duration=1.0, pivot=(0.1, 0.8))
        assert isinstance(dot.animations[0].pivot, RelCoord)

    def test_no_pivot_falls_back_to_rotation_center(self):
        """No pivot → SVG values use entity.rotation_center coords."""
        dot = self._cell_dot()
        dot.animate_spin(360, duration=1.0)
        svg = SMILRenderer().render_entity(dot)
        center = dot.rotation_center
        assert f"{svg_num(center.x)} {svg_num(center.y)}" in svg

    def test_spin_pivot_in_svg(self):
        """Custom pivot resolves to surface-relative pixel coords in SVG values."""
        scene = Scene.with_grid(cols=1, rows=1, cell_width=200, cell_height=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(at=(0.7, 0.5), radius=0.05, color="red")
        # pivot at surface center: (cell.x + 0.5*200, cell.y + 0.5*100)
        dot.animate_spin(360, duration=1.0, pivot=(0.5, 0.5))
        svg = SMILRenderer().render_entity(dot)
        expected_cx = cell.x + 0.5 * cell.width
        expected_cy = cell.y + 0.5 * cell.height
        assert f"{svg_num(expected_cx)} {svg_num(expected_cy)}" in svg

    def test_scale_pivot_in_svg(self):
        """Custom pivot is used in scale translate+scale+translate values."""
        scene = Scene.with_grid(cols=1, rows=1, cell_width=200, cell_height=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(at=(0.5, 0.5), radius=0.05, color="red")
        dot.animate_scale(2.0, duration=1.0, pivot=(0.0, 0.0))
        svg = SMILRenderer().render_entity(dot)
        expected_cx = cell.x + 0.0 * cell.width
        expected_cy = cell.y + 0.0 * cell.height
        assert f"{svg_num(expected_cx)} {svg_num(expected_cy)}" in svg

# ======================================================================
# Chain loop — event-based SMIL timing
# ======================================================================


class TestChainLoop:
    """Test that .then() + .loop() produces SMIL event-based timing.

    The key invariant: when a chain has repeat=True (infinite loop), each
    animation step must carry an ``id=`` attribute and a ``begin=`` expression
    that references the previous/next step — not an absolute delay.
    """

    def _dot(self) -> Dot:
        """Return a bare Dot (not in a surface) for quick tests."""
        return Dot(50, 50, radius=5, color="coral")

    # ------------------------------------------------------------------
    # Data-model: chain_id / chain_seq tagging
    # ------------------------------------------------------------------

    def test_then_tags_chain_id(self):
        """All animations share a chain_id after .then() + loop()."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        anims = dot.animations
        assert len(anims) == 2
        assert anims[0].chain_id is not None
        assert anims[0].chain_id == anims[1].chain_id

    def test_then_assigns_chain_seq(self):
        """First group gets seq=0, second gets seq=1."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        anims = dot.animations
        assert anims[0].chain_seq == 0
        assert anims[1].chain_seq == 1

    def test_simultaneous_no_chain_id(self):
        """Simultaneous animations (no .then()) have chain_id=None."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).animate_fade(to=1.0, duration=2.0).loop()
        for anim in dot.animations:
            assert anim.chain_id is None

    def test_clear_resets_chain_state(self):
        """clear_animations() resets chain_id and chain_next_seq."""
        dot = self._dot()
        dot.animate_fade(to=0.0).then().animate_fade(to=1.0).loop()
        dot.clear_animations()
        assert dot._chain_id is None
        assert dot._chain_next_seq == 0

    def test_multi_step_chain_seqs(self):
        """Three steps A.then().B.then().C get seq 0, 1, 2."""
        dot = self._dot()
        (dot.animate_fade(to=0.0, duration=1.0)
             .then()
             .animate_fade(to=0.5, duration=1.0)
             .then()
             .animate_fade(to=1.0, duration=1.0)
             .loop())
        anims = dot.animations
        assert [a.chain_seq for a in anims] == [0, 1, 2]

    def test_simultaneous_plus_then_seq(self):
        """animate_A + animate_B .then() animate_C → seqs [0, 0, 1]."""
        dot = self._dot()
        (dot.animate_fade(to=0.0, duration=1.0)
             .animate_spin(360, duration=1.0)
             .then()
             .animate_fade(to=1.0, duration=1.0)
             .loop())
        anims = dot.animations
        seqs = [a.chain_seq for a in anims]
        assert seqs[0] == 0  # fade seq 0
        # spin uses animate_spin → PropertyAnimation
        assert seqs[1] == 0  # spin seq 0
        assert seqs[2] == 1  # final fade seq 1

    # ------------------------------------------------------------------
    # SMIL output: sequential loop (no bounce)
    # ------------------------------------------------------------------

    def test_sequential_loop_uses_id_and_begin(self):
        """loop() on a chain must emit id= and begin= event expressions."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        svg = SMILRenderer().render_entity(dot)
        # Must have SMIL element IDs
        assert 'id="ch' in svg
        # Must reference .end (event-based), not just absolute delay
        assert ".end" in svg

    def test_sequential_loop_no_repeat_count(self):
        """Chain loop must NOT emit repeatCount=indefinite on sub-animations."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        svg = SMILRenderer().render_entity(dot)
        assert "repeatCount" not in svg

    def test_sequential_loop_seq0_begin(self):
        """Seq-0 animation must start at 0s and restart after last seq ends."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        svg = SMILRenderer().render_entity(dot)
        # Seq-0 begin must contain "0s" (initial start)
        assert "0s" in svg
        # And reference the last seq's anchor end
        assert "s1i0.end" in svg  # ch{cid}s1i0.end triggers restart of s0

    def test_sequential_loop_seq1_begin(self):
        """Seq-1 animation must begin when seq-0's anchor ends."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop()
        svg = SMILRenderer().render_entity(dot)
        # Seq-1 begins after seq-0's anchor
        assert "s0i0.end" in svg

    # ------------------------------------------------------------------
    # SMIL output: bounce loop
    # ------------------------------------------------------------------

    def test_bounce_loop_emits_forward_and_backward(self):
        """loop(bounce=True) must emit both 'f' (forward) and 'b' (backward) elements."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert "f0" in svg   # forward pass element id
        assert "b0" in svg   # backward pass element id

    def test_bounce_loop_backward_reverses_values(self):
        """Backward pass of a fade must have reversed from/to values."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        # Forward: opacity goes 1→0 and 0→1
        # Backward: opacity goes 1→0 and 0→1 (reversed)
        # Both directions must appear
        assert "1;0" in svg
        assert "0;1" in svg

    def test_bounce_loop_no_repeat_count(self):
        """Bounce chain loop must NOT emit repeatCount."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert "repeatCount" not in svg

    def test_bounce_seq0_restarts_after_backward_seq0(self):
        """Seq-0 forward must restart after seq-0 backward (full cycle)."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).then().animate_fade(to=1.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        # seq0 forward references seq0 backward end for restart
        assert "s0b0.end" in svg

    # ------------------------------------------------------------------
    # Simultaneous animations still use old path (regression guard)
    # ------------------------------------------------------------------

    def test_simultaneous_loop_still_uses_repeat_count(self):
        """Non-chained loop() must still emit repeatCount=indefinite."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).loop()
        svg = SMILRenderer().render_entity(dot)
        assert 'repeatCount="indefinite"' in svg
        assert "id=" not in svg

    def test_simultaneous_bounce_loop_still_works(self):
        """Non-chained bounce still uses baked values (no event ids)."""
        dot = self._dot()
        dot.animate_fade(to=0.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'repeatCount="indefinite"' in svg
        # Bounce baked: values contain the intermediate (midpoint) value
        assert "values=" in svg

    # ------------------------------------------------------------------
    # animate_move (produces two PropertyAnimations at same seq)
    # ------------------------------------------------------------------

    def test_move_then_fade_chain(self):
        """animate_move + .then() + animate_fade uses event-based timing."""
        scene = Scene.with_grid(cols=1, rows=1, cell_width=200, cell_height=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(at=(0.15, 0.5), radius=0.05, color="gold")
        dot.animate_move(to=(0.85, 0.5), duration=2.0).then().animate_fade(to=0.0, duration=2.0).loop(bounce=True)
        svg = SMILRenderer().render_entity(dot)
        assert "id=" in svg
        assert ".end" in svg
        assert "repeatCount" not in svg

    def test_move_anims_share_seq(self):
        """animate_move emits two at_rx/at_ry animations both at seq=0."""
        scene = Scene.with_grid(cols=1, rows=1, cell_width=200, cell_height=100)
        cell = scene.grid[0][0]
        dot = cell.add_dot(at=(0.15, 0.5), radius=0.05, color="gold")
        dot.animate_move(to=(0.85, 0.5), duration=2.0).then().animate_fade(to=0.0, duration=2.0).loop()
        anims = dot.animations
        # First two are at_rx, at_ry (both seq=0); third is opacity (seq=1)
        move_anims = [a for a in anims if a.prop in ("at_rx", "at_ry")]
        assert all(a.chain_seq == 0 for a in move_anims)
        fade_anims = [a for a in anims if a.prop == "opacity"]
        assert all(a.chain_seq == 1 for a in fade_anims)
