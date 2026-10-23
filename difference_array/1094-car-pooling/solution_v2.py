# LeetCode 1094. 拼车（中等）
# 套路：差分数组（第二版：固定 1001 数组，但减号位置错 + 漏 0 号站）
# 2026-10-23
# 我的解答（官方用例能过，隐藏用例挂：提前一站下车、第 0 站没检查）

from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        diff = [0] * 1001                   # 用题目上界，解决越界问题
        for k, L, R in trips:
            diff[L] += k
            diff[R - 1] -= k                # 错：乘客在 R 站下车，不是 R-1 站
        for i in range(1, 1001):            # 错：从 1 开始，第 0 站永远不检查
            diff[i] += diff[i - 1]
            if diff[i] > capacity:
                return False
        return True


if __name__ == "__main__":
    s = Solution()

    # 两个官方用例碰巧都对，掩盖了问题
    assert s.carPooling([[2, 1, 5], [3, 3, 7]], 4) is False
    assert s.carPooling([[2, 1, 5], [3, 5, 7]], 4) is True

    # 下面断言的是「本版实际输出的错误结果」，正是 WA 的证据
    assert s.carPooling([[2, 1, 5], [3, 4, 6]], 4) is True
    print("反面演示 ✓ [[2,1,5],[3,4,6]] 返回 True，正确答案应为 False")
    print("           第 4 站：第一单还在车上(2) + 第二单刚上车(3) = 5 > 4")

    assert s.carPooling([[3, 0, 1]], 2) is True
    print("反面演示 ✓ [[3,0,1]] 返回 True，正确答案应为 False")
    print("           第 0 站就有 3 个人，但循环从 i=1 开始，压根没看第 0 站")


# 踩坑记录：
# 1. diff[R - 1] 是错的，应该是 diff[R]。乘客在 R 站下车，所以 R 站那一刻车上已经没有他们。
#    写成 R-1 等于让人提前一站下车，会少算「R-1 到 R 之间」这段的负载。
#    反例 [[2,1,5],[3,4,6]] capacity=4：第一单 1→5，第 4 站还在车上，
#    与第二单的 3 人叠加是 5 人，本版只算出 3 人，误判通过。
# 2. 循环从 i=1 开始是抄 LC1109 的惯性。但 1109 里下标 0 是哨兵（没有实际航班），
#    而 1094 的站点编号本身就从 0 起算，from 可以等于 0，第 0 站必须检查。
#    [[3,0,1]] capacity=2 就是活证据。
# 3. 关于「为什么 1109 要 R，1094 也是 R，但一个减 1 一个不减」：
#    1109 是 1-based 航班号 → 数组 0-based，起点要 L-1，终点 [L,R] 闭区间推到 R+1
#    再用 0-based 表达正好是 R；1094 站点编号直接用，L 和 R 都不用动。
#    表面上两题代码一样，理由却相反，不能盲目搬运。
# 4. 修正版见 solution_v3.py。
