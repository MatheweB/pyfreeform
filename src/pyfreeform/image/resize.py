"""Resize utilities for image operations."""

from __future__ import annotations

import numpy as np
from PIL import Image as PILImage


def fit_dimensions(
    src_width: int,
    src_height: int,
    max_width: int,
    max_height: int,
) -> tuple[int, int]:
    """
    Calculate dimensions that fit within bounds while preserving aspect ratio.

    Args:
        src_width: Source image width.
        src_height: Source image height.
        max_width: Maximum allowed width.
        max_height: Maximum allowed height.

    Returns:
        Tuple of (new_width, new_height) that fits within bounds.
    """
    if src_width <= max_width and src_height <= max_height:
        return src_width, src_height

    # Calculate scale factors
    width_ratio = max_width / src_width
    height_ratio = max_height / src_height

    # Use the smaller ratio to ensure we fit in both dimensions
    ratio = min(width_ratio, height_ratio)

    new_width = max(1, int(src_width * ratio))
    new_height = max(1, int(src_height * ratio))

    return new_width, new_height


def resize_array(
    arr: np.ndarray,
    width: int,
    height: int,
    resample: int = PILImage.Resampling.LANCZOS,
) -> np.ndarray:
    """
    Resize a 2D numpy array to new dimensions.

    Uses PIL for high-quality resampling.

    Args:
        arr: 2D numpy array to resize.
        width: Target width.
        height: Target height.
        resample: PIL resampling filter (default: LANCZOS for quality).

    Returns:
        Resized numpy array.
    """
    # Convert to PIL Image for resampling
    # Normalize to 0-255 range for PIL
    min_val, max_val = arr.min(), arr.max()
    if max_val > min_val:
        normalized = ((arr - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    else:
        normalized = np.zeros_like(arr, dtype=np.uint8)

    pil_img = PILImage.fromarray(normalized)
    resized_pil = pil_img.resize((width, height), resample=resample)

    # Convert back to original range
    resized = np.array(resized_pil, dtype=np.float64)
    if max_val > min_val:
        resized = resized / 255 * (max_val - min_val) + min_val

    return resized


def downscale_array(arr: np.ndarray, factor: int) -> np.ndarray:
    """
    Downscale a 2D array by an integer factor using averaging.

    Args:
        arr: 2D numpy array to downscale.
        factor: Integer downscale factor (e.g., 2 = half size).

    Returns:
        Downscaled numpy array.
    """
    if factor < 1:
        raise ValueError(f"Downscale factor must be >= 1, got {factor}")

    if factor == 1:
        return arr.copy()

    height, width = arr.shape
    new_height = height // factor
    new_width = width // factor

    # Trim to make dimensions divisible by factor
    trimmed = arr[: new_height * factor, : new_width * factor]

    # Reshape and average
    reshaped = trimmed.reshape(new_height, factor, new_width, factor)
    return reshaped.mean(axis=(1, 3))
