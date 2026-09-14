# LeetCode 11. 盛最多水的容器（中等）
# 套路：左右双指针 + 面积列表，O(n) 时间 / O(n) 空间
# 2026-09-14
# 我的解答（正确解，保留以记录思路）

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """返回两条竖线与 x 轴围成的最大面积。"""
        if len(height) < 2:
            return 0

        left = 0
        right = len(height) - 1
        areas = []

        while left < right:
            if height[left] > height[right]:
                areas.append(height[right] * (right - left))
                right -= 1
            else:
                areas.append(height[left] * (right - left))
                left += 1

        return max(areas)


if __name__ == "__main__":
    solution = Solution()
    assert solution.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert solution.maxArea([1, 1]) == 1
    assert solution.maxArea([]) == 0
    assert solution.maxArea([5]) == 0
    assert solution.maxArea([4, 4, 4, 4]) == 12
    assert solution.maxArea([0, 2, 0, 3]) == 4                          # 下标 1(高 2) × 下标 3(高 3)，宽 2
    print("全部用例通过")


# 思路拆解
# 两个指针先放在最宽的两端。当前面积由较短的边决定，因此每次移动较短的一侧，
# 才有机会在宽度变小的同时换来更高的短边。
#
# 踩坑记录：
# 1. 【空间浪费】把每一轮面积保存到列表，最后再取最大值，额外占用 O(n) 空间。
#    只需要维护当前最大面积即可，见 solution_v2.py。
# 2. 【断言写错】这一条最初写成 assert maxArea([0, 2, 0, 3]) == 3，实际应为 4：
#    下标 1(高 2) 与下标 3(高 3) 围出 2 × 2 = 4。测试挂了先别急着改代码，
#    用暴力解 O(n²) 对拍 5 万组，确认是代码错还是预期值写错——这次是后者。
