from aoc import linetoks

pos = 0
depth = 0
for cmd, n in linetoks:
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
for cmd, n in linetoks:
    if cmd == "forward":
        pos += n
        depth -= aim * n
    elif cmd == "down":
        aim -= n
    elif cmd == "up":
        aim += n
print(pos*depth)
