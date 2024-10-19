from aoc import inp

nums_str, *boards_str = inp.split("\n\n")
nums = list(map(int, nums_str.split(",")))

boards = []
for b in boards_str:
    board = [nums.index(n) for n in list(map(int, b.split()))]
