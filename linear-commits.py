from itertools import islice

import numpy as np
from manim import *
from manim.mobject.geometry import ArrowTriangleTip

config.background_color = WHITE


class LinearCommits(Scene):
    commits_on_master = []
    commits_on_feature = []
    NO_COMMITS_ON_MASTER = 2
    NO_COMMITS_ON_FEATURE = 2
    ARROW_COLOR = GRAY
    COMMIT_FILL_COLOR = BLUE
    COMMIT_STROKE_COLOR = ORANGE
    COMMIT_LABEL_COLOR = BLACK
    HEAD_REF_COLOR = RED
    BRANCH_REF_COLOR = GREEN

    def construct(self):
        arrows_between_master_commits = []
        master_ref = self.create_branch_ref('master')
        self.play(FadeIn(master_ref))

        head_ref = self.create_head_ref()
        head_ref.next_to(master_ref, UP)
        self.play(FadeIn(head_ref))
        head_to_master_arrow = self.create_arrow_between_refs(
            head_ref, master_ref, DOWN)
        self.play(FadeIn(head_to_master_arrow))

        # create the commits
        for i in range(self.NO_COMMITS_ON_MASTER):
            self.commits_on_master.append(self.create_commit(f'M{i}'))

        # arrange the commits and create the arrows between them
        for i in range(1, len(self.commits_on_master)):
            self.commits_on_master[i].next_to(
                self.commits_on_master[i-1], RIGHT)
            arrows_between_master_commits.append(self.create_arrow_between_commits(
                self.commits_on_master[i], self.commits_on_master[i-1]))

        g = Group(master_ref, head_ref, head_to_master_arrow)
        self.play(FadeOut(g))

        # show the commits
        master_to_commit_arrow = None
        for i in range(len(self.commits_on_master)):
            # show new commit
            self.play(FadeIn(self.commits_on_master[i]))
            # connect the current commit with the previous one
            if i > 0:
                self.play(FadeIn(arrows_between_master_commits[i-1]))
            # remove the arrow between master and commit
            self.remove(master_to_commit_arrow)

            # move the master ref
            if i == 0:
                master_ref.next_to(self.commits_on_master[i], UP)
                self.add(master_ref)
            else:
                self.play(master_ref.animate.next_to(
                    self.commits_on_master[i], UP))

            # create new arrow between master and commit
            master_to_commit_arrow = self.create_arrow_between_ref_and_commit(
                master_ref, self.commits_on_master[i], UP)
            self.play(FadeIn(master_to_commit_arrow))

            # remove the arrow between head and master
            self.remove(head_to_master_arrow)

            # move the head ref
            if i == 0:
                head_ref.next_to(master_ref, UP)
                self.add(head_ref)
            else:
                self.play(head_ref.animate.next_to(master_ref, UP))

            # create new arrow between head and master
            head_to_master_arrow = self.create_arrow_between_refs(
                head_ref, master_ref, DOWN)
            self.play(FadeIn(head_to_master_arrow))

        # create a new branch based on the last commit
        feature_ref = self.create_branch_ref("feature")
        feature_ref.next_to(self.commits_on_master[-1], DOWN)
        self.play(FadeIn(feature_ref))

        feature_to_commit_arrow = self.create_arrow_between_ref_and_commit(
            feature_ref, self.commits_on_master[-1], DOWN)
        self.play(FadeIn(feature_to_commit_arrow))

        # create new commits on the feature branch
        for i in range(self.NO_COMMITS_ON_FEATURE):
            self.commits_on_feature.append(self.create_commit(f'F{i}'))
            next_to = self.commits_on_master[-1] if i == 0 else self.commits_on_feature[i-1]
            self.commits_on_feature[i].next_to(
                next_to, DOWN if i == 0 else RIGHT)
            if i == 0:
                self.commits_on_feature[i].shift(RIGHT*0.5)

            if i == 0:
                self.remove(feature_ref)
                self.remove(feature_to_commit_arrow)

            self.play(FadeIn(self.commits_on_feature[i]))

            previous_commit = self.commits_on_master[-1] if i == 0 else self.commits_on_feature[i-1]
            is_linear = False if i == 0 else True
            arrow_between_commits = self.create_arrow_between_commits(
                self.commits_on_feature[i], previous_commit, linear=is_linear)
            self.play(FadeIn(arrow_between_commits))

            self.remove(feature_to_commit_arrow)
            self.play(feature_ref.animate.next_to(
                self.commits_on_feature[i], DOWN))
            feature_to_commit_arrow = self.create_arrow_between_ref_and_commit(
                feature_ref, self.commits_on_feature[i], DOWN)
            self.play(FadeIn(feature_to_commit_arrow))

        self.wait(2)

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=self.COMMIT_FILL_COLOR, opacity=0.5).set_stroke(color=self.COMMIT_STROKE_COLOR, width=1)
        text = MarkupText(id, color=self.COMMIT_LABEL_COLOR).scale(0.2)
        circle.add(text)
        return circle

    def create_arrow_between_commits(self, start, end, linear=True):
        if linear:
            return Arrow(start=start.point_at_angle(
                PI), end=end.point_at_angle(0)).set_color(self.ARROW_COLOR)
        else:
            return Arrow(start=start.point_at_angle(
                PI/2), end=end.point_at_angle(3*PI/2), buff=1).set_color(self.ARROW_COLOR)

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
