from aoc import lineints

def d(i, j):
    x1,y1,z1 = lineints[i]
    x2,y2,z2 = lineints[j]
    return (x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2

n = len(lineints)

def kruskal() -> tuple[int, int]:
    dists = sorted((d(i, j), i, j) for i in range(n) for j in range(i+1,n))

    rep = list(range(n))

    def findrep(i):
        while rep[i] != rep[rep[i]]:
            rep[i] = i = rep[rep[i]]
        return rep[i]

    conns = 0
    for dist, i, j in dists:
        if findrep(i) != findrep(j):
            rep[findrep(i)] = findrep(j)
            conns += 1
            if conns == n - 1:
                return i, j
    raise

def prim(s: int) -> tuple[int, int]:
    ix = [0 if s == i else -1 for i in range(n)]
    ds = [(d(s, i), s, i) for i in range(n)]
    for it in range(1, n):
        _d, i, j = min(ds[i] for i in range(n) if ix[i] == -1)
        assert ix[i] != -1
        assert ix[j] == -1
        ix[j] = it
        if it == n - 1:
            return tuple(sorted((i, j)))
        for i in range(n):
            if ix[i] == -1:
                ds[i] = min(ds[i], (d(j, i), j, i))
    raise

ri, rj = kruskal()
print(lineints[ri][0] * lineints[rj][0])
for i in range(n):
    p = prim(i)
    if p != (ri, rj):
        print(i, p, (ri, rj), lineints[p[0]][0] * lineints[p[1]][0], lineints[i])
