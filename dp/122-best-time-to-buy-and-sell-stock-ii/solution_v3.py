# LeetCode 122. 买卖股票的最佳时机 II（中等）
# 套路：相邻差值 + 只取正数（一行写法）
# 2026-11-07
# 简洁版：代码最短，但可读性下降，面试不建议

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        # zip(prices, prices[1:]) 自动配对出所有相邻对 (a, b)
        # max(0, b - a) 等价于「涨了才算收益，跌了算 0」
        return sum(max(0, b - a) for a, b in zip(prices, prices[1:]))


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

    print("全部用例通过 ✅")


# 踩坑记录：
# 1. 两个技巧叠在一起：
#    ① zip(prices, prices[1:]) —— 把相邻元素配对成 (p0,p1), (p1,p2), ...
#       比 for i in range(len-1) 更直观，也不用手动取下标。
#    ② max(0, b - a) —— 把「涨了累加、跌了跳过」压缩成一个值，
#       省掉了 if。
# 2. 边界天然安全：prices 只有 1 个元素时，prices[1:] 是空列表，
#    zip 配不出任何对，sum 返回 0，正好是正确答案。
# 3. 为什么不推荐面试这么写：
#    - 面试官想看的是「你有没有想清楚为什么累加上涨最优」，
#      一行代码把这些思考全藏起来了；
#    - 万一面官追问「如果加手续费怎么改」，一行版很难直接改。
#    自己刷题、代码量大的时候用它可以省行数。
# 4. 时间复杂度仍是 O(n)，但生成器表达式 + zip 的常数比 for 循环略大，
#    数据量小的时候感知不到。
