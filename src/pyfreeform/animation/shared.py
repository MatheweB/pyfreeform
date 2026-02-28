"""Shared animation logic for Entity, Connection, and Path.

Standalone functions that eliminate duplication across classes that
support animations. Each class keeps its own thin wrapper methods
with correct return types and docstrings.
"""

from __future__ import annotations

from typing import Any

from .models import EasingLike, RepeatLike


def consume_chain_delay(target: Any, delay: float) -> float:
    """Add accumulated chain delay to explicit delay, then reset."""
    result = delay + target._chain_delay
    target._chain_delay = 0.0
    return result


def apply_chain(target: Any, gap: float = 0) -> None:
    """Set chain delay from current animations' end times.

    Computes when all current animations end and stores that time
    (plus gap) as the chain delay for the next animation.
    """
    if not target._animations:
        return

    def _effective_end(anim: Any) -> float:
        dur = anim.duration
        d = anim.delay
        rep = getattr(anim, "repeat", False)
        if isinstance(rep, int) and rep > 1:
            return d + dur * rep
        return d + dur

    target._chain_delay = max(_effective_end(a) for a in target._animations) + gap


def add_fade(
    target: Any,
    to: float,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    repeat: RepeatLike = False,
    bounce: bool = False,
    hold: bool = True,
) -> None:
    """Build and append a fade (opacity) animation."""
    from .builders import build_fade

    delay = consume_chain_delay(target, delay)
    target._animations.append(build_fade(
        target, to, duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold,
    ))


def add_draw(
    target: Any,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "ease-in-out",
    repeat: RepeatLike = False,
    bounce: bool = False,
    hold: bool = True,
    reverse: bool = False,
) -> None:
    """Build and append a draw (stroke reveal) animation."""
    from .builders import build_draw

    delay = consume_chain_delay(target, delay)
    target._animations.append(build_draw(
        duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold, reverse=reverse,
    ))


def add_generic_animate(
    target: Any,
    prop: str,
    *,
    to: Any = None,
    keyframes: dict[float, Any] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    repeat: RepeatLike = False,
    bounce: bool = False,
    hold: bool = True,
) -> None:
    """Build and append a generic property animation."""
    from .builders import build_animate

    delay = consume_chain_delay(target, delay)
    target._animations.append(build_animate(
        target, prop, to=to, keyframes=keyframes,
        duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold,
    ))


def clear_all_animations(target: Any) -> None:
    """Remove all animations and reset chain delay."""
    target._animations.clear()
    target._chain_delay = 0.0
