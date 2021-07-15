import manimpango
from manim import *


class LinearCommits(Scene):
    def construct(self):
        commits = []
        for i in range(7):
            commits.append(self.create_commit(i))

        for i in range(1, len(commits)):
            commits[i].next_to(commits[i-1], RIGHT)

        for i in range(len(commits)):
            self.add(commits[i])
            self.play(FadeIn(commits[i]))

        self.wait(1)

    def create_commit(self, id):
        circle = Circle(0.3).set_fill(
            color=BLUE, opacity=1).set_stroke(color=RED, width=1)
        text = MarkupText(f'C{id}', color=RED).scale(0.2)
        commit = Group(circle, text)
        return commit
