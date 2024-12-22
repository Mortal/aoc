from aoc import ints
import numpy as np

p1 = 0
p2 = {}
for i in ints:
    seq = [i]
    for _ in range(2000):
        i = (i ^ (i * 64)) % 16777216
        i = (i ^ (i // 32)) % 16777216
        i = (i ^ (i * 2048)) % 16777216
        seq.append(i)
    p1 += i
    arr = np.array(seq)
    diffs = np.diff(arr % 10)
    sigs = [tuple(row) for row in np.c_[diffs[:-3], diffs[1:-2], diffs[2:-1], diffs[3:]].tolist()]
    d = dict(zip(sigs[::-1], seq[::-1]))
    for sig, num in d.items():
        p2[sig] = p2.get(sig, 0) + num % 10
print(p1)
print(max(p2.values()))
