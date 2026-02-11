"""Layer - A 2D matrix representing a single channel of image data."""

from __future__ import annotations

import numpy as np


class Layer:
    """
    A 2D matrix of values representing one channel of an image.
    
    Layers are the building blocks of images in PyFreeform. Each layer
    holds a single channel of data (e.g., red, green, blue, alpha, brightness).
    
    Attributes:
        data: The underlying numpy array
        width: Matrix width (number of columns)
        height: Matrix height (number of rows)
    
    Examples:
        >>> layer = Layer(np.zeros((100, 100)))
        >>> layer.width, layer.height
        (100, 100)
        >>> layer[50, 50]
        0.0
    """
    
    def __init__(self, data: np.ndarray) -> None:
        """
        Create a layer from a numpy array.
        
        Args:
            data: A 2D numpy array of values.
        
        Raises:
            ValueError: If data is not 2-dimensional.
        """
        if data.ndim != 2:
            raise ValueError(f"Layer data must be 2D, got {data.ndim}D")
        self._data = data.astype(np.float64)
    
    @property
    def data(self) -> np.ndarray:
        """The underlying numpy array."""
        return self._data
    
    @property
    def width(self) -> int:
        """Matrix width (number of columns)."""
        return self._data.shape[1]
    
    @property
    def height(self) -> int:
        """Matrix height (number of rows)."""
        return self._data.shape[0]
    
    @property
    def shape(self) -> tuple[int, int]:
        """Shape as (height, width) tuple."""
        return (self._data.shape[0], self._data.shape[1])
    
    def __getitem__(self, pos: tuple[int, int]) -> float:
        """
        Get value at position (x, y).
        
        Args:
            pos: Tuple of (x, y) coordinates.
        
        Returns:
            The value at that position.
        
        Note:
            Uses (x, y) order, not numpy's (row, col) order.
        """
        x, y = pos
        return float(self._data[y, x])
    
    def __setitem__(self, pos: tuple[int, int], value: float) -> None:
        """
        Set value at position (x, y).
        
        Args:
            pos: Tuple of (x, y) coordinates.
            value: The value to set.
        """
        x, y = pos
        self._data[y, x] = value
    
    def normalize(self) -> Layer:
        """
        Return a new layer with values scaled to 0-1 range.
        
        Returns:
            A new Layer with normalized values.
        """
        min_val = self._data.min()
        max_val = self._data.max()
        
        if max_val == min_val:
            # Avoid division by zero - return zeros or ones
            normalized = np.zeros_like(self._data)
        else:
            normalized = (self._data - min_val) / (max_val - min_val)
        
        return Layer(normalized)
    
    def to_uint8(self) -> Layer:
        """
        Return a new layer with values clamped and scaled to 0-255 range.
        
        Returns:
            A new Layer with uint8-range values.
        """
        clamped = np.clip(self._data, 0, 255)
        return Layer(clamped)
    
    def copy(self) -> Layer:
        """Return a copy of this layer."""
        return Layer(self._data.copy())
    
    def __repr__(self) -> str:
        return f"Layer({self.width}x{self.height})"
