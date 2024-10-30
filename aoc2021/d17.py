from aoc import ints
x1,x2,y1,y2 = ints
State = tuple[int,int,int,int]
def step(state: State) -> State:
    x,y,r,s = state
    x += r
    y += s
    if r:
        r -= r // abs(r)
    s -= 1
    return x,y,r,s
def inside(state: State) -> bool:
    x,y,r,s = state
    return x1 <= x <= x2 and y1 <= y <= y2
def keepgoing(state: State) -> bool:
    x,y,r,s = state
    return x <= x2 and (y1 <= y or s > 0)
def solve(state: State) -> int | None:
    maxsofar = state[1]
    while keepgoing(state):
        if inside(state):
            return maxsofar
        state = step(state)
        maxsofar = max(maxsofar, state[1])
    return None
maxy = max(filter(None, (solve((0,0,r,s)) for r in range(200) for s in range(200))))
print(maxy)

x_sols = []
for vx in range(x2+1):
    vx_ = vx
    x = 0
    i = 0
    while x < x1 and vx > 0:
        x += vx
        vx -= 1
        i += 1
    if x1 <= x <= x2:
        j = i
        while x <= x2 and vx > 0:
            x += vx
            vx -= 1
            j += 1
        INF = 1000000
        if x <= x2:
            j = INF
        # With this start velocity for x, we are in-range for steps [i,j).
        x_sols.append((vx_, i, j))
        print("vx",vx_,i,j)
count = 0
solns = []
for vy in range(y1, maxy + 1):
    vy_ = vy
    y = 0
    i = 0
    while y2 < y <= maxy:
        y += vy
        vy -= 1
        i += 1
    if y1 <= y <= y2:
        j = i
        while y1 <= y <= y2:
            y += vy
            vy -= 1
            j += 1
        print("vy",vy_,i,j)
        # With this start velocity for y, we are in-range for steps [i,j).
        for vx_, ii, jj in x_sols:
            ii = max(i, ii)
            jj = min(j, jj)
            if ii < jj:
                count += 1
                solns.append((vx_, vy_))
# print(sorted(solns))
print(count)
