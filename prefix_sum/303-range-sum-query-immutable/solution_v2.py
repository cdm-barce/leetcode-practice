# LeetCode 303. 区域和检索 - 数组不可变（简单）
# 套路：前缀和，O(n) 预处理 / O(1) 查询，O(n) 空间
# 2026-10-07
# 最优代码

from typing import List


class NumArray:
    def __init__(self, nums: List[int]):
        # prefix[i] = nums 前 i 个数的和（prefix[0] = 0 作边界占位）
        # 开 n+1 位，让 sumRange(0, right) 不用特判 left=0 的情况
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        # 区间和 = 前 right+1 个的和 − 前 left 个的和
        # 类比：第 5 名到第 10 名总分 = 前 10 名总分 − 前 4 名总分
        return self.prefix[right + 1] - self.prefix[left]


if __name__ == "__main__":
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sumRange(0, 2) == 1
    assert na.sumRange(2, 5) == -1
    assert na.sumRange(0, 5) == -3
    # 边界用例
    assert NumArray([1]).sumRange(0, 0) == 1         # 单元素
    assert NumArray([-1]).sumRange(0, 0) == -1       # 单元素负数
    na2 = NumArray([5, 5, 5, 5])
    assert na2.sumRange(0, 3) == 20                   # 全区间
    assert na2.sumRange(1, 1) == 5                    # left == right 单点
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. prefix 数组开 n+1 位而非 n 位：prefix[0] 故意留 0，这样 sumRange(0, right) = prefix[right+1] - prefix[0]
#    无需特判 left==0，公式统一。
# 2. self.prefix 必须是实例属性（self. 前缀），否则只是 __init__ 的局部变量，函数结束即丢，
#    sumRange 里就拿不到了。
# 3. [0] * (n+1) 对不可变 int 安全；若是可变对象（list/dict）会复制出同一引用，注意区分。
# 4. 学到的点：前缀和是「多次区间查询」的通用套路，560（和为 K 的子数组）、304（二维区域和）都是它的变体。
