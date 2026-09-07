# LeetCode 217. 存在重复元素（简单）
# 套路：一行解，set 自动去重后比长度，O(n)
# 2026-09-07
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) != len(nums)


if __name__ == "__main__":
    s = Solution()
    assert s.containsDuplicate([1, 2, 3, 1]) is True
    assert s.containsDuplicate([1, 2, 3, 4]) is False
    assert s.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("全部用例通过 ✓")


# 说明
# 1. 原理：set 会去重，去重后长度比原数组短就说明有重复。时间复杂度同样是 O(n)。
# 2. 与 v2 的取舍：这行写起来最快，适合笔试抢时间；但它会先把整个数组转成 set，
#    哪怕第 1 个和第 2 个元素就重复也要扫完。v2 的提前返回在真实数据上更快。
#    面试时建议先讲 v2 的思路，再补一句「还有个一行写法」。
# 3. 同类题要能举一反三：
#    - 219 存在重复元素 II（要求下标差不超过 k，用滑动窗口 + set）
#    - 220 存在重复元素 III（用有序集合 / 桶排序）
