from aoc import cmat
p2 = True

start = complex(1, 0)
n, m = cmat.shape
goal = complex(m - 2, n - 1)

def neighbors(pos: complex) -> list[tuple[complex, bool, bool]]:
    if pos == start:
        return [(pos + 1j, False, False)]
    if pos == goal:
        return [(pos - 1j, False, False)]
    n = []
    oneway = {">": 1, "<": -1, "v": 1j, "^": -1j}.get(cmat.read(pos))
    for d in (1, -1, 1j, -1j):
        if cmat.read(pos + d) == "#":
            continue
        n.append((pos + d, oneway == d, oneway == -d))
    return n

vertices = [start]
edgelists: dict[complex, list[tuple[complex, int]]] = {start: []}
i = 0
while i < len(vertices):
    dfs = [vertices[i]]
    print("#", "dfs from", vertices[i])
    i += 1
    dist = {dfs[-1]: 0}
    oneway = {dfs[-1]: 0}
    while dfs:
        pos = dfs.pop()
        d = dist[pos]
        o = oneway[pos]
        ne = neighbors(pos)
        if pos != vertices[i-1] and len(ne) != 2:
            if pos not in edgelists:
                vertices.append(pos)
                edgelists[pos] = []
            # if o != -1:
            #     edgelists[vertices[i-1]].append((pos, d))
            if p2 or o != 1:
                edgelists[pos].append((vertices[i-1], d))
            continue
        for n, outbound, inbound in ne:
            if n in dist:
                continue
            dist[n] = d + 1
            if outbound:
                assert o != -1, (pos, cmat.read(pos), n, cmat.read(n))
                oneway[n] = 1
            elif inbound:
                assert o != 1
                oneway[n] = -1
            else:
                oneway[n] = o
            dfs.append(n)

if p2:
    print("graph {")
else:
    print("digraph {")
for pos in edgelists:
    for n, d in edgelists[pos]:
        if p2:
            if repr(pos) < repr(n):
                print(f'"{pos!r}" -- "{n!r}" [label="{d}"];')
        else:
            print(f'"{pos!r}" -> "{n!r}" [label="{d}"];')
print("}")

if not p2:
    endtime = {start: -1}
    t = 0
    dfs2 = [start]
    while dfs2:
        pos = dfs2.pop()
        if endtime[pos] == -2:
            endtime[pos] = t
            t += 1
            continue
        dfs2.append(pos)
        endtime[pos] = -2
        for n, d in edgelists[pos]:
            if n not in endtime:
                endtime[n] = -1
                dfs2.append(n)
    vertices = sorted(endtime, key=lambda v: -endtime[v])
    maxdist = {start: 0}
    for pos in vertices:
        for n, d in edgelists[pos]:
            dd = maxdist[pos] + d
            maxdist[n] = max(maxdist.get(n, dd), dd)
    print("#", vertices)
    print("#", maxdist[goal])

onpath = {}
path = []

assert goal in vertices

def rundfs(pos: complex, dist: int, depth: int) -> int:
    if pos == goal:
        if dist > 6400:
            print(dist, path)
        return dist
    if depth <= 5:
        print(path, dist)
    onpath[pos] = True
    path.append(pos)
    maxsofar = dist
    for n, d in edgelists[pos]:
        if onpath.get(n):
            continue
        maxsofar = max(maxsofar, rundfs(n, dist+d, depth+1))
    del onpath[pos]
    path.pop()
    return maxsofar

ans = rundfs(start, 0, 0)
assert ans < 6429, ans
print(ans)
