# LeetCode 162. 寻找峰值（中等）
# 套路：二分「验证 mid 是不是峰」+ index(max) 兜底，最坏 O(n) 时间 / O(1) 空间
# 2026-10-06
# 我的解答（能 AC，但有两处侥幸，见末尾踩坑记录）

from typing import List


class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        # 直接验证 mid 本身是不是峰：同时比较左右两个邻居
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[mid + 1] and nums[mid] > nums[mid - 1]:
                # 命中峰值，直接返回
                return mid
            elif nums[mid] < nums[mid + 1]:
                # 上坡：峰值在右边
                l = mid + 1
            else:
                # 下坡：峰值在左边（mid-1）
                r = mid - 1
        # 兜底：二分没收敛出结果时，直接线性找全局最大
        return nums.index(max(nums))


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.findPeakElement([1, 2, 3, 1]) == 2
    assert s.findPeakElement([1, 2, 1, 3, 5, 6, 4]) in (1, 5)
    # 边界用例
    assert s.findPeakElement([1]) == 0          # 单元素，自己就是峰
    assert s.findPeakElement([1, 2]) == 1       # 递增，末尾是峰
    assert s.findPeakElement([2, 1]) == 0       # 递减，开头是峰
    assert s.findPeakElement([6, 5, 4, 3, 7]) in (0, 4)  # 双峰，mid=0 处判定出错但兜底捞回
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. nums[-1] 负索引陷阱：题目定义 nums[-1] = -∞ 是「虚拟边界」，但 Python 里 nums[-1]
#    是真实的最后一个元素。mid=0 时 nums[mid-1] 判的是 nums[-1]=最后一个元素，语义已错。
#    [6,5,4,3,7] 中 mid=0 的 6 明明是峰（左邻是虚拟 -∞），却因 6>nums[-1]=7 为假而没 return。
# 2. 兜底 index(max) 是 O(n)：一旦触发，O(log n) 承诺破产。这题力扣不查复杂度所以能过，
#    面试官会揪。正确做法是「只比右邻」判定峰在哪半边，把虚拟边界藏进不变式（见 solution_v2）。
# 3. r = mid - 1 依赖 if-return 提前返回兜底，否则会跳过候选区间（下坡时 mid 本身可能仍是峰）。
