import bisect
from aoc import cmat
# 8:16:36
# 8:24
start, = cmat.findall("^")
g = start
obs = set(cmat.findall("#"))
byrow = {}
bycol = {}
for p in cmat.findall("#"):
    byrow.setdefault(int(p.imag), []).append(int(p.real))
    bycol.setdefault(int(p.real), []).append(int(p.imag))
dir = complex(0,-1)
visited = {}

positions = []
count = 0
while (g,dir) not in visited and 0 <= g.real < len(cmat[0]) and 0 <= g.imag < len(cmat):
    if g == start:
        print(g,dir,count)
    visited[g,dir] = count
    count += 1
    positions.append((g, dir))
    while g + dir in obs:
        dir = dir * 1j
        visited[g,dir] = count
        count += 1
        positions.append((g, dir))
    g += dir
print(len(set(g for g, dir in visited)))

paras = set()
for g, dir in positions:
    print(f"checkpara {g=}")
    r = dir * 1j
    #if (g, r) in visited and visited[g, r] < visited[g, dir] and g + dir not in obs:
    #    paras.add(g + dir)
    rr = r * 1j
    if r == 1 or r == -1:
        try:
            myrow = byrow[int(g.imag)]
        except KeyError:
            continue
        # right or left
        myix = bisect.bisect(myrow, int(g.imag))
        if r == -1:
            # left: subtract one
            myix -= 1
        if 0 <= myix < len(myrow):
            o = complex(myrow[myix], g.imag) - r
            print(f"check {o=} {rr=}")
            if (o, rr) in visited and visited[o, rr] < visited[g, dir]:
                if g + dir not in obs:
                    paras.add(g + dir)
    elif r == 1j or r == -1j:
        try:
            mycol = bycol[int(g.real)]
        except KeyError:
            continue
        # down or up
        myix = bisect.bisect(mycol, int(g.real))
        if r == -1j:
            # up: subtract one
            myix -= 1
        if 0 <= myix < len(mycol):
            o = complex(g.real, mycol[myix]) - r
            print(f"check {o=} {rr=}")
            if (o, rr) in visited and visited[o, rr] < visited[g, dir]:
                if g + dir not in obs:
                    paras.add(g + dir)
print(paras)
print(len(paras))
print("\n".join("".join("O" if complex(j, i) in paras else row[j] for j in range(len(row))) for i, row in enumerate(cmat)))
