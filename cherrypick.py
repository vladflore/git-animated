from common import *

config.background_color = BLACK


class CherryPick(Scene):
    def construct(self):
        intro(self, "The case of cherry-pick")

        # create the master history: M0, M1, M2
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
        master_history.shift(LEFT * 2).shift(UP * 1.5)

        # create the feature history: F0, F1, F2 – branching from M1
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
        feature_history.shift(LEFT * 0.5).shift(DOWN * 1)

        # arrow showing that feature branches from M1
        branch_out = create_arrow_between_commits(
            feature_commits[0], master_commits[1],
            angle_start=PI / 2, angle_end=3 * PI / 2)

        # git commands (setup context shown on screen)
        git_commands = []
        git_commands.append(create_command("git commit -m 'M0'", after=None))
        git_commands.append(create_command("git commit -m 'M1'", after=git_commands[-1]))
        git_commands.append(create_command('git branch feature', after=git_commands[-1]))
        git_commands.append(create_command('git checkout feature', after=git_commands[-1]))
        git_commands.append(create_command("git commit -m 'F0'", after=git_commands[-1]))
        git_commands.append(create_command("git commit -m 'F1'", after=git_commands[-1]))
        git_commands.append(create_command("git commit -m 'F2'", after=git_commands[-1]))
        git_commands.append(create_command('git checkout master', after=git_commands[-1]))
        git_commands.append(create_command("git commit -m 'M2'", after=git_commands[-1]))

        git_commands_group = Group(*git_commands)
        self.play(FadeIn(git_commands_group), run_time=0.75)

        # branch references
        master_ref = create_branch_ref('master')
        master_ref.next_to(master_commits[-1], UP)
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            master_ref, master_commits[-1], UP)
        group_master = Group(master_ref, master_ref_to_commit_arrow)

        feature_ref = create_branch_ref('feature')
        feature_ref.next_to(feature_commits[-1], DOWN)
        feature_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            feature_ref, feature_commits[-1], DOWN)
        group_feature = Group(feature_ref, feature_ref_to_commit_arrow)

        head_ref = create_head_ref()
        head_ref.next_to(master_ref, UP)
        head_to_master_arrow = create_arrow_between_refs(head_ref, master_ref, DOWN)
        group_head = Group(head_ref, head_to_master_arrow)

        g = Group(master_history, group_master, branch_out,
                  feature_history, group_feature, group_head)
        self.play(FadeIn(g))

        # show the cherry-pick command
        git_commands.append(create_command(
            'git cherry-pick F1', after=git_commands[-1], text_color=WHITE))
        self.play(FadeIn(git_commands[-1]), run_time=0.75)

        # highlight the commit being picked (F1)
        highlight = SurroundingRectangle(feature_commits[1], buff=SMALL_BUFF, color=YELLOW)
        self.play(Create(highlight))
        annotation = MarkupText(
            'this commit will\nbe cherry-picked',
            color=YELLOW).scale(0.2).next_to(highlight, DOWN)
        self.play(Write(annotation))

        # fade F1 to show it is the source of the copy
        f1_faded = feature_commits[1].copy()
        f1_faded.set_opacity(0.25)
        self.play(Transform(feature_commits[1], f1_faded))

        # create the new cherry-picked commit on master (F1')
        new_commit = create_commit("F1'")
        new_commit.next_to(master_commits[-1], RIGHT)
        new_arrow = create_arrow_between_commits(new_commit, master_commits[-1])

        self.play(FadeIn(new_commit))
        self.play(FadeIn(new_arrow))

        # move master ref and HEAD to the new commit
        self.remove(master_ref_to_commit_arrow)
        refs_group = Group(head_ref, head_to_master_arrow, master_ref)
        self.play(refs_group.animate.next_to(new_commit, UP))
        master_ref_to_commit_arrow = create_arrow_between_ref_and_commit(
            master_ref, new_commit, UP)
        self.add(master_ref_to_commit_arrow)

        # clean up highlight and annotate the new commit
        self.play(FadeOut(annotation), FadeOut(highlight))
        new_commit_box = SurroundingRectangle(new_commit, buff=SMALL_BUFF)
        self.play(Create(new_commit_box))
        self.play(Write(MarkupText(
            'new commit with the same\ncontent as F1, but a\ndifferent hash',
            color=YELLOW).scale(0.2).next_to(new_commit, RIGHT)))

        # note: cherry-pick only works on non-ancestor commits
        note = MarkupText(
            'Note: cherry-pick only works if the commit\n'
            'being picked is not an ancestor of HEAD',
            color=WHITE).scale(0.2).to_corner(DOWN)
        self.play(Write(note))

        self.wait(2)
