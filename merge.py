from common import *

config.background_color = BLACK


class Merge(Scene):
    def construct(self):
        intro(self, "From multiple histories to one commit")
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

        self.play(FadeIn(master_history), run_time=.8)
        self.wait(2)
