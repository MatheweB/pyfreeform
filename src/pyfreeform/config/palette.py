"""Palette - Curated color palettes for art."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    """
    A curated color palette for consistent, beautiful artwork.

    Palettes provide named colors for different purposes:
    - background: Scene background color
    - primary: Main element color (dots, fills)
    - secondary: Supporting element color
    - accent: Highlight color for emphasis
    - line: Color for lines and connections
    - grid: Color for grid outlines and borders

    Use pre-built palettes or create custom ones:

        # Pre-built
        colors = Palette.midnight()
        colors = Palette.sunset()

        # Custom
        colors = Palette(
            background="#1a1a2e",
            primary="#ff6b6b",
            secondary="#4ecdc4",
        )

        # Access colors
        scene.background = colors.background
        cell.add_dot(color=colors.primary)

    Attributes:
        background: Scene/canvas background color
        primary: Main element color
        secondary: Supporting element color
        accent: Highlight/emphasis color
        line: Line and connection color
        grid: Grid outline and border color
    """

    background: str = "#ffffff"
    primary: str = "#000000"
    secondary: str = "#666666"
    accent: str = "#ff0000"
    line: str = "#333333"
    grid: str = "#cccccc"

    # --- Pre-built Palettes ---

    @classmethod
    def midnight(cls) -> Palette:
        """
        Dark blue theme with coral accent.

        Perfect for dramatic, high-contrast art pieces.
        """
        return cls(
            background="#1a1a2e",
            primary="#ff6b6b",
            secondary="#4ecdc4",
            accent="#ffe66d",
            line="#666688",
            grid="#3d3d5c",
        )

    @classmethod
    def sunset(cls) -> Palette:
        """
        Warm oranges and purples.

        Evokes warmth and energy.
        """
        return cls(
            background="#2d1b4e",
            primary="#ff6b35",
            secondary="#f7c59f",
            accent="#efa00b",
            line="#8e7dbe",
            grid="#4a3a6e",
        )

    @classmethod
    def ocean(cls) -> Palette:
        """
        Cool blues and teals.

        Calm, serene aesthetic.
        """
        return cls(
            background="#0a1628",
            primary="#00d9ff",
            secondary="#0077b6",
            accent="#90e0ef",
            line="#48cae4",
            grid="#1a3a52",
        )

    @classmethod
    def forest(cls) -> Palette:
        """
        Natural greens and earth tones.

        Organic, grounded feel.
        """
        return cls(
            background="#1a2e1a",
            primary="#4ade80",
            secondary="#86efac",
            accent="#fbbf24",
            line="#6b8e6b",
            grid="#2d4a2d",
        )

    @classmethod
    def monochrome(cls) -> Palette:
        """
        Black, white, and grays.

        Classic, elegant simplicity.
        """
        return cls(
            background="#0a0a0a",
            primary="#ffffff",
            secondary="#888888",
            accent="#ffffff",
            line="#444444",
            grid="#222222",
        )

    @classmethod
    def paper(cls) -> Palette:
        """
        Light theme with paper-like background.

        Clean, minimalist aesthetic.
        """
        return cls(
            background="#fafafa",
            primary="#2c3e50",
            secondary="#7f8c8d",
            accent="#e74c3c",
            line="#bdc3c7",
            grid="#ecf0f1",
        )

    @classmethod
    def neon(cls) -> Palette:
        """
        Vibrant neon colors on dark background.

        Bold, electric energy.
        """
        return cls(
            background="#0d0d0d",
            primary="#ff00ff",
            secondary="#00ffff",
            accent="#ffff00",
            line="#ff00aa",
            grid="#1a1a2e",
        )

    @classmethod
    def pastel(cls) -> Palette:
        """
        Soft pastel colors.

        Gentle, approachable aesthetic.
        """
        return cls(
            background="#fef6e4",
            primary="#f582ae",
            secondary="#8bd3dd",
            accent="#ffc6c7",
            line="#c9b1ff",
            grid="#e8e4e1",
        )

