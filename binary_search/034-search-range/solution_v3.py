# LeetCode 34. 在排序数组中查找元素的第一个和最后一个位置（中等）
# 套路：标准库 bisect 两行流——bisect_left 找左边界、bisect_right 找右边界，O(log n) 时间 / O(1) 空间
# 2026-10-03
# 最优代码（工程派）

from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # bisect_left(nums, target)：返回「第一个 >= target」的下标（= 左端点位置）
        left = bisect_left(nums, target)
        # 越界 或 该位置的值不是 target → target 根本不存在
        if left == len(nums) or nums[left] != target:
            return [-1, -1]
        # bisect_right(nums, target)：返回「第一个 > target」的下标，减 1 即右端点
        return [left, bisect_right(nums, target) - 1]


if __name__ == "__main__":
    s = Solution()
    assert s.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert s.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert s.searchRange([], 0) == [-1, -1]
    assert s.searchRange([1], 1) == [0, 0]
    assert s.searchRange([1], 0) == [-1, -1]
    assert s.searchRange([8, 8, 8, 8], 8) == [0, 3]
    assert s.searchRange([2, 2], 2) == [0, 1]
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. bisect_left / bisect_right 是二分查找的 C 实现，与手写两段二分一一对应：
#      bisect_left(nums, t)  ≡ 找第一个 >= t 的下标（v2 第一段）
#      bisect_right(nums, t) ≡ 找第一个 > t 的下标，减 1 即最后一个 <= t（v2 第二段）
# 2. 关键：bisect_left 不会帮你判断「找到了没」——它只返回插入点。
#    必须自己校验 `left == len(nums) or nums[left] != target` 才能排除「不存在」。
#    手写版的 `if nums[left] != target` 在这里对应同一个判断。
# 3. 生产/竞赛直接 import bisect；面试/刷题要能手写 v2 的两段二分（循环不变量讲清楚）。
