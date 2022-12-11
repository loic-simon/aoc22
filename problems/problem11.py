# https://adventofcode.com/2022/day/11

from dataclasses import dataclass
import math
import operator
import re
import sys
from typing import Callable, Iterator


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test_divisible_by: int
    target_if_true: int
    target_if_false: int
    activity: int = 0

    def round(self, relief_func: Callable[[int], int]) -> Iterator[tuple[int, int]]:
        for item in self.items:
            item = self.operation(item)
            item = relief_func(item)
            if item % self.test_divisible_by == 0:
                yield item, self.target_if_true
            else:
                yield item, self.target_if_false

        self.activity += len(self.items)
        self.items = []


PATTERN = re.compile(
    r"Monkey (?P<monkey_id>\d+):\n"
    r"Starting items: (?P<items>.+)\n"
    r"Operation: new = (?P<op_left>\S+) (?P<op_op>\S+) (?P<op_right>\S+)\n"
    r"Test: divisible by (?P<test_divisible_by>\d+)\n"
    r"If true: throw to monkey (?P<target_if_true>\d+)\n"
    r"If false: throw to monkey (?P<target_if_false>\d+)"
)
OPERATORS = {"+": operator.add, "*": operator.mul}


def parse_operation(left: str, op: str, right: str) -> Callable[[int], int]:
    return lambda item: OPERATORS[op](
        item if right == "old" else int(right),
        item if left == "old" else int(left),
    )


def init_monkeys() -> dict[int, Monkey]:
    monkeys: dict[int, Monkey] = {}

    for i_line in range(0, len(lines), 7):
        monkey_str = "\n".join(lines[i_line : i_line + 7]).strip()
        if not monkey_str:
            continue

        match = PATTERN.fullmatch(monkey_str)
        monkeys[int(match["monkey_id"])] = Monkey(
            items=[int(item.strip()) for item in match["items"].split(",")],
            operation=parse_operation(match["op_left"], match["op_op"], match["op_right"]),
            test_divisible_by=int(match["test_divisible_by"]),
            target_if_true=int(match["target_if_true"]),
            target_if_false=int(match["target_if_false"]),
        )
    return monkeys


def compute_monkey_business(monkeys: dict[int, Monkey]) -> int:
    monkeys_by_activity = sorted(monkeys.values(), key=lambda monkey: monkey.activity, reverse=True)
    monkey_business = monkeys_by_activity[0].activity * monkeys_by_activity[1].activity
    return monkey_business


monkeys = init_monkeys()

for i_round in range(20):
    for monkey_id, monkey in monkeys.items():
        for item, target in monkey.round(relief_func=lambda item: int(item / 3)):
            monkeys[target].items.append(item)

print("Part I:", compute_monkey_business(monkeys))


monkeys = init_monkeys()
common_divisor = math.prod(monkey.test_divisible_by for monkey in monkeys.values())

for i_round in range(10000):
    for monkey_id, monkey in monkeys.items():
        for item, target in monkey.round(relief_func=lambda item: item % common_divisor):
            monkeys[target].items.append(item)


print("Part II:", compute_monkey_business(monkeys))
