# LeetCode 198. 打家劫舍（中等）
# 套路：线性 DP + 滚动变量，只依赖前两项，O(n) 时间 / O(1) 空间
# 2026-11-12
# 优化版（v2 空间压缩，逻辑与 v1 完全一致）


from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        :param nums: 每间房内藏着的现金
        :return: 不触发报警能偷到的最大金额

        prev2 对应 v1 的 dp[i-2]，prev1 对应 dp[i-1]。
        两者初值都给 0，相当于在数组前面垫了两间「金额为 0 的空房」，
        于是 n == 1 的特殊判断可以整个删掉，从第一间房就开始套递推。
        """
        prev2 = prev1 = 0

        for x in nums:
            # 元组同时赋值：右边两个值先一起算好再一起赋给左边，
            # 所以 max 里的 prev2 还是旧值，不会被左边的赋值污染
            # 递推含义：max(不偷本间 = prev1, 偷本间 = prev2 + x)
            prev2, prev1 = prev1, max(prev1, prev2 + x)

        return prev1


if __name__ == "__main__":
    s = Solution()

    assert s.rob([1, 2, 3, 1]) == 4
    assert s.rob([2, 7, 9, 3, 1]) == 12
    assert s.rob([5]) == 5
    assert s.rob([5, 10]) == 10
    assert s.rob([0, 0, 0]) == 0
    assert s.rob([2, 1, 1, 2]) == 4
    assert s.rob([2, 100, 3]) == 100

    # 与 v1 数组版逐例对拍，确认两版结果完全一致
    def rob_v1(nums):
        n = len(nums)
        if n == 1:
            return nums[0]
        dp = [0] * n
        dp[0], dp[1] = nums[0], max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
        return dp[-1]

    import random
    random.seed(0)
    for _ in range(2000):
        k = random.randint(1, 12)
        arr = [random.randint(0, 50) for _ in range(k)]
        assert s.rob(arr) == rob_v1(arr), f"两版不一致：{arr}"

    print("全部用例通过 ✓（含 2000 组随机对拍）")


# 踩坑记录
# 1. 【并发赋值】prev2, prev1 = prev1, max(prev1, prev2 + x) 必须写成一行。
#    拆成两行的话，第一行先把 prev2 覆盖成 prev1 的旧值，第二行的 max 里用的 prev2
#    就变成了新值，等于「偷本间」用了错的历史最优，结果会偏大。
# 2. 【哨兵初值】prev2 = prev1 = 0 让循环从第 0 间房开始就不会越界，
#    代价是概念上多垫了两间空房。这是拿「下标干净」换「多一个哨兵」的取舍。
# 3. 【何时能滚动】判据是看递推式里最远用到前几项——198 用到前 2 项就用 2 个变量；
#    LC121 只用到「历史最低价」1 项，所以 1 个变量就够。
# 4. 空间压到 O(1) 后无法打印 dp 表调试，所以一定先用 v1 把逻辑跑对，再来压缩。
