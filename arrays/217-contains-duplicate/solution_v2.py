# LeetCode 217. 存在重复元素（简单）
# 套路：哈希集合，空间换时间，O(n)
# 2026-09-07
# 提交结果：通过，21 ms / 31.6 MB
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()
        for x in nums:
            if x in seen:       # set 底层是哈希表，in 平均 O(1)
                return True     # 发现重复立刻返回，不必扫完整个数组
            seen.add(x)
        return False


if __name__ == "__main__":
    s = Solution()
    assert s.containsDuplicate([1, 2, 3, 1]) is True
    assert s.containsDuplicate([1, 2, 3, 4]) is False
    assert s.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("全部用例通过 ✓")


# 踩坑记录
# 1. 最初写的结尾是 `return len(num) < len(nums)`，多余。
#    for 循环里一旦发现重复就 return True，能走到最后说明所有元素都不同，
#    直接 return False 即可，那行长度比较永远不会为 True。
# 2. 别写成 `if ...: return True else: ...`，return 之后的分支不会执行，
#    省掉 else 更清爽（v1 里就犯了这个）。
# 3. 复杂度：时间 O(n)，空间 O(n)。用哈希表的空间换取查找从 O(n) 到 O(1) 的提速，
#    这是「空间换时间」最典型的一道题。
