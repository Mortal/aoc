with open("d19.txt") as fp:
    s = fp.read().strip()
if 1:
    s = """
    Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
    Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
    """.strip()
price_lists: list[tuple[int, int, int, int, int, int]] = []
for line in s.splitlines():
    words = line.split()
    price_lists.append(
        (
            int(words[6]),
            int(words[12]),
            int(words[18]),
            int(words[21]),
            int(words[27]),
            int(words[30]),
        )
    )

startstate = (1, 0, 0, 0, 0, 0, 0, 0)


State = tuple[int, int, int, int, int, int, int, int]


def resources(state: State, time):
    (
        orerobots,
        clayrobots,
        obsidianrobots,
        geoderobots,
        ores,
        clays,
        obsidians,
        geodes,
    ) = state
    return (
        ores + orerobots * time,
        clays + clayrobots * time,
        obsidians + obsidianrobots * time,
        geodes + geoderobots * time,
    )


PriceList = tuple[int, int, int, int, int, int]


def edges(price_list: PriceList, state: State) -> tuple[State | None, State | None, State | None, State | None]:
    (orerobots, clayrobots, obsidianrobots, geoderobots, ores, clays, obsidians, geodes) = state

    oretime = max(0, (price_list[0] - ores + orerobots - 1) // orerobots)
    claytime = max(0, (price_list[1] - ores + orerobots - 1) // orerobots)
    obstime = 25 if clayrobots == 0 else max(
        0,
        (price_list[2] - ores + orerobots - 1) // orerobots,
        (price_list[3] - clays + clayrobots - 1) // clayrobots,
    )
    geodetime = 25 if obsidianrobots == 0 else max(
        0,
        (price_list[4] - ores + orerobots - 1) // orerobots,
        (price_list[5] - obsidians + obsidianrobots - 1) // obsidianrobots,
    )
    return (
        None if oretime >= 24 else (
            orerobots + 1,
            clayrobots,
            obsidianrobots,
            geoderobots,
            ores - (oretime + 1) - price_list[0],
            clays,
            obsidians,
            geodes,
        ),
        None if claytime >= 24 else (
            orerobots,
            clayrobots + 1,
            obsidianrobots,
            geoderobots,
            ores - price_list[1],
            clays - (claytime + 1),
            obsidians,
            geodes,
        ),
        None if obstime >= 24 else (
            orerobots,
            clayrobots,
            obsidianrobots + 1,
            geoderobots,
            ores - price_list[2],
            clays - price_list[3],
            obsidians - (obstime + 1),
            geodes,
        ),
        None if geodetime >= 24 else (
            orerobots,
            clayrobots,
            obsidianrobots,
            geoderobots + 1,
            ores - price_list[4],
            clays,
            obsidians - price_list[5],
            geodes - (geodetime + 1),
        ),
    )


def run(price_list: PriceList) -> int:
    dfs0 = [startstate]
    dfs1 = dfs0[0:0]
    dfs2 = dfs0[0:0]
    dfs3 = dfs0[0:0]
    bestsofar = 0
    bt: dict[State, tuple[int, State]] = {}

    def backtrack(s: State) -> list[int]:
        if s == startstate:
            return []
        i, s = bt[s]
        r = backtrack(s)
        r.append(i)
        return r

    while True:
        if dfs3:
            state = dfs3.pop()
            a = 3
        elif dfs2:
            state = dfs2.pop()
            a = 2
        elif dfs1:
            state = dfs1.pop()
            a = 1
        elif dfs0:
            state = dfs0.pop()
            a = 0
        else:
            break
        ns = edges(price_list, state)
        v1 = state[5] + state[1] * 24
        v2 = state[6] + state[2] * 24
        v3 = state[7] + state[3] * 24
        if bestsofar == 9:
            print(state, v1, v2, v3, backtrack(state))
        if v3 > bestsofar:
            bestsofar = v3
            print(state, v3)
        elif ns == (None, None, None, None):
            # print(state, resources(state, 24))
            continue
        for i, neighbor in enumerate(ns):
            if neighbor:
                bt[neighbor] = (i, state)
        if ns[0] and a < 2 and v1 < 30:
            dfs0.append(ns[0])
        if ns[1] and a < 3 and v2 < 30:
            dfs1.append(ns[1])
        if ns[2] and v3 < 30:
            dfs2.append(ns[2])
        if ns[3]:
            dfs3.append(ns[3])
    return bestsofar


def runtest(price_list: PriceList, order: str) -> int:
    state = startstate
    for o in order:
        nextstate = edges(price_list, state)[ord(o) - ord("A")]
        # print(state, o, nextstate)
        assert nextstate is not None
        state = nextstate
    return state[7] + state[3] * 24


from miniscreen import MiniScreen

with MiniScreen() as ms:
    for ev in ms:
        try:
            s = " %s" % runtest(price_lists[1], ms.linebuf)
        except Exception:
            s = ""
        ms.set_text_after_input(s)


print(runtest(price_lists[0], "BBBCBCDD"))
print(runtest(price_lists[1], "AABBBCCD"))
# for price_list in price_lists:
    # print(run(price_list))
    # state = startstate
    # orderindex = 0
    # time = 0
    # for o in order:
    #     nextstate = edges(price_list, state)[ord(o) - ord("A")]
    #     print(state, o, nextstate)
    #     assert nextstate is not None
    #     state = nextstate
    #     # if o == "A":
    #     #     required = (price_list[0], 0, 0, 0)
    #     # elif o == "B":
    #     #     required = (price_list[1], 0, 0, 0)
    #     # elif o == "C":
    #     #     required = (price_list[2], price_list[3], 0, 0)
    #     # elif o == "D":
    #     #     required = (price_list[4], 0, price_list[5], 0)
    #     # have = resources(state, time)
    #     # if all(h >= r for h, r in zip(have, required)):
    #     #     print(time, have, required, "Immediate buy", o)
    #     #     continue
    #     # speed = state[:4]
    #     # wait = max((r - h + s - 1) // s for r, h, s in zip(required, have, speed) if s)
    #     # for i in range(1, wait + 1):
    #     #     print(time + i, resources(state, time + i), speed, required, o)
    #     # time += wait
    #     # which = ord(o) - ord("A")
    #     # buildstate = list(state)
    #     # buildstate[which] += 1
    #     # buildstate[4 + which] -= time + 1
    #     # for i, r in enumerate(required):
    #     #     buildstate[4 + i] -= r
    #     # state = tuple(buildstate)
    #     # # print(state)
    #     # assert len(state) == 8
    # print(24, resources(state, 24))
