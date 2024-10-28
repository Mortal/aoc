from aoc import linetoks


s = 0
sss = 0
for *digits, pip, aa, bb, cc, dd in linetoks:
    assert len(digits) == 10
    digits.sort(key=len)
    s1 = set(digits[0])
    s7 = set(digits[1])
    s4 = set(digits[2])
    s8 = set(digits[9])
    a = s7 ^ s1
    assert len(a) == 1, a
    bd = s1 ^ s4
    assert len(bd) == 2, bd
    s9, = [set(d) for d in digits[6:9] if s4 <= set(d)]
    g = s9 - s7 - s4
    s2, = [set(d) for d in digits[3:6] if not (set(d) <= s9)]
    e = s2 - s9
    s0, = [set(d) for d in digits[6:9] if (s7 | a | g | e) <= set(d)]
    s6, = [set(d) for d in digits[6:9] if set(d) not in (s0, s9)]
    d = s8 - s0
    c = s8 - s6
    f = s1 ^ c
    b = s8 - s2 - f
    soln = [
        s0,s1,s2,s7|d|g,s4,a|b|d|f|g,s6,s7,s8,s9
    ]
    ss = []
    for x in (aa, bb, cc, dd):
        if len(x) in (2,4,3,7):
            s += 1
        for i, k in enumerate(soln):
            if k == set(x):
                ss.append(i)
    sss += int("".join(map(str, ss)))
print(s)
print(sss)
