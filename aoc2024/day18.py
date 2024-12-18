from aoc import lineints, path

if "samp" in path:
    sz = 7
    c = 12
else:
    sz = 71
    c = 1024


def test(c):
    sx = sy = 0
    ex = ey = sz - 1
    bfs = [(sx, sy)]
    dist={(sx,sy):0}
    blocks = {(x,y) for x,y in lineints[:c]}
    i = 0
    while i < len(bfs):
        x, y = bfs[i]
        i += 1
        for (dx,dy) in ((1,0),(-1,0),(0,1),(0,-1)):
            if 0 <= x+dx < sz and 0 <= y+dy < sz and (x+dx,y+dy) not in blocks and (x+dx,y+dy) not in dist:
                dist[(x+dx,y+dy)] = dist[x,y] + 1
                bfs.append((x+dx,y+dy))
    return dist.get((ex,ey))


print(test(c))
lo = c
hi = len(lineints)
while lo + 1 < hi:
    mid = lo + (hi - lo) // 2
    if test(mid) is None:
        hi = mid
    else:
        lo = mid
print(lo)
print(f"{','.join(map(str,lineints[lo]))}")
