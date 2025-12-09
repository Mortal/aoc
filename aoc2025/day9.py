from aoc import lineints

p1, px1, py1, px2, py2 = max((abs(x1-x2+1)*abs(y1-y2+1),x1,y1,x2,y2) for x1, y1 in lineints for x2, y2 in lineints)
print(p1)

xs, ys = zip(*lineints)
xc = {x: i for i, x in enumerate(sorted(set(xs)))}
yc = {y: i for i, y in enumerate(sorted(set(ys)))}
xgrid = [[0] * len(xc) for _ in range(len(yc))]
ygrid = [[0] * len(xc) for _ in range(len(yc))]
for (x1, y1), (x2, y2) in zip(lineints, lineints[1:] + lineints[:1]):
    assert x1 == x2 or y1 == y2
    for x in range(xc[x1], xc[x2]):
        ygrid[yc[y1]][x] += 1
    for x in range(xc[x2], xc[x1]):
        ygrid[yc[y1]][x] -= 1
    for y in range(yc[y1], yc[y2]):
        xgrid[y][xc[x1]] -= 1
    for y in range(yc[y2], yc[y1]):
        xgrid[y][xc[x1]] += 1
for y in range(1, len(yc)):
    for x in range(1, len(xc)):
        xgrid[y][x] += xgrid[y][x-1]
        ygrid[y][x] += ygrid[y-1][x]
        assert xgrid[y][x] in (0, 1), (x, y, xgrid[y][x])
        assert ygrid[y][x] in (0, 1), (x, y, ygrid[y][x])
        assert xgrid[y][x] == ygrid[y][x]

print(max((abs(x1-x2+1)*abs(y1-y2+1)) for x1, y1 in lineints for x2, y2 in lineints if all(xgrid[y][x] == 1 for y in range(yc[min(y1, y2)], yc[max(y1, y2)]) for x in range(xc[min(x1, x2)], xc[max(x1, x2)]))))

#for x, y in lineints:
#    grid[yc[y]][xc[x]] = '#'
#grid[yc[py1]][xc[px1]] = '1'
#grid[yc[py2]][xc[px2]] = '2'
#for row in grid:
#    print(''.join(row))
#print((max(xs)-min(xs)+1)*(max(ys)-min(ys)+1))
#print((1+len(xc))*(1+len(yc)))
