from aoc import ints, Counter

ra, rb, rc, *program = ints

def run(ra: int):
    _ra, rb, rc, *program = ints
    ip = 0
    out: list[int] = []
    while ip < len(program):
        ins = program[ip]
        op = program[ip+1]
        if op < 4:
            comb = op
        elif op == 4:
            comb = ra
        elif op == 5:
            comb = rb
        elif op == 6:
            comb = rc
        else:
            comb = -1
        if ins == 0:
            if comb == -1:
                return
            if isinstance(ra, list):
                ra = ra[comb:]
            else:
                ra = ra // 2**comb
        elif ins == 1:
            if isinstance(rb, list):
                assert isinstance(op, int)
                while op:
                    lsb = (op & -op).bit_length() - 1
                    op ^= 1<<lsb
                    rb = [*rb[:lsb], ~(rb[lsb]), *rb[lsb+1:]]
            else:
                rb = rb ^ op
        elif ins == 2:
            if comb == -1:
                return
            if isinstance(comb, list):
                rb = comb[:3]
            else:
                rb = comb % 8
        elif ins == 3:
            if ra != 0:
                ip = op
                continue
        elif ins == 4:
            if isinstance(rb, list):
                assert isinstance(rc, int)
                op = rc
                while op:
                    lsb = (op & -op).bit_length() - 1
                    op ^= 1<<lsb
                    rb = [*rb[:lsb], ~(rb[lsb]), *rb[lsb+1:]]
            elif isinstance(rc, list):
                assert isinstance(rb, int)
                op = rb
                while op:
                    lsb = (op & -op).bit_length() - 1
                    op ^= 1<<lsb
                    rc = [*rc[:lsb], ~(rc[lsb]), *rc[lsb+1:]]
            else:
                rb = rb ^ rc
        elif ins == 5:
            if comb == -1:
                return
            if isinstance(comb, list):
                yield comb[:3]
            else:
                yield comb % 8
        elif ins == 6:
            if comb == -1:
                return
            if isinstance(ra, list):
                rb = ra[comb:]
            else:
                rb = ra // 2**comb
        elif ins == 7:
            if comb == -1:
                return
            if isinstance(ra, list):
                assert isinstance(comb, int), (ra, comb)
                rc = ra[comb:]
            else:
                rc = ra // 2**comb
        ip += 2
        yield None


def sim(ra: int) -> list[int]:
    out = []
    for x in run(ra):
        if x is not None:
            out.append(x)
    return out


print(",".join(map(str, sim(ra))))


ra = 0
dfs = [(len(program) - 1, 0)]
results = []
while dfs:
    i, ra = dfs.pop()
    options = []
    for v in range(8):
        o = sim(ra + (v << (3*i)))
        if len(o) == len(program) and o[i:] == program[i:]:
            options.append(v)
    # print(i, ra, options)
    for v in options:
        if i == 0:
            results.append(ra + (v << (3*i)))
        else:
            dfs.append((i - 1, ra + (v << (3*i))))
if results:
    print(min(results))
