from common import *

config.background_color = BLACK


class Rebase(Scene):
    def construct(self):
        intro(self, "The case of the rebase")

        # create the master history
        master_commits = [create_commit(f'M{idx}') for idx in range(4)]
        arrows_between_master_commits = []
        master_history = Group()
        for idx in range(len(master_commits) - 1):
            master_commits[idx + 1].next_to(master_commits[idx], RIGHT)
            arrows_between_master_commits.append(
                create_arrow_between_commits(master_commits[idx + 1], master_commits[idx]))

            master_history.add(master_commits[idx])
            master_history.add(arrows_between_master_commits[idx])
        master_history.add(master_commits[-1])
        master_history.shift(LEFT * 2).shift(UP * 2)

        git_commands = []
        for idx in range(len(master_commits)-1):
            after = None if len(git_commands) == 0 else git_commands[idx - 1]
            git_commands.append(create_command(
                f'git commit -m \'M{idx}\'', after=after))

        # create the feature history
        feature_commits = [create_commit(f'F{idx}') for idx in range(3)]
        arrows_between_feature_commits = []
        feature_history = Group()
        for idx in range(len(feature_commits) - 1):
            feature_commits[idx + 1].next_to(feature_commits[idx], RIGHT)
            arrows_between_feature_commits.append(
                create_arrow_between_commits(feature_commits[idx + 1], feature_commits[idx]))

            feature_history.add(feature_commits[idx])
            feature_history.add(arrows_between_feature_commits[idx])
        feature_history.add(feature_commits[-1])
        feature_history.shift(LEFT * 2).shift(UP).shift(RIGHT * 2.25)

        # branch out of master
        branch_out = create_arrow_between_commits(feature_commits[0], master_commits[-2], angle_start=PI / 2,
                                                  angle_end=0)

        git_commands.append(create_command(
            'git branch feature', after=git_commands[-1]))
        git_commands.append(create_command(
            'git checkout feature', after=git_commands[-1]))

        for idx in range(len(feature_commits)):
            git_commands.append(create_command(
                f'git commit -m \'F{idx}\'', after=git_commands[-1]))

        git_commands.append(create_command(
            'git checkout master', after=git_commands[-1]))

        git_commands.append(create_command(
            f'git commit -m \'M{len(master_commits)-1}\'', after=git_commands[-1]))

        git_commands_group = Group(*git_commands)
        self.play(FadeIn(git_commands_group), run_time=.75)

        master_ref = create_branch_ref('master')
        master_ref.next_to(master_commits[-1], UP)
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            master_ref, master_commits[-1], UP)

        group_master = Group()
        group_master.add(master_ref)
        group_master.add(master_ref_to_commit_arrow)

        feature_ref = create_branch_ref('feature')
        feature_ref.next_to(feature_commits[-1], DOWN)
        feature_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            feature_ref, feature_commits[-1], DOWN)

        g = Group()
        g.add(feature_ref)
        g.add(feature_ref_to_commit_arrow)

        head_ref = create_head_ref()
        head_ref.next_to(master_ref, UP)
        head_to_master_arrow = create_arrow_between_refs(
            head_ref, master_ref, DOWN)

        group_head = Group()
        group_head.add(head_ref)
        group_head.add(head_to_master_arrow)

        g = Group(master_history, group_master, branch_out,
                  feature_history, g, group_head)
        self.play(FadeIn(g))

        # checkout feature
        git_commands.append(create_command(
            'git checkout feature', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=.75)
        self.remove(head_to_master_arrow)
        self.play(head_ref.animate.next_to(feature_ref, DOWN))
        head_to_feature_arrow = create_arrow_between_refs(
            head_ref, feature_ref, UP)
        self.add(head_to_feature_arrow)

        git_commands.append(create_command(
            'git rebase master', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=.75)

        # rebase
        new_commits = [create_commit(f'F\'{idx}')
                       for idx in range(len(feature_commits))]
        for idx in range(len(new_commits)):
            arrow = None
            if idx == 0:
                new_commits[idx].next_to(master_commits[-1])
                arrow = create_arrow_between_commits(
                    new_commits[idx], master_commits[-1])
            else:
                new_commits[idx].next_to(new_commits[idx-1])
                arrow = create_arrow_between_commits(
                    new_commits[idx], new_commits[idx-1])

            # fade out the arrows between the original feature commits
            if idx == 0:
                new_branch_out = branch_out.copy()
                new_branch_out.set_opacity(0.25)
                self.play(Transform(branch_out, new_branch_out))
            else:
                a = arrows_between_feature_commits[idx-1].copy()
                a.set_opacity(0.25)
                self.play(Transform(arrows_between_feature_commits[idx-1], a))

            # fade out the original feature commit
            c = feature_commits[idx].copy()
            c.set_opacity(0.25)
            self.play(Transform(feature_commits[idx], c))

            self.play(FadeIn(new_commits[idx]))
            self.play(FadeIn(arrow))

        self.remove(feature_ref_to_commit_arrow, feature_ref,
                    head_to_feature_arrow, head_ref)

        feature_ref.next_to(new_commits[-1], UP)
        feature_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            feature_ref, new_commits[-1], UP)
        head_ref.next_to(feature_ref, UP)
        head_to_feature_arrow = create_arrow_between_refs(
            head_ref, feature_ref, DOWN)
        g = Group(feature_ref, feature_ref_to_commit_arrow,
                  head_ref, head_to_feature_arrow)
        self.play(FadeIn(g))

        g = Group(*new_commits)
        self.play(Create(SurroundingRectangle(
            g, buff=SMALL_BUFF)))
        self.play(Write(MarkupText('these are new commits\nwith the same content\nas the original faded ones', color=YELLOW).scale(0.2).next_to(
            new_commits[-1], RIGHT)))

        g = Group(*feature_commits)
        self.play(Create(SurroundingRectangle(
            g, buff=SMALL_BUFF)))
        self.play(Write(MarkupText('these commits will be eventually garbage collected', color=YELLOW).scale(0.2).next_to(
            feature_commits[-1], RIGHT)))

        self.wait()
