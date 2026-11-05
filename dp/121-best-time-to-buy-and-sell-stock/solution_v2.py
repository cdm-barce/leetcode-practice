# LeetCode 121. 买卖股票的最佳时机（简单）
# 套路：一次遍历 + 用「单位元」做初值，消除第一轮特判
# 2026-11-05
# 最优代码，O(n) 时间 / O(1) 空间（都是理论下界）

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float("inf")   # 初值取正无穷，第一轮自然被替换成 prices[0]
        profit = 0                 # 初值 0：一次都不交易时为 0
        for p in prices:
            min_price = min(min_price, p)      # 更新历史最低价
            profit = max(profit, p - min_price)  # 用今天的价减去历史最低
        return profit


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

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 核心逻辑只有两行：更新最低价、用当前价减最低价更新最大利润。
#    顺序是先更新 min_price 再算 profit——因为「今天卖出」用的最低价必须包含今天，
#    否则 prices[0] 这一天会算出负数（虽然 max 会兜住，但语义不对）。
# 2. 用 float('inf') 做初值是这题最关键的化简：
#    v1 因为初值选 0，不得不用 if i == 0 特判；换成 inf 后循环体完全统一。
#    **单位元初值**是通用技巧：
#       求和 → 0 ；求最大 → -inf ；求最小 → +inf ；求乘积 → 1
# 3. for p in prices 而不是 for i in range(len(prices))：
#    这里不需要下标，直接迭代值更快也更清楚。
# 4. 为什么不能「先算 profit 再更新 min_price」：
#    如果先算 profit 用的是「昨天为止的最低价」，那今天买入今天卖出（利润 0）没问题，
#    但今天创新低时 profit 会用到今天之前的低价——两种顺序结果都正确，
#    因为 p - min_price 在 p 是最低价时等于 0，max 不会受影响。
#    不过先更新 min_price 语义更自然（"今天之前含今天的最低价"）。
# 5. 变体思路见 solution_v3.py（Kadane 最大子段和）。
