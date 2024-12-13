from aoc import sectionints
import sympy

ii, jj = sympy.symbols("i, j", integer=True, nonnegative=True)
aa, bb = sympy.symbols("a, b", integer=True)

p1 = 0
p2 = 0
for (x1,y1),(x2,y2),(x3,y3) in sectionints:
    possibles = [(3 * i + j, i, j) for i in range(101) for j in range(101) if x1 * i + x2 * j == x3 and y1 * i + y2 * j == y3]
    if possibles:
        cheap = min(possibles)[0]
        p1 += cheap
    x3 += 10000000000000
    y3 += 10000000000000
    soln = sympy.solve((ii * x1 + jj * x2 - x3, ii * y1 + jj * y2 - y3))
    if not soln:
        continue
    i = int(soln[ii])
    j = int(soln[jj])
    # a * x1 - b * x2 == 0
    # a * y1 - b * y2 == 0
    soln = sympy.solve((aa * x1 - bb * x2, aa * y1 - bb * y2))
    p2 += 3 * i + j
    continue

print(p1)
print(p2)
