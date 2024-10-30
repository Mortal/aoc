from aoc import lines

def explode(a, depth=0):
    if isinstance(a, int):
        return None
    if depth == 3 and isinstance(a[0], list):
        b = a[0]
        a[0] = 0
    else:
        b = explode(a[0], depth+1)
    if b:
        if b[1]:
            if isinstance(a[1], int):
                a[1] += b[1]
            else:
                addleft(a[1], b[1])
        return b[0], 0
    if depth == 3 and isinstance(a[1], list):
        b = a[1]
        a[1] = 0
    else:
        b = explode(a[1], depth+1)
    if b:
        if b[0]:
            if isinstance(a[0], int):
                a[0] += b[0]
            else:
                addright(a[0], b[0])
        return 0, b[1]
    if depth == 4:
        raise

def split(a):
    if isinstance(a, int):
        return False
    if isinstance(a[0], int) and a[0] >= 10:
        a[0] = [a[0] // 2, a[0] - a[0] // 2]
        return True
    elif split(a[0]):
        return True
    elif isinstance(a[1], int) and a[1] >= 10:
        a[1] = [a[1] // 2, a[1] - a[1] // 2]
        return True
    else:
        return split(a[1])

def addleft(a, b):
    if isinstance(a[0], int):
        a[0] += b
    else:
        addleft(a[0], b)

def addright(a, b):
    if isinstance(a[1], int):
        a[1] += b
    else:
        addright(a[1], b)

def reduce(a):
    while explode(a) or split(a):
        pass #print(".", a)
    return a

a = None
for line in lines:
    b = eval(line)
    print(">", b)
    if a is None:
        a = reduce(b)
    else:
        a = reduce([a, b])
    print("=", a)

def magnitude(a):
    if isinstance(a, int):
        return a
    return 3 * magnitude(a[0]) + 2 * magnitude(a[1])
print(a)
print(magnitude(a))

print(max(magnitude(reduce([eval(a),eval(b)]))

for i, a in enumerate(lines)
    for b in lines[i+1:]))


