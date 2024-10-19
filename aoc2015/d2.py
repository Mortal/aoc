from aoc import lines
tot = 0
totline = 0
for line in lines:
    a, b, c = map(int, line.split("x"))
    d, e, f = sorted((a*b, b*c, c*a))
    g = 3 * d + 2 * e + 2 * f
    tot += g
    h, i, j = sorted((a+b, b+c, c+a))
    length = 2 * h + a * b * c
    totline += length
    print(line, g, length)
print(tot)
print(totline)
