from manim import *

COMMIT_FILL_COLOR = BLUE
COMMIT_STROKE_COLOR = ORANGE
COMMIT_LABEL_COLOR = BLACK
ARROW_COLOR = GRAY


def intro(self, subtitle):
    my_site = Text("vladflore.tech", font="Noto Sans").scale(0.75)
    self.play(Write(my_site))
    self.play(my_site.animate.shift(1.5 * UP))
    t = Text("Git Animated", font="Noto Sans",
             gradient=(RED, BLUE, GREEN)).scale(1.5)
    st = Text(subtitle, font="Noto Sans",
              color=BLUE).scale(0.5)
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


def create_arrow_between_commits(start, end, linear=True):
    if linear:
        return create_arrow(start.point_at_angle(
            PI), end.point_at_angle(0), ARROW_COLOR)
    else:
        return create_arrow(start.point_at_angle(
            PI / 2), end.point_at_angle(0), ARROW_COLOR)


def create_arrow(start, end, color):
    return Line(start=start, end=end, color=color).set_stroke(width=1.0).add_tip(tip_length=0.06)
