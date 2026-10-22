# LeetCode 1109. 航班预订统计（中等）
# 套路：差分数组（区间加 → 两端打标记 + 前缀和还原），O(n+m) 时间 / O(n) 空间
# 2026-10-22
# 最优代码

from typing import List


class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        # diff[i] 记录「第 i+1 号航班相比前一站，座位数变了多少」
        # 开 n+1 格：区间右端 R 可以等于 n，减号要落在下标 n，只开 n 格会 IndexError
        diff = [0] * (n + 1)

        for L, R, k in bookings:        # 序列解包，一次取出左端、右端、座位数
            diff[L - 1] += k            # 起点：从 L 号航班起多 k 个（1-based 转 0-based，故减 1）
            diff[R] -= k                # 终点后一站：R 号之后不再算这笔（0-based 下正好是下标 R）

        # 原地做前缀和：把「变化量」累加成「当前总量」
        # 从 1 开始，因为 0 号左边没有格子；写成 range(0, n) 会让 diff[-1] 取到哨兵格，静默全错
        for i in range(1, n):
            diff[i] += diff[i - 1]

        return diff[:n]                 # 切片丢掉最后那格哨兵


if __name__ == "__main__":
    s = Solution()

    # 官方用例
    assert s.corpFlightBookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5) == [10, 55, 45, 25, 25]

    # 边界：只有一个航班，区间退化成单点
    assert s.corpFlightBookings([[1, 1, 5]], 1) == [5]

    # 边界：区间右端顶到 n，验证哨兵格没越界
    assert s.corpFlightBookings([[1, 3, 7]], 3) == [7, 7, 7]

    # 边界：两条区间落在同一个单点上，验证 += / -= 的累加语义
    assert s.corpFlightBookings([[1, 1, 1], [1, 1, 2]], 2) == [3, 0]

    # 边界：同一航班被多单叠加
    assert s.corpFlightBookings([[1, 3, 1], [2, 3, 1], [3, 3, 1]], 3) == [1, 2, 3]

    # 边界：所有区间都不覆盖 1 号之后的某些航班，验证 0 值正确保留
    assert s.corpFlightBookings([[1, 1, 9], [5, 5, 4]], 5) == [9, 0, 0, 0, 4]

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 第一版（solution_v1.py）给每一单开一整行，O(m·n) 空间直接 MLE，40/83。
#    换差分后同样的测试数据从「爆内存」变成 27 ms / 30 MB。
# 2. 差分数组要开 n+1 格。R 最大取到 n，减号位置就是下标 n，只开 n 格必越界。
# 3. 前缀和循环必须从 i=1 开始。写 range(0, n) 时第一轮就是 diff[0] += diff[-1]，
#    Python 的 -1 取的是最后一个元素（哨兵格），结果从第一个数就错、且不抛异常。
# 4. 起点 diff[L-1] 与终点 diff[R] 看着不对称，其实是同一套换算：
#    闭区间 [L, R] 在 0-based 下标下是 [L-1, R-1]，区间外的第一格自然就是 R。
# 5. 用 += 和 -= 而不是 =，因为同一位置可能被多单命中，必须累加。
# 6. 一句话记忆：区间加数 = 开头记 +k，结尾后一格记 -k，最后从头到尾累加一遍。
#    同类题：LC1094 拼车（上车 +k、下车 -k，完全同构）。
