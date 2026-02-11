"""Generate SVGs for Guide: Connections and Anchors."""

import math
import random

from pyfreeform import (
    Scene,
    Palette,
    Dot,
    Rect,
    Polygon,
    Ellipse,
    Line,
    Curve,
    Path,
    Text,
    ConnectionStyle,
    Coord,
)

from wiki._generator import save


def generate():
    colors = Palette.midnight()
    # midnight: background=#1a1a2e, primary=#ff6b6b, secondary=#4ecdc4,
    #           accent=#ffe66d, line=#666688, grid=#3d3d5c

    # --- 1. Basic connection ---
    scene = Scene(300, 100, background=colors.background)
    d1 = Dot(50, 50, radius=10, color=colors.primary)
    d2 = Dot(250, 50, radius=10, color=colors.secondary)
    scene.place(d1)
    scene.place(d2)
    conn = d1.connect(d2, shape=Line(), style=ConnectionStyle(width=2, color=colors.line))
    scene.add_connection(conn)
    # Labels
    scene.place(Text(50, 85, "dot1", font_size=10, color="#aaaacc"))
    scene.place(Text(250, 85, "dot2", font_size=10, color="#aaaacc"))
    save(scene, "guide/connections-basic.svg")

    # --- 2. Morphing square (4 frames) ---
    frame_w, frame_h = 160, 160
    gap = 20
    total_w = 4 * frame_w + 3 * gap
    scene = Scene(total_w + 40, frame_h + 60, background=colors.background)

    move_amounts = [0.0, 0.33, 0.66, 1.0]
    labels = ["Original", "t = 0.33", "t = 0.66", "t = 1.0"]
    sq_half = 50  # half-size of square
    conn_style = ConnectionStyle(width=2, color=colors.secondary, opacity=0.8)

    for frame_idx, (t, label) in enumerate(zip(move_amounts, labels, strict=False)):
        ox = 20 + frame_idx * (frame_w + gap)
        cx, cy = ox + frame_w / 2, 20 + frame_h / 2

        # 4 corners — top-right moves toward center
        tl = (cx - sq_half, cy - sq_half)
        tr_x = cx + sq_half - t * sq_half
        tr_y = cy - sq_half + t * sq_half
        tr = (tr_x, tr_y)
        br = (cx + sq_half, cy + sq_half)
        bl = (cx - sq_half, cy + sq_half)

        corners = [tl, tr, br, bl]
        dots = []
        for x, y in corners:
            d = Dot(x, y, radius=6, color=colors.primary)
            scene.place(d)
            dots.append(d)

        # 4 edges
        for i in range(4):
            conn = dots[i].connect(dots[(i + 1) % 4], shape=Line(), style=conn_style)
            scene.add_connection(conn)

        # Highlight the moving corner with accent
        if t > 0:
            dots[1].color = colors.accent

        # Ghost outline for original square position (faint)
        if t > 0:
            ghost_style = ConnectionStyle(width=1, color=colors.grid, opacity=0.3)
            orig_tr = Dot(cx + sq_half, cy - sq_half, radius=0, color=colors.background, opacity=0)
            scene.place(orig_tr)
            ghost = dots[0].connect(orig_tr, shape=Line(), style=ghost_style)
            scene.add_connection(ghost)
            ghost2 = orig_tr.connect(dots[2], shape=Line(), style=ghost_style)
            scene.add_connection(ghost2)

        # Frame label
        scene.place(Text(cx, frame_h + 45, label, font_size=11, color="#aaaacc"))

    save(scene, "guide/connections-morphing-square.svg")

    # --- 3. Anchor showcase on Rect ---
    scene = Scene(420, 320, background=colors.background)

    rect = Rect.at_center(
        Coord(210, 150),
        140,
        90,
        fill=colors.primary,
        opacity=0.25,
        stroke=colors.primary,
        stroke_width=1.5,
        stroke_opacity=0.5,
    )
    scene.place(rect)

    # Anchor positions → label offset directions
    anchor_info = {
        "center": (0, 0),
        "top_left": (-40, -30),
        "top": (0, -40),
        "top_right": (40, -30),
        "right": (55, 0),
        "bottom_right": (40, 30),
        "bottom": (0, 40),
        "bottom_left": (-40, 30),
        "left": (-55, 0),
    }

    anchor_style = ConnectionStyle(width=1.5, color=colors.secondary, opacity=0.6)

    for name, (dx, dy) in anchor_info.items():
        anchor_pt = rect.anchor(name)
        # Place label dot outward
        label_x = anchor_pt.x + dx * 1.8
        label_y = anchor_pt.y + dy * 1.8
        label_dot = Dot(label_x, label_y, radius=4, color=colors.accent)
        scene.place(label_dot)

        # Connection from rect anchor to label dot
        conn = rect.connect(label_dot, shape=Line(), start_anchor=name, style=anchor_style)
        scene.add_connection(conn)

        # Text label
        text_x = label_x + (15 if dx >= 0 else -15)
        text_y = label_y + (0 if abs(dy) > 0 else 0)
        text_anchor = "start" if dx >= 0 else "end"
        scene.place(
            Text(text_x, text_y, name, font_size=9, color="#aaaacc", text_anchor=text_anchor)
        )

    scene.place(Text(210, 25, "Rect anchors", font_size=13, color=colors.primary, bold=True))
    save(scene, "guide/connections-anchor-showcase.svg")

    # --- 4. Mixed entity types connected ---
    scene = Scene(520, 200, background=colors.background)

    dot = Dot(60, 100, radius=12, color=colors.primary)
    rect = Rect.at_center(
        Coord(190, 100),
        70,
        50,
        fill=colors.secondary,
        opacity=0.4,
        stroke=colors.secondary,
        stroke_width=1.5,
    )
    hex_verts = []
    hx, hy, hr = 340, 100, 30
    for i in range(6):
        angle = math.radians(60 * i - 30)
        hex_verts.append((hx + hr * math.cos(angle), hy + hr * math.sin(angle)))
    poly = Polygon(
        hex_verts, fill=colors.accent, opacity=0.4, stroke=colors.accent, stroke_width=1.5
    )
    ell = Ellipse(
        460,
        100,
        rx=30,
        ry=20,
        fill=colors.primary,
        opacity=0.3,
        stroke=colors.primary,
        stroke_width=1.5,
    )

    for entity in [dot, rect, poly, ell]:
        scene.place(entity)

    link_style = ConnectionStyle(width=1.5, color=colors.line, opacity=0.7)
    arrow_style = ConnectionStyle(width=1.5, color=colors.line, opacity=0.7, end_cap="arrow")

    # Dot → Rect.left
    conn1 = dot.connect(rect, shape=Line(), end_anchor="left", style=link_style)
    # Rect.right → Polygon.v0
    conn2 = rect.connect(
        poly, shape=Line(), start_anchor="right", end_anchor="v0", style=arrow_style
    )
    # Polygon.v3 → Ellipse.left
    conn3 = poly.connect(ell, shape=Line(), start_anchor="v3", end_anchor="left", style=link_style)
    scene.add_connection(conn1)
    scene.add_connection(conn2)
    scene.add_connection(conn3)

    # Labels
    scene.place(Text(60, 140, "Dot", font_size=10, color="#aaaacc"))
    scene.place(Text(190, 145, "Rect", font_size=10, color="#aaaacc"))
    scene.place(Text(340, 150, "Polygon", font_size=10, color="#aaaacc"))
    scene.place(Text(460, 140, "Ellipse", font_size=10, color="#aaaacc"))
    # Anchor labels on connections
    scene.place(Text(125, 85, "center → left", font_size=8, color="#888899"))
    scene.place(Text(260, 85, "right → v0", font_size=8, color="#888899"))
    scene.place(Text(400, 85, "v3 → left", font_size=8, color="#888899"))

    save(scene, "guide/connections-mixed-entities.svg")

    # --- 5. Cap styles comparison ---
    scene = Scene(360, 240, background=colors.background)

    cap_names = ["round", "square", "butt", "arrow", "arrow_in"]
    for i, cap in enumerate(cap_names):
        y = 30 + i * 44
        d1 = Dot(100, y, radius=4, color=colors.primary)
        d2 = Dot(300, y, radius=4, color=colors.primary)
        for _d in [d1, d2]:
            scene.place(_d)

        style = ConnectionStyle(
            width=3,
            color=colors.secondary,
            opacity=0.8,
            start_cap=cap,
            end_cap=cap,
        )
        conn = d1.connect(d2, shape=Line(), style=style)
        scene.add_connection(conn)

        # Label
        scene.place(Text(45, y, cap, font_size=11, color="#aaaacc", text_anchor="end"))

    scene.place(Text(200, 16, "Cap Styles", font_size=12, color=colors.primary, bold=True))
    save(scene, "guide/connections-cap-styles.svg")

    # --- 6. Connections as Pathable ---
    scene = Scene(380, 260, background=colors.background)

    # Three dots forming a triangle
    tri_pts = [
        Coord(190, 40),  # top
        Coord(330, 220),  # bottom-right
        Coord(50, 220),  # bottom-left
    ]
    tri_dots = []
    for pt in tri_pts:
        d = Dot(pt.x, pt.y, radius=8, color=colors.primary)
        scene.place(d)
        tri_dots.append(d)

    edge_style = ConnectionStyle(width=2, color=colors.line, opacity=0.5)
    edges = []
    for i in range(3):
        conn = tri_dots[i].connect(tri_dots[(i + 1) % 3], shape=Line(), style=edge_style)
        scene.add_connection(conn)
        edges.append(conn)

    # Place small marker dots along each edge at t=0.25, 0.5, 0.75
    marker_colors = [colors.accent, colors.secondary, colors.accent]
    for edge in edges:
        for t_val in [0.25, 0.5, 0.75]:
            pt = edge.point_at(t_val)
            marker = Dot(pt.x, pt.y, radius=4, color=colors.accent, opacity=0.9)
            scene.place(marker)
            # Tiny label
            scene.place(Text(pt.x, pt.y - 10, f"{t_val}", font_size=8, color="#aaaacc"))

    scene.place(
        Text(
            190, 250, "point_at(t) places markers along connections", font_size=10, color="#aaaacc"
        )
    )
    save(scene, "guide/connections-as-pathable.svg")

    # --- 7. Constellation creative pattern ---
    random.seed(42)
    scene = Scene(440, 320, background="#0f0f23")

    # Generate random star positions
    positions = [(random.uniform(30, 410), random.uniform(30, 290)) for _ in range(25)]
    star_dots = []
    for x, y in positions:
        d = Dot(x, y, radius=3, color="#e0c3fc", opacity=0.9)
        scene.place(d)
        star_dots.append(d)

    # Connect dots within distance threshold
    for i, d1 in enumerate(star_dots):
        p1 = d1.position
        for j, d2 in enumerate(star_dots[i + 1 :], start=i + 1):
            p2 = d2.position
            dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
            if dist < 130:
                opacity = 0.5 * (1 - dist / 130)
                width = 0.4 + (1 - dist / 130) * 1.2
                style = ConnectionStyle(
                    width=width,
                    color="#a78bfa",
                    opacity=opacity,
                )
                conn = d1.connect(d2, shape=Line(), style=style)
                scene.add_connection(conn)

                # Midpoint marker on longer connections
                if dist > 90:
                    mid = conn.point_at(0.5)
                    scene.place(Dot(mid.x, mid.y, radius=1.5, color="#ffd700", opacity=0.6))

    # A few bright "hub" dots
    for d in star_dots[:3]:
        d.radius = 5
        d.color = "#ffd700"
        d.opacity = 0.8

    save(scene, "guide/connections-constellation.svg")

    # --- 8. Shape comparison (using built-in Path.Wave) ---
    scene = Scene(540, 160, background=colors.background)

    shapes = [
        ("Line", Line()),
        ("Curve", Curve(curvature=0.4)),
        ("Path (wave)", Path(Path.Wave(amplitude=0.3, frequency=3), segments=32)),
    ]

    for i, (label, shape) in enumerate(shapes):
        ox = 20 + i * 180
        d1 = Dot(ox + 20, 75, radius=8, color=colors.primary)
        d2 = Dot(ox + 150, 75, radius=8, color=colors.secondary)
        for _d in [d1, d2]:
            scene.place(_d)
        conn = d1.connect(d2, shape=shape, style=ConnectionStyle(width=2.5, color=colors.accent))
        scene.add_connection(conn)
        scene.place(Text(ox + 85, 135, label, font_size=11, color="#aaaacc"))
        # Subtle code hint
        code = f"shape={label.split()[0]}()"
        if "wave" in label.lower():
            code = "shape=Path(wave)"
        scene.place(Text(ox + 85, 25, code, font_size=9, color="#888899"))

    save(scene, "guide/connections-shape-comparison.svg")

    # --- 9. Invisible connections demo ---
    scene = Scene(400, 150, background=colors.background)

    d1 = Dot(50, 65, radius=12, color=colors.primary)
    d2 = Dot(350, 65, radius=12, color=colors.secondary)
    for _d in [d1, d2]:
        scene.place(_d)

    # Invisible connection (no shape)
    conn = d1.connect(d2)
    scene.add_connection(conn)

    # Place markers via point_at(t) on the invisible connection
    for i in range(9):
        t = i / 8
        pt = conn.point_at(t)
        r = 5 if i in (0, 8) else 3
        scene.place(Dot(pt.x, pt.y, radius=r, color=colors.accent, opacity=0.85))
        if 0 < t < 1:
            scene.place(Text(pt.x, pt.y - 14, f"t={t:.2f}", font_size=7, color="#aaaacc"))

    scene.place(
        Text(
            200,
            130,
            "shape=None — invisible, but point_at(t) still works",
            font_size=10,
            color="#aaaacc",
        )
    )

    save(scene, "guide/connections-invisible.svg")

    # --- 10. Arc network (curved constellation) ---
    random.seed(42)
    scene = Scene(440, 320, background="#0f0f23")

    positions = [(random.uniform(30, 410), random.uniform(30, 290)) for _ in range(25)]
    arc_dots = []
    for x, y in positions:
        d = Dot(x, y, radius=3, color="#e0c3fc", opacity=0.9)
        scene.place(d)
        arc_dots.append(d)

    for i, d1 in enumerate(arc_dots):
        p1 = d1.position
        for j, d2 in enumerate(arc_dots[i + 1 :], start=i + 1):
            p2 = d2.position
            dist = math.hypot(p1.x - p2.x, p1.y - p2.y)
            if dist < 130:
                opacity = 0.5 * (1 - dist / 130)
                width = 0.4 + (1 - dist / 130) * 1.2
                # Vary curvature by angle for organic feel
                angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
                curvature = 0.3 * math.sin(angle * 3 + i * 0.5)
                style = ConnectionStyle(width=width, color="#a78bfa", opacity=opacity)
                conn = d1.connect(d2, shape=Curve(curvature=curvature), style=style)
                scene.add_connection(conn)

                if dist > 90:
                    mid = conn.point_at(0.5)
                    scene.place(Dot(mid.x, mid.y, radius=1.5, color="#ffd700", opacity=0.6))

    for d in arc_dots[:3]:
        d.radius = 5
        d.color = "#ffd700"
        d.opacity = 0.8

    save(scene, "guide/connections-arc-network.svg")

    # --- 11. Flowing tree ---
    scene = Scene(440, 280, background=colors.background)

    # Tree layout: root → 2 children → 4 grandchildren
    levels = [
        [(220, 45)],
        [(120, 135), (320, 135)],
        [(70, 235), (170, 235), (270, 235), (370, 235)],
    ]
    level_colors = [colors.accent, colors.primary, colors.secondary]
    node_dots = []

    for level_idx, level_positions in enumerate(levels):
        level_dots = []
        for x, y in level_positions:
            r = 10 - level_idx * 2
            d = Dot(x, y, radius=r, color=level_colors[level_idx])
            scene.place(d)
            level_dots.append(d)
        node_dots.append(level_dots)

    arc_style = ConnectionStyle(width=2, color=colors.line, opacity=0.6)

    # Root → children
    for child in node_dots[1]:
        curvature = 0.25 if child.position.x < 220 else -0.25
        conn = node_dots[0][0].connect(child, shape=Curve(curvature=curvature), style=arc_style)
        scene.add_connection(conn)

    # Children → grandchildren
    for parent_idx, parent in enumerate(node_dots[1]):
        for child in node_dots[2][parent_idx * 2 : parent_idx * 2 + 2]:
            curvature = 0.2 if child.position.x < parent.position.x else -0.2
            conn = parent.connect(child, shape=Curve(curvature=curvature), style=arc_style)
            scene.add_connection(conn)

    scene.place(
        Text(220, 270, "Flowing tree with curved connections", font_size=10, color="#aaaacc")
    )

    save(scene, "guide/connections-flowing-tree.svg")
