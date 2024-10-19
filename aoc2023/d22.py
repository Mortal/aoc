from aoc import lines
xs: list[range] = []
ys: list[range] = []
z1: list[int] = []
z2: list[int] = []
bricks: dict[tuple[int, int], list[int]] = {}

for i, line in enumerate(lines):
    p,q = line.split("~")
    a,b,c = map(int, p.split(","))
    x,y,z = map(int, q.split(","))
    dims = {a-x,b-y,c-z}
    assert dims == {0} or len(dims) == 2 and 0 in dims, (line, dims)
    xs.append(range(min(a,x), max(a,x)+1))
    ys.append(range(min(b,y), max(b,y)+1))
    z1.append(min(c,z))
    z2.append(max(c,z)+1)
    for x in xs[-1]:
        for y in ys[-1]:
            bricks.setdefault((x, y), []).append(i)


def gap(i: int) -> int:
    return min([z1[i] - 1, *(z1[i] - z2[k] for k in below[i])])


n = len(xs)

below: dict[int, set[int]] = {i: set() for i in range(n)}
above: dict[int, set[int]] = {i: set() for i in range(n)}

for xy in bricks:
    bricks[xy].sort(key=lambda i: z1[i])
    for i, j in zip(bricks[xy], bricks[xy][1:]):
        above[i].add(j)
        below[j].add(i)

dfs = list(range(n))
settled = set()
while dfs:
    i = dfs.pop()
    if i in settled:
        continue
    if all(n in settled for n in below[i]):
        g = gap(i)
        if g:
            z1[i] -= g
            z2[i] -= g
        print(i, "falls", g, "to", z1[i], z2[i])
        settled.add(i)
    else:
        dfs.append(i)
        dfs += below[i]
        print(i, below[i])

below2: dict[int, set[int]] = {i: set() for i in range(n)}
above2: dict[int, set[int]] = {i: set() for i in range(n)}

for xy in bricks:
    bricks[xy].sort(key=lambda i: z1[i])
    for i, j in zip(bricks[xy], bricks[xy][1:]):
        if z2[i] == z1[j]:
            above2[i].add(j)
            below2[j].add(i)

ans = 0
ans2 = 0
for i in range(n):
    wouldfall = sorted(j for j in above2[i] if len(below2[j]) == 1)
    wouldnotfall = sorted(j for j in above2[i] if len(below2[j]) > 1)
    if not wouldfall:
        ans += 1
    dfs = [*wouldfall]
    seen = {*wouldfall}
    while dfs:
        j = dfs.pop()
        for k in above2[j]:
            if set(below2[k]) <= seen:
                seen.add(k)
                dfs.append(k)
    ans2 += len(seen)
    print(i, wouldfall, wouldnotfall, sorted(seen))

# ans = sum(all(len(below2[j]) > 1 for j in above2[i]) for i in range(n))
# assert ans < 1173, ans
# assert ans == 517
print(ans)
# ans2 = sum(sum(len(below2[j]) == 1 for j in above2[i]) for i in range(n))
assert ans2 > 1978, ans2
print(ans2)
