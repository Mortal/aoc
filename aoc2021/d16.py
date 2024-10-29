from aoc import inp

print(repr(inp))

bits = bin(int(inp, 16))[2:].rjust(4*len(inp),'0')
print(bits)

pos = 0

def read(n: int) -> int:
    global pos
    s = bits[pos : pos + n]
    pos += n
    return int(s, 2)

versionsum = 0

def packet() -> int:
    global versionsum
    version = read(3)
    versionsum += version
    print("version", version)
    typ = read(3)
    if typ == 4:
        r = 0
        while True:
            c = read(1)
            r = (r << 4) | read(4)
            if not c:
                break
        print("literal", r)
        return r
    print("typ", typ)
    lentyp = read(1)
    args = []
    if lentyp == 0:
        totbits = read(15)
        print(f"{totbits=}")
        target = pos + totbits
        while pos < target:
            args.append(packet())
    else:
        subpaks = read(11)
        print(f"{subpaks=}")
        for _ in range(subpaks):
            args.append(packet())
    if typ == 0:
        return sum(args)
    if typ == 1:
        p = 1
        for a in args:
            p *= a
        return p
    if typ == 2:
        return min(args)
    if typ == 3:
        return max(args)
    if typ == 5:
        return int(args[0] > args[1])
    if typ == 6:
        return int(args[0] < args[1])
    if typ == 7:
        return int(args[0] == args[1])


r = packet()
print(inp, versionsum, r)
