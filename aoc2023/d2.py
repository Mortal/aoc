from aoc import lines

games = []
for line in lines:
    gameno, thegame = line.split(": ")
    reds = []
    greens = []
    blues = []
    for round in thegame.split("; "):
        counts = dict(red=0, green=0, blue=0)
        for colored in round.split(", "):
            numstr, color = colored.split()
            counts[color] = int(numstr)
        reds.append(counts['red'])
        greens.append(counts['green'])
        blues.append(counts['blue'])
    games.append((reds, greens, blues))

possible = [i for i, (reds, greens, blues) in enumerate(games, 1) if max(reds) <= 12 and max(greens) <= 13 and max(blues) <= 14]
print(possible)
print(sum(possible))
power = [max(reds) * max(greens) * max(blues) for i, (reds, greens, blues) in enumerate(games, 1)]
print(power)
print(sum(power))
