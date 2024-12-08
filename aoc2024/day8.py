import math
from aoc import cmat

import string


locs = set()
locs2 = set()
for ch in string.digits + string.ascii_letters:
    nodes = cmat.findall(ch)
    for i, a in enumerate(nodes):
        for j, b in enumerate(nodes[:i]):
            aa = 2*a-b
            bb = 2*b-a
            if 0 <= aa.real < len(cmat[0]) and 0 <= aa.imag < len(cmat):
                locs.add(aa)
            if 0 <= bb.real < len(cmat[0]) and 0 <= bb.imag < len(cmat):
                locs.add(bb)
            c = a-b
            d = math.gcd(abs(int(c.real)), abs(int(c.imag)))
            c = complex(c.real / d, c.imag / d)
            for i in range(-max(len(cmat), len(cmat[0])), max(len(cmat), len(cmat[0]))):
                aa = a+i*c
                bb = b+i*c
                if 0 <= aa.real < len(cmat[0]) and 0 <= aa.imag < len(cmat):
                    locs2.add(aa)
                if 0 <= bb.real < len(cmat[0]) and 0 <= bb.imag < len(cmat):
                    locs2.add(bb)
print(len(locs))
print(len(locs2))
