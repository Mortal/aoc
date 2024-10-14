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


State = tuple[int, int, int, int, int, int, int, int, int]
startstate: State = (0, 1, 0, 0, 0, 0, 0, 0, 0)


def resources(state: State, time: int) -> tuple[int, int, int, int]:
    (
        t,
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
    (time, orerobots, clayrobots, obsidianrobots, geoderobots, ores, clays, obsidians, geodes) = state

    oretime = max(time, (price_list[0] - ores + orerobots - 1) // orerobots)
    claytime = max(time, (price_list[1] - ores + orerobots - 1) // orerobots)
    obstime = 25 if clayrobots == 0 else max(
        time,
        (price_list[2] - ores + orerobots - 1) // orerobots,
        (price_list[3] - clays + clayrobots - 1) // clayrobots,
    )
    geodetime = 25 if obsidianrobots == 0 else max(
        time,
        (price_list[4] - ores + orerobots - 1) // orerobots,
        (price_list[5] - obsidians + obsidianrobots - 1) // obsidianrobots,
    )
    return (
        None if oretime >= 24 else (
            oretime,
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
            claytime,
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
            obstime,
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
            geodetime,
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


# dp1: At time t, what is the
for price_list in price_lists:
    state = startstate
    while True:
        s1, s2, s3, s4 = edges(price_list, state)
        if s3 and s4:
            state = min(s3, s4)
        elif (nextstate := s3 or s4) is not None:
            state = nextstate
        elif s1 and s2:
            state = min(s1, s2)
        elif (nextstate := s1 or s2) is not None:
            state = nextstate
        else:
            break
        print(state, resources(state, state[0]))
