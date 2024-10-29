from aoc import sectionints, inp
import re

xy = re.findall('[xy]', inp)
folds = [(a, b) for a, (b,) in zip(xy,sectionints[1])]
dots = []

for x, y in sectionints[0]:
    for a, b in folds:
        if a == "x":
            if x > b:
                x = 2 * b - x
        else:
            if y > b:
                y = 2 * b - y
        # break
    dots.append((x, y))
xs, ys = zip(*dots)
for y in range(max(ys)+1):
    print("".join(".#"[(x, y) in dots] for x in range(max(xs)+1)))
