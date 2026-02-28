"""Animation data model — renderer-agnostic keyframe animations."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from ..core.pathable import Pathable


# ---------------------------------------------------------------------------
# Easing
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Easing:
    """Cubic-bezier easing function.

    Defines the speed curve of an animation using four control points
    of a cubic Bezier curve (x1, y1, x2, y2). The curve maps input
    time (0–1) to output progress (0–1).

    Predefined easings are available as class attributes::

        Easing.LINEAR       # constant speed
        Easing.EASE_IN      # slow start
        Easing.EASE_OUT     # slow end
        Easing.EASE_IN_OUT  # slow start and end

    Custom easing via constructor::

        Easing(0.68, -0.55, 0.27, 1.55)  # back-overshoot
    """

    x1: float = 0.0
    y1: float = 0.0
    x2: float = 1.0
    y2: float = 1.0

    # Predefined constants (assigned after class body)
    LINEAR: ClassVar[Easing]
    EASE_IN: ClassVar[Easing]
    EASE_OUT: ClassVar[Easing]
    EASE_IN_OUT: ClassVar[Easing]
    EASE_IN_CUBIC: ClassVar[Easing]
    EASE_OUT_CUBIC: ClassVar[Easing]

    def evaluate(self, t: float) -> float:
        """Map input time (0–1) to eased progress (0–1).

        Uses De Casteljau subdivision to solve the cubic-bezier curve.
        """
        if t <= 0.0:
            return 0.0
        if t >= 1.0:
            return 1.0
        if self == Easing.LINEAR:
            return t

        # Newton-Raphson to find the parameter u where x(u) = t
        u = t  # initial guess
        for _ in range(8):
            x = _bezier(u, self.x1, self.x2) - t
            if abs(x) < 1e-7:
                break
            dx = _bezier_derivative(u, self.x1, self.x2)
            if abs(dx) < 1e-7:
                break
            u -= x / dx

        # Clamp and evaluate y
        u = max(0.0, min(1.0, u))
        return _bezier(u, self.y1, self.y2)


def _bezier(t: float, p1: float, p2: float) -> float:
    """Evaluate cubic-bezier with implicit P0=0, P3=1."""
    mt = 1.0 - t
    return 3.0 * mt * mt * t * p1 + 3.0 * mt * t * t * p2 + t * t * t


def _bezier_derivative(t: float, p1: float, p2: float) -> float:
    """Derivative of cubic-bezier with implicit P0=0, P3=1."""
    mt = 1.0 - t
    return 3.0 * mt * mt * p1 + 6.0 * mt * t * (p2 - p1) + 3.0 * t * t * (1.0 - p2)


# Predefined easing constants
Easing.LINEAR = Easing(0.0, 0.0, 1.0, 1.0)
Easing.EASE_IN = Easing(0.42, 0.0, 1.0, 1.0)
Easing.EASE_OUT = Easing(0.0, 0.0, 0.58, 1.0)
Easing.EASE_IN_OUT = Easing(0.42, 0.0, 0.58, 1.0)
Easing.EASE_IN_CUBIC = Easing(0.55, 0.055, 0.675, 0.19)
Easing.EASE_OUT_CUBIC = Easing(0.215, 0.61, 0.355, 1.0)


# EasingLike type alias
EasingLike = Easing | str | tuple[float, float, float, float]

_EASING_NAMES: dict[str, Easing] = {
    "linear": Easing.LINEAR,
    "ease-in": Easing.EASE_IN,
    "ease-out": Easing.EASE_OUT,
    "ease-in-out": Easing.EASE_IN_OUT,
    "ease-in-cubic": Easing.EASE_IN_CUBIC,
    "ease-out-cubic": Easing.EASE_OUT_CUBIC,
}


def coerce_easing(value: EasingLike) -> Easing:
    """Convert user input to an Easing object.

    Accepts:
        - ``Easing`` instance (returned as-is)
        - ``str`` name: "linear", "ease-in", "ease-out", "ease-in-out"
        - ``tuple`` of four floats: (x1, y1, x2, y2)

    Raises:
        TypeError: If the value type is not supported.
        ValueError: If a string name is not recognized.
    """
    if isinstance(value, Easing):
        return value
    if isinstance(value, str):
        name = value.strip().lower()
        if name not in _EASING_NAMES:
            raise ValueError(
                f"Unknown easing '{value}'. "
                f"Available: {', '.join(sorted(_EASING_NAMES))}"
            )
        return _EASING_NAMES[name]
    if isinstance(value, tuple):
        if len(value) != 4:
            raise ValueError(f"Easing tuple must have 4 values, got {len(value)}")
        return Easing(*value)
    raise TypeError(f"Cannot coerce {type(value).__name__} to Easing")


# ---------------------------------------------------------------------------
# RepeatLike
# ---------------------------------------------------------------------------

RepeatLike = bool | int
"""Animation repeat specification.

