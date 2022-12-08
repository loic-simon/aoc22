# https://adventofcode.com/2022/day/8

import sys
from typing import Iterable


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


class Tree:
    def __init__(self, value: str) -> None:
        self.height = int(value)


TREES = [[Tree(cell) for cell in row] for row in lines]


def filter_visible(trees: Iterable[Tree]) -> Iterable[Tree]:
    max_height = -1
    for tree in trees:
        if tree.height > max_height:
            max_height = tree.height
            yield tree


visible_trees = set()

for line in TREES:
    visible_trees |= set(filter_visible(line))
    visible_trees |= set(filter_visible(reversed(line)))

for i_col in range(len(TREES[0])):
    visible_trees |= set(filter_visible(line[i_col] for line in TREES))
    visible_trees |= set(filter_visible(line[i_col] for line in reversed(TREES)))


print("Part I:", len(visible_trees))


def compute_view_range(trees: Iterable[Tree], roof: int = 9) -> int:
    view_range = 0
    for tree in trees:
        view_range += 1
        if tree.height >= roof:
            break
    return view_range


max_scenic_score = 0

for i_line, line in enumerate(TREES):
    for i_col, tree in enumerate(line):
        view_right = compute_view_range(line[i_col + 1 :], roof=tree.height)
        view_left = compute_view_range(reversed(line[:i_col]), roof=tree.height)
        view_down = compute_view_range((line_[i_col] for line_ in TREES[i_line + 1 :]), roof=tree.height)
        view_up = compute_view_range(reversed([line_[i_col] for line_ in TREES[:i_line]]), roof=tree.height)

        scenic_score = view_right * view_left * view_down * view_up
        if scenic_score > max_scenic_score:
            max_scenic_score = scenic_score

print("Part II:", max_scenic_score)
