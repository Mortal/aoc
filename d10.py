with open("d10.in") as fp:
    inp = fp.read()
if 0:
    inp = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

rows = inp.strip().splitlines()
start = next((i, row.index("S")) for i, row in enumerate(rows) if "S" in row)
n = len(rows)
m = len(rows[0])

def neighbors(node):
    i, j = node
    if i > 0 and rows[i][j] in "|LJS":
        yield i - 1, j
    if i + 1 < n and rows[i][j] in "|7FS":
        yield i + 1, j
    if j > 0 and rows[i][j] in "-J7S":
        yield i, j - 1
    if j + 1 < m and rows[i][j] in "-LFS":
        yield i, j + 1

bfs = [start]
startneighbors = [n for n in neighbors(start) if start in neighbors(n)]
dist = {start: 0}
parent = {start: start}
branch = {start: start}
i = 0
goal = start, start
branches = start, start
while i < len(bfs):
    node = bfs[i]
    i += 1
    for neighbor in startneighbors if node == start else neighbors(node):
        if neighbor in dist:
            if dist[neighbor] == dist[node] - 1:
                # Where we came from, presumably
                continue
            assert dist[neighbor] == dist[node] + 1
            assert branch[neighbor] != branch[node]
            # We found it!
            goal = neighbor, node
            branches = branch[neighbor], branch[node]
        else:
            dist[neighbor] = dist[node] + 1
            parent[neighbor] = node
            branch[neighbor] = neighbor if node == start else branch[node]
            bfs.append(neighbor)

tour = [goal[1], goal[0]]
while tour[-1] != start:
    tour.append(parent[tour[-1]])
tour.reverse()
assert tour[-1] == goal[1]
while tour[-1] != start:
    tour.append(parent[tour[-1]])
print([dist[n] for n in tour])
assert tour[0] == tour[-1] == start

for i in range(n):
    print("".join("S" if (i,j) == start else "G" if (i, j) == goal[0] else str(dist[i, j] % 10) if branch.get((i, j)) in branches else "." for j in range(m)))
print(max(dist.values()))
assert dist[goal[0]] != 6834, "too low"
print(start, goal[0], dist[goal[0]])

def read(node):
    i, j = node
    if 0 <= i < n and 0 <= j < m:
        return rows[i][j]
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

marks = {}
dfs = []
for a, b, c in zip(tour, tour[1:], tour[2:]):
    neighbors = ccw4(b, a)
    for neighbor in neighbors[:neighbors.index(c)]:
        if neighbor not in dist:
            marks[neighbor] = 1
            dfs.append(neighbor)
    for neighbor in neighbors[neighbors.index(c) + 1 :]:
        if neighbor not in dist:
            marks[neighbor] = 2
            dfs.append(neighbor)

for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))

def allneighbors(node):
    i, j = node
    if i > 0:
        yield i - 1, j
    if i + 1 < n:
        yield i + 1, j
    if j > 0:
        yield i, j - 1
    if j + 1 < m:
        yield i, j + 1

while dfs:
    node = dfs.pop()
    for neighbor in allneighbors(node):
        if neighbor in marks or neighbor in parent:
            continue
        marks[neighbor] = marks[node]
        dfs.append(neighbor)

for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))

count1 = 0
count2 = 0
for i in range(n):
    print("".join(str(marks.get((i, j), ".")) for j in range(m)))
    count1 += sum(marks.get((i, j)) == 1 for j in range(m))
    count2 += sum(marks.get((i, j)) == 2 for j in range(m))
print(count1, count2)
