with open("d25.txt") as fp:
    numbers = fp.read().strip().splitlines()

if 0:
    numbers = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".strip().splitlines()

def decode(s: str) -> int:
    v = sum(5 ** i * ("=-012".index(s) - 2) for i, s in enumerate(s[::-1]))
    assert v == sum(5 ** i * "=-012".index(s) for i, s in enumerate(s[::-1])) - sum(5 ** i * 2 for i in range(len(s)))
    return v

def encode(n: int) -> str:
    m = 1
    v = 0
    i = 0
    while n + v >= m:
        m *= 5
        v += 2 * 5 ** i
        i += 1
    n += v
    res = []
    while n > 0:
        n, r = divmod(n, 5)
        res.append("=-012"[r])
    return "".join(res)[::-1]

print(encode(sum(decode(s) for s in numbers)))
