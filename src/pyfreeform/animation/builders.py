"""Builder functions for creating animations from intuitive parameters."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from ..core.relcoord import RelCoord, RelCoordLike
from .models import (
    DrawAnimation,
    EasingLike,
    Keyframe,
    MotionAnimation,
    PropertyAnimation,
    RepeatLike,
    coerce_easing,
)

if TYPE_CHECKING:
    from ..core.connection import Connection
    from ..core.entity import Entity
    from ..core.pathable import FullPathable


def build_fade(
    entity: Entity | Connection,
    to: float,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> PropertyAnimation:
    """Build an opacity animation."""
    return PropertyAnimation(
        prop="opacity",
        keyframes=[
            Keyframe(0.0, entity.opacity),
            Keyframe(duration, float(to)),
        ],
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        repeat=repeat,
        bounce=bounce,
    )


def build_move(
    entity: Entity,
    to: RelCoordLike | None = None,
    *,
    by: RelCoordLike | None = None,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "ease-in-out",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> list[PropertyAnimation]:
    """Build position animations (one per axis).

    Stores RelCoord values in keyframes. The renderer resolves them
    to concrete coordinates at render time.

    Two modes:
        - Absolute: ``move(to=(0.8, 0.5))`` — move to position.
        - Relative: ``move(by=(0.1, 0))`` — move by offset.

    Args:
        entity: The entity to animate.
        to: Target position (absolute). Mutually exclusive with *by*.
        by: Movement offset (relative). Mutually exclusive with *to*.

    Raises:
        ValueError: If both *to* and *by* are given, or neither.
    """
    if to is not None and by is not None:
        raise ValueError("Cannot specify both 'to' and 'by'")

    current_at = entity.at
    if current_at is None:
        current_at = RelCoord(0.5, 0.5)

    if to is not None:
        target = RelCoord.coerce(to)
    elif by is not None:
        target = current_at + RelCoord.coerce(by)
    else:
        raise ValueError("Must specify either 'to' or 'by'")

    return [
        PropertyAnimation(
            prop="at_rx",
            keyframes=[Keyframe(0.0, current_at.rx), Keyframe(duration, target.rx)],
            easing=coerce_easing(easing),
            hold=hold,
            delay=delay,
            repeat=repeat,
            bounce=bounce,
        ),
        PropertyAnimation(
            prop="at_ry",
            keyframes=[Keyframe(0.0, current_at.ry), Keyframe(duration, target.ry)],
            easing=coerce_easing(easing),
            hold=hold,
            delay=delay,
            repeat=repeat,
            bounce=bounce,
        ),
    ]


def build_spin(
    entity: Entity,
    angle: float = 360,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
    pivot: RelCoordLike | None = None,
) -> PropertyAnimation:
    """Build a rotation animation.

    Args:
        entity: The entity being animated (used to read initial rotation).
        angle: Total rotation in degrees.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after animation ends.
        repeat: False=once, True=forever, int=N times.
        bounce: Alternate direction each cycle.
        pivot: Custom rotation center as surface-relative ``(rx, ry)``.
            ``None`` = entity's natural ``rotation_center``.
    """
    return PropertyAnimation(
        prop="rotation",
        keyframes=[
            Keyframe(0.0, entity.rotation),
            Keyframe(duration, entity.rotation + angle),
        ],
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        repeat=repeat,
        bounce=bounce,
        pivot=RelCoord.coerce(pivot) if pivot is not None else None,
    )


def build_follow(
    path: FullPathable,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "linear",
    hold: bool = True,
    rotate: bool | float = False,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> MotionAnimation:
    """Build a motion-along-path animation."""
    return MotionAnimation(
        path=path,
        duration=duration,
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        rotate=rotate,
        repeat=repeat,
        bounce=bounce,
    )


def build_draw(
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "ease-in-out",
    hold: bool = True,
    reverse: bool = False,
    repeat: RepeatLike = False,
    bounce: bool = False,
) -> DrawAnimation:
    """Build a draw (stroke reveal) animation."""
    return DrawAnimation(
        duration=duration,
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        reverse=reverse,
        repeat=repeat,
        bounce=bounce,
    )


def build_animate(
    entity: Entity | Connection,
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
) -> PropertyAnimation:
    """Build a generic property animation.

    Three modes:
        - Simple: ``animate("opacity", to=0.0, duration=2.0)``
        - Keyframes (dict): ``animate("opacity", keyframes={0: 1.0, 1: 0.3, 2: 1.0})``
        - Keyframes (list): ``animate("fill", keyframes=["red", "blue", "red"], duration=2.0)``
          — values are evenly spaced from 0 to *duration*.

    Args:
        entity: The entity being animated (used to read current value).
        prop: Property name (pyfreeform name, e.g., "opacity", "r", "fill").
        to: Target value (simple mode). Mutually exclusive with keyframes.
        keyframes: Dict of {time_seconds: value}, or list of values
            (evenly spaced over *duration*).
        duration: Duration for simple mode, or total duration when
            keyframes is a list (ignored if keyframes is a dict).
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after completion.

    Raises:
        ValueError: If neither to nor keyframes is provided, or both are.
        ValueError: If keyframes is a list with fewer than 2 values.
    """
    if to is not None and keyframes is not None:
        raise ValueError("Cannot specify both 'to' and 'keyframes'")
    if to is None and keyframes is None:
        raise ValueError("Must specify either 'to' or 'keyframes'")

    if isinstance(keyframes, list):
        if len(keyframes) < 2:
            raise ValueError("keyframes list must have at least 2 values")
        n = len(keyframes) - 1
        keyframes = {i * duration / n: v for i, v in enumerate(keyframes)}

    if keyframes is not None:
        kf_list = [Keyframe(t, v) for t, v in sorted(keyframes.items())]
    else:
        current = _get_current_value(entity, prop)
        kf_list = [Keyframe(0.0, current), Keyframe(duration, to)]

    return PropertyAnimation(
        prop=prop,
        keyframes=kf_list,
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        repeat=repeat,
        bounce=bounce,
    )


def build_scale(
    entity: Entity,
    to: float,
    *,
    duration: float = 1.0,
    delay: float = 0.0,
    easing: EasingLike = "ease-in-out",
    hold: bool = True,
    repeat: RepeatLike = False,
    bounce: bool = False,
    pivot: RelCoordLike | None = None,
) -> PropertyAnimation:
    """Build a scale animation.

    Args:
        entity: The entity being animated (used to read initial scale).
        to: Target scale factor.
        duration: Duration in seconds.
        delay: Seconds before animation starts.
        easing: Speed curve.
        hold: Hold final value after animation ends.
        repeat: False=once, True=forever, int=N times.
        bounce: Alternate direction each cycle.
        pivot: Custom scale origin as surface-relative ``(rx, ry)``.
            ``None`` = entity's natural ``rotation_center``.
    """
    return PropertyAnimation(
        prop="scale_factor",
        keyframes=[
            Keyframe(0.0, entity.scale_factor),
            Keyframe(duration, float(to)),
        ],
        easing=coerce_easing(easing),
        hold=hold,
        delay=delay,
        repeat=repeat,
        bounce=bounce,
        pivot=RelCoord.coerce(pivot) if pivot is not None else None,
    )


def stagger(
    *entities: Entity | Connection,
    offset: float = 0.1,
    each: Callable[[Entity | Connection], Entity | Connection],
) -> list[Entity | Connection]:
    """Apply an animation to entities with staggered timing.

    Calls *each(entity)* for every entity, then adjusts the delay
    of newly added animations by ``i * offset`` seconds.

    Args:
        *entities: Entities (or connections) to animate.
        offset: Seconds between each entity's animation start.
        each: Callable that applies animation(s) to an entity.

    Returns:
        List of entities (same objects, with animations applied).

    Example::

        stagger(*dots, offset=0.2, each=lambda d: d.animate_fade(to=0.0, duration=1.0))
    """
    result = list(entities)
    for i, entity in enumerate(result):
        n_before = len(entity._animations)
        each(entity)
        for anim in entity._animations[n_before:]:
            anim.delay += i * offset
    return result


def _get_current_value(
    entity: Entity | Connection,
    prop: str,
) -> float | int | str:
    """Read the current value of a property from an entity.

    Tries direct attribute access. Returns 0 as fallback.
    """
    if hasattr(entity, prop):
        return getattr(entity, prop)
    # Common aliases
    aliases = {"r": "radius", "cx": "x", "cy": "y"}
    alias = aliases.get(prop)
    if alias and hasattr(entity, alias):
        return getattr(entity, alias)
    return 0
