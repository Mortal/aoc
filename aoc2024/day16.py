from aoc import cmat

startpos, = cmat.findall("S")
start = (startpos, 1+0j)
q = [[(start, start)]]
prev = {}

def enqueue(n, d):
    if n in prev:
        return
    q.extend([[] for _ in range ((d + 1 - len(q)))])
    q[d].append(((pos, dir), n))

dist = 0
done = 0
while dist < len(q) and not done:
    for (fpos, fdir), (pos, dir) in q[dist]:
        if (pos, dir) in prev:
            if prev[pos, dir][0][0] == dist:
                prev[pos, dir].append((dist, fpos, fdir))
            # print(pos, dir, dist, prev[pos, dir][0][0])
            continue
        prev[pos, dir] = [(dist, fpos, fdir)]
        if cmat.read(pos) == "E":
            print(dist)
            done = 1
            break
        enqueue((pos, dir * 1j), dist + 1000)
        enqueue((pos, dir * -1j), dist + 1000)
        if cmat.read(pos + dir) != "#":
            enqueue((pos + dir, dir), dist + 1)
    dist += 1
dfs = [(pos, dir)]
onbest = {(pos, dir)}
while dfs:
    pos, dir = dfs.pop()
    for _, p, d in prev[pos, dir]:
        if (p, d) not in onbest:
            onbest.add((p, d))
            dfs.append((p, d))
b = {pos for pos, dir in onbest}
for row in range(len(cmat)):
    print("".join("O" if complex(col, row) in b else cmat[row][col] for col in range(len(cmat[row]))))
print(len(b))
