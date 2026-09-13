# LeetCode 27. 移除元素（中等）
# 套路：首尾对撞双指针，O(n) 时间 / O(1) 空间，要删的元素少时搬动次数更少
# 2026-09-13
# 最优代码（官方解法二，顺序不保持的变体）

from typing import List


class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        """
        :param nums: 原地移除所有等于 val 的元素，27 题允许结果顺序任意
        :return k: 保留元素个数，nums 前 k 位为保留结果
        """
        left, right = 0, len(nums)            # [left, right) 是待处理区间
        while left < right:
            if nums[left] == val:             # 该删：把尾部元素拉过来覆盖它
                nums[left] = nums[right - 1]
                right -= 1                    # 尾部收缩一格，被拉走的元素视作丢弃
                # 注意 left 不动：拉过来的这个元素还没检查，下一轮继续看它
            else:
                left += 1                     # 该留：left 右移
        return left                           # left == right 时区间清空，left 即保留个数


if __name__ == "__main__":
    s = Solution()

    def run(nums, val):
        n = nums[:]
        k = s.removeElement(n, val)
        return k, sorted(n[:k])               # 对撞法不保持顺序，比较前先排序

    assert run([3, 2, 2, 3], 3) == (2, [2, 2])                        # 官方示例 1
    assert run([0, 1, 2, 2, 3, 0, 4, 2], 2) == (5, [0, 0, 1, 3, 4])   # 官方示例 2（顺序变了）
    assert run([], 0) == (0, [])
    assert run([1], 1) == (0, [])
    assert run([2], 3) == (1, [2])
    assert run([3, 3, 3], 3) == (0, [])
    assert run([4, 5], 4) == (1, [5])
    assert run([-1, -2, -3], -2) == (2, sorted([-1, -3]))
    print("全部用例通过 ✓")


# 思路拆解
# - 核心思路：遇到要删的元素，不搬后面一大段，只从尾部拉一个过来顶替，right 收缩。
#   每一步要么 left 前进、要么 right 后退，区间每轮必缩一格，循环必然终止。
# - 何时比覆盖法（v1）好？val 占比很低时，覆盖法每个非零都要搬一次，
#   对撞法只有「撞上 val」才搬，搬动次数 = val 的个数。
# - 代价：顺序被打乱（27 题允许；283 那种要求尾部补 0 的题不能用这招想当然）。
#
# 踩坑记录
# 1. 拉完尾部元素后 left 不能动——拉过来的是个没检查过的新元素，动了会漏判。
# 2. right 初始是 len(nums)（开区间），取尾部元素要写 nums[right - 1]，
#    直接 nums[right] 会在第一轮就越界。
