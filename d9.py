with open("d9.in") as fp:
    inp = fp.read()
if 0:
    inp = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

import numpy as np

s = 0
for line in inp.strip().splitlines():
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
for line in inp.strip().splitlines():
    xs = [np.fromiter(map(int, line.split()), dtype=np.intp)]
    while np.any(xs[-1] != 0):
        xs.append(np.diff(xs[-1]))
    inc = 0
    for x in xs[::-1]:
        inc = x[0] - inc
        print(inc, *x)
    s += inc
print(s)
