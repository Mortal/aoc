with open("d18.in") as fp:
    inp = fp.read()
if 0:
    inp = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
if 0:
    inp = """R 1 (#000000)
D 1 (#000000)
L 1 (#000000)
U 1 (#000000)
"""

pos = 0+0j
cubes = {pos}
volume = 0
circumference = 0
directions = dict(R=1+0j, D=0+1j, L=-1+0j, U=0-1j)
for line in inp.strip().splitlines():
    direction_str, length_str, color_str = line.split()
    length = int(length_str)
    length = int(color_str[2:-2], 16)
    direction = directions[direction_str]
    direction = list(directions.values())[int(color_str[-2])]
    circumference += 2 * length
    volume -= int(direction.real) * length * int(pos.imag)
    if 1:
        pos += direction * length
    else:
        for _ in range(length):
            pos += direction
            cubes.add(pos)
assert pos == 0+0j
print(circumference)
assert circumference % 4 == 0, divmod(circumference, 4)
print(volume + circumference // 4 + 1)

exit()
minx = min(c.real for c in cubes) - 1
maxx = max(c.real for c in cubes) + 1
miny = min(c.imag for c in cubes) - 1
maxy = max(c.imag for c in cubes) + 1
dfs = [complex(minx, miny)]
visited = set(dfs)
while dfs:
    pos = dfs.pop()
    for n in directions.values():
        p = pos + n
        if minx <= p.real <= maxx and miny <= p.imag <= maxy:
            if p not in visited and p not in cubes:
                visited.add(p)
                dfs.append(p)
print(len(visited), len(cubes))
print(int((maxx - minx + 1) * (maxy - miny + 1)) - len(visited))
