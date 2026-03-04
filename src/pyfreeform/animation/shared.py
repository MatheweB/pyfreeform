"""Shared animation logic for Entity, Connection, and Path.

Standalone functions that eliminate duplication across classes that
support animations. Each class keeps its own thin wrapper methods
with correct return types and docstrings.
"""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .builders import build_animate, build_draw, build_fade
from .models import Animation, EasingLike, RepeatLike

if TYPE_CHECKING:
    from ..core.connection import Connection
    from ..core.entity import Entity

# Monotonically increasing counter — each .then() call gets a unique chain ID.
_chain_id_seq = itertools.count(1)


def consume_chain_delay(target: Entity | Connection, delay: float) -> float:
    """Add accumulated chain delay to explicit delay, then reset."""
    result = delay + target._chain_delay
    target._chain_delay = 0.0
    return result


def _tag_with_chain(target: Entity | Connection, anim: Animation) -> None:
    """If target is in a chain context, tag anim with chain_id and chain_seq."""
    if target._chain_id is not None:
        anim.chain_id = target._chain_id
        anim.chain_seq = target._chain_next_seq


def apply_chain(target: Entity | Connection, gap: float = 0) -> None:
    """Set chain delay from current animations' end times.

    Computes when all current animations end and stores that time
    (plus gap) as the chain delay for the next animation.

    Also assigns a shared ``chain_id`` to all existing animations (seq 0)
    and advances ``_chain_next_seq`` so subsequent animations are tagged
    as later steps in the sequential unit.
    """
    if not target._animations:
        return

    def _effective_end(anim: Animation) -> float:
        duration = anim.duration
        delay = anim.delay
        repeat = getattr(anim, "repeat", False)
        if isinstance(repeat, int) and repeat > 1:
            return delay + duration * repeat
        return delay + duration

    target._chain_delay = max(_effective_end(a) for a in target._animations) + gap

    # Tag existing animations as chain seq=0 on first .then() call
    if target._chain_id is None:
        target._chain_id = next(_chain_id_seq)
        for anim in target._animations:
            anim.chain_id = target._chain_id
            anim.chain_seq = 0
        target._chain_next_seq = 1
    else:
        # Subsequent .then() calls — advance the seq counter for next batch
        target._chain_next_seq += 1


def apply_loop(
    target: Entity | Connection,
    *,
    bounce: bool = False,
    times: RepeatLike = True,
) -> None:
    """Stamp looping behaviour onto all animations on *target*.

    Called by ``Entity.loop()`` and ``Connection.loop()``. Iterates all
    animations and sets their ``bounce`` and ``repeat`` fields directly
    on the dataclass instances — the SMIL renderer reads these fields at
    render time, so no renderer changes are needed.

    Args:
        target: Entity or Connection whose animations will be updated.
        bounce: If True, each cycle reverses direction.
        times: ``True`` = loop forever, ``int >= 2`` = loop N times.

    Raises:
        ValueError: If *times* is ``False``, 0, 1, or any negative integer —
            these values do not actually loop.
        ValueError: If there are no animations to loop (nothing to apply to).
    """
    # bool is a subclass of int in Python, so exclude booleans from the
    # int-range check to avoid `True <= 1` being True (True == 1).
    if times is False or (not isinstance(times, bool) and isinstance(times, int) and times <= 1):
        raise ValueError(
            f"loop(times={times!r}) doesn't actually loop. "
            "Use times=True for infinite or times=N where N >= 2."
        )
    if not target._animations:
        raise ValueError("No animations to loop. Call animate_* methods before .loop().")
    for anim in target._animations:
        anim.bounce = bounce
        anim.repeat = times


def add_fade(
    target: Entity | Connection,
    to: float,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> None:
    """Build and append a fade (opacity) animation."""
    delay = consume_chain_delay(target, delay)
    anim = build_fade(
        target,
        to,
        duration=duration,
        delay=delay,
        easing=easing,
        hold=hold,
        repeat=repeat,
        bounce=bounce,
    )
    _tag_with_chain(target, anim)
    target._animations.append(anim)


def add_draw(
    target: Entity | Connection,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "ease-in-out",
    hold: bool = True,
    reverse: bool = False,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> None:
    """Build and append a draw (stroke reveal) animation."""
    delay = consume_chain_delay(target, delay)
    anim = build_draw(
        duration=duration,
        delay=delay,
        easing=easing,
        hold=hold,
        reverse=reverse,
        repeat=repeat,
        bounce=bounce,
    )
    _tag_with_chain(target, anim)
    target._animations.append(anim)


def add_generic_animate(
    target: Entity | Connection,
    prop: str,
    *,
    to: float | int | str | tuple[float, ...] | None = None,
    keyframes: dict[float, float | int | str | tuple[float, ...]]
    | list[float | int | str | tuple[float, ...]]
    | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> None:
    """Build and append a generic property animation."""
    delay = consume_chain_delay(target, delay)
    anim = build_animate(
        target,
        prop,
        to=to,
        keyframes=keyframes,
        duration=duration,
        delay=delay,
        easing=easing,
        hold=hold,
        repeat=repeat,
        bounce=bounce,
    )
    _tag_with_chain(target, anim)
    target._animations.append(anim)


def clear_all_animations(target: Entity | Connection) -> None:
    """Remove all animations and reset chain delay and chain state."""
    target._animations.clear()
    target._chain_delay = 0.0
    target._chain_id = None
    target._chain_next_seq = 0
