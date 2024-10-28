from aoc import linetoks

def patterns_endswith(chars: str, pattern: str, i: int, j: int) -> bool:
    assert 0 <= i <= j <= len(chars)
    return j - i >= len(pattern) and all(chars[j - k] in ("?", pattern[-k]) for k in range(1, len(pattern) + 1))

totalsum = 0
chars: str
nums: list[int]
for chars, *nums in linetoks:
    chars = "?".join([chars]*5)
    nums = nums * 5
    dp: list[list[int]] = []
    # dp[i][j]: number of ways in which
    # chars[:i] can fit nums[:j],
    # ending on a #.
    for i in range(len(chars) + 1):
        dp.append([])
        for j in range(len(nums) + 1):
            if i == 0 and j == 0:
                dp[i].append(1)
            elif i == 0 or j == 0:
                dp[i].append(0)
            elif j == 1:
                num = nums[j - 1]
                if patterns_endswith(chars, "." * (i - num) + "#" * num, 0, i):
                    dp[i].append(1)
                else:
                    dp[i].append(0)
            else:
                num = nums[j - 1]
                assert isinstance(num, int), num
                dp[i].append(
                    sum(
                        dp[k][j - 1]
                        for k in range(0, i - num)
                        if patterns_endswith(chars, "." * (i - num - k) + "#" * num, k, i)
                    )
                )
    ans = sum(
        dp[i][len(nums)]
        for i in range(len(dp))
        if patterns_endswith(chars, "." * (len(chars) - i), 0, len(chars))
    )
    print(chars, nums, ans)
    totalsum += ans
print(totalsum)
