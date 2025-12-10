from aoc import lines
p1 = 0
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
print(p1)
