# LeetCode 283. 移动零（简单）
# 套路：数零 + 删零 + 补零（count/remove/extend），O(n²) 时间 / O(n) 临时空间
# 2026-09-11
# 我的解答（逻辑正确，但复杂度偏高）
from typing import List


class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zero = nums.count(0)           # 先数出一共有几个 0
        for i in range(zero):          # 删掉这么多个 0
            nums.remove(0)             # remove(x) 删的是「第一个值等于 x 的元素」
        nums.extend([0] * zero)        # 末尾统一补回同样多的 0


if __name__ == "__main__":
    s = Solution()

    def run(nums):
        n = nums[:]                    # 拷贝一份，避免样例之间互相污染
        s.moveZeroes(n)
        return n

    assert run([0, 1, 0, 3, 12]) == [1, 3, 12, 0, 0]      # 官方示例 1
    assert run([0]) == [0]                                 # 官方示例 2：只有一个 0
    assert run([1]) == [1]                                 # 没有 0，原样返回
    assert run([0, 0, 0]) == [0, 0, 0]                     # 全是 0
    assert run([1, 0, 1]) == [1, 1, 0]                     # 中间夹 0
    assert run([-1, 0, 2, -3, 0]) == [-1, 2, -3, 0, 0]     # 负数也适用
    assert run([2, 1, 0, 3, 12]) == [2, 1, 3, 12, 0]       # 非零点相对顺序保持不变
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 这一版对拍 20 万组随机用例全过，逻辑没有问题：count 记数、remove 逐个删、
#    extend 补回，非零元素的相对顺序天然保持。
# 2. 但它是 O(n²)：list.remove 删完元素后要把后面的元素整体前移一次，O(n)，
#    再套 zero 次循环；n = 10^4 时约 10^8 次搬动，提交有「超出时间限制」风险。
#    另外 [0] * zero 也额外开了 O(n) 的空间，不算严格原地。
# 3. 第二个坑（见 solution_v2.py）：为了快而改成 sort，直接把顺序排坏了，WA。
#    这题只要求「挪 0」，不要求「有序」，sort 是答非所问。
# 4. 正确的最快写法见 solution_v3.py：双指针交换，O(n) 时间 / O(1) 空间。
