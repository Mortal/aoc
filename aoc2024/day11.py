from aoc import ints, Counter

counts = Counter(ints)

for it in range(75):
    if it == 25:
        # Part 1
        print(sum(counts.values()))
    c = Counter()
    for k, v in counts.items():
        if k == 0:
            c[1] += v
        else:
            s = str(k)
            if len(s) % 2 == 0:
                c[int(s[:len(s)//2])] += v
                c[int(s[len(s)//2:])] += v
            else:
                c[k * 2024] += v
    counts = c
# Part 2
print(sum(counts.values()))
