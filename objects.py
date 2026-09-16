from common import *

config.background_color = BLACK

BLOB_COLOR = BLUE
TREE_COLOR = ORANGE
COMMIT_OBJ_COLOR = YELLOW
FILE_COLOR = WHITE


def create_object_box(lines, color):
    text = VGroup(*[MarkupText(line, color=color).scale(0.22) for line in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.08)
    box = SurroundingRectangle(text, color=color, buff=0.15)
    return VGroup(box, text)


def create_arrow(start, end, color):
    return Line(start=start, end=end, color=color).set_stroke(width=1.5).add_tip(
        tip_length=0.12, tip_width=0.07)


def create_legend():
    entries = [
        (FILE_COLOR, "working dir file"),
        (BLOB_COLOR, "blob"),
        (TREE_COLOR, "tree"),
        (COMMIT_OBJ_COLOR, "commit"),
        (BRANCH_REF_COLOR, "branch ref"),
        (HEAD_REF_COLOR, "HEAD"),
    ]
    rows = VGroup()
    for color, label in entries:
        swatch = Square(side_length=0.14).set_fill(
            color, opacity=1).set_stroke(color=color, width=1)
        text = Text(label, font="Noto Sans", color=WHITE).scale(0.16)
        rows.add(VGroup(swatch, text).arrange(RIGHT, buff=0.1))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    box = SurroundingRectangle(rows, color=GRAY, buff=0.12)
    return VGroup(box, rows)


class Objects(Scene):
    def construct(self):
        intro(self, "The case of the object database")

        legend = create_legend()
        legend.to_corner(UR, buff=0.3)
        self.play(FadeIn(legend))

        # working directory
        file_box = create_object_box(["hello.txt", '"Hello, Git!"'], FILE_COLOR)
        file_box.to_edge(LEFT).shift(DOWN * 1.2)
        self.play(FadeIn(file_box))

        cmd = create_command("echo 'Hello, Git!' > hello.txt", after=None)
        self.play(Write(cmd), run_time=.5)

        # hash-object -> blob
        cmd = create_command("git hash-object -w hello.txt", after=cmd)
        self.play(Write(cmd), run_time=.5)

        blob1 = create_object_box(["blob 670a245", '"Hello, Git!"'], BLOB_COLOR)
        blob1.next_to(file_box, RIGHT, buff=1.2).shift(UP * 0)
        arrow1 = create_arrow(file_box.get_right(), blob1.get_left(), ARROW_COLOR)
        self.play(FadeIn(arrow1), FadeIn(blob1))
        self.wait()

        # add + commit -> tree + commit
        cmd = create_command("git add hello.txt", after=cmd)
        self.play(Write(cmd), run_time=.5)
        cmd = create_command("git commit -m 'Add hello.txt'", after=cmd)
        self.play(Write(cmd), run_time=.5)

        tree1 = create_object_box(
            ["tree d3ec8a0", "100644 blob 670a245  hello.txt"], TREE_COLOR)
        tree1.next_to(blob1, RIGHT, buff=1.2)
        arrow2 = create_arrow(blob1.get_right(), tree1.get_left(), ARROW_COLOR)
        self.play(FadeIn(arrow2), FadeIn(tree1))

        commit1 = create_object_box(
            ["commit aba6a21", "tree d3ec8a0", "parent (none)"], COMMIT_OBJ_COLOR)
        commit1.next_to(tree1, UP, buff=0.6)
        arrow3 = create_arrow(commit1.get_bottom(), tree1.get_top(), ARROW_COLOR)
        self.play(FadeIn(arrow3), FadeIn(commit1))

        main_ref = create_branch_ref("main")
        main_ref.next_to(commit1, UP, buff=0.4)
        head_ref = create_head_ref()
        head_ref.next_to(main_ref, UP, buff=0.4)
        ref_arrow = create_arrow(main_ref.get_bottom(), commit1.get_top(), ARROW_COLOR)
        head_arrow = create_arrow_between_refs(head_ref, main_ref, DOWN)
        self.play(FadeIn(main_ref), FadeIn(ref_arrow), FadeIn(head_ref), FadeIn(head_arrow))
        self.wait(2)

        # second commit: file changes, new blob, new tree, new commit
        cmd = create_command("echo 'Hello, Git! v2' > hello.txt", after=cmd)
        self.play(Write(cmd), run_time=.5)
        self.play(Transform(file_box[1][1], MarkupText(
            '"Hello, Git! v2"', color=FILE_COLOR).scale(0.22).move_to(file_box[1][1])))

        cmd = create_command("git add hello.txt", after=cmd)
        self.play(Write(cmd), run_time=.5)
        cmd = create_command("git commit -m 'Update hello.txt'", after=cmd)
        self.play(Write(cmd), run_time=.5)

        blob2 = create_object_box(["blob 14f5f0b", '"Hello, Git! v2"'], BLOB_COLOR)
        blob2.next_to(commit1, RIGHT, buff=2.5).align_to(blob1, UP)
        self.play(FadeIn(blob2))

        tree2 = create_object_box(
            ["tree a6b9f46", "100644 blob 14f5f0b  hello.txt"], TREE_COLOR)
        tree2.next_to(blob2, RIGHT, buff=1.2)
        arrow4 = create_arrow(blob2.get_right(), tree2.get_left(), ARROW_COLOR)
        self.play(FadeIn(arrow4), FadeIn(tree2))

        commit2 = create_object_box(
            ["commit a2d9e32", "tree a6b9f46", "parent aba6a21"], COMMIT_OBJ_COLOR)
        commit2.next_to(tree2, UP, buff=0.6)
        arrow5 = create_arrow(commit2.get_bottom(), tree2.get_top(), ARROW_COLOR)
        parent_arrow = create_arrow(commit2.get_left(), commit1.get_right(), ARROW_COLOR)
        self.play(FadeIn(arrow5), FadeIn(commit2), FadeIn(parent_arrow))
        self.wait()

        # move main (and HEAD along with it) to the new commit
        self.remove(ref_arrow, head_arrow)
        g = Group(main_ref, head_ref)
        self.play(g.animate.next_to(commit2, UP, buff=0.4))
        new_ref_arrow = create_arrow(main_ref.get_bottom(), commit2.get_top(), ARROW_COLOR)
        new_head_arrow = create_arrow_between_refs(head_ref, main_ref, DOWN)
        self.play(FadeIn(new_ref_arrow), FadeIn(new_head_arrow))

        self.wait(2)

        note = Text(
            "Every commit is a brand new blob + tree + commit object,\nnever a diff. Nothing here got modified, only added.",
            font="Noto Sans", color=WHITE).scale(0.35)
        note.to_edge(DOWN)
        self.play(Write(note))
        self.wait(3)
