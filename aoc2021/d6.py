from aoc import inp, path
from collections import Counter

nums = list(map(int, inp.split(",")))
counts = Counter(nums)
state = [counts[i] for i in range(7)]
b7 = counts[7]
b8 = counts[8]
for day in range(256):
    if "test" not in path and day < 19:
        s = ",".join(x for i, s in enumerate(state[day % 7:] + state[:day % 7] + [b7,b8]) for x in s * [str(i)])
        print(f"After {day:2d}: {s} {sum(state)+b7+b8}")
    b9 = state[day % 7]
    state[day % 7] += b7
    b7 = b8
    b8 = b9
    if day == 79:
        print(sum(state) + b7 + b8)
print(sum(state) + b7 + b8)
