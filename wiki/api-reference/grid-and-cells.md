# Grid & Cells

A `Grid` divides the scene into rows and columns of `Cell` objects. Each cell is a creative unit with image data, position helpers, and the full set of [builder methods](drawing.md).

!!! info "See also"
    For grid creation patterns, see [Scenes and Grids](../guide/01-scenes-and-grids.md). For cell usage, see [Working with Cells](../guide/02-working-with-cells.md).

---

::: pyfreeform.Grid
    options:
      heading_level: 2
      members:
        - __init__
        - from_image
        - num_columns
        - num_rows
        - cell_width
        - cell_height
        - cell_size
        - pixel_width
        - pixel_height
        - origin
        - source_image
        - cells
        - row
        - column
        - rows
        - columns
        - get
        - cell_at_pixel
        - region
        - border
        - merge
        - merge_row
        - merge_col
        - every
        - checkerboard
        - where
        - diagonal
        - load_layer

---

::: pyfreeform.Cell
    options:
      heading_level: 2
      members:
        - brightness
        - color
        - rgb
        - alpha
        - data
        - row
        - col
        - grid
        - normalized_position
        - above
        - below
        - left
        - right
        - above_left
        - above_right
        - below_left
        - below_right
        - neighbors
        - neighbors_all
        - sample_image
        - sample_brightness
        - sample_hex
        - distance_to

`Cell` extends `Surface` -- it inherits all 12 [builder methods](drawing.md) plus has image data, position helpers, and neighbor access.

!!! warning "Neighbor properties return Cells, not positions"
    `cell.left`, `cell.right`, `cell.above`, `cell.below` return `Cell | None`, **not** position coordinates. Use `cell.center`, `cell.top_left`, etc. for positions.

---

::: pyfreeform.CellGroup
    options:
      heading_level: 2

A `CellGroup` is a virtual surface -- it has all the same `add_*` builder methods as a Cell, and averaged data properties from its constituent cells.
