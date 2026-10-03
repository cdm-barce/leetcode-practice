# LeetCode 34. 在排序数组中查找元素的第一个和最后一个位置（中等）
# 套路：两段闭区间二分——左端点用「下取整 mid + R=mid」，右端点用「上取整 mid + L=mid」，O(log n) 时间 / O(1) 空间
# 2026-10-03
# 我的解答（AC，0ms 击败 100%）

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # 空数组守卫：nums 为空时后面的 nums[ans[0]] 会越界，入口提前拦掉
        if not nums:
            return [-1, -1]

        # 第一段：找「第一个 >= target」的位置（左端点）
        L, R = 0, len(nums) - 1
        while L < R:
            mid = (L + R) // 2          # 下取整：配合 R = mid 保留候选，避免死循环
            if nums[mid] >= target:
                R = mid                 # mid 可能是答案，向左压（不丢 mid）
            else:
                L = mid + 1             # mid 及其左边都 < target，直接跳过
        # 循环结束 L == R，即左端点（第一个 >= target 的下标）
        left = L

        # 第二段：找「最后一个 <= target」的位置（右端点）
        L, R = 0, len(nums) - 1
        while L < R:
            mid = (L + R + 1) // 2      # 上取整：配合 L = mid 保留候选，避免死循环
            if nums[mid] <= target:
                L = mid                 # mid 可能是答案，向右压（不丢 mid）
            else:
                R = mid - 1             # mid 及其右边都 > target，直接跳过
        # 循环结束 L == R，即右端点（最后一个 <= target 的下标）
        right = L

        # 校验：left 处的值是否真的是 target（target 可能根本不在数组里）
        if nums[left] != target:
            return [-1, -1]
        return [left, right]


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert s.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert s.searchRange([], 0) == [-1, -1]
    # 边界用例
    assert s.searchRange([1], 1) == [0, 0]              # 单元素且命中
    assert s.searchRange([1], 0) == [-1, -1]            # 单元素未命中
    assert s.searchRange([8, 8, 8, 8], 8) == [0, 3]     # 全相等，端点分居两侧
    assert s.searchRange([1, 2, 3], 2) == [1, 1]        # target 只出现一次
    assert s.searchRange([2, 2], 2) == [0, 1]           # 两个元素全命中（上取整关键用例）
    assert s.searchRange([1, 2, 3, 4, 5], 5) == [4, 4]  # target 在末尾
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 【核心认知】二分「命中就 return」拿到的是任意一个 target，不是端点。
#    找端点 = 命中时记录 mid 并继续定向收缩，靠区间不变量把答案逼出来：
#      左端点 = 第一个 >= target 的位置；右端点 = 最后一个 <= target 的位置。
# 2. 【死循环规律】谁被保留，mid 就避开谁：
#      R = mid（mid 可能成为新右界）→ mid 下取整 (L+R)//2；
#      L = mid（mid 可能成为新左界）→ mid 上取整 (L+R+1)//2。
#    本质：区间只剩 2 个元素时，若 mid 恰好等于被赋值的那一端，区间就不动 → 死循环。
# 3. 【上取整别写错】(L+R)//2 + 1 不是上取整：L+R 为偶数时会多跳一格
#    （如 L=0,R=2 时算成 2，标准上取整是 1）。正确写法是 (L+R+1)//2。
# 4. 【空数组】nums=[] 时两段 while 都跳过，ans 保持 [-1,-1]，
#    但结尾 `nums[ans[0]]` 即 nums[-1] 会 IndexError。入口 `if not nums` 提前返回。
# 5. 【边界判断顺序】`nums[L_] == target and L_ >= 0` 会先执行 nums[L_]，
#    L_=-1 时 nums[-1] 取尾部元素；应把 `L_ >= 0` 放前面利用短路求值。
# 6. 【最优解】手写两段二分是面试要求；生产代码用标准库
#      bisect_left(nums, target) / bisect_right(nums, target) 一行等价（见 v3）。
