from manim import *
import numpy as np


class MatrixActsOnVectors(Scene):
    def construct(self):
        # -------------------------
        # 1) Symmetric matrix
        # -------------------------
        
        M11 = 3
        M12 = -1
        M21 = M12
        M22 = 1.5
        M = np.array([
            [M11, M12],
            [M21, M22],
        ])

        # -------------------------
        # 2) Vectors x1, x2, x3
        # -------------------------
        xs = [
            np.array([0, 1.0]),
            np.array([-1.0, 0.5]),
            np.array([1, 0]),
        ]
        ys = [M @ v for v in xs]
        colors = [BLUE, PINK, GREEN_B]

        # -------------------------
        # 3) Axes always visible
        # -------------------------
        x_min = -6
        x_max = 6
        y_min = -4
        y_max = 4
        axis_length = 10
        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[y_min, y_max, 1],
            x_length=axis_length,
            y_length=axis_length * (y_max-y_min)/(x_max-x_min),
            axis_config={"include_tip": True},
        ).scale(0.85).to_edge(DR)

        x_label = axes.get_x_axis_label(Tex("x")).scale(0.8)
        y_label = axes.get_y_axis_label(Tex("y")).scale(0.8)

        title = Tex("Consider Matrix-Vector Multiplcation").to_edge(UP)
        M_tex = MathTex(rf"M=\begin{{pmatrix}} {M11} & {M12}\\[3pt] {M21} & {M22}\end{{pmatrix}}").scale(0.9).to_corner(UL, buff = 1.5)        
        rule_tex = MathTex(r"y_i = Mx_i").scale(0.85).next_to(M_tex, DOWN, buff=0.3).align_to(M_tex, LEFT)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(FadeIn(M_tex), FadeIn(rule_tex))
        self.wait(0.3)

        # -------------------------
        # 4) Make "ghost" vectors (static originals)
        # -------------------------
        def arrow_from_vec(v, color, opacity=1.0, width=8):
            return Arrow(
                start=axes.c2p(0, 0),
                end=axes.c2p(v[0], v[1]),
                buff=0,
                color=color,
                stroke_width=width,
                tip_length=0.25,  # fixed tip size
                max_tip_length_to_length_ratio=0.8,
            ).set_opacity(opacity)

        ghost_arrows = VGroup(*[
            arrow_from_vec(xs[i], GREY_A, opacity=0.45, width=5)
            for i in range(3)
        ])

      

        # -------------------------
        # 5) Live arrows whose endpoints we animate (no morphing!)
        # -------------------------
        end_trackers = []
        live_arrows = VGroup()

        for i in range(3):
            tx = ValueTracker(xs[i][0])
            ty = ValueTracker(xs[i][1])
            end_trackers.append((tx, ty))

            arrow = always_redraw(
                lambda i=i, tx=tx, ty=ty: Arrow(
                    start=axes.c2p(0, 0),
                    end=axes.c2p(tx.get_value(), ty.get_value()),
                    buff=0,
                    color=colors[i],
                    stroke_width=8,     # constant width
                    tip_length=0.25,    # constant tip
                    max_tip_length_to_length_ratio=0.8,
                )
            )
            live_arrows.add(arrow)

        # Labels x_i (these disappear during movement)
        labels_x = VGroup(*[
            always_redraw(
                lambda i=i: MathTex(fr"x_{i+1}")
                .scale(0.75)
                .next_to(live_arrows[i].get_end(), normalize(live_arrows[i].get_end() - axes.c2p(0, 0)), buff=0.15)
            )
            for i in range(3)
        ])

        self.play(FadeIn(live_arrows), FadeIn(labels_x), run_time=1.0)
        self.wait(0.4)

        # -------------------------
        # PHASE A: Move arrows only (labels fade out during move)
        # -------------------------
        move_anims = []
        for i in range(3):
            tx, ty = end_trackers[i]
            move_anims.append(tx.animate.set_value(ys[i][0]))
            move_anims.append(ty.animate.set_value(ys[i][1]))

        self.play(FadeOut(labels_x, run_time=0.3))   # disappear during motion
        self.play(FadeIn(ghost_arrows), run_time=0.8)
        self.play(*move_anims, run_time=2.0, rate_func=smooth)

        # Labels y_i (appear after movement)
        labels_y = VGroup(*[
            always_redraw(
                lambda i=i: MathTex(fr"y_{i+1}")
                .scale(0.75)
                .next_to(live_arrows[i].get_end(), normalize(live_arrows[i].get_end() - axes.c2p(0, 0)), buff=0.15)
            )
            for i in range(3)
        ])

        self.play(FadeIn(labels_y), run_time=0.5)
        self.wait(1.0)

        # Clear live arrows for the "repeat with grid"
        self.play(FadeOut(live_arrows), FadeOut(labels_y), run_time=0.8)

        # -------------------------
        # PHASE B: Repeat with light grid underneath
        # -------------------------
        grid = NumberPlane(
           x_range=[x_min, x_max, 1],
            y_range=[y_min, y_max, 1],
            x_length=axis_length,
            y_length=axis_length * (y_max-y_min)/(x_max-x_min),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_opacity": 0.22,
                "stroke_width": 1,
            },
            axis_config={"stroke_opacity": 0},  # hide plane axes; we already have Axes()
        )
        grid.shift(axes.c2p(0, 0) - ORIGIN)

        self.play(FadeIn(grid), run_time=0.8)

        # Rebuild live arrows again at x's
        end_trackers2 = []
        live_arrows2 = VGroup()

        for i in range(3):
            tx = ValueTracker(xs[i][0])
            ty = ValueTracker(xs[i][1])
            end_trackers2.append((tx, ty))

            arrow = always_redraw(
                lambda i=i, tx=tx, ty=ty: Arrow(
                    start=axes.c2p(0, 0),
                    end=axes.c2p(tx.get_value(), ty.get_value()),
                    buff=0,
                    color=colors[i],
                    stroke_width=8,
                    tip_length=0.25,
                    max_tip_length_to_length_ratio=0.8,
                )
            )
            live_arrows2.add(arrow)

        labels_x2 = VGroup(*[
            always_redraw(
                lambda i=i: MathTex(fr"x_{i+1}")
                .scale(0.75)
                .next_to(live_arrows2[i].get_end(), normalize(live_arrows2[i].get_end() - axes.c2p(0, 0)), buff=0.15)
            )
            for i in range(3)
        ])

        self.play(FadeIn(live_arrows2), run_time=1.0)
        self.wait(0.5)

        # Animate arrows by moving endpoints, and grid by ApplyMatrix
        move_anims2 = []
        for i in range(3):
            tx, ty = end_trackers2[i]
            move_anims2.append(tx.animate.set_value(ys[i][0]))
            move_anims2.append(ty.animate.set_value(ys[i][1]))

      #  self.play(FadeOut(labels_x2), run_time=0.3)
        
        self.play(
            ApplyMatrix(M, grid, about_point=axes.c2p(0, 0)),
            *move_anims2,
            run_time=2.2,
            rate_func=smooth,
        )

        labels_y2 = VGroup(*[
            always_redraw(
                lambda i=i: MathTex(fr"y_{i+1}")
                .scale(0.75)
                .next_to(live_arrows2[i].get_end(), normalize(live_arrows2[i].get_end() - axes.c2p(0, 0)), buff=0.15)
            )
            for i in range(3)
        ])
        self.play(FadeIn(labels_y2), run_time=0.5)
        self.wait(5.5)
