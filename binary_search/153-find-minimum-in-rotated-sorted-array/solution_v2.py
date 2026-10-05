# LeetCode 153. 寻找旋转排序数组中的最小值（中等）
# 套路：二分——和 nums[r] 比定位最小值，去特判精简版，O(log n) 时间 / O(1) 空间
# 2026-10-05
# 最优代码

from typing import List


class Solution:
    def findMin(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            mid = (l + r) // 2
            if nums[mid] > nums[r]:
                # mid 在大数段，最小值必在右侧
                l = mid + 1
            else:
                # mid 在小数段，最小值是 mid 或左边；mid 可能就是最小值，不能踢出
                r = mid
        return nums[l]   # 退出时 l == r


if __name__ == "__main__":
    s = Solution()
    assert s.findMin([3, 4, 5, 1, 2]) == 1
    assert s.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert s.findMin([11, 13, 15, 17]) == 11   # 未旋转：nums[mid]<nums[r] 恒成立，r 收缩到 0
    assert s.findMin([1]) == 1
    assert s.findMin([2, 1]) == 1
    assert s.findMin([1, 2]) == 1
    assert s.findMin([5, 1, 2, 3, 4]) == 1
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 相比 v1 删了两处冗余：开头特判、末尾 min(nums[l],nums[r])。
#    未旋转时 nums[mid] < nums[r] 恒成立，else 分支让 r 一路收缩到 0，循环自己兜住，
#    无需特判（脑内跑 [1,2,3]：mid=1 时 2>3?否→r=1；mid=0 时 1>3?否→r=0，退出返回 nums[0]=1）。
# 2. 退出时 l == r，两下标指向同一元素，直接 return nums[l]。
# 3. 元素互异所以没有 nums[mid] == nums[r] 的情况，用 if/else 即可（不必写 elif）。
#    ⚠️ 但别把这个模板原样带进 LC154（最小值 II，元素可重复）：那里会出现
#    nums[mid] == nums[r] 且无法判断方向，标准处理是 r -= 1（安全：即便 nums[r] 是最小值，
#    也有 nums[mid] 顶着，缩掉不丢解）。
