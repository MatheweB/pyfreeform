#!/usr/bin/env python3
"""Generate custom sample images for wiki tutorials.

Creates simple, visually interesting images designed to showcase
PyFreeform's from_image() capabilities clearly.
"""

from __future__ import annotations

import math

from PIL import Image as PILImage, ImageDraw

from . import SAMPLE_IMAGES


def create_gradient() -> None:
    """Create a smooth diagonal color gradient.

    Colors transition from deep blue (top-left) through purple (center)
    to warm orange (bottom-right). This creates clear brightness bands
    that demonstrate brightness-driven effects beautifully.
    """
    w, h = 400, 400
    img = PILImage.new("RGB", (w, h))
    pixels = img.load()
    if pixels is None:
        raise ValueError("Could not access image pixels")

    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2  # Diagonal parameter 0-1
            # Deep blue → purple → warm orange
            r = int(20 + t * 220)
            g = int(10 + (0.5 - abs(t - 0.5)) * 160)
            b = int(200 - t * 180)
            pixels[x, y] = (r, g, b)

    output = SAMPLE_IMAGES / "gradient.png"
    img.save(str(output))
    print(f"  Created {output.name} ({w}x{h})")


def create_circles() -> None:
    """Create concentric circles on a dark background.

    White circles on dark navy — perfect for demonstrating edge detection,
    high-contrast brightness effects, and radial patterns.
    """
    w, h = 400, 400
    img = PILImage.new("RGB", (w, h), (15, 15, 40))
    draw = ImageDraw.Draw(img)

    cx, cy = w // 2, h // 2
    for r in range(20, 200, 30):
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=(240, 240, 255),
            width=8,
        )

    output = SAMPLE_IMAGES / "circles.png"
    img.save(str(output))
    print(f"  Created {output.name} ({w}x{h})")


def create_waves() -> None:
    """Create a colorful wave pattern.

    Horizontal sine waves with smooth color cycling. Great for showing
    how PyFreeform can translate continuous gradients into discrete cell art.
    """
    w, h = 500, 300
    img = PILImage.new("RGB", (w, h), (10, 10, 25))
    pixels = img.load()
    if pixels is None:
        raise ValueError("Could not access image pixels")

    for y in range(h):
        for x in range(w):
            nx, ny = x / w, y / h
            # Multiple overlapping sine waves
            v1 = math.sin(nx * 6 * math.pi + ny * 2) * 0.3
            v2 = math.sin(ny * 4 * math.pi) * 0.4
            v3 = math.cos((nx + ny) * 3 * math.pi) * 0.3
            v = 0.5 + v1 + v2 + v3
            v = max(0, min(1, v))

            # Map to warm color palette
            r = int(v * 255)
            g = int(v * v * 180)
            b = int((1 - v) * 120 + 40)
            pixels[x, y] = (r, g, b)

    output = SAMPLE_IMAGES / "waves.png"
    img.save(str(output))
    print(f"  Created {output.name} ({w}x{h})")


def generate() -> None:
    """Create all custom sample images."""
    SAMPLE_IMAGES.mkdir(parents=True, exist_ok=True)
    print("Creating sample images...")
    create_gradient()
    create_circles()
    create_waves()
    print("Done.")


if __name__ == "__main__":
    generate()
