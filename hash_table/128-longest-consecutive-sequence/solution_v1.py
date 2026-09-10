# LeetCode 128. 最长连续序列（中等）
# 套路：哈希集合 + 只从序列起点扩张，O(n) 时间 / O(n) 空间
# 2026-09-10
# 我的解答（最终通过版）
# 思路：把所有数丢进 set（O(1) 查存在 + 天然去重），
#       只从"序列起点"开始往后数，避免每个数都被重复遍历
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        num_set = set(nums)          # 去重 + O(1) 成员查询
        longest = 0                  # 空数组时自然返回 0，无需特判
        for x in num_set:            # 遍历 set 而非 nums：重复元素只算一次
            if x - 1 in num_set:     # 关键剪枝：x 不是序列起点，跳过
                continue
            length = 1
            while x + length in num_set:   # x 是起点，往后一直数 x+1, x+2...
                length += 1
            longest = max(longest, length)
        return longest


if __name__ == "__main__":
    s = Solution()
    assert s.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([]) == 0                  # 边界：空数组
    assert s.longestConsecutive([1]) == 1                 # 边界：单元素
    assert s.longestConsecutive([1, 1, 1]) == 1           # 边界：全重复
    assert s.longestConsecutive([-2, -1, 0, 1]) == 4      # 负数也适用
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 初版用 length_list 收集每段长度、最后 max(length_list)：
#    空数组时 length_list == []，max([]) 抛
#    ValueError: max() iterable argument is empty
#    -> 修法：改用标量 longest 边走边刷新（本文件写法），空数组天然返回 0；
#       或 max(length_list, default=0)
# 2. 改成标量版后遇到 UnboundLocalError: cannot access local variable 'longest'
#    根因是初始化那行 `longest = 0` 赋值的不是 ASCII 的 longest（中文输入法
#    容易混入形近的全角/Unicode 字符），Python 视为另一个变量名
#    -> 教训：报 UnboundLocalError 时先查同名变量的拼写与输入法
# 3. 复杂度：外层遍历 O(n)，内层 while 只在起点触发，每个元素最多被访问两次
#    -> 整体 O(n)，而不是看起来的 O(n²)
# 相关题目：217. 存在重复元素（set 判重）、1. 两数之和（哈希表查配对）
