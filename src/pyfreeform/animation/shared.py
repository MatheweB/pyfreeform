"""Shared animation logic for Entity, Connection, and Path.

Standalone functions that eliminate duplication across classes that
support animations. Each class keeps its own thin wrapper methods
with correct return types and docstrings.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .builders import build_animate, build_draw, build_fade
from .models import Animation, EasingLike, RepeatLike

if TYPE_CHECKING:
    from ..core.connection import Connection
    from ..core.entity import Entity


def consume_chain_delay(target: Entity | Connection, delay: float) -> float:
    """Add accumulated chain delay to explicit delay, then reset."""
    result = delay + target._chain_delay
    target._chain_delay = 0.0
    return result


def apply_chain(target: Entity | Connection, gap: float = 0) -> None:
    """Set chain delay from current animations' end times.

    Computes when all current animations end and stores that time
    (plus gap) as the chain delay for the next animation.
    """
    if not target._animations:
        return

    def _effective_end(anim: Animation) -> float:
        dur = anim.duration
        d = anim.delay
        rep = getattr(anim, "repeat", False)
        if isinstance(rep, int) and rep > 1:
            return d + dur * rep
        return d + dur

    target._chain_delay = max(_effective_end(a) for a in target._animations) + gap


def add_fade(
    target: Entity | Connection,
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
    delay = consume_chain_delay(target, delay)
    target._animations.append(build_fade(
        target, to, duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold,
    ))


def add_draw(
    target: Entity | Connection,
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
    delay = consume_chain_delay(target, delay)
    target._animations.append(build_draw(
        duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold, reverse=reverse,
    ))


def add_generic_animate(
    target: Entity | Connection,
    prop: str,
    *,
    to: float | int | str | tuple[float, ...] | None = None,
    keyframes: dict[float, float | int | str | tuple[float, ...]] | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    repeat: RepeatLike = False,
    bounce: bool = False,
    hold: bool = True,
) -> None:
    """Build and append a generic property animation."""
    delay = consume_chain_delay(target, delay)
    target._animations.append(build_animate(
        target, prop, to=to, keyframes=keyframes,
        duration=duration, delay=delay, easing=easing,
        repeat=repeat, bounce=bounce, hold=hold,
    ))


def clear_all_animations(target: Entity | Connection) -> None:
    """Remove all animations and reset chain delay."""
    target._animations.clear()
    target._chain_delay = 0.0
