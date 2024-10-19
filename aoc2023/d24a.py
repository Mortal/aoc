with open("d24.in") as fp:
    inp = fp.read()
    xmin = 200000000000000
    xmax = 400000000000000
if 0:
    xmin = 7
    xmax = 27
    inp = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
import sympy
x, y = sympy.symbols("x y")
soln = None
lines = inp.strip().splitlines()

def constraints(i, j):
    px1,py1,pz1,vx1,vy1,vz1 = map(int, lines[i].replace(",", " ").replace("@"," ").split())
    px2,py2,pz2,vx2,vy2,vz2 = map(int, lines[i].replace(",", " ").replace("@"," ").split())
    assert vx1 != 0
    assert vy1 != 0
    assert vz1 != 0
    assert vx2 != 0
    assert vy2 != 0
    assert vz2 != 0
    return [
        (py1 * vx1 - (x - px1) * vy1) / vx1 - (py2 * vx2 - (x - px2) * vy2) / vx2
    ]

for i in range(len(lines)):
    for j in range(i+1, len(lines)):
        print(sympy.solve(constraints(i, j), (x, y)))
