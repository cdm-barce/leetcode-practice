# LeetCode 34. 在排序数组中查找元素的第一个和最后一个位置（中等）
# 套路：二分命中任意 target 后向两边线性扩展（死循环 + 返回错误值），O(log n) 最好 / O(n) 最坏
# 2026-10-03
# 我的解答（初版，含多轮 debug 过程，最终本版本仍为「半二分 + 线性扩展」）

from typing import List


class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        # 初版思路：先二分定位到任意一个 target，再向左右线性扩展找边界
        L, R = 0, len(nums) - 1
        while L < R:
            mid = (L + R) // 2
            if nums[mid] == target:
                break
            elif nums[mid] < target:
                L = mid + 1
            else:
                R = mid - 1

        L_, R = mid, mid
        while nums[L_] == target and L_ >= 0:
            L_ -= 1
        while nums[R] == target and R < len(nums):
            R += 1

        return [L_ + 1, R - 1]


if __name__ == "__main__":
    s = Solution()
    # 本版存在：死循环（外层 if 命中后 break 导致 mid 可能未赋值）、
    # 边界判断顺序错误（nums[L_] 在 L_=-1 时取到尾部元素）、返回值偏移 +1/-1 未补偿。
    # 下面断言的是「逻辑正确时应输出」的值，用于对照；本版实际无法通过，仅作反面留存。
    # 手动模拟 target=8：[5,7,7,8,8,10] 期望 [3,4]，本版会因 while 扩展逻辑得到错误边界。
    print("反面演示版本（死循环 + 边界错误），正确解见 v2/v3")
    print("期望 searchRange([5,7,7,8,8,10], 8) == [3, 4]")

# 踩坑记录：
# 1. 【死循环①】外层 while L < R 的命中分支里写 `break` 而不是 `return`——
#    当第一轮 mid 就命中 target 时直接跳出，但后续 `L_, R = mid, mid` 依赖 mid 一定被赋值，
#    若 while 一次都没进（len(nums) 极小）mid 未定义。更隐蔽的是：命中即 break 后，
#    mid 定位的只是「任意一个 target」，不是端点。
# 2. 【边界判断顺序】`while nums[L_] == target and L_ >= 0`：
#    and 是从左到右短路求值，先执行 `nums[L_]`，当 L_ 已经减到 -1 时，
#    Python 的 `nums[-1]` 取的是数组最后一个元素（负下标），若恰好等于 target，
#    判断不会短路，继续 L_ -= 1 一路越界到 -2、-3…… 应把 `L_ >= 0` 放前面。
# 3. 【返回值偏移】扩展循环的 `L_ -= 1` / `R += 1` 会让指针在退出时多走一格，
#    所以返回 `[L_ + 1, R - 1]` 才对；本版写 `[L_, R]` 是错的。
# 4. 【复杂度】最坏 O(n)（整个数组都是 target 时线性扩展扫全表），
#    不满足题目 O(log n) 期望 → 见 v2 纯二分、v3 bisect。
