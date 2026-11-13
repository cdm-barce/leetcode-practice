# LeetCode 213. 打家劫舍 II（中等）
# 套路：环形拆分 + 线性 DP（滚动变量），max(rob(0..n-2), rob(1..n-1))，O(n) 时间 / O(1) 空间
# 2026-11-13
# 优化版（v2 空间压缩，逻辑与 v1 完全一致）


from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        """
        :param nums: 环形排列的每间房现金
        :return: 不触发报警能偷到的最大金额

        与 v1 的唯一区别：线性部分不再开 dp 数组，改用两个滚动变量。
        因为 dp[i] 只依赖 dp[i-1] 和 dp[i-2]，更早的格子用完就再也用不到。
        """
        def _linear(a: List[int]) -> int:
            # prev2 对应 dp[i-2]，prev1 对应 dp[i-1]
            # 初值都给 0，相当于在数组前垫了两间「金额为 0 的空房」，
            # 于是空数组返回 0、单元素返回 a[0]，边界自动处理，不用特判
            prev2 = prev1 = 0

            for x in a:
                # 元组同时赋值：右边两个值先一起算好再赋给左边，
                # 所以 max 里的 prev2 还是旧值，不会被左边的赋值污染
                # 含义：max(不偷本间 = prev1, 偷本间 = prev2 + x)
                prev2, prev1 = prev1, max(prev1, prev2 + x)

            return prev1

        n = len(nums)

        # 环形约束：首尾两间相邻，最优解里不可能同时被偷，因此二分情况
        if n == 1:
            return nums[0]

        # 情况 A：不偷最后一间    情况 B：不偷第一间
        return max(_linear(nums[:-1]), _linear(nums[1:]))


if __name__ == "__main__":
    s = Solution()

    assert s.rob([2, 3, 2]) == 3
    assert s.rob([1, 2, 3, 1]) == 4
    assert s.rob([5]) == 5
    assert s.rob([2, 1]) == 2
    assert s.rob([0]) == 0
    assert s.rob([0, 0]) == 0
    assert s.rob([1, 2, 3]) == 3
    assert s.rob([2, 7, 9]) == 9
    assert s.rob([2, 1, 1, 2]) == 3
    assert s.rob([1, 2, 3, 1, 2]) == 5
    assert s.rob([200, 3, 140, 20, 10]) == 340

    # ---------- 与 v1 数组版逐例对拍 ----------
    def rob_v1(nums):
        def _linear(a):
            if len(a) == 1:
                return a[0]
            dp = [0] * len(a)
            dp[0] = a[0]
            dp[1] = max(a[0], a[1])
            for i in range(2, len(a)):
                dp[i] = max(dp[i - 1], dp[i - 2] + a[i])
            return dp[-1]

        n = len(nums)
        if n == 1:
            return nums[0]
        return max(_linear(nums[:-1]), _linear(nums[1:]))

    import random
    random.seed(7)
    for _ in range(2000):
        k = random.randint(1, 12)
        arr = [random.randint(0, 50) for _ in range(k)]
        assert s.rob(arr) == rob_v1(arr), f"两版不一致：{arr}"

    # ---------- 与暴力枚举对拍（环形基准） ----------
    def brute(nums):
        n = len(nums)
        if n == 1:
            return nums[0]
        best = 0
        for mask in range(1 << n):
            picked = [i for i in range(n) if mask >> i & 1]
            # 环形相邻判定：(i+1) % n 覆盖首尾
            if all((i + 1) % n not in picked for i in picked):
                best = max(best, sum(nums[i] for i in picked))
        return best

    for _ in range(1000):
        k = random.randint(1, 9)
        arr = [random.randint(0, 30) for _ in range(k)]
        assert s.rob(arr) == brute(arr), f"与暴力解不一致：{arr}"

    print("全部用例通过 ✓（含 2000 组 v1 对拍 + 1000 组暴力对拍）")


# 踩坑记录
# 1. 【并发赋值】prev2, prev1 = prev1, max(prev1, prev2 + x) 必须写在一行。
#    拆成两行的话，第一行先把 prev2 覆盖成 prev1 的旧值，第二行的 max 里用的 prev2
#    就变成了新值，等于「偷本间」用了错的历史最优，结果会偏大。
# 2. 【哨兵初值】prev2 = prev1 = 0 让 _linear 天然支持空数组和单元素，
#    于是 v1 里 `if len(a) == 1` 那个特判可以删掉。代价是概念上多垫了两间空房。
# 3. 【何时能滚动】判据是看递推式里最远用到前几项——本题线性部分用到前 2 项，
#    所以 2 个变量即可；LC121 只用到「历史最低价」1 项，1 个变量就够。
# 4. 空间压到 O(1) 后无法打印 dp 表调试，所以一定先用 v1 把逻辑跑对，再来压缩。
# 5. 【环形不是递推问题】213 的难点不在递推，而在「首尾相邻」这个约束怎么消掉。
#    答案是把环形拆成两条线性链（各自排除一端），而不是在递推式里加条件。
