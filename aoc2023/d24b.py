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
syms = px_,py_,pz_,vx_,vy_,vz_=sympy.symbols("px py pz vx vy vz")
# thesum = sympy.Symbol("thesum")
soln = None
lines = inp.strip().splitlines()

def constraints(i):
    line = lines[i]
    px,py,pz,vx,vy,vz = map(int, line.replace(",", " ").replace("@"," ").split())
    assert vx != 0
    assert vy != 0
    assert vz != 0
    t = sympy.Symbol(f"t{i}")
    return [
        (px_ - px) + t * (vx_ - vx),
        (py_ - py) + t * (vy_ - vy),
        (pz_ - pz) + t * (vz_ - vz),
    ]

soln, = sympy.solve([c for i in range(3) for c in constraints(i)])
print(soln[px_]+soln[py_]+soln[pz_])
exit()
print(soln)
for i in range(len(lines)):
    print(sympy.solve([c.subs(soln) for c in constraints(i)]))
print(soln[px_]+soln[py_]+soln[pz_])
