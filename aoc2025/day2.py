from aoc import ints

ranges = list(zip(ints[::2],ints[1::2]))
p1 = 0
p2 = 0
for a, b in ranges:
    for i in range(a, b + 1):
        s = str(i)
        n = len(s)
        for k in range(2, n+1):
            if n % k:
                continue
            m = n//k
            if all(s[:m] == s[i:i+m] for i in range(0, n, m)):
                p2 += i
                if k == 2:
                    p1 += i
                # print(a, b, i, s[:m])
                break
print(p1)
print(p2)
