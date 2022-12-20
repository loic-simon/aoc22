# https://adventofcode.com/2022/day/17

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from itertools import permutations, cycle
from math import factorial
from pprint import pprint
import re
import subprocess
import sys
import time
from typing import NamedTuple, Self
from tqdm import tqdm

data = sys.stdin.readlines()
lines = [line.strip() for line in data]

[line] = lines
flows = [char == ">" for char in line]


class Pos(NamedTuple):
    x: int
    y: int


CAVE: set[Pos]


def initial_cave() -> set[Pos]:
    return {Pos(0, 0), Pos(1, 0), Pos(2, 0), Pos(3, 0), Pos(4, 0), Pos(5, 0), Pos(6, 0)}


@dataclass
class Rock:
    pixels: set[Pos]

    def _change_pixels(self, new_pixels: set[Pos]) -> bool:
        if any(pos in CAVE or pos.x < 0 or pos.x > 6 for pos in new_pixels):
            return False
        self.pixels = new_pixels
        return True

    def move_left(self) -> bool:
        return self._change_pixels({Pos(pos.x - 1, pos.y) for pos in self.pixels})

    def move_right(self) -> bool:
        return self._change_pixels({Pos(pos.x + 1, pos.y) for pos in self.pixels})

    def move_down(self) -> bool:
        return self._change_pixels({Pos(pos.x, pos.y - 1) for pos in self.pixels})


rocks = [
    Rock(pixels={Pos(0, 0), Pos(1, 0), Pos(2, 0), Pos(3, 0)}),
    Rock(pixels={Pos(1, 0), Pos(0, 1), Pos(1, 1), Pos(2, 1), Pos(1, 2)}),
    Rock(pixels={Pos(0, 0), Pos(1, 0), Pos(2, 0), Pos(2, 1), Pos(2, 2)}),
    Rock(pixels={Pos(0, 0), Pos(0, 1), Pos(0, 2), Pos(0, 3)}),
    Rock(pixels={Pos(0, 0), Pos(1, 0), Pos(0, 1), Pos(1, 1)}),
]


def draw(falling_rock: Rock | None) -> None:
    y_max = max(pos.y for pos in CAVE)
    for y in range(y_max + 7, -1, -1):
        for x in range(7):
            if Pos(x, y) in CAVE:
                print("#", end="")
            elif falling_rock and Pos(x, y) in falling_rock.pixels:
                print("@", end="")
            else:
                print(".", end="")
        print()
    print()
    print()
    time.sleep(1)


def count(n_rocks: int):
    global CAVE

    rocks_in = cycle(rocks)
    flows_in = cycle(flows)
    rocks_count = 0
    falling_rock: Rock | None = None

    bar = iter(tqdm(range(n_rocks)))

    while rocks_count < n_rocks:
        # print(rocks_count)
        if not falling_rock:
            y_max = max(pos.y for pos in CAVE)
            falling_rock = Rock({Pos(pos.x + 2, pos.y + y_max + 4) for pos in next(rocks_in).pixels})

        # draw(falling_rock)

        if next(flows_in):
            # print("RIGHT")
            falling_rock.move_right()
        else:
            # print("LEFT")
            falling_rock.move_left()

        # draw(falling_rock)

        if not falling_rock.move_down():
            CAVE |= falling_rock.pixels
            # CAVE = {max((pos for pos in CAVE if pos.x == x), key=lambda pos: pos.y) for x in range(7)}
            falling_rock = None
            rocks_count += 1
            next(bar)


CAVE = initial_cave()
count(2022)

print("Part I:", max(pos.y for pos in CAVE))

# CAVE = initial_cave()
# count(1000000000000)

# print("Part II:", max(pos.y for pos in CAVE))
