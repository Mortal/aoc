from aoc import lines
import numpy as np

s = 0
for line in lines:
    xs = [np.fromiter(map(int, line.split()), dtype=np.intp)]
    while np.any(xs[-1] != 0):
        xs.append(np.diff(xs[-1]))
    inc = 0
    for x in xs[::-1]:
        inc = x[-1] + inc
        print(*x, inc)
    s += inc
print(s)

s = 0
for line in lines:
    xs = [np.fromiter(map(int, line.split()), dtype=np.intp)]
    while np.any(xs[-1] != 0):
        xs.append(np.diff(xs[-1]))
    inc = 0
    for x in xs[::-1]:
        inc = x[0] - inc
        print(inc, *x)
    s += inc
print(s)
