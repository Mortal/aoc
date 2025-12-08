from aoc import lineints
from math import prod

def d(i, j):
    x1,y1,z1 = lineints[i]
    x2,y2,z2 = lineints[j]
    return (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2

n = len(lineints)
dists = sorted((d(i, j), i, j) for i in range(n) for j in range(i+1,n))

rep = list(range(n))

def findrep(i):
    while rep[i] != rep[rep[i]]:
        rep[i] = i = rep[rep[i]]
    return rep[i]

conns = 0
for dist, i, j in dists:
    # print(dist, i, j, findrep(i), findrep(j), lineints[i], lineints[j])
    if findrep(i) != findrep(j):
        rep[findrep(i)] = findrep(j)
        conns += 1
        if conns == n - 1:
            print(lineints[i][0] * lineints[j][0])
            exit()
sizes = {}
for i in range(n):
    r = findrep(i)
    sizes[r] = sizes.get(r, 0) + 1
print(sizes)
print(sum(sizes.values()))
print(prod(sorted(sizes.values())[-3:]))
