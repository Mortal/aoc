from aoc import lines

p1 = 0
p2 = 0
for line in lines:
    maxsofar = []
    for char in line:
        maxsofar.append(maxsofar[-1] + char if maxsofar else char)
        for i in range(len(maxsofar))[::-1]:
            maxsofar[i] = max(maxsofar[i], f"{maxsofar[i-1]}{char}" if i else char)
        assert [len(x) for x in maxsofar] == list(range(1, len(maxsofar) + 1)), maxsofar
    p1 += int(maxsofar[1])
    p2 += int(maxsofar[11])
print(p1)
print(p2)
