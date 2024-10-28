from aoc import sectionlines, path
import re

themap, (directions,) = sectionlines

if "samp" in path:
    corners = """
    AB
    CD
BAACCD
FGGHHE
    HEED
    GFFB
""".strip(
        "\n"
    ).split(
        "\n"
    )
else:
    corners = """
  GHHD
  FBBA
  FB
  EA
FEEA
GCCD
GC
HD
""".strip(
    "\n"
).split(
    "\n"
)

topleft = next(
    (i, j) for i, line in enumerate(themap) for j, v in enumerate(line) if v != " "
)
area = sum(v != " " for line in themap for v in line)
facesize = int((area / 6) ** 0.5)
RIGHT, DOWN, LEFT, UP = range(4)

portals: dict[tuple[int, int, int], tuple[int, int, int]] = {}
if 0:
    thestarts: dict[int, int] = {}
    for i, line in enumerate(["", *themap, ""], -1):
        thisline: set[int] = set()
        thestart = -1
        for j, column in enumerate(" " + line + " ", -1):
            if column == " ":
                if thestart != -1:
                    # print("Make horizontal portal between", i, thestart, j - 1)
                    portals[LEFT, i, thestart - 1] = (LEFT, i, j - 1)
                    portals[RIGHT, i, j] = (RIGHT, i, thestart)
                    thestart = -1
                continue
            if topleft is None:
                topleft = (i, j)
            if thestart == -1:
                thestart = j
            thisline.add(j)
        for j in thestarts.keys() - thisline:
            # print("Make vertical portal between", j, thestarts[j], i - 1)
            portals[DOWN, i, j] = DOWN, thestarts[j], j
            portals[UP, thestarts[j] - 1, j] = UP, i - 1, j
            del thestarts[j]
        for j in thisline - thestarts.keys():
            thestarts[j] = i
