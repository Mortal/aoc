import operator
from aoc import sectionlines, path
# import sympy

vals = {}
# valss = {}
for line in sectionlines[0]:
    var, valstr = line.split(": ")
    vals[var] = int(valstr)
    # valss[var] = sympy.Symbol(var)
xs = []
ys = []
zs = []
ops = {}
for line in sectionlines[1]:
    a, op, b, _, c = line.split()
    ops[c] = min(a, b), op, max(a, b)
    if c.startswith("z"):
        xs.append(c.replace("z", "x"))
        ys.append(c.replace("z", "y"))
        zs.append(c)

def visit(var) -> int:
    if var in vals:
        return vals[var]
    a, op, b = ops[var]
    f = getattr(operator, "i" + op.lower())
    vals[var] = f(visit(a), visit(b))
    return vals[var]

p1 = sum(visit(z) << i for i, z in enumerate(sorted(zs)))
print(p1)
if "samp" in path:
    exit()

# subs = []
# 
# def visit2(var):
#     if var in valss:
#         return valss[var]
#     a, op, b = ops[var]
#     if 0 and var.startswith("z"):
#         i = int(var[1:])
#         if i == 1:
#             x0, y0, x1, y1, cc = sympy.symbols(f"x{i-1:02d} y{i-1:02d} x{i:02d} y{i:02d} cc{i:02d}")
#             subs.append((x0 & y0 & (x1 ^ y1), cc))
#         if i > 1:
#             x0, y0, x1, y1, cc = sympy.symbols(f"x{i-1:02d} y{i-1:02d} x{i:02d} y{i:02d} cc{i:02d}")
#             subs.append((x0 & y0 & (x1 ^ y1), cc))
#     vals[var] = op(visit2(a), visit2(b)).subs(subs)
#     if var.startswith("z"):
#         subs.append((vals[var], sympy.Symbol(var)))
#     return vals[var]


# z[i] = x[i] ^ y[i] ^ c[i-1]
# c[i] = (x[i] & y[i]) | ((x[i] ^ y[i]) & c[i-1])

opsrev = {v: k for k, v in ops.items()}
assert len(opsrev) == len(ops)
xs.sort()
ys.sort()
zs.sort()
c = ""
cc = ""
swaps = []
for i in range(len(zs) - 1):
    xo = opsrev[xs[i], "XOR", ys[i]]
    an = opsrev[xs[i], "AND", ys[i]]
    if not c:
        c = an
    else:
        pos = []
        for (a, op, b), out in opsrev.items():
            if op == "AND":
                if a == xo:
                    pos.append((c, b, out))
                elif b == xo:
                    pos.append((c, a, out))
                elif a == c:
                    pos.append((xo, b, out))
                elif b == c:
                    pos.append((xo, a, out))
        try:
            cc = opsrev[min(xo, c), "AND", max(xo, c)]
        except KeyError:
            (s1, s2, gt), = pos
            sub = {s1: s2, s2: s1}
            swaps.append(s1)
            swaps.append(s2)
            print(xo, c, ops[gt], s1, s2, gt)
            c = sub.get(c, c)
            xo = sub.get(xo, xo)
            an = sub.get(an, an)
            ops = {sub.get(out, out): (a, op, b) for out, (a, op, b) in ops.items()}
            opsrev = {v: k for k, v in ops.items()}
            cc = opsrev[min(xo, c), "AND", max(xo, c)]
        pos = []
        for (a, op, b), out in opsrev.items():
            if op == "OR":
                if a == cc:
                    pos.append((an, b, out))
                elif b == cc:
                    pos.append((an, a, out))
                elif a == an:
                    pos.append((cc, b, out))
                elif b == an:
                    pos.append((cc, a, out))
        try:
            c = opsrev[min(cc, an), "OR", max(cc, an)]
        except KeyError:
            (s1, s2, gt), = pos
            sub = {s1: s2, s2: s1}
            swaps.append(s1)
            swaps.append(s2)
            print(cc, an, ops[gt], s1, s2, gt)
            cc = sub.get(cc, cc)
            an = sub.get(an, an)
            ops = {sub.get(out, out): (a, op, b) for out, (a, op, b) in ops.items()}
            opsrev = {v: k for k, v in ops.items()}
            c = opsrev[min(cc, an), "OR", max(cc, an)]
    print(i, xo, an, c, cc)
print(",".join(sorted(swaps)))
