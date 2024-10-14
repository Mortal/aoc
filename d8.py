with open("d8.in") as fp:
    inp = fp.read()
if 0:
    inp = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

dirs, lines = inp.strip().split("\n\n")
insns = {line[:3]: (line[7:10], line[12:15]) for line in lines.strip().splitlines()}
print(insns)

n = len(dirs)

edges = {
    (s, i): (insns[s][dirs[i] == "R"], (i + 1) % len(dirs))
    for s in insns
    for i in range(len(dirs))
}
print(len(dirs))
print(len(edges))
allperiods = []
for s in insns:
    if not s.endswith("A"):
        continue
    seen = set()
    path = [(s, 0)]
    ends = []
    while path[-1] not in seen:
        if path[-1][0].endswith("Z"):
            ends.append((path[-1][0], len(path)-1))
        seen.add(path[-1])
        path.append(edges[path[-1]])
    period = len(path) - 1 - path.index(path[-1])
    print(s, path.index(path[-1]), len(path), period, path[-1])
    print(ends)
    (s, end), = ends
    allperiods.append(period)
    assert end == period
print(allperiods)
import math
print(math.lcm(*allperiods))
