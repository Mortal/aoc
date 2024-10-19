from aoc import inp

nums = inp.split()
nn = [0] * len(nums[0])
mm = [0] * len(nums[0])
for line in nums:
    for i, c in enumerate(line):
        nn[i] += 1
        mm[i] += int(c)
gamma = int("".join([str(int(2*a > b)) for a, b in zip(mm, nn)]), 2)
epsilon = int("".join([str(int(2*a <= b)) for a, b in zip(mm, nn)]), 2)
print(gamma*epsilon)

nums = inp.split()
for i in range(len(nums[0])):
    print(len(nums))
    n = sum(w[i] == "1" for w in nums)
    if 2*n >= len(nums):
        nums = [n for n in nums if n[i] == "1"]
    else:
        nums = [n for n in nums if n[i] == "0"]
    if len(nums) == 1:
        a = int(nums[0], 2)
        print("first", a)
        break

nums = inp.split()
for i in range(len(nums[0])):
    n = sum(w[i] == "1" for w in nums)
    if 2*n >= len(nums):
        nums = [n for n in nums if n[i] == "0"]
    else:
        nums = [n for n in nums if n[i] == "1"]
    if len(nums) == 1:
        b = int(nums[0], 2)
        print("second", b)
        break
print(a*b)
