from aoc import lines, inp

pairs = list(zip(*(line.split() for line in lines)))[1:]
prod = 1
for xstr, ystr in pairs:
    x = int(xstr)
    y = int(ystr)
    ways = sum(i * (x - i) > y for i in range(x))
    prod *= ways
    print(x, y, ways)
print(prod)
l1, l2 = inp.replace(" ", "").splitlines()
x = int(l1.split(":")[1])
y = int(l2.split(":")[1])
print(x, y)
for i in range(x):
    if i * (x - i) <= y:
        continue
    print(x, y, i, i * (x - i))
    break
ways = sum(i * (x - i) > y for i in range(x))
print(x, y, ways)
