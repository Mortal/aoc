from aoc import inp

c = 0
p = float("inf")
nums = list(map(float, inp.split()))
for n in nums:
    if n > p:
        c += 1
    p = n
print(c)
p = float("inf")
c = 0
for x, y, z in zip(nums, nums[1:], nums[2:]):
    n = x+y+z
    if n > p:
        c += 1
    p = n

print(c)
