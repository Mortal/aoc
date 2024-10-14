with open("d16.in") as fp:
    inp = fp.read()
if 0:
    inp = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
rows = inp.splitlines()

def go(initpos: complex, initdir: complex) -> int:
    dfs = [(initpos, initdir)]
    seen = set(dfs)

    def read(pos: complex) -> str:
        row = int(pos.imag)
        col = int(pos.real)
        if 0 <= row < len(rows) and 0 <= col < len(rows[row]):
            return rows[row][col]
        return "x"

    while dfs:
        pos, dir = dfs.pop()
        n: list[tuple[complex, complex]] | None = None
        match read(pos):
            case "\\":
                n = [(pos, complex(dir.imag, dir.real))]
            case "/":
                n = [(pos, complex(-dir.imag, -dir.real))]
            case "-":
                if dir.imag:
                    n = [(pos, 1+0j), (pos, -1+0j)]
                else:
                    n = [(pos, dir)]
            case "|":
                if dir.real:
                    n = [(pos, 0+1j), (pos, 0-1j)]
                else:
                    n = [(pos, dir)]
            case ".":
                n = [(pos, dir)]
            case "x":
                n = []
        assert n is not None, read(pos)
        for pos, dir in n:
            pos = pos + dir
            if (pos, dir) not in seen:
                seen.add((pos, dir))
                dfs.append((pos, dir))
    seenpos = {pos for pos, dir in seen if read(pos) != "x"}
    return len(seenpos)

print(go(0+0j, 1+0j))
allrows = range(0, len(rows))
allcols = range(0, len(rows[0]))
print(
    max(
        go(complex(c, r), d)
        for d, cs, rs in (
            (1 + 0j, [0], allrows),
            (0 + 1j, allcols, [0]),
            (-1 + 0j, [len(rows[0]) - 1], allrows),
            (0 - 1j, allcols, [len(rows) - 1]),
        )
        for c in cs
        for r in rs
    )
)
