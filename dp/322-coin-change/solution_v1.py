# LeetCode 322. 零钱兑换（中等）
# 套路：完全背包 DP，dp[i] = min(dp[i-c] + 1)，O(amount × n) 时间 / O(amount) 空间
# 2026-11-14
# 我的解答（v1，从贪心思路改过来的）


from typing import List


class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        :param coins: 硬币面额，每种数量无限
        :param amount: 目标金额
        :return: 凑出该金额的最少硬币数；凑不出返回 -1

        状态定义：dp[i] = 凑出金额 i 需要的最少硬币枚数。
        注意下标 i 是「金额」，不是「第几枚硬币」——这是和 198/213 最大的区别，
        那两个是沿数组位置递推，这个沿数值递推。

        转移思路：枚举「最后一枚硬币用的是哪一面额 c」，
        那么在此之前必须先凑出 i-c 元，所以 dp[i] = dp[i-c] + 1，
        对所有满足 c <= i 的面额取最小值。
        """
        n = len(coins)

        # 整体初始化成 inf：既表达「凑不出」，也保证 min 不会误选到 0
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0          # 凑 0 元不需要任何硬币，这是递推的起点

        for i in range(1, amount + 1):
            for j in range(n):
                # 守卫：面额大于当前金额时跳过。
                # 少了这一行，dp[i - coins[j]] 会变成 dp[-n]，Python 静默指向数组末尾
                if coins[j] <= i:
                    dp[i] = min(dp[i - coins[j]] + 1, dp[i])

        # inf 说明没有任何组合能凑出 amount
        return dp[amount] if dp[amount] != float("inf") else -1


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    assert s.coinChange([1, 2, 5], 11) == 3, "示例1：5+5+1"
    assert s.coinChange([2], 3) == -1, "示例2：只有 2 元，凑不出 3"
    assert s.coinChange([1], 0) == 0, "示例3：金额为 0"

    # 边界
    assert s.coinChange([1], 1) == 1
    assert s.coinChange([1], 2) == 2
    assert s.coinChange([5, 7], 1) == -1, "所有面额都大于金额"

    # 反例：贪心会给出错误答案的场景（本文件踩坑记录第 1 条）
    assert s.coinChange([1, 3, 4], 6) == 2, "贪心得 3（4+1+1），最优是 3+3"
    assert s.coinChange([1, 5, 6, 9], 11) == 2, "贪心得 3（9+1+1），最优是 5+6"
    assert s.coinChange([3, 7, 10], 14) == 2, "贪心直接判无解（拿 10 剩 4），最优是 7+7"

    # 极限数据：验证不会被 O(amount × n) 卡住
    assert s.coinChange([186, 419, 83, 408], 6249) == 20

    # 顺带核对 dp 表，和手推一致
    coins, amount = [1, 2, 5], 11
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    for i in range(1, amount + 1):
        for c in coins:
            if c <= i:
                dp[i] = min(dp[i], dp[i - c] + 1)
    assert dp == [0, 1, 1, 2, 2, 1, 2, 2, 3, 3, 2, 3], f"dp 表不对：{dp}"

    print("全部用例通过 ✓")


# 踩坑记录
# 1. 【贪心不成立】最初的思路是「面额从大到小，能用大的就用大的，再拿剩下的继续」。
#    这在生活里找零钱是对的（人民币面额有倍数设计，属于「规范币制」），但这题不保证。
#    反例：[1,3,4] 凑 6，贪心得 4+1+1=3 枚，最优是 3+3=2 枚；
#          [3,7,10] 凑 14，贪心拿 10 剩 4 凑不出，直接判无解，而 7+7=2 枚其实有解。
#    教训：题目给的 4 个官方示例恰好都能被贪心蒙对，必须自己构造反例才能验出来。
# 2. 【负索引】写成 dp[i] = min(dp[i - coins[j]] + 1, dp[i]) 而没有守卫，
#    当 coins[j] > i 时 i - coins[j] 变负数，dp[-n] 静默指向数组末尾的 0，
#    把正确答案挤掉。实测 [1,2,5] 凑 11 时 dp[3]、dp[4] 全被污染成 1。
#    修正：内层加 if coins[j] <= i。
#    （同类坑：198 里 dp[i-2] 在短数组时污染、162 里 nums[-1] 越界取值。）
# 3. 【循环漏一格】写成 for i in range(1, amount)，只算到 amount-1，
#    dp[amount] 永远是初值 0，最后直接返回 0。修正：range(1, amount + 1)。
# 4. 【返回值】dp[amount] 可能是 inf，必须转成 -1，否则返回的是 float。
# 5. 【初始化位置】一开始在循环里写 dp[i] = inf，虽然能跑，但「凑不出」这个语义
#    藏在循环里不清晰，且容易漏掉某格。改成整体 [inf]*(amount+1) 再单独 dp[0]=0。
# 6. 空间无法再压：dp[i] 依赖的是 i-c（c 有多个取值），不像 198 只依赖前两项，
#    所以 O(amount) 是必需空间，压不到 O(1)。
