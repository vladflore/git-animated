import numpy as np
from manim import *

config.background_color = WHITE


class LinearCommits(Scene):
    commits = []

    def construct(self):
        arrows = []
        for i in range(2):
            self.commits.append(self.create_commit(i))

        for i in range(1, len(self.commits)):
            self.commits[i].next_to(self.commits[i-1], RIGHT)
            arrows.append(Arrow(start=self.commits[i].point_at_angle(
                PI), end=self.commits[i-1].point_at_angle(0)).set_color(ORANGE))

        for i in range(len(self.commits)):
            self.add(self.commits[i])
            self.play(FadeIn(self.commits[i]))
            if i > 0:
                self.add(arrows[i-1])
                self.play(FadeIn(arrows[i-1]))

        new_branch_commit = self.create_commit(4)
        new_branch_commit.next_to(self.commits[-1], UP*0.5).shift(RIGHT*0.5)
        arrow = Arrow(start=new_branch_commit.point_at_angle(
            5*PI/4), end=self.commits[-1].point_at_angle(PI/2)).set_color(ORANGE)
        self.add(new_branch_commit)
        self.play(FadeIn(new_branch_commit))
        self.add(arrow)
        self.play(FadeIn(arrow))

        head = self.create_head()
        head.next_to(new_branch_commit, UP)
        self.add(head)
        arrow = self.create_arrow(head, new_branch_commit, UP)
        self.add(arrow)

        self.wait(1)

        self.remove(arrow)
        self.play(head.animate.next_to(self.commits[-1], DOWN))
        arrow = self.create_arrow(head, self.commits[-1], DOWN)
        self.add(arrow)
        self.wait(1)
        self.remove(arrow)
        self.play(head.animate.next_to(new_branch_commit, UP))
        arrow = self.create_arrow(head, new_branch_commit, UP)
        self.add(arrow)
        self.wait(1)

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=BLUE, opacity=0.5).set_stroke(color=ORANGE, width=1)
        text = MarkupText(f'C{id}', color=BLACK).scale(0.2)
        circle.add(text)
        return circle

    def create_arrow(self, head, commit, side):
        if np.array_equal(UP, side):
            start_arrow = head.get_bottom()
            end_arrow = commit.point_at_angle(PI/2)
        elif np.array_equal(DOWN, side):
            start_arrow = head.get_top()
            end_arrow = commit.point_at_angle(3*PI/2)
        arrow = Arrow(start=start_arrow, end=end_arrow).set_color(ORANGE)
        return arrow

    def create_head(self):
        rectangle = Rectangle(color=RED, width=0.5, height=0.25)
        text = MarkupText('HEAD', color=RED).scale(0.2)
        rectangle.add(text)
        return rectangle
