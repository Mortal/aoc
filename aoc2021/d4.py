from aoc import sectionints

(nums,), *boards = sectionints

result = []
for rows in boards:
    rows = [[nums.index(n) for n in row] for row in rows]
    columns = list(zip(*rows))
    when = min(*[max(r) for r in rows + columns])
    unmarked = sum(nums[i] for row in rows for i in row if i > when)
    score = unmarked * nums[when]
    result.append((when, score))
print(min(result))
print(max(result))
