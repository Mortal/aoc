from aoc import lineints, path, Counter

if "samp" in path:
    w,h=11,7
else:
    w,h=101,103

for i in (100 % (w*h), 7916):
    q = {(a,b):0 for a in (True, False) for b in (True, False)}
    p = {}
    for px, py, vx, vy in lineints:
        px += i * vx
        px %= w
        py += i * vy
        py %= h
        p[px, py] = 1
        if px == w // 2 or py == h // 2:
            continue

        q[px < w // 2, py < h // 2] += 1
    a,b,c,d = q.values()
    if i == 100 % (w*h):
        print("p1")
        print(a*b*c*d)
    print(i, a,b,c,d, "<"*(max([sum((i, j) in p for j in range(w)) for i in range(h)])), ">"* (max([sum((i, j) in p for i in range(h)) for j in range(w)])))
    for i in range(h):
        print("".join(".@"[(j,i) in p] for j in range(w)))
