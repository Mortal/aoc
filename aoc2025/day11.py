from aoc import linetoks
import functools

edgelists = {}
for u, *vs in linetoks:
    edgelists[u.strip(":")] = vs

@functools.cache
def p1count(node: str) -> int:
    if node == "out":
        return 1
    return sum(p1count(v) for v in edgelists[node])
print(p1count("you"))
