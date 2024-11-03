from aoc import mat
from dataclasses import dataclass

sa1,sa2 = mat.findall("A")
sb1,sb2 = mat.findall("B")
sc1,sc2 = mat.findall("C")
sd1,sd2 = mat.findall("D")
ts = ta1,tb1,tc1,td1,ta2,tb2,tc2,td2 = sorted([sa1,sa2, sb1,sb2, sc1,sc2, sd1,sd2])
V = tuple[int,int]
spent = 0

dprint = lambda s: 0

@dataclass(frozen=True)
class State:
    a1:V
    a2:V
    b1:V
    b2:V
    c1:V
    c2:V
    d1:V
    d2:V

    def done(self) -> bool:
        return self.a1[1] == self.a2[1] == 3 and self.b1[1] == self.b2[1] == 5 and self.c1[1] == self.c2[1] == 7 and self.d1[1] == self.d2[1] == 9

    def all(self) -> dict[V,str]:
        return {
            self.a1: "a1",
            self.a2: "a2",
            self.b1: "b1",
            self.b2: "b2",
            self.c1: "c1",
            self.c2: "c2",
            self.d1: "d1",
            self.d2: "d2",
        }

    def edges(self) -> list[tuple[int, "State"]]:
        locs = self.all()
        dprint("\n".join("".join(locs[i,j][0].upper() if (i,j) in locs else "." if c in "ABCD" else c for j, c in enumerate(row)) for i, row in enumerate(mat)))
        edges: list[tuple[int, State]] = []
        for pos, which in locs.items():
            en = dict(a=1,b=10,c=100,d=1000)[which[0]]
            target = dict(a=3,b=5,c=7,d=9)[which[0]]
            if pos[0] == 3:
                if pos[1] == target:
                    continue
                above = (pos[0]-1,pos[1])
                if above in locs:
                    continue
                dprint(f"Move {which} one up to {above} for {en}")
                edges.append((en, State(**({which: pos for pos, which in locs.items()} | {which: above}))))
            elif pos[0] == 2:
                below = (pos[0]+1,pos[1])
                if pos[1] == target and below not in locs:
                    dprint(f"Move {which} one down to {below} for {en}")
                    edges.append((en, State(**({which: pos for pos, which in locs.items()} | {which: below}))))
                    continue
                for above in ((pos[0]-1,pos[1]-1), (pos[0]-1,pos[1]+1)):
                    if above not in locs:
                        dprint(f"Move {which} up to {above} for 2*{en}")
                        edges.append((2*en, State(**({which: pos for pos, which in locs.items()} | {which: above}))))
            else:
                assert pos[0] == 1
                xs = {1: [2], 2: [1,4], 4: [2,6], 6: [4,8], 8: [6, 10], 10: [8, 11], 11: [10]}
                for x in xs[pos[1]]:
                    if (1, x) not in locs:
                        dprint(f"Move {which} horizontally to {x}")
                        edges.append((abs(x-pos[1])*en, State(**({which: pos for pos, which in locs.items()} | {which: (1,x)}))))
                belows = {1: [], 2: [3], 4: [3,5], 6: [5,7], 8: [7,9], 10: [9], 11: []}
                for x in belows[pos[1]]:
                    if (2, x) not in locs and x == target:
                        dprint(f"Move {which} diagonally down to 2,{x}")
                        edges.append((2*en, State(**({which: pos for pos, which in locs.items()} | {which: (2,x)}))))
        return edges

start = State( sa1,sa2, sb1,sb2, sc1,sc2, sd1,sd2)
pq = [[start]]
bestsofar = {start:0}
for v, states in enumerate(pq):
    if v % 1000 == 0:
        print(v)
    if v > 14800:
        print("too bad")
        break
    for state in states:
        if v != bestsofar[state]:
            continue
        if state.done():
            print("Goal:", v)
            break
        for e, s in state.edges():
            if v + e < bestsofar.get(s, v+e+1):
                bestsofar[s] = v+e
                pq.extend([[] for _ in range(v+e+1 - len(pq))])
                pq[v+e].append(s)
    else:
        continue
    break
exit()
def move(s:V,t:V) -> V:
    global spent
    ch = mat.read(s)
    en = dict(A=1,B=10,C=100,D=1000)[ch]
    a,b=s
    c,d=t
    mat[a][b] = '.'
    mat[c][d] = ch
    v = (abs(1-a)+abs(1-c)+abs(b-d))*en
    spent += v
    print(f"Move {ch} from {a},{b} to {c},{d} spending {v}")
    return t

c1=move(sc1,(1,10))
b2=move(sb2,(1,2))
print("\n".join("".join(row) for row in mat))
move(sd2,td2)
move(sd1,td1)
print("\n".join("".join(row) for row in mat))
c2=move(sc2,(1,8))
move(sa1,ta2)
move(sa2,ta1)
move(b2,tb2)
move(sb1,tb1)
move(c2,tc2)
move(c1,tc1)

print("\n".join("".join(row) for row in mat))

print(spent)
