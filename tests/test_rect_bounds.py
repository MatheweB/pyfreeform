"""Visual bounds of a scaled, stroked Rect must include the scale factor.

Regression: Rect.rotated_bounds used stroke_width/2 (no scale), so a scaled
stroked rect inside a rotated EntityGroup under-reported its visual extent and
could be clipped by crop()/fit. Both methods now share Entity._expand_visual.
"""

import pytest

import pyfreeform as pf
from pyfreeform.entities.rect import Rect


class TestRectVisualBounds:
    def test_rotated_bounds_includes_scale(self):
        r = Rect(0, 0, 100, 100, fill="red", stroke="black", stroke_width=10)
        r.scale(2.0)
        geo = r.rotated_bounds(45, visual=False)
        vis = r.rotated_bounds(45, visual=True)
        # padding per side = stroke * scale / 2 = 10 * 2 / 2 = 10
        assert (geo[0] - vis[0]) == pytest.approx(10.0)
        assert (vis[2] - geo[2]) == pytest.approx(10.0)

    def test_bounds_and_rotated_bounds_agree_at_zero(self):
        r = Rect(0, 0, 80, 60, stroke="black", stroke_width=12)
        r.scale(1.5)
        assert r.rotated_bounds(0, visual=True) == r.bounds(visual=True)

    def test_zero_stroke_width_no_expansion(self):
        # _expand_visual returns bounds unchanged when there's no stroke width.
        r = Rect(0, 0, 100, 100, fill="red", stroke=None, stroke_width=0)
        r.scale(2.0)
        assert r.rotated_bounds(30, visual=True) == r.rotated_bounds(30, visual=False)

    def test_group_visual_bounds_contains_scaled_stroke(self):
        g = pf.EntityGroup(0, 0)
        r = Rect(-40, -30, 80, 60, fill="red", stroke="black", stroke_width=16)
        r.scale(2.0)
        g.add(r)
        g.rotate(20)
        bg = g.bounds(visual=False)
        bv = g.bounds(visual=True)
        # uniform expansion per side = stroke * scale / 2 = 16 * 2 / 2 = 16
        assert (bg[0] - bv[0]) == pytest.approx(16.0)
        assert (bv[2] - bg[2]) == pytest.approx(16.0)
