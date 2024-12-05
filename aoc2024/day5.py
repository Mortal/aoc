from aoc import sectionints

edges, updates = sectionints
edgeset = {(i,j) for i,j in edges}
p1 = 0
p2 = 0
for u in updates:
    uu = sorted(u, key=lambda i: sum((j, i) in edgeset for j in u))
    if any((j, i) in edgeset for ix, i in enumerate(u) for j in u[ix+1:]):
        p2 += uu[len(uu)//2]
    else:
        p1 += u[len(u)//2]
print(p1)
print(p2)
