score = 0
with open("aoc2022d2.txt") as fp:
    for line in fp:
        r, s = line.split()
        score += dict(
            AX=3 + 0,
            BX=1 + 0,
            CX=2 + 0,
            AY=1 + 3,
            BY=2 + 3,
            CY=3 + 3,
            AZ=2 + 6,
            BZ=3 + 6,
            CZ=1 + 6,
        )[r + s]
print(score)
