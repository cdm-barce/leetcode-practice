# LeetCode 239. 滑动窗口最大值（困难）
# 套路：暴力 max(win) 每次全量重算，O(n·k) 时间 / O(1) 空间
# 2026-09-30
# 我的解答

from typing import List


class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans = []
        n = len(nums)
        for i in range(n - k + 1):
            # 每次都对整个窗口 [i, i+k) 重新求最大值，上一个窗口的结果完全没用上
            ans.append(max(nums[i:i + k]))
        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert s.maxSlidingWindow([1], 1) == [1]
    assert s.maxSlidingWindow([1, -1], 1) == [1, -1]
    print("暴力版用例通过 ✓")

# 踩坑记录：
# - 这版逻辑正确（两个小用例都能过），但一提交大用例就 TLE。
#   根因：每滑一格都 max(nums[i:i+k]) 全量重算，O(n·k)；n、k 最大 10^5，
#   最坏 10^10 次操作，必超时。
# - 核心浪费：窗口每次只动一格（进一个 nums[R]、出一个 nums[L]），
#   但旧窗口的计算结果一点没用上，重复扫描了整个窗口。
# - 正解见 solution_v2.py：单调队列 O(n)，每个元素最多入队/出队一次，
#   均摊每格 O(1)。
