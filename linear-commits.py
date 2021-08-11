from manim import *

config.background_color = BLACK


class LinearCommits(Scene):
    NO_COMMITS_ON_MASTER = 3
    NO_COMMITS_ON_FEATURE = 3
    ARROW_COLOR = GRAY
    COMMIT_FILL_COLOR = BLUE
    COMMIT_STROKE_COLOR = ORANGE
    COMMIT_LABEL_COLOR = BLACK
    HEAD_REF_COLOR = RED
    BRANCH_REF_COLOR = GREEN

    def construct(self):
        commits_on_feature = []
        arrows_between_master_commits = []

        self.intro()

        master_ref = self.create_branch_ref('master')
        init = self.show_command("git init", None)
        self.play(FadeIn(master_ref))

        head_ref = self.create_head_ref()
        head_ref.next_to(master_ref, UP)
        self.play(FadeIn(head_ref))

        head_to_master_arrow = self.create_arrow_between_refs(
            head_ref, master_ref, DOWN)
        self.play(FadeIn(head_to_master_arrow))

        # create the commits
        commits_on_master = [self.create_commit(f'M{idx}') for idx in range(self.NO_COMMITS_ON_MASTER)]

        # arrange the commits and create the arrows between them
        for idx in range(1, len(commits_on_master)):
            commits_on_master[idx].next_to(
                commits_on_master[idx - 1], RIGHT)
            arrows_between_master_commits.append(self.create_arrow_between_commits(
                commits_on_master[idx], commits_on_master[idx - 1]))

        g = Group(master_ref, head_ref, head_to_master_arrow)
        self.play(FadeOut(g))

        # show the commits
        cmd = None
        master_to_commit_arrow = None
        for idx in range(len(commits_on_master)):
            cmd = self.show_command(f'git commit -m \'M{idx}\'', after=init if cmd is None else cmd)

            # show new commit
            self.play(FadeIn(commits_on_master[idx]))
            # connect the current commit with the previous one
            if idx > 0:
                self.play(FadeIn(arrows_between_master_commits[idx - 1]))
            # remove the arrow between master and commit
            self.remove(master_to_commit_arrow)

            # move the master ref
            if idx == 0:
                master_ref.next_to(commits_on_master[idx], UP)
                self.add(master_ref)
            else:
                self.play(master_ref.animate.next_to(
                    commits_on_master[idx], UP))

            # create new arrow between master and commit
            master_to_commit_arrow = self.create_arrow_between_ref_and_commit(
                master_ref, commits_on_master[idx], UP)
            self.play(FadeIn(master_to_commit_arrow))

            # remove the arrow between head and master
            self.remove(head_to_master_arrow)

            # move the head ref
            if idx == 0:
                head_ref.next_to(master_ref, UP)
                self.add(head_ref)
            else:
                self.play(head_ref.animate.next_to(master_ref, UP))

            # create new arrow between head and master
            head_to_master_arrow = self.create_arrow_between_refs(
                head_ref, master_ref, DOWN)
            self.play(FadeIn(head_to_master_arrow))

        #
        # NEW FEATURE BRANCH
        #

        # create a new branch based on the last commit
        feature_ref = self.create_branch_ref("feature")
        feature_ref.next_to(commits_on_master[-1], DOWN)

        cmd = self.show_command("git branch feature", after=cmd)

        self.play(FadeIn(feature_ref))

        feature_to_commit_arrow = self.create_arrow_between_ref_and_commit(
            feature_ref, commits_on_master[-1], DOWN)
        self.play(FadeIn(feature_to_commit_arrow))

        # remove the arrow between head and master
        self.remove(head_to_master_arrow)

        cmd = self.show_command("git checkout feature", after=cmd)

        # move the head ref to point to the new feature ref
        self.play(head_ref.animate.next_to(feature_ref, DOWN))

        head_to_feature_arrow = self.create_arrow_between_refs(
            head_ref, feature_ref, UP)
        self.play(FadeIn(head_to_feature_arrow))

        g = Group(feature_ref, feature_to_commit_arrow,
                  head_ref, head_to_feature_arrow)

        # create new commits on the feature branch
        for idx in range(self.NO_COMMITS_ON_FEATURE):
            # create commit
            commits_on_feature.append(self.create_commit(f'F{idx}'))

            # position the commit
            next_to = commits_on_master[-1] if idx == 0 else commits_on_feature[idx - 1]
            commits_on_feature[idx].next_to(
                next_to, DOWN if idx == 0 else RIGHT)
            if idx == 0:
                commits_on_feature[idx].shift(RIGHT * 0.5)

            # remove the feature ref and arrow between it and the commit
            if idx == 0:
                self.play(FadeOut(g))

            cmd = self.show_command(f'git commit -m \'F{idx}\'', after=cmd)

            # show the commit
            self.play(FadeIn(commits_on_feature[idx]))

            # show the arrow between the commits
            previous_commit = commits_on_master[-1] if idx == 0 else commits_on_feature[idx - 1]
            is_linear = False if idx == 0 else True
            arrow_between_commits = self.create_arrow_between_commits(
                commits_on_feature[idx], previous_commit, linear=is_linear)
            self.play(FadeIn(arrow_between_commits))

            # remove the arrow between the feature ref and commit
            self.remove(feature_to_commit_arrow)

            # move the feature ref
            self.play(feature_ref.animate.next_to(
                commits_on_feature[idx], DOWN))
            # show the arrow between the feature ref and commit
            feature_to_commit_arrow = self.create_arrow_between_ref_and_commit(
                feature_ref, commits_on_feature[idx], DOWN)
            self.play(FadeIn(feature_to_commit_arrow))

            self.remove(head_to_feature_arrow)
            self.play(head_ref.animate.next_to(feature_ref, DOWN))
            head_to_feature_arrow = self.create_arrow_between_refs(
                head_ref, feature_ref, UP)
            self.play(FadeIn(head_to_feature_arrow))

        self.wait(2)

    def intro(self):
        my_site = Text("vladflore.tech", font="Noto Sans").scale(0.75)
        self.play(Write(my_site))
        self.play(my_site.animate.shift(1.5 * UP))
        t = Text("Git Animated", font="Noto Sans",
                 gradient=(RED, BLUE, GREEN)).scale(1.5)
        st = Text("From your first commit to your first branch", font="Noto Sans",
                  color=BLUE).scale(0.5)
        g = Group(t, st).arrange(DOWN, buff=.8).next_to(my_site, DOWN, buff=0.8)
        self.play(FadeIn(g), run_time=2)
        self.play(FadeOut(g), run_time=2)
        self.play(my_site.animate.shift(1.5 * DOWN))
        self.play(Unwrite(my_site))

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=self.COMMIT_FILL_COLOR, opacity=0.5).set_stroke(color=self.COMMIT_STROKE_COLOR, width=1)
        text = MarkupText(id, color=self.COMMIT_LABEL_COLOR).scale(0.2)
        circle.add(text)
        return circle

    def create_arrow_between_commits(self, start, end, linear=True):
        if linear:
            return self.create_arrow(start.point_at_angle(
                PI), end.point_at_angle(0), self.ARROW_COLOR)
        else:
            return self.create_arrow(start.point_at_angle(
                PI / 2), end.point_at_angle(0), self.ARROW_COLOR)

    def create_arrow_between_ref_and_commit(self, rectangle, circle, side):
        if np.array_equal(UP, side):
            start_arrow = rectangle.get_bottom()
            end_arrow = circle.point_at_angle(PI / 2)
        elif np.array_equal(DOWN, side):
            start_arrow = rectangle.get_top()
            end_arrow = circle.point_at_angle(3 * PI / 2)
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

    @staticmethod
    def create_arrow(start, end, color):
        return Line(start=start, end=end, color=color).set_stroke(width=1.0).add_tip(tip_length=0.06)

    @staticmethod
    def create_command(text, after, corner=LEFT + UP, edge=LEFT):
        if after is None:
            return Text(text).scale(0.3).set_color(ORANGE).to_corner(corner).to_edge(edge)
        else:
            return Text(text).scale(0.3).set_color(ORANGE).next_to(after, DOWN).to_edge(edge)

    def show_command(self, command_text, after, speed=0.5):
        command = self.create_command(command_text, after)
        self.play(Write(command), run_time=speed)
        return command

