from aoc import sectionints
print(sum(sorted(sum(map(sum, section)) for section in sectionints)[-3:]))
