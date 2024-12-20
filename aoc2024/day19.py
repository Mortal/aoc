import re
from aoc import linetoks, path

patterns = linetoks[0]
trie = {}
for p in patterns:
    n = trie
    for c in p:
        n = n.setdefault(c, {})
    n[""] = 1
pattern = re.compile('(?:{})*'.format("|".join(patterns)))
p1 = 0
p2 = 0
for line in linetoks[1:]:
    for target in line:
        if pattern.fullmatch(target):
            p1 += 1
        nodes = [(1, trie)]
        new = 0
        for c in target:
            nodes2 = []
            new = 0
            for count, node in nodes:
                n = node.get(c)
                if n is None:
                    continue
                if "" in n:
                    new += count
                nodes2.append((count, n))
            if new:
                nodes2.append((new, trie))
            nodes = nodes2
        p2 += new

print(p1)
print(p2)
