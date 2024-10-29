from aoc import sectiontoks, Counter

tpl = sectiontoks[0][0][0]
rules = {a:c for a, b, c in sectiontoks[1]}
state = Counter(zip(tpl, tpl[1:]))
counts = Counter(tpl)
for _ in range(40):
    newstate = Counter()
    for (a, b), c in state.items():
        d = rules[a+b]
        newstate[a,d]+=c
        newstate[d,b]+=c
        counts[d] += c
    state = newstate
print(counts)
print(max(counts.values())-min(counts.values()))
