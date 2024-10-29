from aoc import lines
edges: dict[str, list[str]] = {}
for line in lines:
    a, b = line.split("-")
    edges.setdefault(a, []).append(b)
    edges.setdefault(b, []).append(a)
print(sum(len(v) for v in edges.values()))
# edgeset: set[tuple[str,str]] = set()
# for k in edges:
#     if k == k.upper():
#         for a in edges[k]:
#             for b in edges[k]:
#                 if a < b:
#                     edgeset.add((a, b))
#     else:
#         for a in edges[k]:
#             if a < k:
#                 edgeset.add((a, k))
#             else:
#                 edgeset.add((k, a))
# edges = {}
# for a, b in edgeset:
#     edges.setdefault(a, []).append(b)
#     edges.setdefault(b, []).append(a)
# print(sum(len(v) for v in edges.values()))
bit = {k: 2 ** i for i, k in enumerate(edges)}
mask = {bit[k]: 0 if k == k.upper() else bit[k] for k in edges}
bitedges = {bit[k]: [bit[v] for v in vs] for k,vs in edges.items()}
thestart = bit["start"]
theend = bit["end"]

def visit(k: int, seen: int, re: int = 1) -> int:
    r = 0
    for g in bitedges[k]:
        if g & seen:
            if re and g != thestart:
                r += 1 if g == theend else visit(g, seen | mask[g], 0)
            continue
        r += 1 if g == theend else visit(g, seen | mask[g], re)
    return r

print(visit(bit["start"], bit["start"]))
