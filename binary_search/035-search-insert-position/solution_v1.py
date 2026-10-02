# LeetCode 35. 搜索插入位置（简单）
# 套路：闭区间二分（LC704 模板复用），找不到时 return left 即插入位置，O(log n) 时间 / O(1) 空间
# 2026-10-02
# 我的解答

from typing import List


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        # 与 LC704 完全相同的闭区间二分 [left, right]
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid          # 找到了，返回下标（题目保证元素不重复）
            elif nums[mid] < target:
                left = mid + 1      # mid 及其左边都 < target，去右半边
            else:
                right = mid - 1     # mid 及其右边都 > target，去左半边
        # 唯一区别：没找到时不返回 -1，返回 left = 应插入的位置
        return left


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.searchInsert([1, 3, 5, 6], 5) == 2
    assert s.searchInsert([1, 3, 5, 6], 2) == 1
    assert s.searchInsert([1, 3, 5, 6], 7) == 4   # 插入末尾
    # 边界用例
    assert s.searchInsert([1], 0) == 0            # 比所有元素都小 → 插到开头
    assert s.searchInsert([1], 2) == 1            # 比所有元素都大 → 插到末尾
    assert s.searchInsert([1, 3], 2) == 1         # 落在两元素缝隙之间
    assert s.searchInsert([1, 3], 3) == 1         # 等于末尾元素
    assert s.searchInsert([2, 4, 6], 1) == 0      # 开头插入
    print("全部用例通过 ✓")

# 踩坑记录：
# 本题一次 AC，无踩坑。记录几个关键认知：
# 1. 与 LC704 唯一的代码区别在最后一行：return -1 → return left。
#    模板一行不改，只改「找不到时返回什么」——这就是闭区间二分模板的复用价值。
# 2. 为什么循环结束时 left 恰好是插入位置？
#    循环不变量：进入循环前始终有
#      [0, left-1] 里的元素全部 < target（只有 nums[mid] < target 才会 left = mid+1）
#      [right+1, n-1] 里的元素全部 > target（只有 nums[mid] > target 才会 right = mid-1）
#    循环结束 left = right + 1，此时 left 左边全 < target、右边全 > target，
#    且数组里没有 target（等于的情况已提前 return）→ left 正是第一个 > target 的下标。
# 3. 两个极端自动覆盖，无需特判：
#    target 比所有元素都小 → left 一路被推到 0；比所有都大 → left 最终 = len(nums)。
# 4. 这就是标准库 bisect.bisect_left(nums, target) 的手写版
#    （无重复元素时二者完全等价；有重复时 bisect_left 返回最左插入点）。
#    生产代码里直接 import bisect 更稳，面试/刷题要会手写。
