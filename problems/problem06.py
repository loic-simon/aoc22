# https://adventofcode.com/2022/day/6

import sys


[data] = sys.stdin.readlines()
line = data.strip()

bloc_4 = 4
while len(set(line[bloc_4 - 4 : bloc_4])) < 4:
    bloc_4 += 1


print("Part I:", bloc_4)


bloc_14 = 14
while len(set(line[bloc_14 - 14 : bloc_14])) < 14:
    bloc_14 += 1


print("Part II:", bloc_14)
