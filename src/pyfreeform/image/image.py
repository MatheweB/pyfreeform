"""Image - Container for multiple layers representing an image."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

import numpy as np
from PIL import Image as PILImage

from .layer import Layer
from .resize import (
    downscale_array,
    fit_dimensions,
    quantize_dimensions,
    resize_array,
)


class Image:
    """
    An image composed of multiple layers.
    
    Each layer represents a channel of the image (red, green, blue, alpha)
    or a computed property (brightness, grayscale). Layers are created
    lazily when accessed.
    
    Attributes:
        width: Image width in pixels
        height: Image height in pixels
        layers: Dictionary of layer name to Layer object
    
    Examples:
        >>> img = Image.load("photo.png")
        >>> img.width, img.height
        (800, 600)
        >>> red_layer = img["red"]
        >>> color = img.hex_at(100, 100)
        '#ff5733'
    """
    
    # Standard layer names
    CHANNEL_LAYERS = ("red", "green", "blue", "alpha")
    COMPUTED_LAYERS = ("brightness", "grayscale")
    
    def __init__(
        self,
        red: np.ndarray,
        green: np.ndarray,
        blue: np.ndarray,
        alpha: np.ndarray | None = None,
    ) -> None:
        """
        Create an image from channel arrays.
        
        Use Image.load() to create from a file instead.
        
        Args:
            red: Red channel as 2D numpy array (0-255).
            green: Green channel as 2D numpy array (0-255).
            blue: Blue channel as 2D numpy array (0-255).
            alpha: Optional alpha channel as 2D numpy array (0-255).
        """
        # Validate shapes match
        shape = red.shape
        if green.shape != shape or blue.shape != shape:
            raise ValueError("All channel arrays must have the same shape")
        if alpha is not None and alpha.shape != shape:
            raise ValueError("Alpha channel must have the same shape as RGB")
        
        self._layers: dict[str, Layer] = {
            "red": Layer(red),
            "green": Layer(green),
            "blue": Layer(blue),
        }
        
        if alpha is not None:
            self._layers["alpha"] = Layer(alpha)
        
        self._width = shape[1]
        self._height = shape[0]
    
    @classmethod
    def load(cls, path: str | Path, frame: int = 0) -> Image:
        """
        Load an image from a file.
        
        Supports PNG, JPEG, GIF, WebP, BMP, TIFF, and other formats
        supported by Pillow.
        
        Args:
            path: Path to the image file.
            frame: For animated images (GIF), which frame to load (default: 0).
        
        Returns:
            A new Image instance.
        
        Raises:
            FileNotFoundError: If the file doesn't exist.
            ValueError: If the file can't be decoded as an image.
        """
        path = Path(path)
        
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")
        
        try:
            pil_img = PILImage.open(path)
        except Exception as e:
            raise ValueError(f"Could not open image: {e}")
        
        # Handle animated images (GIF, WebP)
        if hasattr(pil_img, 'n_frames') and pil_img.n_frames > 1:
            if frame < 0 or frame >= pil_img.n_frames:
                raise ValueError(
                    f"Frame {frame} out of range (0-{pil_img.n_frames - 1})"
                )
            pil_img.seek(frame)
        
        # Convert to RGBA to ensure consistent format
        pil_img = pil_img.convert("RGBA")
        
        # Extract channels
        arr = np.array(pil_img)
        red = arr[:, :, 0].astype(np.float64)
        green = arr[:, :, 1].astype(np.float64)
        blue = arr[:, :, 2].astype(np.float64)
        alpha = arr[:, :, 3].astype(np.float64)
        
        return cls(red, green, blue, alpha)
    
    @classmethod
    def from_pil(cls, pil_img: PILImage.Image) -> Image:
        """
        Create an Image from a PIL Image object.
        
        Args:
            pil_img: A PIL Image object.
        
        Returns:
            A new Image instance.
        """
        pil_img = pil_img.convert("RGBA")
        arr = np.array(pil_img)
        
        return cls(
            red=arr[:, :, 0].astype(np.float64),
            green=arr[:, :, 1].astype(np.float64),
            blue=arr[:, :, 2].astype(np.float64),
            alpha=arr[:, :, 3].astype(np.float64),
        )
    
    @staticmethod
    def frame_count(path: str | Path) -> int:
        """
        Get the number of frames in an image file.
        
        For static images, returns 1. For animated GIFs/WebPs,
        returns the total frame count.
        
        Args:
            path: Path to the image file.
        
        Returns:
            Number of frames in the image.
        """
        path = Path(path)
        with PILImage.open(path) as pil_img:
            return getattr(pil_img, 'n_frames', 1)
    
    @property
    def width(self) -> int:
        """Image width in pixels."""
        return self._width
    
    @property
    def height(self) -> int:
        """Image height in pixels."""
        return self._height
    
    @property
    def size(self) -> tuple[int, int]:
        """Image size as (width, height) tuple."""
        return (self._width, self._height)
    
    @property
    def has_alpha(self) -> bool:
        """Whether this image has an alpha channel."""
        return "alpha" in self._layers
    
    @property
    def layers(self) -> dict[str, Layer]:
        """Dictionary of all available layers."""
        # Ensure computed layers are generated
        self._ensure_computed_layers()
        return dict(self._layers)
    
    def _ensure_computed_layers(self) -> None:
        """Generate computed layers if not already present."""
        if "brightness" not in self._layers:
            # Perceptual luminance formula
            brightness = (
                0.299 * self._layers["red"].data +
                0.587 * self._layers["green"].data +
                0.114 * self._layers["blue"].data
            )
            self._layers["brightness"] = Layer(brightness)
        
        if "grayscale" not in self._layers:
            # Simple average
            grayscale = (
                self._layers["red"].data +
                self._layers["green"].data +
                self._layers["blue"].data
            ) / 3
            self._layers["grayscale"] = Layer(grayscale)
    
    def __getitem__(self, layer_name: str) -> Layer:
        """
        Get a layer by name.
        
        Args:
            layer_name: One of 'red', 'green', 'blue', 'alpha',
                        'brightness', or 'grayscale'.
        
        Returns:
            The requested Layer.
        
        Raises:
            KeyError: If the layer doesn't exist.
        """
        if layer_name in self.COMPUTED_LAYERS:
            self._ensure_computed_layers()
        
        if layer_name not in self._layers:
            raise KeyError(f"Layer '{layer_name}' not found")
        
        return self._layers[layer_name]
    
    def rgb_at(self, x: int, y: int) -> tuple[int, int, int]:
        """
        Get RGB color at a position.
        
        Args:
            x: Horizontal position (0 = left).
            y: Vertical position (0 = top).
        
        Returns:
            Tuple of (red, green, blue) as integers 0-255.
        """
        r = int(np.clip(self._layers["red"][x, y], 0, 255))
        g = int(np.clip(self._layers["green"][x, y], 0, 255))
        b = int(np.clip(self._layers["blue"][x, y], 0, 255))
        return (r, g, b)
    
    def rgba_at(self, x: int, y: int) -> tuple[int, int, int, int]:
        """
        Get RGBA color at a position.
        
        Args:
            x: Horizontal position (0 = left).
            y: Vertical position (0 = top).
        
        Returns:
            Tuple of (red, green, blue, alpha) as integers 0-255.
            If no alpha channel exists, alpha is 255.
        """
        r, g, b = self.rgb_at(x, y)
        if self.has_alpha:
            a = int(np.clip(self._layers["alpha"][x, y], 0, 255))
        else:
            a = 255
        return (r, g, b, a)
    
    def hex_at(self, x: int, y: int) -> str:
        """
        Get hex color string at a position.
        
        Args:
            x: Horizontal position (0 = left).
            y: Vertical position (0 = top).
        
        Returns:
            Color as "#rrggbb" string.
        """
        r, g, b = self.rgb_at(x, y)
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def alpha_at(self, x: int, y: int) -> float:
        """
        Get alpha (opacity) at a position.
        
        Args:
            x: Horizontal position (0 = left).
            y: Vertical position (0 = top).
        
        Returns:
            Alpha value as float 0.0-1.0 (0 = transparent, 1 = opaque).
        """
        if self.has_alpha:
            return self._layers["alpha"][x, y] / 255.0
        return 1.0
    
    # --- Transformation methods (return new Image) ---
    
    def downscale(self, factor: int) -> Image:
        """
        Downscale the image by an integer factor.
        
        Uses averaging for smooth results.
        
        Args:
            factor: Downscale factor (e.g., 2 = half size).
        
        Returns:
            A new, smaller Image.
        """
        new_layers = {}
        for name, layer in self._layers.items():
            new_layers[name] = downscale_array(layer.data, factor)
        
        return Image(
            red=new_layers["red"],
            green=new_layers["green"],
            blue=new_layers["blue"],
            alpha=new_layers.get("alpha"),
        )
    
    def resize(self, width: int, height: int) -> Image:
        """
        Resize to exact dimensions.
        
        May distort aspect ratio. For aspect-preserving resize, use fit().
        
        Args:
            width: Target width.
            height: Target height.
        
        Returns:
            A new Image with the specified dimensions.
        """
        new_layers = {}
        for name, layer in self._layers.items():
            new_layers[name] = resize_array(layer.data, width, height)
        
        return Image(
            red=new_layers["red"],
            green=new_layers["green"],
            blue=new_layers["blue"],
            alpha=new_layers.get("alpha"),
        )
    
    def fit(self, width: int, height: int) -> Image:
        """
        Resize to fit within bounds, preserving aspect ratio.
        
        The result will be at most width x height, but may be smaller
        in one dimension to maintain proportions.
        
        Args:
            width: Maximum width.
            height: Maximum height.
        
        Returns:
            A new Image that fits within the bounds.
        """
        new_width, new_height = fit_dimensions(
            self._width, self._height, width, height
        )
        return self.resize(new_width, new_height)
    
    def quantize(self, cols: int | None = None, rows: int | None = None) -> Image:
        """
        Resize to a specific grid size.
        
        Useful for creating dot art with a specific number of dots.
        If only cols or rows is specified, the other is calculated
        to maintain aspect ratio.
        
        Args:
            cols: Target number of columns (width in pixels).
            rows: Target number of rows (height in pixels).
        
        Returns:
            A new Image with the specified grid dimensions.
        """
        if cols is None and rows is None:
            raise ValueError("At least one of cols or rows must be specified")
        
        target_cols, target_rows = quantize_dimensions(
            self._width, self._height, cols, rows
        )
        return self.resize(target_cols, target_rows)
    
    def __repr__(self) -> str:
        alpha_str = "+alpha" if self.has_alpha else ""
        return f"Image({self._width}x{self._height}{alpha_str})"
    
    def __iter__(self) -> Iterator[tuple[int, int, tuple[int, int, int]]]:
        """
        Iterate over all pixels as (x, y, (r, g, b)) tuples.
        
        Useful for converting an image to dots.
        """
        for y in range(self._height):
            for x in range(self._width):
                yield x, y, self.rgb_at(x, y)
