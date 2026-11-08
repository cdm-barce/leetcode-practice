# LeetCode 714. 买卖股票的最佳时机含手续费（中等）
# 套路：状态机 DP —— 另一种初值写法（第一天直接买入）
# 2026-11-08
# 变体写法：初值更直观，但要多处理"第一天"

class Solution:
    def maxProfit(self, prices: list[int], fee: int) -> int:
        hold = -prices[0] - fee   # 第一天就买入：欠买价 + 手续费
        free = 0                  # 第一天不买：现金 0

        for p in prices[1:]:      # 从第二天开始
            new_hold = max(hold, free - p - fee)
            new_free = max(free, hold + p)
            hold, free = new_hold, new_free

        return free


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([1, 3, 2, 8, 4, 9], 2) == 8
    assert s.maxProfit([1, 3, 7, 5, 10, 3], 3) == 6
    assert s.maxProfit([1, 2, 3, 4, 5], 0) == 4
    assert s.maxProfit([1], 0) == 0
    assert s.maxProfit([1, 2], 1) == 0
    assert s.maxProfit([1, 4, 2], 3) == 0
    assert s.maxProfit([2, 1, 4], 1) == 2
    assert s.maxProfit([2, 2, 2], 0) == 0

    print("全部用例通过 ✅")


# 踩坑记录：
# 1. 和 v2 的结果完全等价，区别只在「怎么表达初始状态」：
#    v2：hold = -inf，循环从第 0 天开始（-inf 表示"不可能"）
#    本版：hold = -prices[0] - fee，循环从第 1 天开始（第一天直接买入）
# 2. 本版的好处：初值是具体数字，调试时容易理解。
#    坏处：多一个"第 0 天"的特判思维，而且 prices[0] 要求数组非空
#    （题目保证 prices.length >= 1，所以安全）。
# 3. 为什么不能 hold = 0：0 表示"手里有股票但没花钱"，
#    这会让第一天就能凭空卖出赚钱，答案虚高（见 solution_v1.py 的实测轨迹）。
# 4. 通用建议：状态机 DP 更推荐 v2 的写法（初值用极值），
#    因为它不依赖"第 0 天"的具体含义，加更多状态时也不用逐个想初值。
# 5. 这题和 309（冷冻期）的差别：309 需要第三个状态"刚卖出"，
#    因为"卖完要等一天"这条约束，两个状态表达不了。
