from aoc import inp

nums_str, *boards_str = inp.split("\n\n")
nums = list(map(int, nums_str.split(",")))

boards = []
for b in boards_str:
    rows = [[nums.index(n) for n in list(map(int, line.split()))] for line in b.splitlines()]
    columns = list(zip(*rows))
    when = min(*[max(r) for r in rows + columns])
    unmarked = sum(nums[i] for row in rows for i in row if i > when)
    score = unmarked * nums[when]
    boards.append((when, score))
print(min(boards))
print(max(boards))
