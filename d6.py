with open("d6.in") as fp:
    inp = fp.read()
if 0:
    inp = """Time:      7  15   30
Distance:  9  40  200
"""

pairs = list(zip(*(line.split() for line in inp.strip().splitlines())))[1:]
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
