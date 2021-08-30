from manim import *

COMMIT_FILL_COLOR = BLUE
COMMIT_STROKE_COLOR = ORANGE
COMMIT_LABEL_COLOR = BLACK
ARROW_COLOR = GRAY
BRANCH_REF_COLOR = GREEN
HEAD_REF_COLOR = RED


def intro(self, subtitle):
    my_site = Text("vladflore.tech", font="Noto Sans").scale(0.75)
    self.play(Write(my_site))
    self.play(my_site.animate.shift(1.5 * UP))
    t = Text("Git Animated", font="Noto Sans",
             gradient=(RED, BLUE, GREEN)).scale(1.5)
    st = Text(subtitle, font="Noto Sans",
              color=BLUE).scale(0.3)
    g = Group(t, st).arrange(DOWN, buff=.8).next_to(my_site, DOWN, buff=0.8)
    self.play(FadeIn(g), run_time=2)
    self.play(FadeOut(g), run_time=2)
    self.play(my_site.animate.shift(1.5 * DOWN))
    self.play(Unwrite(my_site))


def create_commit(commit_id):
    circle = Circle(0.3).set_fill(
        color=COMMIT_FILL_COLOR, opacity=0.5).set_stroke(color=COMMIT_STROKE_COLOR, width=1)
    text = MarkupText(commit_id, color=COMMIT_LABEL_COLOR).scale(0.2)
    circle.add(text)
    return circle


def create_arrow_between_commits(start, end, angle_start=PI, angle_end=0):
    return create_arrow(start.point_at_angle(angle_start), end.point_at_angle(angle_end), ARROW_COLOR)


def create_arrow(start, end, color):
    return Line(start=start, end=end, color=color).set_stroke(width=1.0).add_tip(tip_length=0.06)


def create_arrow_between_ref_and_commit(rectangle, circle, side):
    if np.array_equal(UP, side):
        start_arrow = rectangle.get_bottom()
        end_arrow = circle.point_at_angle(PI / 2)
    elif np.array_equal(DOWN, side):
        start_arrow = rectangle.get_top()
        end_arrow = circle.point_at_angle(3 * PI / 2)
    arrow = Arrow(start=start_arrow, end=end_arrow).set_color(
        ARROW_COLOR)
    return arrow


def create_branch_ref(name):
    rectangle = Rectangle(color=BRANCH_REF_COLOR,
                          width=0.6, height=0.25)
    text = MarkupText(name, color=BRANCH_REF_COLOR).scale(0.2)
    rectangle.add(text)
    return rectangle


def create_head_ref():
    rectangle = Rectangle(color=HEAD_REF_COLOR,
                          width=0.5, height=0.25)
    text = MarkupText('HEAD', color=HEAD_REF_COLOR).scale(0.2)
    rectangle.add(text)
    return rectangle


def create_arrow_between_refs(start, end, side):
    if np.array_equal(UP, side):
        start_arrow = start.get_bottom()
        end_arrow = end.get_top()
    elif np.array_equal(DOWN, side):
        start_arrow = start.get_top()
        end_arrow = end.get_bottom()
    arrow = Arrow(start=start_arrow, end=end_arrow).set_color(
        ARROW_COLOR)
    return arrow


def _create_command(text, text_color, after, corner=LEFT + UP, edge=LEFT):
    if after is None:
        return Text(text).scale(0.3).set_color(text_color).to_corner(corner).to_edge(edge)
    else:
        return Text(text).scale(0.3).set_color(text_color).next_to(after, DOWN).to_edge(edge)


def create_command(command_text, after, text_color=ORANGE):
    return _create_command(command_text, text_color, after)
