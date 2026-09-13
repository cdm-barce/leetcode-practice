# LeetCode 27. 移除元素（中等）
# 套路：快慢双指针覆盖法，slow = 下一个可写位置，O(n) 时间 / O(1) 空间
# 2026-09-13
# 我的解答（0ms 击败 100%）

from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        :param nums: 原地移除所有等于 val 的元素，顺序需保持
        :return k: 保留元素个数，nums 前 k 位为保留结果（后面随便留垃圾）
        """
        slow = 0                              # 循环不变量：nums[:slow] 全是已保留的元素
        for fast in range(len(nums)):         # fast 一路向右扫描
            if nums[fast] != val:             # 不等于 val → 该保留
                nums[slow] = nums[fast]       # 填进下一个空位（fast==slow 时是自己赋自己，无害）
                slow += 1                     # 空位右移
        return slow                           # 保留个数 = 空位最终落点


if __name__ == "__main__":
    s = Solution()

    def run(nums, val):
        n = nums[:]
        k = s.removeElement(n, val)
        return k, n[:k]

    assert run([3, 2, 2, 3], 3) == (2, [2, 2])                       # 官方示例 1
    assert run([0, 1, 2, 2, 3, 0, 4, 2], 2) == (5, [0, 1, 3, 0, 4])  # 官方示例 2，顺序保持
    assert run([], 0) == (0, [])                                     # 空数组
    assert run([1], 1) == (0, [])                                    # 单元素全删
    assert run([2], 3) == (1, [2])                                   # 单元素不删
    assert run([3, 3, 3], 3) == (0, [])                              # 全是要删的
    assert run([4, 5], 4) == (1, [5])                                # 删头元素
    assert run([-1, -2, -3], -2) == (2, [-1, -3])                    # 负数
    print("全部用例通过 ✓")


# 思路拆解
# - 这版和 26 题的差异只在 slow 的语义：26 里 slow 是「已去重前缀的末尾」，
#   先 slow += 1 再写入；27 里 slow 是「下一个可写位置」，先写入再 slow += 1。
#   差别的根源：26 题第一个元素天然合法（fast 从 1 起），27 题第一个位置是不是
#   空位要等判断完才知道（fast 从 0 起）。
# - 顺序天然保持：保留的元素按原顺序落位，正好满足 27 题判题器对 nums[:k] 的要求。
# - 为什么 27 用覆盖、283 用交换？27 只要求前 k 位对、后面是垃圾，覆盖即可；
#   283 要求尾部全补 0，交换后 0 自然沉到右边，一趟搞定。
#   题目对尾部的额外要求决定了用覆盖还是交换。
#
# 踩坑记录
# 1. 这题一次写对（0ms 击败 100%），是独立写对的第三道同族题（283 → 26 → 27/80）。
# 2. 官方还提供首尾对撞双指针写法（顺序可乱时更少搬动），见 solution_v2.py；
#    面试优先写本版：顺序保持、逻辑最简、边界最少。
