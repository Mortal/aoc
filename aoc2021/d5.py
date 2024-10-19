from aoc import linetoks, path
from collections import Counter

count = Counter[tuple[int,int]]()

for x1,y1,x2,y2 in linetoks:
    assert isinstance(x1, int), (x1,y1,x2,y2)
    assert isinstance(x2, int), (x1,y1,x2,y2)
    assert isinstance(y1, int), (x1,y1,x2,y2)
    assert isinstance(y2, int), (x1,y1,x2,y2)
    for x in range(min(x1,x2),max(x1,x2)+1):
        if x1 == x2 or y1 == y2:
            ya = min(y1,y2)
            yb = max(y1,y2)+1
            ys = range(ya,yb)
        else:
            if (x1 >= x2) == (y1 >= y2):
                ya = y1 + (x - x1)
            else:
                ya = y1 - (x - x1)
            ys = range(ya, ya + 1)
        for y in ys:
            count[x,y] += 1
    if "test" not in path:
        print(x1,y1,x2,y2)
        print("\n".join("".join(str(count.get((x,y)) or ".") for x in range(0, 10)) for y in range(0, 10)))
if "test" not in path:
    print(count.keys())
print(sum(v>1 for v in count.values()))
