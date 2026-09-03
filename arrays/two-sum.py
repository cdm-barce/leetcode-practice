# LeetCode 1. 两数之和（简单）
# 套路：哈希表，空间换时间，O(n)
# 2026-09-03
# 最优代码
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []

# 我的解答
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []   # 没找到就返回空数组（题目保证有解，这行其实走不到）




