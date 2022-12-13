# https://adventofcode.com/2022/day/13

import ast
from dataclasses import dataclass
from itertools import chain
import sys
from typing import Self


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


@dataclass
class Signal:
    value: int | list[int | list]

    def __lt__(self, other: Self) -> bool:
        if (result := self._is_lower(other)) is None:
            return True
        return result

    def _is_lower(self, other: Self) -> bool:
        match self.value, other.value:
            case int(), int():
                if self.value < other.value:
                    return True
                if self.value > other.value:
                    return False
                return None

            case list(), int():
                return self._is_lower(Signal([other.value]))

            case int(), list():
                return Signal([self.value])._is_lower(other)

            case list(), list():
                for self_item, other_item in zip(self.value, other.value):
                    if (result := Signal(self_item)._is_lower(Signal(other_item))) is not None:
                        return result

                if len(self.value) > len(other.value):
                    return False
                if len(other.value) > len(self.value):
                    return True
                return None

            case _:
                raise RuntimeError


signals = {
    index: (
        Signal(ast.literal_eval(lines[n_line])),
        Signal(ast.literal_eval(lines[n_line + 1])),
    )
    for index, n_line in enumerate(range(0, len(lines), 3), 1)
}

print("Part I:", sum(index for index, (signal_1, signal_2) in signals.items() if signal_1 < signal_2))


divisor_1 = Signal([[2]])
divisor_2 = Signal([[6]])

flat_signals: list[Signal] = list(chain(*signals.values())) + [divisor_1, divisor_2]
flat_signals.sort()

print("Part II:", (flat_signals.index(divisor_1) + 1) * (flat_signals.index(divisor_2) + 1))
