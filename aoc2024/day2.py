from aoc import lineints
import numpy as np
p1 = 0
p2 = 0
for line in lineints:
    row = np.array(line)
    c = row[1:] > row[:-1]
    d = row[1:] < row[:-1]
    e = np.abs(np.diff(row.astype(float)))
    if (c.all() or d.all()) and ((1 <= e) & (e <= 3)).all():
        p1 += 1
        p2 += 1
        continue
    for i in range(len(row)):
        row2 = np.r_[row[:i], row[i+1:]]
        c = row2[1:] > row2[:-1]
        d = row2[1:] < row2[:-1]
        e = np.abs(np.diff(row2.astype(float)))
        if (c.all() or d.all()) and ((1 <= e) & (e <= 3)).all():
            p2 += 1
            break
print(p1)
print(p2)
