with open("aoc2022d1.txt") as fp:
    inputs = fp.read().split("\n\n")
print(sum(sorted(sum(map(int, s.split())) for s in inputs)[-3:]))
