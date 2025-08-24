import os
import random
#import qrcode
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
        self.next_slide(notes="Basics of Clinical Trials")
        self.new_clean_slide("Basics of Clinical Trials")
        self.camera.frame.save_state()

        trialdef = paragraph(
            "A research study conducted with human participants\n"
            "to evaluate medical, surgical, or behavioural interventions.",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        )
        box = SurroundingRectangle(trialdef, color=BLUE, buff=0.3, corner_radius=0.1)
        contents = VGroup(trialdef, box)
        contents.next_to(self.slide_title, DOWN, buff=0.5).align_to(self.slide_title, LEFT)

        self.add(trialdef)
        self.play(Create(box), run_time=1.5)
        self.next_slide()
        # Phase labels + simple text lines
        phase_info = [
            ("Phase I", ["Evaluate safety", "Determine dosage"]),
            ("Phase II", ["Further evaluate safety", "Test efficacy"]),
            ("Phase III", ["Larger scale confirmatory trial", "Compare to other treatments"]),
            ("Phase IV", ["Post marketing surveillance"]),
        ]

        circles = VGroup()
        for phase, lines in phase_info:
            circle = Circle(radius=0.5, color=BLUE)
            label = Text(phase, font_size=20)
            text_lines = VGroup(*[Text(line, font_size=16) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.05)

            # Stack circle + label first
            top_group = VGroup(circle, label).arrange(DOWN, buff=0.1)
            # Then add text below
            phase_group = VGroup(top_group, text_lines).arrange(DOWN, buff=0.1)
            circles.add(phase_group)

        # Arrange horizontally by **circle centers only**
        circles.arrange(RIGHT, buff=2)
        for pg in circles:
            circle = pg[0][0]     # the circle inside the top_group
            label = pg[0][1]      # the label
            text_lines = pg[1]    # the text lines group

            # Move circle baseline to same y-coordinate
            circle.move_to([circle.get_center()[0], 0, 0])  # align all circles to y=0
            # Position label and text relative to circle
            label.next_to(circle, DOWN, buff=0.1)
            text_lines.next_to(label, DOWN, buff=0.05)

        # Scale to fit width if needed
        circles.scale_to_fit_width(config.frame_width - 2)
        circles.next_to(contents, DOWN, buff=1)

        # --- Show first circle + text ---
        self.play(FadeIn(*circles[0].submobjects), run_time=1.2)
        self.play(self.camera.frame.animate.move_to(circles[0][0][0].get_center()).set(width=5), run_time=1.5)
        self.next_slide()

        # Animate arrows + next phases
        for i in range(len(circles) - 1):
            start = circles[i][0][0].get_right()  # circle right
            end = circles[i + 1][0][0].get_left()  # next circle left
            arrow = Arrow(start, end, buff=0, color=YELLOW)
            self.play(
                AnimationGroup(
                    GrowArrow(arrow),
                    self.camera.frame.animate.move_to(circles[i + 1][0][0].get_center()),
                    FadeIn(*circles[i + 1].submobjects),
                    lag_ratio=0
                ),
                run_time=1.5
            )
            self.next_slide()

        # Zoom out to full view
        self.play(Restore(self.camera.frame), run_time=1)
        self.next_slide()
        #self.play(self.wipe(self.mobjects_without_canvas, return_animation=True))
   


    def construct_gsdesign(self):
        # Group Sequential Designs
        self.next_slide(notes="Group Sequential Designs")
        self.new_clean_slide("Group Sequential Designs")

        line1 = Text("Data is accumulated in blocks of K analyses", font_size=28)
        line2 = MathTex(r"Z_k = \hat{\theta}_k \sqrt{1 / Var_k(\theta)}", font_size=32)
        line3 = Text("Allows for stopping for futility or efficacy at each analysis", font_size=28)

        explanation = VGroup(line1, line2, line3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        explanation.next_to(self.slide_title, DOWN)
        explanation.align_to(self.slide_title, LEFT)
        # Animate lines one by one
        for line in explanation:
            self.play(Write(line))
            self.wait(1)

        self.next_slide()
        # Boundary
        # Define k values and boundaries (boundaries start at k=1)
        k_values = np.array([0, 1, 2, 3, 4, 5])
        a_crit = np.array([-1.61511306, -0.07126633, 0.81610852, 1.46393433, 1.986610])  
        b_crit = np.array([4.442196, 3.141107, 2.564703, 2.221098, 1.986610])  
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
        axes_center_y = explanation.get_bottom()[1] - axes.height/2 - 0.2  
        axes.move_to([0, axes_center_y, 0])
        x_label = Tex("Analysis (k)").next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = MathTex("Z_k").next_to(axes.y_axis, LEFT, buff=0)
        self.play(
            self.camera.frame.animate.move_to(axes)
        )
        self.wait(1)

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
            add_vertex_dots=False, line_color=RED, stroke_width=0  
        )

        lower_curve = axes.plot_line_graph(
            x_values=k_values[1:], y_values=a_crit,
            add_vertex_dots=False, line_color=GREEN, stroke_width=0 
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
        # Function to animate each scenario
        def animate_path(observed_values):
            observed_dot = Dot(axes.c2p(k_values[0], observed_values[0]), color=BLUE)
            self.add(observed_dot)

            prev_point = axes.c2p(k_values[0], observed_values[0])
            line_segments = []
            for i in range(1, len(k_values)):
                target_point = axes.c2p(k_values[i], observed_values[i])
                new_line = Line(prev_point, target_point, color=BLUE)
                line_segments.append(new_line)

                self.play(observed_dot.animate.move_to(target_point), Create(new_line), run_time=1)

                # Check only for k >= 1 (boundaries start at k=1)
                if i >= 1:
                    print(f"k = {k_values[i]}, observed = {observed_values[i]}, a_crit = {a_crit[i-1]}, b_crit = {b_crit[i-1]}")

                    if observed_values[i] > b_crit[i-1]:  # Crossed upper boundary
                        new_line.set_color(RED)
                        self.play(observed_dot.animate.set_color(RED), new_line.animate.set_color(RED), run_time=0.5)
                        break
                    elif observed_values[i] < a_crit[i-1]:  # Crossed lower boundary
                        new_line.set_color(GREEN)
                        self.play(observed_dot.animate.set_color(GREEN), new_line.animate.set_color(GREEN), run_time=0.5)
                        break

                prev_point = target_point

            self.wait(1)
            self.play(*[FadeOut(obj) for obj in line_segments], FadeOut(observed_dot))

        # Run all three scenarios separately
        animate_path(observed_red_cross)  # Scenario 1: Turns red
        animate_path(observed_green_cross)  # Scenario 2: Turns green
        animate_path(observed_no_cross)  # Scenario 3: Final analysis
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
        self.next_slide()
        full_slide_center = (0,0,0)
        # Target width for plot scaling
        scale_factor = 0.75

        # Compute the new vertical position so the top of the plot stays just below the explanation text
        text_bottom_y = explanation.get_bottom()[1] 
        plot_height = boundary_group.height * scale_factor
        target_center_y = text_bottom_y - plot_height/2 - 0.3 
        target_center = np.array([0, target_center_y, 0])

        self.play(
            self.camera.frame.animate.move_to(ORIGIN).set(width=config.frame_width),
            boundary_group.animate.scale(scale_factor).move_to(target_center),
            run_time=1.5
        )
        self.next_slide()
        
    def construct_rar(self):
        # RAR
        self.next_slide(notes="Response-Adaptive Randomisation")
        self.new_clean_slide("Response-Adaptive Randomisation")
        # Import svg
        cohort = VGroup()
        for i in range(-2, 3):
            for j in range(-1, 3):
                cohort.add(
                    SVGMobject("Images/person.svg", fill_color=BLACK,opacity=1)
                    .scale(0.25)
                    .shift(i * UP + j * LEFT)
                )
        cohort.shift(3 * LEFT)

        # Add and fade in cohort
        self.add(cohort)
        self.play(FadeIn(cohort))
        self.next_slide()
        label_x = 1.5

        treatment_label = Text("Treatment").shift(UP * 2)
        control_label = Text("Control").shift(DOWN * 2)

        treatment_label.align_to(np.array([label_x, 0, 0]), LEFT)
        control_label.align_to(np.array([label_x, 0, 0]), LEFT)

        self.add(treatment_label, control_label)
        self.play(FadeIn(treatment_label), FadeIn(control_label))

         # Starting point: middle right edge of the cohort
        start_point = cohort.get_right()

        # Arrows going from the middle right of cohort outward forming a sideways V
        arrow_to_treatment = Arrow(
            start=start_point,
            end=treatment_label.get_left() + LEFT * 0.3,
            buff=0,
            stroke_width=3
        )

        arrow_to_control = Arrow(
            start=start_point,
            end=control_label.get_left() + LEFT * 0.3,
            buff=0,
            stroke_width=3
        )

        # Labels
        p_label = MathTex("p", font_size=28, color=BLACK)
        one_minus_p_label = MathTex("1 - p", font_size=28, color=BLACK)

        # Position p_label above the first arrow
        p_label.next_to(arrow_to_treatment, UP, buff=0.2)

        # Position 1 - p label below the second arrow
        one_minus_p_label.next_to(arrow_to_control, DOWN, buff=0.2)

        self.play(GrowArrow(arrow_to_treatment),
                  GrowArrow(arrow_to_control),
                  Write(p_label),
                  Write(one_minus_p_label))
        self.wait(0.5)

        self.next_slide()

        for idx, person in enumerate(cohort):
            # Clear existing fills and strokes on all submobjects inside each SVG
            for submob in person.submobjects:
                submob.set_fill(opacity=0)
                submob.set_stroke(width=0)

            if idx < 10:
                person.set_fill(RED, opacity=1)
            else:
                person.set_fill(BLUE, opacity=1)

        self.play(
            *[person.animate.set_fill(person.get_fill_color(), opacity=1) for person in cohort]
        )

        self.next_slide()
        # Step 1: Camera pans to the right
        self.play(self.camera.frame.animate.shift(RIGHT * 6))  # Adjust shift as needed

        # Step 2: Add the new title
        interim_text = Text("Interim Analysis I", font_size=28, color=BLACK)
        interim_text.move_to(self.camera.frame.get_right() + LEFT * 4)
        self.play(FadeIn(interim_text))

        # Step 3: Draw arrows from Treatment and Control to Interim Analysis I
        arrow_from_treatment = Arrow(
            start=treatment_label.get_right(),
            end=interim_text.get_left() + UP * 0.5,
            buff=0.1,
            stroke_width=3
        )

        arrow_from_control = Arrow(
            start=control_label.get_right(),
            end=interim_text.get_left() + DOWN * 0.5,
            buff=0.1,
            stroke_width=3
        )

        self.play(GrowArrow(arrow_from_treatment), GrowArrow(arrow_from_control))
        self.next_slide()  
        p = 0.5  # Example probability
        chart = BarChart(
            values=[p * 100, (1 - p) * 100],  # Convert to percentages
            y_range=[0, 100, 10],
            y_length=3,
            x_length=2.5,
            bar_names=["T", "C"],
            y_axis_config={
                "decimal_number_config": {
                    "unit": "\\%",
                    "num_decimal_places": 0,
                    "color": BLACK
               },
               "color": BLACK
           },
           x_axis_config={"color": BLACK}
        )
        bar_names_labels = VGroup()
        chart.move_to(interim_text.get_bottom()+ DOWN*1.5)
        y_label = Text("Allocation Prob (%)", font_size=24).rotate(PI / 2)
        y_label.next_to(chart.y_axis, LEFT, buff=0.1)  # Position to the left of Y-axis
        self.add(y_label)

        h_lines = VGroup(*[
           Line(chart.c2p(0, x), chart.c2p(3, x), stroke_width=1)
           for x in range(0, 110, 10)
        ])
        h_lines.set_opacity(0)
        h_r, s_r = chart.bars
        s_r.set_color(RED)

        chart_group = VGroup(chart, h_lines, y_label)
        chart_group.scale(0.7)
        self.add(chart_group)
        #self.add(chart, h_lines, *chart.bars)
        self.chart = chart
        self.h_lines = h_lines

        # Decimal values for percentages
        h_dn = DecimalNumber(p * 100, color=BLACK,font_size=24)
        s_dn = DecimalNumber((1 - p) * 100, color=BLACK,font_size=24)
        hsl_variables = VGroup(h_dn, s_dn)

        def chart_updater(mob: BarChart):
            hb, sb = mob.bars
            new_vals = [h_dn.get_value(), s_dn.get_value()]
            mob.change_bar_values(new_vals)

    # Position & update color of number labels
            h_dn.next_to(hb, UP, buff=0.1)
            s_dn.next_to(sb, UP, buff=0.1)
            h_dn.set_color(BLACK)
            s_dn.set_color(BLACK)

        chart.add_updater(chart_updater, call_updater=True)
        self.add(chart, hsl_variables)

    # Animate change in probability
        self.play(
            ChangeDecimalToValue(h_dn, 70),
            ChangeDecimalToValue(s_dn, 30),
         run_time=2
        )
        self.play(
            ChangeDecimalToValue(h_dn, 40),
            ChangeDecimalToValue(s_dn, 60),
            run_time=2
        )
        self.wait()
        self.next_slide()
        self.play(
            self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN),
            run_time=2  # Optional: adjust duration
        )
        #self.play(self.next_slide_number_animation(),
        #          self.wipe(self.mobjects_without_canvas,return_animation=True)
        #          )
        


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
        # Boxes around formula parts with faint fill
        post_box = SurroundingRectangle(formula[0], color=BLUE, buff=0.15)\
            .set_fill(BLUE, opacity=0.1)
        like_box = SurroundingRectangle(formula[3], color=PURPLE, buff=0.15)\
            .set_fill(PURPLE, opacity=0.1)
        prior_box = SurroundingRectangle(formula[5], color=RED, buff=0.15)\
            .set_fill(RED, opacity=0.1)
        marg_box = SurroundingRectangle(formula[7], color=GREEN, buff=0.15)\
            .set_fill(GREEN, opacity=0.1)
        

        # Annotation texts
        post_ann = Tex("Posterior (updated belief)").scale(0.6).next_to(post_box, DOWN, buff=0.6)
        like_ann = Tex("Likelihood (model)").scale(0.6).next_to(like_box, UP, buff=0.6)
        prior_ann = Tex("Prior belief").scale(0.6).next_to(prior_box, UP, buff=0.6)
        marg_ann = Tex("Normalising constant").scale(0.6).next_to(marg_box, DOWN, buff=0.6)

        # Arrows from annotation to formula part
        arrows = VGroup(
            Arrow(post_ann.get_top(), post_box.get_bottom(), buff=0.1, color=BLUE),
            Arrow(like_ann.get_bottom(), like_box.get_top(), buff=0.1, color=PURPLE),
            Arrow(prior_ann.get_bottom(), prior_box.get_top(), buff=0.1, color=RED),
            Arrow(marg_ann.get_top(), marg_box.get_bottom(), buff=0.1, color=GREEN),
        )

        # Step 1: Write formula
        self.play(Write(formula))
        self.wait(0.5)

        # Step 2: Animate each box + arrow + label
        for box, ann, arr in [(prior_box, prior_ann, arrows[2]), 
                              (like_box, like_ann, arrows[1]),
                              (marg_box, marg_ann, arrows[3]), 
                              (post_box, post_ann, arrows[0])]:
            self.play(Create(box))
            self.play(FadeIn(ann), GrowArrow(arr))
            self.play(box.animate.set_stroke(width=6), run_time=0.3)  # pulse
            self.play(box.animate.set_stroke(width=2), run_time=0.3)
            self.wait(2)

        # Step 3: "Where" explanation below
        where_text = VGroup(
            Tex(r"$\theta$ is a parameter of interest").scale(0.6),
            Tex(r"$X$ is the observed data").scale(0.6)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(formula, DOWN, buff=2)

        self.play(FadeIn(where_text, shift=DOWN))

        #self.play(
        #          self.wipe(self.mobjects_without_canvas, [],return_animation=True)
        #          )   
        
    def construct_simstudy(self):
        # Simulation Study
        
        self.next_slide(notes="Simulation Study")
        self.new_clean_slide("Trial Design")


        # --- Block Content ---
        intro_text = Text(
            "Consider a trial comparing treatment vs control\n"
            "with 100 patients per arm and k = 1,..,5 stages",
            font_size=24
        )

        # Math items
        item1 = MathTex(r"\textbf{New Treatment: } X_{1,i} \sim \mathcal{N}(\mu_1, \sigma^2)", font_size=28)
        item2 = MathTex(r"\textbf{Control: } X_{2,i} \sim \mathcal{N}(\mu_2, \sigma^2)", font_size=28)
        item3 = MathTex(r"\textbf{Treatment Effect: } \theta = \mu_1 - \mu_2", font_size=28)
        item4 = MathTex(
            r"\textbf{Hypothesis Test: } H_0 : \theta \leq 0 \quad \text{vs} \quad H_1 : \theta > 0",
            font_size=28
        )

        footer = MathTex(
            r"\text{Type I error } \alpha = 0.025 \quad \text{and power } 1-\beta = 0.9 \quad \text{at } \theta = \delta",
            font_size=26
        )

        # Group all items like in a block
        block_content = VGroup(intro_text, item1, item2, item3, item4, footer).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        # Surrounding box
        block = VGroup(block_content)

        # Position under title
        block.next_to(self.slide_title, DOWN, buff=0.5).align_to(self.slide_title, LEFT)

        # --- Animation ---
        for elem in [intro_text, item1, item2, item3, item4, footer]:
            self.play(Write(elem))
            self.wait(0.3)

        #trialtext = Text("O")
        #trialtext.next_to(self.slide_title, DOWN)
        #trialtext.align_to(self.slide_title, LEFT)

        norm_data = MathTex(
            r"\text{Data } = \begin{cases}"
            r"X_{i,1}\sim N(\mu_1,\sigma^2) \\"
            r"X_{i,2}\sim N(\mu_2,\sigma^2)"
            r"\end{cases}",
            font_size=28,
            color=BLACK
        ).move_to(UL + DOWN*1 + RIGHT*0.8)
        self.next_slide()

        fade_out_group = VGroup(intro_text, item3, item4, footer)    
        mu = 1
        sigma = 1
        self.play(
            FadeOut(fade_out_group),
            ReplacementTransform(VGroup(item1, item2), norm_data,path_arc=0),
            run_time=2
        )

        self.play(
            norm_data.animate.to_corner(UL).shift(DOWN*1 + RIGHT*0.8),
            run_time=1.5
        )
        
        latex_eq = MathTex(
        r"L(\theta) = \begin{cases}"
        r"I_1 + a^{\theta/\delta}I_2 & \text{if } \theta \geq 0 \\"
        r"I_2 + a^{-\theta/\delta}I_1 & \text{if } \theta \leq 0"
        r"\end{cases}",
        font_size=28,
        color=BLACK
        )
        self.next_slide()
# Group equations
        #text_group = VGroup(norm_data).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        #text_group.to_corner(UL)
        #text_group.shift(DOWN*1 + RIGHT*0.8)
        #self.play(Write(text_group))
        #self.wait()
        #self.next_slide()

# Add in priors
        prior_group = MathTex(
        r"\text{Priors } = \begin{cases}"
        r"\theta \sim N(\mu_1 - \mu_2,\sigma_1^2 + \sigma_2^2) \\"
        r"\mu_j \sim N(\mu_j,\sigma_j^2)"
        r"\end{cases}",
        font_size=28,
        color=BLACK
        )

        prior_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        prior_group.next_to(norm_data, DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(prior_group))
        self.wait()
        self.next_slide()
        latex_eq.next_to(prior_group,DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(latex_eq))
        self.next_slide()
        ratio_text = MathTex(
            r"\text{Ratio }=",          # 0
            r"\frac{I_1}{I_2}",         # 1
            r"=",                        # 2
            r"a^{",                      # 3
            r"\theta",                   # 4 
            r"/2\delta}",                # 5
            font_size=28,
            color=BLACK
        )
        ratio_text.next_to(latex_eq,DOWN, aligned_edge=LEFT, buff=0.5)
        self.play(Write(ratio_text))
        self.next_slide()

        #norm_data.generate_target()
        #norm_data.target.to_corner(UL)
        #norm_data.target.shift(DOWN*1 + RIGHT*0.8)
        #self.play(MoveToTarget(norm_data), run_time=1.2)
        # Create the new axes
        newaxes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=6,
            y_length=5,
            axis_config={"color": BLACK},
        )
        x_label = MathTex(r"\theta").scale(0.6).next_to(newaxes.x_axis, DOWN, buff=0.5)
        y_label = Tex(r"\text{Density}").scale(0.6).next_to(newaxes.y_axis, LEFT, buff=0.1)

# Normal PDF function
        def normal_pdf(x):
           return (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)

        graph = newaxes.plot(normal_pdf, color=RED)

# Transform the axes
        self.play(Create(newaxes), Write(x_label), Write(y_label), run_time=2)
        self.wait()

    # Now draw the red curve gradually
        self.play(Create(graph), run_time=2)
        self.wait()
        #self.play(Write(x_label), Write(y_label),Create(graph))

# Group everything to scale and shift
        graph_group = VGroup(newaxes, x_label, y_label, graph)
        #self.play(Create(graph_group), run_time=2)
        self.wait()
        self.play(
            graph_group.animate.scale(0.8, about_point=graph_group.get_center()).shift(RIGHT * 3),
        run_time=1.5
        )


# Add vertical line animation
        current_x = ValueTracker(mu)

        vertical_line = always_redraw(
         lambda: newaxes.get_vertical_line(
             newaxes.coords_to_point(
                 current_x.get_value(),
                 normal_pdf(current_x.get_value())
             ),
             color=BLACK,
             stroke_width=3,
           )
        )
        self.add(vertical_line)
        self.play(current_x.animate.set_value(mu + 1), run_time=3)
        self.play(current_x.animate.set_value(mu - 1), run_time=3)
        self.wait()

        # Create a static vertical line at mu to flash
        # Create a copy of the current vertical line at mu for indication
        highlight_line = newaxes.get_vertical_line(
            newaxes.coords_to_point(mu, normal_pdf(mu)),
            color=BLACK,
            stroke_width=6
        )

        self.play(Indicate(highlight_line, scale_factor=1.2, color=YELLOW))
        self.next_slide()
        theta_box = SurroundingRectangle(   
            ratio_text[4], color=BLUE, buff=0.15
        ).set_fill(BLUE, opacity=0.1)
        theta_label = Tex("MLE / Posterior mean", font_size=20, color=BLUE).next_to(theta_box, UP, buff=0.2)
        theta_arrow = Arrow(
            theta_label.get_bottom(), theta_box.get_top(), buff=0.1, color=BLUE
        )
        # Animate the rectangle and label
        self.play(
            GrowFromCenter(theta_box),
            Write(theta_label),
            GrowArrow(theta_arrow)
        )
        self.next_slide()

# Add and animate shaded area
        a = ValueTracker(mu - 1)
        b = ValueTracker(mu - 1)
        area = always_redraw(
           lambda: newaxes.get_area(
               graph,
               x_range=[a.get_value(), b.get_value()],
               color=BLUE,
               opacity=0.5,
           )
        )
        self.add(area)
        self.play(a.animate.set_value(mu - 2), b.animate.set_value(mu + 2), run_time=3)
        self.play(a.animate.set_value(mu - 1), b.animate.set_value(mu + 1), run_time=3)
        self.wait()

        self.play(
            self.wipe(self.mobjects_without_canvas, [],return_animation=True)
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
        self.play(self.wipe(self.mobjects_without_canvas, ratios, return_animation=True))   
        #self.play(self.next_slide_number_animation(),
        #          self.wipe(self.mobjects_without_canvas,ratios,return_animation=True)
        #          )
        
        self.next_slide(notes="Results")
        self.new_clean_slide("GSD + RAR, Expected Sample Sizes")
        ess = ImageMobject("Images/ess_group.png").scale(0.5)
        title_bottom_y = self.slide_title.get_bottom()[1]
        ess.set_y(title_bottom_y - buff - ess.height / 2)
        ess.set_x(0)    
        self.play(self.wipe(self.mobjects_without_canvas, ess, return_animation=True))   
        #self.play(self.next_slide_number_animation(),
        #          self.wipe(self.mobjects_without_canvas,ess,return_animation=True)
        #          )


    def construct_conclusion(self):
        # Conclusion
        self.next_slide(notes="Conclusions")
        self.new_clean_slide("Conclusions")

        conclusiontext = paragraph(
            "• Hybrid methods matain type I error and power whilst \n allowing flexibility in other design aspects;",
            "• Use of uncertainty in treatment effects improves sampling \n ratios even when using minimally information \n prior data-conflict;",
            "• Advantage of leveraging posterior uncertainty diminishes when \n there is a lot of prior information.",
            color=BLACK,
            font_size=self.CONTENT_FONT_SIZE,
        ).align_to(self.slide_title, LEFT)

        self.play(self.next_slide_number_animation(),
                  self.wipe(self.mobjects_without_canvas,conclusiontext,return_animation=True),
                  )   
        
    def construct_qr(self):
        self.next_slide(notes="QR")
        self.new_clean_slide("QR")
        qr = ImageMobject("Images/github_qr.png")
        qr.scale(1.5)
        qr.move_to(ORIGIN)
        title = Tex("Scan to view presentation code on GitHub").to_edge(DOWN, buff=0.5)
        self.play(FadeIn(qr),run_time=1.5)
        self.wait(1)
        self.play(Write(title))
        self.wait(3)


    def construct(self):
       self.wait_time_between_slides = 0.10
       self.construct_intro()
       self.construct_trialintro()
       self.construct_gsdesign()
       self.construct_rar()
       self.construct_bayes()
       self.construct_simstudy()
       self.construct_results()
       self.construct_conclusion()
       self.construct_qr()

# # ---------- Scenes split by section ----------
# class Intro(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_intro()

# class TrialIntro(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_trialintro()

# class GSDDesign(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_gsdesign()

# class RAR(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_rar()

# class BayesianMethods(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_bayes()

# class SimulationStudy(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_simstudy()

# class Results(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_results()

# class Conclusion(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_conclusion()

# class QR(Main,Slide, MovingCameraScene):
#     def construct(self):
#         self.wait_time_between_slides = 0.10
#         self.construct_qr()
