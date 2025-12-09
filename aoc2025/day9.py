from aoc import lineints

print(
    max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for x1, y1 in lineints
        for x2, y2 in lineints
    )
)
# Coordinate compression
xs, ys = zip(*lineints)
xc = {x: i + 1 for i, x in enumerate(sorted(set(xs)))}
yc = {y: i + 1 for i, y in enumerate(sorted(set(ys)))}
# First, create grid of -1/0/+1 with +1 on +y edges and -1 on -y edges.
grid = [[0] * (1 + len(xc)) for _ in range(1 + len(yc))]
for (x1, y1), (x2, y2) in zip(lineints, lineints[1:] + lineints[:1]):
    if y1 == y2:
        continue
    assert x1 == x2
    # Note: half-open ranges.
    for y in range(yc[y1], yc[y2]):
        grid[y][xc[x1]] -= 1
    for y in range(yc[y2], yc[y1]):
        grid[y][xc[x1]] += 1
# Then apply prefix sum to obtain a 0/1 grid with 0=outside, 1=inside
for y in range(1, 1 + len(yc)):
    for x in range(1, 1 + len(xc)):
        grid[y][x] += grid[y][x - 1]
        assert grid[y][x] in (0, 1)
# Then apply double prefix sum to obtain a grid of areas from 0,0 to x,y
for y in range(1 + len(yc)):
    for x in range(1, 1 + len(xc)):
        grid[y][x] += grid[y][x - 1]
    if y > 0:
        for x in range(1 + len(xc)):
            grid[y][x] += grid[y - 1][x]
print(
    max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for x1, y1 in lineints
        for x2, y2 in lineints
        if grid[yc[max(y1, y2)] - 1][xc[max(x1, x2)] - 1]
        - grid[yc[max(y1, y2)] - 1][xc[min(x1, x2)] - 1]
        - grid[yc[min(y1, y2)] - 1][xc[max(x1, x2)] - 1]
        + grid[yc[min(y1, y2)] - 1][xc[min(x1, x2)] - 1]
        == (yc[max(y1, y2)] - yc[min(y1, y2)]) * (xc[max(x1, x2)] - xc[min(x1, x2)])
    )
)
