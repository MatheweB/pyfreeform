"""Generate animated SVGs for Guide: Animation.

Every SVG here uses real SMIL animations — open in a browser to see them play.
All examples use relative coordinates via Scene.with_grid and cell add_* methods.
"""

from __future__ import annotations

from pyfreeform import Polygon, Scene, stagger
from pyfreeform.paths import Wave, Zigzag

from wiki._generator import save


def generate():
    # --- 1. Fade: coral dot pulsing opacity ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=240, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_dot(at=(0.5, 0.43), radius=0.2, color="coral") \
        .animate_fade(to=0.0, duration=3.0, easing="ease-in-out",
              bounce=True, repeat=True)
    cell.add_text(".animate_fade(to=0.0, bounce=True)", at=(0.5, 0.88),
                  font_size=0.065, color="gray")
    save(scene, "guide/anim-fade.svg")

    # --- 2. Spin: blue rect spinning forever ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=240, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_rect(at=(0.5, 0.43), width=0.38, height=0.38,
                  fill="dodgerblue", stroke="white", stroke_width=2) \
        .animate_spin(360, duration=2.5, repeat=True, easing="linear")
    cell.add_text(".animate_spin(360, repeat=True)", at=(0.5, 0.88),
                  font_size=0.065, color="gray")
    save(scene, "guide/anim-spin.svg")

    # --- 3. Draw: wave drawing and undrawing ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=360, cell_height=140,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    w, h = cell.width, cell.height
    wave = Wave(start=(w * 0.08, h * 0.4), end=(w * 0.92, h * 0.4),
                amplitude=h * 0.28, frequency=3)
    cell.add_path(wave, width=3, color="limegreen") \
        .animate_draw(duration=2.5, easing="ease-in-out", bounce=True, repeat=True)
    cell.add_text(".animate_draw(bounce=True)", at=(0.5, 0.88),
                  font_size=0.075, color="gray")
    save(scene, "guide/anim-draw.svg")

    # --- 4. Easing: four dots sliding back and forth with different curves ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=440, cell_height=210,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    easing_names = ["linear", "ease-in", "ease-out", "ease-in-out"]
    colors = ["coral", "gold", "skyblue", "mediumpurple"]
    for i, (name, color) in enumerate(zip(easing_names, colors, strict=True)):
        y = 0.12 + i * 0.2
        cell.add_text(name, at=(0.11, y), font_size=0.055, color="gray")
        cell.add_line(start=(0.26, y), end=(0.95, y), width=1, color="#333")
        cell.add_dot(at=(0.26, y), radius=0.035, color=color) \
            .animate_move(to=(0.95, y), duration=3.0, easing=name,
                  bounce=True, repeat=True)
    cell.add_text("all move the same distance in 3s", at=(0.5, 0.95),
                  font_size=0.045, color="#555")
    save(scene, "guide/anim-easing.svg")

    # --- 5. Chaining: rect that fades AND spins simultaneously ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=240, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_rect(at=(0.5, 0.43), width=0.35, height=0.35,
                  fill="mediumpurple", stroke="white", stroke_width=1) \
        .animate_fade(to=0.3, duration=2.0, easing="ease-in-out",
              bounce=True, repeat=True) \
        .animate_spin(360, duration=3.0, repeat=True)
    cell.add_text(".animate_fade(...).animate_spin(360)", at=(0.5, 0.88),
                  font_size=0.065, color="gray")
    save(scene, "guide/anim-chaining.svg")

    # --- 6. Connection draw: curve drawing between dots ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=360, cell_height=120,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    d1 = cell.add_dot(at=(0.1, 0.42), radius=0.04, color="white")
    d2 = cell.add_dot(at=(0.9, 0.42), radius=0.04, color="white")
    conn = d1.connect(d2, curvature=0.4, color="skyblue", width=2)
    conn.animate_draw(duration=2.0, easing="ease-in-out", bounce=True, repeat=True)
    cell.add_text("conn.animate_draw(bounce=True)", at=(0.5, 0.88),
                  font_size=0.085, color="gray")
    save(scene, "guide/anim-connection.svg")

    # --- 7. Generic animate: pulsing dot (radius) ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=240, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_dot(at=(0.5, 0.43), radius=0.06, color="coral") \
        .animate_radius(to=35, duration=1.2, easing="ease-in-out",
                 repeat=True, bounce=True)
    cell.add_text('.animate_radius(to=35, bounce=True)', at=(0.5, 0.88),
                  font_size=0.06, color="gray")
    save(scene, "guide/anim-animate.svg")

    # --- 8. Scale: pulsing circle ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=240, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_dot(at=(0.5, 0.43), radius=0.08, color="tomato") \
        .animate_scale(to=2.0, duration=2.0, easing="ease-in-out",
              bounce=True, repeat=True)
    cell.add_text(".animate_scale(to=2.0, bounce=True)", at=(0.5, 0.88),
                  font_size=0.065, color="gray")
    save(scene, "guide/anim-scale.svg")

    # --- 9. Then: sequential fade → spin ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=300, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    cell.add_rect(at=(0.5, 0.43), width=0.33, height=0.33,
                  fill="gold", stroke="white", stroke_width=1) \
        .animate_fade(to=0.3, duration=1.5, easing="ease-in-out") \
        .then() \
        .animate_spin(360, duration=2.0, easing="ease-in-out")
    cell.add_text(".animate_fade(...).then().animate_spin(360)", at=(0.5, 0.88),
                  font_size=0.06, color="gray")
    save(scene, "guide/anim-then.svg")

    # --- 10. Stagger: row of dots pulsing ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=360, cell_height=140,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    dots = []
    for i in range(6):
        d = cell.add_dot(at=(0.1 + i * 0.15, 0.4), radius=0.08, color="coral")
        dots.append(d)
    stagger(*dots, offset=0.3,
            each=lambda d: d.animate_fade(to=0.0, duration=1.5, easing="ease-in-out",
                                  bounce=True, repeat=True))
    cell.add_text("stagger(*dots, offset=0.3, ...)", at=(0.5, 0.88),
                  font_size=0.065, color="gray")
    save(scene, "guide/anim-stagger.svg")

    # --- 11. Reactive: polygon vertices + connection endpoints animate ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=360, cell_height=160,
                            background="#1a1a2e")
    cell = scene.grid[0][0]

    # Four corner dots for the polygon (left half of cell)
    p1 = cell.add_dot(at=(0.1, 0.12), radius=0.02, color="white")
    p2 = cell.add_dot(at=(0.1, 0.72), radius=0.02, color="white")
    p3 = cell.add_dot(at=(0.42, 0.72), radius=0.02, color="white")
    p4 = cell.add_dot(at=(0.42, 0.12), radius=0.02, color="white")

    # Polygon references the dots — vertices react to their movement
    poly = Polygon([p1, p2, p3, p4], fill="mediumpurple", stroke="white",
                   stroke_width=1, opacity=0.7)
    scene.place(poly)

    # Move dots inward with relative coords — polygon follows
    p1.animate_move(to=(0.2, 0.28), duration=2.0, bounce=True, repeat=True,
            easing="ease-in-out")
    p2.animate_move(to=(0.16, 0.58), duration=2.0, bounce=True, repeat=True,
            easing="ease-in-out")
    p3.animate_move(to=(0.48, 0.58), duration=2.0, bounce=True, repeat=True,
            easing="ease-in-out")
    p4.animate_move(to=(0.52, 0.28), duration=2.0, bounce=True, repeat=True,
            easing="ease-in-out")

    # Connection between two moving dots (right half)
    d1 = cell.add_dot(at=(0.62, 0.2), radius=0.03, color="coral")
    d2 = cell.add_dot(at=(0.92, 0.7), radius=0.03, color="gold")
    conn = d1.connect(d2, color="skyblue", width=2)
    d1.animate_move(to=(0.75, 0.7), duration=2.5, bounce=True, repeat=True,
            easing="ease-in-out")
    d2.animate_move(to=(0.8, 0.18), duration=2.5, bounce=True, repeat=True,
            easing="ease-in-out")

    cell.add_text("vertices + endpoints react to .animate_move()", at=(0.5, 0.92),
                  font_size=0.06, color="gray")
    save(scene, "guide/anim-reactive.svg")

    # --- 12. Showcase: everything together ---
    scene = Scene.with_grid(cols=1, rows=1, cell_width=460, cell_height=300,
                            background="#1a1a2e")
    cell = scene.grid[0][0]
    w, h = cell.width, cell.height

    # Self-drawing connection across the top
    da = cell.add_dot(at=(0.06, 0.12), radius=0.012, color="white")
    db = cell.add_dot(at=(0.94, 0.12), radius=0.012, color="white")
    cn = da.connect(db, curvature=0.3, color="coral", width=2)
    cn.animate_draw(duration=2.0, delay=0.3, easing="ease-in-out",
            bounce=True, repeat=True)

    # Spinning rect with pulsing opacity
    cell.add_rect(at=(0.17, 0.43), width=0.1, height=0.16,
                  fill="mediumpurple", stroke="white", stroke_width=1) \
        .animate_spin(360, duration=3.0, repeat=True) \
        .animate_fade(to=0.3, duration=2.0, easing="ease-in-out",
              bounce=True, repeat=True)

    # Pulsing dot
    cell.add_dot(at=(0.43, 0.43), radius=0.025, color="coral") \
        .animate_radius(to=28, duration=1.5, easing="ease-in-out",
                 repeat=True, bounce=True)

    # Fading dot
    cell.add_dot(at=(0.74, 0.43), radius=0.06, color="gold") \
        .animate_fade(to=0.0, duration=3.0, easing="ease-in-out",
              bounce=True, repeat=True)

    # Self-drawing zigzag
    zz = Zigzag(start=(w * 0.06, h * 0.77), end=(w * 0.48, h * 0.77),
                amplitude=h * 0.07, teeth=5)
    cell.add_path(zz, width=2, color="skyblue") \
        .animate_draw(duration=2.0, easing="ease-in-out",
              bounce=True, repeat=True)

    # Self-drawing wave
    wv = Wave(start=(w * 0.52, h * 0.77), end=(w * 0.96, h * 0.77),
              amplitude=h * 0.07, frequency=3)
    cell.add_path(wv, width=2, color="limegreen") \
        .animate_draw(duration=2.5, delay=0.5, easing="ease-in-out",
              bounce=True, repeat=True)

    # Row of spinning squares
    sq_colors = ["coral", "gold", "skyblue", "limegreen", "mediumpurple"]
    for i, c in enumerate(sq_colors):
        rx = 0.22 + i * 0.15
        cell.add_rect(at=(rx, 0.93), width=0.03, height=0.045,
                      fill=c) \
            .animate_spin(360, duration=1.5 + i * 0.3, repeat=True, easing="linear")

    save(scene, "guide/anim-showcase.svg")


if __name__ == "__main__":
    generate()
