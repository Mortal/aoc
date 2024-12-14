from aoc import lineints, path, Counter

if "samp" in path:
    w,h=11,7
else:
    w,h=101,103

def positions(time: int) -> list[tuple[int, int]]:
    return [((px + time * vx) % w, (py + time * vy) % h) for px, py, vx, vy in lineints]

p1pos = positions(100)
a = sum(x < w//2 and y < h//2 for x,y in p1pos)
b = sum(x > w//2 and y < h//2 for x,y in p1pos)
c = sum(x < w//2 and y > h//2 for x,y in p1pos)
d = sum(x > w//2 and y > h//2 for x,y in p1pos)
p1 = a*b*c*d

p2 = max(range(w*h), key=lambda i: max(Counter(x for x, y in positions(i)).values()) * max(Counter(y for x, y in positions(i)).values()))
p2pos = set(positions(p2))
for i in range(h):
    print("".join(".@"[(j,i) in p2pos] for j in range(w)))

print(p1)
print(p2)
