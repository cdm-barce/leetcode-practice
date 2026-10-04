# LeetCode 33. 搜索旋转排序数组（中等）
# 套路：两趟二分——先找旋转点（最小元素下标），再在对应有序段里二分，O(log n) 时间 / O(1) 空间
# 2026-10-04
# 我的解答

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        # ---- 第一趟：找旋转点 k = 数组最小元素的下标（即"塌陷"后重新升序的起点）----
        # 旋转数组的最小值，就是旋转点。用闭区间二分，通过和 nums[-1]（最右元素）比较定位。
        l, r = 0, n - 1
        while l < r:
            mid = (l + r) // 2
            # 若 nums[mid] 比最右元素大，说明 mid 在"大数段"，最小值一定在 mid 右边
            if nums[mid] > nums[-1]:
                l = mid + 1
            else:
                # 否则 mid 在"小数段"，最小值是 mid 或 mid 左边
                r = mid
        k = l  # 旋转点（最小元素下标）

        # ---- 第二趟：在 [0, k) 或 [k, n) 两个有序段里挑一个做普通二分 ----
        # 先判断 target 落在哪一段（两段内部各自有序，用端点即可判断）
        if k == 0:
            # 数组未旋转（整体有序，没有"左段"），直接整段二分
            lo, hi = 0, n - 1
        elif target > nums[-1]:
            # target 比最右元素还大，只能落在左边的大数段 [0, k)
            lo, hi = 0, k - 1
        else:
            # target 落在右边的小数段 [k, n)
            lo, hi = k, n - 1

        # 普通二分，在选定的有序段里找 target
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert s.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert s.search([1], 0) == -1
    # 边界：未旋转、target 在左段/右段/两端、单元素命中
    assert s.search([4, 5, 6, 7, 0, 1, 2], 6) == 2   # target 在左段
    assert s.search([4, 5, 6, 7, 0, 1, 2], 2) == 6   # target 在最右
    assert s.search([1, 3, 5], 3) == 1               # 未旋转（k==0）
    assert s.search([1], 1) == 0                     # 单元素命中
    assert s.search([3, 1], 1) == 1                  # 两元素旋转
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 这版是"两趟二分"思路：先找旋转点 k，再在左段 [0,k) 或右段 [k,n) 里挑一段普通二分。
#    渐进复杂度同样是 O(log n)，但两次扫描、判断更多，LeetCode 实测 3ms（击败约 5.30%），
#    常数比一趟二分的标准解更大。
# 2. 关键认知：旋转数组的最小元素就是旋转点 k。找 k 的二分和"最小值"判定有关：
#    用 nums[mid] 与 nums[-1]（最右）比较，比最右大则 mid 在大数段、最小值在右边；
#    否则最小值在 mid 或左边。这跟一趟解法里"和 nums[l]/nums[r] 比端点"是同一套端点思想。
# 3. 第二趟挑段的条件要小心：k==0 表示数组根本没旋转（整体有序），此时左段为空，
#    必须直接整段二分，否则 hi = k-1 = -1 会越界。这是本思路最容易漏的边界。
#    【实测踩坑】初版写成 `if k == 0 or target < nums[k] or target > nums[-1]: lo,hi = 0,k-1`，
#    把 k==0 也归进了"左段"空区间 → [1,3,5] 找 3、[1] 找 1 都返回 -1（越界漏检）。
#    修正：k==0 单独处理、直接整段 [0,n) 二分；否则再用 target 与 nums[-1] 比较决定落在左段还是右段。
# 4. 进阶：这题更优的是"一趟二分"（见 solution_v2.py）——利用"旋转数组一刀切开必有一半有序"
#    的性质，每轮直接判断哪半有序、target 在不在里面，一轮扫描就能定位，代码更短、常数更小。
