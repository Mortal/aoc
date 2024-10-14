with open("d15.in") as fp:
    inp = fp.read()
if 0:
    inp = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"

def thehash(part: str) -> int:
    h = 0
    for c in part:
        h = (h + ord(c)) * 17 % 256
    return h

boxes = {}
for part in inp.strip().split(","):
    if "=" in part:
        label, fole_str = part.split("=")
        fole = int(fole_str)
    else:
        label = part.strip("-")
        fole = -1
    h = thehash(label)
    if fole >= 0:
        boxes.setdefault(h, {})[label] = fole
    else:
        boxes.get(h, {}).pop(label, None)
    print("After", part)
    for b in boxes:
        if boxes[b]:
            print("Box", b, boxes[b])
tot = 0
for b in boxes:
    for i, (label, fole) in enumerate(boxes[b].items()):
        v = (1 + b) * (1 + i) * fole
        print(label, v)
        tot += v
print(tot)
