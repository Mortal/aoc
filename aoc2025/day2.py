from aoc import ints

ranges = list(zip(ints[::2],ints[1::2]))
p1 = 0
for a, b in ranges:
    for i in range(a, b + 1):
        n = len(str(i))
        if n % 2 == 0 and str(i)[:n//2] == str(i)[n//2:]:
            p1 += i
print(p1)
