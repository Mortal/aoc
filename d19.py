with open("d19.in") as fp:
    inp = fp.read()
if 0:
    inp = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

transitions_str, states_str = inp.strip().split("\n\n")
import re
transitions = {
        k: v
        for line in transitions_str.splitlines()
        for k, *v in [re.findall(r'[A-Za-z0-9]+|[<>]', line)]
        }

thesum = 0
for line in states_str.splitlines():
    vals1 = list(map(int, re.findall(r'[0-9]+', line)))
    state = "in"
    while state in transitions:
        t = transitions[state]
        for var, op, val, nextstate in zip(t[::4], t[1::4], t[2::4], t[3::4]):
            myval = vals1["xmas".index(var)]
            if op == "<" and myval < int(val) or op == ">" and myval > int(val):
                print(state,vals1,var,op,val,nextstate)
                state = nextstate
                break
        else:
            print(state,vals1,t[-1])
            state = t[-1]
    print(state)
    if state == "A":
        thesum += sum(vals1)
print(thesum)

dfs = [("in", ((1,4001),)*4)]
thesum = 0
while dfs:
    state, vals = dfs.pop()
    print(thesum, len(dfs), state, vals)
    if state == "A":
        a,b,c,d = (b-a for a, b in vals)
        thesum += a*b*c*d
        continue
    if state == "R":
        continue
    t = transitions[state]
    for var, op, val, nextstate in zip(t[::4], t[1::4], t[2::4], t[3::4]):
        i = "xmas".index(var)
        a, b = vals[i]
        if op == "<":
            yes = a, min(b, int(val))
            no = max(a, int(val)), b
        else:
            no = a, min(b, int(val) + 1)
            yes = max(a, int(val) + 1), b
        if yes[0] < yes[1]:
            dfs.append((nextstate, (*vals[:i], yes, *vals[i+1:])))
        if no[0] < no[1]:
            vals = (*vals[:i], no, *vals[i+1:])
        else:
            break
    else:
        dfs.append((t[-1], vals))
print(thesum)
