with open("d21.in") as fp:
    inp = fp.read()
if 0:
    inp = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
    steps = 6

steps = 26501365

rows = inp.strip().splitlines()
n = len(rows)
m = len(rows[0])
s, = [(0, 0, i, j) for i, row in enumerate(rows) for j, c in enumerate(row) if c == "S"]
bfs = [s]
dists = {s: 0}
i = 0

def neighbors(s: tuple[int, int, int, int]) -> list[tuple[int, int, int, int]]:
    a, b, c, d = s
    return [
        (a + e // n, b + f // m, e % n, f % n)
        for g in (1, -1, 1j, -1j)
        for e in [c + int(g.imag)]
        for f in [d + int(g.real)]
    ]


def read(pos: tuple[int, int, int, int]) -> str:
    a, b, i, j = pos
    assert 0 <= i < n and 0 <= j < m
    if rows[i][j] == "S":
        return "."
    return rows[i][j]

counts = {65+n*131: 1 for n in range(5)}

while i < len(bfs):
    pos = bfs[i]
    # print(pos, dists[pos])
    if dists[pos] > 9 * n:
        break
    i += 1
    for npos in neighbors(pos):
        if read(npos) == "." and npos not in dists:
            dists[npos] = dists[pos] + 1
            for c in counts:
                if dists[npos] % 2 == 0 and dists[npos] <= c:
                    counts[c] += 1
            bfs.append(npos)
print(counts)
exit()

def expecteddist(pos: tuple[int, int, int, int]) -> int:
    a, b, c, d = pos
    e, f, g, h = s
    return int(abs((a * n + c) - (e * n + g))) + int(abs((b * m + d) - (f * m + h)))


nums = "_123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def overdist(pos: tuple[int, int, int, int]) -> int:
    dist = dists.get(pos)
    if dist is None:
        return -1
    e = expecteddist(pos)
    assert 0 <= dist - e < len(nums)
    return int(dist - e)

seen: dict[str, list[tuple[int, int]]] = {}
for a in range(-3, 4):
    for b in range(-3, 4):
        printout = []
        for c, row in enumerate(rows):
            printout.append(list(row))
            for d in range(m):
                o = overdist((a, b, c, d))
                if o < 0:
                    continue
                printout[-1][d] = nums[o]
        printstr = "\n".join("".join(p) for p in printout)
        seen.setdefault(printstr, []).append((a, b))
for printstr, tiles in seen.items():
    print(tiles)
    print(printstr)
    print("================================")


def countdiag(a: int, b: int, steps: int) -> int:
    count = 0
    for c in range(n):
        for d in range(m):
            pos = (a, b, c, d)
            if pos not in dists:
                continue
            dist = dists[pos]
            assert n == m
            assert n % 2 == 1
            # For how many x=0,1,2,... y=0,1,2,... is dist+n*(x+y) <= steps AND dist+n*(x+y) % 2 == steps % 2?
            if dist % 2 == steps % 2:
                # must have x % 2 == y % 2
                # There are two cases: x,y even ; x,y odd.
                # Even case:
                # For how many x=0,2,4,... y=0,2,4,... is dist+n*(x+y) <= steps?
                # Reformulate:
                # For how many x=0,1,2,... y=0,1,2,... is dist+n*(2*(x+y)) <= steps?
                if dist <= steps:
                    # x+y <= (steps - dist) // (2 * n)
                    # Number of solutions to x + y < z is
                    # z + (z-1) + ... + 1 = z*(z+1)//2
                    z = 1 + (steps - dist) // (2 * n)
                    count += z*(z+1)//2
                # Odd case:
                # For how many x=0,1,2,... y=0,1,2,... is dist+n*(2*(x+y+1)) <= steps?
                if dist + 2 * n <= steps:
                    # x+y <= (steps - dist) // (2 * n) - 1
                    z = 1 + (steps - dist) // (2 * n) - 1
                    count += z*(z+1)//2
            else:
                # must have x % 2 != y % 2
                # There are two cases: x even ; y even.
                # x even case:
                # For how many x=0,2,4,... y=1,3,5,... is dist+n*(x+y) <= steps?
                # Reformulate:
                # For how many x=0,1,2,... y=0,1,2,... is dist+n*(2*x+1+2*y) <= steps?
                # y even case is the same:
                # For how many x=0,1,2,... y=0,1,2,... is dist+n*(2*x+2*y+1) <= steps?
                if dist + n <= steps:
                    # dist+n+2*n*(x+y) <= steps
                    # x+y <= (steps - dist - n) // (2 * n)
                    z = 1 + (steps - dist - n) // (2 * n)
                    count += z*(z+1)//2
    return count


def countcard(a: int, b: int, steps: int) -> int:
    count = 0
    for c in range(n):
        for d in range(m):
            pos = (a, b, c, d)
            if pos not in dists:
                continue
            dist = dists[pos]
            k = abs(a) * n + abs(b) * m
            # For how many x=0,1,2,3,4,... is dist+k*x <= steps AND dist+k*x % 2 == steps % 2?
            assert k % 2 == 1, (a, n, b, m, k)
            if dist % 2 == steps % 2:
                # must have x=0,2,4,...
                # reformulate:
                # For how many x=0,1,2,3,4,... is dist+k*(2*x) <= steps?
                if dist > steps:
                    continue
                # x <= (steps - dist) // (2 * k)
                count += 1 + (steps - dist) // (2 * k)
            else:
                # must have x=1,3,5,...
                # reformulate:
                # For how many x=0,1,2,3,4,... is dist+k*(2*x+1) <= steps?
                if dist + k > steps:
                    continue
                # x <= (steps - dist - k) // (2 * k)
                count += 1 + (steps - dist - k) // (2 * k)
    return count


def countcenter(a: int, b: int, steps: int) -> int:
    count = 0
    for c in range(n):
        for d in range(m):
            pos = (a, b, c, d)
            if pos not in dists:
                continue
            if dists[pos] % 2 == steps % 2 and dists[pos] <= steps:
                count += 1
    return count


for steps in (6, 10, 50, 100, 500, 1000, 5000, 26501365):
    a = countdiag(-1, -1, steps)
    b = countcard(-1, 0, steps)
    c = countdiag(-1, 1, steps)
    d = countcard(0, -1, steps)
    e = countcenter(0, 0, steps)
    f = countcard(0, 1, steps)
    g = countdiag(1, -1, steps)
    h = countcard(1, 0, steps)
    i = countdiag(1, 1, steps)
    ans = a+b+c+d+e+f+g+h+i
    print(f"In exactly {steps} steps, he can reach {a}+{b}+{c}+{d}+{e}+{f}+{g}+{h}+{i}={ans} garden plots.")
    assert n < 131 or steps < 26501365 or ans > 454070227768055, ans
