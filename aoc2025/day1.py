from aoc import lines

v = 50
p = 0
p2 = 0

for line in lines:
    atzero = v == 0
    v += int(line.replace("L", "-").replace("R", ""))
    if v > 0:
        p2 += ((v - v % 100) // 100)
        if v % 100 == 0:
            p2 -= 1
    else:
        p2 += -((v - v % 100) // 100)
        if atzero:
            p2 -= 1
    if v % 100 == 0:
        p += 1
        p2 += 1
    # print(f"{line} -> {v} = {v%100} (p={p} p2={p2})")
    v %= 100
print(p)
print(p2)
