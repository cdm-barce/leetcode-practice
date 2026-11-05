# LeetCode 121. 买卖股票的最佳时机（简单）
# 套路：一次遍历维护「历史最低价」
# 2026-11-05
# 我的解答（逻辑正确、复杂度最优，但写了一个多余的特判）

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        pro = 0                 # 建议改名 profit
        min_price = 0           # 问题根源：初值选 0
        for i in range(len(prices)):
            if i == 0:          # 多余的特判（因为初值选错了才需要）
                min_price = prices[i]
            else:
                min_price = min(min_price, prices[i])
            pro = max(prices[i] - min_price, pro)
        return pro


if __name__ == "__main__":
    s = Solution()

    # 官方示例 1：第 2 天买（1）第 5 天卖（6），利润 5
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5

    # 官方示例 2：一路下跌，不交易，利润 0
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0

    # 边界：只有一天，无法交易
    assert s.maxProfit([1]) == 0

    # 边界：先跌后涨
    assert s.maxProfit([2, 4, 1]) == 2

    # 边界：价格全相同
    assert s.maxProfit([3, 3, 3]) == 0

    # 边界：只有两天
    assert s.maxProfit([1, 2]) == 1
    assert s.maxProfit([2, 1]) == 0

    # 波动行情
    assert s.maxProfit([2, 1, 2, 1, 0, 1, 2]) == 2
    assert s.maxProfit([1, 4, 2]) == 3

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 算法本身已经最优：每个价格看一次 O(n)，只用两个变量 O(1)，双下界，没有更好的办法。
# 2. 唯一可改进的是代码结构：`if i == 0` 这个特判是多余的，根因是 min_price 初值选了 0。
#    价格都是正数，min(0, 任何价格) 永远是 0，所以只能靠特判绕过第一轮。
#    把初值改成 float('inf')，第一轮 min(inf, 7) 自然变成 7，特判就不需要了。
# 3. 通用规律：**需要给「第一轮」写特判时，先看看是不是初值没选好。**
#    单位元做初值（求和用 0、求最大用 -inf、求最小用 inf）能让循环体保持统一。
#    这条规律在动态规划里更重要。
# 4. 变量名 pro 容易误读成 professional，改成 profit 更清楚。
# 5. for i in range(len(prices)) + prices[i] 不如 for p in prices，只在需要下标时才用 range。
# 6. 优化版见 solution_v2.py，另一种思路（Kadane）见 solution_v3.py。
