from manim import *

class LatexTest(Scene):
    def construct(self):
        eq = MathTex(r"\int_0^1 x^2\,dx = \frac{1}{3}")
        self.play(Write(eq))
        self.wait()