from aoc import mat

flashes = 0
for _ in range(10000):
    inits = []
    for i, row in enumerate(mat):
        for j, c in enumerate(row):
            if c == '9':
                inits.append((i, j))
                row[j] = "*"
            else:
                row[j] = str(int(row[j]) + 1)
    flashes += len(inits)
    for ij in mat.bfs(inits):
        for i, j in mat.neigh8(ij):
            c = mat.read((i, j))
            if not c:
                continue
            if c in "012345678":
                mat[i][j] = str(int(mat[i][j]) + 1)
            elif mat.bfs.enqueue((i, j)):
                flashes += 1
                inits.append((i,j))
    # if _ < 10 or _ % 10 == 0:
    #     print(_, flashes)
    #     print("\n".join("".join(line) for line in mat))
    for i, j in inits:
        mat[i][j] = '0'
    if _ == 100:
        print(flashes)
    if len(inits) == 100:
        print(_ + 1)
        break
