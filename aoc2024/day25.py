from aoc import sectionlines

locks = []
keys = []
for s in sectionlines:
    if s[0][0] == "#":
        conv = [next(i-1 for i in range(len(s)) if s[i][j] == ".") for j in range(len(s[0]))]
        locks.append(conv)
    else:
        conv = [next(len(s) - i - 1 for i in range(len(s)) if s[i][j] == "#") for j in range(len(s[0]))]
        keys.append(conv)
p1 = 0
for a in locks:
    for b in keys:
        if all(a[i] + b[i] <= 5 for i in range(len(a))):
            p1 += 1
print(p1)
