import sympy

numbers: dict[str, int] = {}
ops: dict[str, tuple[str, str, str]] = {}


s = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""


with open("d21.txt") as fp:
    for line in fp:
        words = line.split()
        name = words[0].strip(":")
        if len(words) == 2:
            numbers[name] = int(words[1])
        else:
            op = words[2]
            if op == "/":
                op = "//"
            ops[name] = words[1], op, words[3]


numbers["humn"] = sympy.Symbol("humn")


def evalname(name: str) -> int:
    try:
        return numbers[name]
    except KeyError:
        pass
    left, op, right = ops[name]
    leftval = evalname(left)
    rightval = evalname(right)
    if op == "+":
        value = leftval + rightval
    elif op == "-":
        value = leftval - rightval
    elif op == "*":
        value = leftval * rightval
    elif op == "//":
        if isinstance(leftval, int) and isinstance(rightval, int):
            assert leftval % rightval == 0
            value = leftval // rightval
        else:
            value = leftval / rightval
    else:
        raise
    numbers[name] = value
    return value

ops["root"] = (ops["root"][0], "-", ops["root"][2])
print(sympy.solve(evalname("root")))
