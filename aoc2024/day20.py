from aoc import cmat, Counter


realdist = float("inf")
st, = cmat.findall("S")
en, = cmat.findall("E")

for pos in cmat.bfs(en):
    for n in cmat.neigh4(pos):
        if cmat.read(n) in (".", "S", "E"):
            cmat.bfs.enqueue(n)
from_end = {**cmat.bfs.dist}
print(from_end[st])
p1 = {}
p2 = {}
t = [complex(x,y) for x in range(-20,21) for y in range(-20,21) if 0 < abs(x)+abs(y) <= 20]
for pos in cmat.bfs(st):
    for n in cmat.neigh4(pos):
        if cmat.read(n) in (".", "S", "E"):
            cmat.bfs.enqueue(n)
        elif cmat.read(n) == "#":
            if cmat.read(2*n-pos) in (".", "S", "E"):
                d = cmat.bfs.dist[pos] + from_end[2*n-pos] + 2
                if d < from_end[st]:
                    p1[n] = from_end[st] - d
    for v in t:
        if cmat.read(pos + v) in (".", "E", "S"):
            p2[pos, pos + v] = from_end[st] - (cmat.bfs.dist[pos] + from_end[pos + v] + int(abs(v.real)) + int(abs(v.imag)))

print(sorted(Counter(p1.values()).items()))
print(sorted(Counter(v for v in p2.values() if v >= 50).items()))
print(len({r for r, d in p1.items() if d >= 100}))
print(len({r for r, d in p2.items() if d >= 100}))
