# https://adventofcode.com/2022/day/1

from collections import defaultdict
import sys

data = sys.stdin.readlines()

elf = 0
inventories = defaultdict(int)
for line in data:
    amount = line.strip()
    if not amount:
        elf += 1
        continue

    inventories[elf] += int(line)

print("Part I:", max(inventories.values()))
print("Part II:", sum(sorted(inventories.values())[-3:]))
