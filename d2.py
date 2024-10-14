import re

lines = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
""".strip().splitlines()

if 1:
    with open("d2.in") as fp:
        lines = fp.read().strip().splitlines()

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
