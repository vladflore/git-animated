### Animating Git

...for learning purposes

#### Modules

| File | Scene | Git concept |
|---|---|---|
| `linear-commits.py` | `LinearCommits` | basic commits and branching |
| `mergeff.py` | `MergeFF` | fast-forward merge |
| `merge3w.py` | `Merge3W` | three-way merge |
| `rebase.py` | `Rebase` | rebase |
| `cherrypick.py` | `CherryPick` | cherry-pick |

#### Setup

Dependencies are managed with [uv](https://docs.astral.sh/uv/). To create the virtual environment and install all dependencies:

```sh
uv sync
```

#### How to run

```sh
uv run manim -p linear-commits.py
uv run manim -p mergeff.py
uv run manim -p merge3w.py
uv run manim -p rebase.py
uv run manim -p cherrypick.py
```

Note:

- add `--format=gif` to change the output format
- omit `-p` if you don't want the video to open automatically after rendering
