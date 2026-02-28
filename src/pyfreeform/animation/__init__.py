"""Animation system for PyFreeform — renderer-agnostic animation data."""

from .builders import stagger
from .models import (
    Animation,
    DrawAnimation,
    Easing,
    EasingLike,
    Keyframe,
    MotionAnimation,
    PropertyAnimation,
    RepeatLike,
    coerce_easing,
)

__all__ = [
    "Animation",
    "DrawAnimation",
    "Easing",
    "EasingLike",
    "Keyframe",
    "MotionAnimation",
    "PropertyAnimation",
    "RepeatLike",
    "coerce_easing",
    "stagger",
]
