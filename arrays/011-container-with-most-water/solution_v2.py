# LeetCode 11. 盛最多水的容器（中等）
# 套路：左右双指针 + 原地维护最大值，O(n) 时间 / O(1) 空间
# 2026-09-14
# 最优代码

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """返回两条竖线与 x 轴围成的最大面积。"""
        left = 0
        right = len(height) - 1
        max_area = 0

        while left < right:
            area = min(height[left], height[right]) * (right - left)
            max_area = max(max_area, area)

            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return max_area


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
# 当前面积受较短边限制。若左边更短，移动右边只会让宽度变小，而短边高度不会变大，
# 不可能得到更优面积，所以应移动左边；右边更短时同理。
#
# 踩坑记录：
# 1. 【空间浪费】逐轮保存面积会额外占用 O(n) 空间，直接维护最大值即可。
# 2. 【错误移动】不能固定移动某一侧；移动较长边无法突破当前较短边的高度限制。
# 3. 【断言写错】maxArea([0, 2, 0, 3]) 应为 4 而非 3（下标 1 与 3，2 × 2）。
#    测试失败时先用暴力解对拍定位是代码错还是预期错，别直接改代码去迁就错的预期。
