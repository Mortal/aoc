s = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()
price_lists: list[tuple[int, int, int, int, int, int]] = []
for line in s.splitlines():
    words = line.split()
    price_lists.append((int(words[6]), int(words[12]), int(words[18]), int(words[21]), int(words[27]), int(words[30])))
for priceindex, prices in enumerate(price_lists):
    # First ore robot: n ore after n minutes
    # Second ore robot: n ore after n-p[0] minutes
    # => 2*n-p[0] ore after n minutes
    # Earliest time to build 1 clay robot: p[0] minutes
    states = [(1, 0, 0, 0, 0, 0, 0, 0)]
    s2 = states[0:0]
    for dayindex in range(24):
        print(priceindex, dayindex, len(states), max(bb for a, b, c, d, aa, bb, cc, dd in states), max(dd for a, b, c, d, aa, bb, cc, dd in states))
        # print(states)
        for a, b, c, d, aa, bb, cc, dd in states:
            aa += a
            bb += b
            cc += c
            dd += d
            for na in range(aa // prices[0] + 1):
                sa = na * prices[0]
                for nb in range((aa - sa) // prices[1] + 1):
                    sb = sa + nb * prices[1]
                    for nc in range(min((aa - sb) // prices[2], bb // prices[3]) + 1):
                        sc = sb + nc * prices[2]
                        sd = nc * prices[3]
                        for nd in range(min((aa - sc) // prices[4], cc // prices[5]) + 1):
                            se = sc + nd * prices[4]
                            sf = nd * prices[5]
                            if se + max(prices[0], prices[1], prices[2], prices[4]) >= aa or 0 < sd >= bb - prices[3] or 0 < sf >= cc - prices[5]:
                                s2.append((a + na, b + nb, c + nc, d + nd, aa - se, bb - sd, cc - sf, dd))
        states, s2 = s2, states
        del s2[:]
    print(max(dd for a, b, c, d, aa, bb, cc, dd in states))
