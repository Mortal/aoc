with open("day9.in") as fp:
    s = fp.read()
x = [0] * 10
y = [0] * 10
positions = {(x[-1], y[-1])}
for line in s.splitlines():
    d, n_str = line.split()
    n = int(n_str)
    dx, dy = dict(R=(1,0),U=(0,1),L=(-1,0),D=(0,-1))[d]
    for j in range(n):
        x[0] += dx
        y[0] += dy
        for i in range(1, len(x)):
            while not (x[i-1] - 1 <= x[i] <= x[i-1] + 1 and y[i-1] - 1 <= y[i] <= y[i-1] + 1):
                x[i] += max(-1, min(1, x[i-1] - x[i]))
                y[i] += max(-1, min(1, y[i-1] - y[i]))
        positions.add((x[-1], y[-1]))
print(len(positions))
