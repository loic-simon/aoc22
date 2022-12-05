# https://adventofcode.com/2022/day/5

import queue
import re
import sys


data = sys.stdin.readlines()
lines = [row.strip() for row in data]

blank_line_index = next(index for index, line in enumerate(lines) if not line)
initial_lines = lines[: blank_line_index - 1]
piles_numbers_line = lines[blank_line_index - 1]
process_lines = lines[blank_line_index + 1 :]

piles_numbers = [int(pile_number) for pile_number in piles_numbers_line.split()]


def read_initial_configuration() -> dict[int, queue.LifoQueue]:
    stacks = {pile_number: queue.LifoQueue() for pile_number in piles_numbers}

    for line in reversed(initial_lines):
        for index, pile_number in enumerate(piles_numbers):
            if crate := line[4 * index : 4 * (index + 1)].strip("[ ]"):
                stacks[pile_number].put(crate)

    return stacks


pattern = re.compile(r"move (\d+) from (\d+) to (\d+)\s*")
process = []
for line in process_lines:
    n_moves, origin, destination = re.fullmatch(pattern, line).groups()
    process.append((int(n_moves), int(origin), int(destination)))


stacks = read_initial_configuration()


for n_moves, origin, destination in process:
    for _ in range(n_moves):
        stacks[destination].put_nowait(stacks[origin].get_nowait())


print("Part I:", "".join(stack.get() for stack in stacks.values()))


stacks = read_initial_configuration()

crane_queue = queue.LifoQueue()
for n_moves, origin, destination in process:
    for _ in range(n_moves):
        crane_queue.put_nowait(stacks[origin].get_nowait())
    for _ in range(n_moves):
        stacks[destination].put_nowait(crane_queue.get_nowait())

print("Part II:", "".join(stack.get() for stack in stacks.values()))
