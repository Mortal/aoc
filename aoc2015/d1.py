from aoc import inp
print(inp.count("(") - inp.count(")"))
f = 0
n = 0
for c in inp:
    if c == "(":
        f += 1
        n += 1
    elif c == ")":
        f -= 1
        n += 1
    if f == -1:
        print(n)
        break
