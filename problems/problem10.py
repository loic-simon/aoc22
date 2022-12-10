# https://adventofcode.com/2022/day/10

import sys


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


x_values = [1]

for line in lines:
    match line.split():
        case "noop",:
            x_values.append(x_values[-1])
        case "addx", value:
            x_values.append(x_values[-1])
            x_values.append(x_values[-1] + int(value))
        case _:
            raise RuntimeError


def cycle_val(num: int) -> int:
    return num * x_values[num - 1]


print("Part I:", cycle_val(20) + cycle_val(60) + cycle_val(100) + cycle_val(140) + cycle_val(180) + cycle_val(220))


pixels = []
x_value = 1

for line in lines:
    match line.split():
        case "noop",:
            pixels.append(x_value - 1 <= (len(pixels) % 40) <= x_value + 1)
        case "addx", value:
            pixels.append(x_value - 1 <= (len(pixels) % 40) <= x_value + 1)
            pixels.append(x_value - 1 <= (len(pixels) % 40) <= x_value + 1)
            x_value += int(value)
        case _:
            raise RuntimeError

print("Part II:")
for row in range(6):
    for pixel in pixels[row * 40 : (row + 1) * 40]:
        print("██" if pixel else "  ", end="")
    print()
