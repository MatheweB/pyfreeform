"""Tests for the animation system — models, builders, and SMIL rendering."""

from __future__ import annotations

import pytest

from pyfreeform import Dot, Easing, Line, Rect, Scene, Path, Connection
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
