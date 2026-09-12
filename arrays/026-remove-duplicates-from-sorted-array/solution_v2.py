# LeetCode 26. 删除有序数组中的重复项（简单）
# 套路：快慢双指针，slow = 已去重前缀的末尾，O(n) 时间 / O(1) 空间
# 2026-09-12
# 最优代码
from typing import List


class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        """
        :param nums: 非严格递增排列的数组（原地删除重复元素）
        :return k: 去重后数组的长度，nums 前 k 位为去重结果
        """
        slow = 0                                 # 循环不变量：nums[0..slow] 是已去重的有序前缀
        for fast in range(1, len(nums)):         # fast 一路向右，负责发现新值
            if nums[fast] != nums[slow]:         # 和前缀「最后一个值」不同 → 是新值
                slow += 1                        # 先把前缀扩一格（顺序不能反）
                nums[slow] = nums[fast]          # 再把新值写进前缀末尾
        return slow + 1 if nums else 0           # 长度 = 末尾下标 + 1，空数组单独处理


if __name__ == "__main__":
    s = Solution()

    def run(nums):
        n = nums[:]
        k = s.removeDuplicates(n)
        return k, n[:k]

    assert run([1, 1, 2]) == (2, [1, 2])                                  # 官方示例 1
    assert run([0, 0, 1, 1, 1, 2, 2, 3, 3, 4]) == (5, [0, 1, 2, 3, 4])    # 官方示例 2
    assert run([]) == (0, [])                                             # 空数组
    assert run([1]) == (1, [1])                                           # 单元素
    assert run([1, 1, 1, 1]) == (1, [1])                                  # 全部重复
    assert run([1, 2, 3]) == (3, [1, 2, 3])                               # 没有重复
    assert run([-3, -1, -1, 0, 0, 2]) == (4, [-3, -1, 0, 2])              # 负数也适用
    assert run([0, 0, 0, 1]) == (2, [0, 1])                               # 重复集中在开头
    print("全部用例通过 ✓")


# 思路拆解
# - 为什么只跟 nums[slow] 比就够了？数组有序，重复值必然相邻；
#   nums[slow] 是已收进前缀的最后一个值，fast 遇到的新值只要跟它不同，
#   就说明整个前缀里都没出现过——这是这题能用双指针的根本前提。
#   换成一个无序数组，这套写法立刻失效，得上 set。
# - 为什么先 slow += 1 再写入？slow 当前位置存放的是「刚收进来的最后一个新值」，
#   新值要放在它后面；反着写会把自己刚收到的值覆盖掉。
# - 尾部残留不用管：[0,1,2,1,2] 返回 3 就是正确答案，判题器只看前 k 位。
#   所以这题不需要真的「删除」元素，覆盖写就够了，这也是 O(1) 空间的来源。
#
# 踩坑记录
# 1. 我第一版（见 solution_v1.py）踩了三个坑：range(len(nums)) 里访问 nums[i+1] 越界；
#    数组递增导致 nums[i] > nums[i+1] 恒假；以及最要命的——只 return len(set(nums))，
#    数量对了但数组没改，判题器照样判错。
# 2. 【通用范式】「原地整理数组」类题目（283 移动零、26 删重复项、27 移除元素、
#    80 删重复项 II）第一反应都该是快慢双指针，而不是额外的辅助数组或 set。
#    283 与 26 的区别只在于写入方式：283 用交换、26 用先移后写。
# 3. 写「和相邻元素比较」的循环时，先想清楚边界：要么 range(1, n) 跟前面比，
#    要么 range(n - 1) 跟后面比，别写成 range(n) 再取 i+1。
