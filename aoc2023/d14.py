from aoc import mat
n, m = mat.shape

place = {}
for j in range(m):
    count = 0
    for i in range(n)[::-1]:
        if mat[i][j] == "#" and count:
            place[i + 1, j] = count
            count = 0
        elif mat[i][j] == "O":
            count += 1
    if count:
        place[0, j] = count
newrows = [list("." * m) for _ in range(n)]
load = 0
for j in range(m):
    count = place.get((0, j), 0)
    for i in range(n):
        if (i, j) in place:
            count = place[i, j]
        if count:
            newrows[i][j] = "O"
            count -= 1
            load += n - i
        if mat[i][j] == "#":
            newrows[i][j] = "#"
print("\n".join("".join(row) for row in newrows))
print(load)

def main() -> None:
    rowss = [list(row) for row in mat]
    init = "\n".join("".join(row) for row in rowss)
    ocount = sum(c == "O" for row in rowss for c in row)
    assert ocount, ocount
    import time
    t = time.time()
    totit = 1000
    testhash = 0
    stopafter = -1

    for it in range(totit):

        c2 = sum(c == "O" for row in rowss for c in row)
        assert ocount == c2, (it, ocount, c2)
        # NORTH
        place = {}
        for j in range(m):
            count = 0
            for i in range(n)[::-1]:
                if rowss[i][j] == "#" and count:
                    place[i + 1, j] = count
                    count = 0
                elif rowss[i][j] == "O":
                    count += 1
                    rowss[i][j] = "."
            if count:
                place[0, j] = count
        load = 0
        for j in range(m):
            count = 0
            for i in range(n):
                if (i, j) in place:
                    count = place[i, j]
                if count:
                    assert rowss[i][j] == ".", (i, j)
                    rowss[i][j] = "O"
                    count -= 1
                    load += n - i

        # WEST
        place = {}
        for i in range(n):
            count = 0
            for j in range(m)[::-1]:
                if rowss[i][j] == "#" and count:
                    place[i, j + 1] = count
                    count = 0
                elif rowss[i][j] == "O":
                    count += 1
                    rowss[i][j] = "."
            if count:
                place[i, 0] = count
        load = 0
        for i in range(n):
            count = 0
            for j in range(m):
                if (i, j) in place:
                    count = place[i, j]
                if count:
                    assert rowss[i][j] == ".", (i, j)
                    rowss[i][j] = "O"
                    count -= 1
                    load += n - i

        # SOUTH
        place = {}
        for j in range(m):
            count = 0
            for i in range(n):
                if rowss[i][j] == "#" and count:
                    place[i - 1, j] = count
                    count = 0
                elif rowss[i][j] == "O":
                    count += 1
                    rowss[i][j] = "."
            if count:
                place[n-1, j] = count
        load = 0
        for j in range(m):
            count = 0
            for i in range(n)[::-1]:
                if (i, j) in place:
                    count = place[i, j]
                if count:
                    assert rowss[i][j] == ".", (i, j, mat[i][j], count)
                    rowss[i][j] = "O"
                    count -= 1
                    load += n - i

        # EAST
        place = {}
        for i in range(n):
            count = 0
            for j in range(m):
                if rowss[i][j] == "#" and count:
                    place[i, j - 1] = count
                    count = 0
                elif rowss[i][j] == "O":
                    count += 1
                    rowss[i][j] = "."
            if count:
                place[i, m-1] = count
        load = 0
        for i in range(n):
            count = 0
            for j in range(m)[::-1]:
                if (i, j) in place:
                    count = place[i, j]
                if count:
                    rowss[i][j] = "O"
                    count -= 1
                    load += n - i

        out = "\n".join("".join(row) for row in rowss)
        if it and it % 1000 == 0:
            t2 = time.time()
            print(it, (t2 - t), (totit - it) * (t2 - t) / it, hash(out))
        if out == init or it < 3 or hash(out) == testhash or it == stopafter:
            print(it+1)
            print(out)
            print(load)
        if it == stopafter:
            break
        if stopafter == -1 and testhash == hash(out):
            cyclelen = it - 10000
            stopafter = it + 1 + (totit - it - 2) % cyclelen
            print("stopafter", stopafter, cyclelen)
        if it == 10000:
            testhash = hash(out)


main()
