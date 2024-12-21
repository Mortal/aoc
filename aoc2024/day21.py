from aoc import lines, Counter

keypad = {ch: complex(j, i) for i, line in enumerate(
    ("789", "456", "123", " 0A"))
    for j, ch in enumerate(line)}

dirpad = {ch: complex(j, i) for i, line in enumerate(
    (" ^A", "<v>"))
    for j, ch in enumerate(line)}


def looksee(line: str, pad: dict[str, complex]) -> str:
    # ^ > 7 9
    # < ^ 7 9
    # < v 4 8
    # v > 4 8
    pos = pad["A"]
    blank = pad[" "]
    dirs = []
    for ch in line:
        dest = pad[ch]
        d = dest - pos
        # <v^>
        if d.real < 0 and blank != complex(dest.real, pos.imag):
            dirs.append(int(-d.real) * "<")
        if d.imag > 0 and blank != complex(pos.real, dest.imag):
            dirs.append(int(d.imag) * "v")
        if d.imag < 0 and blank != complex(pos.real, dest.imag):
            dirs.append(int(-d.imag) * "^")
        if d.real > 0:
            dirs.append(int(d.real) * ">")
        if d.imag < 0 and blank == complex(pos.real, dest.imag):
            dirs.append(int(-d.imag) * "^")
        if d.real < 0 and blank == complex(dest.real, pos.imag):
            dirs.append(int(-d.real) * "<")
        if d.imag > 0 and blank == complex(pos.real, dest.imag):
            dirs.append(int(d.imag) * "v")
        dirs.append("A")
        pos = dest
    return "".join(dirs)


edges = {}
for ch1 in "^A<v>":
    for ch2 in "^A<v>":
        dirs1, dirs2, _ = looksee(ch1 + ch2, dirpad).split("A")
        edgeto = "A" + dirs2 + "A"
        edges[ch1 + ch2] = Counter(
            a + b
            for a, b in zip(edgeto, edgeto[1:])
        )
# print(edges)


def looksee2(line: Counter[str]) -> Counter[str]:
    res = Counter[str]()
    for k, count in line.items():
        for kk, cc in edges[k].items():
            res[kk] += count * cc
    return res


p1 = 0
p2 = 0
for line in lines:
    dirs1 = looksee(line, keypad)
    dirs2 = looksee(dirs1, dirpad)
    dirs3 = looksee(dirs2, dirpad)
    print(line, len(dirs3), dirs1, dirs2, dirs3)
    p1 += (int(line[:-1]) * len(dirs3))

    dirs = "A" + looksee(line, keypad)
    dd = Counter(
        a + b
        for a, b in zip(dirs, dirs[1:])
    )
    for it in range(25):
        if it == 2:
            assert sum(dd.values()) == len(dirs3)
            # p1 += (int(line[:-1]) * sum(dd.values()))
        dd = looksee2(dd)
    p2 += (int(line[:-1]) * sum(dd.values()))
print(p1)
print(p2)
