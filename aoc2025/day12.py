from aoc import sectionlines, sectionints

Shape = tuple[tuple[str, ...], ...]

def flipy(shape: Shape) -> Shape:
    return shape[::-1]

def rot(shape: Shape) -> Shape:
    return tuple(tuple(line[::-1]) for line in zip(*shape))

*shapes_str, _regions_str = sectionlines
shapes = [tuple(tuple(line) for line in shape_str[1:]) for shape_str in shapes_str]
for shape in shapes:
    variants = {
        shape,
        rot(shape),
        rot(rot(shape)),
        rot(rot(rot(shape))),
        flipy(shape),
        rot(flipy(shape)),
        rot(rot(flipy(shape))),
        rot(rot(rot(flipy(shape)))),
    }
    print("\n".join("".join(s) for s in shape))
    print(len(variants))
p1 = 0
for width, height, *counts in sectionints[-1]:
    used = 0
    for shape, count in zip(shapes, counts):
        variants = {
            shape,
            rot(shape),
            rot(rot(shape)),
            rot(rot(rot(shape))),
            flipy(shape),
            rot(flipy(shape)),
            rot(rot(flipy(shape))),
            rot(rot(rot(flipy(shape)))),
        }
        blocks = sum(c == "#" for row in shape for c in row)
        used += count * blocks
    if width*height < used:
        # print(f"skip {width}x{height} {counts}")
        continue
    if width*height >= sum(count * 9 for count in counts):
        # print(f"trivial {width}x{height} {counts}")
        p1 += 1
        continue
    raise Exception(f"check {width}x{height} {counts}")
print(p1)
