# LeetCode 714. 买卖股票的最佳时机含手续费（中等）
# 套路：状态机 DP（持有 / 空仓两个状态）
# 2026-11-08
# 我的解答（结构完全正确，但有两处 bug）

class Solution:
    def maxProfit(self, prices: list[int], fee: int) -> int:
        hold = 0                        # 错 1：初值应该是 -inf
        free = 0
        for i in range(len(prices)):
            new_hold = max(hold, free - prices[i] - 2)   # 错 2：写死了 2，没用 fee
            new_free = max(free, hold + prices[i])
            hold, free = new_hold, new_free
        return free


if __name__ == "__main__":
    s = Solution()

    # 下面断言的是「本版的实际输出」，用来保留 WA 证据
    assert s.maxProfit([1, 3, 2, 8, 4, 9], 2) == 11
    print("反面演示 ✓ [1,3,2,8,4,9] fee=2 返回 11，正确答案应为 8")

    assert s.maxProfit([1, 3, 7, 5, 10, 3], 3) == 10
    print("反面演示 ✓ [1,3,7,5,10,3] fee=3 返回 10，正确答案应为 6")

    print()
    print("两个 bug：")
    print("  ① fee 参数没用，写死了 2 —— 换个 fee 就全错")
    print("  ② hold 初值 0 —— 相当于'白送一只成本 0 的股票'，凭空造钱")


# 踩坑记录：
# 1. 结构完全正确：两个状态、new_ 临时变量同时更新、返回 free。
#    错的全在细节上，而且是「不报错、只算错」的那种。
# 2. Bug ①：`- 2` 写死了。函数签名里明明有 fee 参数，却没用上。
#    这类错误在 LeetCode 上表现为「部分用例通过、部分不过」，很难一眼看出。
# 3. Bug ②（致命）：hold = 0 的含义是「手里有股票，成本 0 元」。
#    于是第一天 new_free = max(0, 0 + prices[0]) = 1，
#    程序认为「我有一只免费的股票，今天卖了赚 1 块」——凭空造钱。
#    实测轨迹对比（[1,3,2,8,4,9], fee=2）：
#        hold=0     →  (hold, free) = (0, 1), (0, 3), (0, 3)…  最终 11（错）
#        hold=-inf  →  (-3, 0), (-3, 0), (-3, 0)…              最终 8（对）
# 4. 通用规律：**DP 里「不可能的状态」必须用极值表示，绝不能用 0。**
#    求最大且初始不可达 → -inf；求最小且初始不可达 → +inf。
#    这和 121 用 min_price = float('inf') 是同一个思路：单位元表示「还没开始」。
# 5. 为什么 hold 可以是负数：它表示「买入时欠的钱」，不是亏损。
#    hold = -3 的意思是「买股票花了 1 块 + 手续费 2 块，账上是 -3」。
# 6. 修复版见 solution_v2.py，另一种初值写法见 solution_v3.py。
