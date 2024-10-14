with open("d20.in") as fp:
    inp = fp.read()
if 0:
    inp = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
elif 0:
    inp = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
config: dict[str, list[str]] = {}
typ: dict[str, str] = {}
for line in inp.strip().splitlines():
    signame, targets_str = line.split(" -> ")
    name = signame.strip("%&")
    typ[name] = signame
    config[name] = targets_str.split(", ")
sources: dict[str, list[str]] = {}
for name in config:
    for target in config[name]:
        sources.setdefault(target, []).append(name)

OFF = False
ON = True
flipflop: dict[str, bool] = {
    # name: False
    # for name in typ
    # if typ[name].startswith("%")
}

conj: dict[str, dict[str, bool]] = {
    name: {s: False for s in sources[name]}
    for name in typ
    if typ[name].startswith("&")
}

LOW = False
HIGH = True

bfs: list[tuple[bool, str, str]] = []
i = 0
for presses in range(1000000):
    if presses % 1000 == 0:
        print(hex(presses + 1))
    verbose = 1 or presses == 0
    verbose and print(hex(presses + 1), " ".join("-+"[v] + k for k, v in flipflop.items()), " ".join("[{}: {}]".format(name, " ".join("-+"[v] + k for k, v in f.items())) for name, f in conj.items()))
    verbose and print(hex(presses + 1), "button -low-> broadcaster")
    bfs.append((LOW, "broadcaster", "button"))
    while i < len(bfs):
        signal, name, source = bfs[i]
        i += 1
        if name == "broadcaster":
            mysig = LOW
            for target in config[name]:
                bfs.append((mysig, target, "broadcaster"))
                verbose and print(hex(presses + 1), name, ["-low->", "-high->"][mysig], target)
        elif name in ("rx", "output"):
            if signal == LOW:
                print(hex(presses + 1), name, ["LOW", "HIGH"][signal], presses)
        elif typ[name].startswith("%"):
            if signal == LOW:
                mysig = flipflop[name] = not flipflop.get(name)
                for target in config[name]:
                    bfs.append((mysig, target, name))
                    verbose and print(hex(presses + 1), name, ["-low->", "-high->"][mysig], target)
        elif typ[name].startswith("&"):
            c = conj.setdefault(name, {})
            c[source] = signal
            mysig = not all(c.get(s) for s in sources[name])
            for target in config[name]:
                bfs.append((mysig, target, name))
                verbose and print(hex(presses + 1), name, ["-low->", "-high->"][mysig], target)

countlow = sum(s == LOW for s, n, src in bfs)
counthigh = sum(s == HIGH for s, n, src in bfs)
print(countlow, counthigh, countlow * counthigh)
