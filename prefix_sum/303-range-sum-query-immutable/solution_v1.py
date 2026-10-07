# LeetCode 303. 区域和检索 - 数组不可变（简单）
# 套路：每次 sumRange 现场切片求和，O(n) 查询 / O(n) 空间
# 2026-10-07
# 我的解答（能 AC，但查询 O(n)，731ms 只击败 20%，见末尾踩坑记录）

from typing import List


class NumArray:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def sumRange(self, left: int, right: int) -> int:
        if len(self.nums) == 0:
            return
        # 切片会额外复制整个区间，再加 sum 求和，等于双重浪费
        return sum(self.nums[left: right + 1])


if __name__ == "__main__":
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1
    assert na.sumRange(0, 5) == -3
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 查询复杂度 O(n)：sumRange 每次现场 sum(nums[left:right+1])，反复调用会 O(n) 重算。
#    实测 731ms / 20.85%，是本题唯一的性能瓶颈。
# 2. 切片 self.nums[left:right+1] 除了求和，还会复制整个区间，时间内存双重浪费。
# 3. `if len(self.nums) == 0: return` 是多余且有害的：LeetCode 约束 1 <= nums.length 永远非空；
#    且 return 返回 None 当作 int 使用本身就是隐患。
# 4. 学到的点：涉及「多次区间查询」时，考虑在 __init__ 做一次预处理（前缀和），把每次查询降到 O(1)。
