"""Display utilities for PyFreeform."""

from __future__ import annotations

import tempfile
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scene import Scene


def display(target: Scene | str | Path) -> None:
    """
    Display an SVG in the default web browser.

    Can display either a Scene (renders to temp file first)
    or an existing SVG file.

    Args:
        target: A Scene to render, or a path to an existing SVG file.

    Examples:
        >>> from pyfreeform import Scene, Dot, display
        >>> scene = Scene(200, 200)
        >>> scene.add(Dot(100, 100, radius=50, color="coral"))  # Dot() uses pixels
        >>> display(scene)  # Opens in browser

        >>> display("my_art.svg")  # Opens existing file
    """
    # Import here to avoid circular imports
    from .scene import Scene

    if isinstance(target, Scene):
        # Render scene to a temporary file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".svg", delete=False, encoding="utf-8"
        ) as f:
            f.write(target.to_svg())
            temp_path = f.name

        # Open in browser
        webbrowser.open(f"file://{temp_path}")

    elif isinstance(target, str | Path):
        # Open existing file
        path = Path(target).resolve()

        if not path.exists():
            raise FileNotFoundError(f"SVG file not found: {path}")

        webbrowser.open(f"file://{path}")

    else:
        raise TypeError(f"Expected Scene or path, got {type(target).__name__}")
