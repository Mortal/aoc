import math

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
print("digraph {")
for name in config:
    print(f'"{typ.get(name, name)}" [label="{typ.get(name, name)}"];')
    for target in config[name]:
        print(f'"{typ.get(name, name)}" -> "{typ.get(target, target)}";')
        sources.setdefault(target, []).append(name)
print("}")

zr, = sources["rx"]
assert typ[zr].startswith("&")
for inv in sources[zr]:
    assert typ[inv].startswith("&")
    con, = sources[inv]
    assert typ[con].startswith("&")
    chain = {}
    for src in sources[con]:
        while src != "broadcaster":
            assert typ[src].startswith("%")
            prev, = [s for s in sources[src] if s != con]
            chain[prev] = src
            src = prev
    broadcaster, = chain.keys() - chain.values()
    sink, = chain.values() - chain.keys()
    assert broadcaster == "broadcaster"
    src = chain[broadcaster]
    # Find out how many lows and highs are sent
    # when sending pulses to src
    # before a high pulse is sent to zr

    OFF = False
    ON = True

    LOW = False
    HIGH = True

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

    bfs: list[tuple[bool, str, str]] = []
    i = 0
    for presses in range(1000000):
        verbose = 0
        verbose and print(presses, src, zr, inv, conj[zr].get(inv))
        if conj[zr].get(inv):
            verbose and print(zr, inv, presses)
            break
        # verbose and print("button -low-> broadcaster")
        # bfs.append((LOW, "broadcaster", "button"))
        verbose and print(f"broadcaster -low-> {typ[src]}")
        bfs.append((LOW, src, "broadcaster"))
        foundit = False
        while i < len(bfs):
            signal, name, source = bfs[i]
            i += 1
            if name == "broadcaster":
                mysig = LOW
                for target in config[name]:
                    bfs.append((mysig, target, "broadcaster"))
                    verbose and print(name, ["-low->", "-high->"][mysig], target)
            elif name in ("rx", "output"):
                if signal == LOW:
                    print(name, ["LOW", "HIGH"][signal], presses)
            elif typ[name].startswith("%"):
                if signal == LOW:
                    mysig = flipflop[name] = not flipflop.get(name)
                    for target in config[name]:
                        bfs.append((mysig, target, name))
                        verbose and print(name, ["-low->", "-high->"][mysig], target)
            elif typ[name].startswith("&"):
                c = conj.setdefault(name, {})
                c[source] = signal
                mysig = not all(c.get(s) for s in sources[name])
                for target in config[name]:
                    bfs.append((mysig, target, name))
                    verbose and print(name, ["-low->", "-high->"][mysig], target)
                if name == zr and signal is HIGH:
                    countlow = sum(s == LOW for s, n, src in bfs)
                    counthigh = sum(s == HIGH for s, n, src in bfs)
                    print(repr((zr, inv, presses, countlow, counthigh)))
                    foundit = True
        if foundit:
            break

    countlow = sum(s == LOW for s, n, src in bfs)
    counthigh = sum(s == HIGH for s, n, src in bfs)
    print(repr((zr, inv, presses, countlow, counthigh)))
