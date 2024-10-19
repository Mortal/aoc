from aoc import lines

pos = 0
depth = 0
for line in lines:
    cmd, n_str = line.split()
    n = int(n_str)
    if cmd == "forward":
        pos += n
    elif cmd == "down":
        depth += n
    elif cmd == "up":
        depth -= n
print(pos*depth)

pos = 0
depth = 0
aim = 0
for line in lines:
    cmd, n_str = line.split()
    n = int(n_str)
    if cmd == "forward":
        pos += n
        depth -= aim * n
    elif cmd == "down":
        aim -= n
    elif cmd == "up":
        aim += n
print(pos*depth)
