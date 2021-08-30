from common import *

config.background_color = BLACK


class Merge3W(Scene):
    def construct(self):
        intro(self, "The case of the recursive merge")

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
        master_history.shift(LEFT * 2).shift(UP * 2)

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
        feature_history.shift(LEFT * 2).shift(UP).shift(RIGHT * 2.25)

        # branch out of master
        branch_out = create_arrow_between_commits(feature_commits[0], master_commits[-1], angle_start=PI / 2,
                                                  angle_end=0)

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

        g = Group(master_history, group_master, branch_out, feature_history, group_feature, group_head)
        self.play(FadeIn(g))
        self.wait()

        # checkout master
        git_commands.append(create_command('git checkout master', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=.75)

        self.remove(head_to_feature_arrow)
        self.play(head_ref.animate.next_to(master_ref, UP))
        head_to_master_arrow = create_arrow_between_refs(head_ref, master_ref, DOWN)
        self.add(head_to_master_arrow)

        self.wait()

        # add one commit on the master branch
        master_commits.append(create_commit(f'M{len(master_commits)}'))
        master_commits[-1].next_to(master_commits[-2], RIGHT)
        arrows_between_master_commits.append(
            create_arrow_between_commits(master_commits[-1], master_commits[-2]))
        git_commands.append(
            create_command(f'git commit -m \'M{len(master_commits) - 1}\'', after=git_commands[-1]))
        self.play(FadeIn(git_commands[-1]))
        self.play(FadeIn(master_commits[-1]))
        self.play(FadeIn(arrows_between_master_commits[-1]))
        self.remove(master_ref_to_commit_arrow)
        self.play(master_ref.animate.next_to(master_commits[-1], UP))
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(master_ref, master_commits[-1], UP)
        self.add(master_ref_to_commit_arrow)
        self.remove(head_to_master_arrow)
        self.play(head_ref.animate.next_to(master_ref, UP))
        head_to_master_arrow = create_arrow_between_refs(head_ref, master_ref, DOWN)
        self.add(head_to_master_arrow)

        # merge feature into master - 3-way merge
        master_commits.append(create_commit('MF'))
        master_commits[-1].next_to(master_commits[-2], RIGHT * 6)
        arrows_between_master_commits.append(
            create_arrow_between_commits(master_commits[-1], master_commits[-2]))
        git_commands.append(create_command('git merge feature', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]))
        self.play(FadeIn(master_commits[-1]))
        self.play(FadeIn(arrows_between_master_commits[-1]))
        merge_commit_to_feature_arrow = create_arrow_between_commits(master_commits[-1], feature_commits[-1],
                                                                     angle_start=PI, angle_end=PI / 2)
        self.play(FadeIn(merge_commit_to_feature_arrow))
        self.wait()

        self.remove(master_ref_to_commit_arrow)
        self.play(master_ref.animate.next_to(master_commits[-1], UP))
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(master_ref, master_commits[-1], UP)
        self.add(master_ref_to_commit_arrow)
        self.remove(head_to_master_arrow)
        self.play(head_ref.animate.next_to(master_ref, UP))
        head_to_master_arrow = create_arrow_between_refs(head_ref, master_ref, DOWN)
        self.add(head_to_master_arrow)

        self.wait()

        # this is the merge commit
        self.play(Create(SurroundingRectangle(master_commits[-1], buff=SMALL_BUFF)))
        self.play(Write(MarkupText('this is the merge commit\nit has two parents', color=YELLOW).scale(0.2).next_to(
            master_commits[-1], RIGHT)))

        # delete feature branch
        git_commands.append(create_command('git branch -d feature', after=git_commands[-1]))
        self.play(FadeIn(git_commands[-1]),
                  run_time=.75)
        g = Group(feature_ref, feature_ref_to_commit_arrow)
        self.play(FadeOut(g), run_time=1.5)

        self.wait()
