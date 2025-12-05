from aoc import sectionints

rangeints, idlines = sectionints
ids = [i for i, in idlines]
ranges = [range(a, b+1) for a, b in rangeints]
print(sum(any(i in r for r in ranges) for i in ids))