- ``False`` — play once (default)
- ``True`` — loop forever
- ``int`` — play N times
"""


# ---------------------------------------------------------------------------
# Keyframe
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class Keyframe:
    """A single value at a point in time.

    Attributes:
        time: Time in seconds.
        value: The property value at this time.
    """

    time: float
    value: Any


# ---------------------------------------------------------------------------
# PropertyAnimation
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class PropertyAnimation:
    """Animation of a single entity property over time.

    Stores the property name (pyfreeform name, NOT SVG attribute),
    keyframes, and playback parameters. The renderer decides how
    to output this — SVG SMIL emits ``<animate>``, a game renderer
    calls ``evaluate(t)``.

    Attributes:
        prop: Property name (e.g., "opacity", "r", "fill").
        keyframes: Ordered list of (time, value) pairs.
        easing: Speed curve between keyframes.
        hold: If True, hold final value after animation ends.
        repeat: False=once, True=forever, int=N times.
        bounce: If True, alternate direction each cycle.
        delay: Seconds before animation starts.
    """

    prop: str
    keyframes: list[Keyframe] = field(default_factory=list)
    easing: Easing = field(default_factory=lambda: Easing.LINEAR)
    hold: bool = True
    repeat: RepeatLike = False
    bounce: bool = False
    delay: float = 0.0

    @property
    def duration(self) -> float:
        """Duration from first to last keyframe (seconds)."""
        if len(self.keyframes) < 2:
            return 0.0
        return self.keyframes[-1].time - self.keyframes[0].time

    def evaluate(self, t: float) -> Any:
        """Compute the interpolated value at time *t* (seconds).

        Handles delay, repeat, bounce, and easing. Works for numeric
        values (float, int) and color strings (interpolated in RGB).

        Args:
            t: Absolute time in seconds since animation start.

        Returns:
            Interpolated property value at time t.
        """
        if len(self.keyframes) < 2:
            return self.keyframes[0].value if self.keyframes else None

        dur = self.duration
        if dur <= 0:
            return self.keyframes[-1].value

        # Apply delay
        t = t - self.delay
        if t < 0:
            return self.keyframes[0].value

        # Handle repeat and bounce
        t = _apply_repeat(t, dur, self.repeat, self.bounce)
        if t is None:
            # Past the end, no repeat
            return self.keyframes[-1].value if self.hold else self.keyframes[0].value

        # Normalize t to [0, dur]
        base_time = self.keyframes[0].time

        # Find the two keyframes we're between
        for i in range(len(self.keyframes) - 1):
            kf0 = self.keyframes[i]
            kf1 = self.keyframes[i + 1]
            if t <= kf1.time - base_time:
                seg_dur = kf1.time - kf0.time
                if seg_dur <= 0:
                    return kf1.value
                local_t = (t - (kf0.time - base_time)) / seg_dur
                eased_t = self.easing.evaluate(local_t)
                return _interpolate(kf0.value, kf1.value, eased_t)

        return self.keyframes[-1].value


# ---------------------------------------------------------------------------
# MotionAnimation
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class MotionAnimation:
    """Animation that moves an entity along a path.

    The path is stored as a Pathable object. The renderer extracts
    geometry as needed — SVG SMIL uses ``<animateMotion>``, a game
    renderer calls ``path.point_at(t)``.

    Attributes:
        path: The path to follow.
        duration: Total duration in seconds.
        easing: Speed curve along the path.
        hold: If True, hold final position.
        repeat: False=once, True=forever, int=N times.
        bounce: If True, alternate direction each cycle.
        delay: Seconds before animation starts.
        rotate: True for auto-rotation along tangent, float for fixed angle.
    """

    path: Pathable
    duration: float
    easing: Easing = field(default_factory=lambda: Easing.LINEAR)
    hold: bool = True
    repeat: RepeatLike = False
    bounce: bool = False
    delay: float = 0.0
    rotate: bool | float = False

    def evaluate(self, t: float) -> tuple[float, float]:
        """Compute the (x, y) position at time *t*.

        Args:
            t: Absolute time in seconds.

        Returns:
            (x, y) position on the path.
        """
        t = t - self.delay
        if t < 0:
            pt = self.path.point_at(0.0)
            return (pt.x, pt.y)

        path_t = _apply_repeat(t, self.duration, self.repeat, self.bounce)
        if path_t is None:
            pt = self.path.point_at(1.0) if self.hold else self.path.point_at(0.0)
            return (pt.x, pt.y)

        normalized = path_t / self.duration if self.duration > 0 else 1.0
        eased = self.easing.evaluate(normalized)
        pt = self.path.point_at(eased)
        return (pt.x, pt.y)


# ---------------------------------------------------------------------------
# DrawAnimation
# ---------------------------------------------------------------------------

@dataclass(slots=True)
class DrawAnimation:
    """Animation that draws a path/connection progressively.

    Uses stroke-dashoffset technique: the path appears to be drawn
    from start to end (or end to start if reversed).

    Attributes:
        duration: Total duration in seconds.
        easing: Speed curve of the drawing.
        hold: If True, hold final state (path fully drawn).
        repeat: False=once, True=forever, int=N times.
        bounce: If True, alternate draw/erase each cycle.
        delay: Seconds before animation starts.
        reverse: If True, draw from end to start.
    """

    duration: float
    easing: Easing = field(default_factory=lambda: Easing.EASE_IN_OUT)
    hold: bool = True
    repeat: RepeatLike = False
    bounce: bool = False
    delay: float = 0.0
    reverse: bool = False

    def evaluate(self, t: float) -> float:
        """Compute the draw progress (0.0 = hidden, 1.0 = fully drawn).

        Args:
            t: Absolute time in seconds.

        Returns:
            Progress from 0.0 to 1.0.
        """
        t = t - self.delay
        if t < 0:
            return 0.0 if not self.reverse else 1.0

        raw_t = _apply_repeat(t, self.duration, self.repeat, self.bounce)
        if raw_t is None:
            progress = 1.0 if self.hold else 0.0
        else:
            normalized = raw_t / self.duration if self.duration > 0 else 1.0
            progress = self.easing.evaluate(normalized)

        if self.reverse:
            progress = 1.0 - progress
        return progress


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Union of all animation types
Animation = PropertyAnimation | MotionAnimation | DrawAnimation


def _apply_repeat(
    t: float,
    duration: float,
    repeat: RepeatLike,
    bounce: bool,
) -> float | None:
    """Apply repeat/bounce logic to raw elapsed time.

    Returns the effective time within one cycle [0, duration],
    or None if past the end with no repeat.
    """
    if duration <= 0:
        return 0.0

    if repeat is False or repeat == 1:
        # Single play
        if t >= duration:
            return None
        return t

    if repeat is True:
        # Infinite loop
        cycle = t / duration
        if bounce:
            # Alternate direction on odd cycles
            cycle_int = int(cycle)
            frac = cycle - cycle_int
            if cycle_int % 2 == 1:
                return duration * (1.0 - frac)
            return duration * frac
        return (t % duration)

    # Finite repeat count
    total = duration * int(repeat)
    if t >= total:
        return None
    cycle = t / duration
    if bounce:
        cycle_int = int(cycle)
        frac = cycle - cycle_int
        if cycle_int % 2 == 1:
            return duration * (1.0 - frac)
        return duration * frac
    return (t % duration)


def _interpolate(a: Any, b: Any, t: float) -> Any:
    """Linearly interpolate between two values.

    Supports:
        - Numeric (int, float): standard lerp
        - Color strings: RGB channel interpolation
        - Tuples of numbers: element-wise lerp
    """
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + (b - a) * t

    if isinstance(a, tuple) and isinstance(b, tuple):
        return tuple(
            a_i + (b_i - a_i) * t
            for a_i, b_i in zip(a, b)
        )

    if isinstance(a, str) and isinstance(b, str):
        return _interpolate_color(a, b, t)

    # Fallback: snap to b at t >= 0.5
    return a if t < 0.5 else b


def _interpolate_color(a: str, b: str, t: float) -> str:
    """Interpolate between two color strings in RGB space."""
    from ..color import Color

    try:
        rgb_a = Color(a).to_rgb()
        rgb_b = Color(b).to_rgb()
    except (ValueError, TypeError):
        # Can't parse — snap at midpoint
        return a if t < 0.5 else b

    r = int(rgb_a[0] + (rgb_b[0] - rgb_a[0]) * t)
    g = int(rgb_a[1] + (rgb_b[1] - rgb_a[1]) * t)
    b_ch = int(rgb_a[2] + (rgb_b[2] - rgb_a[2]) * t)
    return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b_ch)):02x}"
