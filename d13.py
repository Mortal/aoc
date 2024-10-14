with open("d13.in") as fp:
    inp = fp.read()
if 0:
    inp = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

def isreflection(rows: list[str], i: int) -> bool:
    smudge = False
    for j in range(min(len(rows) - i, i)):
        if rows[i + j] != rows[i - 1 - j]:
            if not smudge and sum(c != d for c, d in zip(rows[i + j], rows[i - 1 - j])) == 1:
                smudge = True
                continue
            return False
    return smudge

s = 0
for maze in inp.strip().split("\n\n"):
    rows = maze.splitlines()
    cols = list("".join(col) for col in zip(*rows))
    #print("\n".join(cols))
    #print("")
    ns = [i for i in range(1, len(rows)) if isreflection(rows, i)]
    ms = [i for i in range(1, len(cols)) if isreflection(cols, i)]
    print(ns, ms)
    assert {len(ns), len(ms)} == {0, 1}
    s += sum(100 * n for n in ns) + sum(ms)
print(s)
