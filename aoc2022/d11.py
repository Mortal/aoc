from aoc import sectionlines, sectionints, gcd


count: list[int] = []
items: list[list[int]] = []
op: list = []
divisor: list[int] = []
true: list[int] = []
false: list[int] = []
with open("d11.txt") as fp:
    inp = fp.read()
lcm = 1
for lines, lineints in zip(sectionlines, sectionints):
    monkey, = lineints[0]
    count.append(0)
    items.append(lineints[1])
    op.append(eval("lambda old: " + lines[2].split("=")[1]))
    divisor.append(lineints[3][0])
    true.append(lineints[4][0])
    false.append(lineints[5][0])
    lcm = lcm * divisor[-1] // gcd(lcm, divisor[-1])
for round in range(10000):
    for i in range(len(items)):
        my_items = items[i][:]
        del items[i][:]
        for item in my_items:
            count[i] += 1
            item = op[i](item)
            # item //= 3
            item %= lcm
            if item % divisor[i] == 0:
                items[true[i]].append(item)
            else:
                items[false[i]].append(item)
    # print(f"\nAfter round {round+1}, the monkeys are holding items with these worry levels:")
    # for i in range(len(items)):
    #     print(f"Monkey {i}: {', '.join(map(str, items[i]))}")
    print(f"\n== After round {round+1} ==")
    for i in range(len(items)):
        print(f"Monkey {i} inspected items {count[i]} times.")

c1, c2 = sorted(count)[-2:]
print(c1, c2)
print(c1 * c2)
