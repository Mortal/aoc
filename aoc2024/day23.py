from aoc import lines
import networkx as nx

edgesets = {}
edges = set()
hist = []
sets = set()

for line in lines:
    u, v = line.split("-")
    edgesets.setdefault(u, []).append(v)
    edgesets.setdefault(v, []).append(u)
    edges.add((u, v))
    edges.add((v, u))
for u in edgesets:
    if u.startswith("t"):
        hist.append(u)
p1 = 0
for u in hist:
    for v in edgesets[u]:
        for w in set(edgesets[v]) & set(edgesets[u]):
            if len({u,v,w}) == 3:
                sets.add(frozenset({u,v,w}))
print(len(sets))
g = nx.Graph()
g.add_nodes_from(edgesets.keys())
g.add_edges_from(edges)
cliques = list(nx.find_cliques(g))
largest = max(cliques, key=len)
print(','.join(sorted(largest)))
