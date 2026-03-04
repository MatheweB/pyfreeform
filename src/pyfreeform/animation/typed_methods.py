"""Typed animation methods for entity/connection subclasses.

Each entity picks only the methods that match its constructor parameters —
users get IDE autocomplete and can't accidentally animate a property that
doesn't exist on their entity type.

Usage in an entity module::

    from ..animation import typed_methods as _anim

    class Rect(Entity):
        animate_fill = _anim.animate_fill
        animate_stroke = _anim.animate_stroke
        animate_width = _anim.animate_width
        ...
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..color import ColorLike
    from ..core.entity import Entity
    from .models import EasingLike, RepeatLike


# ======================================================================
# Color animation methods
# ======================================================================


def animate_fill(
    self,
    to: ColorLike | None = None,
    *,
    keyframes: dict[float, ColorLike] | list[ColorLike] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``fill`` color.

    Args:
        to: Target color (name, hex, or RGB tuple).
        keyframes: Dict of {time_seconds: color} or list of colors
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "fill", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_color(
    self,
    to: ColorLike | None = None,
    *,
    keyframes: dict[float, ColorLike] | list[ColorLike] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``color`` property.

    Args:
        to: Target color (name, hex, or RGB tuple).
        keyframes: Dict of {time_seconds: color} or list of colors
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "color", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_stroke(
    self,
    to: ColorLike | None = None,
    *,
    keyframes: dict[float, ColorLike] | list[ColorLike] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``stroke`` color.

    Args:
        to: Target color (name, hex, or RGB tuple).
        keyframes: Dict of {time_seconds: color} or list of colors
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "stroke", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


# ======================================================================
# Numeric animation methods
# ======================================================================


def animate_fade(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``opacity`` property.

    Args:
        to: Target opacity value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "opacity", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_radius(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``r`` (radius) property.

    Args:
        to: Target radius value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "r", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_width(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``width`` property.

    Args:
        to: Target width value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "width", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_height(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``height`` property.

    Args:
        to: Target height value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "height", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_stroke_width(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``stroke_width`` property.

    Args:
        to: Target stroke width value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "stroke_width", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_rx(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``rx`` (horizontal radius) property.

    Args:
        to: Target rx value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "rx", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_ry(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``ry`` (vertical radius) property.

    Args:
        to: Target ry value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "ry", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_font_size(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``font_size`` property.

    Args:
        to: Target font size value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "font_size", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_fill_opacity(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``fill_opacity`` property.

    Args:
        to: Target fill opacity value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "fill_opacity", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )


def animate_stroke_opacity(
    self,
    to: float | None = None,
    *,
    keyframes: dict[float, float] | list[float] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> Entity:
    """Animate the ``stroke_opacity`` property.

    Args:
        to: Target stroke opacity value.
        keyframes: Dict of {time_seconds: value} or list of values
            (evenly spaced over duration) for multi-step animation.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.
        repeat: ``False`` = play once, ``True`` = loop forever,
            ``int`` = play N times.
        bounce: If ``True``, alternate direction each cycle.

    Returns:
        Self, for method chaining.
    """
    return self.animate(
        "stroke_opacity", to=to, keyframes=keyframes, duration=duration,
        delay=delay, easing=easing, hold=hold, repeat=repeat, bounce=bounce,
    )
