import numpy as np
from manim import *
from manim.mobject.geometry import ArrowTriangleTip

config.background_color = WHITE


class LinearCommits(Scene):
    commits = []
    NO_COMMITS = 2
    ARROW_COLOR = GRAY
    COMMIT_FILL_COLOR = BLUE
    COMMIT_STROKE_COLOR = ORANGE
    COMMIT_LABEL_COLOR = BLACK
    HEAD_REF_COLOR = RED
    BRANCH_REF_COLOR = GREEN

    def construct(self):
        arrows = []
        master_ref = self.create_branch_ref('master')
        self.play(FadeIn(master_ref))

        head_ref = self.create_head_ref()
        head_ref.next_to(master_ref, UP)
        self.play(FadeIn(head_ref))
        head_to_master_arrow = self.create_arrow_between_refs(
            head_ref, master_ref, DOWN)
        self.play(FadeIn(head_to_master_arrow))

        # create the commits
        for i in range(self.NO_COMMITS):
            self.commits.append(self.create_commit(i))

        # arrange the commits and create the arrows between them
        for i in range(1, len(self.commits)):
            self.commits[i].next_to(self.commits[i-1], RIGHT)
            arrows.append(self.create_arrow_between_commits(
                self.commits[i], self.commits[i-1]))

        g = Group(master_ref, head_ref, head_to_master_arrow)
        self.play(FadeOut(g))

        # show the commits
        a = None
        for i in range(len(self.commits)):
            # show new commit
            self.play(FadeIn(self.commits[i]))
            # connect the current commit with the previous one
            if i > 0:
                self.play(FadeIn(arrows[i-1]))
            # remove the arrow between master and commit
            self.remove(a)
            # move the master ref
            self.play(master_ref.animate.next_to(self.commits[i], UP))
            # create new arrow between master and commit
            a = self.create_arrow_between_ref_and_commit(
                master_ref, self.commits[i], UP)
            self.play(FadeIn(a))

            # remove the arrow between head and master
            self.remove(head_to_master_arrow)
            # move the head ref
            self.play(head_ref.animate.next_to(master_ref, UP))
            # create new arrow between head and master
            head_to_master_arrow = self.create_arrow_between_refs(
                head_ref, master_ref, DOWN)
            self.play(FadeIn(head_to_master_arrow))

        self.wait(1)

        # create a new branch based on the last commit
        b = self.create_branch_ref("feature")
        b.next_to(master_ref, RIGHT)
        self.play(FadeIn(b))
        a = self.create_arrow_between_ref_and_commit(
            b, self.commits[-1], UP)
        self.play(FadeIn(a))

        self.wait(1)

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=self.COMMIT_FILL_COLOR, opacity=0.5).set_stroke(color=self.COMMIT_STROKE_COLOR, width=1)
        text = MarkupText(f'C{id}', color=self.COMMIT_LABEL_COLOR).scale(0.2)
        circle.add(text)
        return circle

    def create_arrow_between_commits(self, start, end):
        return Arrow(start=start.point_at_angle(
            PI), end=end.point_at_angle(0)).set_color(self.ARROW_COLOR)

    def create_arrow_between_ref_and_commit(self, rectangle, circle, side):
        if np.array_equal(UP, side):
            start_arrow = rectangle.get_bottom()
            end_arrow = circle.point_at_angle(PI/2)
        elif np.array_equal(DOWN, side):
            start_arrow = rectangle.get_top()
            end_arrow = circle.point_at_angle(3*PI/2)
        arrow = Arrow(start=start_arrow, end=end_arrow).set_color(
            self.ARROW_COLOR)
        return arrow

    def create_arrow_between_refs(self, start, end, side):
        if np.array_equal(UP, side):
            start_arrow = start.get_bottom()
            end_arrow = end.get_top()
        elif np.array_equal(DOWN, side):
            start_arrow = start.get_top()
            end_arrow = end.get_bottom()
        arrow = Arrow(start=start_arrow, end=end_arrow).set_color(
            self.ARROW_COLOR)
        return arrow

    def create_head_ref(self):
        rectangle = Rectangle(color=self.HEAD_REF_COLOR,
                              width=0.5, height=0.25)
        text = MarkupText('HEAD', color=self.HEAD_REF_COLOR).scale(0.2)
        rectangle.add(text)
        return rectangle

    def create_branch_ref(self, name):
        rectangle = Rectangle(color=self.BRANCH_REF_COLOR,
                              width=0.6, height=0.25)
        text = MarkupText(name, color=self.BRANCH_REF_COLOR).scale(0.2)
        rectangle.add(text)
        return rectangle
