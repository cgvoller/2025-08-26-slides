import numpy as np
import sympy as sy
import random
from manim import *
from manim_slides import Slide
from scipy.stats import norm

def row(*args):
    """Create a symbol row (or col) vector from input arguments."""
    return sy.Matrix(args)


"""
Here, because I switched the background from black to white,
so I have to make default color for most things to be black (instead of white).
"""


def black(func):
    """Sets default color to black"""

    def wrapper(*args, color=BLACK, **kwargs):
        return func(*args, color=color, **kwargs)

    return wrapper


Tex = black(Tex)
Text = black(Text)
MathTex = black(MathTex)
Line = black(Line)
Dot = black(Dot)
Brace = black(Brace)
Arrow = black(Arrow)
Angle = black(Angle)


class Item:
    def __init__(self, initial=1):
        self.value = initial

    def __repr__(self):
        s = repr(self.value)
        self.value += 1
        return s

def paragraph(*strs, alignment=LEFT, direction=DOWN, **kwargs):
    texts = VGroup(*[Text(s, **kwargs) for s in strs]).arrange(direction)

    if len(strs) > 1:
        for text in texts[1:]:
            text.align_to(texts[0], direction=alignment)

    return texts
"""
Slides generation
"""

class Main(Slide,MovingCameraScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slide_no = None
        self.slide_text = None

    def write_slide_number(self, inital=1, text=Tex, animation=Write, position=ORIGIN):
        self.slide_no = inital
        self.slide_text = text(str(inital)).shift(position)
        return animation(self.slide_text)

    def update_slide_number(self, text=Tex, animation=Transform):
        self.slide_no += 1
        new_text = text(str(self.slide_no)).move_to(self.slide_text)
        return animation(self.slide_text, new_text)
    
    def next_slide_number_animation(self):
        return self.slide_number.animate(run_time=0.5).set_value(
            self.slide_number.get_value() + 1
        )

    def next_slide_title_animation(self, title):
        return Transform(
            self.slide_title,
            Text(title, color=BLACK, font_size=self.TITLE_FONT_SIZE)
            .move_to(self.slide_title)
            .align_to(self.slide_title, LEFT),
        )
    def new_clean_slide(self, title, contents=None):
        if self.mobjects_without_canvas:
            self.play(
                self.next_slide_number_animation(),
                self.next_slide_title_animation(title),
                self.wipe(
                    self.mobjects_without_canvas,
                    contents if contents else [],
                    return_animation=True,
                ),
            )
        else:
            self.play(
                self.next_slide_number_animation(),
                self.next_slide_title_animation(title),
            )

    def construct(self):
        self.camera.background_color = WHITE
        WALL_COLOR = ORANGE
        BS_COLOR = BLUE
        UE_COLOR = "#201E1E"
        GOOD_COLOR = "#28C137"
        BAD_COLOR = "#FF0000"
        IMAGE_COLOR = "#636463"
        X_COLOR = DARK_BROWN

        NW = Dot().to_corner(UL)
        NE = Dot().to_corner(UR)
        SW = Dot().to_corner(DL)
        SE = Dot().to_corner(DR)
        NL = Line(NW.get_center(), NE.get_center()).set_color(WALL_COLOR)
        SL = Line(SW.get_center(), SE.get_center()).set_color(WALL_COLOR)
        WL = Line(NW.get_center(), SW.get_center()).set_color(WALL_COLOR)
        EL = Line(NE.get_center(), SE.get_center()).set_color(WALL_COLOR)

        self.TITLE_FONT_SIZE = 36
        self.CONTENT_FONT_SIZE = 0.6 * self.TITLE_FONT_SIZE
        self.SOURCE_FONT_SIZE = 0.2 * self.TITLE_FONT_SIZE

        # Mutable variables

        self.slide_number = Integer(1).set_color(BLACK).to_corner(DR)
        self.slide_title = Text(
            "Contents", color=BLACK, font_size=self.TITLE_FONT_SIZE
        ).to_corner(UL)
        self.add_to_canvas(slide_number=self.slide_number, slide_title=self.slide_title)

        slide_no_pos = SE.shift(0.15 * RIGHT + 0.2 * DOWN).get_center()

        # TeX Preamble
        tex_template = TexTemplate()
        tex_template.add_to_preamble(
            r"""
\usepackage{fontawesome5}
\usepackage{siunitx}
\DeclareSIQualifier\wattref{W}
\DeclareSIUnit\dbw{\decibel\wattref}
\usepackage{amsmath,amssymb,amsfonts,mathtools}
\newcommand{\bs}{\boldsymbol}
\newcommand{\scp}[3][]{#1\langle #2, #3 #1\rangle}
\newcommand{\bb}{\mathbb}
\newcommand{\cl}{\mathcal}
"""
        )

        # Slide: Title
        logo= ImageMobject("Images/logo.png")
        logo.scale(0.05)
        logo.to_corner(DL, buff=0.2)
        self.add(logo)
        line1 = Text("Leveraging Posterior Uncertainty of Treatment Effects", color=BLACK).scale(0.5)
        line2 = Text("in Bayesian Response-Adaptive Group Sequential Designs", color=BLACK).scale(0.5)
        title = VGroup(line1, line2).arrange(DOWN, buff=0.1).move_to(ORIGIN)
        author = (
            Text("Corey Voller", color=BLACK)
            .scale(0.4)
            .next_to(title, DOWN)
        )
        date = (
            Text("August 26th 2025", color=BLACK)
            .scale(0.4)
            .next_to(author, DOWN)
        )

        self.play(FadeIn(title),FadeIn(author,direction=DOWN),FadeIn(date,direction=DOWN),self.write_slide_number(position=slide_no_pos))
        self.next_slide()

        self.wipe(
            [],
            Text(
                "x",
                color=BLACK,
                font_size=self.CONTENT_FONT_SIZE,
            ).shift(3 * DOWN),
        )

        # Contents

        i = Item()

        contents = paragraph(
            f"{i}. Basics of Clinical Trials;",
            f"{i}. Group Sequential Designs;",
            f"{i}. Response-adaptive Randomisation;",
            f"{i}. Bayesian Methods;",
            f"{i}. Simulation Study and Leveraging Uncertainty;",
            f"{i}. Results/Closing Thoughts.",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        ).align_to(self.slide_title, LEFT)

        self.next_slide(notes="Table of contents")
        self.wipe(self.mobjects_without_canvas, [*self.canvas_mobjects, contents])

        # Intro to clinical trials
        self.next_slide(notes="Basics of Clinical Trials")
        slide_number = self.update_slide_number()
        self.play(slide_number,
                  self.wipe(self.mobjects_without_canvas, [])
                  )
