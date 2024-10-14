with open("aoc2022d4.txt") as fp:
    lines = fp.read().split()
s = 0
for line in lines:
    a, b, c, d = map(int, line.replace("-", ",").split(","))
    if a <= c <= b or c <= a <= d:
        s += 1
print(s)
