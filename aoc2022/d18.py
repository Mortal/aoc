with open("d18.txt") as fp:
    points = {eval(line) for line in fp}
print(len(points ^ {(x+1, y, z) for x, y, z in points})
      + len(points ^ {(x, y+1, z) for x, y, z in points})
      + len(points ^ {(x, y, z+1) for x, y, z in points}))
xs, ys, zs = zip(*points)
x1 = min(xs) -1
x2 = max(xs) + 1
y1 = min(ys) -1
y2 = max(ys) + 1
z1 = min(zs) -1
z2 = max(zs) + 1
v = {(x1, y1, z1)} | points
dfs = [(x1, y1, z1)]
neighbors = [(dx, dy, dz) for dx in (-1,0,1) for dy in (-1,0,1) for dz in (-1,0,1) if abs(dx)+abs(dy)+abs(dz)==1]
while dfs:
    x, y, z = dfs.pop()
    for dx, dy, dz in neighbors:
        if (x + dx, y + dy, z + dz) not in v and x1 <= x + dx <= x2 and y1 <= y + dy <= y2 and z1 <= z + dz <= z2:
            v.add((x + dx, y + dy, z + dz))
            dfs.append((x + dx, y + dy, z + dz))
v -= points
print(len(v ^ {(x+1, y, z) for x, y, z in v})
      + len(v ^ {(x, y+1, z) for x, y, z in v})
      + len(v ^ {(x, y, z+1) for x, y, z in v}) - 2 * (x2 - x1 + 1) * (y2 - y1 + 1 + z2 - z1 + 1) - 2 * (y2 - y1 + 1) * (z2 - z1 + 1))
