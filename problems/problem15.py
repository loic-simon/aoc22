# https://adventofcode.com/2022/day/15

import re
import subprocess
import sys
from typing import NamedTuple


data = sys.stdin.readlines()
lines = [line.strip() for line in data]

PATTERN = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def get_dist(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x1 - x2) + abs(y1 - y2)


class Sensor(NamedTuple):
    x: int
    y: int
    range: int


sensors: list[Sensor] = []
beacons: set[tuple[int, int]] = set()

for line in lines:
    match = PATTERN.fullmatch(line)
    sensor_x = int(match[1])
    sensor_y = int(match[2])
    beacon_x = int(match[3])
    beacon_y = int(match[4])

    beacons.add((beacon_x, beacon_y))
    sensors.append(Sensor(sensor_x, sensor_y, get_dist(sensor_x, sensor_y, beacon_x, beacon_y)))


y = 2000000
x_without_beacons = set()
for sensor in sensors:
    if sensor.y - sensor.range <= y <= sensor.y + sensor.range:
        x_without_beacons |= {
            x
            for x in range(sensor.x - sensor.range, sensor.x + sensor.range + 1)
            if get_dist(x, y, sensor.x, sensor.y) <= sensor.range and (x, y) not in beacons
        }

print("Part I:", len(x_without_beacons))


c_max = 4000000

C_CODE = f"""
#include <stdio.h>
#include <stdlib.h>

#define N_SENSORS {len(sensors)}
#define C_MAX {c_max}

const long sensors_x[N_SENSORS] = {{{",".join(str(sensor.x) for sensor in sensors)}}};
const long sensors_y[N_SENSORS] = {{{",".join(str(sensor.y) for sensor in sensors)}}};
const long sensors_range[N_SENSORS] = {{{",".join(str(sensor.range) for sensor in sensors)}}};

int main(int argc, char const *argv[]) {{
    long x, y;
    int i = 0;
    for (y = 0; y <= C_MAX; y++) {{
        for (x = 0; x <= C_MAX; x++) {{
            for (int k = 0; k < N_SENSORS; k++) {{
                if (labs(x - sensors_x[i]) + labs(y - sensors_y[i]) <= sensors_range[i])  goto endfor;
                i++;
                i %= N_SENSORS;
            }}
            goto finish;
            endfor:;
        }}
    }}
    return 1;
    finish:
    printf("%ld,%ld", x, y);
    return 0;
}}
"""

subprocess.run(["gcc", "-O3", "-o", "./.p15", "-xc", "-"], input=C_CODE, text=True, check=True)
try:
    result = subprocess.run(["./.p15"], capture_output=True, text=True, check=True)
finally:
    subprocess.run(["rm", "./.p15"])

x, y = result.stdout.split(",")
tuning_frequency = c_max * int(x) + int(y)

print("Part II:", tuning_frequency)
