from aoc import inp, lines


names = "one|two|three|four|five|six|seven|eight|nine".split("|")
numbers: list[int] = []
for line in lines:
    firstpos, first = min(
        [(line.find(str(i + 1)), i + 1)
         for i in range(9)
         if str(i + 1) in line] +
        [(line.find(n), i + 1)
        for i, n in enumerate(names)
        if n in line]
    )
    lastpos, last = max(
        [(line.rfind(str(i + 1)), i + 1)
         for i in range(9)
         if str(i + 1) in line] +
        [(line.rfind(n), i + 1)
        for i, n in enumerate(names)
        if n in line]
    )
    #assert firstpos < lastpos, line
    numbers.append(first * 10 + last)
print(sum(numbers))
