"""Generate SVGs for Guide: Shapes and Polygons."""

import math

from pyfreeform import (
    Scene,
    Palette,
    Polygon,
    EntityGroup,
    Dot,
    Line,
    Ellipse,
    Rect,
    Text,
    Point,
    Coord,
)

from wiki._generator import save, sample_image


def generate():
    colors = Palette.midnight()

    # --- 1. Shape classmethod gallery ---
    shapes = [
        ("triangle", Polygon.triangle(size=0.7)),
        ("square", Polygon.square(size=0.7)),
        ("diamond", Polygon.diamond(size=0.7)),
        ("hexagon", Polygon.hexagon(size=0.7)),
        ("star", Polygon.star(points=5, size=0.7)),
        ("octagon", Polygon.regular_polygon(sides=8, size=0.7)),
        ("squircle", Polygon.squircle(size=0.7)),
        ("rounded", Polygon.rounded_rect(size=0.7, corner_radius=0.25)),
    ]
    scene = Scene.with_grid(cols=8, rows=2, cell_size=50, background=colors.background)
    for i, (_name, verts) in enumerate(shapes):
        cell = scene.grid[0][i]
        cell.add_polygon(verts, fill=colors.primary, opacity=0.8)
        cell.add_border(color=colors.grid, width=0.3, opacity=0.3)
    for i, (name, _) in enumerate(shapes):
        cell = scene.grid[1][i]
        cell.add_text(name, at="center", font_size=0.20, color="#aaaacc", fit=True)
    save(scene, "guide/shapes-gallery.svg")

    # --- 2. Hexagonal grid ---
    colors_ocean = Palette.ocean()
    scene = Scene.with_grid(cols=14, rows=14, cell_size=20, background=colors_ocean.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        t = (nx + ny) / 2
        cell.add_polygon(
            Polygon.hexagon(size=0.85),
            fill=colors_ocean.primary,
            opacity=0.2 + t * 0.6,
            stroke=colors_ocean.secondary,
            stroke_width=0.5,
        )
    save(scene, "guide/shapes-hex-grid.svg")

    # --- 3. Stars sized by brightness ---
    scene = Scene.from_image(
        sample_image("FrankMonster.png"),
        grid_size=25,
        cell_size=16,
    )
    for cell in scene.grid:
        size = 0.3 + cell.brightness * 0.5
        inner = 0.3 + cell.brightness * 0.2
        cell.add_polygon(
            Polygon.star(points=5, size=size, inner_ratio=inner),
            fill=cell.color,
            opacity=0.6 + cell.brightness * 0.4,
        )
    save(scene, "guide/shapes-stars-brightness.svg")

    # --- 4. EntityGroup: flower pattern ---
    def make_flower(petal_color, center_color):
        """Create a flower EntityGroup."""
        group = EntityGroup()
        # 6 petals around center
        for i in range(6):
            angle = i * 60 * math.pi / 180
            px, py = 12 * math.cos(angle), 12 * math.sin(angle)
            group.add(Ellipse(px, py, rx=8, ry=4, rotation=i * 60, fill=petal_color, opacity=0.7))
        # Center dot
        group.add(Dot(0, 0, radius=5, color=center_color))
        return group

    colors_pastel = Palette.pastel()
    scene = Scene.with_grid(cols=6, rows=5, cell_size=48, background=colors_pastel.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        flower = make_flower(colors_pastel.primary, colors_pastel.accent)
        cell.add(flower)
        flower.fit_to_surface(0.85)
    save(scene, "guide/shapes-entity-group.svg")

    # --- 5. fit_to_surface demo ---
    colors_sunset = Palette.sunset()
    scene = Scene.with_grid(cols=5, rows=1, cell_size=60, background=colors_sunset.background)
    fractions = [0.3, 0.5, 0.7, 0.9, 1.0]
    for i, cell in enumerate(scene.grid):
        frac = fractions[i]
        group = EntityGroup()
        group.add(Dot(0, 0, radius=20, color=colors_sunset.primary))
        group.add(Line(-15, -15, 15, 15, width=2, color=colors_sunset.accent))
        group.add(Line(-15, 15, 15, -15, width=2, color=colors_sunset.accent))
        cell.add(group)
        group.fit_to_surface(frac)
        cell.add_text(
            f"{frac:.0%}",
            at="bottom",
            font_size=0.15,
            color="#aaaacc",
            baseline="auto",
        )
        cell.add_border(color=colors_sunset.grid, width=0.5, opacity=0.3)
    save(scene, "guide/shapes-fit-to-cell.svg")

    # --- 6. fit_to_surface with rotation ---
    scene = Scene.with_grid(cols=6, rows=6, cell_size=40, background=colors.background)
    for cell in scene.grid:
        nx, ny = cell.normalized_position
        rotation = (nx + ny) * 180
        group = EntityGroup()
        group.add(Dot(0, 0, radius=12, color=colors.primary, opacity=0.7))
        group.add(Line(-10, 0, 10, 0, width=2, color=colors.accent))
        group.add(Line(0, -10, 0, 10, width=2, color=colors.accent))
        cell.add(group)
        group.fit_to_surface(0.75)
        group.rotate(rotation)
    save(scene, "guide/shapes-fit-rotated.svg")

    # --- 7. Reactive polygon intro: three Points forming a triangle ---
    scene = Scene(300, 180, background=colors.background)
    a = Point(50, 140)
    b = Point(250, 140)
    c = Point(150, 30)
    tri = Polygon(
        [a, b, c],
        fill=colors.primary,
        opacity=0.6,
        stroke=colors.primary,
        stroke_width=1.5,
        stroke_opacity=0.8,
    )
    scene.place(tri)
    # Decorative markers at Point positions (Points are invisible)
    for pt, label in [(a, "a"), (b, "b"), (c, "c")]:
        scene.place(Dot(pt.x, pt.y, radius=5, color=colors.accent))
        scene.place(Text(pt.x, pt.y - 14, label, font_size=11, color="#aaaacc"))
    save(scene, "guide/shapes-reactive-intro.svg")

    # --- 8. Shared vertex: two triangles, one shared Point (3 frames) ---
    frame_w, frame_h = 200, 160
    gap = 20
    total_w = 3 * frame_w + 2 * gap
    scene = Scene(total_w + 40, frame_h + 50, background=colors.background)

    move_steps = [(0.0, "Original"), (0.5, "Moving shared"), (1.0, "Final")]
    # Shared vertex moves from (150, 40) to (210, 60)
    shared_start = Coord(150, 40)
    shared_end = Coord(210, 60)

    for frame_idx, (t, label) in enumerate(move_steps):
        ox = 20 + frame_idx * (frame_w + gap)

        # Shared vertex position at this step
        sx = shared_start.x + t * (shared_end.x - shared_start.x) + ox - 20
        sy = shared_start.y + t * (shared_end.y - shared_start.y) + 10

        # Left triangle base
        l1 = Coord(ox + 20, frame_h - 10)
        l2 = Coord(ox + 100, frame_h - 10)
        # Right triangle base
        r1 = Coord(ox + 100, frame_h - 10)
        r2 = Coord(ox + 180, frame_h - 10)

        # Ghost outlines (original shape, faint)
        if t > 0:
            orig_sx = shared_start.x + ox - 20
            orig_sy = shared_start.y + 10
            ghost = Polygon(
                [l1, l2, Coord(orig_sx, orig_sy)],
                fill=None,
                stroke=colors.grid,
                stroke_width=1,
                opacity=0.3,
            )
            scene.place(ghost)
            ghost2 = Polygon(
                [r1, r2, Coord(orig_sx, orig_sy)],
                fill=None,
                stroke=colors.grid,
                stroke_width=1,
                opacity=0.3,
            )
            scene.place(ghost2)

        # The two triangles
        tri_left = Polygon(
            [l1, l2, Coord(sx, sy)],
            fill=colors.primary,
            opacity=0.6,
            stroke=colors.primary,
            stroke_width=1.5,
            stroke_opacity=0.8,
        )
        tri_right = Polygon(
            [r1, r2, Coord(sx, sy)],
            fill=colors.secondary,
            opacity=0.6,
            stroke=colors.secondary,
            stroke_width=1.5,
            stroke_opacity=0.8,
        )
        scene.place(tri_left)
        scene.place(tri_right)

        # Dot markers at base vertices
        for v in [l1, l2, r2]:
            scene.place(Dot(v.x, v.y, radius=4, color=colors.line))

        # Shared vertex marker (accent)
        scene.place(Dot(sx, sy, radius=6, color=colors.accent))

        # Label
        scene.place(Text(ox + frame_w / 2, frame_h + 35, label, font_size=11, color="#aaaacc"))

    save(scene, "guide/shapes-shared-vertex.svg")

    # --- 9. Mixed vertices: Point + Rect anchors ---
    scene = Scene(360, 200, background=colors.background)
    rect = Rect.at_center(
        Coord(240, 110),
        100,
        70,
        fill=colors.secondary,
        opacity=0.3,
        stroke=colors.secondary,
        stroke_width=1.5,
        stroke_opacity=0.6,
    )
    scene.place(rect)

    # Point entity as the triangle tip
    tip = Point(80, 40)
    scene.place(Dot(tip.x, tip.y, radius=5, color=colors.accent))  # visual marker

    # Polygon with mixed vertex types
    tri = Polygon(
        [tip, (rect, "top_left"), (rect, "top_right")],
        fill=colors.primary,
        opacity=0.5,
        stroke=colors.primary,
        stroke_width=1.5,
        stroke_opacity=0.7,
    )
    scene.place(tri)

    # Anchor dots on Rect
    for anchor_name in ["top_left", "top_right"]:
        pos = rect.anchor(anchor_name)
        scene.place(Dot(pos.x, pos.y, radius=4, color=colors.accent))

    # Labels
    scene.place(Text(tip.x, tip.y - 14, "Point", font_size=10, color="#aaaacc"))
    tl = rect.anchor("top_left")
    tr = rect.anchor("top_right")
    scene.place(
        Text(tl.x - 5, tl.y - 12, "top_left", font_size=9, color="#aaaacc", text_anchor="end")
    )
    scene.place(
        Text(tr.x + 5, tr.y - 12, "top_right", font_size=9, color="#aaaacc", text_anchor="start")
    )
    rc = rect.anchor("center")
    scene.place(Text(rc.x, rc.y, "Rect", font_size=12, color="#aaaacc"))

    save(scene, "guide/shapes-mixed-vertices.svg")
