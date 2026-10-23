# LeetCode 1094. 拼车（中等）
# 套路：差分数组 + itertools.accumulate 一行求前缀和，O(n + 1000) 时间 / O(1001) 空间
# 2026-10-23
# 最优代码（更短更快，但放弃提前退出）

from itertools import accumulate
from typing import List


class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        diff = [0] * 1001
        for k, L, R in trips:
            diff[L] += k            # L 站上车
            diff[R] -= k            # R 站下车

        # accumulate 是 C 层实现的前缀和，比手写 for 快；
        # 但它必须把所有元素都算出来，没法在中途「超载就返回」
        return max(accumulate(diff)) <= capacity


if __name__ == "__main__":
    s = Solution()

    assert s.carPooling([[2, 1, 5], [3, 3, 7]], 4) is False
    assert s.carPooling([[2, 1, 5], [3, 5, 7]], 4) is True
    assert s.carPooling([[7, 5, 6], [6, 7, 8], [10, 1, 6]], 16) is False
    assert s.carPooling([[3, 0, 1]], 2) is False
    assert s.carPooling([[2, 1, 5], [3, 4, 6]], 4) is False
    assert s.carPooling([[1, 0, 1]], 1) is True
    assert s.carPooling([[4, 0, 2]], 4) is True

    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 这一版和 v3 结果完全一致，区别只在性能取舍（实测 n=1000）：
#    - 不超载、扫满全程：accumulate 约 0.09 ms，手写 for 约 0.12 ms（C 层更快）
#    - 第 1 站就超载：手写 for 约 0.07 ms（能提前 return），accumulate 约 0.09 ms
#    结论：数据大概率超载、想尽早剪枝 → 用 v3；只求短和稳 → 用这一版。
# 2. max(accumulate(diff)) 只需遍历一次，额外空间是 O(1)（accumulate 返回生成器）。
# 3. 如果站点范围不是 1000 而是 1e9，固定数组就开不出来了，那时改用「排序扫描线」：
#        events = []
#        for k, L, R in trips:
#            events.append((L, k))       # 上车
#            events.append((R, -k))      # 下车
#        events.sort()
#        cur = 0
#        for _, delta in events:
#            cur += delta
#            if cur > capacity:
#                return False
#        return True
#    复杂度变成 O(n log n)。妙处在于同一站 sort 会把 -k 排在 +k 前面，
#    自动实现「先下车再上车」，正好符合「下车的人不占座」的语义。
