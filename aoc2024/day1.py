from aoc import ints, Counter

xs, ys = ints[::2], ints[1::2]
xs.sort()
ys.sort()
s = 0
for x, y in zip(xs, ys):
    d = abs(x-y)
    s += d
print(s)

# Part 2
c = Counter(ys)
s = 0
for x in xs:
    s += x * c.get(x,0)
print(s)
