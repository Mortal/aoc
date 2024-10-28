from aoc import ints

# Part 1: min sum L1 dist = median
med = sorted(ints)[len(ints)//2]
print(sum(abs(i-med) for i in ints))
# Part 2: min sum L2 dist = average (rounded up or down)
avg = int(sum(ints)/len(ints))
sqrs = lambda x: x*(x+1)//2
cost = lambda x: sqrs(abs(x-avg))
c1 = sum(cost(x) for x in ints)
avg += 1
c2 = sum(cost(x) for x in ints)
print(min(c1, c2))
