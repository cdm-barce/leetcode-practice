# LeetCode 121. 买卖股票的最佳时机（简单）
# 套路：转成「相邻差值数组」，求最大子段和（Kadane 算法，即 LC53）
# 2026-11-05
# 思路对比版：逻辑正确，但常数略大，实际不如 v2 快

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        best = cur = 0
        for i in range(1, len(prices)):
            # 今天的涨跌 = prices[i] - prices[i-1]
            # cur 表示「以今天结尾的最大连续收益」，亏了就归零重新开始
            cur = max(0, cur + prices[i] - prices[i - 1])
            best = max(best, cur)
        return best


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
    assert s.maxProfit([1]) == 0
    assert s.maxProfit([2, 4, 1]) == 2
    assert s.maxProfit([3, 3, 3]) == 0
    assert s.maxProfit([1, 2]) == 1
    assert s.maxProfit([2, 1]) == 0
    assert s.maxProfit([2, 1, 2, 1, 0, 1, 2]) == 2
    assert s.maxProfit([1, 4, 2]) == 3

    print("全部用例通过 ✅")


# 踩坑记录：
# 1. 这题和 LC53（最大子数组和）是同一个问题，只是换了层皮：
#    「低买高卖的最大收益」 = 「所有相邻涨跌的最大连续子段和」
#    举例：[7,1,5,3,6,4] 的差值数组是 [-6, +4, -2, +3, -2]
#          最大连续子段和 = 4 + (-2) + 3 = 5，正是答案。
# 2. Kadane 的核心：cur = max(0, cur + 当天涨跌)
#    「如果到昨天为止的累计收益是负的，那不如从今天重新开始买」。
# 3. 为什么日常写这题不用这个版本：
#    - 每轮多算一次减法
#    - 要多维护一个变量 cur
#    - 同复杂度下常数更大
#    v2 的「维护最低价」是这题最直接的解法。
# 4. 但这个思路的价值在于：它能自然推广到「允许多次交易」的 LC122，
#    以及「最多 k 次交易」的 LC188（那时必须用 DP 而不是贪心）。
#    所以值得理解，不值得优先用。
