from aoc import sectionlines
import re

transitions_str, states_str = sectionlines
transitions = {
        k: v
        for line in transitions_str
        for k, *v in [re.findall(r'[A-Za-z0-9]+|[<>]', line)]
        }

thesum = 0
for line in states_str:
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
