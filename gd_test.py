import numpy as np
from manim import *


class GDQuadraticUpperBound1D(Scene):
    def construct(self):
        # -----------------------------
        # 1) Define a "generic" function
        # -----------------------------
        # Cubic polynomial (nice curvature)
        # f(x) = 0.2 x^3 + 0.5 x^2 + 0.2 x + 1
        # f'(x) = 0.6 x^2 + x + 0.2
        # f''(x) = 1.2 x + 1
        #
        # On [-3, 3], max |f''(x)| <= max(|1.2x+1|)
        # = max( |4.6|, | -2.6| ) = 4.6, so L=5 works.
        #
        L = 6
        a = 0.3
        b = -1
        c = 0.5
        d = 2.4
        
        def f(x):
            return a * x**3 + b * x**2 + c * x + d

        def grad(x):
            return 3*a * x**2 + 2*b*x + c

        # Domain where we claim L-smoothness
        x_min, x_max = -1, 4
        y_max = 8
        # -----------------------------
        # 2) Axes + function graph
        # -----------------------------
        axes = Axes(
            x_range=[x_min, x_max, 1],
            y_range=[-1, y_max, 1],
            x_length=6,
            y_length=5,
            axis_config={"include_tip": True},
        ).to_corner(DR)

        x_label = axes.get_x_axis_label(Tex("x")).scale(0.8)
        y_label = axes.get_y_axis_label(Tex("f(x)")).scale(0.8)

        f_graph = axes.plot(lambda t: f(t), x_range=[x_min, x_max], stroke_width=4)

        title = Tex(r"Gradient Descent as Minimizing a Quadratic Upper Bound").to_edge(UP)

        self.play(Write(title))
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))
        self.play(Create(f_graph))
        self.wait(0.5)

        # -----------------------------
        # 3) Display formulas
        # -----------------------------
        formula1 = MathTex(
            r"q_k(y)= f(x_k)+f'(x_k)(y-x_k)+\frac{L}{2}(y-x_k)^2"
        ).scale(0.75)
        formula2 = MathTex(
            r"y^\star=\arg\min_y q_k(y)=x_k-\frac{1}{L}f'(x_k)"
        ).scale(0.75)

        formulas = VGroup(formula1, formula2).arrange(DOWN, aligned_edge=LEFT).to_corner(UL, buff = 1)

        self.play(Write(formulas))
        self.wait(0.5)

        # -----------------------------
        # 4) Choose a starting point x_k
        # -----------------------------
        xk = ValueTracker(3.4)

        def q(y, x0):
            # Quadratic upper bound at x0:
            return f(x0) + grad(x0) * (y - x0) + 0.5 * L * (y - x0) ** 2

        # Helper: minimizer of quadratic
        def y_star(x0):
            return x0 - grad(x0) / L

        # -----------------------------
        # 5) Always-redraw objects
        # -----------------------------
        # Dot at (x_k, f(x_k))
        xk_dot = always_redraw(
            lambda: Dot(axes.c2p(xk.get_value(), f(xk.get_value())), radius=0.07)
        )

        xk_label = always_redraw(
            lambda: MathTex(r"x_k").scale(0.7).next_to(xk_dot, UP, buff=0.15)
        )

        # Quadratic upper bound curve q_k(y)
        x_val = xk.get_value()
        A = L/2
        B = grad(x_val) - L*x_val
        C = L/2*(x_val**2)-grad(x_val)*x_val + f(x_val) - y_max
        x_min_quad = (-B-np.sqrt(B**2-4*A*C))/(2*A)
        x_max_quad = (-B+np.sqrt(B**2-4*A*C))/(2*A)

        q_graph = always_redraw(
            lambda: axes.plot(
                lambda t: q(t, xk.get_value()),
                x_range=[x_min_quad, x_max_quad],
                stroke_width=3,
                color = RED,
            )
        )

        q_label = always_redraw(
            lambda: MathTex(r"q_k(y)").scale(0.7).next_to(q_graph, UP, buff=0.2)
        )

        # Minimizer y* of the quadratic
        ystar_dot = always_redraw(
            lambda: Dot(
                axes.c2p(y_star(xk.get_value()), q(y_star(xk.get_value()), xk.get_value())),
                radius=0.07,
                color=YELLOW,
            )
        )

        ystar_label = always_redraw(
            lambda: MathTex(r"y^\star").scale(0.7).next_to(ystar_dot, UP, buff=0.45)
        )

        # Vertical "drop" from quadratic minimizer down to the function
        drop_line = always_redraw(
            lambda: DashedLine(
                axes.c2p(y_star(xk.get_value()), q(y_star(xk.get_value()), xk.get_value())),
                axes.c2p(y_star(xk.get_value()), f(y_star(xk.get_value()))),
                dash_length=0.08,
                color=GREY_B,
            )
        )

        # Next iterate point on function: (x_{k+1}, f(x_{k+1})) where x_{k+1}=y*
        xkp1_dot = always_redraw(
            lambda: Dot(
                axes.c2p(y_star(xk.get_value()), f(y_star(xk.get_value()))),
                radius=0.07,
                color=YELLOW,
            )
        )

        xkp1_label = always_redraw(
            lambda: MathTex(r"x_{k+1}").scale(0.7).next_to(xkp1_dot, DOWN, buff=0.45)
        )

        # Optional: show the tangent line at x_k
        tangent_line = always_redraw(
            lambda: axes.plot(
                lambda t: f(xk.get_value()) + grad(xk.get_value()) * (t - xk.get_value()),
                x_range=[x_min, x_max],
                stroke_width=3,
                color=BLUE,
            )
        )
        tangent_label = always_redraw(
            lambda: MathTex(r"\text{tangent}").scale(0.6).set_color(BLUE).next_to(
                tangent_line, DOWN, buff=0.2
            )
        )

        # L value display
        # L_text = Tex(rf"Choose $L={int(L)}$ so $|f''(x)|\le L$ on $[-3,3]$").scale(0.65)
        # L_text.to_corner(UR)

        # -----------------------------
        # 6) Animate in the objects
        # -----------------------------
      #  self.play(FadeIn(L_text))
        self.play(FadeIn(xk_dot), FadeIn(xk_label))
        self.wait(0.4)

        self.play(Create(tangent_line), FadeIn(tangent_label))
        self.wait(0.4)

        self.play(Create(q_graph), FadeIn(q_label))
        self.wait(0.4)

        self.play(FadeIn(ystar_dot), FadeIn(ystar_label))
        self.play(Create(drop_line))
        self.play(FadeIn(xkp1_dot), FadeIn(xkp1_label))
        self.wait(1.0)

        # -----------------------------
        # 7) "Update" iterate: move x_k to x_{k+1}
        # -----------------------------
        step_text = MathTex(
            r"x_{k+1}=x_k-\frac{1}{L}f'(x_k)"
        ).scale(0.8).next_to(formulas, DOWN, buff=0.3).align_to(formulas, LEFT)

        self.play(Write(step_text))
        self.wait(0.5)

        # Animate xk -> ystar(xk)
        new_x = y_star(xk.get_value())
        self.play(
            xk.animate.set_value(new_x),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(1.0)

        # Emphasize that the dot is now at the next iterate
        highlight = SurroundingRectangle(xkp1_dot, buff=0.15, color=YELLOW)
        self.play(Create(highlight))
        self.wait(1.0)
        
        
        self.wait(3.5)
