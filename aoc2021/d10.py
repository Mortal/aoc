from aoc import lines

ma={a:b for a, b in zip("([{<", ")]}>")}
pts={b:p for p, b in zip((3,57,1197,25137), ")]}>")}
pts2={b:p for p, b in zip((1,2,3,4), ")]}>")}
p = 0
p2 = []
for line in lines:
    stack = []
    inval = False
    for c in line:
        if c in ma:
            stack.append(ma[c])
        elif stack and stack[-1] == c:
            stack.pop()
        else:
            if not inval:
                # print(f"Expected {stack[-1]}, but found {c} instead")
                p += pts[c]
            inval = True
    if stack and not inval:
        score = 0
        for c in stack[::-1]:
            score = 5 * score + pts2[c]
        p2.append(score)
print(p)
print(sorted(p2)[len(p2)//2])
