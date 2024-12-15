from aoc import inp, mat, path

mapstr, dirs = inp.split("\n\n")

boxes = set(mat.findall("O"))
walls = set(mat.findall("#"))
(i, j), = mat.findall("@")

for it, d in enumerate(dirs):
    if d == "^":
        dfs = [(i, j)]
        moveboxes = []
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii - 1, jj) in boxes:
                dfs.append((ii - 1, jj))
                moveboxes.append((ii - 1, jj))
            elif (ii - 1, jj) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii - 1, jj))
        i -= 1
    if d == "<":
        dfs = [(i, j)]
        moveboxes = []
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii, jj - 1) in boxes:
                dfs.append((ii, jj - 1))
                moveboxes.append((ii, jj - 1))
            elif (ii, jj - 1) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii, jj - 1))
        j -= 1
    if d == "v":
        dfs = [(i, j)]
        moveboxes = []
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii + 1, jj) in boxes:
                dfs.append((ii + 1, jj))
                moveboxes.append((ii + 1, jj))
            elif (ii + 1, jj) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii + 1, jj))
        i += 1
    if d == ">":
        dfs = [(i, j)]
        moveboxes = []
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii, jj + 1) in boxes:
                dfs.append((ii, jj + 1))
                moveboxes.append((ii, jj + 1))
            elif (ii, jj + 1) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii, jj + 1))
        j += 1
    # break
print(sum((100 * i + j) for i, j in boxes))


boxes = {(i, 2 * j) for i, j in (mat.findall("O"))}
walls = {x for i, j in mat.findall("#") for x in ((i, 2 * j), (i, 2 * j + 1))}
(i, j), = mat.findall("@")
j *= 2

if "test" not in path:
    rows = mapstr.splitlines()
    print(d, i, j)
    for ii in range(len(rows)):
        print("".join("#" if (ii, jj) in walls else "[" if (ii, jj) in boxes else "]" if (ii, jj - 1) in boxes else "@" if (ii, jj) == (i, j) else "." for jj in range(2 * len(rows[0]))))

for it, d in enumerate(dirs):
    # if "test" not in path:
    #     rows = mapstr.splitlines()
    #     print(d, i, j)
    #     for ii in range(len(rows)):
    #         print("".join("#" if (ii, jj) in walls else "[" if (ii, jj) in boxes else "]" if (ii, jj - 1) in boxes else "@" if (ii, jj) == (i, j) else "." for jj in range(2 * len(rows[0]))))
    # rows = mapstr.splitlines()
    # print(d, i, j)
    # for ii in range(len(rows)):
    #     print("".join("#" if (ii, jj) in walls else "O" if (ii, jj) in boxes else "@" if (ii, jj) == (i, j) else "." for jj in range(len(rows))))
    if d == "^":
        dfs = [(i, j)]
        moveboxes = set()
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii - 1, jj) in boxes:
                if (ii - 1, jj) in moveboxes:
                    continue
                moveboxes.add((ii - 1, jj))
                dfs.append((ii - 1, jj))
                dfs.append((ii - 1, jj + 1))
            elif (ii - 1, jj - 1) in boxes:
                if (ii - 1, jj - 1) in moveboxes:
                    continue
                moveboxes.add((ii - 1, jj - 1))
                dfs.append((ii - 1, jj - 1))
                dfs.append((ii - 1, jj))
            elif (ii - 1, jj) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii - 1, jj))
        i -= 1
    if d == "<":
        dfs = [(i, j)]
        moveboxes = set()
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii, jj - 1) in boxes:
                if (ii, jj - 1) in moveboxes:
                    continue
                moveboxes.add((ii, jj - 1))
                dfs.append((ii, jj - 1))
            elif (ii, jj - 2) in boxes:
                if (ii, jj - 2) in moveboxes:
                    continue
                moveboxes.add((ii, jj - 2))
                dfs.append((ii, jj - 2))
            elif (ii, jj - 1) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii, jj - 1))
        j -= 1
    if d == "v":
        dfs = [(i, j)]
        moveboxes = set()
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii + 1, jj) in boxes:
                if (ii + 1, jj) in moveboxes:
                    continue
                moveboxes.add((ii + 1, jj))
                dfs.append((ii + 1, jj))
                dfs.append((ii + 1, jj + 1))
            elif (ii + 1, jj - 1) in boxes:
                if (ii + 1, jj - 1) in moveboxes:
                    continue
                moveboxes.add((ii + 1, jj - 1))
                dfs.append((ii + 1, jj - 1))
                dfs.append((ii + 1, jj))
            elif (ii + 1, jj) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii + 1, jj))
        i += 1
    if d == ">":
        dfs = [(i, j)]
        moveboxes = set()
        foundwall = False
        while dfs:
            ii, jj = dfs.pop()
            if (ii, jj + 1) in boxes:
                if (ii, jj + 1) in moveboxes:
                    continue
                moveboxes.add((ii, jj + 1))
                dfs.append((ii, jj + 2))
            elif (ii, jj + 0) in boxes:
                if (ii, jj + 0) in moveboxes:
                    continue
                moveboxes.add((ii, jj + 0))
                dfs.append((ii, jj + 1))
            elif (ii, jj + 1) in walls:
                foundwall = True
                break
        if foundwall:
            continue
        for ii, jj in moveboxes:
            boxes.remove((ii, jj))
        for ii, jj in moveboxes:
            boxes.add((ii, jj + 1))
        j += 1
    # break
print(sum((100 * i + j) for i, j in boxes))
# if "test" not in path:
#     rows = mapstr.splitlines()
#     print(d, i, j)
#     for ii in range(len(rows)):
#         print("".join("#" if (ii, jj) in walls else "[" if (ii, jj) in boxes else "]" if (ii, jj - 1) in boxes else "@" if (ii, jj) == (i, j) else "." for jj in range(2 * len(rows[0]))))


