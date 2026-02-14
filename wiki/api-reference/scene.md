# Scene

Everything starts with a `Scene`. Three constructors cover all use cases: `Scene(w, h)` for freeform art, `Scene.from_image()` for image-based art, and `Scene.with_grid()` for grid-based art without an image.

!!! info "See also"
    For a hands-on walkthrough, see [Scenes and Grids](../guide/01-scenes-and-grids.md).

::: pyfreeform.Scene
    options:
      members:
        - __init__
        - from_image
        - with_grid
        - width
        - height
        - background
        - grid
        - grids
        - entities
        - connections
        - add
        - place
        - add_grid
        - remove
        - remove_grid
        - clear
        - to_svg
        - save
        - render
        - crop
        - trim
        - viewbox
        - set_viewbox
