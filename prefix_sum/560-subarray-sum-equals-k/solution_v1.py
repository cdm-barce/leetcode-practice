# LeetCode 560. 和为 K 的子数组（中等）
# 套路：前缀和 + 哈希表计数，O(n) 时间 / O(n) 空间
# 2026-10-08
# 最优代码

from collections import defaultdict


class Solution:
    def subarraySum(self, nums, k):
        # cnt 记录「每个前缀和值出现了几次」
        cnt = defaultdict(int)
        cnt[0] = 1          # 关键：空前缀和，让「从下标 0 开始就凑出 k」的子数组能命中
        pre = 0             # 走到当前下标为止的前缀和
        ans = 0
        for x in nums:
            pre += x                          # 先累加当前元素，得到 pre[j]
            ans += cnt[pre - k]               # 先查：之前有多少个前缀和等于 pre-k，累加
            cnt[pre] += 1                     # 再记录当前前缀和（顺序不能反，避免算进自己）
        return ans


if __name__ == "__main__":
    s = Solution()
    # 官方用例
    assert s.subarraySum([1, 1, 1], 2) == 2
    assert s.subarraySum([1, 2, 3], 3) == 2
    # 边界用例：负数、0、单元素、整个数组恰好为 k
    assert s.subarraySum([1, -1, 0], 0) == 3       # [1,-1]、[0]、[1,-1,0] 三个
    assert s.subarraySum([1], 0) == 0
    assert s.subarraySum([-1, -1, 1], 0) == 1
    assert s.subarraySum([0, 0, 0], 0) == 6        # C(4,2)=6 个子数组
    print("全部用例通过 ✓")


# 踩坑记录：
# 1. 数组含负数时，前缀和不再单调递增，滑动窗口/双指针的「total > k 就缩左端」判断失效，
#    必须换成「前缀和 + 哈希表」：把子数组和转成 pre[j] - pre[i-1] == k，即找 pre[i-1] == pre[j] - k。
# 2. 初始化 cnt[0] = 1 不能省：否则从数组开头就凑出 k 的子数组（如 [1,2,3], k=3 里的 [1,2]）会被漏掉。
# 3. 顺序不能反：必须先查 cnt[pre-k] 再更新 cnt[pre]，否则会把「当前元素自己」或空子数组错误计入。
