# https://adventofcode.com/2022/day/9

from dataclasses import dataclass
import enum
import sys
from time import sleep
from typing import NamedTuple


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


class Direction(enum.Enum):
    LEFT = "L"
    RIGHT = "R"
    UP = "U"
    DOWN = "D"


@dataclass()
class Pos:
    x: int
    y: int


moves = []

for line in lines:
    dir, n_steps = line.split()
    for _ in range(int(n_steps)):
        moves.append(Direction(dir))


head = Pos(0, 0)
tail = Pos(0, 0)

visited_pos = {(tail.x, tail.y)}

for move in moves:
    match move:
        case Direction.LEFT:
            head.x -= 1
        case Direction.RIGHT:
            head.x += 1
        case Direction.UP:
            head.y -= 1
        case Direction.DOWN:
            head.y += 1

    if abs(tail.y - head.y) ** 2 + abs(tail.x - head.x) ** 2 >= 4:
        match move:
            case Direction.LEFT:
                tail = Pos(head.x + 1, head.y)
            case Direction.RIGHT:
                tail = Pos(head.x - 1, head.y)
            case Direction.UP:
                tail = Pos(head.x, head.y + 1)
            case Direction.DOWN:
                tail = Pos(head.x, head.y - 1)

        visited_pos.add((tail.x, tail.y))


print("Part I:", len(visited_pos))


knots = [Pos(0, 0) for _ in range(10)]
visited_pos = {(0, 0)}

for move in moves:
    match move:
        case Direction.LEFT:
            knots[0].x -= 1
        case Direction.RIGHT:
            knots[0].x += 1
        case Direction.UP:
            knots[0].y -= 1
        case Direction.DOWN:
            knots[0].y += 1

    for i in range(1, 10):
        delta_x = knots[i].x - knots[i - 1].x
        delta_y = knots[i].y - knots[i - 1].y

        if abs(delta_x) ** 2 + abs(delta_y) ** 2 >= 4:
            if delta_x:
                knots[i].x -= delta_x / abs(delta_x)
            if delta_y:
                knots[i].y -= delta_y / abs(delta_y)

    visited_pos.add((knots[9].x, knots[9].y))


print("Part II:", len(visited_pos))
