import bisect
from aoc import cmat

UP = -1j
DOWN = 1j
LEFT = -1
RIGHT = 1
CW90 = 1j

start, = cmat.findall("^")
obs = set(cmat.findall("#"))

def sim(o: complex) -> set[complex] | None:
    byrow: dict[int, list[int]] = {}
    bycol: dict[int, list[int]] = {}
    for p in sorted({*cmat.findall("#"), o}, key=lambda c: (c.imag, c.real)):
        byrow.setdefault(int(p.imag), []).append(int(p.real))
        bycol.setdefault(int(p.real), []).append(int(p.imag))
    dir = UP

    def go(pos: complex, dir: complex) -> complex | None:
        if dir == RIGHT or dir == LEFT:
            try:
                myrow = byrow[int(pos.imag)]
            except KeyError:
                return None
            # right or left
            myix = bisect.bisect(myrow, int(pos.real))
            if dir == LEFT:
                # left: subtract one
                myix -= 1
            if 0 <= myix < len(myrow):
                return complex(myrow[myix], pos.imag) - dir
            return None

        try:
            mycol = bycol[int(pos.real)]
        except KeyError:
            return None
        # down or up
        myix = bisect.bisect(mycol, int(pos.imag))
        if dir == UP:
            # up: subtract one
            myix -= 1
        if 0 <= myix < len(mycol):
            return complex(pos.real, mycol[myix]) - dir
        return None

    pos = start
    p2: set[complex] = set()
    dir = UP
    longmoves: list[tuple[complex, complex]] = []
    turns: dict[tuple[complex, complex], int] = {}
    while True:
        if (pos, dir) in turns:
            return None
        turns[pos, dir] = len(turns)
        nextpos = go(pos, dir)
        if nextpos is None:
            if dir == 1j:
                nextpos = complex(pos.real, len(cmat)-1)
            elif dir == -1j:
                nextpos = complex(pos.real, 0)
            elif dir == 1:
                nextpos = complex(len(cmat[0])-1, pos.imag)
            else:
                nextpos = complex(0, pos.imag)
            longmoves.append((pos, nextpos))
            # while pos != nextpos:
            #     if pos + dir not in obs and (go(pos, dir * CW90), dir * CW90 * CW90) in turns:
            #         print(pos + dir, go(pos, dir * CW90))
            #         p2.add(pos + dir)
            #     pos += dir
            pos = nextpos
            break
        longmoves.append((pos, nextpos))
        # while pos != nextpos:
        #     if pos + dir not in obs and (go(pos, dir * CW90), dir * CW90 * CW90) in turns:
        #         print(pos + dir, go(pos, dir * CW90))
        #         p2.add(pos + dir)
        #     pos += dir
        pos = nextpos
        dir = dir * CW90
    return {
        complex(x, y)
        for a, b in longmoves
        for x in range(min(int(a.real), int(b.real)), max(int(a.real), int(b.real))+1)
        for y in range(min(int(a.imag), int(b.imag)), max(int(a.imag), int(b.imag))+1)
    }
p1 = sim(next(iter(obs)))
assert p1 is not None
print(len(p1))
p2 = set()
for o in sorted(p1, key=lambda c: (c.imag, c.real)):
    if sim(o) is None:
        print(o)
        p2.add(o)
print(len(p2))
