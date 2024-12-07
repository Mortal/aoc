import itertools
from aoc import lineints

# p1 = 0
p2 = 0
for ans, *nums in lineints:
    # print(ans, nums)
    for choices in itertools.product((0,1,2),repeat=len(nums)-1):
        a = nums[0]
        # ops = [str(a)]
        assert len(choices) == len(nums[1:])
        for n, o in zip(nums[1:], choices):
            if o == 0:
                a *= n
                # ops.append(f"*{n}")
            elif o == 1:
                a += n
                # ops.append(f"+{n}")
            elif o == 2:
                a *= 10 ** len(str(n))
                a += n
                # ops.append(f"||{n}")
        if a == ans:
            p2 += ans
            # print("".join(ops))
            break
print(p2)
