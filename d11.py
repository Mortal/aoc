with open("d11.in") as fp:
    inp = fp.read()
if 0:
    inp = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
lines = inp.strip().splitlines()
n = len(lines)
m = len(lines[0])
galaxies = [
    (i, j)
    for i, line in enumerate(lines)
    for j, c in enumerate(line)
    if c == "#"
]
rowset = {i for i, j in galaxies}
colset = {j for i, j in galaxies}
rowtorow = [0]
extra = 1000000 - 1
for i in range(n):
    if i not in rowset:
        rowtorow[-1] += extra
    rowtorow.append(rowtorow[-1] + 1)
coltocol = [0]
for i in range(m):
    if i not in colset:
        coltocol[-1] += extra
    coltocol.append(coltocol[-1] + 1)
galaxies = [(rowtorow[i], coltocol[j]) for i, j in galaxies]
print(sum(abs(i1 - i2) + abs(j1 - j2) for i, (i1, j1) in enumerate(galaxies) for i2, j2 in galaxies[i:]))
