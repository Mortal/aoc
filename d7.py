from aoc import lines
import collections

order = "AKQT98765432J"[::-1]

def keyfun(s: str) -> tuple[int, tuple[int, ...]]:
    counter = collections.Counter(s[:5])
    jokercount = counter.pop("J", 0)
    counts = sorted(counter.items(), key=lambda x: -x[1])
    indices = tuple(order.index(c) for c in s[:5])
    c1 = counts[0][1] if len(counts) >= 1 else 0
    c2 = counts[1][1] if len(counts) >= 2 else 0
    if c1 + jokercount == 5:
        return 10, indices
    if c1 + jokercount == 4:
        return 9, indices
    if jokercount == 3:
        return 8, indices
    if jokercount == 2:
        if c1 == 2:
            return 8, indices
        return 7, indices
    assert jokercount <= 1
    if c1 + jokercount == 3:
        if c2 == 2:
            return 8, indices
        return 7, indices
    if c1 + jokercount == 2:
        if c2 == 2:
            return 6, indices
        return 5, indices
    return 0, indices

lines.sort(key=keyfun)
print("\n".join(f"{s} {keyfun(s)[0]}" for s in lines))
print(sum(i * int(s[6:]) for i, s in enumerate(lines, 1)))
