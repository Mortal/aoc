rocks_strs = """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".strip().split("\n\n")
rocks = [[(i, j) for i, line in enumerate(reversed(rock.splitlines())) for j, c in enumerate(line) if c == "#"] for rock in rocks_strs]
print(rocks)


def simulate(dirstring: str):
    field: list[list[int]] = []
    time = 0
    rockindex = 0

    def sim(steps: int) -> tuple[int, int, int]:
        nonlocal time, rockindex

        for _ in range(steps):
            rock = rocks[rockindex % len(rocks)]
            rockindex += 1
            rockwidth = max(j for i, j in rock) + 1
            x = 2
            for _ in range(3):
                d = dirstring[time % len(dirstring)]
                time += 1
                if d == "<" and x > 0:
                    x -= 1
                elif d == ">" and x + rockwidth < 7:
                    x += 1
            y = len(field)
            while True:
                d = dirstring[time % len(dirstring)]
                time += 1
                if d == "<" and x > 0 and not any(y + i < len(field) and field[y + i][x + j - 1] for i, j in rock):
                    x -= 1
                elif d == ">" and x + rockwidth < 7 and not any(y + i < len(field) and field[y + i][x + j + 1] for i, j in rock):
                    x += 1
                if y > 0 and not any(y + i - 1 < len(field) and field[y + i - 1][x + j] for i, j in rock):
                    y -= 1
                else:
                    break
            for i, j in rock:
                while len(field) <= i + y:
                    field.append([0] * 7)
                assert not field[y + i][x + j]
                field[y + i][x + j] = rockindex
                assert field[y + i][x + j]
        return time, rockindex, len(field)

    return sim


def go(dirstring: str) -> int:
    print(*simulate(dirstring)(2022))
    sim = simulate(dirstring)
    d = len(dirstring) * len(rocks)
    t = r = f = 0
    while t < d:
        t, r, f = sim(1)
    t1, r1, f1 = t, r, f
    while t < 2 * d:
        t, r, f = sim(1)
    t2, r2, f2 = t, r, f
    while t < 3 * d:
        t, r, f = sim(1)
    t3, r3, f3 = t, r, f
    assert r2 - r1 == r3 - r2
    assert t2 - t1 == t3 - t2
    assert f2 - f1 == f3 - f2
    extrarounds = (1000000000000 - r3) // (r3 - r2)
    extrarocks = (1000000000000 - r3) % (r3 - r2)
    t, r, f = sim(extrarocks)
    print(r)
    print(f3 + extrarounds * (f3 - f2) + f - f3)
    return 0


print(go(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"))
with open("day17.txt") as fp:
    print(go(fp.read().strip()))
