from aoc import mat


p1 = 0
p2 = 0
mat.bfs.multi()
for i in range(len(mat)):
    for j in range(len(mat[0])):
        start = (i, j)
        if not mat.bfs.newsource(start):
            continue
        ch = mat.read(start)
        area = 0
        peri = 0
        sides: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for pos in mat.bfs:
            area += 1
            for n in mat.neigh4(pos):
                if mat.read(n) == ch:
                    mat.bfs.enqueue(n)
                else:
                    a,b=pos
                    c,d=n
                    peri += 1
                    sides.setdefault((a-c,b-d),[]).append(pos)
        p1 += area * peri
        for (a,b), ss in sides.items():
            sideset = set(ss)
            peri2 = 0
            for (c,d) in sorted(ss):
                prev = c-b,d+a
                if prev not in sideset:
                    peri2 += 1
            p2 += area * peri2
print(p1)
print(p2)
