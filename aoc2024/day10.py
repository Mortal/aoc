from aoc import mat

starts = mat.findall("0")
score = 0
for s in starts:
    for u in mat.bfs(s):
        for v in mat.neigh4inside(u):
            if mat.read(v) == str(int(mat.read(u)) + 1):
                if mat.bfs.enqueue(v):
                    if mat.read(v) == "9":
                        score += 1
print(score)

counts = {}
for s in starts:
    counts[s] = 1
for i in range(0, 9):
    for u in mat.findall(str(i)):
        for v in mat.neigh4inside(u):
            if mat.read(v) == str(int(mat.read(u)) + 1):
                counts[v] = counts.get(v, 0) + counts.get(u, 0)
# print([(v, counts.get(v, 0)) for v in mat.findall('9')])
print(sum(counts.get(v, 0) for v in mat.findall('9')))
