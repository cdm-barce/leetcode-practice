# LeetCode 300. 最长递增子序列（中等）
# 套路：贪心 + 二分，tails[k] = 长度为 k+1 的递增子序列的最小结尾，O(n log n) 时间 / O(n) 空间
# 2026-11-15
# 最优代码（v2，由 O(n²) DP 优化而来）


from typing import List


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        :param nums: 整数数组
        :return: 最长严格递增子序列的长度

        核心思路：不再问「以 i 结尾能有多长」，改问
        「长度为 k+1 的递增子序列，结尾最小能是多少」，记在 tails[k] 里。

        为什么这样可以：结尾越小，后面能接上的数就越多。
        所以同一长度下，只需要保留「结尾最小」的那一个候选，
        其余候选全部是劣汰的，可以直接丢弃。

        三条不变量（很关键）：
          ① tails 始终严格递增
          ② len(tails) 就是「当前已见过的元素」能构成的最大长度
          ③ tails 本身不是答案序列，只有长度是对的
             （例：[10,9,2,5,3,7] 结束时 tails=[2,3,7]，但真实 LIS 是 [2,5,7] 或 [2,3,7]）
        """
        tails = []

        for x in nums:
            # 规则 A：x 比当前所有结尾都大 → 可以接在最长的序列后面，长度 +1
            if not tails or x > tails[-1]:
                tails.append(x)
            # 规则 B：x 不是最大的 → 找到「第一个 >= x 的位置」替换掉
            # 这样做有两个效果：长度不变，但该长度的结尾从大值变成小值（更优）
            # 注意不能直接替换末尾：若 x 比中间某元素还小，替换末尾会破坏 tails 的递增性
            else:
                left, right = 0, len(tails) - 1
                while left < right:
                    mid = (left + right) // 2
                    if tails[mid] < x:
                        left = mid + 1        # 中间值比 x 小，答案在右半区
                    else:
                        right = mid           # 中间值 >= x，它可能就是答案，也可能更左
                # 循环退出时 left == right，即「第一个 >= x 的位置」
                tails[left] = x

        return len(tails)


if __name__ == "__main__":
    s = Solution()

    # 官方示例
    assert s.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert s.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4
    assert s.lengthOfLIS([7, 7, 7, 7, 7, 7, 7, 7, 7]) == 1

    # 边界
    assert s.lengthOfLIS([1]) == 1
    assert s.lengthOfLIS([2, 2]) == 1, "严格递增：相等的数不能接上"
    assert s.lengthOfLIS([1, 2, 3, 4, 5]) == 5
    assert s.lengthOfLIS([5, 4, 3, 2, 1]) == 1
    assert s.lengthOfLIS([1, 2, 3, 0]) == 3

    # 反例：从全局最小值出发的贪心会错
    assert s.lengthOfLIS([4, 5, 1, 2, 3, 0, 6]) == 4

    # 关键：验证「>= 而非 >」——若二分找的是第一个 > x 的位置，
    # 遇到相等的数会 append 而不是替换，长度会虚增
    assert s.lengthOfLIS([2, 2, 2]) == 1
    assert s.lengthOfLIS([1, 1, 1, 2]) == 2

    # ---------- 与 v1（O(n²) DP）随机对拍 ----------
    def lis_v1(nums):
        n = len(nums)
        if n == 0:
            return 0
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    import random
    random.seed(300)
    for _ in range(3000):
        k = random.randint(1, 30)
        arr = [random.randint(-50, 50) for _ in range(k)]
        assert s.lengthOfLIS(arr) == lis_v1(arr), f"两版不一致：{arr}"

    # ---------- 与暴力枚举对拍（保证独立正确性） ----------
    def brute(nums):
        n = len(nums)
        best = 0
        for mask in range(1 << n):
            seq = [nums[i] for i in range(n) if mask >> i & 1]
            if all(seq[k] < seq[k + 1] for k in range(len(seq) - 1)):
                best = max(best, len(seq))
        return best

    for _ in range(600):
        k = random.randint(1, 10)
        arr = [random.randint(-20, 20) for _ in range(k)]
        assert s.lengthOfLIS(arr) == brute(arr), f"与暴力解不一致：{arr}"

    # ---------- 手推一遍 tails 的演变，确认代码行为和纸上一致 ----------
    tails = []
    for x in [10, 9, 2, 5, 3]:
        if not tails or x > tails[-1]:
            tails.append(x)
        else:
            left, right = 0, len(tails) - 1
            while left < right:
                mid = (left + right) // 2
                if tails[mid] < x:
                    left = mid + 1
                else:
                    right = mid
            tails[left] = x
    assert tails == [2, 3], f"tails 演变不对：{tails}"

    print("全部用例通过 ✓（含 3000 组 v1 对拍 + 600 组暴力对拍）")


# 踩坑记录
# 1. 【贪心规则的边界】最初以为「x 比末尾小，那就直接替换末尾」，这在 x 只比末尾小、
#    但比倒数第二个大时是对的（如 tails=[2,5,7]，x=6）；一旦 x 更小就崩：
#    tails=[2,5,7]，x=3，替换末尾得 [2,5,3] —— 数组不再递增，后续二分全部失效。
#    正确做法是「找第一个 >= x 的位置」，得到 [2,3,7]，替换后仍然有序。
#    本质：不是把 x 丢到末尾，而是把它插到它该在的位置。
# 2. 【为什么必须保持有序】tails 的有序性是二分的唯一前提。
#    而且 tails 递增本身就是其定义的推论：若长度 k+1 的结尾比长度 k 的还小，
#    那删掉后面几个元素就能得到一个长度 k、结尾更小的序列，与「最小结尾」矛盾。
# 3. 【>= 而不是 >】二分里判 tails[mid] < x 才往右走，等价于找「第一个 >= x 的位置」。
#    若改成 tails[mid] <= x 往右走（即找第一个 > x），遇到相等的数就会 append，
#    长度虚增。用 [2,2,2] 可测：正确是 1，写错会得 3。
#    （对应 Python 内置：bisect_left = 第一个 >= x，bisect_right = 第一个 > x。
#      这题要 bisect_left，所以可以写成：
#          import bisect; tails[bisect.bisect_left(tails, x)] = x
#      手写二分是为了把边界逻辑练清楚，生产环境直接用 bisect 更快更稳。）
# 4. 【tails 不是答案序列】这是最容易误解的一点。tails 只保证「长度」正确，
#    数组里装的是「每种长度的最小结尾」，并不是某一条真实的 LIS。
#    例 [10,9,2,5,3,7] 结束时 tails=[2,3,7]，但 2 和 3 在原数组里的相对关系
#    并不能拼出一条真实序列。如果题目要求「返回具体序列」，这题方法不能用，
#    需要换成记录前驱 + 从最大 dp 值回溯。
# 5. 【为什么不用对每个起点都贪心】也想过「对每个元素，在它右边反复找
#    『大于它的最小值』接上去，取最长」。这在逻辑上能得到正确答案，
#    但每个起点都要重扫一遍右边，总复杂度仍是 O(n²)，等于没优化
#    （而且实现比 DP 更复杂）。tails 的价值在于把「所有起点的信息」
#    压缩成「每种长度的最优结尾」，一次遍历通吃。
# 6. 【复杂度来源】外层 n 次，内层二分 log(len(tails)) ≤ log n，合计 O(n log n)。
#    对比 v1 的 O(n²)：n=2500 时约 2.8 万次 vs 625 万次操作，实测从 1274ms 降到几十 ms。
# 7. 【变体】若题目改为「非递减子序列」（允许相等），
#    判断要改成 x >= tails[-1]（规则 A）和 tails[mid] <= x 往右走（规则 B），
#    即整体换成 bisect_right。一个符号决定题目对不对。
