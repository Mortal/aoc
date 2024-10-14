with open("d23.txt") as fp:
    s = fp.read()
if 0:
    s = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip()
if 0:
    s = """
.....
..##.
..#..
.....
..##.
.....
""".strip()
elves = {
    (i, j)
    for i, line in enumerate(s.splitlines())
    for j, c in enumerate(line)
    if c == "#"
}
north, south, west, east = range(4)
directions = {
    north: (-1, 0, 0, 1),
    east: (0, 1, 1, 0),
    south: (1, 0, 0, 1),
    west: (0, -1, 1, 0),
}
for round in range(100000):
    proposal: dict[tuple[int, int], list[tuple[int, int]]] = {}
    nmoves = 0
    for i, j in elves:
        if sum((i + di, j + dj) in elves for di in (-1, 0, 1) for dj in (-1, 0, 1)) == 1:
            assert (i, j) not in proposal
            # print(i, j, i, j)
            proposal[i, j] = [(i, j)]
            continue
        nmoves += 1
        for d in [(round + d) % 4 for d in range(4)]:
            di, dj, ei, ej = directions[d]
            overlap = elves & {
                (i + di, j + dj),
                (i + di + ei, j + dj + ej),
                (i + di - ei, j + dj - ej),
            }
            if not overlap:
                # print(i, j, i + di, j + dj)
                proposal.setdefault((i + di, j + dj), []).append((i, j))
                break
        else:
            assert (i, j) not in proposal
            # print(i, j, i, j)
            proposal[i, j] = [(i, j)]
    n = len(elves)
    # print(proposal)
    elves = {
        (i, j)
        for (ai, aj), e in proposal.items()
        for i, j in ([(ai, aj)] if len(e) == 1 else e)
    }
    assert len(elves) == n
    if round % 10 == 0 or not nmoves:
        print(round, nmoves)
    if 0:
        for i in range(-2, 11):
            print("".join(".#"[(i, j) in elves] for j in range(-3, 11)))
    if round > 10 and not nmoves:
        break
i_s, j_s = zip(*elves)
mini = min(i_s)
maxi = max(i_s)
minj = min(j_s)
maxj = max(j_s)
print(mini, maxi, minj, maxj, (maxi - mini + 1) * (maxj - minj + 1) - len(elves))
