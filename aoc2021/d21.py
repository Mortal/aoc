from aoc import ints
_1,p1,_2,p2 = ints

def mod(a:int,b:int) -> int:
    return (a % b) or b

s1 = 0
s2 = 0
d = 1
rolls = 0
for _ in range(100000):
    roll = d + ((d + 1) % 100 or 100) + ((d + 2) % 100 or 100)
    rolls += 3
    d = (d + 3) % 100 or 100
    p1 = (p1 + roll) % 10 or 10
    s1 += p1
    if s1 >= 1000:
        print(s2, rolls, s2 * rolls)
        break
    roll = d + ((d + 1) % 100 or 100) + ((d + 2) % 100 or 100)
    rolls += 3
    d = (d + 3) % 100 or 100
    p2 = (p2 + roll) % 10 or 10
    s2 += p2
    if s2 >= 1000:
        print(s1, rolls, s1 * rolls)
        break


_1,p1,_2,p2 = ints
outcomes = [a+b+c for a in range(1,4) for b in range(1,4) for c in range(1,4)]
print(outcomes)
N = 33
ps1 = [[0] * 10 for _ in range(N)]
ps2 = [[0] * 10 for _ in range(N)]
ps1[0][p1%10] = 1
ps2[0][p2%10] = 1
wins1 = wins2 = 0
while any(z for x in (ps1,ps2) for y in x for z in y):
    ps1 = [
        [
            0 if newscore < (newpos or 10)
            else sum(ps1[newscore - (newpos or 10)][(newpos - o) % 10] for o in outcomes)
            for newpos, count in enumerate(ps1[newscore])
        ]
        for newscore in range(N)
    ]
    wins1 += sum(sum(os) for os in ps1[21:]) * sum(sum(os) for os in ps2[:21])
    ps1[21:] = [[0] * 10 for _ in range(N - 21)]
    ps2 = [
        [
            0 if newscore < (newpos or 10)
            else sum(ps2[newscore - (newpos or 10)][(newpos - o) % 10] for o in outcomes)
            for newpos, count in enumerate(ps2[newscore])
        ]
        for newscore in range(N)
    ]
    wins2 += sum(sum(os) for os in ps2[21:]) * sum(sum(os) for os in ps1[:21])
    ps2[21:] = [[0] * 10 for _ in range(N - 21)]
    # print([(score, pos, c) for score, r in enumerate(ps1) for pos, c in enumerate(r) if c])
    print(sum(sum(r) for r in ps1), sum(sum(r) for r in ps2), wins1, wins2)
print(max(wins1, wins2))
