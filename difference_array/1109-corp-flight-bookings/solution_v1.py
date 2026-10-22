# LeetCode 1109. 航班预订统计（中等）
# 套路：二维矩阵逐单累加，O(m·n) 时间 / O(m·n) 空间
# 2026-10-22
# 我的解答（超内存 MLE，40/83 个用例通过）

from typing import List


class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        r = len(bookings)
        c = len(bookings[0])                    # 未使用：每行固定 3 个元素，本来想拿列数但没用上
        flight = [[0] * n for _ in range(r)]    # 致命点：给每一单都开一整行 n 格
        for i in range(r):
            L = bookings[i][0]
            R = bookings[i][1]
            orders = bookings[i][2]
            for j in range(L - 1, R):           # 把这一单覆盖到的航班逐个加上
                flight[i][j] += orders
        answer = []
        for i in range(n):
            total = 0
            for j in range(r):                  # 再按「列」把每单的贡献加起来
                total += flight[j][i]
            answer.append(total)
        return answer


if __name__ == "__main__":
    s = Solution()

    # 官方用例
    assert s.corpFlightBookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5) == [10, 55, 45, 25, 25]

    # 边界：只有一个航班，区间退化成单点
    assert s.corpFlightBookings([[1, 1, 5]], 1) == [5]

    # 边界：区间右端顶到 n
    assert s.corpFlightBookings([[1, 3, 7]], 3) == [7, 7, 7]

    # 边界：同一航班被多单命中
    assert s.corpFlightBookings([[1, 3, 1], [2, 3, 1], [3, 3, 1]], 3) == [1, 2, 3]

    print("全部用例通过 ✓（逻辑正确，但大数据会 MLE，见末尾踩坑记录）")


# 踩坑记录：
# 1. 逻辑完全正确，小用例全过，但提交后报「超出内存限制」40/83。
#    根因：flight = [[0] * n for _ in range(r)] 给每一单都存了一整行「各航班贡献」，
#    r 和 n 都能到 2e4，矩阵就是 4e8 个格子，光指针就 3 GB 起步。
#    本质错误是把「明细」当成了必要的中间状态——题目只要「每个航班的总量」。
# 2. c = len(bookings[0]) 定义了却没用，属于思考过程中的遗留变量，能删。
# 3. 时间上也不划算：先逐单填充 O(m·n)，再按列求和 O(m·n)，两次都白跑。
# 4. 正确方向见 solution_v2.py：差分数组，只在区间两端打标记，O(n+m)。
