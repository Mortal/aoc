from typing import Callable, Iterable

with open("d25.in") as fp:
    inp = fp.read()
if 0:
    inp = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

edgelists: dict[str, dict[str, int]] = {}
for line in inp.strip().splitlines():
    a, bs = line.split(":")
    for b in bs.split():
        edgelists.setdefault(a, {})[b] = 1
        edgelists.setdefault(b, {})[a] = 1


def bfs(start: str, edges: Callable[[str], Iterable[str]]) -> dict[str, str]:
    q = [start]
    src = {start: start}
    i = 0
    while i < len(q):
        s = q[i]
        i += 1
        for e in edges(s):
            if e not in src:
                src[e] = s
                q.append(e)
    return src


def backtrack(start: str, goal: str, src: dict[str, str]) -> list[str]:
    if goal not in src:
        return []
    res = [goal]
    while res[-1] != start:
        res.append(src[res[-1]])
    return res[::-1]


def maxflowmincut(start: str, goal: str) -> tuple[list[str], list[tuple[str, str]]]:
    flow: dict[tuple[str, str], int] = {}

    def residuals(s: str) -> Iterable[tuple[str, int]]:
        for t in edgelists[s]:
            yield t, edgelists[s][t] + flow.get((t, s), 0) - flow.get((s, t), 0)

    def edges(s: str) -> Iterable[str]:
        for t, r in residuals(s):
            if r > 0:
                yield t

    src = {}
    for _ in range(len(edgelists) ** 3):
        src = bfs(start, edges)
        path = backtrack(start, goal, src)
        if not path:
            break
        for a, b in zip(path, path[1:]):
            flow[a, b] = flow.get((a, b), 0) + 1
    else:
        raise Exception("loop")

    maxflow = sum(edgelists[start].values()) - sum(r for t, r in residuals(start))
    mincut = []
    for s in src:
        for t, r in residuals(s):
            if t not in src:
                mincut.append((s, t))
    assert maxflow == len(mincut), (maxflow, mincut)
    return list(src), mincut


nodes = list(edgelists)
for goal in nodes[1:]:
    startnodes, mincut = maxflowmincut(nodes[0], goal)
    print(nodes[0], goal, mincut, len(startnodes) * (len(nodes) - len(startnodes)))
    if len(mincut) == 3:
        break
