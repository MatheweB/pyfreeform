"""Tests for the animation system — models, builders, and SMIL rendering."""

from __future__ import annotations

import pytest

from pyfreeform import Dot, Easing, Ellipse, Line, Polygon, Rect, Scene, Path, Text, Connection, stagger
from pyfreeform.core.coord import Coord
from pyfreeform.entities.point import Point
from pyfreeform.animation.models import (
    DrawAnimation,
    Easing,
    Keyframe,
    MotionAnimation,
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
        anim = build_spin(dot, angle=360, duration=3.0, repeat=True)
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
        result = dot.fade(to=0.0, duration=1.0)
        assert result is dot

    def test_fade_adds_animation(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "opacity"

    def test_chaining(self):
        dot = Dot(0, 0)
        dot.fade(to=0.5, duration=1.0).spin(360, duration=2.0)
        assert len(dot.animations) == 2

    def test_clear_animations(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0).spin(360)
        assert len(dot.animations) == 2
        dot.clear_animations()
        assert len(dot.animations) == 0

    def test_generic_animate(self):
        dot = Dot(0, 0, radius=5)
        dot.animate("r", to=20, duration=1.5)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "r"

    def test_spin(self):
        rect = Rect(0, 0, 100, 100)
        rect.spin(360, duration=2.0, repeat=True)
        assert len(rect.animations) == 1
        assert rect.animations[0].prop == "rotation"


# ======================================================================
# Path draw animation
# ======================================================================


class TestPathDraw:
    def test_path_draw(self):
        from pyfreeform.paths import Wave

        p = Path(Wave(), width=2, color="blue")
        result = p.draw(duration=2.0)
        assert result is p
        assert len(p.animations) == 1
        assert isinstance(p.animations[0], DrawAnimation)


# ======================================================================
# Connection animation API
# ======================================================================


class TestConnectionAnimation:
    def test_connection_fade(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        result = conn.fade(to=0.0, duration=1.0)
        assert result is conn
        assert len(conn.animations) == 1

    def test_connection_draw(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.draw(duration=1.5)
        assert len(conn.animations) == 1
        assert isinstance(conn.animations[0], DrawAnimation)

    def test_connection_clear(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.fade(to=0.0).draw(duration=1.0)
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
        dot.fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_entity(dot)
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg
        assert 'dur="2.0s"' in svg

    def test_spin_produces_animate_transform(self):
        rect = Rect(0, 0, 100, 100)
        rect.spin(360, duration=3.0, repeat=True)
        svg = SMILRenderer().render_entity(rect)
        assert "animateTransform" in svg
        assert 'type="rotate"' in svg
        assert 'repeatCount="indefinite"' in svg

    def test_draw_produces_dashoffset(self):
        from pyfreeform.paths import Wave

        p = Path(Wave(), width=2, color="blue")
        p.draw(duration=2.0)
        svg = SMILRenderer().render_entity(p)
        assert "stroke-dasharray" in svg
        assert "stroke-dashoffset" in svg
        assert "<animate" in svg

    def test_easing_produces_key_splines(self):
        dot = Dot(10, 20)
        dot.fade(to=0.0, duration=1.0, easing="ease-in-out")
        svg = SMILRenderer().render_entity(dot)
        assert 'calcMode="spline"' in svg
        assert "keySplines" in svg

    def test_hold_produces_fill_freeze(self):
        dot = Dot(10, 20)
        dot.fade(to=0.0, duration=1.0, hold=True)
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
        dot.fade(to=0.0, duration=2.0)
        svg = scene.to_svg()
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg


# ======================================================================
# .then() — Sequential chaining
# ======================================================================


class TestThen:
    def test_basic_chaining(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then().spin(360, duration=1.0)
        assert len(dot.animations) == 2
        fade_anim = dot.animations[0]
        spin_anim = dot.animations[1]
        assert fade_anim.delay == 0.0
        assert spin_anim.delay == pytest.approx(1.0)

    def test_gap_parameter(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then(0.5).spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        assert spin_anim.delay == pytest.approx(1.5)

    def test_no_animations(self):
        dot = Dot(0, 0)
        result = dot.then()
        assert result is dot
        # Chain delay should be 0 — next animation starts immediately
        dot.fade(to=0.0, duration=1.0)
        assert dot.animations[0].delay == 0.0

    def test_repeat_finite(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0, repeat=3).then().spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        # repeat=3 means 3 cycles × 1.0s = 3.0s total
        assert spin_anim.delay == pytest.approx(3.0)

    def test_repeat_infinite(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0, repeat=True).then().spin(360, duration=1.0)
        spin_anim = dot.animations[1]
        # repeat=True: use single cycle duration (pragmatic fallback)
        assert spin_anim.delay == pytest.approx(1.0)

    def test_multi_then(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then().spin(360, duration=2.0).then().fade(to=1.0, duration=0.5)
        anims = dot.animations
        assert anims[0].delay == pytest.approx(0.0)   # fade
        assert anims[1].delay == pytest.approx(1.0)   # spin
        assert anims[2].delay == pytest.approx(3.0)   # fade back (1.0 + 2.0)

    def test_with_explicit_delay(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then().spin(360, duration=1.0, delay=0.5)
        spin_anim = dot.animations[1]
        # Chain delay 1.0 + explicit delay 0.5 = 1.5
        assert spin_anim.delay == pytest.approx(1.5)

    def test_returns_self(self):
        dot = Dot(0, 0)
        result = dot.fade(to=0.0).then()
        assert result is dot

    def test_connection_then(self):
        d1 = Dot(0, 0)
        d2 = Dot(100, 100)
        conn = Connection(d1, d2)
        conn.draw(duration=1.5).then().fade(to=0.0, duration=0.5)
        draw_anim = conn.animations[0]
        fade_anim = conn.animations[1]
        assert draw_anim.delay == 0.0
        assert fade_anim.delay == pytest.approx(1.5)

    def test_clear_resets_chain_delay(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then()
        dot.clear_animations()
        dot.fade(to=0.5, duration=1.0)
        assert dot.animations[0].delay == 0.0

    def test_chain_delay_consumed_once(self):
        dot = Dot(0, 0)
        dot.fade(to=0.0, duration=1.0).then()
        dot.spin(360, duration=1.0)  # consumes chain delay
        dot.fade(to=1.0, duration=1.0)  # no chain delay left
        assert dot.animations[1].delay == pytest.approx(1.0)
        assert dot.animations[2].delay == pytest.approx(0.0)


# ======================================================================
# stagger()
# ======================================================================


class TestStagger:
    def test_basic_stagger(self):
        dots = [Dot(i * 10, 0) for i in range(5)]
        result = stagger(*dots, offset=0.2, each=lambda d: d.fade(to=0.0, duration=1.0))
        assert result is not dots  # returns new list
        assert len(result) == 5
        for i, dot in enumerate(result):
            assert len(dot.animations) == 1
            assert dot.animations[0].delay == pytest.approx(i * 0.2)

    def test_custom_offset(self):
        dots = [Dot(0, 0), Dot(10, 0), Dot(20, 0)]
        stagger(*dots, offset=0.5, each=lambda d: d.fade(to=0.0))
        assert dots[0].animations[0].delay == pytest.approx(0.0)
        assert dots[1].animations[0].delay == pytest.approx(0.5)
        assert dots[2].animations[0].delay == pytest.approx(1.0)

    def test_multiple_animations_per_entity(self):
        dots = [Dot(0, 0), Dot(10, 0)]
        stagger(*dots, offset=0.3, each=lambda d: d.fade(to=0.0).spin(360))
        # Both fade and spin should get stagger offset
        assert dots[0].animations[0].delay == pytest.approx(0.0)
        assert dots[0].animations[1].delay == pytest.approx(0.0)
        assert dots[1].animations[0].delay == pytest.approx(0.3)
        assert dots[1].animations[1].delay == pytest.approx(0.3)

    def test_preserves_explicit_delay(self):
        dots = [Dot(0, 0), Dot(10, 0)]
        stagger(*dots, offset=0.2, each=lambda d: d.fade(to=0.0, delay=0.5))
        # dot[0]: 0.5 + 0*0.2 = 0.5
        # dot[1]: 0.5 + 1*0.2 = 0.7
        assert dots[0].animations[0].delay == pytest.approx(0.5)
        assert dots[1].animations[0].delay == pytest.approx(0.7)


# ======================================================================
# .move(by=)
# ======================================================================


class TestMoveBy:
    def test_move_by_basic(self):
        dot = Dot(0, 0)
        dot.move(by=(0.1, 0.2), duration=1.0)
        # Should have 2 animations (at_rx, at_ry)
        assert len(dot.animations) == 2

    def test_move_to_still_works(self):
        dot = Dot(0, 0)
        dot.move(to=(0.8, 0.5), duration=1.0)
        assert len(dot.animations) == 2

    def test_move_positional_to(self):
        dot = Dot(0, 0)
        dot.move((0.8, 0.5), duration=1.0)
        assert len(dot.animations) == 2

    def test_move_to_and_by_error(self):
        dot = Dot(0, 0)
        with pytest.raises(ValueError, match="Cannot specify both"):
            dot.move(to=(0.5, 0.5), by=(0.1, 0))

    def test_move_neither_error(self):
        dot = Dot(0, 0)
        with pytest.raises(ValueError, match="Must specify either"):
            dot.move(duration=1.0)

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
# .zoom()
# ======================================================================


class TestZoom:
    def test_zoom_returns_self(self):
        dot = Dot(0, 0)
        result = dot.zoom(to=2.0, duration=1.0)
        assert result is dot

    def test_zoom_adds_animation(self):
        dot = Dot(0, 0)
        dot.zoom(to=2.0)
        assert len(dot.animations) == 1
        assert dot.animations[0].prop == "scale_factor"

    def test_zoom_keyframes(self):
        dot = Dot(0, 0)
        dot.zoom(to=2.0, duration=1.5)
        anim = dot.animations[0]
        assert anim.keyframes[0].value == pytest.approx(1.0)
        assert anim.keyframes[1].value == pytest.approx(2.0)
        assert anim.duration == pytest.approx(1.5)

    def test_zoom_pulse(self):
        dot = Dot(0, 0)
        dot.zoom(to=1.5, bounce=True, repeat=True, duration=0.8)
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

    def test_zoom_smil_output(self):
        dot = Dot(10, 20, radius=5, color="red")
        dot.zoom(to=2.0, duration=1.0)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        assert 'type="scale"' in svg

    def test_zoom_with_then(self):
        dot = Dot(0, 0)
        dot.fade(to=0.5, duration=1.0).then().zoom(to=2.0, duration=0.5)
        zoom_anim = dot.animations[1]
        assert zoom_anim.delay == pytest.approx(1.0)


# ======================================================================
# Bounce SMIL rendering
# ======================================================================


class TestBounceSMIL:
    """Test that bounce=True produces correct SMIL output."""

    def test_property_bounce_values_mirrored(self):
        """bounce=True mirrors values: A;B → A;B;A."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate("r", to=10, duration=1.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'values="5;10;5"' in svg

    def test_property_bounce_keytimes(self):
        """bounce=True produces keyTimes 0;0.5;1."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate("r", to=10, duration=1.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'keyTimes="0;0.5;1"' in svg

    def test_property_bounce_doubled_splines(self):
        """bounce=True doubles keySplines for 2 segments."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate("r", to=10, duration=1.0, bounce=True, repeat=True,
                     easing="ease-in-out")
        svg = SMILRenderer().render_entity(dot)
        # 2 segments (3 values) → 2 keySplines
        assert 'keySplines="0.42 0.0 0.58 1.0;0.42 0.0 0.58 1.0"' in svg

    def test_property_no_bounce_unchanged(self):
        """Without bounce, values stay as-is."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate("r", to=10, duration=1.0, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'values="5;10"' in svg
        assert 'keyTimes="0;1"' in svg

    def test_motion_bounce_keypoints(self):
        """bounce=True on follow() adds keyPoints='0;1;0'."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.follow(wave, duration=2.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert 'keyPoints="0;1;0"' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_motion_no_bounce_no_keypoints(self):
        """Without bounce, no keyPoints on animateMotion."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.follow(wave, duration=2.0, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert "keyPoints" not in svg

    def test_motion_bounce_eased(self):
        """bounce + easing produces 2 keySplines on animateMotion."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.follow(wave, duration=2.0, bounce=True, repeat=True,
                   easing="ease-in-out")
        svg = SMILRenderer().render_entity(dot)
        assert 'keySplines="0.42 0.0 0.58 1.0;0.42 0.0 0.58 1.0"' in svg

    def test_motion_bounce_linear_uses_linear_calcmode(self):
        """bounce + linear easing uses calcMode='linear'."""
        from pyfreeform.paths import Wave
        dot = Dot(10, 20, radius=5, color="red")
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        dot.follow(wave, duration=2.0, bounce=True, repeat=True,
                   easing="linear")
        svg = SMILRenderer().render_entity(dot)
        assert 'calcMode="linear"' in svg
        assert "keySplines" not in svg

    def test_draw_bounce_values(self):
        """bounce=True on draw() produces forward-then-reverse dashoffset."""
        from pyfreeform.paths import Wave
        wave = Wave(start=(0, 0), end=(100, 0), amplitude=30, frequency=2)
        path = Path(wave, width=2, color="red")
        scene = Scene(200, 200)
        scene.place(path)
        path.draw(duration=2.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(path)
        # Should have 3 values (forward;peak;forward) for dashoffset
        assert 'values="' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_rotation_bounce(self):
        """bounce=True on spin mirrors rotation values."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.spin(90, duration=1.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        # Should have 3 values for rotation (forward;peak;back)
        assert 'keyTimes="0;0.5;1"' in svg

    def test_scale_bounce(self):
        """bounce=True on zoom mirrors scale values."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.zoom(to=2.0, duration=1.0, bounce=True, repeat=True)
        svg = SMILRenderer().render_entity(dot)
        assert "animateTransform" in svg
        assert 'values="1;2;1"' in svg
        assert 'keyTimes="0;0.5;1"' in svg

    def test_multi_keyframe_bounce(self):
        """Bounce with 3+ keyframes mirrors correctly."""
        dot = Dot(10, 20, radius=5, color="red")
        dot.animate("r", keyframes={0: 5, 0.5: 10, 1.0: 15},
                    bounce=True, repeat=True)
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
        e.animate("fill_opacity", keyframes={0: 1.0, 1.0: 0.0}, duration=2.0)
        svg = SMILRenderer().render_entity(e)
        assert 'attributeName="fill-opacity"' in svg
        assert 'values="1;0"' in svg

    def test_stroke_opacity_animation_polygon(self):
        """stroke_opacity animates to stroke-opacity on Polygon."""
        p = Polygon([(0, 0), (20, 0), (10, 20)], fill="red", stroke="black")
        p.animate("stroke_opacity", keyframes={0: 1.0, 1.0: 0.3}, duration=1.5)
        svg = SMILRenderer().render_entity(p)
        assert 'attributeName="stroke-opacity"' in svg

    def test_fill_opacity_animation_rect(self):
        """fill_opacity still works on Rect after universal mapping."""
        r = Rect(10, 10, 50, 30, fill="green")
        r.animate("fill_opacity", keyframes={0: 1.0, 1.0: 0.0}, duration=1.0)
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
        t.fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_entity(t)
        assert "<textPath" in svg
        assert 'href="#tp1"' in svg
        assert 'attributeName="opacity"' in svg
        assert "<animate" in svg

    def test_textpath_color_animation(self):
        """Text on a path with color animation emits fill attribute."""
        t = Text(0, 0, "World", font_size=16, color="red")
        t.set_textpath("tp2", "M 0 0 L 100 0", start_offset="0%")
        t.animate("color", keyframes={0: "red", 1.0: "blue"}, duration=1.0)
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
        conn.fade(to=0.0, duration=1.5)
        svg = SMILRenderer().render_connection(conn)
        assert "<animate" in svg
        assert 'attributeName="opacity"' in svg

    def test_connection_color_animation_smil(self):
        """Connection color animation maps to stroke attribute."""
        d1 = Dot(10, 20, radius=5, color="red")
        d2 = Dot(80, 80, radius=5, color="blue")
        conn = Connection(d1, d2)
        conn.animate("color", keyframes={0: "red", 1.0: "blue"}, duration=1.0)
        svg = SMILRenderer().render_connection(conn)
        assert 'attributeName="stroke"' in svg


# ======================================================================
# Reactive animation tests
# ======================================================================


class TestReactivePolygonAnimation:
    """Reactive polygon animations when vertices are animated entities."""

    def test_animated_vertex_emits_points_animate(self):
        """Polygon vertex entity with .move() produces <animate attributeName="points">."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        scene.add(b, at=(0.9, 0.1))
        scene.add(c, at=(0.5, 0.9))
        b.move(to=(0.5, 0.5), duration=2.0)
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
        a.move(to=(0.9, 0.9), duration=1.0)
        poly = Polygon([a, Coord(100, 100), Coord(0, 100)], fill="green")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' in svg
        # Static coords should appear in the values (constant across keyframes)
        assert "100,100" in svg

    def test_incompatible_vertex_anims_no_reactive(self):
        """Vertices with different durations produce no reactive animation."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        b = Point(0, 0)
        c = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        scene.add(b, at=(0.9, 0.1))
        scene.add(c, at=(0.5, 0.9))
        a.move(to=(0.5, 0.5), duration=1.0)
        b.move(to=(0.5, 0.5), duration=2.0)  # Different duration
        poly = Polygon([a, b, c], fill="red")
        scene.place(poly)
        svg = SMILRenderer().render_entity(poly)
        assert '<animate attributeName="points"' not in svg

    def test_own_animations_coexist(self):
        """Polygon's own opacity animation + reactive vertex animation both appear."""
        scene = Scene(200, 200)
        a = Point(0, 0)
        scene.add(a, at=(0.1, 0.1))
        a.move(to=(0.5, 0.5), duration=1.0)
        poly = Polygon([a, Coord(100, 100), Coord(0, 100)], fill="green")
        poly.fade(to=0.0, duration=1.0)
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
        a.move(to=(0.5, 0.5), duration=2.0, bounce=True, repeat=True)
        b.move(to=(0.5, 0.5), duration=2.0, bounce=True, repeat=True)
        c.move(to=(0.5, 0.5), duration=2.0, bounce=True, repeat=True)
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
        d1.move(to=(0.5, 0.5), duration=2.0)
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
        d1.move(to=(0.5, 0.5), duration=2.0)
        d2.move(to=(0.5, 0.8), duration=2.0)
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
        d1.move(to=(0.5, 0.5), duration=2.0)
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
        d1.move(to=(0.5, 0.5), duration=2.0)
        conn = Connection(d1, d2)
        conn.fade(to=0.0, duration=2.0)
        svg = SMILRenderer().render_connection(conn)
        assert '<animate attributeName="x1"' in svg
        assert '<animate attributeName="opacity"' in svg
