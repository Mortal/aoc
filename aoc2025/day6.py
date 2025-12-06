from aoc import linetoks

p1 = 0
for col in zip(*linetoks):
    ints = [int(c) for c in col[:-1]]
    if col[-1] == "+":
        p1 += sum(ints)
    else:
        assert col[-1] == "*"
        m = 1
        for i in ints:
            m *= i
        p1 += m
print(p1)
