# https://adventofcode.com/2022/day/4

import sys


data = sys.stdin.readlines()
lines = [row.strip() for row in data]


sets = []
for line in lines:
    left, right = line.split(",")
    left_start, left_end = left.split("-")
    right_start, right_end = right.split("-")

    left_set = set(range(int(left_start), int(left_end) + 1))
    right_set = set(range(int(right_start), int(right_end) + 1))

    sets.append((left_set, right_set))

    print(len(left_set), len(right_set), len(left_set | right_set))


print("Part I:", len([1 for left_set, right_set in sets if not (left_set - right_set) or not (right_set - left_set)]))
print("Part II:", len([1 for left_set, right_set in sets if left_set & right_set]))
