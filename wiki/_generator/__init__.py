"""Common utilities for wiki SVG generators."""

from __future__ import annotations

import math
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyfreeform import Scene

WIKI_ROOT = Path(__file__).parent.parent
IMAGES_DIR = WIKI_ROOT / "_images"
SAMPLE_IMAGES = WIKI_ROOT / "sample_images"


def save(scene: Scene, path: str) -> Path:
    """Save a scene to the _images/ directory.

    Args:
        scene: The Scene to render.
        path: Relative path within _images/ (e.g. "guide/dot-art.svg").

    Returns:
        The absolute output path.

    Raises:
        AssertionError: If the file wasn't created or is suspiciously small.
    """
    output = IMAGES_DIR / path
    output.parent.mkdir(parents=True, exist_ok=True)
    scene.save(str(output))
    assert output.exists(), f"Failed to generate: {output}"
    assert output.stat().st_size > 100, f"Suspiciously small file: {output}"
    print(f"    saved {path}  ({output.stat().st_size:,} bytes)")
    return output


def sample_image(name: str) -> Path:
    """Get the absolute path to a sample image.

    Args:
        name: Filename inside sample_images/ (e.g. "MonaLisa.jpg").

    Returns:
        Absolute path to the image.

    Raises:
        AssertionError: If the image doesn't exist.
    """
    path = SAMPLE_IMAGES / name
    assert path.exists(), f"Sample image not found: {path}"
    return path


def image_path(section: str, name: str) -> str:
    """Build a relative image path for use in markdown.

    Args:
        section: Section directory (e.g. "guide", "getting-started").
        name: SVG filename (e.g. "dot-art.svg").

    Returns:
        Relative path from wiki root (e.g. "_images/guide/dot-art.svg").
    """
    return f"_images/{section}/{name}"


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp value to [lo, hi]."""
    return max(lo, min(hi, value))


def wave(t: float, frequency: float = 1.0, phase: float = 0.0) -> float:
    """Sine wave normalized to 0-1 range."""
    return 0.5 + 0.5 * math.sin(2 * math.pi * frequency * t + phase)
