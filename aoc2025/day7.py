from aoc import mat

splits = {}
for i, j in mat.findall("^"):
    splits.setdefault(i, []).append(j)

(si, sj), = mat.findall("S")
places = {sj: 1}
p1 = 0
for i in range(len(mat)):
    newplaces = {}
    for j in places:
        if j in splits.get(i, []):
            newplaces[j-1] = newplaces.get(j-1, 0) + places[j]
            newplaces[j+1] = newplaces.get(j+1, 0) + places[j]
            p1 += 1
        else:
            newplaces[j] = newplaces.get(j, 0) + places[j]
    places = newplaces
print(p1)
print(sum(places.values()))
