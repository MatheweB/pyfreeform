"""Helper module for creating sample images in examples."""

from pathlib import Path

import numpy as np
from PIL import Image as PILImage


def create_gradient_image(
    width: int = 200,
    height: int = 200,
    output_dir: Path | None = None,
) -> Path:
    """
    Create a colorful gradient image for demo purposes.
    
    Corners:
    - Top-left: Blue (#0000ff)
    - Top-right: Red (#ff0000)
    - Bottom-left: Cyan (#00ffff)
    - Bottom-right: Yellow (#ffff00)
    
    Plus a soft bright circle in the center.
    
    Returns path to the created image.
    """
    if output_dir is None:
        output_dir = Path(__file__).parent
    
    arr = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Use (size - 1) for proper 0-255 range at edges
    max_x = max(1, width - 1)
    max_y = max(1, height - 1)
    
    for y in range(height):
        for x in range(width):
            arr[y, x, 0] = int(255 * x / max_x)           # Red: 0-255 left to right
            arr[y, x, 1] = int(255 * y / max_y)           # Green: 0-255 top to bottom
            arr[y, x, 2] = int(255 * (1 - x / max_x))     # Blue: 255-0 left to right
    
    # Add a soft bright circle in the center
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 4
    
    for y in range(height):
        for x in range(width):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            if dist < radius:
                # Smooth falloff using squared distance
                factor = 1 - (dist / radius) ** 2
                arr[y, x, 0] = min(255, int(arr[y, x, 0] + 80 * factor))
                arr[y, x, 1] = min(255, int(arr[y, x, 1] + 80 * factor))
                arr[y, x, 2] = min(255, int(arr[y, x, 2] + 80 * factor))
    
    path = output_dir / "sample_gradient.png"
    PILImage.fromarray(arr, mode='RGB').save(path)
    return path

def create_radial_gradient(
    width: int = 200,
    height: int = 200,
    output_dir: Path | None = None,
) -> Path:
    """
    Create a radial gradient - bright in center, dark at edges.
    
    Useful for demonstrating radial effects.
    """
    if output_dir is None:
        output_dir = Path(__file__).parent
    
    arr = np.zeros((height, width), dtype=np.uint8)
    
    center_x, center_y = width // 2, height // 2
    max_dist = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5
    
    for y in range(height):
        for x in range(width):
            dist = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            # Brightness decreases with distance from center
            brightness = max(0, 1 - dist / max_dist)
            arr[y, x] = int(255 * brightness)
    
    rgb = np.stack([arr, arr, arr], axis=2)
    
    path = output_dir / "gradient_radial.png"
    PILImage.fromarray(rgb, mode='RGB').save(path)
    return path


if __name__ == "__main__":
    # Create all sample images
    p1 = create_gradient_image()
    print(f"Created: {p1}")
    
    p2 = create_horizontal_gradient()
    print(f"Created: {p2}")
    
    p3 = create_radial_gradient()
    print(f"Created: {p3}")
