with open("d17.in") as fp:
    inp = fp.read()
if 0:
    inp = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
if 0:
    inp = """111111111111
999999999991
999999999991
999999999991
999999999991
"""

rows = [list(map(int, line)) for line in inp.strip().splitlines()]
n = len(rows)
m = len(rows[0])

def go(minturn: int, maxturn: int) -> tuple[int, dict[complex, str]]:
    pq = [[(0+0j, 1+0j, 0), (0+0j, 0+1j, 0)]]
    seen: set[tuple[complex, complex, int]] = set()
    bestsofar = {s: 0 for s in pq[0]}
    src = {s: s for s in pq[0]}

    def read(pos: complex) -> int:
        row = int(pos.imag)
        col = int(pos.real)
        if 0 <= row < len(rows) and 0 <= col < len(rows[row]):
            return rows[row][col]
        return -1

    def backtrace(state: tuple[complex, complex, int]) -> dict[complex, str]:
        bt = [state]
        while src[bt[-1]] != bt[-1]:
            bt.append(src[bt[-1]])
        dirmap = {1+0j: ">", -1+0j: "<", 0+1j: "v", 0-1j: "^"}
        return {pos: dirmap[dir] for pos, dir, count in bt}

    d = 0
    while d < len(pq):
        print(d, len(pq[d]), len(seen))
        for srcstate in pq[d]:
            if srcstate in seen:
                continue
            seen.add(srcstate)
            pos, dir, count = srcstate
            if pos == complex(m - 1, n - 1) and count >= minturn:
                return d, backtrace(srcstate)
            rightdir = complex(-dir.imag, dir.real)
            leftdir = complex(dir.imag, -dir.real)
            nextstates = [(pos + leftdir, leftdir, 1), (pos + rightdir, rightdir, 1)]
            if count < minturn:
                del nextstates[:]
            if count < maxturn:
                nextstates.append((pos + dir, dir, count + 1))
            for state in nextstates:
                pos, dir, count = state
                c = read(pos)
                if c == -1:
                    continue
                dd = d + c
                if state in bestsofar and bestsofar[state] < dd:
                    continue
                bestsofar[state] = dd
                src[state] = srcstate
                while len(pq) <= dd:
                    pq.append([])
                pq[dd].append(state)
        d += 1
    raise

d, bt = go(0, 3)
print("\n".join("".join(bt.get(complex(j, i), str(rows[i][j])) for j in range(m)) for i in range(n)))
print(d)

d, bt = go(4, 10)
print("\n".join("".join(bt.get(complex(j, i), str(rows[i][j])) for j in range(m)) for i in range(n)))
print(d)
