# LeetCode 1094. 拼车（中等）
# 套路：差分数组（区间加 → 站点两端打标记 + 前缀和逐站判断），O(n + 1000) 时间 / O(1001) 空间
# 2026-10-23
# 最优代码

from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        # 题目给定 0 <= from < to <= 1000，直接开 1001 格，不用求 max，也不会越界
        diff = [0] * 1001

        for k, L, R in trips:           # [人数, 上车站, 下车站]
            diff[L] += k                # L 站上车：从这一站起车上多了 k 人
            diff[R] -= k                # R 站下车：R 站这一刻车上已经没有他们了

        for i in range(1001):           # 从 0 开始，from 可以等于 0，第 0 站也要查
            if i:                       # i=0 时左边无格；直接 diff[0] += diff[-1] 会取到末元素
                diff[i] += diff[i - 1]  # 原地前缀和：当前 = 自己 + 上一站累积
            if diff[i] > capacity:      # 任何一站超载就立刻返回，可提前剪枝
                return False

        return True


if __name__ == "__main__":
    s = Solution()

    # 官方用例 1：第 3 站 2+3=5 > 4
    assert s.carPooling([[2, 1, 5], [3, 3, 7]], 4) is False

    # 官方用例 2：第 5 站先下 2 人再上 3 人，峰值只有 3
    assert s.carPooling([[2, 1, 5], [3, 5, 7]], 4) is True

    # 隐藏用例：第 5 站 10+7=17 > 16
    assert s.carPooling([[7, 5, 6], [6, 7, 8], [10, 1, 6]], 16) is False

    # 边界：from 可以等于 0，第 0 站就要检查
    assert s.carPooling([[3, 0, 1]], 2) is False

    # 边界：下车时刻不能提前一站（v2 就是栽在这里）
    assert s.carPooling([[2, 1, 5], [3, 4, 6]], 4) is False

    # 边界：最小规模
    assert s.carPooling([[1, 0, 1]], 1) is True

    # 边界：刚好装满，不算超载
    assert s.carPooling([[4, 0, 2]], 4) is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 站点上界直接用题目给的 1000（开 1001 格），别自己 max 求半截。
#    v1 只取 max(from)，装不下 to，全部用例 IndexError。
# 2. 减号必须落在 diff[R]，不是 diff[R-1]。乘客在 R 站下车，R 站就不占座了。
#    提前一站会漏算「R-1 到 R」这段负载，[[2,1,5],[3,4,6]] 会误判通过。
# 3. 循环必须覆盖 i=0。站点编号从 0 起算，from 可以是 0；
#    但累加那一步要跳过 i=0，否则 diff[0] += diff[-1] 会取到最后一格（Python 负索引）。
#    `if i:` 这个写法同时满足了「检查第 0 站」和「跳过第一次累加」。
# 4. 和 LC1109 的对照（最容易混淆的点）：
#    1109 航班是 [L, R] 闭区间且编号 1-based → 起点 L-1、终点 R；
#    1094 站点编号直接是 0-based 且 R 站下车 → 起点 L、终点 R，都不减 1。
#    两题代码长得一模一样，但「为什么」完全相反，不能凭手感搬运。
# 5. 一句话记忆：区间加数 = 开头 +k、结尾后一格 -k，最后从头累加一遍。
