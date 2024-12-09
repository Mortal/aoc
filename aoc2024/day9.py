from aoc import inp

numbers = list(map(int, inp))
if len(numbers) % 2 == 0:
    numbers.pop()
i = 0
cksum = 0
pos = 0
end = len(numbers) - 1
remain = numbers[end]
while i < end:
    if i % 2 == 0:
        print("File", i//2, "pos", pos)
        for _ in range(numbers[i]):
            cksum += pos * (i // 2)
            pos += 1
    else:
        free = numbers[i]
        print("File", end // 2, "pos", pos)
        while free > 0:
            while remain > 0 and (free > 0 or i + 1 == end):
                cksum += pos * (end // 2)
                pos += 1
                remain -= 1
                free -= 1
            if remain == 0:
                end -= 2
                print("File", end // 2, "pos", pos)
                if end == i:
                    break
                remain = numbers[end]
    i += 1
print(cksum)

files = []
freespace = []
pos = 0
for i in range(0, len(numbers), 2):
    files.append((pos, numbers[i], i // 2))
    pos += numbers[i]
    if i + 1 < len(numbers):
        freespace.append((pos, numbers[i + 1]))
        pos += numbers[i + 1]
for fpos, flen in freespace:
    for i in range(len(files))[::-1]:
        pos, le, file = files[i]
        if pos < fpos:
            continue
        if le == flen:
            print("Move1", file, "from", pos, "to", fpos)
            files[i] = (fpos, le, file)
            break
        elif le < flen:
            print("Move2", file, "from", pos, "to", fpos)
            files[i] = (fpos, le, file)
            fpos += le
            flen -= le
        else:
            print("Stay", file, "at", pos, "because", flen, le)
print(files)
print(sum(a*i for pos, le, i in files for a in range(pos, pos + le)))
