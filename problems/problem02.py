# https://adventofcode.com/2022/day/2

from __future__ import annotations

import enum
import sys
from typing import Self


class RPS(enum.Enum):
    ROCK = enum.auto()
    PAPER = enum.auto()
    SCISSORS = enum.auto()

    @property
    def beat_table(self) -> dict[Self, Self]:
        return {
            RPS.ROCK: RPS.SCISSORS,
            RPS.PAPER: RPS.ROCK,
            RPS.SCISSORS: RPS.PAPER,
        }

    @property
    def beat_table_reverse(self) -> dict[Self, Self]:
        return {value: key for key, value in self.beat_table.items()}

    @classmethod
    def from_opponent(cls, value: str) -> Self:
        return {
            "A": RPS.ROCK,
            "B": RPS.PAPER,
            "C": RPS.SCISSORS,
        }[value]

    @classmethod
    def from_me(cls, value: str) -> Self:
        return {
            "X": RPS.ROCK,
            "Y": RPS.PAPER,
            "Z": RPS.SCISSORS,
        }[value]

    @property
    def choice_score(self) -> int:
        return {
            RPS.ROCK: 1,
            RPS.PAPER: 2,
            RPS.SCISSORS: 3,
        }[self]

    def beat_score(self, other: Self) -> int:
        if self is other:
            return Result.DRAW.score
        if self.beat_table[self] is other:
            return Result.WIN.score
        return Result.LOSE.score

    def to_play_from_result(self, result: Result) -> Self:
        match result:
            case Result.LOSE:
                return self.beat_table[self]
            case Result.DRAW:
                return self
            case Result.WIN:
                return self.beat_table_reverse[self]


class Result(enum.Enum):
    WIN = enum.auto()
    DRAW = enum.auto()
    LOSE = enum.auto()

    @classmethod
    def from_value(cls, value: str) -> Self:
        return {
            "X": Result.LOSE,
            "Y": Result.DRAW,
            "Z": Result.WIN,
        }[value]

    @property
    def score(self) -> int:
        return {
            Result.LOSE: 0,
            Result.DRAW: 3,
            Result.WIN: 6,
        }[self]


data = sys.stdin.readlines()


score = 0
for row in data:
    opponent_value, me_value = row.split()
    opponent = RPS.from_opponent(opponent_value)
    me = RPS.from_me(me_value)

    score += me.choice_score + me.beat_score(opponent)


print("Part I:", score)


score = 0
for row in data:
    opponent_value, result_value = row.split()
    opponent = RPS.from_opponent(opponent_value)
    result = Result.from_value(result_value)

    me = opponent.to_play_from_result(result)
    score += me.choice_score + me.beat_score(opponent)


print("Part II:", score)
