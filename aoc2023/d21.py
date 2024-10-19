from aoc import path, lines, ComplexStringMatrix

steps = 26501365 if "test" in path else 6
rep = 5
steps *= rep
cmat = ComplexStringMatrix(rep * [rep * line for line in lines])
n, m = cmat.shape
ss = cmat.findall("S")
s = ss[len(ss)//2]
bfs = [s]
dists = {s: 0}
i = 0
dirs = [1,-1,1j,-1j]

while i < len(bfs):
    pos = bfs[i]
    i += 1
    for d in dirs:
        if cmat.read(pos + d) in (".", "S") and pos + d not in dists:
            dists[pos + d] = dists[pos] + 1
            bfs.append(pos + d)

def expecteddist(i: int, j: int) -> int:
    return int(abs(j - s.real) + abs(i - s.imag))


nums = "_123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def overdist(i: int, j: int) -> int:
    dist = dists.get(complex(j, i))
    if dist is None:
        return -1
    e = expecteddist(i, j)
    assert 0 <= dist - e < len(nums)
    return int(dist - e)

count = 0
cases = {(b, d): 0 for b in range(n // rep) for d in range(n // rep)}
for i, row in enumerate(cmat):
    printout = ["."] * m
    printout = list(row)
    for j in range(m):
        o = overdist(i, j)
        a, b = divmod(i, n // rep)
        c, d = divmod(j, m // rep)
        if a < 2:
            a = 1 - a
        elif a > 2:
            a = 7 - a
        if c < 2:
            c = 1 - c
        elif c > 2:
            c = 7 - c
        assert o == overdist(a * (n // rep) + b, c * (m // rep) + d), (i, j, a * (n // rep) + b, c * (m // rep) + d, o, overdist(a * (n // rep) + b, c * (m // rep) + d))
        assert o == overdist(i, c * (m // rep) + d)
        assert o == overdist(a * (n // rep) + b, j)
        if o < 0:
            continue
        if complex(j, i) == s:
            printout[j] = "S"
        elif o == 0:
            printout[j] = "_"
        else:
            printout[j] = nums[o]
        dist = dists[complex(j, i)]
        if {a, c} == {2}:
            cases[b, d] += 1
            # Center.
            if dist is not None and dist <= steps and dist % 2 == steps % 2:
                count += 1
        elif {a, c} in ({1, 2}, {2, 3}):
            cases[b, d] += 1
            # Cardinal. How many solutions x >= 0 are there to the equation
            # dist + nn * x <= steps AND (dist + nn * x) % 2 == steps % 2
            assert n == m
            nn = n // rep
            assert nn % 2 == 1
            if dist % 2 == steps % 2:
                # x must be even
                # dist + nn * 2 * x <= steps
                # nn * 2 * x <= steps - dist
                # x <= (steps - dist) / (2 * nn)
                # x <= floor((steps - dist) / (2 * nn))
                # x <= (steps - dist) // (2 * nn)
                count += 1 + (steps - dist) // (2 * nn)
            else:
                # x must be odd
                # dist + nn * (2 * x + 1) <= steps
                # nn * (2 * x + 1) <= steps - dist
                # nn * 2 * x <= steps - dist - nn
                # x <= (steps - dist - nn) // (2 * nn)
                count += 1 + (steps - dist - nn) // (2 * nn)
        elif {a, c} in ({1}, {1, 3}, {3}):
            cases[b, d] += 1
            # Diagonal. How many solutions x >= 0, y >= 0 are there to the equation
            # dist + nn * x + nn * y <= steps AND (dist + nn * x + nn * y) % 2 == steps % 2
            assert n == m
            nn = n // rep
            assert nn % 2 == 1
            if dist % 2 == steps % 2:
                # x % 2 == y % 2.
                # First let's count where x and y are even.
                # dist + nn * 2 * x + nn * 2 * y <= steps
                # 2 * nn * (x + y) <= steps - dist
                # x + y < 1 + (steps - dist) // (2 * nn)
                # Number of solutions to x + y < z is
                # z + (z-1) + ... + 1 = z*(z+1)//2
                z = 1 + (steps - dist) // (2 * nn)
                count += z*(z+1)//2
                # Now let's count where x and y are odd.
                # dist + nn * 2 * (x + 1) + nn * 2 * (y + 1) <= steps
                # 2 * nn * (x + y + 2) <= steps - dist
                # x + y + 2 < 1 + (steps - dist) // (2 * nn)
                # x + y < -1 + (steps - dist) // (2 * nn)
                z = -1 + (steps - dist) // (2 * nn)
                count += z*(z+1)//2
            else:
                # x % 2 != y % 2.
                # First let's count x odd, y even.
                # dist + nn * 2 * (x + 1) + nn * 2 * y <= steps
                # 2 * nn * (x + y + 1) <= steps - dist
                # x + y + 1 < 1 + (steps - dist) // (2 * nn)
                # x + y < (steps - dist) // (2 * nn)
                z = (steps - dist) // (2 * nn)
                count += z*(z+1)//2
                # x even, y odd is symmetrical.
                count += z*(z+1)//2
    print("".join(printout))
print([dists[complex(j, i)] == (abs(j - s.real) + abs(i - s.imag)) for j in range(m) for i in [0]]) 
print([dists[complex(j, i)] == (abs(j - s.real) + abs(i - s.imag)) for j in range(m) for i in [n-1]]) 
print([dists[complex(j, i)] == (abs(j - s.real) + abs(i - s.imag)) for j in [0] for i in range(n)])
print([dists[complex(j, i)] == (abs(j - s.real) + abs(i - s.imag)) for j in [m-1] for i in range(n)])
print(set(cases.values()))
assert count < 15131079815481851, count
print(count) 
