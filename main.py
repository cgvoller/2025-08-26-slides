import os
import random
import qrcode
from manim import *
from manim_slides import Slide


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


class VideoAnimation(Animation):
    def __init__(self, video_mobject, **kwargs):
        self.video_mobject = video_mobject
        self.index = 0
        self.dt = 1.0 / len(video_mobject)
        super().__init__(video_mobject, **kwargs)

    def interpolate_mobject(self, dt):
        index = int(dt / self.dt) % len(self.video_mobject)

        if index != self.index:
            self.index = index
            self.video_mobject.pixel_array = self.video_mobject[index].pixel_array

        return self


class VideoMobject(ImageMobject):
    def __init__(self, image_files, **kwargs):
        assert len(image_files) > 0, "Cannot create empty video"
        self.image_files = image_files
        self.kwargs = kwargs
        super().__init__(image_files[0], **kwargs)

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, index):
        return ImageMobject(self.image_files[index], **self.kwargs)

    def play(self, **kwargs):
        return VideoAnimation(self, **kwargs)


class Main(Slide, MovingCameraScene):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        random.seed(1234)

        # Colors
        self.camera.background_color = WHITE
        self.BS_COLOR = BLUE_D
        self.UE_COLOR = MAROON_D
        self.SIGNAL_COLOR = BLUE_B
        self.WALL_COLOR = LIGHT_BROWN
        self.INVALID_COLOR = RED
        self.VALID_COLOR = "#28C137"
        self.IMAGE_COLOR = "#636463"
        self.X_COLOR = DARK_BROWN

        # Coordinates

        self.UL = Dot().to_corner(UL).get_center()
        self.UR = Dot().to_corner(UR).get_center()
        self.DL = Dot().to_corner(DL).get_center()
        self.DR = Dot().to_corner(DR).get_center()

        # Font sizes
        self.TITLE_FONT_SIZE = 48
        self.CONTENT_FONT_SIZE = 0.6 * self.TITLE_FONT_SIZE
        self.SOURCE_FONT_SIZE = 0.2 * self.TITLE_FONT_SIZE

        # Mutable variables

        self.slide_number = Integer(1).set_color(BLACK).to_corner(DR)
        self.slide_title = Text(
            "Contents", color=BLACK, font_size=self.TITLE_FONT_SIZE
        ).to_corner(UL)
        self.add_to_canvas(slide_number=self.slide_number, slide_title=self.slide_title)

        self.tex_template = TexTemplate()
        self.tex_template.add_to_preamble(
            r"""
        \usepackage{siunitx}
        \usepackage{amsmath}
        \newcommand{\ts}{\textstyle}
        """
        )

        
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

    def construct_intro(self):
        # Title
        logo= ImageMobject("Images/logo.png")
        logo.scale(0.05)
        logo.to_corner(DL, buff=0.2)
        self.add_to_canvas(logo=logo)
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
        self.play(FadeIn(title),
                  FadeIn(author,direction=DOWN),
                  FadeIn(date,direction=DOWN)
                  )
        #self.play(self.wipe(self.mobjects_without_canvas, return_animation=True))


         # Contents

        i = Item()

        contents = paragraph(
            f"{i}. Basics of Clinical Trials;",
            f"{i}. Group Sequential Designs;",
            f"{i}. Response-adaptive Randomisation;",
            f"{i}. Bayesian Methods;",
            f"{i}. Simulation Study and Leveraging Uncertainty;",
            f"{i}. Results and Conclusions.",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        ).align_to(self.slide_title, LEFT)

        self.next_slide(notes="Table of contents")
        self.play(
            self.wipe(self.mobjects_without_canvas, [*self.canvas_mobjects, contents], return_animation=True)
        )

    def construct_trialintro(self):
        # Intro to clinical trials

        trialdef = paragraph(
            "A research study conducted with human participants\n"
            "to evaluate medical, surgical, or behavioural interventions.",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        )
        
        box = SurroundingRectangle(
        trialdef,            
        color=BLUE,          
        buff=0.3,            
        corner_radius=0.1    
        ) 
        contents = VGroup(trialdef,box)
        contents.next_to(self.slide_title, DOWN, buff=0.5).align_to(self.slide_title, LEFT)

        self.next_slide(notes="Basics of Clinical Trials")
        self.new_clean_slide("Basics of Clinical Trials")

        #self.play(self.next_slide_number_animation(),
        #          self.wipe(self.mobjects_without_canvas,contents,return_animation=True)
        #          )  
        self.add(trialdef)
        self.play(Create(box),run_time=1.5)
            # --- Circles for Phases ---
        circle_labels = ["Phase I", "Phase II", "Phase III", "Phase IV"]
        descriptions = [
            "Small group testing, safety focus",
            "Larger group, efficacy evaluation",
            "Large-scale testing, confirm results",
            "Post-market surveillance"
        ]

        circles = VGroup(*[
        VGroup(
            Circle(radius=0.6, color=BLUE),
            Tex(label).scale(0.5),
            Tex(desc).scale(0.4).next_to(Tex(label).scale(0.5), DOWN, buff=0.3)
        ).arrange(DOWN, buff=0.2)
            for label, desc in zip(circle_labels, descriptions)
        ])
        circles.arrange(RIGHT, buff=1.5).next_to(contents, DOWN, buff=1)
        circles.move_to([0, circles.get_center()[1], 0])

        for i, phase in enumerate(circles):
            # Animate circle + labels
            self.play(Create(phase), run_time=1.0)
            self.next_slide()  # pause after circle appears

        # Draw arrow to next circle if not last
            if i < len(circles) - 1:
                start = phase[0].get_right()  # circle itself
                end = circles[i + 1][0].get_left()

                arrow = Arrow(start, end, buff=0, color=YELLOW)
                self.play(
                    GrowArrow(arrow),
                    self.camera.frame.animate.move_to(circles[i + 1].get_center()).set(width=7),
                    run_time=1.5
                )
                self.next_slide()  # pause after arrow
    # Zoom out to see all phases
            self.play(self.camera.frame.animate.move_to(ORIGIN).set(width=14), run_time=2)
            self.next_slide()

        self.play(self.next_slide_number_animation(),
            self.wipe(self.mobjects_without_canvas,return_animation=True)
        )    


    def construct_gsdesign(self):
        # Group Sequential Designs
        self.next_slide(notes="Group Sequential Designs")
        self.new_clean_slide("Group Sequential Designs")

         # Boundary
        # Define k values and boundaries (boundaries start at k=1)
        k_values = np.array([0, 1, 2, 3, 4, 5])
        a_crit = np.array([-1.61511306, -0.07126633, 0.81610852, 1.46393433, 1.986610])  # No k=0 boundary
        b_crit = np.array([4.442196, 3.141107, 2.564703, 2.221098, 1.986610])  # No k=0 boundary
        a_crit_ext = np.insert(a_crit, 0, a_crit[0])
        b_crit_ext = np.insert(b_crit, 0, b_crit[0])
        # Observed paths (starting from k=0, y=0)
        observed_red_cross = np.array([0, 1.5, 2.3, 2.7, 4.5])  # Crosses upper boundary
        observed_green_cross = np.array([0, -1.2, -1.8, -2.2, -2.5])  # Crosses lower boundary
        observed_no_cross = np.array([0,1.8, 1, 1.5, 1.8, 2.1])  # Stays within bounds
                # Create axes
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[-3, 5, 1],
            axis_config={"color": BLACK},
            x_axis_config={
                "include_numbers": True,
                "numbers_to_include": [1, 2, 3, 4, 5],
                "decimal_number_config": {"num_decimal_places":0,
                "color": BLACK}
            },
            y_axis_config={
                "include_numbers": True,
                "decimal_number_config": {"color": BLACK}
            }
        )
        #axes.next_to(cohort, DOWN, buff=1.5)
        #axes.shift(RIGHT * 1)
        x = axes.get_x_axis()
        x.numbers.set_color(BLACK)
        x_label = Tex("Analysis (k)").next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = MathTex("Z_k").next_to(axes.y_axis, LEFT, buff=0)
        
        self.play(
            self.camera.frame.animate.move_to(axes)
        )
        self.wait()

        self.play(Create(axes),Write(x_label), Write(y_label))

        # Plot boundaries (starting at k=1)
        a_crit_line = axes.plot_line_graph(
            x_values=k_values[1:], y_values=a_crit, add_vertex_dots=False, line_color=GREEN, stroke_width=4
        )
        b_crit_line = axes.plot_line_graph(
            x_values=k_values[1:], y_values=b_crit, add_vertex_dots=False, line_color=RED, stroke_width=4
        )
        self.play(Create(a_crit_line), Create(b_crit_line))
        # Labels on graph
        reject_text = MathTex(r"\text{Reject } H_0", font_size=28)
        reject_text.move_to(axes.c2p(3, b_crit[2]) + UP * 0.5)
        self.play(Write(reject_text))

        accept_text = MathTex(r"\text{Accept } H_0", font_size=28)
        accept_text.move_to(axes.c2p(4, a_crit[2]))
        self.play(Write(accept_text))
        continue_text = MathTex(r"\text{Continue}", font_size=28)
        continue_text.move_to(axes.c2p(1, 2) + UP * 0.5)
        self.play(Write(continue_text))

        upper_curve = axes.plot_line_graph(
            x_values=k_values[1:], y_values=b_crit,
            add_vertex_dots=False, line_color=RED, stroke_width=0  # Invisible curve
        )

        lower_curve = axes.plot_line_graph(
            x_values=k_values[1:], y_values=a_crit,
            add_vertex_dots=False, line_color=GREEN, stroke_width=0  # Invisible curve
        )
        fill_tracker = ValueTracker(0.0)

        def get_blue_region():
            lower_points = [axes.c2p(x, a) for x, a in zip(k_values[1:], a_crit)]
            upper_points = [axes.c2p(x, a + (b - a) * fill_tracker.get_value())
                    for x, a, b in zip(k_values[1:], a_crit, b_crit)]
            return Polygon(*lower_points, *reversed(upper_points),
                   color=BLUE, fill_opacity=0.2, stroke_opacity=0)

        blue_region = always_redraw(get_blue_region)
        self.add(blue_region)

        def get_left_blue_strip():
            top_y = axes.y_range[1]
            bottom_y = axes.y_range[0]
            k0 = 0
            k1 = 1
            return Polygon(
                axes.c2p(k0, bottom_y),
                axes.c2p(k1, bottom_y),
                axes.c2p(k1, bottom_y + (top_y - bottom_y) * fill_tracker.get_value()),
                axes.c2p(k0, bottom_y + (top_y - bottom_y) * fill_tracker.get_value()),
                color=BLUE, fill_opacity=0.2, stroke_opacity=0
            )

        left_blue_strip = always_redraw(get_left_blue_strip)
        self.add(left_blue_strip)

        def get_red_region():
            top_y = axes.y_range[1]
            upper_points = [axes.c2p(x, b) for x, b in zip(k_values[1:], b_crit)]
            top_points = [axes.c2p(x, b + (top_y - b) * fill_tracker.get_value())
                  for x, b in zip(k_values[1:], b_crit)]
            return Polygon(*upper_points, *reversed(top_points),
                   color=RED, fill_opacity=0.3, stroke_opacity=0)

        red_region = always_redraw(get_red_region)
        self.add(red_region)

        def get_green_region():
            bottom_y = axes.y_range[0]
            lower_points = [axes.c2p(x, a) for x, a in zip(k_values[1:], a_crit)]
            bottom_points = [axes.c2p(x, a + (bottom_y - a) * fill_tracker.get_value())
                     for x, a in zip(k_values[1:], a_crit)]
            return Polygon(*lower_points, *reversed(bottom_points),
                   color=PURE_GREEN, fill_opacity=0.3, stroke_opacity=0)

        green_region = always_redraw(get_green_region)
        self.add(green_region)
        # Add shaded regions in the correct back-to-front order
        #self.add(red_region, green_region, blue_region)
        self.play(fill_tracker.animate.set_value(1.0), run_time=2)
        self.wait()
        self.next_slide()

        boundary_group = VGroup(axes, a_crit_line, b_crit_line, reject_text, accept_text, continue_text,
                        blue_region, red_region, green_region, left_blue_strip, x_label, y_label)
        #everything = VGroup(cohort, treatment_label, control_label, interim_text, chart_group, hsl_variables, boundary_group)
        #target_center = everything.get_center()
        #target_width = everything.width
        #target_height = everything.height
        #zoom_out_factor = max(target_width / config.frame_width, target_height / config.frame_height)
        self.play(
            self.camera.frame.animate.set(width=config.frame_width),
            run_time=1
        )
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas,return_animation=True)
                  )    
        
    def construct_rar(self):
        # RAR
        contents = paragraph(
            "How to compute derivatives?",
            "⟜  symbolically;",
            "⟜  using finite-differences;",
            "⟜  ... with automatic differentiation!",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        ).align_to(self.slide_title, LEFT)

        self.next_slide(notes="Response-Adaptive Randomisation")
        self.new_clean_slide("Response-Adaptive Randomisation")
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas,contents,return_animation=True)
                  ) 


    def construct_bayes(self):
        # Bayesian Methods
        self.next_slide(notes="Bayesian Methods")
        self.new_clean_slide("Bayesian Methods")

        # Bayes formula
        formula = MathTex(
            "P(\\theta \\mid X)",
            "=",
            "{",
            "P(X \\mid \\theta)",
            "\\cdot",
            "P(\\theta)",
            "\\over",
            "P(X)",
            "}"
        ).scale(1.2)

        formula.to_edge(ORIGIN)

        # Group parts
        posterior = formula[0]
        likelihood = formula[3]
        prior = formula[5]
        marginal = formula[7]

        # Annotations
        post_ann = Tex("Posterior (updated belief)").scale(0.6).next_to(posterior, DOWN, buff=0.5)
        like_ann = Tex("Likelihood (model)").scale(0.6).next_to(likelihood, UP, buff=0.5)
        prior_ann = Tex("Prior belief").scale(0.6).next_to(prior, UP, buff=0.5)
        marg_ann = Tex("Normalising constant").scale(0.6).next_to(marginal, DOWN, buff=0.5)

        # Arrows
        arrows = VGroup(
            Arrow(post_ann.get_top(), posterior.get_bottom(), buff=0.1, color=BLUE),
            Arrow(like_ann.get_bottom(), likelihood.get_top(), buff=0.1, color=PURPLE),
            Arrow(prior_ann.get_bottom(), prior.get_top(), buff=0.1, color=RED),
            Arrow(marg_ann.get_top(), marginal.get_bottom(), buff=0.1, color=GREEN),
        )

        # Add items
        self.play(Write(formula))
        self.wait()
        self.play(
            FadeIn(post_ann), GrowArrow(arrows[0])
        )
        self.play(
            FadeIn(like_ann), GrowArrow(arrows[1])
        )
        self.play(
            FadeIn(prior_ann), GrowArrow(arrows[2])
        )
        self.play(
            FadeIn(marg_ann), GrowArrow(arrows[3])
        )
        self.wait(2)

        # Add "Where" explanation
        where_text = VGroup(
            Tex(r"$\theta$ is a parameter of interest").scale(0.6),
            Tex(r"$X$ is the observed data").scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=2)

        self.play(FadeIn(where_text, shift=DOWN))
        self.wait(3)

        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas, [],return_animation=True)
                  )   
        
    def construct_simstudy(self):
        # Simulation Study
        self.next_slide(notes="Simulation Study")
        self.new_clean_slide("Trial Design")



        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas, [])
                  ) 

        # Leveraging Uncertainty
        self.new_clean_slide("Leveraging Uncertainty")
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas, [])
                  ) 

    def construct_results(self):
        # Results
        self.next_slide(notes="Results")
        self.new_clean_slide("GSD + RAR, Sampling Ratios")
        ratios = ImageMobject("Images/ratios.png").scale(0.5)
        buff = 0.5
        title_bottom_y = self.slide_title.get_bottom()[1]
        ratios.set_y(title_bottom_y - buff - ratios.height / 2)
        ratios.set_x(0)      
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas,ratios,return_animation=True)
                  )
        
        self.next_slide(notes="Results")
        self.new_clean_slide("GSD + RAR, Expected Sample Sizes")
        ess = ImageMobject("Images/ess_group.png").scale(0.5)
        title_bottom_y = self.slide_title.get_bottom()[1]
        ess.set_y(title_bottom_y - buff - ess.height / 2)
        ess.set_x(0)        
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas,ess,return_animation=True)
                  )


    def construct_conclusion(self):
        # Conclusion
        self.next_slide(notes="Conclusion")
        self.new_clean_slide("Conclusion")
        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas, [])
                  )   
        
    def construct_qr(self):
        self.next_slide(notes="QR")
        self.new_clean_slide("QR")
        qr = ImageMobject("Images/github_qr.png")
        qr.scale(2)
        qr.move_to(ORIGIN)
        title = Tex("Scan to view presentation code on GitHub").to_edge(DOWN, buff=0.5)
        self.play(FadeIn(qr),run_time=1.5)
        self.wait(2)
        self.play(Write(title))
        self.wait(4)


    def construct(self):
        self.wait_time_between_slides = 0.10
        self.construct_intro()
        self.construct_trialintro()
        self.construct_gsdesign()
        #self.construct_rar()
        self.construct_bayes()
        #self.construct_simstudy()
        self.construct_results()
        #self.construct_conclusion()
        self.construct_qr()