# LeetCode 153. 寻找旋转排序数组中的最小值（中等）
# 套路：二分——和 nums[r] 比（而非 nums[l]），判断最小值在 mid 右还是 mid 及左，O(log n) 时间 / O(1) 空间
# 2026-10-05
# 我的解答

from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        # 特判：数组未旋转（整体有序）时，最小值就是最左元素，直接返回
        if nums[l] < nums[r]:
            return nums[0]

        while l < r:
            mid = (l + r) // 2
            # 关键：和 nums[r]（最右）比，而不是 nums[l]。
            # 若 mid 比最右大，说明 mid 落在"大数段"，最小值必在 mid 右侧 → 收缩左边界
            if nums[mid] > nums[r]:
                l = mid + 1
            else:
                # mid 在"小数段"，最小值是 mid 或 mid 左边；mid 本身可能就是最小值，不能踢出
                r = mid

        # 退出时 l == r，两个下标指向同一元素，取 min 兜底
        return min(nums[l], nums[r])


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.findMin([3, 4, 5, 1, 2]) == 1
    assert s.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert s.findMin([11, 13, 15, 17]) == 11   # 未旋转（触发特判）
    # 边界
    assert s.findMin([1]) == 1                  # 单元素
    assert s.findMin([2, 1]) == 1               # 两元素旋转
    assert s.findMin([1, 2]) == 1               # 两元素未旋转
    assert s.findMin([5, 1, 2, 3, 4]) == 1      # 最小值在偏左
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 和 LC33 同源（都是"旋转数组 + 二分"），但目标从"找 target"变成"找最小值"。
#    开头特判 `if nums[l] < nums[r]: return nums[0]` 正是复用 LC33 踩过的"未旋转数组"坑——
#    未旋转时最小值就是 nums[0]，提前返回省去二分。
# 2. 核心认知：为什么和 nums[r] 比、不能和 nums[l] 比？
#    - 和 nums[l] 比：nums[mid] > nums[l] 无法定位最小值。
#      [3,4,5,1,2] 中 mid=5>3，最小值在右；[1,2,3,4,5] 中 mid=3>1，最小值在左 → 区分不了。
#    - 和 nums[r] 比：mid > r → 最小值必在 mid 右侧（l = mid+1）；
#      mid < r → 最小值在 mid 及左侧（r = mid）。无歧义，是标准姿势。
# 3. 细节：mid < r 时是 r = mid 而不是 r = mid - 1，因为 mid 本身可能就是最小值
#    （如 [4,5,1,2,3] 中 mid 指到 1），踢掉会丢解。
# 4. 可精简点（见 solution_v2.py）：开头特判可省（未旋转时 nums[mid] < nums[r] 恒成立、
#    r 一路收缩到 0）；退出后 l==r，return min(nums[l],nums[r]) 可直接写成 nums[l]。
