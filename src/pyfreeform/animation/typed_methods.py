"""Factory-generated typed animation methods.

Provides reusable method objects for entity/connection subclasses to assign
as class attributes.  Each entity picks only the methods that match its
constructor parameters — users get IDE autocomplete and can't accidentally
animate a property that doesn't exist on their entity type.

Usage in an entity module::

    from ..animation import typed_methods as _anim

    class Rect(Entity):
        animate_fill = _anim.animate_fill
        animate_stroke = _anim.animate_stroke
        animate_width = _anim.animate_width
        ...
"""

from __future__ import annotations


# ======================================================================
# Factory helpers
# ======================================================================

def _color_anim(prop: str):
    """Create a typed color animation method for *prop*."""

    def method(self, to=None, *, keyframes=None, duration=1.0, delay=0.0,
               easing="linear", repeat=False, bounce=False, hold=True):
        return self.animate(prop, to=to, keyframes=keyframes,
                            duration=duration, delay=delay, easing=easing,
                            repeat=repeat, bounce=bounce, hold=hold)

    method.__name__ = f"animate_{prop}"
    method.__qualname__ = f"animate_{prop}"
    method.__doc__ = (
        f"Animate the ``{prop}`` color.\n\n"
        "Args:\n"
        "    to: Target color (name, hex, or RGB tuple).\n"
        "    keyframes: Dict of {time_seconds: color} for multi-step animation.\n"
        "    duration: Duration in seconds (simple mode only).\n"
        "    delay: Seconds before animation starts.\n"
        "    easing: Speed curve.\n"
        "    repeat: False=once, True=forever, int=N times.\n"
        "    bounce: Alternate direction each cycle.\n"
        "    hold: Hold final value after completion.\n\n"
        "Returns:\n"
        "    Self, for method chaining."
    )
    return method


def _numeric_anim(prop: str, label: str | None = None):
    """Create a typed numeric animation method for *prop*.

    *label* overrides the documented property name (e.g. ``"opacity"``
    is documented as ``"fade"`` when used for ``animate_fade``).
    """
    display = label or prop

    def method(self, to=None, *, keyframes=None, duration=1.0, delay=0.0,
               easing="linear", repeat=False, bounce=False, hold=True):
        return self.animate(prop, to=to, keyframes=keyframes,
                            duration=duration, delay=delay, easing=easing,
                            repeat=repeat, bounce=bounce, hold=hold)

    method.__name__ = f"animate_{display}"
    method.__qualname__ = f"animate_{display}"
    method.__doc__ = (
        f"Animate the ``{prop}`` property.\n\n"
        "Args:\n"
        "    to: Target value.\n"
        "    keyframes: Dict of {time_seconds: value} for multi-step animation.\n"
        "    duration: Duration in seconds (simple mode only).\n"
        "    delay: Seconds before animation starts.\n"
        "    easing: Speed curve.\n"
        "    repeat: False=once, True=forever, int=N times.\n"
        "    bounce: Alternate direction each cycle.\n"
        "    hold: Hold final value after completion.\n\n"
        "Returns:\n"
        "    Self, for method chaining."
    )
    return method


# ======================================================================
# Pre-built color animation methods
# ======================================================================

animate_fill: object = _color_anim("fill")
animate_color: object = _color_anim("color")
animate_stroke: object = _color_anim("stroke")

# ======================================================================
# Pre-built numeric animation methods
# ======================================================================

animate_fade: object = _numeric_anim("opacity", label="fade")
animate_radius: object = _numeric_anim("r", label="radius")
animate_width: object = _numeric_anim("width")
animate_height: object = _numeric_anim("height")
animate_stroke_width: object = _numeric_anim("stroke_width")
animate_rx: object = _numeric_anim("rx")
animate_ry: object = _numeric_anim("ry")
animate_font_size: object = _numeric_anim("font_size")
animate_fill_opacity: object = _numeric_anim("fill_opacity")
animate_stroke_opacity: object = _numeric_anim("stroke_opacity")
