from aoc import mat,path

n,m= mat.shape
for i in range(n):
    for j in range(4*m):
        mat[i].append(str(((int(mat[i][-m]) + 1) % 10) or 1))
for i in range(4*n):
    mat.append([str(((int(c) + 1) % 10) or 1) for c in mat[-n]])
print(mat.shape, n,m)
if "samp" in path:
    print("\n".join("".join(row) for row in mat))

start = 0,0

queue = [[start]]

def enq(d, st):
    queue.extend([[] for _ in range(d + 2 - len(queue))])
    queue[d].append(st)

d = 0
dist = {}
n,m= mat.shape
end = n-1,m-1
while end not in dist:
    for st in queue[d]:
        if st in dist:
            continue
        dist[st] = d
        for i,j in mat.neigh4inside(st):
            enq(d + int(mat[i][j]), (i,j))
    d += 1
print(dist[end])
