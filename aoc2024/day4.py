from aoc import cmat

p1 = 0
for s in cmat.findall("X"):
    for n in cmat.neigh8(s):
        if cmat.read(n) == "M":
            for o in cmat.neigh8(n):
                if cmat.read(o) == "A" and o - n == n - s:
                    for p in cmat.neigh8(o):
                        if cmat.read(p) == "S" and p - o == o - n:
                            p1 += 1

print(p1)

p2 = 0
for s in cmat.findall("A"):
    a,b,c,d = [cmat.read(a) for a in cmat.neigh4diag(s)]
    
    if all(ch in ("M", "S") for ch in (a,b,c,d)):
        if a != d and b != c:
            p2 += 1
print(p2)
