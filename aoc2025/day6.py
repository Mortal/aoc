from aoc import linetoks, lines

p1 = 0
for col in zip(*linetoks):
    ints = [int(c) for c in col[:-1]]
    if col[-1] == "+":
        p1 += sum(ints)
    else:
        assert col[-1] == "*"
        m = 1
        for i in ints:
            m *= i
        p1 += m
print(p1)
p2 = 0
*intlines, oplines = lines
ops = oplines.split()
assert all(len(line) == len(intlines[0]) for line in intlines)

buf = []
res = []
for col in zip(*intlines):
    if all(c == " " for c in col):
        res.append(buf[:])
        del buf[:]
    else:
        buf.append(int("".join(c.strip() for c in col)))
assert buf
res.append(buf[:])
assert len(ops) == len(res)
for op, myints in zip(ops, res):
    print(p2, op, myints, myints[0], sum(myints))
    if op == "+":
        p2 += sum(myints)
        print(sum(myints))
    else:
        m = 1
        for i in myints:
            m *= i
        print(m)
        p2 += m
print(p2)
