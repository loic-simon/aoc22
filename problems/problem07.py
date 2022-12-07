# https://adventofcode.com/2022/day/7

import sys


data = sys.stdin.readlines()
lines = [line.strip() for line in data]


ROOT = {"_size": 0}
FILE_SYSTEM = {"/": ROOT}

path = []

tfs = 0
for line in lines:
    # print(line)
    match line.split():
        case "$", "cd", "/":
            path = [ROOT]
        case "$", "cd", "..":
            path.pop(-1)
        case "$", "cd", dir:
            path.append(path[-1][dir])
        case "$", "ls":
            continue
        case "dir", dir:
            path[-1].setdefault(dir, {"_size": 0})
        case size, file:
            size = int(size)
            tfs += size
            path[-1][file] = size
            for dir in path:
                dir["_size"] += size
        case _:
            raise RuntimeError

folders = {}


def flatten_folders(root_name: str, root_dir: dict[str, int | dict]) -> None:
    folders[root_name] = root_dir["_size"]

    for dirname, item in root_dir.items():
        if isinstance(item, int):
            continue
        flatten_folders(f"{root_name}/{dirname}", item)


flatten_folders("", ROOT)

print("Part I:", sum(size for size in folders.values() if size <= 100000))

total_space = 70000000
free_space = total_space - ROOT["_size"]

needed_space = 30000000
space_to_clean = needed_space - free_space

print("Part II:", min(size for size in folders.values() if size >= space_to_clean))
