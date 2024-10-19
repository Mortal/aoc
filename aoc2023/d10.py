from aoc import mat

start, = mat.findall("S")
n, m = mat.shape

def neighbors(node):
    i, j = node
    if i > 0 and mat[i][j] in "|LJS":
        yield i - 1, j
    if i + 1 < n and mat[i][j] in "|7FS":
        yield i + 1, j
    if j > 0 and mat[i][j] in "-J7S":
        yield i, j - 1
    if j + 1 < m and mat[i][j] in "-LFS":
        yield i, j + 1

startneighbors = [n for n in neighbors(start) if start in neighbors(n)]
goal = start, start
branches = start, start
branch = {start: start}

for node in mat.bfs(start):
    for neighbor in startneighbors if node == start else neighbors(node):
        if mat.bfs.enqueue(neighbor):
            branch[neighbor] = neighbor if node == start else branch[node]
        else:
            if mat.bfs.dist[neighbor] == mat.bfs.dist[node] - 1:
                # Where we came from, presumably
                continue
            assert mat.bfs.dist[neighbor] == mat.bfs.dist[node] + 1
            assert branch[neighbor] != branch[node]
            print("We found it!")
            goal = neighbor, node
            branches = branch[neighbor], branch[node]

assert goal != (start, start)
tour = [goal[1], goal[0]]
while tour[-1] != start:
    tour.append(mat.bfs.parent[tour[-1]])
tour.reverse()
assert tour[-1] == goal[1]
while tour[-1] != start:
    tour.append(mat.bfs.parent[tour[-1]])
print([mat.bfs.dist[n] for n in tour])
assert tour[0] == tour[-1] == start

for i in range(n):
    print("".join("S" if (i,j) == start else "G" if (i, j) == goal[0] else str(mat.bfs.dist[i, j] % 10) if branch.get((i, j)) in branches else "." for j in range(m)))
print(max(mat.bfs.dist.values()))
assert mat.bfs.dist[goal[0]] != 6834, "too low"
print(start, goal[0], mat.bfs.dist[goal[0]])

def read(node):
    i, j = node
    if 0 <= i < n and 0 <= j < m:
        return mat[i][j]
    return "."

def ccw(center, neighbor):
    i, j = center
    a, b = neighbor
    return i + b - j, j + i - a

def ccw4(center, neighbor):
    a = ccw(center, neighbor)
    b = ccw(center, a)
    c = ccw(center, b)
    assert ccw(center, c) == neighbor
    assert len({neighbor,a,b,c,center}) == 5
    return a, b, c

marks: dict[tuple[int, int], int] = {}
inits = []
for a, b, c in zip(tour, tour[1:], tour[2:]):
    neighs = ccw4(b, a)
    for neighbor in neighs[:neighs.index(c)]:
        if neighbor not in mat.bfs.dist:
            marks[neighbor] = 1
            inits.append(neighbor)
    for neighbor in neighs[neighs.index(c) + 1 :]:
        if neighbor not in mat.bfs.dist:
            marks[neighbor] = 2
            inits.append(neighbor)

for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))

seen = mat.bfs.parent
for node in mat.bfs(inits):
    for neighbor in mat.neigh4inside(node):
        if neighbor in seen:
            continue
        marks[neighbor] = marks[node]
        mat.bfs.enqueue(neighbor)

for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))

count1 = 0
count2 = 0
for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))
    count1 += sum(marks.get((i, j)) == 1 for j in range(m))
    count2 += sum(marks.get((i, j)) == 2 for j in range(m))
print(count1, count2)
