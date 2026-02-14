*[RelCoordLike]: RelCoord | tuple[float, float] | str — a named position, relative coordinate, or tuple
*[AnchorSpec]: str | RelCoord | tuple[float, float] — anchor name, relative coord, or tuple
*[Pathable]: Any object implementing point_at(t: float) → Coord
*[ColorLike]: str | tuple[int, int, int] — hex color, named color, or RGB tuple
*[Connectable]: Entity | Surface — anything that can be an endpoint for a Connection
