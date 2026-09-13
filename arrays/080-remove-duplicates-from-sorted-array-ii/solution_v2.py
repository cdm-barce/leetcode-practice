# LeetCode 80. 删除有序数组中的重复项 II（中等）
# 套路：通用「保留至多 k 个」模板，一次写死 26 题（k=1）和 80 题（k=2）
# 2026-09-13
# 最优代码（v1 的一般化）

from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """80 题入口：每值最多保留 2 个。"""
        return self.keepAtMost(nums, 2)

    def keepAtMost(self, nums: List[int], k: int) -> int:
        """
        :param nums: 非严格递增数组
        :param k: 每个值最多保留的个数（k=1 即 LC26，k=2 即 LC80）
        :return: 保留个数，nums 前 k 位之后照常是垃圾
        """
        if len(nums) <= k:                    # 数组比 k 短：全保留，先堵边界
            return len(nums)
        slow = k                              # 前 k 个必然合法，直接收进前缀
        for fast in range(k, len(nums)):
            if nums[fast] != nums[slow - k]:  # 守门员 = 前缀倒数第 k 个已保留元素
                nums[slow] = nums[fast]
                slow += 1
        return slow


if __name__ == "__main__":
    s = Solution()

    def run(nums, k):
        n = nums[:]
        r = s.keepAtMost(n, k)
        return r, n[:r]

    assert s.removeDuplicates([1, 1, 1, 2, 2, 3]) == 5                 # 80 官方示例 1
    assert run([0, 0, 1, 1, 1, 1, 2, 3, 3], 2) == (7, [0, 0, 1, 1, 2, 3, 3])
    assert run([1, 1, 2], 1) == (2, [1, 2])                            # k=1 退化为 26 题
    assert run([0, 0, 1, 1, 1, 2, 2, 3, 3, 4], 1) == (5, [0, 1, 2, 3, 4])
    assert run([1, 1, 1, 1], 3) == (3, [1, 1, 1])                      # k=3，第 4 个被拦
    assert run([], 2) == (0, [])                                       # 边界早退
    assert run([1], 2) == (1, [1])                                     # 边界早退
    assert run([1, 2, 3], 2) == (3, [1, 2, 3])                         # 比守门员全不同
    print("全部用例通过 ✓")


# 思路拆解
# - 为什么守门员取 slow-k 就够？数组有序，前缀末尾的 k 个元素若都与 nums[fast] 不同，
#   则整个前缀中该值出现次数 < k，写入安全；前缀末尾连续 k 个相同则已达上限，跳过。
#   有序性是前提，无序数组必须先排序或换 set 计数。
# - 这个模板的价值：面试遇到「保留至多 k 个重复」这类抽象追问，改一个参数直接交。
#
# 踩坑记录
# 1. k 作为参数后，len(nums) <= k 的早退就是唯一需要的边界——
#   「数组比 k 短」和「k 比数组长的极端取法」一并覆盖。
# 2. 同族题对照表（都在本仓库）：
#    283 移动零：守门员是 != 0，用交换（尾部要补 0）
#    26 删重复项：守门员 nums[slow]，每值留 1 个
#    27 移除元素：守门员 nums[fast] != val，覆盖写入
#    80 删重复项 II：守门员 nums[slow-2]，每值留 2 个
