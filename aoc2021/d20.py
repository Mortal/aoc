from aoc import sectionlines
import numpy as np

algostr = "".join(sectionlines[0])
assert len(algostr) == 512
algo = np.asarray([int(c == "#") for c in algostr])
sign = algo[0]

img = np.asarray([[int(c == "#") for c in line] for line in sectionlines[1]])
inf = 0

print("\n".join("".join(".#"[c] for c in row) for row in img))
print("--------------")
for round in range(50):
    n, m = img.shape
    inf = 0 if round % 2 == 0 else sign
    img = np.c_[[inf] * n, [inf] * n, img, [inf] * n, [inf] * n]
    assert img.shape == (n, m + 4)
    img = np.r_[2*[[inf] * (4 + m)], img, 2*[[inf] * (4 + m)]]
    assert img.shape == (n+4,m+4)
    parts = [2 ** (8-i) * img[(i // 3):, (i % 3):][:n+2,:m+2] for i in range(9)]
    assert all(p.shape == (n+2,m+2) for p in parts), [p.shape for p in parts]
    bits = np.sum(parts, axis=0)
    img = algo[bits]
    print("\n".join("".join(".#"[c] for c in row) for row in img))
    print("--------------", np.sum(img))
