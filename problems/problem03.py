# https://adventofcode.com/2022/day/3

import string
import sys


PRIORITIES = {letter: index for index, letter in enumerate(string.ascii_letters, 1)}


data = sys.stdin.readlines()
lines = [row.strip() for row in data]


commons = []
score = 0
for line in lines:
    pack_size = len(line)
    part_1 = line[: pack_size // 2]
    part_2 = line[pack_size // 2 :]
    common_letters = set(part_1) & set(part_2)

    commons.append(common_letters)
    score += sum(PRIORITIES[letter] for letter in common_letters)


print("Part I:", score)


score_2 = 0
for index in range(0, len(lines), 3):
    [common_in_group] = set(lines[index]) & set(lines[index + 1]) & set(lines[index + 2])
    score_2 += PRIORITIES[common_in_group]

print("Part I:", score_2)
