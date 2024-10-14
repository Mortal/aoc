import math

d = [
('zr', 'gc', 3852, 15688, 49100),
('zr', 'gc', 3852, 15711, 49156),
('zr', 'sz', 4092, 17368, 31680),
('zr', 'sz', 4092, 17398, 31721),
('zr', 'cm', 4090, 18895, 36268),
('zr', 'cm', 4090, 18924, 36309),
('zr', 'xf', 4072, 15383, 35469),
('zr', 'xf', 4072, 15409, 35518),
]

presses = math.lcm(*[x[2] + 1 for x in d[::2]])
# presses *= 2
print(presses)
ns = [x[2] for x in d[::2]]
lowlast = [x[3] for x in d[::2]]
low = [x[3] * (presses // x[2] - 1) for x in d[1::2]]
highlast = [x[4] for x in d[::2]]
high = [x[4] * (presses // x[2] - 1) for x in d[1::2]]
lowbutton = 4 * presses
assert presses > 2734524052920, presses
assert presses > 5469048105840, presses
