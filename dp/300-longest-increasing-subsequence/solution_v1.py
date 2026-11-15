# LeetCode 300. 最长递增子序列（中等）
# 套路：线性 DP，dp[i] = 以 nums[i] 结尾的 LIS 长度，O(n²) 时间 / O(n) 空间
# 2026-11-15
# 我的解答（v1，双层循环枚举「上一个接谁」）


from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        :param nums: 整数数组
        :return: 最长严格递增子序列的长度（子序列不要求连续，但相对顺序不变）

        状态定义：dp[i] = 以 nums[i] 作为最后一个元素的 LIS 长度。
        注意「以 i 结尾」这四个字必须咬死 —— 它意味着 nums[i] 一定被选中。
        所以答案不是 dp[-1]，而是 max(dp)，因为最长的那个序列
        可能结尾在任何位置（比如 [1,2,3,0] 的最优解结尾在下标 2）。

        转移：枚举 nums[i] 前面所有比它小的元素 j，
        把 nums[i] 接在「以 j 结尾的最优序列」后面，长度就是 dp[j] + 1。
        所有可接的 j 里取最大。
        """
        n = len(nums)
        if n == 0:
            return 0

        # 每个元素自己单独就能构成一个长度为 1 的递增子序列，所以初值全 1。
        # （若初始化为 0，则「谁都不接」的情况会算成 0 而不是 1）
        dp = [1] * n

        for i in range(1, n):
            for j in range(i):
                # 严格递增：必须 nums[j] < nums[i]，等于也不算（不能写成 <=）
                if nums[j] < nums[i]:
                    # 保留最大值，不能直接 dp[i] = dp[j] + 1
                    # 因为不同的 j 会给出不同长度，要挑最长的那个接
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4, "示例1：[2,3,7,101] 或 [2,3,7,18]"
    assert s.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4, "示例2：[0,1,2,3]"
    assert s.lengthOfLIS([7, 7, 7, 7, 7, 7, 7, 7, 7]) == 1, "示例3：全相等，严格递增只能取 1 个"

    # 边界
    assert s.lengthOfLIS([1]) == 1, "单元素"
    assert s.lengthOfLIS([2, 2]) == 1, "两个相等元素，不能同时选"
    assert s.lengthOfLIS([1, 2, 3, 4, 5]) == 5, "完全递增：整个数组"
    assert s.lengthOfLIS([5, 4, 3, 2, 1]) == 1, "完全递减：只能取 1 个"

    # 关键用例：验证「dp[-1] 不等于答案」
    # [1,2,3,0] 的最优解 [1,2,3] 结尾在下标 2，而 dp[-1] 对应的是 0，只有 1
    assert s.lengthOfLIS([1, 2, 3, 0]) == 3, "答案不能取 dp[-1]"

    # 反例：验证「先找全局最小值再往右贪心」是错的（踩坑记录第 1 条）
    # 全局最小值 0 在末尾附近，从它出发只能得 [0,6] 长度 2；
    # 而 0 前面的 [1,2,3] 才是真正的宝藏，接上 6 得长度 4
    assert s.lengthOfLIS([4, 5, 1, 2, 3, 0, 6]) == 4, "从全局最小值出发会得到 2（错误）"

    # ---------- 与暴力枚举对拍（子序列最多 2^n 种，n 取小值） ----------
    def brute(nums):
        n = len(nums)
        best = 0
        for mask in range(1 << n):
            seq = [nums[i] for i in range(n) if mask >> i & 1]
            if all(seq[k] < seq[k + 1] for k in range(len(seq) - 1)):
                best = max(best, len(seq))
        return best

    import random
    random.seed(300)
    for _ in range(600):
        k = random.randint(1, 10)
        arr = [random.randint(-20, 20) for _ in range(k)]
        assert s.lengthOfLIS(arr) == brute(arr), f"与暴力解不一致：{arr}"

    print("全部用例通过 ✓（含 600 组暴力对拍）")


# 踩坑记录
# 1. 【贪心思路不成立】优化这题时最先想到的是「先找整个数组的最小值当起点，
#    然后在它右边反复找『大于当前值的最小值』接上去」。这个贪心在给定起点时是对的
#    （结尾越小，后面越容易接），但**起点选错就全盘皆输**：
#    反例 [4,5,1,2,3,0,6]，全局最小值 0 在倒数第二个，从它出发只能得到 [0,6] 长度 2，
#    而正确答案是 [1,2,3,6] 长度 4 —— 因为最小值把前面的长序列全扔掉了。
#    教训：贪心前先问「我这个选择会不会排除掉更优的未来」，不能只看眼前。
# 2. 【dp 定义咬死「以 i 结尾」】这题最容易写错的是最后 return 什么。
#    如果 dp[i] 定义为「前 i 个元素里的 LIS 长度」，那 dp[i] 就没法递推了
#    （因为不知道 nums[i] 到底有没有被选中）。定义为「以 i 结尾」才能递推，
#    代价是最后必须取 max(dp) 而不是 dp[-1]。
#    验证用例：[1,2,3,0]，dp = [1,2,3,1]，max 是 3，而 dp[-1] 只有 1。
# 3. 【严格递增】判断条件必须是 nums[j] < nums[i]，写成 <= 就把相等元素也算进去了。
#    官方示例 3 全是 7，正好能测出这个错。
# 4. 【为什么不能直接赋值】写 dp[i] = dp[j] + 1 是错的，必须 max 比较。
#    因为 i 前面可能有好几个比它小的 j，各自给出的候选长度不同，要挑最长的。
# 5. range(1, n) 和 range(n) 等价：i=0 时内层 range(0) 是空循环，什么也不做。
#    写 range(1, n) 语义更清楚（第一个元素没有前驱可接）。
# 6. 【边界】题目约束保证 n >= 1，所以 max(dp) 不会崩；
#    如果哪天遇到允许空数组的变体，需要先判 n == 0 返回 0。
# 7. O(n²) 在本机实测 1274 ms（击败 47.55%），能过但离最优差得远。
#    优化方向见 solution_v2.py：把「每个起点都往后贪心」合并成
#    「一次遍历维护每种长度的最小结尾」，复杂度降到 O(n log n)。
