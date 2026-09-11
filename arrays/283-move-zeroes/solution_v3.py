# LeetCode 283. 移动零（简单）
# 套路：双指针（交换版）—— j 是非零区右边界，O(n) 时间 / O(1) 空间
# 2026-09-11
# 最优代码
from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        j = 0                                  # 循环不变量：nums[:j] 始终全是非零元素
        for i in range(len(nums)):             # i：扫描指针，一路向右不回头
            if nums[i] == 0:
                continue                       # 0 不用管，留给后面的 swap 清走
            nums[i], nums[j] = nums[j], nums[i]  # 把非零元素放到 nums[j]，原地的 0 被换到右边
            j += 1                             # 非零区右扩一格


if __name__ == "__main__":
    s = Solution()

    def run(nums):
        n = nums[:]
        s.moveZeroes(n)
        return n

    assert run([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]      # 官方示例 1
    assert run([0]) == [0]                                 # 官方示例 2
    assert run([1]) == [1]                                 # 没有 0
    assert run([]) == []                                   # 空列表
    assert run([0, 0, 0]) == [0, 0, 0]                     # 全是 0
    assert run([1, 0, 1]) == [1, 1, 0]                     # 中间夹 0
    assert run([-1, 0, 2, -3, 0]) == [-1, 2, -3, 0, 0]     # 负数也适用
    assert run([2, 1, 0, 3, 12]) == [2, 1, 3, 12, 0]       # 顺序敏感用例：sort 版就死在这
    assert run([1, 0, 0, 0, 2]) == [1, 2, 0, 0, 0]         # 连续多个 0
    print("全部用例通过 ✓")


# 思路拆解
# - j 的含义不是「下一个 0」，而是「下一个非零元素应该落的位置」。
#   这两个指针的分工是单向的：i 负责往前扫，j 负责接收。
# - 为什么不等式/相对顺序天然保持？非零元素是按原顺序被依次搬到下标 0,1,2... 的，
#   搬的过程只做交换，不存在任何跳跃或重排。
# - i == j 时会发生 nums[i], nums[j] = nums[j], nums[i]，也就是自己跟自己换，
#   无副作用，所以不用额外判断。
#
# 踩坑记录
# 1. 同一件事还有种「覆盖法」写法：先遍历把非零元素依次写到 nums[j] 并 j+=1，
#    再把 nums[j:] 整段赋值为 0。它是两次遍历，且全零时会有多余的覆盖，
#    交换法只一趟，是这题的最优答案。
# 2. 千万别为了「看起来整齐」先 sort（见 solution_v2.py），顺序会被排坏，直接 WA。
# 3. 也别用 remove 反复删（见 solution_v1.py），那是 O(n²)，容易超时。
# 4. 通用范式：数组原地整理类题目（去重、移除指定元素、按奇偶分区）
#    第一反应都该是「快慢双指针」，而不是额外的辅助数组。
