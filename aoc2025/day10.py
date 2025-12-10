from aoc import lines
p1 = 0
for line in lines:
    goal_str, *buttons_str, jolt_str = line.split()
    goal = sum(2**i for i, c in enumerate(goal_str[1:-1]) if c == "#")
    buttons = [sum(2**int(v) for v in button_str[1:-1].split(",")) for button_str in buttons_str]
    print(bin(goal), [bin(b) for b in buttons])
    dists = {0: 0}
    bfs = [0]
    i = 0
    while i < len(bfs):
        st = bfs[i]
        i += 1
        for b in buttons:
            n = st ^ b
            if n not in dists:
                dists[n] = dists[st] + 1
                if n == goal:
                    break
                bfs.append(n)
        if goal in dists:
            break
    print(dists[goal])
    p1 += dists[goal]
print(p1)
