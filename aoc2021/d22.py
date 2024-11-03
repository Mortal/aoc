from aoc import lineints, linetoks, ints
import numpy as np

state = np.zeros((101,101,101),dtype=np.uint8)

for line, (x1,x2,y1,y2,z1,z2) in zip(linetoks, lineints):
    v = 1 if line[0] == "on" else 0
    x1 = 50 + min(51,max(-50,x1))
    x2 = 50 + min(51,max(-50,x2+1))
    y1 = 50 + min(51,max(-50,y1))
    y2 = 50 + min(51,max(-50,y2+1))
    z1 = 50 + min(51,max(-50,z1))
    z2 = 50 + min(51,max(-50,z2+1))
    state[x1:x2,y1:y2,z1:z2] = v
print(np.sum(state))

xs = sorted(set(a for x1,x2,y1,y2,z1,z2 in lineints for a in (x1,x2+1)))
ys = sorted(set(a for x1,x2,y1,y2,z1,z2 in lineints for a in (y1,y2+1)))
zs = sorted(set(a for x1,x2,y1,y2,z1,z2 in lineints for a in (z1,z2+1)))
xc = {n:i for i, n in enumerate(xs)}
yc = {n:i for i, n in enumerate(ys)}
zc = {n:i for i, n in enumerate(zs)}

state = np.zeros((len(xs),len(ys),len(zs)),dtype=np.uint8)

for line, (x1,x2,y1,y2,z1,z2) in zip(linetoks, lineints):
    v = 1 if line[0] == "on" else 0
    x1 = xc[x1]
    x2 = xc[x2+1]
    y1 = yc[y1]
    y2 = yc[y2+1]
    z1 = zc[z1]
    z2 = zc[z2+1]
    state[x1:x2,y1:y2,z1:z2] = v
xz = np.r_[np.diff(xs), 0]
yz = np.r_[np.diff(ys), 0]
zz = np.r_[np.diff(zs), 0]
print(np.sum(state * xz[:,None,None] * yz[None,:,None] * zz[None,None,:]))
