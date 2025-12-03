from aoc import lines

p1 = 0
for line in lines:
    m = max(int(a + b) for i, a in enumerate(line) for b in line[i+1:])
    p1 += m
print(p1)
