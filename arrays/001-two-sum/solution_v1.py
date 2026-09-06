# LeetCode 1. 两数之和（简单）
# 套路：暴力 O(n²)
# 2026-09-03
# 我的解答
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []   # 没找到就返回空数组（题目保证有解，这行其实走不到）




if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    assert s.twoSum([3, 3], 6) == [0, 1]
    print("全部用例通过 ✓")
