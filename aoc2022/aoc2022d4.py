from aoc import lineints
s = 0
for a, b, c, d in lineints:
    if a <= c <= d <= b or c <= a <= b <= d:
        s += 1
print("part 1:", s)
s = 0
for a, b, c, d in lineints:
    if a <= c <= b or c <= a <= d:
        s += 1
print("part 2:", s)
