from aoc import mat

s = 0
locs = []
for ij in mat.keys():
    if all(mat.read(ij) < mat.read(n) for n in mat.neigh4inside(ij)):
        s += 1 + int(mat.read(ij))
        locs.append(ij)
print("part 1", s)
szs = []
for loc in locs:
    sz = 1
    for ij in mat.bfs(loc):
        for n in mat.neigh4inside(ij):
            if mat.read(n) != "9":
                if mat.bfs.enqueue(n):
                    sz += 1
    szs.append(sz)
a,b,c = sorted(szs)[-3:]
print("part 2", a*b*c)
