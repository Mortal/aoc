from aoc import lineints, ceil


def step(costs, resources=(0, 0, 0), dr=(1, 0, 0), timeleft=24):
    if (resources, dr, timeleft) in MEMO:
        return MEMO[(resources, dr, timeleft)]

    if timeleft <= 1:
        MEMO[(resources, dr, timeleft)] = 0
        return 0

    # assert all(x >= 0 for x in resources), (resources, dr, timeleft)

    # Observation 0: There's no point in building more bots for a given type
    #  if we can already optimally spend the resources in the remaining time without them
    max_dor = int(ceil((max(costs[0], costs[1], costs[2], costs[4]) * timeleft - resources[0]) / timeleft))
    max_dcl = int(ceil((costs[3] * timeleft - resources[1]) / timeleft))
    max_dob = int(ceil((costs[5] * timeleft - resources[2]) / timeleft))

    need_or = dr[0] < max_dor
    need_cl = dr[1] < max_dcl
    need_ob = dr[2] < max_dob

    build_ge = resources[0] >= costs[4] and resources[2] >= costs[5]
    build_ob = resources[0] >= costs[2] and resources[1] >= costs[3] and need_ob
    # Observation 1: We don't need more Clay Institutes if we can't hire any more Obsidian employees
    build_cl = resources[0] >= costs[1] and need_cl and need_ob
    build_or = resources[0] >= costs[0] and need_or

    score = 0
    # Observation 2: We want to prioritize the Geodudes where possible
    if build_ge:
        resources_ = (resources[0] + dr[0] - costs[4], resources[1] + dr[1], resources[2] + dr[2] - costs[5])
        # if we're building a Geodude then we're getting T - 1 geodes from this newly built Geodude
        score = max(score, step(costs, resources=resources_, dr=dr, timeleft=timeleft-1) + timeleft - 1)
    else:
    # Observation 3: We want to prioritize Obsidian employees when Geodudes are unavailable
        if build_ob:
            resources_ = (resources[0] + dr[0] - costs[2], resources[1] + dr[1] - costs[3], resources[2] + dr[2])
            score = max(score, step(costs, resources=resources_, dr=(dr[0], dr[1], dr[2] + 1), timeleft=timeleft-1))
        else:
            if build_or:
                resources_ = (resources[0] + dr[0] - costs[0], resources[1] + dr[1], resources[2] + dr[2])
                score = max(score, step(costs, resources=resources_, dr=(dr[0] + 1, dr[1], dr[2]), timeleft=timeleft-1))
            if build_cl:
                resources_ = (resources[0] + dr[0] - costs[1], resources[1] + dr[1], resources[2] + dr[2])
                score = max(score, step(costs, resources=resources_, dr=(dr[0], dr[1] + 1, dr[2]), timeleft=timeleft-1))
            resources_ = (resources[0] + dr[0], resources[1] + dr[1], resources[2] + dr[2])
            score = max(score, step(costs, resources=resources_, dr=dr, timeleft=timeleft-1))
    MEMO[(resources, dr, timeleft)] = score
    return score

t = 0
for bpid, oro, clo, obo, obc, gor, gob in lineints:
    costs = (oro, clo, obo, obc, gor, gob)
    MEMO = {}
    score = step(costs)
    print("Done with", bpid, len(MEMO), score)
    t += (bpid * score)
print("Part 1:", t)

t = 1
for bpid, oro, clo, obo, obc, gor, gob in lineints[0:3]:
    costs = (oro, clo, obo, obc, gor, gob)
    MEMO = {}
    score = step(costs, timeleft=32)
    print("Done with", bpid, len(MEMO), score)
    t *= score
print("Part 2:", t)
