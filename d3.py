import string

with open("d3.in") as fp:
    lines = fp.read().split()
if 0:
    lines = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""".split()

def read(ij):
    i, j = ij
    if 0 <= i < len(lines) and 0 <= j < len(lines[i]):
        return lines[i][j]
    return ''

def num(ij):
    i, j = ij
    while j > 0 and lines[i][j-1] in string.digits:
        j -= 1
    return i, j

def readnum(ij):
    i, j = ij
    v = int(lines[i][j])
    while j + 1 < len(lines[i]) and lines[i][j + 1] in string.digits:
        j += 1
        v *= 10
        v += int(lines[i][j])
    return v

def neighbors(ij):
    i, j = ij
    return [(i + a, j + b) for a in (-1, 0, 1) for b in (-1, 0, 1) if not a == b == 0]

gears = []
nums = set()
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == "*":
            myneigh = set()
            for n in neighbors((i, j)):
                if read(n) not in string.digits:
                    continue
                myneigh.add(num(n))
            if len(myneigh) == 2:
                a, b = sorted(myneigh)
                gears.append(((i, j), num(a), num(b)))
        if lines[i][j] not in string.digits:
            continue
        if num((i, j)) in nums:
            continue
        for n in neighbors((i, j)):
            if read(n) not in ["", ".", *string.digits]:
                print(num((i, j)), readnum(num((i, j))), repr(n), repr(read(n)))
                nums.add(num((i, j)))
                break
print([readnum(ij) for ij in nums])
print(sum(readnum(ij) for ij in nums))
print(gears)
print(sum(readnum(g1) * readnum(g2) for g, g1, g2 in gears))
