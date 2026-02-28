"""SVG rendering backend — static and SMIL-animated."""

from .smil import SMILRenderer
from .static import SVGRenderer

__all__ = ["SMILRenderer", "SVGRenderer"]
