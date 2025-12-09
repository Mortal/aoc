from aoc import lineints

print(max(abs(x1-x2+1)*abs(y1-y2+1) for x1, y1 in lineints for x2, y2 in lineints))
