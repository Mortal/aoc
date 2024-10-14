import re

edgelists: dict[str, list[str]] = {}
flowrates: dict[str, int] = {}

with open("day16.txt") as fp:
    for line in fp:
        name, flowrate, *edges = re.findall(r"[A-Z]{2}|\d+", line)
        edgelists[name] = edges
        flowrates[name] = int(flowrate)

dp1: list[dict[frozenset[str], dict[str, int]]] = [{} for _ in range(31)]
dp1[0][frozenset()] = {"AA": 0}
for minute in range(1, len(dp1)):
    for openset in dp1[minute - 1]:
        flowsum = sum(flowrates[n] for n in openset)
        for name, acc in dp1[minute - 1][openset].items():
            if flowrates.get(name) and name not in openset:
                n = dp1[minute].setdefault(openset | {name}, {})
                v = acc + flowsum
                n[name] = max(n.get(name, v), v)
            for neighbor in edgelists[name]:
                n = dp1[minute].setdefault(openset, {})
                v = acc + flowsum
                n[neighbor] = max(n.get(neighbor, v), v)
dp2: list[dict[frozenset[str], int]] = [{} for _ in range(len(dp1))]
for minute in range(len(dp1)):
    for openset in dp1[minute]:
        dp2[minute][openset] = max(dp1[minute][openset].values())
print(max(dp2[30].values()))
print(max(dp2[26][s1] + dp2[26][s2] for s1 in dp2[26] for s2 in dp2[26] if not (s1 & s2)))
