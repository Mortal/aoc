from aoc import sectionints

assert all(len(row) == 3 for rows in sectionints for row in rows[1:])

xp = (1,0,0)
xm = (-1,0,0)
yp = (0,1,0)
ym = (0,-1,0)
zp = (0,0,1)
zm = (0,0,-1)

V = tuple[int,int,int]

def neg(a:V) -> V:
    return (-a[0],-a[1],-a[2])

def dot(a:V,b:V) -> int:
    return (a[0]*b[0]+a[1]*b[1]+a[2]*b[2])

def add(a:V,b:V) -> V:
    return (a[0]+b[0],a[1]+b[1],a[2]+b[2])

def cross(a:V,b:V) -> V:
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

def reorient(a:V,b:tuple[V,V,V]) -> V:
    return (dot(a,b[0]),dot(a,b[1]),dot(a,b[2]))

orients = [
    (a,b,cross(a,b))
    for a in (xp,xm,yp,ym,zp,zm)
    for b in (xp,xm,yp,ym,zp,zm)
    if dot(a,b) == 0
]
assert (xm,yp,zm) in orients
assert len(orients) == len(set(orients)) == 24

data = [{(a[0],a[1],a[2]) for a in rows[1:]} for rows in sectionints]
edgelists: dict[int, list[tuple[int, tuple[V,V,V], V]]] = {i: [] for i in range(len(data))}
for i, rowsi in list(enumerate(data)):
    subsi = {add(neg(a),b):(a,b) for a in rowsi for b in rowsi if a != b}
    for j, rowsj in list(enumerate(data)):
        if i == j:
            continue
        for orient in orients:
            jj = [reorient(r, orient) for r in rowsj]
            subsj = {add(neg(a),b):(a,b) for a in jj for b in jj if a != b}
            if len(subsi.keys()&subsj.keys()) >= 132:
                print(i,j,orient,len(subsi.keys()&subsj.keys()))
                k = next(iter(subsi.keys()&subsj.keys()))
                ai,bi = subsi[k]
                aj,bj = subsj[k]
                offs = add(ai,neg(aj))
                edgelists[i].append((j,orient,offs))
                assert len({add(offs,reorient(r, orient)) for r in rowsj} & set(rowsi)) >= 12

seen: set[int] = set()
def visit(i: int) -> set[V]:
    res = set(data[i])
    for j, orient, offs in edgelists[i]:
        if j not in seen:
            seen.add(j)
            res |= {add(offs, reorient(r, orient)) for r in visit(j)}
    return res

print(len(visit(0)))

seen2: set[int] = set()
def visit2(i: int) -> set[V]:
    res = {(0,0,0)}
    for j, orient, offs in edgelists[i]:
        if j not in seen2:
            seen2.add(j)
            res |= {add(offs, reorient(r, orient)) for r in visit2(j)}
    return res

def dist(a: V, b: V) -> int:
    return abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2])

scanners = sorted(visit2(0))
print(max(dist(a,b) for a in scanners for b in scanners))
