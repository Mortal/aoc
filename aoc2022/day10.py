res1 = 0
output = []
with open("day10.in") as fp:
    c = 0
    x = 1
    for line in fp:
        if line.strip() == "noop":
            cs = 1
            n = 0
        else:
            n = int(line.split()[1])
            cs = 2
        for _ in range(cs):
            if x - 1 <= c % 40 <= x + 1:
                output.append("#")
            else:
                output.append(".")
            c += 1
            if c in range(20, 260, 40):
                print(f"{c=} {x=} {c * x=}")
                res1 += c * x
            if c in range(0, 240, 40):
                output.append("\n")
        x += n
print(res1)
print("".join(output))
