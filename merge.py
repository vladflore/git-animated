from common import *

config.background_color = BLACK


class Merge(Scene):
    def construct(self):
        intro(self, "The case of fast-forward merging")

        # create the master history
        master_commits = [create_commit(f'M{idx}') for idx in range(3)]
        arrows_between_master_commits = []
        master_history = Group()
        for idx in range(len(master_commits) - 1):
            master_commits[idx + 1].next_to(master_commits[idx], RIGHT)
            arrows_between_master_commits.append(
                create_arrow_between_commits(master_commits[idx + 1], master_commits[idx]))

            master_history.add(master_commits[idx])
            master_history.add(arrows_between_master_commits[idx])
        master_history.add(master_commits[-1])
        master_history.shift(UP * 2)

        git_commands = []
        for idx in range(len(master_commits)):
            after = None if len(git_commands) == 0 else git_commands[idx - 1]
            git_commands.append(create_command(f'git commit -m \'M{idx}\'', after=after))

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
        feature_history.shift(UP).shift(RIGHT * 2.5)

        # branch out of master
        branch_out = create_arrow_between_commits(feature_commits[0], master_commits[-1], False)

        git_commands.append(create_command('git branch feature', after=git_commands[-1]))
        git_commands.append(create_command('git checkout feature', after=git_commands[-1]))

        for idx in range(len(feature_commits)):
            git_commands.append(create_command(f'git commit -m \'F{idx}\'', after=git_commands[len(git_commands) - 1]))

        git_commands_group = Group(*git_commands)
        self.play(FadeIn(git_commands_group), run_time=.75)

        master_ref = create_branch_ref('master')
        master_ref.next_to(master_commits[-1], UP)
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(master_ref, master_commits[-1], UP)

        group_master = Group()
        group_master.add(master_ref)
        group_master.add(master_ref_to_commit_arrow)

        feature_ref = create_branch_ref('feature')
        feature_ref.next_to(feature_commits[-1], DOWN)
        feature_ref_to_commit_arrow = create_arrow_between_ref_and_commit(feature_ref, feature_commits[-1], DOWN)

        group_feature = Group()
        group_feature.add(feature_ref)
        group_feature.add(feature_ref_to_commit_arrow)

        head_ref = create_head_ref()
        head_ref.next_to(feature_ref, DOWN)
        head_to_feature_arrow = create_arrow_between_refs(head_ref, feature_ref, UP)

        group_head = Group()
        group_head.add(head_ref)
        group_head.add(head_to_feature_arrow)

        # create a box around the git history animation
        all_objects = Group(master_history, group_master, branch_out, feature_history, group_feature, group_head)
        box = SurroundingRectangle(all_objects, color=WHITE, buff=0.75)
        self.play(Create(box))
        self.wait(1)

        self.play(FadeIn(master_history))
        self.play(FadeIn(group_master))
        self.play(FadeIn(branch_out))
        self.play(FadeIn(feature_history))
        self.play(FadeIn(group_feature))
        self.play(FadeIn(group_head))

        # checkout master
        git_commands.append(create_command('git checkout master', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=.75)

        self.remove(head_to_feature_arrow)
        self.play(head_ref.animate.next_to(master_ref, UP))
        head_to_master_arrow = create_arrow_between_refs(head_ref, master_ref, DOWN)
        self.add(head_to_master_arrow)

        self.wait(1)

        # merge feature into master
        git_commands.append(create_command('git merge feature', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=.75)
        self.remove(master_ref_to_commit_arrow)
        g = Group(head_ref, head_to_master_arrow, master_ref)
        self.play(g.animate.next_to(feature_commits[-1], UP))
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(master_ref, feature_commits[-1], UP)
        self.add(master_ref_to_commit_arrow)

        # delete feature branch
        git_commands.append(create_command('git branch -d feature', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]),
                  run_time=.75)
        g = Group(feature_ref, feature_ref_to_commit_arrow)
        self.play(FadeOut(g), run_time=1.5)

        self.wait(2)
