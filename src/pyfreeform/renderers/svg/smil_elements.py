"""Pure SMIL element building — no entity/connection dependencies.

Provides ``build_animate_element()`` and supporting helpers for assembling
SVG SMIL ``<animate>`` and ``<animateTransform>`` elements from pre-computed
values, keyTimes, and timing parameters.
"""

from __future__ import annotations

from ...animation.models import Easing, RepeatLike
from ...core.svg_utils import svg_num


# ======================================================================
# Helpers
# ======================================================================


def format_value(v: float | int | str) -> str:
    """Format a single keyframe value for SVG output."""
    if isinstance(v, float):
        return svg_num(v)
    if isinstance(v, int):
        return str(v)
    return str(v)


def smil_repeat(repeat: RepeatLike) -> str:
    """Convert repeat parameter to SVG ``repeatCount`` attribute fragment."""
    if repeat is True:
        return ' repeatCount="indefinite"'
    if isinstance(repeat, int) and repeat > 1:
        return f' repeatCount="{repeat}"'
    return ""


def apply_bounce(
    values: list[str], key_times: list[float],
) -> tuple[list[str], list[float]]:
    """Mirror values and key-times for bounce (forward then backward).

    Forward half maps to [0, 0.5], backward half to [0.5, 1].
    The peak value is shared (not duplicated) between halves.
    """
    n = len(values)
    if n < 2:
        return values, key_times

    # Forward half: compress into [0, 0.5]
    forward_kt = [t * 0.5 for t in key_times]

    # Backward half: reverse values (skip last) and remap times
    backward_vals = values[-2::-1]
    backward_kt = [
        0.5 + (1.0 - key_times[i]) * 0.5
        for i in range(n - 2, -1, -1)
    ]

    return values + backward_vals, forward_kt + backward_kt


def smil_easing_n(easing: Easing, n_segments: int) -> str:
    """Build ``calcMode`` + ``keySplines`` for *n_segments* segments.

    Returns an empty string for linear easing (the SVG default).
    """
    if easing == Easing.LINEAR:
        return ""
    spline = f"{easing.x1} {easing.y1} {easing.x2} {easing.y2}"
    return f' calcMode="spline" keySplines="{";".join([spline] * n_segments)}"'


# ======================================================================
# Main builder
# ======================================================================


def build_animate_element(
    *,
    tag: str = "animate",
    attribute_name: str,
    values: list[str],
    key_times: list[float],
    duration: float,
    delay: float = 0.0,
    easing: Easing | None = None,
    bounce: bool = False,
    hold: bool = True,
    repeat: RepeatLike = False,
    extra_attrs: str = "",
) -> str:
    """Build a single SMIL ``<animate>`` or ``<animateTransform>`` element.

    This is the single consolidated builder for all SMIL animation elements.
    Handles bounce, easing, delay, hold, and repeat.

    Args:
        tag: SVG element tag (``"animate"`` or ``"animateTransform"``).
        attribute_name: The SVG attribute being animated.
        values: Pre-formatted value strings for each keyframe.
        key_times: Normalized [0..1] time values for each keyframe.
        duration: Animation duration in seconds.
        delay: Seconds before animation starts.
        easing: An ``Easing`` object, or ``None`` for pre-baked
            (calcMode="linear") animations where easing is already
            baked into the sampled values.
        bounce: If True, mirror values/keyTimes for forward-then-backward.
        hold: If True, emit ``fill="freeze"`` to hold the final value.
        repeat: False=once, True=forever, int=N times.
        extra_attrs: Additional attributes to include (e.g.
            ``' type="rotate" additive="sum"'``).

    Returns:
        Complete SMIL element string.
    """
    if bounce:
        values, key_times = apply_bounce(values, key_times)

    n_segments = max(1, len(values) - 1)

    parts = [f'<{tag} attributeName="{attribute_name}"']
    parts.append(f' values="{";".join(values)}"')
    parts.append(f' keyTimes="{";".join(svg_num(t) for t in key_times)}"')
    parts.append(f' dur="{duration}s"')

    if delay > 0:
        parts.append(f' begin="{delay}s"')

    if easing is None:
        # Pre-baked: easing already applied to values via resampling
        pass  # SVG default calcMode is "linear", which is what we want
    else:
        parts.append(smil_easing_n(easing, n_segments))

    if hold:
        parts.append(' fill="freeze"')

    parts.append(smil_repeat(repeat))

    if extra_attrs:
        parts.append(extra_attrs)

    parts.append(" />")
    return "".join(parts)
