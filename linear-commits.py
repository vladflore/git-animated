from manim import *
from numpy.core.numeric import moveaxis

config.background_color = WHITE


class LinearCommits(Scene):
    def construct(self):
        commits = []
        arrows = []
        for i in range(2):
            commits.append(self.create_commit(i))

        for i in range(1, len(commits)):
            commits[i].next_to(commits[i-1], RIGHT)
            arrows.append(Arrow(start=commits[i].point_at_angle(
                PI), end=commits[i-1].point_at_angle(0)).set_color(ORANGE))

        for i in range(len(commits)):
            self.add(commits[i])
            self.play(FadeIn(commits[i]))
            if i > 0:
                self.add(arrows[i-1])
                self.play(FadeIn(arrows[i-1]))

        new_branch_commit = self.create_commit(4)
        new_branch_commit.next_to(commits[-1], UP*0.5).shift(RIGHT*0.5)
        arrow = Arrow(start=new_branch_commit.point_at_angle(
            5*PI/4), end=commits[-1].point_at_angle(PI/2)).set_color(ORANGE)
        self.add(new_branch_commit)
        self.play(FadeIn(new_branch_commit))
        self.add(arrow)
        self.play(FadeIn(arrow))

        self.move_head(new_branch_commit, UP)

        self.wait(1)

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=BLUE, opacity=0.5).set_stroke(color=ORANGE, width=1)
        text = MarkupText(f'C{id}', color=BLACK).scale(0.2)
        circle.add(text)
        return circle

    def move_head(self, commit, side):
        text = MarkupText('HEAD', color=RED).scale(0.2)
        text.next_to(commit, side)
        arrow = Arrow(start=text, end=commit).set_color(ORANGE)
        self.add(text)
        self.play(FadeIn(text))
        self.add(arrow)
        self.play(FadeIn(arrow))
