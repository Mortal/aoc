from aoc import lines
import z4

p1 = 0
p2 = 0
for line in lines:
    goal1_str, *buttons_str, goal2_str = line.split()
    goal1 = sum(2**i for i, c in enumerate(goal1_str[1:-1]) if c == "#")
    buttons1 = [sum(2**int(v) for v in button_str[1:-1].split(",")) for button_str in buttons_str]
    dists1 = {0: 0}
    bfs = [0]
    i = 0
    while i < len(bfs):
        st = bfs[i]
        i += 1
        for b in buttons1:
            n = st ^ b
            if n not in dists1:
                dists1[n] = dists1[st] + 1
                if n == goal1:
                    break
                bfs.append(n)
        if goal1 in dists1:
            break
    p1 += dists1[goal1]

    goal2 = tuple(map(int, goal2_str[1:-1].split(',')))
    buttons2 = [tuple(map(int, button_str[1:-1].split(','))) for button_str in buttons_str]
    zero = (0,)*len(goal2)
    dists2 = {zero: 0}
    vars = [z4.Int(f"b{i}") for i in range(len(buttons2))]
    res = z4.minimize(
        sum(vars),
        [var >= 0 for var in vars]
        + [
            sum(vars[j] for j in range(len(buttons2)) if i in buttons2[j]) == goal2[i]
            for i in range(len(goal2))
        ],
    )
    p2 += int(res[0].as_long())
print(p1)
print(p2)
