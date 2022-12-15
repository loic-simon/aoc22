# https://adventofcode.com/2022/day/14

from itertools import pairwise
import sys


data = sys.stdin.readlines()
lines = [line.strip() for line in data]

initial_rocks = set()

for line in lines:
    for start, end in pairwise(line.split(" -> ")):
        x1, y1 = start.split(",")
        x2, y2 = end.split(",")
        start_x = min(int(x1), int(x2))
        end_x = max(int(x1), int(x2))
        start_y = min(int(y1), int(y2))
        end_y = max(int(y1), int(y2))

        if start_x == end_x:
            for y in range(start_y, end_y + 1):
                initial_rocks.add((start_x, y))
        elif start_y == end_y:
            for x in range(start_x, end_x + 1):
                initial_rocks.add((x, start_y))
        else:
            raise RuntimeError


rocks = initial_rocks.copy()
y_max = max(y for (x, y) in rocks)

count = 0
while True:
    x = 500
    y = 0

    if (x, y) in rocks:
        raise RuntimeError

    while y <= y_max:
        if (x, y + 1) not in rocks:
            y += 1
        elif (x - 1, y + 1) not in rocks:
            x -= 1
            y += 1
        elif (x + 1, y + 1) not in rocks:
            x += 1
            y += 1
        else:
            rocks.add((x, y))
            count += 1
            break
    else:
        break

print("Part I:", count)


rocks = initial_rocks.copy()
y_floor = y_max + 1

count = 0
while True:
    x = 500
    y = 0

    if (x, y) in rocks:
        break

    while True:
        if y < y_floor and (x, y + 1) not in rocks:
            y += 1
        elif y < y_floor and (x - 1, y + 1) not in rocks:
            x -= 1
            y += 1
        elif y < y_floor and (x + 1, y + 1) not in rocks:
            x += 1
            y += 1
        else:
            rocks.add((x, y))
            count += 1
            break


print("Part II:", count)
