with open("d24.txt") as fp:
    s = fp.read().strip()

if 0:
    s = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".strip()

if 0:
    s = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".strip()

themap = s.splitlines()
startposition = (0, 1)
endposition = (len(themap) - 1, len(themap[-1]) - 2)
rows = len(themap)
cols = len(themap[0])

def wall(i: int, j: int, time: int) -> bool:
    if not (0 <= i < rows and 0 <= j < cols) or themap[i][j] == "#":
        return True
    down = (i - time - 1) % (rows - 2) + 1
    up = (i + time - 1) % (rows - 2) + 1
    right = (j - time - 1) % (cols - 2) + 1
    left = (j + time - 1) % (cols - 2) + 1
    return themap[down][j] == "v" or themap[up][j] == "^" or themap[i][left] == "<" or themap[i][right] == ">"

def wallname(i: int, j: int, time: int) -> str:
    if not (0 <= i < rows and 0 <= j < cols) or themap[i][j] == "#":
        return "#"
    down = (i - time - 1) % (rows - 2) + 1
    up = (i + time - 1) % (rows - 2) + 1
    right = (j - time - 1) % (cols - 2) + 1
    left = (j + time - 1) % (cols - 2) + 1
    idown = themap[down][j] == "v"
    iup = themap[up][j] == "^"
    ileft = themap[i][left] == "<"
    iright = themap[i][right] == ">"
    isum = idown + iup + ileft + iright
    if isum == 0:
        return "."
    if isum > 1:
        return str(isum)
    if idown:
        return "v"
    if iup:
        return "^"
    if ileft:
        return "<"
    assert iright
    return ">"

visited: list[list[list[bool]]] = [[[False] * cols for _ in range(rows)] for _ in range((rows - 2) * (cols - 2))]
movements = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]

time = 564
time_ = time % len(visited)
reachable: list[tuple[int, int]] = [startposition]
goal = endposition
neighbors = reachable[0:0]
visited[time_][reachable[0][0]][reachable[0][1]] = True
while reachable:
    print(time, len(reachable))
    if 0:
        print(reachable)
        for i in range(rows):
            print("".join(wallname(i, j, time) for j in range(cols)))
    time += 1
    time_ = time % len(visited)
    for i, j in reachable:
        if (i, j) == goal:
            print(time - 1)
            raise SystemExit
        for di, dj in movements:
            ni = i + di
            nj = j + dj
            if not wall(ni, nj, time):
                if not visited[time_][ni][nj]:
                    visited[time_][ni][nj] = True
                    neighbors.append((ni, nj))
    neighbors, reachable = reachable, neighbors
    del neighbors[:]
