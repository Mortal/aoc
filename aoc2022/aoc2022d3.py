import string

with open("aoc2022d3.txt") as fp:
    s = fp.read().split()
# print(sum(1 + (string.ascii_lowercase + string.ascii_uppercase).index(next(iter(set(t[:len(t)//2]) & set(t[len(t)//2:])))) for t in s))
print(
    sum(
        1
        + (string.ascii_lowercase + string.ascii_uppercase).index(
            next(iter(set(a) & set(b) & set(c)))
        )
        for a, b, c in zip(s[::3], s[1::3], s[2::3])
    )
)
