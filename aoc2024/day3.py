from aoc import inp
import re

p1 = 0
p2 = 0
ac = 1
for mo in re.finditer(r'(?:do\(\)|don\'t\(\)|mul\(([0-9]+),([0-9]+)\))', inp):
    if mo.group(0) == 'do()':
        ac = 1
    elif mo.group(0) == 'don\'t()':
        ac = 0
    else:
        a, b = map(int, mo.groups())
        p1 += a*b
        p2 += a*b*ac
print(p1)
print(p2)
