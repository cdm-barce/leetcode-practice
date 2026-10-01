# LeetCode 704. 二分查找（简单）
# 套路：闭区间二分查找 [left, right]，O(log n) 时间 / O(1) 空间
# 2026-10-01
# 我的解答

from typing import List


class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # 闭区间写法：left/right 都是可取到的下标，搜索范围是 [left, right]
        left, right = 0, len(nums) - 1
        # 循环条件 left <= right：left == right 时区间还剩一个元素，也要检查
        while left <= right:
            # 中间下标，向下取整；Python 整数无溢出问题
            # （C/Java 里要写 left + (right - left) // 2 防 int 溢出）
            mid = (left + right) // 2
            if nums[mid] == target:
                return mid          # 命中，返回下标
            elif nums[mid] < target:
                left = mid + 1      # target 在右半边，mid 及其左边整体排除
            else:
                right = mid - 1     # target 在左半边，mid 及其右边整体排除
        return -1                   # 区间缩空（left > right），target 不存在


if __name__ == "__main__":
    s = Solution()
    # 官方示例
    assert s.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert s.search([-1, 0, 3, 5, 9, 12], 2) == -1
    # 边界用例：单元素（命中/不命中）、目标在两端、目标落在缝隙里
    assert s.search([5], 5) == 0
    assert s.search([5], -5) == -1
    assert s.search([1, 3, 5, 7], 1) == 0      # 目标是最左端
    assert s.search([1, 3, 5, 7], 7) == 3      # 目标是最右端
    assert s.search([1, 3, 5, 7], 0) == -1     # 比最小还小
    assert s.search([1, 3, 5, 7], 9) == -1     # 比最大还大
    assert s.search([2, 4], 3) == -1           # 落在两元素之间
    print("全部用例通过 ✓")

# 踩坑记录：
# 本题一次 AC，无踩坑。记录几个关键认知：
# 1. 循环不变量是「target 只可能出现在 [left, right] 里」。
#    每轮比较后把 mid 彻底排除（+1 / -1），区间每轮至少缩短一半，
#    最多 log2(n) 轮必然终止——这正是题目要求 O(log n) 的来源。
# 2. while 条件用 left <= right 而不是 left < right：
#    闭区间里 left == right 时还剩最后一个元素没检查，漏掉会 WA（如单元素数组）。
#    left < right 对应的是左闭右开 [left, right) 写法，两套模板不能混用。
# 3. mid = (left + right) // 2 在 Python 里不用防溢出，
#    但 C/Java 面试常问：要写成 left + (right - left) // 2。
# 4. n = 10000 时最多比较 log2(10000) ≈ 14 次——数据量翻 10 倍只多 3~4 次比较，
#    这就是对数复杂度的直观威力。
