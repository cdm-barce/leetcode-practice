# LeetCode 80. 删除有序数组中的重复项 II（中等）
# 套路：快慢双指针 + 守门员 nums[slow-2]，每值最多保留 2 个，O(n) 时间 / O(1) 空间
# 2026-09-13
# 我的解答（176/176 通过）

from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        :param nums: 非严格递增数组，原地删除使每个元素最多出现两次
        :return k: 保留个数，nums 前 k 位为结果，后面是垃圾
        """
        if len(nums) <= 2:                    # 长度 ≤ 2 时任何值都不会超 2 个，全保留
            return len(nums)

        slow = 2                              # 前 2 个直接收进前缀
        for fast in range(2, len(nums)):
            if nums[fast] != nums[slow - 2]:  # 守门员 = 前缀倒数第 2 个已保留元素
                nums[slow] = nums[fast]       # 和它不同才安全；相同则写入会成为第 3 个
                slow += 1
        return slow


if __name__ == "__main__":
    s = Solution()

    def run(nums):
        n = nums[:]
        k = s.removeDuplicates(n)
        return k, n[:k]

    assert run([1, 1, 1, 2, 2, 3]) == (5, [1, 1, 2, 2, 3])            # 官方示例 1
    assert run([0, 0, 1, 1, 1, 1, 2, 3, 3]) == (7, [0, 0, 1, 1, 2, 3, 3])  # 官方示例 2
    assert run([]) == (0, [])                                         # 空数组
    assert run([1]) == (1, [1])                                       # 单元素（早退救的边界）
    assert run([1, 1]) == (2, [1, 1])                                 # 两个元素
    assert run([1, 1, 1, 1]) == (2, [1, 1])                           # 全部重复
    assert run([1, 2, 3]) == (3, [1, 2, 3])                           # 无重复
    assert run([-1, -1, -1, 2]) == (3, [-1, -1, 2])                   # 负数
    assert run([1, 1, 2, 2]) == (4, [1, 1, 2, 2])                     # 恰好各两个
    print("全部用例通过 ✓")


# 思路拆解
# - 守门员机制：nums[slow-2] 是结果前缀里倒数第 2 个已保留元素。数组有序，
#   若 fast 的值和它相同，说明该值已在前缀里出现 2 次，再写入就是第 3 个 → 跳过；
#   不同 → 安全放行。守门员只挡「当前这个值会不会变成第 3 个」，互不误伤。
# - 和 26 题只差一个下标：26 的守门员是 nums[slow]（倒数第 1 个，每值留 1 个），
#   80 的是 nums[slow-2]（倒数第 2 个，每值留 2 个）。
# - 一般化：每值最多保留 k 个 → slow 从 k 起步、守门员 nums[slow-k]，见 solution_v2.py。
#
# 踩坑记录
# 1. 第一版提交（copilot 提示后自己落地的）漏了 len(nums) < 2 的边界：
#    slow=2 硬起步，输入 [1] 会返回 2。力扣测试用例恰好没放长度 1~2 的坑，
#    176/176 也照样过——「通过了」不等于「没 bug」。补上
#    if len(nums) <= 2: return len(nums) 早退后重交才真正无死角。
#    早退写法比 return min(slow, len(nums)) 更直白：长度 ≤ 2 时每个值天然不超限。
# 2. 硬起步的 slow=k 前提是「前 k 个必然合法」，这个前提只在 len >= k 时成立，
#    写这类模板先问自己一句：数组比 k 还短怎么办？
