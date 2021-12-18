from common import *

config.background_color = BLACK


class Rebase(Scene):
    def construct(self):
        # intro(self, "The case of the rebase")

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

        group_feature = Group()
        group_feature.add(feature_ref)
        group_feature.add(feature_ref_to_commit_arrow)

        head_ref = create_head_ref()
        head_ref.next_to(master_ref, UP)
        head_to_master_arrow = create_arrow_between_refs(
            head_ref, master_ref, DOWN)

        group_head = Group()
        group_head.add(head_ref)
        group_head.add(head_to_master_arrow)

        g = Group(master_history, group_master, branch_out,
                  feature_history, group_feature, group_head)
        self.play(FadeIn(g))

        self.wait()

        # tbd visualize the rebase of feature against master