elif 0:
    faces = {
        (i // facesize, j // facesize)
        for i, line in enumerate(themap)
        for j, v in enumerate(line)
        if v != " "
    }
    assert len(faces) == 6
    print(sorted(faces))
    if faces == {(0, 2), (1, 0), (1, 1), (1, 2), (2, 2), (2, 3)}:
        folding = {
            (LEFT, 0, 2): (DOWN, 1, 1),
            (UP, 0, 2): (DOWN, 1, 0),
            (RIGHT, 0, 2): (LEFT, 2, 3),
            (LEFT, 1, 0): (LEFT, 1, 2),
            (UP, 1, 0): (DOWN, 0, 2),
            (DOWN, 1, 0): (UP, 2, 2),
            (UP, 1, 1): (RIGHT, 0, 2),
            (DOWN, 1, 1): (RIGHT, 2, 2),
            (RIGHT, 1, 2): (DOWN, 2, 3),
            (LEFT, 2, 2): (UP, 1, 1),
            (DOWN, 2, 2): (UP, 1, 0),
            (UP, 2, 3): (LEFT, 1, 2),
            (RIGHT, 2, 3): (LEFT, 0, 2),
            (DOWN, 2, 3): ...,
        }
else:
    edges: dict[tuple[str, str], list[tuple[int, int, int, int]]] = {}

    def add_edge(i1: int, j1: int, i2: int, j2: int) -> None:
        v0 = corners[i1][j1]
        v1 = corners[i2][j2]
        (e0a, e0ai, e0aj), (e0b, e0bi, e0bj) = sorted([(v0, i1, j1), (v1, i2, j2)])
        edges.setdefault((e0a, e0b), []).append((e0ai, e0aj, e0bi, e0bj))

    for i in range(0, len(corners), 2):
        for j in range(0, len(corners[i]), 2):
            if corners[i][j] == " ":
                continue
            add_edge(i, j, i, j + 1)
            add_edge(i, j + 1, i + 1, j + 1)
            add_edge(i + 1, j + 1, i + 1, j)
            add_edge(i + 1, j, i, j)
    assert len(edges) == 12
    assert all(len(e) == 2 for e in edges.values())

    def edge_coords_to_dir(ia1: int, ja1: int, ia2: int, ja2: int) -> int:
        if ja1 % 2 == ja2 % 2 == 1:
            return RIGHT
        elif ia1 % 2 == ia2 % 2 == 1:
            return DOWN
        elif ja1 % 2 == ja2 % 2 == 0:
            return LEFT
        elif ia1 % 2 == ia2 % 2 == 0:
            return UP
        else:
            raise Exception((ia1, ja1, ia2, ja2))

    print(edges)

    for (ia1, ja1, ia2, ja2), (ib1, jb1, ib2, jb2) in edges.values():
        dia = ia2 - ia1
        dja = ja2 - ja1
        dib = ib2 - ib1
        djb = jb2 - jb1
        dira = edge_coords_to_dir(ia1, ja1, ia2, ja2)
        dirb = edge_coords_to_dir(ib1, jb1, ib2, jb2)
        print("EDGE", corners[ia1][ja1], corners[ia2][ja2], ia1, dia, ja1, dja, ">v<^"[dira], ib1, dib, jb1, djb, ">v<^"[dirb])
        assert corners[ia1][ja1] == corners[ib1][jb1]
        assert corners[ia2][ja2] == corners[ib2][jb2]
        for i in range(facesize):
            # ia1=0
            # dia=0
            # ja1=4
            # dja=1
            # ib1=2
            # dib=0
            # jb1=1
            # djb=-1
            # facesize=4
            # i=0
            ia = facesize * (ia1 // 2) + (ia1 % 2) * (facesize - 1) + i * dia
            ib = facesize * (ib1 // 2) + (ib1 % 2) * (facesize - 1) + i * dib
            ja = facesize * (ja1 // 2) + (ja1 % 2) * (facesize - 1) + i * dja
            jb = facesize * (jb1 // 2) + (jb1 % 2) * (facesize - 1) + i * djb
            if i % (facesize // 4) == 0:
                print("PORTAL", ia, ja, ">v<^"[dira], ib, jb, ">v<^"[dirb])
            portals[dira, ia + [0, 1, 0, -1][dira], ja + [1, 0, -1, 0][dira]] = ((dirb + 2) % 4, ib, jb)
            portals[dirb, ib + [0, 1, 0, -1][dirb], jb + [1, 0, -1, 0][dirb]] = ((dira + 2) % 4, ia, ja)

facing = RIGHT
assert topleft is not None
i, j = topleft
lastdir = {topleft: facing}
for direction in re.findall(r"\d+|.", directions):
    if direction == "L":
        print("Let's rotate", direction, facing, i, j)
        facing = (facing - 1) % 4
        lastdir[i, j] = facing
    elif direction == "R":
        print("Let's rotate", direction, facing, i, j)
        facing = (facing + 1) % 4
        lastdir[i, j] = facing
    else:
        print("Let's move", direction, facing, i, j)
        for _ in range(int(direction)):
            if facing == RIGHT:
                n = i, j + 1
            elif facing == DOWN:
                n = i + 1, j
            elif facing == LEFT:
                n = i, j - 1
            elif facing == UP:
                n = i - 1, j
            nfacing = facing
            if (facing, *n) in portals:
                print("Take portal at", ">v<^"[facing], n)
                nfacing, ni, nj = portals[facing, n[0], n[1]]
                n = ni, nj
                print("... to", ">v<^"[nfacing], n)
            assert 0 <= n[0] < len(themap)
            assert 0 <= n[1] < len(themap[n[0]])
            assert themap[n[0]][n[1]] != " ", n
            if themap[n[0]][n[1]] == "#":
                break
            i, j = n
            facing = nfacing
            lastdir[i, j] = facing
res = 1000 * (i + 1) + 4 * (j + 1) + facing
print(i, j, facing)
for i in range(len(themap)):
    print(
        "".join(
            ">v<^"[lastdir[i, j]] if (i, j) in lastdir else themap[i][j]
            for j in range(len(themap[i]))
        )
    )
print(res)
