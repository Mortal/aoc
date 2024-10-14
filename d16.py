from aoc import cmat
n, m = cmat.shape

def go(initpos: complex, initdir: complex) -> int:
    dfs = [(initpos, initdir)]
    seen = set(dfs)

    while dfs:
        pos, dir = dfs.pop()
        n: list[tuple[complex, complex]] | None = None
        match cmat.read(pos) or "x":
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
        assert n is not None, cmat.read(pos)
        for pos, dir in n:
            pos = pos + dir
            if (pos, dir) not in seen:
                seen.add((pos, dir))
                dfs.append((pos, dir))
    seenpos = {pos for pos, dir in seen if (cmat.read(pos) or "x") != "x"}
    return len(seenpos)

print(go(0+0j, 1+0j))
allrows = range(0, n)
allcols = range(0, m)
print(
    max(
        go(complex(c, r), d)
        for d, cs, rs in (
            (1 + 0j, [0], allrows),
            (0 + 1j, allcols, [0]),
            (-1 + 0j, [m - 1], allrows),
            (0 - 1j, allcols, [n - 1]),
        )
        for c in cs
        for r in rs
    )
)
