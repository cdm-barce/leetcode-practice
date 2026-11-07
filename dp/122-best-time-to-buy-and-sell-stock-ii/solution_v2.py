# LeetCode 122. 买卖股票的最佳时机 II（中等）
# 套路：贪心（把越界判断内化到循环范围，省掉每轮的 if）
# 2026-11-07
# 最优代码，O(n) 时间 / O(1) 空间

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        profit = 0
        for i in range(len(prices) - 1):      # 只到倒数第二个，prices[i+1] 天然不越界
            if prices[i + 1] > prices[i]:     # 上涨才赚，下跌不动
                profit += prices[i + 1] - prices[i]
        return profit


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 7
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
    assert s.maxProfit([1]) == 0
    assert s.maxProfit([1, 2]) == 1
    assert s.maxProfit([2, 1]) == 0
    assert s.maxProfit([2, 1, 2, 1, 0, 1, 2]) == 3
    assert s.maxProfit([3, 3, 3]) == 0

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 和 v1 的差别只有一处：`range(len(prices) - 1)` 替代了 `i <= len - 2` 的判断。
#    这是通用套路——**能写进循环范围的约束，就不要写进循环体的条件里**。
#    （LC45 里用 range(n-1) 省掉 n==1 特判，是同一个思路。）
# 2. 复杂度：每个相邻对看一次，O(n)；只用两个变量，O(1)。这是理论下界。
# 3. 「下跌不动」这一行看起来像"什么都不做"，实际是主动决策：
#    下跌区间里空仓，才不会被跌幅吃掉收益。
# 4. 为什么不能直接 return sum(prices[i+1]-prices[i])：
#    那会把下跌也加进去，等于"一直持有"，收益反而变小
#    （[7,1,5,3,6,4] 会得到 4-7 = -3）。
# 5. 一行写法见 solution_v3.py，但面试不建议——可读性换不来什么。
