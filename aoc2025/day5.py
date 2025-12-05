from aoc import sectionints

rangeints, idlines = sectionints
ids = [i for i, in idlines]
ranges = [range(a, b+1) for a, b in rangeints]
p1 = sum(any(i in r for r in ranges) for i in ids)
print(p1)
vs = [(a, 1) for a, b in rangeints] + [(b+1, -1) for a, b in rangeints]
prev = 0
thesum = 0
p2 = 0
for val, sign in sorted(vs):
    if thesum:
        p2 += val - prev
    thesum += sign
    prev = val
print(p2)
