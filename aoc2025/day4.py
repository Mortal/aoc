from aoc import mat

p1 = 0
check = set()
for k in mat.findall("@"):
    if sum(mat.read(n) == "@" for n in mat.neigh8(k)) < 4:
        check.add(k)
        p1 += 1
p2 = p1
assert mat.read((0, 0)) == "."
removed = check
while True:
    to_check = set(n for k in check for n in mat.neigh8(k) if mat.read(n) == "@") - removed
    print(p2, len(to_check))
    check = set()
    for k in to_check:
        if sum(mat.read(n) == "@" and n not in removed for n in mat.neigh8(k)) < 4:
            check.add(k)
            p2 += 1
    if not check:
        break
    removed |= check
print(p1)
print(p2)
