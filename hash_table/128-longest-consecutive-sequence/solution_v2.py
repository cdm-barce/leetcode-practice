# LeetCode 128. 最长连续序列（中等）
# 套路：排序 + 去重后扫描最长连续段，O(n log n) 时间 / O(n) 空间
# 2026-09-10
# 对照解法（不满足题目 O(n) 要求，但思路直白，可作兜底）
# 思路：排序后连续的数字会挨在一起，扫描时比较相邻元素差是否为 1；
#       用 set 去重，避免 [1,1,1] 这类重复元素把长度算错
class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        if not nums:
            return 0
        sorted_nums = sorted(set(nums))     # 去重 + 排序
        longest = 1
        length = 1
        for i in range(1, len(sorted_nums)):
            if sorted_nums[i] == sorted_nums[i - 1] + 1:   # 和第 1 个元素相连
                length += 1
            else:                                          # 断开了，重新起算
                longest = max(longest, length)
                length = 1
        return max(longest, length)         # 别忘了最后一段还没比较过


if __name__ == "__main__":
    s = Solution()
    assert s.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([]) == 0
    assert s.longestConsecutive([1]) == 1
    assert s.longestConsecutive([1, 1, 1]) == 1
    print("全部用例通过 ✓")

# 踩坑记录：
# 1. 循环结束后必须再 max 一次：最长的一段可能一直延续到数组末尾，
#    此时循环里从没触发过 else 分支去更新 longest
# 2. sorted(set(nums)) 里的 set 不能省：重复元素会让 sorted_nums[i] 和
#    前一个相等，差为 0 而不是 1，逻辑上虽会被 else 处理但容易写错
# 3. 面试取舍：这版更好写、更不容易错，但复杂度 O(n log n)，
#    题目明确要求 O(n) 时会被追问，所以主力答案是 v1 的哈希集合版
