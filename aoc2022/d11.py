import math
import re


pattern = r'Monkey (\d+):\s*Starting items: (.*)\s*Operation: new = (.*)\s*Test: divisible by (\d+)\s*If true: throw to monkey (\d+)\s*If false: throw to monkey (\d+)'


count = []
items = []
op = []
divisor = []
true = []
false = []
with open("d11.txt") as fp:
    inp = fp.read()
lcm = 1
for i, mo in enumerate(re.finditer(pattern, inp)):
    monkey = int(mo.group(1))
    assert monkey == i
    count.append(0)
    items.append(list(map(int, mo.group(2).split(", "))))
    op.append(eval("lambda old: " + mo.group(3)))
    divisor.append(int(mo.group(4)))
    true.append(int(mo.group(5)))
    false.append(int(mo.group(6)))
    lcm = lcm * divisor[-1] // math.gcd(lcm, divisor[-1])
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
